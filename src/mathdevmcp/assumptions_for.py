from __future__ import annotations

"""High-level assumption discovery workflow."""

from typing import Any

from .assumption_discovery import assumptions_required
from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_assumption_result


def assumptions_for(
    target: str,
    *,
    provided_assumptions: list[str] | None = None,
) -> dict[str, Any]:
    """Return route-required assumptions for a scoped target."""
    low_level = assumptions_required(target, provided_assumptions=provided_assumptions)
    result = package_assumption_result(low_level, question=f"What assumptions are required for {target}?")
    result["actions"].append(
        action(
            "human_review",
            "Review whether route-required assumptions are sufficient for the intended mathematical setting.",
        )
    )
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid assumptions_for result: {errors}")
    return result


def score_assumption_set(result: dict[str, Any], expected_terms: set[str]) -> dict[str, Any]:
    """Score assumptions by set containment rather than brittle exact strings."""
    observed = {str(item.get("text", "")).lower() for item in result.get("assumptions", []) if isinstance(item, dict)}
    expected = {term.lower() for term in expected_terms}
    matched = sorted(term for term in expected if any(term in item for item in observed))
    missing = sorted(expected - set(matched))
    return {
        "status": "passed" if not missing else "failed",
        "matched_terms": matched,
        "missing_terms": missing,
        "observed_assumptions": sorted(observed),
        "metadata": {"schema_version": "1.0", "contract": "assumption_set_rubric"},
    }
