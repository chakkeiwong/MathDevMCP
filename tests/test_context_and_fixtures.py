from pathlib import Path

from mathdevmcp.benchmarks import (
    benchmark_gate_report,
    benchmark_cases,
    build_benchmark_report,
    run_derivation_benchmark,
    run_label_consistency_benchmark,
    run_seeded_mismatch_benchmark,
    run_workflow_benchmark,
    summarize_benchmark_results,
    write_benchmark_report,
)
from mathdevmcp.consistency import compare_files, compare_label_to_code
from mathdevmcp.latex_index import build_index, extract_context_for_label


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_extract_context_for_label_returns_local_excerpt():
    index = build_index(FIXTURES)

    context = extract_context_for_label(index, "prop:transport-logdet", before=0, after=0)

    assert context["label"] == "prop:transport-logdet"
    assert context["kind"] == "proposition"
    assert any("Jacobian correction term" in line["text"] for line in context["excerpt"])


def test_compare_files_marks_good_fixture_consistent():
    result = compare_files(
        str(FIXTURES / "doc_consistency_good.tex"),
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "consistent"
    assert result["missing_in_code"] == []


def test_compare_files_marks_bad_fixture_mismatch():
    result = compare_files(
        str(FIXTURES / "doc_consistency_bad.tex"),
        str(FIXTURES / "doc_consistency_bad.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "mismatch"
    assert result["missing_in_code"] == ["logdet"]



def test_seeded_mismatch_benchmark_runner_reports_expected_results():
    root = FIXTURES.parent.parent

    results = run_seeded_mismatch_benchmark(root)

    assert {result["id"] for result in results} == {"doc_consistency_good", "doc_consistency_bad"}
    assert all(result["category"] == "consistency" for result in results)
    assert all(result["evaluation_focus"] == "status_regression" for result in results)
    assert all(result["passed"] for result in results)
    assert all(result["quality_checks"]["status_match"] for result in results)
    assert all("details" in result for result in results)



def test_compare_label_to_code_ignores_incidental_environment_terms_without_required_terms():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-implementation",
        str(FIXTURES / "doc_consistency_context_good.py"),
        paragraph_context=True,
    )

    assert result["status"] == "consistent"
    assert "proposition" not in result["doc_terms"]
    assert all(finding["severity"] == "required" for finding in result["findings"] if finding["kind"] != "extra_code_terms")



def test_compare_label_to_code_detects_realistic_context_terms_and_code_extras():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-implementation",
        str(FIXTURES / "doc_consistency_context_good.py"),
        paragraph_context=True,
        required_terms=["logdet"],
    )

    assert result["status"] == "consistent"
    assert result["missing_in_code"] == []
    assert result["extra_in_code"] == ["def", "log_pi", "return", "transformed_density"]
    assert any(finding == {"kind": "extra_code_terms", "terms": ["def", "log_pi", "return", "transformed_density"], "severity": "audit_only"} for finding in result["findings"])



def test_compare_label_to_code_reports_extra_math_terms_as_audit_only():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-implementation",
        str(FIXTURES / "doc_consistency_context_extra.py"),
        paragraph_context=True,
        required_terms=["logdet"],
    )

    assert result["status"] == "consistent"
    assert "temperature" in result["extra_in_code"]
    assert any(finding["kind"] == "extra_code_terms" and finding["severity"] == "audit_only" for finding in result["findings"])



def test_compare_label_to_code_returns_traceable_doc_context():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "mismatch"
    assert result["label"] == "prop:transport-mismatch"
    assert result["doc_context"]["file"] == "doc_consistency_bad.tex"
    assert result["findings"][0]["kind"] == "missing_term"



def test_label_consistency_benchmark_runner_reports_expected_results():
    root = FIXTURES.parent.parent

    results = run_label_consistency_benchmark(root)

    assert {result["id"] for result in results} == {
        "label_consistency_good",
        "label_consistency_bad",
        "label_consistency_hamiltonian_energy",
    }
    assert any(result["evaluation_focus"] == "realistic_fixture" for result in results)
    assert all(result["quality_checks"]["provenance_match"] for result in results)
    assert all(result["passed"] for result in results)



def test_derivation_benchmark_runner_reports_abstention_and_false_confidence_checks():
    root = FIXTURES.parent.parent

    results = run_derivation_benchmark(root)

    assert {result["id"] for result in results} == {"derivation_context_support", "derivation_symbol_mismatch"}
    assert {result["evaluation_focus"] for result in results} == {"abstention_quality", "false_confidence_control"}
    assert all(result["quality_checks"]["supported_by_context_match"] for result in results)
    assert all(result["quality_checks"]["provenance_match"] for result in results)
    assert all(result["passed"] for result in results)



def test_workflow_benchmark_runner_reports_contract_checks():
    root = FIXTURES.parent.parent

    results = run_workflow_benchmark(root)

    assert {result["id"] for result in results} == {
        "workflow_implementation_brief_consistent",
        "workflow_implementation_brief_unverified",
        "workflow_implementation_brief_mismatch",
    }
    assert all(result["evaluation_focus"] == "workflow_contract" for result in results)
    assert all(result["quality_checks"]["envelope_match"] for result in results)
    assert all(result["quality_checks"]["check_statuses_match"] for result in results)
    assert all(result["details"]["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"} for result in results)
    assert all(result["details"]["ok"] is True for result in results)
    assert all(result["passed"] for result in results)



def test_benchmark_cases_cover_consistency_derivation_and_workflow_categories():
    root = FIXTURES.parent.parent

    cases = benchmark_cases(root)

    assert len(cases) == 10
    assert {case["category"] for case in cases} == {"consistency", "derivation", "workflow"}



def test_build_benchmark_report_returns_contract_and_typed_results():
    root = FIXTURES.parent.parent

    report = build_benchmark_report(root)

    assert report["ok"] is True
    assert report["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert report["total"] == 10
    assert report["passed"] == 10
    assert all("details" in result for result in report["results"])



def test_write_benchmark_report_writes_json(tmp_path):
    root = FIXTURES.parent.parent
    output = tmp_path / "benchmark_report.json"

    result = write_benchmark_report(root, output)

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_report"}
    assert output.exists()



def test_benchmark_gate_report_is_ci_friendly():
    root = FIXTURES.parent.parent

    gate = benchmark_gate_report(root)

    assert gate == {
        "ok": True,
        "passed": True,
        "total": 10,
        "passed_count": 10,
        "failed_count": 0,
        "summary": {
            "by_category": {
                "consistency": {"total": 5, "passed": 5},
                "derivation": {"total": 2, "passed": 2},
                "workflow": {"total": 3, "passed": 3},
            },
            "by_focus": {
                "status_regression": {"total": 2, "passed": 2},
                "provenance_correctness": {"total": 2, "passed": 2},
                "abstention_quality": {"total": 1, "passed": 1},
                "false_confidence_control": {"total": 1, "passed": 1},
                "realistic_fixture": {"total": 1, "passed": 1},
                "workflow_contract": {"total": 3, "passed": 3},
            },
        },
        "policy": {
            "name": "all_benchmarks_must_pass",
            "required_pass_rate": 1.0,
            "allow_category_failures": {},
            "description": "Every benchmark case must pass; no category-specific failure budget is currently allowed.",
        },
        "metadata": {"schema_version": "1.0", "contract": "benchmark_gate"},
    }



def test_summarize_benchmark_results_groups_by_category_and_focus():
    root = FIXTURES.parent.parent

    results = (
        run_seeded_mismatch_benchmark(root)
        + run_label_consistency_benchmark(root)
        + run_derivation_benchmark(root)
        + run_workflow_benchmark(root)
    )
    summary = summarize_benchmark_results(results)

    assert summary == {
        "by_category": {
            "consistency": {"total": 5, "passed": 5},
            "derivation": {"total": 2, "passed": 2},
            "workflow": {"total": 3, "passed": 3},
        },
        "by_focus": {
            "status_regression": {"total": 2, "passed": 2},
            "provenance_correctness": {"total": 2, "passed": 2},
            "abstention_quality": {"total": 1, "passed": 1},
            "false_confidence_control": {"total": 1, "passed": 1},
            "realistic_fixture": {"total": 1, "passed": 1},
            "workflow_contract": {"total": 3, "passed": 3},
        },
    }
