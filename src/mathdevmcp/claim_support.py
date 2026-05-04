"""Local claim-support packets separate from mathematical proof."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from .contracts import attach_contract, contract_metadata


ClaimStatus = Literal[
    "exact_identity",
    "theorem_from_cited_source",
    "model_assumption",
    "diagnostic_evidence",
    "empirical_regularity",
    "proposed_extension",
    "open_problem",
]


@dataclass(frozen=True)
class ClaimSupportPacket:
    claim_id: str
    claim: str
    claim_status: str
    citations: list[dict]
    linked_labels: list[str]
    linked_packets: list[str]
    evidence_boundary: str
    findings: list[dict]
    metadata: dict[str, str]


def classify_claim(claim: str, *, citations: list[dict] | None = None, empirical: bool = False, assumption: bool = False, proposed: bool = False) -> str:
    lowered = claim.lower()
    if assumption or "assume" in lowered or "assumption" in lowered:
        return "model_assumption"
    if proposed or "we propose" in lowered or "future work" in lowered:
        return "proposed_extension"
    if empirical or "empirical" in lowered or "data" in lowered:
        return "empirical_regularity"
    if citations:
        return "theorem_from_cited_source" if "theorem" in lowered or "standard" in lowered else "diagnostic_evidence"
    if "=" in claim and any(token in lowered for token in ["identity", "equals", "="]):
        return "exact_identity"
    return "open_problem"


def build_claim_support_packet(
    claim: str,
    *,
    claim_id: str | None = None,
    citations: list[dict] | None = None,
    linked_labels: list[str] | None = None,
    linked_packets: list[str] | None = None,
    empirical: bool = False,
    assumption: bool = False,
    proposed: bool = False,
) -> dict:
    citations = citations or []
    claim_status = classify_claim(claim, citations=citations, empirical=empirical, assumption=assumption, proposed=proposed)
    findings = []
    if not citations and claim_status in {"theorem_from_cited_source", "diagnostic_evidence", "empirical_regularity"}:
        findings.append({"kind": "missing_citation", "severity": "high", "reason": "Claim status requires citation or data evidence."})
    if claim_status == "empirical_regularity":
        findings.append({"kind": "requires_data_evidence", "severity": "medium", "reason": "Empirical regularities need data or experiment linkage."})
    packet = ClaimSupportPacket(
        claim_id=claim_id or f"claim:{abs(hash(claim)) % 10_000_000}",
        claim=claim,
        claim_status=claim_status,
        citations=citations,
        linked_labels=linked_labels or [],
        linked_packets=linked_packets or [],
        evidence_boundary="Citation and claim-support evidence is not mathematical proof unless linked to a certified scoped proof obligation.",
        findings=findings,
        metadata=contract_metadata("claim_support_packet"),
    )
    return attach_contract(asdict(packet), "claim_support_packet")
