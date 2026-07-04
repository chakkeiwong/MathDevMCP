from __future__ import annotations

"""Batch non-gating scored report for real-task structural scoring."""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .real_tasks_manifest import load_real_task_public_manifest
from .real_tasks_scoring import score_real_task_case


@dataclass(frozen=True)
class RealTaskScoredReport:
    ok: bool
    results: list[dict[str, Any]]
    summary: dict[str, Any]
    metadata: dict[str, str]


def score_real_task_public_candidates(
    candidates: list[dict[str, Any]],
    *,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    manifest = load_real_task_public_manifest(root_path, manifest_path=manifest_path)
    cases = manifest.get("cases", [])
    case_by_id = {case["id"]: case for case in cases}

    results: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    for candidate in candidates:
        case_id = candidate.get("case_id")
        if not isinstance(case_id, str) or case_id not in case_by_id:
            results.append(
                attach_contract(
                    {
                        "case_id": case_id if isinstance(case_id, str) else "<unknown>",
                        "status": "inconclusive",
                        "reason": "Candidate does not reference a known public real-task benchmark case.",
                        "quality_checks": {
                            "expected_status_match": False,
                            "expected_substatus_match": False,
                            "expected_labels_present": False,
                            "required_terms_present": False,
                            "forbidden_claims_absent": False,
                            "required_next_actions_present": False,
                            "evidence_class_match": False,
                            "false_confidence_veto_clear": False,
                        },
                        "details": {"candidate": candidate},
                    },
                    "real_task_case_structural_score",
                )
            )
            continue
        seen_case_ids.add(case_id)
        results.append(score_real_task_case(case_by_id[case_id], candidate))

    missing_candidates = sorted(set(case_by_id) - seen_case_ids)
    by_status: dict[str, int] = {}
    by_case_family: dict[str, dict[str, int]] = {}
    false_confidence_veto_failures = 0
    for result in results:
        status = str(result.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        case = case_by_id.get(result.get("case_id"))
        if case is not None:
            family = str(case.get("family", "unknown"))
            bucket = by_case_family.setdefault(family, {"total": 0, "consistent": 0, "mismatch": 0, "inconclusive": 0})
            bucket["total"] += 1
            bucket[status] = bucket.get(status, 0) + 1
        quality = result.get("quality_checks", {}) if isinstance(result.get("quality_checks", {}), dict) else {}
        if quality.get("false_confidence_veto_clear") is False:
            false_confidence_veto_failures += 1

    warnings: list[str] = []
    if missing_candidates:
        warnings.append("Not all public cases received candidate answers in this scored report.")

    summary = {
        "public_case_total": len(cases),
        "scored_candidate_total": len(results),
        "missing_candidate_case_ids": missing_candidates,
        "by_status": by_status,
        "by_case_family": by_case_family,
        "false_confidence_veto_failures": false_confidence_veto_failures,
        "non_gating": True,
    }

    payload = asdict(
        RealTaskScoredReport(
            ok=True,
            results=results,
            summary=summary,
            metadata={"schema_version": "1.0", "contract": "real_task_structural_score_report"},
        )
    )
    payload["warnings"] = warnings
    payload["policy_boundary"] = [
        "This is a non-gating scored report over normalized candidate answers.",
        "It reflects only structural scoring against public-manifest gold fields.",
        "It is not semantic benchmark execution over free-form model outputs.",
        "It is not holdout-local or private-external evidence.",
        "It is not release-readiness evidence.",
    ]
    return payload
