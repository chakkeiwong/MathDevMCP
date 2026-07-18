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
    audit_provenance: dict
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
    index: dict[str, Any] | None = None,
    resumable_session: dict[str, Any] | None = None,
    resumable_record: dict[str, Any] | None = None,
    resumable_record_index: int | None = None,
) -> dict:
    shared_index = index or build_index(Path(root))
    audit_provenance = {"mode": "computed", "record_id": None}
    if resumable_record is not None or resumable_session is not None or resumable_record_index is not None:
        if not isinstance(resumable_record, dict) or not isinstance(resumable_session, dict) or resumable_record_index is None:
            raise ValueError("resumable packet reuse requires session, record, and record index")
        if assumption_manifest is not None or numeric_artifacts is not None:
            raise ValueError("resumable packet reuse does not cover assumption or numeric audit inputs")
        from .resumable_audit import validate_resumable_label_record

        validate_resumable_label_record(resumable_record, resumable_session, resumable_record_index)
        if Path(root).resolve().as_posix() != resumable_session.get("root") or label != resumable_session["labels"][resumable_record_index]:
            raise ValueError("resumable packet root or label mismatch")
        if file != resumable_session.get("target_file") or source_digest != resumable_session.get("source_digest"):
            raise ValueError("resumable packet source binding mismatch")
        if summary_only != resumable_session.get("options", {}).get("summary_only"):
            raise ValueError("resumable packet summary configuration mismatch")
        audit = resumable_record["result"]
        audit_provenance = {"mode": "reused_validated_checkpoint", "record_id": resumable_record["record_id"]}
    else:
        audit = audit_derivation_v2_for_label(
            root,
            label,
            assumption_manifest=assumption_manifest,
            numeric_artifacts=numeric_artifacts,
            summary_only=summary_only,
            file=file,
            source_digest=source_digest,
            index=shared_index,
        )
    graph = build_dependency_graph(index=shared_index, manifest=assumption_manifest, packets=[{"packet_id": label, "label": label, "status": audit.get("status")}])
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
        audit_provenance=audit_provenance,
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
