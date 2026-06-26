import json
from pathlib import Path

from mathdevmcp.real_tasks_holdout_local import (
    discover_local_holdout_candidate_answers,
    discover_local_holdout_manifest,
    initialize_local_holdout_candidate_answers,
    initialize_local_holdout_manifest,
)


ROOT = Path(__file__).resolve().parent.parent


def test_holdout_local_discovery_is_inconclusive_when_no_local_manifest_exists(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    result = discover_local_holdout_manifest(ROOT, manifest_path=path)

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_holdout_local_discovery",
    }
    assert result["status"] == "inconclusive"
    assert result["exists"] is False


def test_holdout_local_discovery_reports_consistent_when_local_manifest_exists(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    path.write_text(json.dumps({"metadata": {"status": "local"}, "cases": []}), encoding="utf-8")
    result = discover_local_holdout_manifest(ROOT, manifest_path=path)

    assert result["status"] == "consistent"
    assert result["exists"] is True


def test_holdout_local_discovery_preserves_non_public_boundary_language(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_cases.json"
    result = discover_local_holdout_manifest(ROOT, manifest_path=path)
    text = " ".join(result["policy_boundary"])

    assert "not committed by default" in text
    assert "not a benchmark failure" in text


def test_holdout_local_initializer_creates_local_scaffold_from_template(tmp_path: Path) -> None:
    target = tmp_path / "holdout_local_cases.json"
    result = initialize_local_holdout_manifest(ROOT, manifest_path=target)

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_holdout_local_initialization",
    }
    assert result["status"] == "consistent"
    assert result["created"] is True
    assert target.exists()
    payload = json.loads(target.read_text())
    assert payload["metadata"]["contract"] == "real_task_holdout_local_case_template"


def test_holdout_local_initializer_refuses_to_overwrite_existing_local_file(tmp_path: Path) -> None:
    target = tmp_path / "holdout_local_cases.json"
    target.write_text('{"existing": true}', encoding="utf-8")
    result = initialize_local_holdout_manifest(ROOT, manifest_path=target)

    assert result["status"] == "consistent"
    assert result["created"] is False
    assert result["overwrote_existing"] is False
    assert target.read_text() == '{"existing": true}'


def test_holdout_local_initializer_preserves_non_public_boundary_language(tmp_path: Path) -> None:
    target = tmp_path / "holdout_local_cases.json"
    result = initialize_local_holdout_manifest(ROOT, manifest_path=target)
    text = " ".join(result["policy_boundary"])

    assert "local scaffold only" in text
    assert "non-committed local artifact" in text


def test_holdout_local_candidate_discovery_is_inconclusive_when_no_local_file_exists(tmp_path: Path) -> None:
    path = tmp_path / "holdout_local_candidate_answers.json"
    result = discover_local_holdout_candidate_answers(ROOT, candidate_path=path)

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_holdout_local_candidate_discovery",
    }
    assert result["status"] == "inconclusive"
    assert result["exists"] is False


def test_holdout_local_candidate_initializer_creates_local_scaffold_from_template(tmp_path: Path) -> None:
    target = tmp_path / "holdout_local_candidate_answers.json"
    result = initialize_local_holdout_candidate_answers(ROOT, candidate_path=target)

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_holdout_local_candidate_initialization",
    }
    assert result["status"] == "consistent"
    assert result["created"] is True
    payload = json.loads(target.read_text())
    assert payload["metadata"]["contract"] == "real_task_holdout_local_candidate_template"


def test_holdout_local_candidate_initializer_refuses_to_overwrite_existing_local_file(tmp_path: Path) -> None:
    target = tmp_path / "holdout_local_candidate_answers.json"
    target.write_text('{"existing": true}', encoding="utf-8")
    result = initialize_local_holdout_candidate_answers(ROOT, candidate_path=target)

    assert result["status"] == "consistent"
    assert result["created"] is False
    assert result["overwrote_existing"] is False
    assert target.read_text() == '{"existing": true}'
