from __future__ import annotations

"""High-level derivability workflow."""

from typing import Any

from .derive_or_refute import derive_or_refute
from .high_level_contracts import action, default_non_claims, evidence_entry, high_level_result, validate_high_level_result, veto_reason
from .high_level_workflows import package_low_level_math_result


def derive_from(
    target: str,
    *,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
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
            givens=given_list,
            assumptions=assumption_list,
            lhs=lhs,
            rhs=rhs,
            backend=backend,
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
    result["evidence"][0]["givens"] = given_list
    result["evidence"][0]["explicit_assumptions"] = assumption_list
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid derive_from result: {errors}")
    return result
