import json
from pathlib import Path

from mathdevmcp.real_local_high_level_pilot import (
    load_high_level_pilot_manifest,
    run_high_level_pilot,
    score_probe_result,
)


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "benchmarks" / "real_tasks" / "holdout_local" / "high_level_pilot_cases.json"


def test_high_level_pilot_manifest_loads_with_separate_channels() -> None:
    result = load_high_level_pilot_manifest(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_high_level_pilot_manifest"
    assert result["status"] == "consistent"
    assert len(result["cases"]) == 5
    for case in result["cases"]:
        assert case["tier"] == "holdout_local"
        assert "source_obligation" in case
        assert "executable_probe" in case
        assert "adapter_gap" in case
        assert "forbidden_claims" in case
        assert "case_status" not in case
        assert "accuracy" not in case


def test_high_level_pilot_manifest_rejects_absolute_source_path(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["source_snapshot"]["source_files"][0]["path"] = "/tmp/not-local.tex"
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_high_level_pilot_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "absolute_source_path" for item in result["findings"])


def test_high_level_pilot_manifest_rejects_blended_status_field(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["case_status"] = "passed"
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_high_level_pilot_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "blended_status_or_accuracy_forbidden" for item in result["findings"])


def test_score_probe_result_fails_when_required_non_claim_is_missing() -> None:
    case = load_high_level_pilot_manifest(ROOT, MANIFEST)["cases"][0]
    result = {
        "status": "refuted",
        "evidence_classes": ["backend_counterexample"],
        "certification_source": "backend",
        "non_claims": [{"code": "general_theorem_proving_not_claimed"}],
        "veto_reasons": [],
        "assumptions": [],
        "counterexamples": [{"assignments": {"x": 1}}],
    }

    score = score_probe_result(case, result)

    assert score["status"] == "failed"
    assert score["checks"]["required_non_claims_present"] is False


def test_score_probe_result_fails_when_adapter_gap_hidden() -> None:
    case = dict(load_high_level_pilot_manifest(ROOT, MANIFEST)["cases"][0])
    case["adapter_gap"] = {"status": "none"}
    result = {
        "status": "refuted",
        "evidence_classes": ["backend_counterexample"],
        "certification_source": "backend",
        "non_claims": [
            {"code": "general_theorem_proving_not_claimed"},
            {"code": "release_readiness_not_claimed"},
        ],
        "veto_reasons": [],
        "assumptions": [],
        "counterexamples": [{"assignments": {"x": 1}}],
    }

    score = score_probe_result(case, result)

    assert score["status"] == "failed"
    assert score["checks"]["adapter_gap_visible"] is False


def test_run_high_level_pilot_reports_separate_ledgers_and_no_accuracy_metric() -> None:
    report = run_high_level_pilot(ROOT, MANIFEST)

    assert report["metadata"]["contract"] == "real_local_high_level_pilot_report"
    assert report["status"] == "passed"
    assert report["summary"]["case_total"] == 5
    assert report["summary"]["probe_passed"] == 5
    assert report["summary"]["probe_failed"] == 0
    assert report["summary"]["adapter_required"] == 5
    assert report["summary"]["aggregate_accuracy"] is None
    assert len(report["source_obligation_ledger"]) == 5
    assert len(report["probe_ledger"]) == 5
    assert len(report["adapter_gap_ledger"]) == 5
    assert "No single aggregate pilot accuracy metric is emitted." in report["policy_boundary"]
