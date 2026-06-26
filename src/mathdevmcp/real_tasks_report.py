from __future__ import annotations

"""Non-gating report surface for the real-task public benchmark manifest."""

from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .real_tasks_manifest import (
    load_real_task_public_manifest,
    validate_real_task_public_manifest,
)


def _count_by(items: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = item.get(field)
        key = str(value) if value is not None else "unknown"
        counts[key] = counts.get(key, 0) + 1
    return counts


def _count_by_nested(items: list[dict[str, Any]], parent: str, field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        nested = item.get(parent, {})
        value = nested.get(field) if isinstance(nested, dict) else None
        key = str(value) if value is not None else "unknown"
        counts[key] = counts.get(key, 0) + 1
    return counts


def real_task_public_report(root: str | Path | None = None, manifest_path: str | Path | None = None) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    manifest = load_real_task_public_manifest(root_path, manifest_path=manifest_path)
    validation = validate_real_task_public_manifest(root_path, manifest_path=manifest_path)
    cases = manifest.get("cases", [])
    manifest_status = manifest.get("status", "inconclusive")
    validation_status = validation.get("status", "inconclusive")
    findings = validation.get("findings", [])

    if manifest_status == "inconclusive":
        status = "inconclusive"
        reason = "Public real-task benchmark report is incomplete because the manifest did not load cleanly."
    elif validation_status != "consistent":
        status = "mismatch"
        reason = "Public real-task benchmark report found manifest validation issues."
    else:
        status = "consistent"
        reason = "Public real-task benchmark manifest is valid and summarized as a non-gating report."

    false_confidence_veto_cases = sum(
        1
        for case in cases
        if isinstance(case.get("gold"), dict) and case["gold"].get("false_confidence_veto") is True
    )

    summary = {
        "by_family": _count_by(cases, "family"),
        "by_repo": _count_by(cases, "repo"),
        "by_difficulty": _count_by(cases, "difficulty"),
        "by_evidence_class": _count_by_nested(cases, "gold", "evidence_class"),
        "by_expected_status": _count_by_nested(cases, "gold", "expected_status"),
        "false_confidence_veto_cases": false_confidence_veto_cases,
    }

    policy_boundary = [
        "This report summarizes the committed public benchmark corpus only.",
        "This is not benchmark execution evidence.",
        "This is not holdout-local or private-external evaluation evidence.",
        "This is not release-readiness evidence.",
        "No pass/fail gate is implied by this report.",
    ]

    warnings: list[str] = []
    if len(cases) < 5:
        warnings.append("Public corpus is still small; summary counts are only early-slice inventory signals.")
    if findings:
        warnings.append("Manifest validation findings are present; treat the summary as diagnostic-only until they are resolved.")

    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "manifest_status": manifest_status,
            "validation_status": validation_status,
            "public_case_total": len(cases),
            "summary": summary,
            "findings": findings,
            "warnings": warnings,
            "policy_boundary": policy_boundary,
            "manifest": manifest,
        },
        "real_task_public_report",
    )
