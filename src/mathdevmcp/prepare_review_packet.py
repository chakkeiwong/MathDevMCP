from __future__ import annotations

"""High-level review packet workflow."""

from typing import Any

from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_review_packet_result
from .math_review_packet import build_math_review_packet


def prepare_review_packet(
    question: str,
    *,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    packet_id: str | None = None,
) -> dict[str, Any]:
    """Aggregate evidence for human review without certifying it."""
    evidence_items = evidence or []
    low_level = build_math_review_packet(question, source=source, evidence=evidence_items, packet_id=packet_id)
    result = package_review_packet_result(low_level, question=question)
    result["actions"].append(action("human_review", "Inspect nested evidence, non-claims, and action items."))
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid prepare_review_packet result: {errors}")
    return result


def score_review_packet(result: dict[str, Any]) -> dict[str, Any]:
    """Rubric score for review-packet usefulness and boundary preservation."""
    evidence = result.get("evidence", [])
    low_level = evidence[0].get("low_level", {}) if evidence and isinstance(evidence[0], dict) else {}
    nested = low_level.get("evidence", []) if isinstance(low_level, dict) else []
    non_claim_codes = {item.get("code") for item in result.get("non_claims", []) if isinstance(item, dict)}
    checks = {
        "has_nested_evidence": bool(nested),
        "has_actions": bool(result.get("actions")),
        "diagnostic_only": result.get("status") == "diagnostic_only",
        "not_certificate": result.get("certification_source") == "none",
        "boundary_nonclaim": "diagnostic_evidence_not_proof" in non_claim_codes,
    }
    return {
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "metadata": {"schema_version": "1.0", "contract": "review_packet_rubric"},
    }
