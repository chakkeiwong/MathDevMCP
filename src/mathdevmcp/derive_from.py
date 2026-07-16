from __future__ import annotations

"""High-level derivability workflow."""

from typing import Any

from .derivation_gap_proposals import (
    DERIVATION_VALIDATION_BOUNDARY,
    build_derivation_gaps,
    build_derivation_proposals,
    build_derivation_tool_uses,
    summarize_derivation_validation,
)
from .derive_or_refute import derive_or_refute
from .high_level_contracts import action, default_non_claims, evidence_entry, high_level_result, refresh_evidence_ledger, validate_high_level_result, veto_reason
from .high_level_workflows import package_low_level_math_result


def _derive_route_plan(
    low_level: dict[str, Any],
    *,
    givens: list[str],
    explicit_assumptions: list[str],
) -> dict[str, Any]:
    route = low_level.get("route_decision") if isinstance(low_level.get("route_decision"), dict) else {}
    workbench = low_level.get("workbench_result") if isinstance(low_level.get("workbench_result"), dict) else {}
    obligations = workbench.get("obligations") if isinstance(workbench.get("obligations"), list) else []
    assumption_diagnostic = (
        low_level.get("assumption_diagnostic")
        if isinstance(low_level.get("assumption_diagnostic"), dict)
        else {}
    )
    route_gaps: list[dict[str, Any]] = []
    if assumption_diagnostic.get("missing_assumptions"):
        route_gaps.append(
            {
                "kind": "missing_assumptions",
                "items": assumption_diagnostic["missing_assumptions"],
            }
        )
    if low_level.get("status") in {"unknown", "inconclusive", "not_encodable", "backend_unavailable"}:
        route_gaps.append(
            {
                "kind": str(low_level.get("status")),
                "reason": str(low_level.get("reason", "Route did not produce a certifying result.")),
            }
        )
    return {
        "version": "1.0",
        "scope": "derive_from_route_plan",
        "givens": list(givens),
        "explicit_assumptions": list(explicit_assumptions),
        "backend_route": {
            "route": route.get("route"),
            "status": route.get("status"),
            "reason": route.get("reason"),
        },
        "obligations": [
            {
                key: obligation.get(key)
                for key in ("id", "lhs", "rhs", "status", "reason", "missing_assumptions")
                if key in obligation
            }
            for obligation in obligations
            if isinstance(obligation, dict)
        ],
        "route_gaps": route_gaps,
        "boundary": (
            "This route plan records attempted derivation evidence and gaps; "
            "it is not an unchecked derivation chain or a proof beyond scoped "
            "backend evidence."
        ),
    }


def _source_summary(source: dict[str, Any] | None) -> str:
    if not isinstance(source, dict):
        return ""
    for key in ("context_summary", "summary", "label", "file", "path"):
        value = source.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _attach_derivation_gap_packet(
    result: dict[str, Any],
    low_level: dict[str, Any],
    *,
    target: str,
    givens: list[str],
    assumptions: list[str],
    backend: str,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    gaps = build_derivation_gaps(low_level, source=source)
    proposals = build_derivation_proposals(gaps)
    result["source"] = dict(source or {"target": target})
    result["coverage"] = {
        "target": target,
        "gap_count": len(gaps),
        "proposal_count": len(proposals),
        "backend_attempt_count": sum(
            len(gap.get("backend_attempts", []))
            for gap in gaps
            if isinstance(gap.get("backend_attempts"), list)
        ),
        "counterexample_count": sum(
            len(gap.get("counterexamples", []))
            for gap in gaps
            if isinstance(gap.get("counterexamples"), list)
        ),
        "inspected": ["direct_target"],
        "not_inspected": [
            "document-wide derivation context",
            "global theorem applicability",
            "free-form givens as formal assumptions",
        ],
    }
    result["tool_uses"] = build_derivation_tool_uses(
        target,
        givens=givens,
        assumptions=assumptions,
        backend=backend,
    )
    result["gaps"] = gaps
    result["proposals"] = proposals
    result["validation"] = summarize_derivation_validation(proposals)
    if proposals:
        result["actions"].append(
            action(
                "review_derivation_proposals",
                "Inspect gap-linked derivation proposals before editing text or retrying proof.",
            )
        )
    result["agent_handoff"] = {
        "scoped_question": result.get("question", ""),
        "status": result.get("status", ""),
        "reason": result.get("answer", ""),
        "source_context": _source_summary(result.get("source")),
        "gap_count": len(gaps),
        "proposal_count": len(proposals),
        "derivation_gap_ledger": gaps,
        "proposals": proposals,
        "validation": result["validation"],
        "non_claim_boundary": result.get("non_claims", []),
        "next_actions": result.get("actions", []),
        "next_artifact": "Use the derivation proposals and linked assumption repairs before applying source edits.",
        "certification_boundary": DERIVATION_VALIDATION_BOUNDARY,
    }
    return result


def _not_encodable_low_level(
    target: str,
    *,
    reason: str,
    givens: list[str],
    assumptions: list[str],
) -> dict[str, Any]:
    return {
        "status": "not_encodable",
        "reason": reason,
        "givens": list(givens),
        "target": target,
        "lhs": "",
        "rhs": "",
        "route_decision": {
            "route": "router",
            "status": "not_encodable",
            "reason": reason,
            "backend_attempt": {
                "backend": "router",
                "status": "not_encodable",
                "reason": reason,
                "evidence": [],
                "severity": "diagnostic",
            },
        },
        "assumption_diagnostic": {
            "status": "unknown",
            "reason": "No route-required assumptions were checked because the target was not encodable.",
            "target": target,
            "provided_assumptions": list(assumptions),
            "assumptions": [],
            "missing_assumptions": [],
        },
        "counterexample_search": None,
        "workbench_result": {
            "status": "not_encodable",
            "reason": reason,
            "obligations": [],
            "assumptions": [],
            "backend_attempts": [
                {
                    "backend": "router",
                    "status": "not_encodable",
                    "reason": reason,
                    "evidence": [],
                    "severity": "diagnostic",
                }
            ],
            "counterexamples": [],
            "actions": [],
        },
    }


def derive_from(
    target: str,
    *,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    source: dict[str, Any] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    claim_semantics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Answer a scoped "can I derive target from givens?" question.

    Free-form givens are preserved as context. Only explicit assumptions are
    passed to the low-level backend route.
    """
    given_list = givens or []
    assumption_list = assumptions or []
    try:
        low_level = derive_or_refute(
            target,
            givens=[],
            assumptions=assumption_list,
            lhs=lhs,
            rhs=rhs,
            backend=backend,
            claim_semantics=claim_semantics,
        )
    except ValueError as exc:
        result = high_level_result(
            status="not_encodable",
            workflow="derive_from",
            question=f"Can I derive {target} from the supplied givens?",
            claim_class="derivation",
            answer=str(exc),
            evidence=[
                evidence_entry(
                    id="derive_from:not-encodable",
                    evidence_class="not_encodable",
                    source="router",
                    summary=str(exc),
                    extra={"givens": given_list, "explicit_assumptions": assumption_list},
                )
            ],
            certification_source="none",
            veto_reasons=[veto_reason("not_encodable", str(exc))],
            actions=[
                action(
                    "formalize_claim",
                    "Provide lhs/rhs or a target containing an equality sign.",
                )
            ],
            non_claims=default_non_claims(extra_codes={"not_encodable_not_false", "givens_not_formal_assumptions"}),
        )
        errors = validate_high_level_result(result)
        if errors:
            raise ValueError(f"invalid derive_from not-encodable result: {errors}") from exc
        low_level = _not_encodable_low_level(
            target,
            reason=str(exc),
            givens=given_list,
            assumptions=assumption_list,
        )
        _attach_derivation_gap_packet(
            result,
            low_level,
            target=target,
            givens=given_list,
            assumptions=assumption_list,
            backend=backend,
            source=source,
        )
        refresh_evidence_ledger(result)
        errors = validate_high_level_result(result)
        if errors:
            raise ValueError(f"invalid derive_from not-encodable rich result: {errors}") from exc
        return result
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question=f"Can I derive {target} from the supplied givens?",
    )
    result["actions"].append(
        action(
            "human_review",
            "Check whether the recorded givens should be promoted to explicit route assumptions.",
            extra={"givens": given_list, "explicit_assumptions": assumption_list},
        )
    )
    result["non_claims"] = default_non_claims(
        extra_codes={
            *(item["code"] for item in result["non_claims"]),
            "givens_not_formal_assumptions",
        }
    )
    result["evidence"].append(
        evidence_entry(
            id="derive_from:route-plan",
            evidence_class="review_packet",
            source="derive_from_route_plan",
            summary="Diagnostic route plan records givens, explicit assumptions, obligations, and gaps.",
            extra={
                "givens": given_list,
                "explicit_assumptions": assumption_list,
                "route_plan": _derive_route_plan(
                    low_level,
                    givens=given_list,
                    explicit_assumptions=assumption_list,
                ),
            },
        )
    )
    _attach_derivation_gap_packet(
        result,
        low_level,
        target=target,
        givens=given_list,
        assumptions=assumption_list,
        backend=backend,
        source=source,
    )
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid derive_from result: {errors}")
    return result
