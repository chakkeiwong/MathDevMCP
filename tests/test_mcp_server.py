from pathlib import Path

from mathdevmcp.mcp_server import audit_derivation_label, audit_kalman_recursion, benchmark_gate, compare_label_code, extract_latex_context, get_tool_matrix, implementation_brief, run_benchmarks, typed_obligation_label
from test_context_and_fixtures import EXPECTED_BENCHMARK_TOTAL


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent


def test_mcp_server_extract_latex_context_returns_label_metadata():
    result = extract_latex_context(str(FIXTURES), "prop:transport-logdet")

    assert result["label"] == "prop:transport-logdet"
    assert result["file"] == "doc_consistency_good.tex"



def test_mcp_server_compare_label_code_returns_mismatch():
    result = compare_label_code(
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "mismatch"
    assert result["missing_in_code"] == ["logdet"]



def test_mcp_server_implementation_brief_returns_consistent_result():
    result = implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "consistent"
    assert result["selected_label"] == "prop:transport-logdet"



def test_mcp_server_run_benchmarks_returns_structured_report():
    result = run_benchmarks(str(ROOT))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert result["total"] == EXPECTED_BENCHMARK_TOTAL
    assert result["passed"] == EXPECTED_BENCHMARK_TOTAL



def test_mcp_server_audit_derivation_label_returns_proof_audit_result():
    result = audit_derivation_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_result"}
    assert result["status"] == "verified"


def test_mcp_server_audit_kalman_recursion_returns_ast_result():
    result = audit_kalman_recursion(str(FIXTURES / "doc_kalman_recursion_bad.py"))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "kalman_recursion_audit"}
    assert result["status"] == "mismatch"
    assert result["missing_operations"] == ["covariance_update"]


def test_mcp_server_typed_obligation_label_returns_diagnostic_result():
    result = typed_obligation_label(str(FIXTURES), "eq:dept-hmc-leapfrog")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "typed_obligation_label_diagnostic"}
    assert result["status"] == "unverified"
    assert result["typed_diagnostic"]["status"] == "needs_assumptions"



def test_mcp_server_benchmark_gate_returns_ci_result():
    result = benchmark_gate(str(ROOT))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_gate"}
    assert result["passed"] is True
    assert result["failed_count"] == 0
    assert result["policy"]["name"] == "all_benchmarks_must_pass"



def test_mcp_server_tool_matrix_exposes_core_problem_classes():
    problems = {entry["problem"] for entry in get_tool_matrix()}

    assert "long_document_tracking" in problems
    assert "document_grounded_implementation" in problems
