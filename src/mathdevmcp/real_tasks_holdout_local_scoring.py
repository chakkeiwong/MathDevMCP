from __future__ import annotations

"""Local-only holdout scoring over explicitly provided candidate answers."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .real_tasks_holdout_local import (
    _default_local_holdout_candidate_answers_path,
    _default_local_holdout_path,
)
from .real_tasks_scoring import score_real_task_case


@dataclass(frozen=True)
class RealTaskHoldoutLocalScoreReport:
    ok: bool
    results: list[dict[str, Any]]
    summary: dict[str, Any]
    metadata: dict[str, str]


def _load_local_holdout_cases(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    return cases if isinstance(cases, list) else []


def _load_local_holdout_candidate_answers(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    fixtures = payload.get("fixtures", [])
    if not isinstance(fixtures, list):
        return []
    return [fixture.get("candidate") for fixture in fixtures if isinstance(fixture, dict) and isinstance(fixture.get("candidate"), dict)]


def score_local_holdout_candidates(
    candidates: list[dict[str, Any]],
    *,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    default_path = _default_local_holdout_path(root_path)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_path

    if not path.exists():
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "No local holdout manifest was found for scoring. This is expected until a local holdout inventory is populated.",
                "path": str(path),
                "results": [],
                "summary": {
                    "holdout_case_total": 0,
                    "scored_candidate_total": 0,
                    "missing_candidate_case_ids": [],
                    "by_status": {},
                    "by_case_family": {},
                    "false_confidence_veto_failures": 0,
                    "local_only": True,
                },
                "policy_boundary": [
                    "This is local holdout scoring only.",
                    "It is not public benchmark evidence.",
                    "Absence of a local holdout manifest is not a benchmark failure.",
                    "It is not benchmark-gate evidence.",
                    "It is not release-readiness evidence.",
                ],
            },
            "real_task_holdout_local_score_report",
        )

    cases = _load_local_holdout_cases(path)
    case_by_id = {case.get("id"): case for case in cases if isinstance(case, dict) and isinstance(case.get("id"), str)}

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
                        "reason": "Candidate does not reference a known local holdout case.",
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

    payload = asdict(
        RealTaskHoldoutLocalScoreReport(
            ok=True,
            results=results,
            summary={
                "holdout_case_total": len(case_by_id),
                "scored_candidate_total": len(results),
                "missing_candidate_case_ids": missing_candidates,
                "by_status": by_status,
                "by_case_family": by_case_family,
                "false_confidence_veto_failures": false_confidence_veto_failures,
                "local_only": True,
            },
            metadata={"schema_version": "1.0", "contract": "real_task_holdout_local_score_report"},
        )
    )
    payload["path"] = str(path)
    payload["policy_boundary"] = [
        "This is local holdout scoring only.",
        "It is not public benchmark evidence.",
        "It is not benchmark-gate evidence.",
        "It is not release-readiness evidence.",
        "Local holdout artifacts should not be committed by default.",
    ]
    return payload


def score_local_holdout_candidate_fixtures(
    *,
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    candidate_path: str | Path | None = None,
) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    default_candidate_path = _default_local_holdout_candidate_answers_path(root_path)
    path = Path(candidate_path).resolve() if candidate_path is not None else default_candidate_path

    if not path.exists():
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "No local holdout candidate-answer file was found for scoring. This is expected until a local candidate fixture file is populated.",
                "path": str(path),
                "results": [],
                "summary": {
                    "scored_candidate_total": 0,
                    "local_only": True,
                },
                "policy_boundary": [
                    "This is local holdout fixture scoring only.",
                    "It is not public benchmark evidence.",
                    "Absence of a local candidate-answer file is not a benchmark failure.",
                    "It is not benchmark-gate evidence.",
                    "It is not release-readiness evidence.",
                ],
            },
            "real_task_holdout_local_score_report",
        )

    candidates = _load_local_holdout_candidate_answers(path)
    report = score_local_holdout_candidates(candidates, root=root_path, manifest_path=manifest_path)
    report["candidate_path"] = str(path)
    report["policy_boundary"] = [
        "This is local holdout fixture scoring only.",
        "It is not public benchmark evidence.",
        "It is not benchmark-gate evidence.",
        "It is not release-readiness evidence.",
        "Local holdout artifacts should not be committed by default.",
    ]
    return report
