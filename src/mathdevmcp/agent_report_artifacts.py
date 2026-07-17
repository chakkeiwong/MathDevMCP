from __future__ import annotations

"""Verified local artifacts and bounded summaries for large agent reports."""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .contracts import attach_contract


AGENT_REPORT_TRANSPORT_BYTES = 30_720
PACKET_TRANSPORT_SCHEMA = "compact_evidence_packet@1"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def _finalize_payload_guardrail(value: dict[str, Any]) -> int:
    guardrail = value["payload_guardrail"]
    guardrail["canonical_byte_count"] = 0
    guardrail["status"] = "pending"
    while True:
        size = len(_canonical_bytes(value))
        status = "met" if size <= AGENT_REPORT_TRANSPORT_BYTES else "exceeded"
        if guardrail["canonical_byte_count"] == size and guardrail["status"] == status:
            return size
        guardrail["canonical_byte_count"] = size
        guardrail["status"] = status


def _safe_root(value: str | Path, *, create: bool) -> Path:
    root = Path(value).expanduser()
    if root.exists() and root.is_symlink():
        raise ValueError("artifact_root must not be a symlink")
    if create:
        root.mkdir(parents=True, exist_ok=True)
    if not root.is_dir():
        raise ValueError("artifact_root must be an existing directory")
    return root.resolve(strict=True)


def persist_agent_report(report: Mapping[str, Any], artifact_root: str | Path) -> dict[str, Any]:
    payload = _canonical_bytes(report)
    digest = hashlib.sha256(payload).hexdigest()
    root = _safe_root(artifact_root, create=True)
    directory = root / "agent-reports"
    if directory.exists() and directory.is_symlink():
        raise ValueError("agent report directory must not be a symlink")
    directory.mkdir(exist_ok=True)
    directory = directory.resolve(strict=True)
    if root not in directory.parents:
        raise ValueError("agent report directory escapes artifact_root")
    destination = directory / f"{digest}.json"
    if destination.exists():
        if destination.is_symlink() or destination.read_bytes() != payload:
            raise ValueError("agent report artifact identity collision")
    else:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(destination, flags, 0o600)
        try:
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    return {
        "state": "verified",
        "sha256": digest,
        "byte_count": len(payload),
        "media_type": "application/json",
        "authority": "local_byte_identity_only",
        "resolver_tool": "resolve_agent_report",
    }


def resolve_agent_report(artifact_root: str | Path, sha256: str) -> dict[str, Any]:
    if not isinstance(sha256, str) or len(sha256) != 64 or any(character not in "0123456789abcdef" for character in sha256):
        raise ValueError("sha256 must be lowercase hexadecimal")
    root = _safe_root(artifact_root, create=False)
    directory = root / "agent-reports"
    destination = directory / f"{sha256}.json"
    if directory.is_symlink() or destination.is_symlink() or not destination.is_file():
        raise ValueError("verified agent report artifact is missing or unsafe")
    resolved = destination.resolve(strict=True)
    if root not in resolved.parents:
        raise ValueError("agent report artifact escapes artifact_root")
    payload = resolved.read_bytes()
    if hashlib.sha256(payload).hexdigest() != sha256:
        raise ValueError("agent report artifact digest mismatch")
    try:
        report = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("agent report artifact is invalid JSON") from exc
    if _canonical_bytes(report) != payload:
        raise ValueError("agent report artifact is not canonical")
    return attach_contract(
        {
            "status": "resolved",
            "artifact": {"sha256": sha256, "byte_count": len(payload), "authority": "local_byte_identity_only"},
            "report": report,
            "non_claim": "Artifact resolution restores evidence bytes; it does not create proof, publication, or scientific authority.",
        },
        "agent_report_artifact",
    )


def compact_evidence_packet(report: Mapping[str, Any], artifact: Mapping[str, Any]) -> dict[str, Any]:
    """Build a bounded, source-literal handoff for proof or negative evidence."""
    metadata = report.get("metadata") if isinstance(report.get("metadata"), Mapping) else {}
    contract = str(metadata.get("contract", ""))
    if contract not in {"proof_packet", "negative_evidence_packet"}:
        raise ValueError("compact evidence packet requires a proof or negative-evidence packet")
    source = report.get("source") if isinstance(report.get("source"), Mapping) else {}
    nested = report.get("proof_audit_v2") if isinstance(report.get("proof_audit_v2"), Mapping) else report.get("evidence")
    audit = nested if isinstance(nested, Mapping) else {}
    obligations = [
        {
            key: item.get(key)
            for key in (
                "id",
                "label",
                "kind",
                "status",
                "substatus",
                "reason",
                "route",
                "missing_constraints",
                "verification_boundary",
            )
            if item.get(key) not in (None, "", [], {})
        }
        for item in audit.get("obligations", [])
        if isinstance(item, Mapping)
    ]
    specialist = source.get("specialist_execution") if isinstance(source.get("specialist_execution"), Mapping) else {}
    non_claims = [
        str(report.get("certification_boundary", "")),
        *[str(item) for item in specialist.get("non_claims", []) if str(item)],
    ]
    compact = attach_contract(
        {
            "response_schema_version": PACKET_TRANSPORT_SCHEMA,
            "response_mode": "compact",
            "packet_contract": contract,
            "packet_id": report.get("packet_id"),
            "label": report.get("label", report.get("source_label")),
            "status": report.get("status"),
            "reason": report.get("reason", audit.get("reason")),
            "likely_cause": report.get("likely_cause"),
            "substatus_counts": report.get("substatus_counts", audit.get("substatus_counts", {})),
            "source": dict(source),
            "obligation_summaries": obligations,
            "assumption_manifest": report.get("assumption_manifest"),
            "convention_context": report.get("convention_context"),
            "numeric_evidence": report.get("numeric_evidence"),
            "code_links": report.get("code_links", []),
            "actions": report.get("actions", audit.get("high_priority_actions", [])),
            "vetoes": {
                "claim_eligibility": "ineligible",
                "publication_enabled": False,
                "promotion_allowed": False,
            },
            "non_claims": list(dict.fromkeys(item for item in non_claims if item)),
            "artifact": dict(artifact),
            "detail_resolution": {
                "tool": "resolve_agent_report",
                "sha256": artifact.get("sha256"),
                "semantic_parity": "exact canonical detailed packet bytes",
            },
            "payload_guardrail": {
                "transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES,
                "status": "pending",
            },
        },
        "compact_evidence_packet",
    )
    size = _finalize_payload_guardrail(compact)
    if size > AGENT_REPORT_TRANSPORT_BYTES:
        raise ValueError("compact evidence packet exceeds the transport budget")
    return compact


def compact_audit_fix_report(result: Mapping[str, Any], artifact: Mapping[str, Any]) -> dict[str, Any]:
    evidence = result.get("evidence") if isinstance(result.get("evidence"), list) else []
    low = evidence[0].get("low_level", {}) if evidence and isinstance(evidence[0], dict) else {}
    details = low.get("proposal_details") if isinstance(low.get("proposal_details"), list) else []
    ledger = [
        {
            key: item[key]
            for key in ("kind", "target", "label", "location", "problem", "proof_target", "evidence_ref", "evidence_only")
            if key in item and item[key] not in (None, "", [], {})
        }
        for item in details
        if isinstance(item, dict)
    ]
    total_ledger_count = len(ledger)
    coverage = low.get("coverage", {}) if isinstance(low.get("coverage"), Mapping) else {}
    compact_coverage = {
        key: coverage[key]
        for key in (
            "mode",
            "target_file",
            "source_digest",
            "discovered_label_count",
            "audited_label_count",
            "skipped_label_count",
            "audit_complete",
            "limit",
        )
        if key in coverage
    }
    audited_labels = coverage.get("audited_labels")
    if isinstance(audited_labels, list):
        compact_coverage["audited_label_preview"] = [
            str(item.get("label"))
            for item in audited_labels[:20]
            if isinstance(item, Mapping) and item.get("label")
        ]
        compact_coverage["audited_label_preview_truncated"] = len(audited_labels) > 20
    compact = attach_contract(
        {
            "status": result.get("status"),
            "workflow": "audit_and_propose_fix",
            "answer": result.get("answer"),
            "source": low.get("source", result.get("source", {})),
            "coverage": compact_coverage,
            "repair_ledger": ledger,
            "repair_ledger_total_count": total_ledger_count,
            "repair_ledger_truncated": False,
            "validation": low.get("validation", {}),
            "veto_reasons": result.get("veto_reasons", []),
            "assumptions": result.get("assumptions", []),
            "actions": result.get("actions", []),
            "non_claims": result.get("non_claims", []),
            "artifact": dict(artifact),
            "payload_guardrail": {"transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES, "status": "pending"},
        },
        "compact_agent_report",
    )
    size = _finalize_payload_guardrail(compact)
    while size > AGENT_REPORT_TRANSPORT_BYTES and compact["repair_ledger"]:
        compact["repair_ledger"].pop()
        compact["repair_ledger_truncated"] = True
        size = _finalize_payload_guardrail(compact)
    if size > AGENT_REPORT_TRANSPORT_BYTES:
        raise ValueError("compact audit/fix report exceeds the transport budget")
    return compact


def compact_review_packet(result: Mapping[str, Any], artifact: Mapping[str, Any]) -> dict[str, Any]:
    handoff = result.get("agent_handoff") if isinstance(result.get("agent_handoff"), dict) else {}
    compact = attach_contract(
        {
            "status": result.get("status"),
            "workflow": "prepare_review_packet",
            "question": result.get("question"),
            "answer": result.get("answer"),
            "handoff": dict(handoff),
            "veto_reasons": result.get("veto_reasons", []),
            "assumptions": result.get("assumptions", []),
            "actions": result.get("actions", []),
            "non_claims": result.get("non_claims", []),
            "artifact": dict(artifact),
            "payload_guardrail": {"transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES, "status": "pending"},
        },
        "compact_agent_report",
    )
    size = _finalize_payload_guardrail(compact)
    if size > AGENT_REPORT_TRANSPORT_BYTES:
        raise ValueError("compact review packet exceeds the transport budget")
    return compact


def compact_rigor_report(result: Mapping[str, Any], artifact: Mapping[str, Any]) -> dict[str, Any]:
    gaps = result.get("gaps") if isinstance(result.get("gaps"), list) else []
    ledger = [
        {
            key: item[key]
            for key in ("id", "kind", "label", "location", "problem", "evidence_ref", "substantive_classification")
            if key in item and item[key] not in (None, "", [], {})
        }
        for item in gaps
        if isinstance(item, dict)
    ]
    selection = result.get("target_selection") if isinstance(result.get("target_selection"), dict) else {}
    target_rows = [
        {
            "label": item.get("label"),
            "line_start": item.get("line_start"),
            "line_end": item.get("line_end"),
            "relation_kind": item.get("normalized_target", {}).get("kind")
            if isinstance(item.get("normalized_target"), Mapping)
            else None,
            "routing_role": {
                key: item.get("routing_role", {}).get(key)
                for key in ("role", "authority")
                if item.get("routing_role", {}).get(key) is not None
            }
            if isinstance(item.get("routing_role"), Mapping)
            else None,
            "obligation_id": item.get("obligation_id"),
            "obligation_digest": item.get("obligation_digest"),
            "local_obligation_ids": [
                obligation.get("id")
                for obligation in item.get("local_obligations", [])
                if isinstance(obligation, Mapping) and obligation.get("id")
            ],
            "downstream_integration_obligation_ids": [
                obligation.get("id")
                for obligation in item.get("downstream_integration_obligations", [])
                if isinstance(obligation, Mapping) and obligation.get("id")
            ],
        }
        for item in selection.get("targets", [])
        if isinstance(item, dict)
    ]
    total_target_count = len(target_rows)
    total_gap_count = len(ledger)
    compact = attach_contract(
        {
            "status": result.get("coverage", {}).get("status"),
            "workflow": "audit_math_document_rigor",
            "source": dict(result.get("source", {}))
            if isinstance(result.get("source"), Mapping)
            else {"file": Path(str(result.get("tex_path", ""))).name},
            "coverage": result.get("coverage", {}),
            "target_selection": {
                "selected_count": selection.get("selected_count"),
                "available_labeled_equation_count": selection.get("available_labeled_equation_count"),
                "partial_coverage": selection.get("partial_coverage"),
                "targets": target_rows,
                "target_total_count": total_target_count,
                "target_preview_truncated": False,
            },
            "gap_ledger": ledger,
            "gap_ledger_total_count": total_gap_count,
            "gap_ledger_truncated": False,
            "non_claims": result.get("non_claims", []),
            "artifact": dict(artifact),
            "payload_guardrail": {"transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES, "status": "pending"},
        },
        "compact_agent_report",
    )
    size = _finalize_payload_guardrail(compact)
    while size > AGENT_REPORT_TRANSPORT_BYTES and compact["gap_ledger"]:
        compact["gap_ledger"].pop()
        compact["gap_ledger_truncated"] = True
        size = _finalize_payload_guardrail(compact)
    while size > AGENT_REPORT_TRANSPORT_BYTES and compact["target_selection"]["targets"]:
        compact["target_selection"]["targets"].pop()
        compact["target_selection"]["target_preview_truncated"] = True
        size = _finalize_payload_guardrail(compact)
    if size > AGENT_REPORT_TRANSPORT_BYTES:
        raise ValueError("compact rigor report exceeds the transport budget")
    return compact
