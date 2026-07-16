from __future__ import annotations

"""High-level proof-or-counterexample workflow."""

from typing import Any

from .high_level_contracts import action, default_non_claims, evidence_entry, high_level_result, refresh_evidence_ledger, validate_high_level_result, veto_reason
from .high_level_workflows import package_low_level_math_result
from .prove_or_refute import prove_or_refute


def prove_or_counterexample(
    claim: str,
    *,
    assumptions: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
    claim_semantics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Answer a scoped "can we prove this?" question."""
    assumption_list = assumptions or []
    try:
        low_level = prove_or_refute(
            claim,
            assumptions=assumption_list,
            lhs=lhs,
            rhs=rhs,
            backend=backend,
            lean_source=lean_source,
            claim_semantics=claim_semantics,
        )
    except ValueError as exc:
        result = high_level_result(
            status="not_encodable",
            workflow="prove_or_counterexample",
            question=f"Can we prove {claim}?",
            claim_class="proof",
            answer=str(exc),
            evidence=[
                evidence_entry(
                    id="prove_or_counterexample:not-encodable",
                    evidence_class="not_encodable",
                    source="router",
                    summary=str(exc),
                    extra={"explicit_assumptions": assumption_list},
                )
            ],
            certification_source="none",
            veto_reasons=[veto_reason("not_encodable", str(exc))],
            actions=[action("formalize_claim", "Provide lhs/rhs or a claim containing an equality sign.")],
            non_claims=default_non_claims(extra_codes={"not_encodable_not_false"}),
        )
        errors = validate_high_level_result(result)
        if errors:
            raise ValueError(f"invalid prove_or_counterexample not-encodable result: {errors}") from exc
        return result

    result = package_low_level_math_result(
        low_level,
        workflow="prove_or_counterexample",
        question=f"Can we prove {claim}?",
    )
    result["actions"].append(action("human_review", "Review proof scope, assumptions, and backend route before reusing the result."))
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid prove_or_counterexample result: {errors}")
    return result
