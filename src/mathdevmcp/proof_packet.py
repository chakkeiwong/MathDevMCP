"""Durable proof and diagnostic packet builders."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .contracts import attach_contract, contract_metadata
from .dependency_graph import build_dependency_graph
from .latex_index import build_index
from .proof_audit_v2 import audit_derivation_v2_for_label


@dataclass(frozen=True)
class ProofPacket:
    packet_id: str
    label: str
    doc_root: str
    status: str
    substatus_counts: dict[str, int]
    source: dict[str, Any]
    assumption_manifest: dict | None
    convention_context: dict | None
    dependency_graph: dict
    proof_audit_v2: dict
    numeric_evidence: dict | None
    code_links: list[dict]
    actions: list[dict]
    certification_boundary: str
    metadata: dict[str, str]


def build_proof_packet_label(
    root: str,
    label: str,
    *,
    assumption_manifest: dict | None = None,
    convention_context: dict | None = None,
    numeric_artifacts: dict[str, dict] | None = None,
    code_links: list[dict] | None = None,
    summary_only: bool = True,
) -> dict:
    index = build_index(Path(root))
    audit = audit_derivation_v2_for_label(
        root,
        label,
        assumption_manifest=assumption_manifest,
        numeric_artifacts=numeric_artifacts,
        summary_only=summary_only,
    )
    graph = build_dependency_graph(index=index, manifest=assumption_manifest, packets=[{"packet_id": label, "label": label, "status": audit.get("status")}])
    source = index.get("labels", {}).get(label, {})
    packet = ProofPacket(
        packet_id=f"proof-packet:{label}",
        label=label,
        doc_root=str(Path(root).resolve()),
        status=audit.get("status", "inconclusive"),
        substatus_counts=audit.get("substatus_counts", {}),
        source=source,
        assumption_manifest=assumption_manifest,
        convention_context=convention_context,
        dependency_graph=graph,
        proof_audit_v2=audit,
        numeric_evidence={"artifacts_supplied": sorted(numeric_artifacts)} if numeric_artifacts else None,
        code_links=code_links or [],
        actions=audit.get("high_priority_actions", []),
        certification_boundary=(
            "This packet is an evidence bundle. Only nested deterministic backend certificates for scoped "
            "obligations can verify mathematical claims."
        ),
        metadata=contract_metadata("proof_packet"),
    )
    return attach_contract(asdict(packet), "proof_packet", doc_context=source)
