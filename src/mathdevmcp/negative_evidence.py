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
    source: dict
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
    extraction = evidence.get("target_extraction") if isinstance(evidence.get("target_extraction"), dict) else {}
    targets = extraction.get("targets", []) if isinstance(extraction, dict) else []
    target = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
    source = (
        {
            "file": target.get("file"),
            "label": target.get("label"),
            "line_start": target.get("line_start"),
            "line_end": target.get("line_end"),
            "target": target.get("target"),
            "normalized_target": target.get("normalized_target"),
            "routing_role": target.get("routing_role"),
            "specialist_execution": target.get("specialist_execution"),
            "obligation_id": target.get("obligation_id"),
            "obligation_digest": target.get("obligation_digest"),
            "source_digest": target.get("label_scoped_obligation", {}).get("document", {}).get("source_digest"),
            "source_binding_status": evidence.get("source_binding_status"),
            "specialist_parser_readiness": evidence.get("specialist_parser_readiness"),
        }
        if target is not None
        else {
            "label": label,
            "status": "unresolved_source_target",
            "source_binding_status": evidence.get("source_binding_status"),
            "specialist_parser_readiness": evidence.get("specialist_parser_readiness"),
        }
    )
    packet = NegativeEvidencePacket(
        packet_id=f"negative-evidence:{label}",
        source_label=label,
        status=status,
        reason=str(evidence.get("reason", "Evidence remains diagnostic.")),
        likely_cause=likely_cause,
        source=source,
        evidence=evidence,
        actions=list(evidence.get("high_priority_actions", [])),
        certification_boundary="Negative evidence can block or guide review, but it is not a proof of the corrected statement.",
        metadata=contract_metadata("negative_evidence_packet"),
    )
    return attach_contract(asdict(packet), "negative_evidence_packet", doc_context=evidence.get("provenance"))
