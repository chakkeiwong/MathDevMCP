import json
from pathlib import Path

from mathdevmcp.real_tasks_holdout_local_scoring import (
    score_local_holdout_candidate_fixtures,
    score_local_holdout_candidates,
)


ROOT = Path(__file__).resolve().parent.parent


def _local_case() -> dict:
    return {
        "id": "HOLDOUT-CASE-001",
        "family": "retrieval_and_provenance",
        "repo": "latex-papers",
        "task_type": "local_holdout_example",
        "difficulty": "hard",
        "public": False,
        "document_roots": ["../latex-papers/CIP_monograph"],
        "document_files": ["../latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex"],
        "code_roots": [],
        "code_files": [],
        "labels": [],
        "prompt": "Example local holdout prompt.",
        "gold": {
            "expected_status": "unverified",
            "expected_substatus": "local_holdout_candidate_only",
            "expected_labels": [],
            "required_terms": ["chapter neighborhood", "provenance"],
            "forbidden_claims": ["This local holdout entry proves benchmark generalization."],
            "required_next_actions": ["Keep this case local until a deliberate public-promotion decision is made."],
            "evidence_class": "holdout_local_example",
            "false_confidence_veto": True,
        },
        "notes": "Local-only example.",
        "holdout_reason": "Example holdout reason.",
        "disjointness_axes": ["different_label_neighborhood", "different_task_template"],
    }


def test_holdout_local_scoring_is_inconclusive_when_no_local_manifest_exists(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    result = score_local_holdout_candidates([], root=ROOT, manifest_path=path)

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_holdout_local_score_report",
    }
    assert result["status"] == "inconclusive"
    assert result["summary"]["local_only"] is True


def test_holdout_local_scoring_scores_valid_local_case(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    path.write_text(json.dumps({"cases": [_local_case()]}), encoding="utf-8")
    result = score_local_holdout_candidates(
        [
            {
                "case_id": "HOLDOUT-CASE-001",
                "status": "unverified",
                "substatus": "local_holdout_candidate_only",
                "labels": [],
                "evidence_class": "holdout_local_example",
                "summary_text": "chapter neighborhood provenance",
                "claims": ["safe local holdout summary"],
                "next_actions": ["Keep this case local until a deliberate public-promotion decision is made."],
            }
        ],
        root=ROOT,
        manifest_path=path,
    )

    assert result["ok"] is True
    assert result["summary"]["holdout_case_total"] == 1
    assert result["summary"]["by_status"]["consistent"] == 1


def test_holdout_local_scoring_reports_mismatch_for_violating_candidate(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    path.write_text(json.dumps({"cases": [_local_case()]}), encoding="utf-8")
    result = score_local_holdout_candidates(
        [
            {
                "case_id": "HOLDOUT-CASE-001",
                "status": "unverified",
                "substatus": "local_holdout_candidate_only",
                "labels": [],
                "evidence_class": "holdout_local_example",
                "summary_text": "chapter neighborhood provenance",
                "claims": ["This local holdout entry proves benchmark generalization."],
                "next_actions": ["Keep this case local until a deliberate public-promotion decision is made."],
            }
        ],
        root=ROOT,
        manifest_path=path,
    )

    assert result["ok"] is True
    assert result["summary"]["by_status"]["mismatch"] == 1
    assert result["summary"]["false_confidence_veto_failures"] == 1


def test_holdout_local_scoring_preserves_local_only_policy_boundary(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    result = score_local_holdout_candidates([], root=ROOT, manifest_path=path)
    text = " ".join(result["policy_boundary"])

    assert "local holdout scoring only" in text
    assert "not public benchmark evidence" in text
    assert "not release-readiness evidence" in text


def test_holdout_local_fixture_runner_is_inconclusive_when_no_local_candidate_file_exists(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    path.write_text(json.dumps({"cases": [_local_case()]}), encoding="utf-8")
    candidate_path = tmp_path / "holdout_local_candidate_answers.json"
    result = score_local_holdout_candidate_fixtures(root=ROOT, manifest_path=path, candidate_path=candidate_path)

    assert result["status"] == "inconclusive"
    assert result["summary"]["scored_candidate_total"] == 0


def test_holdout_local_fixture_runner_scores_temp_local_manifest_and_candidates(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    path.write_text(json.dumps({"cases": [_local_case()]}), encoding="utf-8")
    candidate_path = tmp_path / "holdout_local_candidate_answers.json"
    candidate_path.write_text(
        json.dumps(
            {
                "fixtures": [
                    {
                        "id": "fixture-holdout-001",
                        "case_id": "HOLDOUT-CASE-001",
                        "candidate": {
                            "case_id": "HOLDOUT-CASE-001",
                            "status": "unverified",
                            "substatus": "local_holdout_candidate_only",
                            "labels": [],
                            "evidence_class": "holdout_local_example",
                            "summary_text": "chapter neighborhood provenance",
                            "claims": ["safe local holdout summary"],
                            "next_actions": ["Keep this case local until a deliberate public-promotion decision is made."],
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    result = score_local_holdout_candidate_fixtures(root=ROOT, manifest_path=path, candidate_path=candidate_path)

    assert result["ok"] is True
    assert result["summary"]["scored_candidate_total"] == 1
    assert result["summary"]["by_status"]["consistent"] == 1
    assert "local holdout fixture scoring only" in result["policy_boundary"][0]
