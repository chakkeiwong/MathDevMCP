from pathlib import Path

from mathdevmcp.mcp_server import audit_derivation_label, audit_implementation_label, audit_kalman_recursion, benchmark_gate, check_equality, compare_label_code, extract_latex_context, get_tool_matrix, governance_policy, implementation_brief, latex_label_lookup, lean_check, release_readiness, run_benchmarks, typed_obligation_label, validate_release_corpus
from test_context_and_fixtures import EXPECTED_BENCHMARK_TOTAL


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent


def test_mcp_server_extract_latex_context_returns_label_metadata():
    result = extract_latex_context(str(FIXTURES), "prop:transport-logdet")

    assert result["label"] == "prop:transport-logdet"
    assert result["file"] == "doc_consistency_good.tex"


def test_mcp_server_preferred_label_lookup_returns_paragraph_context():
    result = latex_label_lookup(str(FIXTURES), "prop:transport-logdet")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "latex_paragraph_context"}
    assert result["label"] == "prop:transport-logdet"



def test_mcp_server_compare_label_code_returns_mismatch():
    result = compare_label_code(
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
        required_terms=["logdet"],
    )

    assert result["status"] == "mismatch"
    assert result["missing_in_code"] == ["logdet"]


def test_mcp_server_audit_implementation_label_matches_legacy_alias():
    args = (
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
    )

    preferred = audit_implementation_label(*args, required_terms=["logdet"])
    legacy = compare_label_code(*args, required_terms=["logdet"])

    assert preferred == legacy
    assert preferred["status"] == "mismatch"


def test_mcp_server_check_equality_returns_proof_obligation_contract():
    result = check_equality("(a+b)*(a-b)", "a*a - b*b")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_obligation_result"}
    assert result["status"] in {"equivalent", "verified", "inconclusive"}


def test_mcp_server_lean_check_returns_lean_contract():
    result = lean_check("example : 1 + 1 = 2 := rfl")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_check_result"}
    assert result["status"] in {"verified", "inconclusive", "mismatch"}



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


def test_mcp_server_release_policy_tools_return_contracts():
    corpus = validate_release_corpus(str(FIXTURES))
    governance = governance_policy()
    release = release_readiness(str(ROOT))

    assert corpus["metadata"] == {"schema_version": "1.0", "contract": "release_corpus_validation_report"}
    assert corpus["status"] == "consistent"
    assert governance["metadata"] == {"schema_version": "1.0", "contract": "governance_policy"}
    assert release["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert release["benchmark_gate"]["passed"] is True



def test_mcp_server_tool_matrix_exposes_core_problem_classes():
    problems = {entry["problem"] for entry in get_tool_matrix()}

    assert "long_document_tracking" in problems
    assert "document_grounded_implementation" in problems
