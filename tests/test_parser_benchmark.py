from pathlib import Path

from mathdevmcp.parser_benchmark import compare_parser_backends, run_parser_backend


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_parser_backend_current_preserves_labels_and_provenance():
    result = run_parser_backend(FIXTURES, "current")

    assert result["status"] == "parsed"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["labels_found"] >= 1
    assert result["quality_checks"]["label_preservation"] is True
    assert result["quality_checks"]["provenance_available"] is True
    assert "eq:proof-audit-single" in result["labels"]


def test_parser_backend_current_preserves_department_corpus_labels():
    result = run_parser_backend(FIXTURES, "current")

    assert "eq:dept-state-space-recursion" in result["labels"]
    assert "eq:dept-hmc-leapfrog" in result["labels"]
    assert result["details"]["missing_expected_labels"] == []
    assert result["details"]["expected_label_recall"] == 1.0
    assert result["details"]["generated_like_labels"] == []
    assert result["details"]["provenance_score"] == 1.0
    assert result["details"]["environment_count"] >= 1


def test_parser_backend_latexml_runs_or_reports_inconclusive():
    result = run_parser_backend(FIXTURES, "latexml")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["status"] in {"parsed", "inconclusive"}
    if result["status"] == "parsed":
        assert result["quality_checks"]["label_preservation"] is True
        assert result["labels_found"] >= 1


def test_parser_backend_pandoc_runs_or_reports_inconclusive():
    result = run_parser_backend(FIXTURES, "pandoc")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["status"] in {"parsed", "inconclusive"}
    if result["status"] == "parsed":
        assert result["quality_checks"]["label_preservation"] is True
        assert result["labels_found"] >= 1


def test_compare_parser_backends_returns_ci_friendly_summary():
    result = compare_parser_backends(FIXTURES, backends=["current", "latexml", "pandoc"])

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_benchmark_report"}
    assert {item["backend"] for item in result["results"]} == {"current", "latexml", "pandoc"}
    assert result["summary"]["total"] == 3
    assert result["summary"]["parsed"] >= 1
    assert result["summary"]["label_preserving"] >= 1
