from __future__ import annotations

"""Bind source-local mathematical routing roles without asserting truth."""

from copy import deepcopy
import hashlib
from pathlib import Path
import re
from typing import Any, Mapping

from .evidence_manifest import EvidenceValidationError, canonical_json_bytes


ROLE_SCHEMA_VERSION = "1.0"
ROUTING_ROLES = frozenset(
    {
        "definition",
        "accounting_identity",
        "placeholder_definition",
        "policy_value_recursion",
        "causal_estimand_object",
        "identification_assumption",
        "statistical_estimator",
        "theorem_proposition",
        "diagnostic_expression",
        "unsupported_or_ambiguous",
    }
)
_ROLE_PATTERNS: tuple[tuple[str, tuple[re.Pattern[str], ...]], ...] = (
    (
        "identification_assumption",
        (
            re.compile(r"\bidentification assumptions?\b", re.IGNORECASE),
            re.compile(r"\brequired condition\b", re.IGNORECASE),
            re.compile(r"\bassignment is independent\b", re.IGNORECASE),
        ),
    ),
    (
        "policy_value_recursion",
        (
            re.compile(r"\bBellman recursion\b", re.IGNORECASE),
            re.compile(r"\bpolicy-value object\b", re.IGNORECASE),
            re.compile(r"\bdiscounted value is\b", re.IGNORECASE),
        ),
    ),
    (
        "causal_estimand_object",
        (
            re.compile(r"\bcausal object\b", re.IGNORECASE),
            re.compile(r"\bcausal-inference literature\b", re.IGNORECASE),
        ),
    ),
    (
        "accounting_identity",
        (
            re.compile(r"\bstock-flow identity\b", re.IGNORECASE),
            re.compile(r"\bexpected-loss identity\b", re.IGNORECASE),
            re.compile(r"\b(?:incremental )?cash-flow primitive\b", re.IGNORECASE),
            re.compile(r"\bidentity object\b", re.IGNORECASE),
        ),
    ),
    (
        "placeholder_definition",
        (
            re.compile(r"\btransparent placeholder\b", re.IGNORECASE),
            re.compile(r"\binitial convention\b", re.IGNORECASE),
            re.compile(r"\bterminal value should be explicit\b", re.IGNORECASE),
        ),
    ),
    (
        "statistical_estimator",
        (
            re.compile(r"\bestimat(?:e|es|ed|or|ion)\b", re.IGNORECASE),
            re.compile(r"\bestimand\b", re.IGNORECASE),
            re.compile(r"\bcomplier (?:or )?local-average-treatment effect\b", re.IGNORECASE),
        ),
    ),
    ("theorem_proposition", (re.compile(r"\b(?:theorem|proposition|lemma)\b", re.IGNORECASE),)),
    ("diagnostic_expression", (re.compile(r"\bdiagnostic expression\b", re.IGNORECASE),)),
    ("definition", (re.compile(r"\bdefin(?:e|es|ed|ition)\b", re.IGNORECASE),)),
)


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _context_span(raw: bytes, start: int, end: int) -> tuple[int, int]:
    before = raw.rfind(b"\n\n", 0, start)
    before = 0 if before < 0 else before + 2
    before2 = raw.rfind(b"\n\n", 0, before - 2) if before > 2 else -1
    if before2 >= 0:
        before = before2 + 2
    after = raw.find(b"\n\n", end)
    after = len(raw) if after < 0 else after
    after2 = raw.find(b"\n\n", after + 2) if after < len(raw) else -1
    if after2 >= 0:
        after = after2
    return before, after


def _distance(match_start: int, match_end: int, target_start: int, target_end: int) -> int:
    if match_end <= target_start:
        return target_start - match_end
    if match_start >= target_end:
        return match_start - target_end
    return 0


def infer_source_routing_role(source_path: Path, obligation: Mapping[str, Any]) -> dict[str, Any]:
    """Infer a routing-only role from the nearest exact source cue."""
    raw = source_path.read_bytes()
    document = obligation.get("document", {})
    if _sha256(raw) != document.get("source_digest"):
        raise EvidenceValidationError("routing-role source bytes do not match the obligation")
    environment = obligation.get("environment", {})
    target_start = int(environment["start_byte"])
    target_end = int(environment["end_byte"])
    context_start, context_end = _context_span(raw, target_start, target_end)
    context_raw = raw[context_start:context_end]
    context = context_raw.decode("utf-8", errors="strict")
    candidates: list[dict[str, Any]] = []
    for priority, (role, patterns) in enumerate(_ROLE_PATTERNS):
        for pattern in patterns:
            for match in pattern.finditer(context):
                start = context_start + len(context[: match.start()].encode("utf-8"))
                end = context_start + len(context[: match.end()].encode("utf-8"))
                candidates.append(
                    {
                        "role": role,
                        "priority": priority,
                        "start_byte": start,
                        "end_byte": end,
                        "distance": _distance(start, end, target_start, target_end),
                        "cue_text": match.group(0),
                    }
                )
    candidates.sort(key=lambda item: (item["distance"], item["priority"], item["start_byte"], item["role"]))
    selected = candidates[0] if candidates else None
    if selected is None:
        role = "unsupported_or_ambiguous"
        status = "role_ambiguous"
        authority = "role_ambiguous"
        routing_effect = "block_pending_source_role_evidence"
        cue_start, cue_end, cue_text = context_start, context_end, ""
    else:
        role = str(selected["role"])
        status = "source_role_validated"
        authority = "source_evidenced_role"
        routing_effect = f"route_{role}"
        cue_start, cue_end, cue_text = int(selected["start_byte"]), int(selected["end_byte"]), str(selected["cue_text"])
    payload = {
        "schema_version": ROLE_SCHEMA_VERSION,
        "status": status,
        "role": role,
        "authority": authority,
        "routing_effect": routing_effect,
        "obligation_digest": obligation.get("obligation_digest"),
        "source": {
            "file": document.get("file"),
            "source_digest": document.get("source_digest"),
            "context_start": context_start,
            "context_end": context_end,
            "context_digest": _sha256(context_raw),
            "cue_start": cue_start,
            "cue_end": cue_end,
            "cue_digest": _sha256(raw[cue_start:cue_end]),
            "cue_text": cue_text,
        },
        "non_claims": [
            "The role controls routing only and does not establish mathematical, causal, empirical, or economic validity.",
            "A source-stated assumption is not thereby satisfied.",
        ],
    }
    digest = _sha256(canonical_json_bytes(payload))
    record = {**payload, "role_id": f"role_{digest}", "role_digest": digest}
    return validate_source_routing_role(record, source_path=source_path, obligation=obligation)


def validate_source_routing_role(
    value: Mapping[str, Any],
    *,
    source_path: Path,
    obligation: Mapping[str, Any],
) -> dict[str, Any]:
    record = deepcopy(dict(value))
    role = record.get("role")
    if role not in ROUTING_ROLES:
        raise EvidenceValidationError("routing role is outside the closed registry")
    digest = record.pop("role_digest", None)
    role_id = record.pop("role_id", None)
    expected = _sha256(canonical_json_bytes(record))
    if digest != expected or role_id != f"role_{expected}":
        raise EvidenceValidationError("routing-role identity does not match its canonical payload")
    if record.get("obligation_digest") != obligation.get("obligation_digest"):
        raise EvidenceValidationError("routing role is bound to a different obligation")
    raw = source_path.read_bytes()
    source = record.get("source", {})
    if _sha256(raw) != source.get("source_digest"):
        raise EvidenceValidationError("routing-role source digest mismatch")
    context_start, context_end = int(source["context_start"]), int(source["context_end"])
    cue_start, cue_end = int(source["cue_start"]), int(source["cue_end"])
    if not 0 <= context_start <= cue_start < cue_end <= context_end <= len(raw):
        raise EvidenceValidationError("routing-role spans are invalid")
    if _sha256(raw[context_start:context_end]) != source.get("context_digest"):
        raise EvidenceValidationError("routing-role context digest mismatch")
    if _sha256(raw[cue_start:cue_end]) != source.get("cue_digest"):
        raise EvidenceValidationError("routing-role cue digest mismatch")
    return {**record, "role_id": role_id, "role_digest": digest}
