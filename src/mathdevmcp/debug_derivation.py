from __future__ import annotations

"""High-level derivation debugging workflow."""

from typing import Any

from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_proof_gap_result
from .proof_gap import localize_proof_gap


def debug_derivation(
    steps: list[str],
    *,
    assumptions: list[str] | None = None,
    backend: str = "auto",
) -> dict[str, Any]:
    """Localize the first unsupported or refuted derivation transition."""
    try:
        low_level = localize_proof_gap(steps, assumptions=assumptions, backend=backend)
    except ValueError as exc:
        low_level = {
            "status": "inconclusive",
            "reason": str(exc),
            "steps": steps,
            "first_gap": None,
            "metadata": {"schema_version": "1.0", "contract": "proof_gap_result"},
        }
    result = package_proof_gap_result(low_level, question="Where does this derivation first fail?")
    result["actions"].append(action("human_review", "Inspect the localized transition before changing the derivation."))
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid debug_derivation result: {errors}")
    return result


def score_gap_localization(result: dict[str, Any], *, expected_index: int | None, expected_statuses: set[str]) -> dict[str, Any]:
    evidence = result.get("evidence", [])
    first_gap = None
    if evidence and isinstance(evidence[0], dict):
        first_gap = evidence[0].get("first_gap")
    observed_index = first_gap.get("index") if isinstance(first_gap, dict) else None
    observed_status = first_gap.get("status") if isinstance(first_gap, dict) else result.get("status")
    index_ok = observed_index == expected_index
    status_ok = observed_status in expected_statuses
    return {
        "status": "passed" if index_ok and status_ok else "failed",
        "observed_index": observed_index,
        "expected_index": expected_index,
        "observed_status": observed_status,
        "expected_statuses": sorted(expected_statuses),
        "metadata": {"schema_version": "1.0", "contract": "gap_localization_rubric"},
    }
