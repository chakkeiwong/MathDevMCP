from __future__ import annotations

"""Shared orchestration helpers for high-level math workflows."""

from typing import Any

from .high_level_contracts import (
    action,
    assumption_record,
    default_non_claims,
    evidence_entry,
    high_level_result,
    validate_high_level_result,
    veto_reason,
)


LOW_LEVEL_STATUS_MAP: dict[str, str] = {
    "proved": "proved",
    "refuted": "refuted",
    "missing_assumptions": "missing_assumptions",
    "backend_unavailable": "backend_unavailable",
    "not_encodable": "not_encodable",
}


def workflow_claim_class(workflow: str) -> str:
    mapping = {
        "derive_from": "derivation",
        "prove_or_counterexample": "proof",
        "assumptions_for": "assumption_discovery",
        "debug_derivation": "derivation_debugging",
        "audit_math_to_code": "math_to_code",
        "prepare_review_packet": "review_packet",
        "propose_fix": "fix_proposal",
        "audit_and_propose_fix": "fix_report",
    }
    return mapping[workflow]


def ensure_valid_high_level_result(result: dict[str, Any]) -> dict[str, Any]:
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid high-level workflow envelope: {errors}")
    return result


def _first_backend_attempt(low_level: dict[str, Any]) -> dict[str, Any] | None:
    route = low_level.get("route_decision")
    if isinstance(route, dict) and isinstance(route.get("backend_attempt"), dict):
        return route["backend_attempt"]
    workbench = low_level.get("workbench_result")
    attempts = workbench.get("backend_attempts") if isinstance(workbench, dict) else None
    if isinstance(attempts, list) and attempts and isinstance(attempts[0], dict):
        return attempts[0]
    return None


def _low_level_counterexamples(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    counterexamples: list[dict[str, Any]] = []
    direct = low_level.get("counterexample")
    if isinstance(direct, dict):
        counterexamples.append(direct)
    search = low_level.get("counterexample_search")
    if isinstance(search, dict) and isinstance(search.get("counterexample"), dict):
        counterexamples.append(search["counterexample"])
    workbench = low_level.get("workbench_result")
    nested = workbench.get("counterexamples") if isinstance(workbench, dict) else None
    if isinstance(nested, list):
        counterexamples.extend(item for item in nested if isinstance(item, dict))
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in counterexamples:
        marker = repr(sorted(item.items()))
        if marker not in seen:
            deduped.append(item)
            seen.add(marker)
    return deduped


def _low_level_assumptions(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    raw = low_level.get("missing_assumptions") or low_level.get("assumptions") or []
    if not raw and isinstance(low_level.get("assumption_diagnostic"), dict):
        diagnostic = low_level["assumption_diagnostic"]
        raw = diagnostic.get("missing_assumptions") or diagnostic.get("assumptions") or []
    if not isinstance(raw, list):
        raw = []
    normalized: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        normalized.append(
            assumption_record(
                text=text,
                status=str(item.get("status", "missing") or "missing"),
                source=str(item.get("source", "low_level_tool") or "low_level_tool"),
                necessity=str(item.get("necessity", "required_by_route") or "required_by_route"),
                extra={key: value for key, value in item.items() if key not in {"text", "status", "source", "necessity"}},
            )
        )
    return normalized


def _backend_evidence_summary(attempt: dict[str, Any] | None, fallback: str) -> str:
    if isinstance(attempt, dict) and isinstance(attempt.get("reason"), str) and attempt["reason"]:
        return attempt["reason"]
    return fallback


def _first_workbench_obligation(low_level: dict[str, Any]) -> dict[str, Any] | None:
    workbench = low_level.get("workbench_result")
    obligations = workbench.get("obligations") if isinstance(workbench, dict) else None
    if isinstance(obligations, list) and obligations and isinstance(obligations[0], dict):
        return obligations[0]
    return None


def _proof_evidence_extra(low_level: dict[str, Any], attempt: dict[str, Any] | None) -> dict[str, Any]:
    obligation = _first_workbench_obligation(low_level)
    extra: dict[str, Any] = {
        "low_level": low_level,
        "backend_route_status": low_level.get("status"),
    }
    if isinstance(attempt, dict):
        extra["backend_attempt"] = {
            key: attempt.get(key)
            for key in ("backend", "status", "reason", "severity")
            if key in attempt
        }
    if isinstance(obligation, dict):
        extra["obligation"] = {
            key: obligation.get(key)
            for key in ("id", "lhs", "rhs", "status", "reason")
            if key in obligation
        }
    return extra


def _counterexample_evidence_extra(
    low_level: dict[str, Any],
    attempt: dict[str, Any] | None,
    counterexamples: list[dict[str, Any]],
) -> dict[str, Any]:
    extra = _proof_evidence_extra(low_level, attempt)
    if counterexamples:
        counterexample = counterexamples[0]
        extra["counterexample"] = {
            key: counterexample.get(key)
            for key in ("assignments", "lhs_value", "rhs_value", "reason", "backend")
            if key in counterexample
        }
    return extra


def _has_proof_artifacts(attempt: dict[str, Any] | None, obligation: dict[str, Any] | None) -> bool:
    if not isinstance(attempt, dict) or not isinstance(obligation, dict):
        return False
    return (
        attempt.get("status") == "proved"
        and attempt.get("severity") == "certifying"
        and obligation.get("status") == "proved"
        and bool(obligation.get("id"))
    )


def package_low_level_math_result(
    low_level: dict[str, Any],
    *,
    workflow: str,
    question: str,
    answer: str | None = None,
) -> dict[str, Any]:
    status = str(low_level.get("status", "inconclusive"))
    high_status = LOW_LEVEL_STATUS_MAP.get(status, "inconclusive")
    claim_class = workflow_claim_class(workflow)
    reason = answer or str(low_level.get("reason", "No bounded answer was produced."))
    attempt = _first_backend_attempt(low_level)
    counterexamples = _low_level_counterexamples(low_level)
    assumptions = _low_level_assumptions(low_level)
    evidence: list[dict[str, Any]] = []
    vetoes: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    certification_source = "none"
    extra_non_claim_codes: set[str] = set()

    if high_status == "proved":
        obligation = _first_workbench_obligation(low_level)
        if _has_proof_artifacts(attempt, obligation):
            certification_source = "backend"
            evidence.append(
                evidence_entry(
                    id=f"{workflow}:backend-certificate",
                    evidence_class="backend_certificate",
                    source="backend",
                    summary=_backend_evidence_summary(attempt, "Scoped obligation was certified by backend evidence."),
                    extra=_proof_evidence_extra(low_level, attempt),
                )
            )
        else:
            high_status = "inconclusive"
            evidence.append(
                evidence_entry(
                    id=f"{workflow}:human-review-required",
                    evidence_class="human_review_required",
                    source="kernel",
                    summary="Low-level proof status was not promoted because certifying artifacts were incomplete.",
                    extra={"low_level": low_level},
                )
            )
            vetoes.append(veto_reason("certifying_evidence_not_promoted", "Proof status lacked a certifying backend attempt or scoped obligation artifact."))
            actions.append(action("supply_more_evidence", "Provide backend attempt and scoped obligation artifacts before promoting proof."))
    elif high_status == "refuted":
        if counterexamples:
            certification_source = "backend"
            evidence.append(
                evidence_entry(
                    id=f"{workflow}:backend-counterexample",
                    evidence_class="backend_counterexample",
                    source="backend",
                    summary=_backend_evidence_summary(attempt, "Scoped obligation was refuted by backend evidence."),
                    extra=_counterexample_evidence_extra(low_level, attempt, counterexamples),
                )
            )
        else:
            high_status = "inconclusive"
            certification_source = "none"
            evidence.append(
                evidence_entry(
                    id=f"{workflow}:human-review-required",
                    evidence_class="human_review_required",
                    source="kernel",
                    summary="Low-level refutation status was not promoted because no counterexample artifact was present.",
                    extra={"low_level": low_level},
                )
            )
            vetoes.append(veto_reason("counterexample_missing", "Refutation evidence was not promoted because no counterexample object was present."))
            vetoes.append(veto_reason("certifying_evidence_not_promoted", "Blocking evidence lacked the Phase 1 counterexample artifact."))
            actions.append(action("supply_more_evidence", "Provide a concrete counterexample artifact."))
    elif high_status == "missing_assumptions":
        evidence.append(
            evidence_entry(
                id=f"{workflow}:missing-assumption",
                evidence_class="missing_assumption",
                source="route",
                summary=str(low_level.get("reason", "Route-required assumptions are missing.")),
                extra={"low_level": low_level},
            )
        )
        extra_non_claim_codes.add("route_assumptions_not_global_minimality")
    elif high_status == "backend_unavailable":
        evidence.append(
            evidence_entry(
                id=f"{workflow}:backend-unavailable",
                evidence_class="backend_unavailable",
                source="backend",
                summary=str(low_level.get("reason", "A backend was unavailable.")),
                extra={"low_level": low_level},
            )
        )
        vetoes.append(veto_reason("backend_unavailable", str(low_level.get("reason", "Backend unavailable."))))
        extra_non_claim_codes.add("backend_unavailable_not_refutation")
    elif high_status == "not_encodable":
        evidence.append(
            evidence_entry(
                id=f"{workflow}:not-encodable",
                evidence_class="not_encodable",
                source="router",
                summary=str(low_level.get("reason", "The claim was not encodable.")),
                extra={"low_level": low_level},
            )
        )
        vetoes.append(veto_reason("not_encodable", str(low_level.get("reason", "Not encodable."))))
        extra_non_claim_codes.add("not_encodable_not_false")
    else:
        evidence.append(
            evidence_entry(
                id=f"{workflow}:human-review-required",
                evidence_class="human_review_required",
                source="kernel",
                summary=str(low_level.get("reason", "No certifying route resolved the question.")),
                extra={"low_level": low_level},
            )
        )
        vetoes.append(veto_reason("unresolved_low_level_status", f"Unsupported or inconclusive low-level status: {status}"))
        actions.append(action("human_review", "Review low-level evidence manually."))

    result = high_level_result(
        status=high_status,
        workflow=workflow,
        question=question,
        claim_class=claim_class,
        answer=reason,
        evidence=evidence,
        certification_source=certification_source,
        veto_reasons=vetoes,
        assumptions=assumptions,
        counterexamples=counterexamples,
        actions=actions,
        non_claims=default_non_claims(extra_codes=extra_non_claim_codes),
    )
    return ensure_valid_high_level_result(result)


def package_assumption_result(low_level: dict[str, Any], *, question: str) -> dict[str, Any]:
    return package_low_level_math_result(low_level, workflow="assumptions_for", question=question)


def package_proof_gap_result(low_level: dict[str, Any], *, question: str) -> dict[str, Any]:
    first_gap = low_level.get("first_gap")
    if low_level.get("status") == "proved":
        return package_low_level_math_result(low_level, workflow="debug_derivation", question=question)
    if low_level.get("status") == "refuted":
        return package_low_level_math_result(low_level, workflow="debug_derivation", question=question)
    evidence = [
        evidence_entry(
            id="debug_derivation:proof-gap",
            evidence_class="proof_gap",
            source="proof_gap_localizer",
            summary=str(low_level.get("reason", "A derivation gap was localized.")),
            extra={"first_gap": first_gap, "low_level": low_level},
        )
    ]
    result = high_level_result(
        status="gap_found",
        workflow="debug_derivation",
        question=question,
        claim_class="derivation_debugging",
        answer=str(low_level.get("reason", "A derivation gap was localized.")),
        evidence=evidence,
        certification_source="none",
        actions=[action("human_review", "Inspect and repair the localized derivation gap.")],
        non_claims=default_non_claims(extra_codes={"gap_localization_not_global_failure"}),
    )
    return ensure_valid_high_level_result(result)


def package_code_audit_result(low_level: dict[str, Any], *, question: str) -> dict[str, Any]:
    if low_level.get("status") == "scope_limited":
        status = "scope_limited_match"
        evidence_class = "scope_limited_match"
    else:
        status = "structural_match" if low_level.get("status") == "consistent" else "structural_mismatch"
        evidence_class = "structural_match" if status == "structural_match" else "structural_mismatch"
    non_claim_codes = {"structural_evidence_not_proof"}
    vetoes: list[dict[str, Any]] = []
    if status == "scope_limited_match":
        non_claim_codes.add("scope_limited_evidence_not_proof")
        vetoes.append(
            veto_reason(
                "scope_limited_evidence_not_promoted",
                "The code evidence supports only a value-level or instance-level slice of the mathematical claim.",
            )
        )
    result = high_level_result(
        status=status,
        workflow="audit_math_to_code",
        question=question,
        claim_class="math_to_code",
        answer=str(low_level.get("reason", "Structural code/equation audit completed.")),
        evidence=[
            evidence_entry(
                id=f"audit_math_to_code:{evidence_class}",
                evidence_class=evidence_class,
                source="structural_matcher",
                summary=str(low_level.get("reason", "Structural audit completed.")),
                extra={"low_level": low_level},
            )
        ],
        certification_source="none",
        veto_reasons=vetoes,
        actions=[] if status == "structural_match" else [action("human_review", "Inspect structural mismatch or scope limitation.")],
        non_claims=default_non_claims(extra_codes=non_claim_codes),
    )
    return ensure_valid_high_level_result(result)


def package_review_packet_result(low_level: dict[str, Any], *, question: str) -> dict[str, Any]:
    result = high_level_result(
        status="diagnostic_only",
        workflow="prepare_review_packet",
        question=question,
        claim_class="review_packet",
        answer=str(low_level.get("reason", "Review packet prepared.")),
        evidence=[
            evidence_entry(
                id="prepare_review_packet:review-packet",
                evidence_class="review_packet",
                source="packet_builder",
                summary=str(low_level.get("reason", "Review packet prepared.")),
                extra={"low_level": low_level},
            )
        ],
        certification_source="none",
        actions=[action("human_review", "Review the packet and nested evidence boundaries.")],
        non_claims=default_non_claims(extra_codes={"diagnostic_evidence_not_proof"}),
    )
    return ensure_valid_high_level_result(result)
