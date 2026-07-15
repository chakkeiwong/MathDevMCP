from __future__ import annotations

"""Bounded recursive expansion of derivation trees with agent hypotheses."""

from dataclasses import asdict, dataclass
from typing import Any

from .agent_hypothesis_expansion import (
    AGENT_HYPOTHESIS_EXPANSION_CONTRACT,
    hypothesis_generator_provenance,
    propose_hypothesis_expansions,
    validate_agent_hypothesis_expansion,
)
from .contracts import attach_contract
from .backend_formalization_target import build_backend_formalization_target
from .derivation_search_tree import (
    AssumptionSet,
    BlockerNode,
    DerivationStep,
    summarize_search_tree,
    validate_search_tree,
)


DERIVATION_TREE_EXPANSION_CONTRACT = "derivation_tree_expansion_result"
DERIVATION_TREE_EXPANSION_BOUNDARY = (
    "Tree expansion records candidate child nodes from validated agent "
    "hypotheses. It is not backend certification, proof search completeness, "
    "or a repair proposal."
)


@dataclass(frozen=True)
class TreeExpansionBudget:
    max_depth: int = 1
    max_nodes: int = 3
    max_agent_expansions_per_blocker: int = 2
    max_backend_attempts: int = 0
    timeout_seconds: float | None = None


def _as_int(value: Any, default: int) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def _budget_dict(budget: TreeExpansionBudget | dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(budget, TreeExpansionBudget):
        payload = asdict(budget)
    elif isinstance(budget, dict):
        payload = dict(budget)
    else:
        payload = asdict(TreeExpansionBudget())
    payload["max_depth"] = _as_int(payload.get("max_depth"), 1)
    payload["max_nodes"] = _as_int(payload.get("max_nodes"), 3)
    payload["max_agent_expansions_per_blocker"] = _as_int(payload.get("max_agent_expansions_per_blocker"), 2)
    payload["max_backend_attempts"] = _as_int(payload.get("max_backend_attempts"), 0)
    return payload


def _walk_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = [node]
    children = node.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                nodes.extend(_walk_nodes(child))
    return nodes


def _open_blockers(root: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for node in _walk_nodes(root):
        if node.get("status") in {"proved", "refuted"}:
            continue
        blockers = node.get("blockers", [])
        if not isinstance(blockers, list):
            continue
        for blocker in blockers:
            if isinstance(blocker, dict):
                pairs.append((node, blocker))
    return pairs


def _external_plan_from_parent(parent: dict[str, Any]) -> dict[str, Any]:
    plan = parent.get("external_tool_first_plan")
    return dict(plan) if isinstance(plan, dict) else {}


def _source_context_from_node(parent: dict[str, Any]) -> dict[str, Any]:
    span = parent.get("source_span") if isinstance(parent.get("source_span"), dict) else {}
    return {
        "id": parent.get("id"),
        "label": span.get("label"),
        "location": " > ".join(str(item) for item in (span.get("file"), span.get("label")) if item),
    }


def _child_from_hypothesis(
    parent: dict[str, Any],
    blocker: dict[str, Any],
    hypothesis: dict[str, Any],
) -> dict[str, Any]:
    generator = hypothesis_generator_provenance(hypothesis)
    generator_label = "agent" if generator["kind"] == "agent_generated" else "rule"
    assumptions = [
        asdict(
            AssumptionSet(
                id=f"assumption_{hypothesis['id']}_{index}",
                assumptions=[str(assumption)],
                status=f"{generator_label}_hypothesis_pending_verification",
                source=f"{generator_label}_hypothesis_expansion",
                closes=[str(blocker.get("id", ""))],
                evidence_refs=[str(hypothesis.get("id", ""))],
            )
        )
        for index, assumption in enumerate(hypothesis.get("assumptions_added", []), start=1)
        if str(assumption).strip()
    ]
    blockers = [
        asdict(
            BlockerNode(
                id=f"blocker_{hypothesis['id']}_backend_evidence_required",
                kind="backend_evidence_required",
                problem="The candidate hypothesis has not been checked by its expected backend or source-evidence route.",
                why=str(hypothesis.get("success_criterion", "The route still needs validation.")),
                required_next_evidence=(
                    f"Run or prepare `{hypothesis.get('expected_backend')}` evidence for "
                    f"`{hypothesis.get('expected_backend_role')}`."
                ),
                source="derivation_tree_expansion",
                evidence_refs=[str(hypothesis.get("id", "")), str(blocker.get("id", ""))],
            )
        )
    ]
    return {
        "id": f"node_{hypothesis['id']}",
        "target": str(parent.get("target", "")),
        "status": "expanded_by_agent" if generator_label == "agent" else "expanded_by_rule",
        "source_span": dict(parent.get("source_span", {})) if isinstance(parent.get("source_span"), dict) else {},
        "external_tool_first_plan": _external_plan_from_parent(parent),
        "assumptions": assumptions,
        "backend_attempts": [],
        "derivation_steps": [
            asdict(
                DerivationStep(
                    id=f"step_{hypothesis['id']}",
                    claim=str(hypothesis.get("proposed_route", "")),
                    justification=str(hypothesis.get("why_might_close", "")),
                    checker=f"{generator_label}_hypothesis_expansion",
                    checker_status="candidate_pending_tree_verification",
                    evidence_refs=[str(hypothesis.get("id", ""))],
                )
            )
        ],
        "blockers": blockers,
        "patch_candidates": [],
        "children": [],
        "score": 0.0,
        "parent_node_id": parent.get("id"),
        "parent_blocker_id": blocker.get("id"),
        "agent_hypothesis": hypothesis,
        "generator": generator,
        "boundary": DERIVATION_TREE_EXPANSION_BOUNDARY,
    }


def expand_tree_with_hypotheses(
    tree: dict[str, Any],
    *,
    budget: TreeExpansionBudget | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Expand open blockers into validated agent-hypothesis child nodes."""
    budget_payload = _budget_dict(budget)
    root = tree.get("root")
    if not isinstance(root, dict):
        result = {
            "status": "invalid_tree",
            "reason": "Tree root is missing.",
            "budget": budget_payload,
            "expanded_node_count": 0,
            "expanded_blocker_count": 0,
            "budget_exhausted": False,
            "tree": tree,
            "validation_errors": ["root must be a dict"],
            "boundary": DERIVATION_TREE_EXPANSION_BOUNDARY,
        }
        return attach_contract(result, DERIVATION_TREE_EXPANSION_CONTRACT)
    expanded_nodes = 0
    expanded_blockers = 0
    skipped: list[dict[str, Any]] = []
    for parent, blocker in _open_blockers(root):
        if expanded_nodes >= budget_payload["max_nodes"]:
            skipped.append({"blocker_id": blocker.get("id"), "reason": "max_nodes_exhausted"})
            continue
        expansion_set = propose_hypothesis_expansions(
            blocker,
            source_context=_source_context_from_node(parent),
            max_candidates=budget_payload["max_agent_expansions_per_blocker"],
        )
        children = parent.setdefault("children", [])
        added_for_blocker = 0
        for hypothesis in expansion_set.get("candidates", []):
            if expanded_nodes >= budget_payload["max_nodes"]:
                skipped.append({"blocker_id": blocker.get("id"), "reason": "max_nodes_exhausted"})
                break
            if not isinstance(hypothesis, dict):
                continue
            errors = validate_agent_hypothesis_expansion(hypothesis)
            if errors or hypothesis.get("metadata", {}).get("contract") != AGENT_HYPOTHESIS_EXPANSION_CONTRACT:
                skipped.append({"blocker_id": blocker.get("id"), "reason": "invalid_hypothesis", "errors": errors})
                continue
            child = _child_from_hypothesis(parent, blocker, hypothesis)
            formalization_target = build_backend_formalization_target(child)
            child["backend_formalization_targets"] = [formalization_target]
            if formalization_target.get("status") == "backend_ready":
                child["status"] = "backend_ready"
            for target_blocker in formalization_target.get("blockers", []):
                if isinstance(target_blocker, dict):
                    child["blockers"].append(target_blocker)
            children.append(child)
            expanded_nodes += 1
            added_for_blocker += 1
        if added_for_blocker:
            expanded_blockers += 1
        if budget_payload["max_depth"] <= 1 and expanded_nodes >= budget_payload["max_nodes"]:
            continue
    budget_exhausted = bool(skipped)
    tree["summary"] = summarize_search_tree(tree)
    validation_errors = validate_search_tree(tree)
    result = {
        "status": "expanded" if expanded_nodes else "no_expansion",
        "budget": budget_payload,
        "expanded_node_count": expanded_nodes,
        "expanded_blocker_count": expanded_blockers,
        "budget_exhausted": budget_exhausted,
        "skipped": skipped,
        "tree": tree,
        "summary": tree["summary"],
        "validation_errors": validation_errors,
        "boundary": DERIVATION_TREE_EXPANSION_BOUNDARY,
        "non_claims": [
            "Expanded child nodes are candidate paths only.",
            "No backend evidence is created by tree expansion.",
            "Tree expansion is not proof-search completeness.",
        ],
    }
    return attach_contract(result, DERIVATION_TREE_EXPANSION_CONTRACT)
