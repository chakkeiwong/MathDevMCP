from __future__ import annotations

"""Budgeted derivation branch controller over external-tool evidence actions."""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .contracts import attach_contract
from .derivation_search_tree import (
    BlockerNode,
    branch_promotion_report,
    build_initial_search_tree,
    summarize_search_tree,
    validate_branch_record,
    validate_search_tree,
)
from .evidence_manifest import content_digest
from .external_tool_adapters import (
    EvidenceContext,
    adapt_algebra_check,
    adapt_counterexample_search,
    adapt_lean_check,
    adapt_proof_state_evidence,
    adapt_retrieval_evidence,
    adapt_static_extraction_evidence,
)
from .external_adapter_contract import reader_verified_claim_evidence_record
from .failure_ledgers import (
    build_ledger_entry,
    build_ledgers,
    rank_repair_branches_partial_order,
    select_next_discriminating_action,
)
from .lean_check import LeanDiagnosticContext, LeanTargetBinding, validate_lean_target_binding


DERIVATION_BRANCH_CONTROLLER_BOUNDARY = (
    "The branch controller schedules bounded evidence actions and records a "
    "search-tree ledger. It is not a complete theorem search, proof engine, "
    "or document repair renderer."
)
DERIVATION_BRANCH_RANKING_CONTRACT = "repair_branch_ranking_result"
DERIVATION_BRANCH_RANKING_BOUNDARY = (
    "Branch ranking is a validity-gated partial order over recorded branch "
    "evidence, blockers, assumptions, coverage, and comparable declared cost. "
    "It is not MCTS, a scalar quality score, global optimization, proof, "
    "minimality, or scientific validation."
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
            generation = item.get("generation") if isinstance(item.get("generation"), dict) else {}
            generator_kind = str(generation.get("kind") or item.get("provenance") or "unknown")
            executed_agent = generator_kind == "agent_generated"
            records.append(
                {
                    "id": f"expansion_{branch_id}_{item.get('id', 'agent_hypothesis')}",
                    "kind": "agent_hypothesis_candidate" if executed_agent else "rule_hypothesis_candidate",
                    "generator_kind": generator_kind,
                    "status": str(item.get("status", "candidate_pending_tree_verification")),
                    "summary": str(
                        item.get("proposed_route")
                        or ("Agent-generated candidate route." if executed_agent else "Rule-generated candidate route.")
                    ),
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


def _legacy_scope(branch: dict[str, Any], *, blocker_kind: str) -> dict[str, Any]:
    branch_id = str(branch.get("id") or "legacy_branch")
    target = str(branch.get("target") or branch.get("normalized_target") or "").strip()
    obligation_ids = _as_text_list(branch.get("typed_obligation_ids"))
    obligation_id = str(branch.get("obligation_id") or branch.get("obligation_digest") or "")
    if not obligation_id and obligation_ids:
        obligation_id = obligation_ids[0]
    return {
        "obligation_id": obligation_id or None,
        "target": target or None,
        "candidate_conclusion": str(branch.get("candidate_conclusion") or target).strip() or None,
        "branch_ids": [branch_id],
        "source_spans": [],
        "closed_blocker_scope": [blocker_kind],
    }


def _legacy_blocker_ledger_kind(kind: str) -> tuple[str, str]:
    normalized = kind.strip().lower()
    engineering_markers = (
        "adapter_error",
        "worker_exception",
        "backend_unavailable",
        "tool_unavailable",
        "timeout",
        "budget_exhausted",
        "resource",
        "configuration",
    )
    evidence_markers = (
        "binding",
        "manifest",
        "source_extraction_uncertainty",
        "request_invalid",
        "result_record",
    )
    mathematical_markers = (
        "assumption",
        "formalization",
        "domain",
        "shape",
        "law",
        "integrability",
        "expectation",
        "conditioning",
        "branch_bound_backend_execution",
        "derivative",
        "invertib",
        "conformab",
        "macro_translation",
        "external_tool_or_gap_justification",
        "adapter_diagnostic",
    )
    if any(marker in normalized for marker in engineering_markers):
        return "engineering", normalized or "unclassified_engineering_failure"
    if any(marker in normalized for marker in evidence_markers):
        return "evidence_integrity", normalized or "unclassified_evidence_failure"
    if any(marker in normalized for marker in mathematical_markers):
        return "mathematical_validity", normalized
    return "evidence_integrity", "unclassified_legacy_blocker"


def _legacy_ledger_entry(
    branch: dict[str, Any],
    item: dict[str, Any],
    *,
    ledger_kind: str,
    normalized_kind: str,
    origin_prefix: str,
    veto_role: str = "veto",
) -> dict[str, Any]:
    branch_id = str(branch.get("id") or "legacy_branch")
    origin_id = str(item.get("id") or f"{origin_prefix}_{normalized_kind}")
    required = str(
        item.get("required_next_evidence")
        or item.get("next_discriminator")
        or "Produce an exact scope-bound diagnostic artifact."
    )
    return build_ledger_entry(
        ledger_kind=ledger_kind,
        kind=normalized_kind,
        scope=_legacy_scope(branch, blocker_kind=normalized_kind),
        target_ids=[str(branch.get("target_id") or branch.get("target") or branch_id)],
        severity="error" if veto_role == "veto" else "info",
        veto_role=veto_role,
        source_refs=_as_text_list(item.get("source_refs")),
        evidence_refs=[
            *_as_text_list(item.get("evidence_refs")),
            *([str(item["output_ref"])] if item.get("output_ref") else []),
        ],
        problem=str(item.get("problem") or f"Legacy branch input has status {normalized_kind}."),
        why=str(item.get("why") or item.get("reason") or required),
        smallest_discriminator={
            "kind": f"resolve_{normalized_kind}",
            "description": required,
            "closes_scope": [normalized_kind],
        },
        required_artifact={
            "kind": f"{normalized_kind}_resolution",
            "schema_version": "p06_legacy_discriminator@1",
            "binding_fields": ["branch_id", "target_id", "origin_id"],
            "path_role": "diagnostic_decision_evidence",
        },
        origin_ids=[origin_id],
        non_claims=[
            "legacy diagnostic records are not exact Phase 04 claim evidence",
            "classification does not establish proof, refutation, or publication authority",
        ],
    )


def _legacy_branch_ledgers(branch: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    seen_objects: set[tuple[str, str]] = set()
    for blocker in [
        *_as_dict_list(branch.get("translation_blockers")),
        *_as_dict_list(branch.get("blockers")),
    ]:
        marker = (str(blocker.get("id", "")), str(blocker.get("kind", "")))
        if marker in seen_objects:
            continue
        seen_objects.add(marker)
        ledger_kind, normalized_kind = _legacy_blocker_ledger_kind(str(blocker.get("kind", "")))
        entries.append(
            _legacy_ledger_entry(
                branch,
                blocker,
                ledger_kind=ledger_kind,
                normalized_kind=normalized_kind,
                origin_prefix="blocker",
            )
        )
    for attempt in _as_dict_list(branch.get("backend_attempts")):
        status = str(attempt.get("status", "unknown")).strip().lower()
        if status in {
            "adapter_error",
            "execution_error",
            "translation_error",
            "malformed_output",
            "truncated_output",
            "timeout",
            "unavailable",
            "backend_unavailable",
        }:
            entries.append(
                _legacy_ledger_entry(
                    branch,
                    attempt,
                    ledger_kind="engineering",
                    normalized_kind=status,
                    origin_prefix="attempt",
                )
            )
        entries.append(
            _legacy_ledger_entry(
                branch,
                attempt,
                ledger_kind="evidence_integrity",
                normalized_kind="unnormalized_legacy_backend_attempt",
                origin_prefix="attempt",
            )
        )
        if status in {"proved", "certified", "verified", "refuted"}:
            entries.append(
                _legacy_ledger_entry(
                    branch,
                    attempt,
                    ledger_kind="mathematical_validity",
                    normalized_kind=f"scoped_{status}_diagnostic",
                    origin_prefix="attempt",
                    veto_role="supporting",
                )
            )
        elif status in {"unknown", "diagnostic", "missing_assumptions", "missing_assumption"}:
            entries.append(
                _legacy_ledger_entry(
                    branch,
                    attempt,
                    ledger_kind="mathematical_validity",
                    normalized_kind="diagnostic_no_decision",
                    origin_prefix="attempt",
                )
            )
    return build_ledgers(entries)


def _legacy_typed_assumptions(branch: dict[str, Any]) -> list[dict[str, Any]]:
    typed = branch.get("typed_assumptions")
    if isinstance(typed, list) and all(isinstance(item, dict) for item in typed):
        return [dict(item) for item in typed]
    return [
        {"id": f"legacy_assumption_{index}", "statement": value, "status": "candidate"}
        for index, value in enumerate(_as_text_list(branch.get("assumptions")), start=1)
    ]


def _phase06_ranking_input(
    branch: dict[str, Any],
    claim_evidence: Any = None,
) -> dict[str, Any]:
    branch_id = str(branch.get("id") or "legacy_branch")
    try:
        verified_evidence = reader_verified_claim_evidence_record(claim_evidence)
    except (TypeError, ValueError):
        verified_evidence = {}
    obligation_ids = _as_text_list(branch.get("typed_obligation_ids"))
    obligation_id = (
        branch.get("obligation_id")
        or branch.get("obligation_digest")
        or (obligation_ids[0] if obligation_ids else None)
    )
    target = branch.get("target") or branch.get("normalized_target") or ""
    branch_errors = validate_branch_record(branch)
    evidence_branch = (
        verified_evidence.get("branch")
        if isinstance(verified_evidence.get("branch"), Mapping)
        else {}
    )
    exact_verified = bool(
        not branch_errors
        and verified_evidence.get("certifying") is True
        and evidence_branch.get("id") == branch_id
        and evidence_branch.get("lineage") == branch.get("lineage")
        and evidence_branch.get("record_digest") == content_digest(branch)
        and verified_evidence.get("obligation", {}).get("digest") == obligation_id
        and verified_evidence.get("obligation", {}).get("target") == target
        and verified_evidence.get("typed_assumptions")
        == branch.get("typed_assumptions")
        and verified_evidence.get("typed_assumption_digests")
        == branch.get("typed_assumption_digests")
    )
    return {
        "id": branch_id,
        "obligation_id": obligation_id,
        "target": target,
        "candidate_conclusion": branch.get("candidate_conclusion")
        or branch.get("target")
        or branch.get("normalized_target")
        or "",
        "exact_verified_evidence": exact_verified,
        "ledgers": _legacy_branch_ledgers(branch),
        "typed_assumptions": _legacy_typed_assumptions(branch),
        "covered_obligation_ids": _as_text_list(branch.get("covered_obligation_ids"))
        or _as_text_list(branch.get("closes_obligations")),
        "execution_cost": branch.get("execution_cost"),
    }


def _rank_outcome(branch: dict[str, Any], ranking_input: dict[str, Any]) -> str:
    entries = ranking_input["ledgers"]["deduplicated_entries"]
    if ranking_input["exact_verified_evidence"] and not ranking_input["ledgers"]["veto_entry_ids"]:
        return "exact_verified_scoped_evidence"
    if any(item["veto_role"] == "veto" for item in entries):
        return "blocked_with_specific_next_evidence"
    if _as_dict_list(branch.get("backend_attempts")):
        return "diagnostic_attempt_only"
    return "open_or_template_only"


def rank_repair_branches(
    branches: list[dict[str, Any]],
    *,
    claim_evidence_by_branch_id: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare repair branches without compensating scalar scores."""
    source_branches = [item for item in branches if isinstance(item, dict) and item.get("id")]
    evidence_by_id = (
        claim_evidence_by_branch_id
        if isinstance(claim_evidence_by_branch_id, Mapping)
        else {}
    )
    ranking_inputs = [
        _phase06_ranking_input(branch, evidence_by_id.get(str(branch["id"])))
        for branch in source_branches
    ]
    aggregate_ledgers = build_ledgers(
        entry
        for item in ranking_inputs
        for entry in item["ledgers"]["raw_entries"]
    )
    partial = rank_repair_branches_partial_order(ranking_inputs)
    by_id = {str(branch["id"]): branch for branch in source_branches}
    input_by_id = {str(item["id"]): item for item in ranking_inputs}
    nondominated = list(partial["nondominated_branch_ids"])
    dominated = [branch_id for branch_id in partial["branch_ids"] if branch_id not in nondominated]
    serialization_ids = [*nondominated, *dominated]
    rankings: list[dict[str, Any]] = []
    for position, branch_id in enumerate(serialization_ids, start=1):
        branch = by_id[branch_id]
        ranking_input = input_by_id[branch_id]
        outcome = _rank_outcome(branch, ranking_input)
        rankings.append(
            {
                "branch_id": branch_id,
                "status": str(branch.get("status", "unknown")),
                "outcome": outcome,
                "nondominated": branch_id in nondominated,
                "serialization_position": position,
                "decision_dimensions": {
                    "exact_verified_evidence": ranking_input["exact_verified_evidence"],
                    "veto_entry_ids": ranking_input["ledgers"]["veto_entry_ids"],
                    "covered_obligation_ids": ranking_input["covered_obligation_ids"],
                    "typed_assumptions": ranking_input["typed_assumptions"],
                    "execution_cost": ranking_input["execution_cost"],
                },
                "ledger_entry_ids": sorted(
                    entry["entry_id"]
                    for entry in ranking_input["ledgers"]["deduplicated_entries"]
                ),
                "veto_entry_ids": list(ranking_input["ledgers"]["veto_entry_ids"]),
                "legacy_promotion_projection": {
                    "authority": "diagnostic_only",
                    "value": _branch_promotion(branch),
                },
                "expansion_record_count": len(branch_expansion_records(branch)),
                "explanation": (
                    f"{outcome}; relation membership is determined by validity gates and "
                    "set/comparable-cost relations, never attempt or blocker volume."
                ),
                "non_claim": DERIVATION_BRANCH_RANKING_BOUNDARY,
            }
        )
    all_entries = aggregate_ledgers["deduplicated_entries"]
    selected_action = (
        select_next_discriminating_action(partial, all_entries)
        if partial["branch_ids"]
        else None
    )
    result = {
        "status": partial["status"],
        "branch_count": len(rankings),
        "ranked_branch_ids": serialization_ids,
        "serialization_order_authority": "diagnostic_only",
        "nondominated_branch_ids": nondominated,
        "top_branch_id": partial["unique_top_branch_id"],
        "top_branch_id_semantics": "unique_nondominated_only",
        "relations": partial["relations"],
        "tie_groups": partial["tie_groups"],
        "ledgers": aggregate_ledgers,
        "selected_action": selected_action,
        "rankings": rankings,
        "boundary": DERIVATION_BRANCH_RANKING_BOUNDARY,
        "non_claims": [
            "Serialization order is deterministic display order only.",
            "A unique nondominated branch is not globally optimal, minimal, proved, or publication-ready.",
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
        attachment = adapter_result.get("evidence_attachment")
        if isinstance(attachment, dict):
            root.setdefault("evidence_attachments", []).append(dict(attachment))
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
    lean_target_binding: LeanTargetBinding | None = None,
    retrieval_hits: dict[str, list[dict[str, Any]]] | None = None,
    static_extractions: dict[str, dict[str, Any]] | None = None,
    proof_state_traces: dict[str, list[dict[str, Any]]] | None = None,
    lean_diagnostic_contexts: dict[str, LeanDiagnosticContext] | None = None,
    evidence_contexts: dict[str, EvidenceContext] | None = None,
    artifact_root: str | Path | None = None,
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
    contexts = evidence_contexts or {}
    diagnostic_contexts = lean_diagnostic_contexts or {}
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
                evidence_context=contexts.get("algebra_check"),
                artifact_root=artifact_root,
            ),
        )
    )
    lean_action = None
    lean_binding_validation = (
        validate_lean_target_binding(lean_source, lean_target_binding)
        if lean_source and lean_target_binding is not None
        else None
    )
    lean_bound_to_target = bool(
        lean_binding_validation
        and lean_binding_validation["can_certify"]
        and lean_binding_validation["record"]["branch_id"] == str(root.get("id"))
        and lean_binding_validation["record"]["normalized_target"] == " ".join(target.split())
    )
    if lean_source and not lean_bound_to_target:
        binding_errors = (
            lean_binding_validation["errors"]
            if lean_binding_validation is not None
            else ["an explicit LeanTargetBinding was not supplied"]
        )
        root["blockers"].append(
            _blocker(
                "blocker_lean_source_target_binding_required",
                kind="formalization_required",
                problem="Lean source was supplied without an exact valid branch-target binding.",
                why=(
                    "Direct Lean certification requires exact target, assumptions, theorem, imports, source, "
                    "project, toolchain, and executable identity. " + "; ".join(binding_errors)
                ),
                required_next_evidence="Supply a valid LeanTargetBinding for this exact controller branch before direct Lean execution.",
                source="derivation_branch_controller",
            )
        )
    elif lean_source and lean_bound_to_target:
        lean_action = (
            "lean_check",
            lambda: adapt_lean_check(
                lean_source,
                runner=lean_runner,
                target_binding=lean_target_binding,
                evidence_context=contexts.get("lean_check"),
                artifact_root=artifact_root,
            ),
        )
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
                lambda: adapt_counterexample_search(
                    left,
                    right,
                    runner=counterexample_runner,
                    evidence_context=contexts.get("counterexample_search"),
                    artifact_root=artifact_root,
                ),
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
        candidates.append(
            (
                "retrieval",
                lambda tool=tool, hits=hits: adapt_retrieval_evidence(
                    tool=tool,
                    query=target,
                    hits=hits,
                    lean_context=diagnostic_contexts.get(tool),
                ),
            )
        )
    for tool, extracted in sorted((static_extractions or {}).items()):
        candidates.append(
            (
                "static_extraction",
                lambda tool=tool, extracted=extracted: adapt_static_extraction_evidence(
                    tool=tool,
                    target=target,
                    extracted=extracted,
                    lean_context=diagnostic_contexts.get(tool),
                ),
            )
        )
    for tool, trace in sorted((proof_state_traces or {}).items()):
        candidates.append(
            (
                "proof_state",
                lambda tool=tool, trace=trace: adapt_proof_state_evidence(
                    tool=tool,
                    target=target,
                    trace=trace,
                    lean_context=diagnostic_contexts.get(tool),
                ),
            )
        )
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
