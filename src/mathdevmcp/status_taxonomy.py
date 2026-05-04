"""Shared status/substatus helpers for conservative workflow reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from .contracts import attach_contract


TopLevelStatus = Literal["verified", "consistent", "mismatch", "unverified", "inconclusive"]


@dataclass(frozen=True)
class StatusClassification:
    status: str
    substatus: str
    severity: str
    reason: str
    actions: list[dict]


SUBSTATUS_SEVERITY: dict[str, str] = {
    "verified:deterministic_backend": "none",
    "consistent:diagnostic_supported": "low",
    "unverified:missing_assumption": "high",
    "unverified:missing_shape": "high",
    "unverified:parser_limit": "high",
    "unverified:unsupported_noncommutative_algebra": "high",
    "unverified:manual_formalization_required": "medium",
    "mismatch:likely_formula_error": "high",
    "mismatch:normalization_gap": "high",
    "inconclusive:source_label_missing": "high",
    "inconclusive:partial_index_only": "medium",
    "inconclusive:backend_unavailable": "medium",
    "inconclusive:toolchain_not_ready": "medium",
    "inconclusive:timeout": "medium",
}


def status_taxonomy() -> dict:
    """Return the public status taxonomy as a contract-bearing payload."""

    return attach_contract(
        {
            "status": "consistent",
            "reason": "Status taxonomy is available.",
            "top_level_statuses": ["verified", "consistent", "mismatch", "unverified", "inconclusive"],
            "substatuses": [
                {"substatus": substatus, "severity": severity}
                for substatus, severity in sorted(SUBSTATUS_SEVERITY.items())
            ],
        },
        "status_taxonomy",
    )


def action(kind: str, reason: str, *, severity: str = "medium", target: str | None = None) -> dict:
    result = {"kind": kind, "severity": severity, "reason": reason}
    if target is not None:
        result["target"] = target
    return result


def classify_status(
    status: str,
    reason: str,
    *,
    parser_policy: dict | None = None,
    base_obligation: dict | None = None,
    route: dict | None = None,
    shape: dict | None = None,
    actions: list[dict] | None = None,
) -> dict:
    """Classify a report with an additive substatus and next-action list."""

    parser_policy = parser_policy or {}
    base_obligation = base_obligation or {}
    route = route or {}
    shape = shape or {}
    next_actions = list(actions or [])

    if status == "verified":
        substatus = "verified:deterministic_backend"
    elif status == "consistent":
        substatus = "consistent:diagnostic_supported"
    elif status == "mismatch":
        evidence_text = " ".join(str(item) for item in base_obligation.get("evidence", []))
        if "normalization" in reason.lower() or "normalization" in evidence_text.lower():
            substatus = "mismatch:normalization_gap"
        else:
            substatus = "mismatch:likely_formula_error"
    elif parser_policy.get("status") not in {"", None, "selected", "selected_for_proof_audit"}:
        substatus = "unverified:parser_limit" if status == "unverified" else "inconclusive:source_label_missing"
    elif base_obligation.get("classification") == "not_extracted":
        substatus = "unverified:parser_limit" if status == "unverified" else "inconclusive:source_label_missing"
    elif shape.get("missing_constraints"):
        missing_kinds = {item.get("kind") for item in shape.get("missing_constraints", [])}
        substatus = "unverified:missing_shape" if any("shape" in str(kind) or "square" in str(kind) for kind in missing_kinds) else "unverified:missing_assumption"
    elif route.get("route") == "human_review":
        substatus = "unverified:manual_formalization_required"
    elif "timeout" in reason.lower() or "timed out" in reason.lower():
        substatus = "inconclusive:timeout"
    elif "backend" in reason.lower() or "toolchain" in reason.lower():
        substatus = "inconclusive:backend_unavailable" if "backend" in reason.lower() else "inconclusive:toolchain_not_ready"
    elif status == "unverified":
        substatus = "unverified:manual_formalization_required"
    else:
        substatus = "inconclusive:backend_unavailable"

    if not next_actions and status not in {"verified", "consistent"}:
        next_actions.append(action("inspect_status_blocker", reason, severity=SUBSTATUS_SEVERITY.get(substatus, "medium")))
    classification = StatusClassification(
        status=status,
        substatus=substatus,
        severity=SUBSTATUS_SEVERITY.get(substatus, "medium"),
        reason=reason,
        actions=next_actions,
    )
    return asdict(classification)
