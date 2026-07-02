from __future__ import annotations

"""Aggregate math debugging evidence into a human-review packet."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .math_debugging import CERTIFICATION_BOUNDARY


@dataclass(frozen=True)
class MathReviewPacket:
    packet_id: str
    question: str
    status: str
    reason: str
    source: dict[str, Any]
    obligations: list[dict[str, Any]]
    assumptions: list[dict[str, Any]]
    backend_attempts: list[dict[str, Any]]
    counterexamples: list[dict[str, Any]]
    code_links: list[dict[str, Any]]
    notation_conflicts: list[dict[str, Any]]
    generated_diagnostics: list[dict[str, Any]]
    backend_checks: list[dict[str, Any]]
    nested_evidence_summary: list[dict[str, Any]]
    route_plans: list[dict[str, Any]]
    trace_maps: list[dict[str, Any]]
    residual_gaps: list[dict[str, Any]]
    decision_criteria: list[str]
    risk_register: list[dict[str, Any]]
    non_claims: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    actions: list[dict[str, Any]]
    certification_boundary: str


def _contract(evidence: dict[str, Any]) -> str:
    metadata = evidence.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return "untyped"


def _compact_projection(item: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: item[field] for field in fields if field in item and item[field] not in (None, [], {})}


def _append_unique(target: list[dict[str, Any]], item: dict[str, Any]) -> None:
    if item not in target:
        target.append(item)


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _source_id(evidence: dict[str, Any], index: int) -> str:
    for key in ("workflow", "id"):
        value = evidence.get(key)
        if isinstance(value, str) and value:
            return value
    contract = _contract(evidence)
    if contract != "untyped":
        return contract
    return f"evidence[{index}]"


def _status(evidence: dict[str, Any]) -> str:
    value = evidence.get("status")
    return value if isinstance(value, str) else ""


def _extend_from_workbench(target: list[dict[str, Any]], evidence: dict[str, Any], key: str) -> None:
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get(key), list):
        for item in workbench[key]:
            if isinstance(item, dict):
                _append_unique(target, item)


def _route_backend_attempt(evidence: dict[str, Any]) -> dict[str, Any] | None:
    route = evidence.get("route_decision")
    if isinstance(route, dict) and isinstance(route.get("backend_attempt"), dict):
        return route["backend_attempt"]
    return None


def _actions_from_evidence(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    actions = evidence.get("actions")
    if isinstance(actions, list):
        return [item for item in actions if isinstance(item, dict)]
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get("actions"), list):
        return [item for item in workbench["actions"] if isinstance(item, dict)]
    next_action = evidence.get("next_action")
    if isinstance(next_action, str) and next_action:
        return [{"kind": next_action, "source": _contract(evidence)}]
    return []


def _evidence_summary(
    evidence: dict[str, Any],
    *,
    scope: str,
    index: int | None = None,
    parent_index: int | None = None,
) -> dict[str, Any]:
    summary = {
        "scope": scope,
        "contract": _contract(evidence),
        "index": index,
        "parent_index": parent_index,
        "workflow": evidence.get("workflow"),
        "status": evidence.get("status"),
        "question": evidence.get("question"),
        "answer": evidence.get("answer") or evidence.get("reason"),
        "id": evidence.get("id"),
        "class": evidence.get("class"),
        "source": evidence.get("source"),
        "summary": evidence.get("summary"),
        "evidence_classes": evidence.get("evidence_classes"),
        "certification_source": evidence.get("certification_source"),
        "has_low_level": isinstance(evidence.get("low_level"), dict),
        "has_route_plan": isinstance(evidence.get("route_plan"), dict),
    }
    return _compact_projection(summary, tuple(summary))


def _record_non_claims(
    target: list[dict[str, Any]],
    evidence: dict[str, Any],
    *,
    source: str,
) -> None:
    for item in _as_dict_list(evidence.get("non_claims")):
        copied = _compact_projection(item, ("code", "text"))
        if copied:
            copied["source"] = source
            _append_unique(target, copied)


def build_math_review_packet(
    question: str,
    *,
    source: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    packet_id: str | None = None,
) -> dict:
    evidence_items = evidence or []
    if not all(isinstance(item, dict) for item in evidence_items):
        raise ValueError("evidence must be a list of objects")

    obligations: list[dict[str, Any]] = []
    assumptions: list[dict[str, Any]] = []
    backend_attempts: list[dict[str, Any]] = []
    counterexamples: list[dict[str, Any]] = []
    code_links: list[dict[str, Any]] = []
    notation_conflicts: list[dict[str, Any]] = []
    generated_diagnostics: list[dict[str, Any]] = []
    backend_checks: list[dict[str, Any]] = []
    nested_evidence_summary: list[dict[str, Any]] = []
    route_plans: list[dict[str, Any]] = []
    trace_maps: list[dict[str, Any]] = []
    residual_gaps: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    non_claims: list[dict[str, Any]] = [
        {
            "code": "review_packet_not_proof_certificate",
            "text": "This review packet is not a proof certificate.",
        },
        {
            "code": "nested_status_not_recertified",
            "text": "Nested workflow statuses are preserved for review and are not recertified by the packet.",
        },
        {
            "code": "diagnostic_route_and_trace_context_not_proof",
            "text": "Route plans and trace maps are diagnostic context, not proof or semantic code verification.",
        },
        {
            "code": "packet_completeness_not_downstream_reliability",
            "text": "A self-contained packet does not establish downstream-agent reliability.",
        },
    ]

    def record_backend_attempt(attempt: Any, *, source_id: str) -> None:
        if not isinstance(attempt, dict):
            return
        _append_unique(backend_attempts, attempt)
        check = _compact_projection(
            {
                **attempt,
                "source": source_id,
                "boundary": "Backend attempts are scoped to their encoded obligation and are not recertified by this packet.",
            },
            ("source", "backend", "status", "reason", "severity", "boundary"),
        )
        if check:
            _append_unique(backend_checks, check)

    def record_route_plan(route_plan: Any, *, source_id: str) -> None:
        if not isinstance(route_plan, dict):
            return
        _append_unique(
            route_plans,
            {
                "source": source_id,
                "route_plan": route_plan,
                "boundary": route_plan.get(
                    "boundary",
                    "Route plan is diagnostic context and is not a proof certificate.",
                ),
            },
        )

    def record_trace_map(trace_map: Any, *, source_id: str) -> None:
        if not isinstance(trace_map, dict):
            return
        _append_unique(
            trace_maps,
            {
                "source": source_id,
                "trace_map": trace_map,
                "boundary": trace_map.get(
                    "boundary",
                    "Trace map is structural context and is not semantic proof.",
                ),
            },
        )

    def record_gap(gap: dict[str, Any]) -> None:
        _append_unique(residual_gaps, _compact_projection(gap, tuple(gap)))

    def collect_low_level(low_level: dict[str, Any], *, source_id: str) -> None:
        _extend_from_workbench(obligations, low_level, "obligations")
        _extend_from_workbench(assumptions, low_level, "assumptions")
        _extend_from_workbench(counterexamples, low_level, "counterexamples")
        _extend_from_workbench(generated_diagnostics, low_level, "artifacts")
        record_backend_attempt(_route_backend_attempt(low_level), source_id=source_id)
        workbench = low_level.get("workbench_result")
        if isinstance(workbench, dict):
            for attempt in _as_dict_list(workbench.get("backend_attempts")):
                record_backend_attempt(attempt, source_id=source_id)
            for obligation in _as_dict_list(workbench.get("obligations")):
                if obligation.get("status") not in {None, "", "proved"}:
                    record_gap(
                        {
                            "kind": "obligation_not_proved",
                            "source": source_id,
                            "obligation": _compact_projection(
                                obligation,
                                ("id", "lhs", "rhs", "status", "reason", "missing_assumptions"),
                            ),
                        }
                    )
        if low_level.get("counterexample"):
            _append_unique(counterexamples, low_level["counterexample"])
        record_trace_map(low_level.get("trace_map"), source_id=source_id)
        diagnostic = low_level.get("assumption_diagnostic")
        if isinstance(diagnostic, dict) and diagnostic.get("missing_assumptions"):
            record_gap(
                {
                    "kind": "missing_assumptions",
                    "source": source_id,
                    "items": diagnostic.get("missing_assumptions"),
                }
            )
        if _status(low_level) in {"missing_assumptions", "backend_unavailable", "not_encodable", "mismatch", "structural_mismatch", "gap_found", "inconclusive"}:
            record_gap(
                {
                    "kind": _status(low_level),
                    "source": source_id,
                    "reason": low_level.get("reason"),
                }
            )

    for index, item in enumerate(evidence_items):
        nested_evidence_summary.append(_evidence_summary(item, scope="top_level_evidence", index=index))
        source_id = _source_id(item, index)
        _record_non_claims(non_claims, item, source=source_id)
        _extend_from_workbench(obligations, item, "obligations")
        _extend_from_workbench(assumptions, item, "assumptions")
        _extend_from_workbench(counterexamples, item, "counterexamples")
        for assumption in _as_dict_list(item.get("assumptions")):
            _append_unique(assumptions, assumption)
        for counterexample in _as_dict_list(item.get("counterexamples")):
            _append_unique(counterexamples, counterexample)
        for attempt in _as_dict_list(item.get("backend_attempts")):
            record_backend_attempt(attempt, source_id=source_id)
        record_backend_attempt(_route_backend_attempt(item), source_id=source_id)
        collect_low_level(item, source_id=source_id)
        if item.get("counterexample"):
            _append_unique(counterexamples, item["counterexample"])
        if _contract(item) == "equation_code_match_result":
            _append_unique(code_links, item)
            record_trace_map(item.get("trace_map"), source_id=source_id)
        if _contract(item) == "notation_reconciliation_result":
            notation_conflicts.extend(item.get("conflicts", []))
            notation_conflicts.extend(item.get("unresolved_symbols", []))
        if _contract(item) == "math_test_generation_result":
            generated_diagnostics.extend(item.get("artifacts", []))
        for item_action in _actions_from_evidence(item):
            _append_unique(actions, item_action)
        for action in _as_dict_list(item.get("actions")):
            _append_unique(actions, action)
        for veto in _as_dict_list(item.get("veto_reasons")):
            record_gap(
                {
                    "kind": veto.get("code", "veto_reason"),
                    "source": source_id,
                    "reason": veto.get("reason"),
                }
            )
        if item.get("status") in {"missing_assumptions", "backend_unavailable", "not_encodable", "mismatch", "structural_mismatch", "gap_found", "inconclusive"}:
            record_gap(
                {
                    "kind": item.get("status"),
                    "source": source_id,
                    "reason": item.get("answer") or item.get("reason"),
                }
            )
        for nested_index, nested in enumerate(_as_dict_list(item.get("evidence"))):
            nested_id = str(nested.get("id") or f"{source_id}.evidence[{nested_index}]")
            nested_evidence_summary.append(
                _evidence_summary(
                    nested,
                    scope="nested_evidence_item",
                    index=nested_index,
                    parent_index=index,
                )
            )
            record_route_plan(nested.get("route_plan"), source_id=nested_id)
            record_backend_attempt(nested.get("backend_attempt"), source_id=nested_id)
            if isinstance(nested.get("obligation"), dict):
                _append_unique(obligations, nested["obligation"])
            if isinstance(nested.get("counterexample"), dict):
                _append_unique(counterexamples, nested["counterexample"])
            low_level = nested.get("low_level")
            if isinstance(low_level, dict):
                collect_low_level(low_level, source_id=nested_id)
                if _contract(low_level) == "equation_code_match_result":
                    _append_unique(code_links, low_level)
            if nested.get("class") in {
                "missing_assumption",
                "backend_unavailable",
                "not_encodable",
                "structural_mismatch",
                "proof_gap",
                "human_review_required",
            }:
                record_gap(
                    {
                        "kind": nested.get("class"),
                        "source": nested_id,
                        "reason": nested.get("summary"),
                    }
                )
            if nested.get("class") == "review_packet" and isinstance(nested.get("route_plan"), dict):
                record_gap(
                    {
                        "kind": "diagnostic_route_plan",
                        "source": nested_id,
                        "reason": "Route plan is available for review but is not proof evidence.",
                    }
                )

    statuses = [_status(item) for item in evidence_items]
    if any(status == "refuted" for status in statuses) or counterexamples:
        status = "blocked_by_refutation"
        reason = "At least one nested evidence record contains a refutation or counterexample."
    elif notation_conflicts:
        status = "needs_human_review"
        reason = "Notation conflicts or unresolved notation decisions require human review."
    elif any(
        status in {
            "missing_assumptions",
            "backend_unavailable",
            "not_encodable",
            "mismatch",
            "structural_mismatch",
            "gap_found",
            "inconclusive",
        }
        for status in statuses
    ):
        status = "needs_human_review"
        reason = "At least one nested evidence record is blocked, unavailable, not encodable, or mismatched."
    else:
        status = "review_ready"
        reason = "Evidence is aggregated for review without changing nested meanings."

    decision_criteria = [
        "Use nested certification_source and evidence classes as scoped provenance; the packet itself does not recertify evidence.",
        "Treat backend checks as applying only to the encoded obligations shown in this packet.",
        "Treat route plans as derivation-route context and preserve the separation between givens and explicit assumptions.",
        "Treat trace maps as structural math-to-code visibility, not semantic implementation proof.",
        "Resolve residual gaps, counterexamples, and notation conflicts before using the packet to guide further work.",
    ]
    risk_register: list[dict[str, Any]] = []
    if not evidence_items:
        risk_register.append(
            {
                "code": "empty_packet",
                "risk": "No nested evidence was supplied.",
                "mitigation": "Collect workflow outputs before using the packet for review.",
            }
        )
    if not source:
        risk_register.append(
            {
                "code": "source_context_missing",
                "risk": "Packet source context is empty or minimal.",
                "mitigation": "Attach source anchors or a context summary before relying on human or downstream-agent review.",
            }
        )
    if residual_gaps:
        risk_register.append(
            {
                "code": "residual_gaps_present",
                "risk": "At least one nested workflow reported a gap, veto, or diagnostic-only route.",
                "mitigation": "Inspect residual_gaps and nested actions before drawing a conclusion.",
            }
        )
    if counterexamples:
        risk_register.append(
            {
                "code": "counterexample_present",
                "risk": "At least one nested workflow contains counterexample evidence.",
                "mitigation": "Treat the packet as blocked until the counterexample scope is reviewed.",
            }
        )
    if route_plans:
        risk_register.append(
            {
                "code": "route_plans_are_diagnostic",
                "risk": "Route plans may be mistaken for derivation proofs.",
                "mitigation": "Use route_plan boundaries and non-claims; do not promote route context to proof.",
            }
        )
    if trace_maps:
        risk_register.append(
            {
                "code": "trace_maps_are_structural",
                "risk": "Structural trace matches may be mistaken for semantic code correctness.",
                "mitigation": "Use trace_map boundaries and require semantic checks for code-correctness claims.",
            }
        )
    if any(item.get("certification_source") in {"backend", "scoped_contradiction"} for item in evidence_items):
        risk_register.append(
            {
                "code": "nested_certification_is_scoped",
                "risk": "Nested certifying evidence can be overgeneralized beyond its encoded obligation.",
                "mitigation": "Inspect backend_checks and obligations; preserve the nested scope.",
            }
        )

    packet = MathReviewPacket(
        packet_id=packet_id or f"math-review:{abs(hash(question)) % 10_000_000}",
        question=question,
        status=status,
        reason=reason,
        source=source or {},
        obligations=obligations,
        assumptions=assumptions,
        backend_attempts=backend_attempts,
        counterexamples=counterexamples,
        code_links=code_links,
        notation_conflicts=notation_conflicts,
        generated_diagnostics=generated_diagnostics,
        backend_checks=backend_checks,
        nested_evidence_summary=nested_evidence_summary,
        route_plans=route_plans,
        trace_maps=trace_maps,
        residual_gaps=residual_gaps,
        decision_criteria=decision_criteria,
        risk_register=risk_register,
        non_claims=non_claims,
        evidence=evidence_items,
        actions=actions,
        certification_boundary=(
            "This packet is an evidence bundle, not a proof certificate. "
            f"{CERTIFICATION_BOUNDARY}"
        ),
    )
    return attach_contract(asdict(packet), "math_review_packet")
