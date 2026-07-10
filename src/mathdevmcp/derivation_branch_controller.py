from __future__ import annotations

"""Budgeted derivation branch controller over external-tool evidence actions."""

from dataclasses import asdict, dataclass
from typing import Any, Callable

from .contracts import attach_contract
from .derivation_search_tree import (
    BlockerNode,
    branch_promotion_report,
    build_initial_search_tree,
    summarize_search_tree,
    validate_search_tree,
)
from .external_tool_adapters import (
    adapt_algebra_check,
    adapt_counterexample_search,
    adapt_lean_check,
    adapt_proof_state_evidence,
    adapt_retrieval_evidence,
    adapt_static_extraction_evidence,
)


DERIVATION_BRANCH_CONTROLLER_BOUNDARY = (
    "The branch controller schedules bounded evidence actions and records a "
    "search-tree ledger. It is not a complete theorem search, proof engine, "
    "or document repair renderer."
)
DERIVATION_BRANCH_RANKING_CONTRACT = "repair_branch_ranking_result"
DERIVATION_BRANCH_RANKING_BOUNDARY = (
    "Branch ranking is a deterministic evidence ordering over recorded branch "
    "attempts, blockers, assumptions, and route evidence. It is not MCTS, "
    "global optimization, proof, minimality, or scientific validation."
)

BUDGET_PROFILES: dict[str, dict[str, int]] = {
    "smoke": {"max_attempts": 1},
    "standard": {"max_attempts": 3},
}


@dataclass(frozen=True)
class ControllerAction:
    kind: str
    tool: str
    status: str
    reason: str
    evidence_ref: str | None = None


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _as_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def branch_expansion_records(branch: dict[str, Any]) -> list[dict[str, Any]]:
    """Return auditable expansion records for a candidate repair branch."""
    branch_id = str(branch.get("id", "branch"))
    records: list[dict[str, Any]] = []
    assumptions = _as_text_list(branch.get("assumptions"))
    if assumptions:
        records.append(
            {
                "id": f"expansion_{branch_id}_assumptions",
                "kind": "assumption_addition",
                "status": "proposed",
                "summary": f"Propose {len(assumptions)} assumption(s) for this branch.",
                "evidence_refs": _as_text_list(branch.get("evidence_refs")),
                "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    for index, step in enumerate(_as_dict_list(branch.get("derivation_route_under_assumptions")), start=1):
        records.append(
            {
                "id": f"expansion_{branch_id}_derivation_{index}",
                "kind": "derivation_split",
                "status": str(step.get("checker_status") or "diagnostic_route"),
                "summary": str(step.get("detail") or step.get("step") or "Route step recorded."),
                "evidence_refs": _as_text_list(step.get("evidence_refs")),
                "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    for item in _as_dict_list(branch.get("translation_attempts")):
        records.append(
            {
                "id": f"expansion_{branch_id}_formalization_{item.get('backend', 'backend')}",
                "kind": "formalization_route",
                "status": str(item.get("status", "unknown")),
                "summary": str(item.get("reason") or item.get("expected_next_artifact") or "Formalization route recorded."),
                "evidence_refs": [
                    *[str(ref) for ref in item.get("backend_attempt_ids", []) if str(ref)],
                    *[str(ref) for ref in item.get("blocker_ids", []) if str(ref)],
                ],
                "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    for group in _as_dict_list(branch.get("agent_hypothesis_expansions")):
        candidates = _as_dict_list(group.get("candidates"))
        for item in candidates:
            records.append(
                {
                    "id": f"expansion_{branch_id}_{item.get('id', 'agent_hypothesis')}",
                    "kind": "agent_hypothesis_candidate",
                    "status": str(item.get("status", "candidate_pending_tree_verification")),
                    "summary": str(item.get("proposed_route") or "Agent-generated candidate route."),
                    "evidence_refs": _as_text_list(item.get("source_refs")),
                    "boundary": str(item.get("boundary") or DERIVATION_BRANCH_RANKING_BOUNDARY),
                }
            )
    for item in _as_dict_list(branch.get("backend_attempts")):
        records.append(
            {
                "id": f"expansion_{branch_id}_backend_{item.get('id', 'attempt')}",
                "kind": "backend_attempt",
                "status": str(item.get("status", "unknown")),
                "summary": (
                    f"{item.get('tool', 'backend')} attempt with evidence "
                    f"{item.get('evidence_kind', 'unknown')} and certification "
                    f"{item.get('certification_status', 'unknown')}."
                ),
                "evidence_refs": [str(item.get("id", ""))] if item.get("id") else [],
                "boundary": str(item.get("boundary") or DERIVATION_BRANCH_RANKING_BOUNDARY),
            }
        )
    blockers_seen: set[str] = set()
    for item in [*_as_dict_list(branch.get("translation_blockers")), *_as_dict_list(branch.get("blockers"))]:
        blocker_id = str(item.get("id", "blocker"))
        if blocker_id in blockers_seen:
            continue
        blockers_seen.add(blocker_id)
        records.append(
            {
                "id": f"expansion_{branch_id}_blocker_{blocker_id}",
                "kind": "blocker",
                "status": "blocking",
                "summary": str(item.get("problem") or item.get("why") or "Blocker recorded."),
                "evidence_refs": _as_text_list(item.get("evidence_refs")),
                "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    return records


def _specific_blockers(branch: dict[str, Any]) -> list[dict[str, Any]]:
    generic_kinds = {
        "adapter_diagnostic",
        "formalization_required",
        "budget_exhausted",
        "source_extraction_uncertainty",
    }
    blockers: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in [*_as_dict_list(branch.get("translation_blockers")), *_as_dict_list(branch.get("blockers"))]:
        blocker_id = str(item.get("id", ""))
        if blocker_id in seen:
            continue
        seen.add(blocker_id)
        kind = str(item.get("kind", ""))
        if kind in generic_kinds:
            continue
        if item.get("problem") and item.get("why") and item.get("required_next_evidence"):
            blockers.append(item)
    return blockers


def _branch_promotion(branch: dict[str, Any]) -> dict[str, Any]:
    evidence = branch.get("backend_evidence")
    if isinstance(evidence, dict) and isinstance(evidence.get("promotion"), dict):
        return dict(evidence["promotion"])
    return branch_promotion_report(
        {
            "status": str(branch.get("status", "partial")),
            "backend_attempts": _as_dict_list(branch.get("backend_attempts")),
        }
    )


def _source_support(branch: dict[str, Any]) -> int:
    refs = set(_as_text_list(branch.get("evidence_refs")))
    refs.update(_as_text_list(branch.get("typed_obligation_ids")))
    for item in _as_dict_list(branch.get("external_tool_first_ledger")):
        if item.get("selected_route"):
            refs.add(str(item.get("tool", "")))
    return len([ref for ref in refs if ref])


def _rank_components(branch: dict[str, Any]) -> dict[str, Any]:
    promotion = _branch_promotion(branch)
    backend_attempts = _as_dict_list(branch.get("backend_attempts"))
    blockers = _specific_blockers(branch)
    closes = _as_text_list(branch.get("closes_obligations"))
    assumptions = _as_text_list(branch.get("assumptions"))
    if promotion.get("can_promote"):
        backend_certification = 100
    elif backend_attempts:
        backend_certification = 25
    else:
        backend_certification = 0
    closure_strength = min(20, 6 * len(closes))
    source_support = min(15, 3 * _source_support(branch))
    blocker_specificity = 0 if promotion.get("can_promote") else min(25, 5 * len(blockers))
    non_minimality_penalty = max(0, len(assumptions) - 2) * 2
    if "not_minimal" in str(branch.get("non_claim", "")).lower() or "not minimal" in str(branch.get("non_claim", "")).lower():
        non_minimality_penalty += 2
    score = backend_certification + closure_strength + source_support + blocker_specificity - non_minimality_penalty
    return {
        "backend_certification": backend_certification,
        "closure_strength": closure_strength,
        "source_support": source_support,
        "blocker_specificity": blocker_specificity,
        "non_minimality_penalty": non_minimality_penalty,
        "score": score,
        "specific_blocker_count": len(blockers),
        "backend_attempt_count": len(backend_attempts),
        "assumption_count": len(assumptions),
    }


def _rank_outcome(branch: dict[str, Any], promotion: dict[str, Any], components: dict[str, Any]) -> str:
    if promotion.get("can_promote"):
        supported = str(promotion.get("supported_status") or "certified")
        return f"scoped_{supported}"
    if components.get("specific_blocker_count", 0) > 0:
        return "blocked_with_specific_next_evidence"
    if components.get("backend_attempt_count", 0) > 0:
        return "diagnostic_attempt_only"
    return "open_or_template_only"


def rank_repair_branches(branches: list[dict[str, Any]]) -> dict[str, Any]:
    """Rank repair branches by recorded evidence without inventing repairs."""
    rankings: list[dict[str, Any]] = []
    for branch in branches:
        if not isinstance(branch, dict):
            continue
        promotion = _branch_promotion(branch)
        components = _rank_components(branch)
        outcome = _rank_outcome(branch, promotion, components)
        branch_id = str(branch.get("id", f"branch_{len(rankings) + 1}"))
        rankings.append(
            {
                "branch_id": branch_id,
                "status": str(branch.get("status", "unknown")),
                "outcome": outcome,
                "score": components["score"],
                "score_components": components,
                "promotion": promotion,
                "expansion_record_count": len(branch_expansion_records(branch)),
                "explanation": (
                    f"Ranked as {outcome}: backend={components['backend_certification']}, "
                    f"closure={components['closure_strength']}, source={components['source_support']}, "
                    f"blocker_specificity={components['blocker_specificity']}, "
                    f"non_minimality_penalty={components['non_minimality_penalty']}."
                ),
                "non_claim": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    rankings.sort(key=lambda item: (-float(item["score"]), item["branch_id"]))
    for rank, item in enumerate(rankings, start=1):
        item["rank"] = rank
    result = {
        "status": "ranked" if rankings else "no_branches",
        "branch_count": len(rankings),
        "ranked_branch_ids": [item["branch_id"] for item in rankings],
        "top_branch_id": rankings[0]["branch_id"] if rankings else None,
        "rankings": rankings,
        "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
        "non_claims": [
            "Ranking is deterministic evidence ordering only.",
            "Top-ranked does not mean globally optimal, minimal, proved, or publication-ready.",
        ],
    }
    return attach_contract(result, DERIVATION_BRANCH_RANKING_CONTRACT)


def _split_target(target: str, lhs: str | None, rhs: str | None) -> tuple[str | None, str | None]:
    if lhs is not None and rhs is not None:
        return lhs, rhs
    if "=" not in target:
        return None, None
    left, right = target.split("=", 1)
    left = left.strip()
    right = right.strip()
    if not left or not right:
        return None, None
    return left, right


def _lean_source_binds_target(target: str, lean_source: str) -> bool:
    normalized_target = " ".join(target.split())
    normalized_source = " ".join(lean_source.split())
    if not normalized_target or not normalized_source:
        return False
    if normalized_target in normalized_source:
        return True
    target_terms = [part.strip() for part in normalized_target.split("=")]
    return len(target_terms) == 2 and all(term and term in normalized_source for term in target_terms)


def _budget(profile: str, max_attempts: int | None) -> dict[str, int]:
    base = BUDGET_PROFILES.get(profile, BUDGET_PROFILES["smoke"])
    attempts = int(max_attempts if max_attempts is not None else base["max_attempts"])
    return {"profile": profile if profile in BUDGET_PROFILES else "smoke", "max_attempts": max(0, attempts)}


def _blocker(
    blocker_id: str,
    *,
    kind: str,
    problem: str,
    why: str,
    required_next_evidence: str,
    source: str,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    return asdict(
        BlockerNode(
            id=blocker_id,
            kind=kind,
            problem=problem,
            why=why,
            required_next_evidence=required_next_evidence,
            source=source,
            evidence_refs=evidence_refs or [],
        )
    )


def _record_adapter_result(root: dict[str, Any], adapter_result: dict[str, Any], actions: list[dict[str, Any]]) -> None:
    attempt = adapter_result.get("attempt") if isinstance(adapter_result, dict) else None
    if isinstance(attempt, dict):
        root["backend_attempts"].append(attempt)
        actions.append(
            asdict(
                ControllerAction(
                    kind="backend_attempt",
                    tool=str(attempt.get("tool", "unknown")),
                    status=str(attempt.get("status", "unknown")),
                    reason=str(adapter_result.get("reason", "")),
                    evidence_ref=str(attempt.get("id", "")),
                )
            )
        )
        if attempt.get("certification_status") == "diagnostic":
            root["blockers"].append(
                _blocker(
                    f"blocker_{attempt.get('id', 'adapter_diagnostic')}",
                    kind="adapter_diagnostic",
                    problem=f"{attempt.get('tool', 'adapter')} did not certify or refute the target.",
                    why=str(adapter_result.get("reason", "The adapter returned diagnostic evidence.")),
                    required_next_evidence="Provide a certifying backend result, concrete counterexample, formalization, or stronger assumption set.",
                    source=str(adapter_result.get("source_contract") or "external_tool_adapter"),
                    evidence_refs=[str(attempt.get("id", ""))],
                )
            )


def _adapter_exception_result(kind: str, exc: Exception) -> dict[str, Any]:
    return {
        "status": "adapter_error",
        "reason": f"{kind} adapter action failed inside the controller: {type(exc).__name__}: {exc}",
        "attempt": {
            "id": f"{kind}_controller_adapter_error",
            "tool": kind,
            "status": "adapter_error",
            "evidence_kind": "diagnostic",
            "certification_status": "diagnostic",
            "input_summary": kind,
            "output_ref": None,
            "timeout_seconds": None,
            "version": None,
            "boundary": "Controller-caught adapter errors are diagnostic only.",
        },
        "source_contract": "derivation_branch_controller",
        "source_status": "adapter_error",
        "raw_result": None,
        "boundary": DERIVATION_BRANCH_CONTROLLER_BOUNDARY,
    }
def _apply_promotion(root: dict[str, Any]) -> dict[str, Any]:
    promotion = branch_promotion_report(root)
    if promotion["can_promote"] and promotion["supported_status"] in {"proved", "refuted"}:
        root["status"] = promotion["supported_status"]
    elif root.get("blockers"):
        root["status"] = "partial" if root.get("backend_attempts") else "blocked"
    elif root.get("backend_attempts"):
        root["status"] = "partial"
    return promotion


def _selected_tools(plan: dict[str, Any]) -> list[str]:
    selected = plan.get("selected_external_tools", [])
    tools: list[str] = []
    if isinstance(selected, list):
        for item in selected:
            if isinstance(item, dict) and isinstance(item.get("tool"), str):
                tools.append(item["tool"])
    return tools


def can_derive_with_budget(
    target: str,
    *,
    lhs: str | None = None,
    rhs: str | None = None,
    lean_source: str | None = None,
    budget_profile: str = "smoke",
    max_attempts: int | None = None,
    external_tool_plan: dict[str, Any] | None = None,
    capabilities: dict[str, Any] | None = None,
    integrations: dict[str, Any] | None = None,
    algebra_runner: Callable[..., dict[str, Any]] | None = None,
    counterexample_runner: Callable[..., dict[str, Any]] | None = None,
    lean_runner: Callable[..., dict[str, Any]] | None = None,
    retrieval_hits: dict[str, list[dict[str, Any]]] | None = None,
    static_extractions: dict[str, dict[str, Any]] | None = None,
    proof_state_traces: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Run a small deterministic evidence-action budget and return a tree."""
    budget = _budget(budget_profile, max_attempts)
    tree = build_initial_search_tree(
        target,
        external_tool_plan=external_tool_plan,
        goal_kind="derivation",
        capabilities=capabilities,
        integrations=integrations,
    )
    root = tree["root"]
    actions: list[dict[str, Any]] = []
    exhausted_actions: list[str] = []
    attempts_used = 0

    plan = root.get("external_tool_first_plan", {})
    if plan.get("status") == "blocked_pending_external_tool_or_gap_justification":
        tree["controller"] = {
            "status": "blocked",
            "reason": "External-tool-first gate is blocked; no in-house branch actions were run.",
            "budget": budget,
            "actions": actions,
            "exhausted_actions": exhausted_actions,
            "boundary": DERIVATION_BRANCH_CONTROLLER_BOUNDARY,
        }
        tree["status"] = root["status"]
        tree["summary"] = summarize_search_tree(tree)
        return tree

    left, right = _split_target(target, lhs, rhs)
    selected_tools = _selected_tools(plan)
    candidates: list[tuple[str, Callable[[], dict[str, Any]]]] = []

    algebra_tool = "sympy" if "sympy" in selected_tools or not selected_tools else selected_tools[0]
    candidates.append(
        (
            "algebra_check",
            lambda tool=algebra_tool: adapt_algebra_check(
                target,
                lhs=left,
                rhs=right,
                tool=tool,
                runner=algebra_runner,
            ),
        )
    )
    lean_action = None
    lean_bound_to_target = bool(lean_source and _lean_source_binds_target(target, lean_source))
    if lean_source and not lean_bound_to_target:
        root["blockers"].append(
            _blocker(
                "blocker_lean_source_target_binding_required",
                kind="formalization_required",
                problem="Lean source was supplied but is not conservatively bound to the controller target.",
                why="A direct Lean check can only certify this branch if the Lean source states the scoped target or contains the target lhs/rhs terms.",
                required_next_evidence="Supply Lean source that explicitly formalizes the target before using Lean as certifying evidence.",
                source="derivation_branch_controller",
            )
        )
    elif lean_source and lean_bound_to_target:
        lean_action = ("lean_check", lambda: adapt_lean_check(lean_source, runner=lean_runner))
    if not lean_source and "lean" in selected_tools:
        root["blockers"].append(
            _blocker(
                "blocker_lean_source_required",
                kind="formalization_required",
                problem="Lean certification was selected but no Lean source was supplied.",
                why="Direct Lean checking requires an explicit Lean statement/proof artifact.",
                required_next_evidence="Supply Lean source or a formalization branch before Lean certification.",
                source="derivation_branch_controller",
            )
        )
    if left is not None and right is not None:
        candidates.append(
            (
                "counterexample_search",
                lambda: adapt_counterexample_search(left, right, runner=counterexample_runner),
            )
        )
    else:
        root["blockers"].append(
            _blocker(
                "blocker_counterexample_requires_lhs_rhs",
                kind="formalization_required",
                problem="Counterexample search requires a target equality with lhs and rhs.",
                why="The controller could not split the target into non-empty lhs/rhs expressions.",
                required_next_evidence="Provide lhs/rhs or formalize the target as an equality.",
                source="derivation_branch_controller",
            )
        )

    for tool, hits in sorted((retrieval_hits or {}).items()):
        candidates.append(("retrieval", lambda tool=tool, hits=hits: adapt_retrieval_evidence(tool=tool, query=target, hits=hits)))
    for tool, extracted in sorted((static_extractions or {}).items()):
        candidates.append(
            (
                "static_extraction",
                lambda tool=tool, extracted=extracted: adapt_static_extraction_evidence(tool=tool, target=target, extracted=extracted),
            )
        )
    for tool, trace in sorted((proof_state_traces or {}).items()):
        candidates.append(("proof_state", lambda tool=tool, trace=trace: adapt_proof_state_evidence(tool=tool, target=target, trace=trace)))
    if lean_action is not None:
        candidates.append(lean_action)

    for kind, action in candidates:
        if attempts_used >= budget["max_attempts"]:
            exhausted_actions.append(kind)
            continue
        try:
            adapter_result = action()
        except Exception as exc:
            adapter_result = _adapter_exception_result(kind, exc)
        attempts_used += 1
        _record_adapter_result(root, adapter_result, actions)
        promotion = _apply_promotion(root)
        if promotion["can_promote"] and root["status"] in {"proved", "refuted"}:
            break

    budget_exhausted = bool(exhausted_actions and root["status"] not in {"proved", "refuted"})
    if budget_exhausted:
        root["status"] = "budget_exhausted"
        root["blockers"].append(
            _blocker(
                "blocker_budget_exhausted",
                kind="budget_exhausted",
                problem="The controller exhausted its attempt budget before proof or refutation.",
                why="Some scheduled evidence actions were not attempted within the selected budget profile.",
                required_next_evidence="Increase budget, provide a stronger formalization, or inspect exhausted actions.",
                source="derivation_branch_controller",
                evidence_refs=exhausted_actions,
            )
        )

    promotion = branch_promotion_report(root) if budget_exhausted else _apply_promotion(root)
    tree["status"] = root["status"]
    tree["summary"] = summarize_search_tree(tree)
    validation_errors = validate_search_tree(tree)
    tree["controller"] = {
        "status": root["status"],
        "reason": (
            "A branch was promoted by certifying/refuting evidence."
            if root["status"] in {"proved", "refuted"}
            else "Controller stopped with diagnostic evidence, blockers, or exhausted budget."
        ),
        "budget": budget,
        "attempts_used": attempts_used,
        "actions": actions,
        "exhausted_actions": exhausted_actions,
        "promotion": promotion,
        "validation_errors": validation_errors,
        "boundary": DERIVATION_BRANCH_CONTROLLER_BOUNDARY,
    }
    return tree
