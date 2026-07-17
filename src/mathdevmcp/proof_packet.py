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
    file: str | None = None,
    source_digest: str | None = None,
) -> dict:
    index = build_index(Path(root))
    audit = audit_derivation_v2_for_label(
        root,
        label,
        assumption_manifest=assumption_manifest,
        numeric_artifacts=numeric_artifacts,
        summary_only=summary_only,
        file=file,
        source_digest=source_digest,
    )
    graph = build_dependency_graph(index=index, manifest=assumption_manifest, packets=[{"packet_id": label, "label": label, "status": audit.get("status")}])
    selected_extraction = audit.get("target_extraction")
    targets = selected_extraction.get("targets", []) if isinstance(selected_extraction, dict) else []
    candidate = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
    observed_digest = (
        candidate.get("label_scoped_obligation", {}).get("document", {}).get("source_digest")
        if candidate is not None
        else None
    )
    source_binding_accepted = source_digest is None or observed_digest == source_digest
    target = candidate if source_binding_accepted else None
    source = (
        {
            "file": target.get("file"),
            "label": target.get("label"),
            "line_start": target.get("line_start"),
            "line_end": target.get("line_end"),
            "obligation_id": target.get("obligation_id"),
            "obligation_digest": target.get("obligation_digest"),
            "target": target.get("target"),
            "normalized_target": target.get("normalized_target"),
            "routing_role": target.get("routing_role"),
            "specialist_execution": target.get("specialist_execution"),
            "source_digest": target.get("label_scoped_obligation", {}).get("document", {}).get("source_digest"),
            "target_ingress": "validated_label_scoped_obligation",
            "source_binding_status": audit.get("source_binding_status"),
            "specialist_parser_readiness": audit.get("specialist_parser_readiness"),
        }
        if isinstance(target, dict)
        else {
            "label": label,
            "file": file,
            "source_digest": source_digest,
            "status": "unresolved_source_target",
            "normalized_target": None,
            "routing_role": None,
            "specialist_execution": None,
            "source_binding_status": audit.get("source_binding_status"),
            "specialist_parser_readiness": audit.get("specialist_parser_readiness"),
        }
    )
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
