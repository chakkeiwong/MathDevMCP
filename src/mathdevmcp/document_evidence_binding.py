from __future__ import annotations

"""Current replayable evidence binding for exact document-tree targets."""

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any, Mapping

from .evidence_manifest import EvidenceValidationError, canonical_json_bytes
from .label_scoped_obligation import validate_label_scoped_obligation
from .source_routing_role import validate_source_routing_role


DOCUMENT_BINDING_SCHEMA_VERSION = "1.0"


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _payload(packet: Mapping[str, Any], branches: list[Mapping[str, Any]]) -> dict[str, Any]:
    specialist = packet.get("specialist_execution") if isinstance(packet.get("specialist_execution"), Mapping) else {}
    return {
        "schema_version": DOCUMENT_BINDING_SCHEMA_VERSION,
        "source": {
            "file": packet.get("source_span", {}).get("file"),
            "source_digest": packet.get("source_span", {}).get("source_digest"),
            "span": {
                "start_byte": packet.get("source_span", {}).get("start_byte"),
                "end_byte": packet.get("source_span", {}).get("end_byte"),
            },
            "label": packet.get("label"),
        },
        "obligation": {
            "id": packet.get("obligation_id"),
            "digest": packet.get("obligation_digest"),
            "target": packet.get("target"),
            "relation": deepcopy(packet.get("normalized_target")),
            "routing_role": deepcopy(packet.get("routing_role")),
        },
        "local_obligations": deepcopy(packet.get("local_obligations", [])),
        "branches": [
            {
                "id": branch.get("id"),
                "assumptions": deepcopy(branch.get("assumptions", [])),
                "closes_obligations": deepcopy(branch.get("closes_obligations", [])),
                "specialist_status": branch.get("specialist_execution", {}).get("status")
                if isinstance(branch.get("specialist_execution"), Mapping)
                else None,
            }
            for branch in branches
        ],
        "specialist": {
            "status": specialist.get("status"),
            "selected_tool": specialist.get("selected_tool"),
            "canonical_target": specialist.get("canonical_target"),
            "backend_environment": deepcopy(specialist.get("backend_environment", {})),
            "tool_ledger": deepcopy(specialist.get("tool_ledger", [])),
            "backend_attempt": deepcopy(specialist.get("result", {}).get("backend_attempt"))
            if isinstance(specialist.get("result"), Mapping)
            else None,
        },
        "boundary": {
            "claim_eligibility": "ineligible",
            "publication_enabled": False,
            "promotion_allowed": False,
            "non_claim": "Evidence identity and replay do not establish mathematical or scientific truth.",
        },
    }


def build_document_evidence_binding(
    packet: Mapping[str, Any],
    branches: list[Mapping[str, Any]],
    *,
    source_path: Path,
) -> dict[str, Any]:
    payload = _payload(packet, branches)
    digest = _sha256(canonical_json_bytes(payload))
    record = {
        **payload,
        "binding_id": f"document_binding_{digest}",
        "binding_digest": digest,
        "integrity_binding_status": "verified_current_evidence",
        "integrity_binding_verified": True,
    }
    return validate_document_evidence_binding(
        record,
        packet=packet,
        branches=branches,
        source_path=source_path,
    )


def validate_document_evidence_binding(
    value: Mapping[str, Any],
    *,
    packet: Mapping[str, Any],
    branches: list[Mapping[str, Any]],
    source_path: Path,
) -> dict[str, Any]:
    record = deepcopy(dict(value))
    digest = record.pop("binding_digest", None)
    binding_id = record.pop("binding_id", None)
    status = record.pop("integrity_binding_status", None)
    verified = record.pop("integrity_binding_verified", None)
    expected_payload = _payload(packet, branches)
    if record != expected_payload:
        raise EvidenceValidationError("document binding does not match the live source/branch packet")
    expected_digest = _sha256(canonical_json_bytes(expected_payload))
    if digest != expected_digest or binding_id != f"document_binding_{expected_digest}":
        raise EvidenceValidationError("document binding identity is stale or mutated")
    if status != "verified_current_evidence" or verified is not True:
        raise EvidenceValidationError("document binding status is not verified current evidence")
    raw = source_path.read_bytes()
    source = expected_payload["source"]
    if _sha256(raw) != source.get("source_digest"):
        raise EvidenceValidationError("document binding source digest is stale")
    start = source.get("span", {}).get("start_byte")
    end = source.get("span", {}).get("end_byte")
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(raw):
        raise EvidenceValidationError("document binding source span is invalid")

    obligation = packet.get("label_scoped_obligation")
    routing_role = packet.get("routing_role")
    if not isinstance(obligation, Mapping) or not isinstance(routing_role, Mapping):
        raise EvidenceValidationError("document binding requires exact obligation and routing-role records")
    validated_obligation = validate_label_scoped_obligation(obligation, source_bytes=raw)
    validated_role = validate_source_routing_role(
        routing_role,
        source_path=source_path,
        obligation=validated_obligation,
    )
    owned_spans = validated_obligation.get("owned_spans", [])
    expected_span = {
        "start_byte": owned_spans[0].get("start_byte") if owned_spans else None,
        "end_byte": owned_spans[-1].get("end_byte") if owned_spans else None,
    }
    if source.get("span") != expected_span:
        raise EvidenceValidationError("document binding span differs from the exact obligation")
    if source.get("file") != validated_obligation.get("document", {}).get("file"):
        raise EvidenceValidationError("document binding file differs from the exact obligation")
    if source.get("label") != validated_obligation.get("label"):
        raise EvidenceValidationError("document binding label differs from the exact obligation")
    expected_obligation = expected_payload["obligation"]
    if expected_obligation.get("id") != validated_obligation.get("obligation_id"):
        raise EvidenceValidationError("document binding obligation id mismatch")
    if expected_obligation.get("digest") != validated_obligation.get("obligation_digest"):
        raise EvidenceValidationError("document binding obligation digest mismatch")
    if expected_obligation.get("target") != validated_obligation.get("normalized_target", {}).get("display_text"):
        raise EvidenceValidationError("document binding target differs from the exact obligation")
    if expected_obligation.get("relation") != validated_obligation.get("normalized_target"):
        raise EvidenceValidationError("document binding relation differs from the exact obligation")
    if expected_obligation.get("routing_role") != validated_role:
        raise EvidenceValidationError("document binding routing role differs from verified source evidence")

    specialist = expected_payload["specialist"]
    if specialist.get("canonical_target") != expected_obligation.get("target"):
        raise EvidenceValidationError("document binding specialist target mismatch")
    backend_attempt = specialist.get("backend_attempt")
    if specialist.get("selected_tool") and not isinstance(backend_attempt, Mapping):
        raise EvidenceValidationError("selected specialist tool lacks a serializable native result")
    if expected_payload["boundary"] != {
        "claim_eligibility": "ineligible",
        "publication_enabled": False,
        "promotion_allowed": False,
        "non_claim": "Evidence identity and replay do not establish mathematical or scientific truth.",
    }:
        raise EvidenceValidationError("document binding crossed a claim or publication boundary")
    return {
        **expected_payload,
        "binding_id": binding_id,
        "binding_digest": digest,
        "integrity_binding_status": status,
        "integrity_binding_verified": verified,
    }
