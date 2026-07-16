from __future__ import annotations

"""Validate source-evidenced claim roles before they affect proof routing."""

import hashlib
from pathlib import Path
import re
from typing import Any, Mapping

from .contracts import attach_contract


CLAIM_ROLES = frozenset(
    {"theorem", "definition", "identity", "assumption", "estimator", "diagnostic"}
)
ROLE_AUTHORITIES = frozenset(
    {"source_evidenced_role", "caller_asserted_role", "role_ambiguous"}
)
ROUTING_ROLES = frozenset({"definition", "identity"})

_ROLE_CUES = {
    "definition": (
        re.compile(r"\bdefin(?:e|es|ed|ition)\b", re.IGNORECASE),
        re.compile(r"\binitial convention\b", re.IGNORECASE),
        re.compile(r"\btransparent placeholder\b", re.IGNORECASE),
    ),
    "identity": (
        re.compile(r"\bidentity layer\b", re.IGNORECASE),
        re.compile(r"\baccounting identit(?:y|ies)\b", re.IGNORECASE),
        re.compile(r"\bdefines?\b", re.IGNORECASE),
    ),
    "assumption": (re.compile(r"\bassum(?:e|es|ed|ption)\b", re.IGNORECASE),),
    "estimator": (re.compile(r"\bestimat(?:e|es|ed|or|ion)\b", re.IGNORECASE),),
    "diagnostic": (re.compile(r"\bdiagnostic\b", re.IGNORECASE),),
    "theorem": (
        re.compile(r"\btheorem\b", re.IGNORECASE),
        re.compile(r"\bproposition\b", re.IGNORECASE),
        re.compile(r"\blemma\b", re.IGNORECASE),
    ),
}


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _diagnostic(
    *,
    status: str,
    role: str,
    requested_authority: str,
    effective_authority: str,
    routing_effect: str,
    reason: str,
    source: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    source = source or {}
    public_source = {
        key: source[key]
        for key in ("file", "source_digest", "span_start", "span_end", "span_digest", "source_target_digest", "label")
        if key in source
    }
    return attach_contract(
        {
            "status": status,
            "role": role,
            "requested_authority": requested_authority,
            "effective_authority": effective_authority,
            "routing_effect": routing_effect,
            "reason": reason,
            "source": public_source,
            "non_claims": [
                "Claim-role evidence controls routing only; it is not a proof certificate.",
                "A source definition or identity is not thereby economically or scientifically valid.",
            ],
        },
        "claim_semantics_validation",
    )


def validate_claim_semantics(
    value: Mapping[str, Any] | None,
    *,
    routed_target: str | None = None,
) -> dict[str, Any]:
    """Return the closed routing decision for optional claim-role metadata."""
    if value is None:
        return _diagnostic(
            status="generic_theorem_route",
            role="theorem",
            requested_authority="none",
            effective_authority="implicit_generic_theorem",
            routing_effect="ordinary_proof_or_counterexample",
            reason="No source-evidenced claim role was supplied; generic equality semantics apply.",
        )
    if not isinstance(value, Mapping):
        raise ValueError("claim_semantics must be an object")
    role = str(value.get("role", "")).strip()
    authority = str(value.get("authority", "")).strip()
    if role not in CLAIM_ROLES:
        raise ValueError(f"unsupported claim role: {role or '<empty>'}")
    if authority not in ROLE_AUTHORITIES:
        raise ValueError(f"unsupported claim-role authority: {authority or '<empty>'}")
    if authority == "caller_asserted_role":
        return _diagnostic(
            status="caller_assertion_only",
            role=role,
            requested_authority=authority,
            effective_authority="caller_asserted_role",
            routing_effect="ordinary_proof_or_counterexample",
            reason="Caller-asserted roles are diagnostic context and cannot alter proof routing.",
        )
    if authority == "role_ambiguous":
        return _diagnostic(
            status="role_ambiguous",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason="The claim role is ambiguous and requires exact source evidence before routing.",
        )

    source_path = value.get("source_path")
    source_digest = str(value.get("source_digest", ""))
    span = value.get("source_span")
    if not isinstance(source_path, str) or not source_path:
        raise ValueError("source_evidenced_role requires source_path")
    if not re.fullmatch(r"[0-9a-f]{64}", source_digest):
        raise ValueError("source_evidenced_role requires a lowercase SHA-256 source_digest")
    if not isinstance(span, Mapping):
        raise ValueError("source_evidenced_role requires source_span")
    try:
        start = int(span["start_byte"])
        end = int(span["end_byte"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("source_span requires integer start_byte and end_byte") from exc
    span_digest = str(span.get("sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", span_digest):
        raise ValueError("source_span requires a lowercase SHA-256 sha256")
    source_target = value.get("source_target")
    if not isinstance(source_target, str) or not source_target.strip():
        raise ValueError("source_evidenced_role requires a non-empty source_target")
    source_target_digest = str(value.get("source_target_digest", ""))
    if source_target_digest != _sha256(source_target.encode("utf-8")):
        raise ValueError("source_target_digest does not match source_target")
    path = Path(source_path).expanduser().resolve(strict=True)
    raw = path.read_bytes()
    public_source = {
        "file": path.name,
        "source_digest": source_digest,
        "span_start": start,
        "span_end": end,
        "span_digest": span_digest,
        "source_target_digest": source_target_digest,
    }
    label = value.get("label")
    if isinstance(label, str) and label:
        public_source["label"] = label
    if _sha256(raw) != source_digest:
        return _diagnostic(
            status="source_identity_mismatch",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason="The current source bytes do not match the supplied source digest.",
            source=public_source,
        )
    if not 0 <= start < end <= len(raw):
        raise ValueError("source_span is outside the source byte range")
    evidence_bytes = raw[start:end]
    if _sha256(evidence_bytes) != span_digest:
        return _diagnostic(
            status="source_span_mismatch",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason="The current source span does not match the supplied span digest.",
            source=public_source,
        )
    evidence_text = evidence_bytes.decode("utf-8", errors="strict")
    if source_target not in evidence_text:
        return _diagnostic(
            status="source_target_not_evidenced",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason="The exact source span does not contain the declared source target.",
            source=public_source,
        )
    if routed_target is not None and routed_target != source_target:
        return _diagnostic(
            status="source_target_routing_mismatch",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason="The routed workflow target is not exactly the validated source target.",
            source=public_source,
        )
    if not any(pattern.search(evidence_text) for pattern in _ROLE_CUES[role]):
        return _diagnostic(
            status="source_role_not_evidenced",
            role=role,
            requested_authority=authority,
            effective_authority="role_ambiguous",
            routing_effect="block_pending_source_role_evidence",
            reason=f"The exact source span does not contain a recognized {role} role cue.",
            source=public_source,
        )
    routing_effect = (
        "source_definition_or_identity_route"
        if role in ROUTING_ROLES
        else "ordinary_proof_or_counterexample"
    )
    return _diagnostic(
        status="source_role_validated",
        role=role,
        requested_authority=authority,
        effective_authority="source_evidenced_role",
        routing_effect=routing_effect,
        reason="The exact current source span independently evidences the requested claim role.",
        source=public_source,
    )


def source_role_controls_routing(result: Mapping[str, Any]) -> bool:
    return (
        result.get("effective_authority") == "source_evidenced_role"
        and result.get("role") in ROUTING_ROLES
        and result.get("routing_effect") == "source_definition_or_identity_route"
    )
