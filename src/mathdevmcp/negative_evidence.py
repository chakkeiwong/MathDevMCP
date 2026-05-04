"""Negative-evidence packets for mismatches and blocked audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract, contract_metadata


@dataclass(frozen=True)
class NegativeEvidencePacket:
    packet_id: str
    source_label: str
    status: str
    reason: str
    likely_cause: str
    evidence: dict
    actions: list[dict]
    certification_boundary: str
    metadata: dict[str, str]


def build_negative_evidence_packet(label: str, evidence: dict) -> dict:
    status = str(evidence.get("status", "inconclusive"))
    substatuses = evidence.get("substatus_counts", {})
    if status == "mismatch":
        likely_cause = "formula_error_or_backend_refutation"
    elif any("parser_limit" in key for key in substatuses):
        likely_cause = "parser_or_localization_limit"
    elif any("missing_assumption" in key or "missing_shape" in key for key in substatuses):
        likely_cause = "missing_assumption_or_shape"
    else:
        likely_cause = "diagnostic_gap"
    packet = NegativeEvidencePacket(
        packet_id=f"negative-evidence:{label}",
        source_label=label,
        status=status,
        reason=str(evidence.get("reason", "Evidence remains diagnostic.")),
        likely_cause=likely_cause,
        evidence=evidence,
        actions=list(evidence.get("high_priority_actions", [])),
        certification_boundary="Negative evidence can block or guide review, but it is not a proof of the corrected statement.",
        metadata=contract_metadata("negative_evidence_packet"),
    )
    return attach_contract(asdict(packet), "negative_evidence_packet", doc_context=evidence.get("provenance"))
