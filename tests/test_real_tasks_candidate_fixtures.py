import json
from pathlib import Path

from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest
from mathdevmcp.real_tasks_scored_report import score_real_task_public_candidates
from mathdevmcp.real_tasks_scoring import score_real_task_case


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_SET = ROOT / "benchmarks" / "real_tasks" / "fixtures" / "public_candidate_answers.json"


def test_public_candidate_answer_fixture_set_is_well_formed() -> None:
    payload = json.loads(FIXTURE_SET.read_text())

    assert payload["metadata"]["contract"] == "real_task_candidate_fixture_set"
    assert len(payload["fixtures"]) >= 11


def test_public_candidate_answer_fixtures_score_to_expected_statuses() -> None:
    payload = json.loads(FIXTURE_SET.read_text())
    manifest = load_real_task_public_manifest(ROOT)
    by_id = {case["id"]: case for case in manifest["cases"]}

    for fixture in payload["fixtures"]:
        result = score_real_task_case(by_id[fixture["case_id"]], fixture["candidate"])
        assert result["status"] == fixture["expected_score_status"], fixture["id"]


def test_public_candidate_answer_fixture_set_drives_scored_report() -> None:
    payload = json.loads(FIXTURE_SET.read_text())
    candidates = [fixture["candidate"] for fixture in payload["fixtures"]]
    report = score_real_task_public_candidates(candidates, root=ROOT)

    assert report["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_structural_score_report",
    }
    assert report["summary"]["scored_candidate_total"] == len(payload["fixtures"])
    assert report["summary"]["by_status"]["consistent"] >= 1
    assert report["summary"]["by_status"]["mismatch"] >= 1
    assert len(report["summary"]["missing_candidate_case_ids"]) < 3
