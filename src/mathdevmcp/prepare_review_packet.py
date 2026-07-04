from __future__ import annotations

"""High-level review packet workflow."""

from typing import Any

from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_review_packet_result
from .math_review_packet import build_math_review_packet


def review_packet_agent_handoff(result: dict[str, Any]) -> dict[str, Any]:
    """Return the compact review handoff from a prepared packet result."""
    handoff = result.get("agent_handoff")
    if isinstance(handoff, dict):
        return handoff
    evidence = result.get("evidence")
    if isinstance(evidence, list) and evidence and isinstance(evidence[0], dict):
        low_level = evidence[0].get("low_level")
        if isinstance(low_level, dict) and isinstance(low_level.get("agent_handoff"), dict):
            return low_level["agent_handoff"]
    return {
        "scoped_question": str(result.get("question", "")),
        "status": str(result.get("status", "")),
        "reason": str(result.get("answer", "No review handoff was available.")),
        "evidence_ledger": [],
        "assumption_gap_ledger": [],
        "veto_risks": [],
        "non_claim_boundary": result.get("non_claims") if isinstance(result.get("non_claims"), list) else [],
        "next_actions": result.get("actions") if isinstance(result.get("actions"), list) else [],
        "next_artifact": "Inspect the full review packet before making a mathematical or code claim.",
        "certification_boundary": "This handoff is diagnostic only and is not a proof certificate.",
    }


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
    result["agent_handoff"] = review_packet_agent_handoff(result)
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
