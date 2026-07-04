from __future__ import annotations

"""Compare explicitly supplied theorem assumptions with a local setting."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract


@dataclass(frozen=True)
class AssumptionComparison:
    assumption_id: str
    theorem_text: str
    local_text: str
    status: str
    reason: str


@dataclass(frozen=True)
class LiteratureLocalAuditResult:
    status: str
    reason: str
    theorem_id: str
    local_context: str
    matched_assumptions: list[dict[str, Any]]
    missing_assumptions: list[dict[str, Any]]
    conflicting_assumptions: list[dict[str, Any]]
    unreviewed_assumptions: list[dict[str, Any]]
    notation_notes: list[dict[str, Any]]
    applicability_boundary: str


def _assumption_id(record: dict[str, Any]) -> str:
    for key in ("id", "name", "assumption_id"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    text = str(record.get("text", ""))
    return "text:" + " ".join(text.lower().split())[:80]


def _text(record: dict[str, Any]) -> str:
    return str(record.get("text") or record.get("statement") or record.get("name") or "")


def _status(record: dict[str, Any]) -> str:
    value = record.get("status")
    return value if isinstance(value, str) else "asserted"


def literature_local_audit(
    theorem_id: str,
    theorem_assumptions: list[dict[str, Any]],
    local_assumptions: list[dict[str, Any]],
    *,
    local_context: str = "local",
    notation_audit: dict[str, Any] | None = None,
    human_waivers: list[str] | None = None,
) -> dict:
    if not all(isinstance(item, dict) for item in theorem_assumptions):
        raise ValueError("theorem_assumptions must be a list of objects")
    if not all(isinstance(item, dict) for item in local_assumptions):
        raise ValueError("local_assumptions must be a list of objects")
    waiver_set = set(human_waivers or [])
    local_by_id = {_assumption_id(item): item for item in local_assumptions}
    matched: list[AssumptionComparison] = []
    missing: list[AssumptionComparison] = []
    conflicts: list[AssumptionComparison] = []
    unreviewed: list[AssumptionComparison] = []

    for theorem in theorem_assumptions:
        assumption_id = _assumption_id(theorem)
        local = local_by_id.get(assumption_id)
        theorem_text = _text(theorem)
        if local is None:
            if assumption_id in waiver_set:
                unreviewed.append(
                    AssumptionComparison(
                        assumption_id=assumption_id,
                        theorem_text=theorem_text,
                        local_text="",
                        status="waived_unreviewed",
                        reason="A human waiver id was supplied, but applicability remains unreviewed.",
                    )
                )
            else:
                missing.append(
                    AssumptionComparison(
                        assumption_id=assumption_id,
                        theorem_text=theorem_text,
                        local_text="",
                        status="missing",
                        reason="The theorem assumption was not found in local assumptions.",
                    )
                )
            continue
        local_text = _text(local)
        local_status = _status(local)
        if local_status in {"conflict", "contradicted", "mismatch"}:
            conflicts.append(
                AssumptionComparison(
                    assumption_id=assumption_id,
                    theorem_text=theorem_text,
                    local_text=local_text,
                    status="conflict",
                    reason="The local assumption record explicitly conflicts with the theorem assumption.",
                )
            )
        elif local_status in {"unreviewed", "unknown"}:
            unreviewed.append(
                AssumptionComparison(
                    assumption_id=assumption_id,
                    theorem_text=theorem_text,
                    local_text=local_text,
                    status="unreviewed",
                    reason="The local assumption is present but not reviewed.",
                )
            )
        else:
            matched.append(
                AssumptionComparison(
                    assumption_id=assumption_id,
                    theorem_text=theorem_text,
                    local_text=local_text,
                    status="matched",
                    reason="The local assumption record matches the theorem assumption id.",
                )
            )

    notation_notes: list[dict[str, Any]] = []
    if notation_audit:
        notation_notes.extend(notation_audit.get("conflicts", []))
        notation_notes.extend(notation_audit.get("unresolved_symbols", []))

    if conflicts or notation_audit and notation_audit.get("status") == "conflict":
        status = "applicability_conflict"
        reason = "The theorem has conflicting local assumptions or notation conflicts."
    elif missing:
        status = "applicability_gap"
        reason = "The theorem has required assumptions missing from the local setting."
    elif unreviewed or notation_notes:
        status = "applicability_unreviewed"
        reason = "All required assumptions are present or waived, but some items require review."
    else:
        status = "applicability_supported"
        reason = "Explicit theorem assumptions match local assumptions and no notation conflicts were supplied."

    result = LiteratureLocalAuditResult(
        status=status,
        reason=reason,
        theorem_id=theorem_id,
        local_context=local_context,
        matched_assumptions=[asdict(item) for item in matched],
        missing_assumptions=[asdict(item) for item in missing],
        conflicting_assumptions=[asdict(item) for item in conflicts],
        unreviewed_assumptions=[asdict(item) for item in unreviewed],
        notation_notes=notation_notes,
        applicability_boundary=(
            "This audit compares explicitly supplied theorem and local assumptions only. "
            "It does not verify the paper theorem, fetch literature, or establish local scientific validity."
        ),
    )
    return attach_contract(asdict(result), "literature_local_audit_result")
