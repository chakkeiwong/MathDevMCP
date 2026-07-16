from __future__ import annotations

"""Verified local artifacts and bounded summaries for large agent reports."""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .contracts import attach_contract


AGENT_REPORT_TRANSPORT_BYTES = 30_720


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


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
    compact = attach_contract(
        {
            "status": result.get("status"),
            "workflow": "audit_and_propose_fix",
            "answer": result.get("answer"),
            "source": low.get("source", result.get("source", {})),
            "coverage": low.get("coverage", {}),
            "repair_ledger": ledger,
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
    size = len(_canonical_bytes(compact))
    compact["payload_guardrail"] = {
        "transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES,
        "canonical_byte_count": size,
        "status": "met" if size <= AGENT_REPORT_TRANSPORT_BYTES else "exceeded",
    }
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
    size = len(_canonical_bytes(compact))
    compact["payload_guardrail"] = {
        "transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES,
        "canonical_byte_count": size,
        "status": "met" if size <= AGENT_REPORT_TRANSPORT_BYTES else "exceeded",
    }
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
    compact = attach_contract(
        {
            "status": result.get("coverage", {}).get("status"),
            "workflow": "audit_math_document_rigor",
            "source": {"file": Path(str(result.get("tex_path", ""))).name},
            "coverage": result.get("coverage", {}),
            "target_selection": {
                "selected_count": selection.get("selected_count"),
                "available_labeled_equation_count": selection.get("available_labeled_equation_count"),
                "partial_coverage": selection.get("partial_coverage"),
                "targets": [
                    {key: item.get(key) for key in ("label", "line_start", "classification") if item.get(key) is not None}
                    for item in selection.get("targets", [])
                    if isinstance(item, dict)
                ],
            },
            "gap_ledger": ledger,
            "non_claims": result.get("non_claims", []),
            "artifact": dict(artifact),
            "payload_guardrail": {"transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES, "status": "pending"},
        },
        "compact_agent_report",
    )
    size = len(_canonical_bytes(compact))
    compact["payload_guardrail"] = {
        "transport_target_bytes": AGENT_REPORT_TRANSPORT_BYTES,
        "canonical_byte_count": size,
        "status": "met" if size <= AGENT_REPORT_TRANSPORT_BYTES else "exceeded",
    }
    if size > AGENT_REPORT_TRANSPORT_BYTES:
        raise ValueError("compact rigor report exceeds the transport budget")
    return compact
