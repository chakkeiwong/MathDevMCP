from pathlib import Path

from mathdevmcp.mcp_server import assumptions_for, audit_and_propose_assumptions, audit_and_propose_derivations, audit_derivation_label, audit_implementation_label, audit_kalman_recursion, audit_math_to_code, benchmark_gate, check_equality, compare_label_code, debug_derivation, derive_from, extract_latex_context, get_tool_matrix, governance_policy, high_level_workflow_quality, implementation_brief, latex_label_lookup, lean_check, prepare_review_packet, prove_or_counterexample, release_readiness, run_benchmarks, typed_obligation_label, validate_release_corpus, workbench_benchmark_quality
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


def test_mcp_server_audit_implementation_label_returns_rich_audit_while_alias_stays_legacy():
    args = (
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
    )

    preferred = audit_implementation_label(*args, required_terms=["logdet"])
    legacy = compare_label_code(*args, required_terms=["logdet"])

    assert preferred["metadata"] == {"schema_version": "1.0", "contract": "implementation_audit_result"}
    assert legacy["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert preferred["status"] == "mismatch"
    assert legacy["status"] == "mismatch"


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


def test_mcp_server_high_level_workflows_return_contract_envelopes():
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    proof = prove_or_counterexample("A*B = B*A")
    assumptions = assumptions_for("logdet(A)")
    assumption_report = audit_and_propose_assumptions("Audit assumptions", target="logdet(A)")
    derivation_report = audit_and_propose_derivations("Audit derivations", target="logdet(A) = trace(A)")
    debug = debug_derivation(["logdet(A)", "trace(A)", "trace(A)"])
    code = audit_math_to_code("logdet(S)", "def f(S):\n    return logdet(S)\n")
    packet = prepare_review_packet("Review failed proof", evidence=[proof])

    assert derived["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert derived["status"] == "proved"
    assert "givens_not_formal_assumptions" in {item["code"] for item in derived["non_claims"]}
    assert proof["status"] == "refuted"
    assert proof["counterexamples"]
    assert assumptions["status"] == "missing_assumptions"
    assert assumption_report["metadata"]["contract"] == "audit_assumption_report_result"
    assert assumption_report["proposals"][0]["validation"]["status"] == "validated_by_rule"
    assert derivation_report["metadata"]["contract"] == "derivation_audit_report_result"
    assert derivation_report["proposals"][0]["validation"]["status"] == "blocked_by_missing_assumptions"
    assert debug["status"] == "gap_found"
    assert code["status"] == "structural_match"
    assert code["certification_source"] == "none"
    assert packet["status"] == "diagnostic_only"
    assert packet["certification_source"] == "none"


def test_mcp_server_prepare_review_packet_preserves_phase6_packet_fields():
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    code = audit_math_to_code(
        "logdet(Sigma) + trace(Cov)",
        "def f(S):\n    return logdet(S) + trace(S)\n",
        aliases={"Sigma": "S", "Cov": "S"},
    )
    packet = prepare_review_packet(
        "Review derivation and implementation context",
        evidence=[derived, code],
        source={"context_summary": "MCP server preservation fixture."},
    )
    low_level = packet["evidence"][0]["low_level"]

    assert packet["status"] == "diagnostic_only"
    assert packet["certification_source"] == "none"
    assert low_level["backend_checks"]
    assert low_level["nested_evidence_summary"]
    assert low_level["route_plans"]
    assert low_level["trace_maps"]
    assert low_level["residual_gaps"]
    assert low_level["decision_criteria"]
    assert low_level["risk_register"]
    assert low_level["agent_handoff"]["scoped_question"] == "Review derivation and implementation context"
    assert low_level["agent_handoff"]["evidence_ledger"]
    assert low_level["agent_handoff"]["veto_risks"]
    assert packet["agent_handoff"] == low_level["agent_handoff"]
    assert any(item["code"] == "diagnostic_route_and_trace_context_not_proof" for item in low_level["non_claims"])


def test_mcp_server_prepare_review_packet_can_return_compact_handoff():
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    handoff = prepare_review_packet("Review compact server handoff", evidence=[derived], handoff=True)

    assert handoff["scoped_question"] == "Review compact server handoff"
    assert handoff["evidence_ledger"]
    assert handoff["non_claim_boundary"]
    assert "not a proof certificate" in handoff["certification_boundary"]
    assert "metadata" not in handoff



def test_mcp_server_run_benchmarks_returns_structured_report():
    result = run_benchmarks(str(ROOT))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert result["total"] == EXPECTED_BENCHMARK_TOTAL
    assert result["passed"] == EXPECTED_BENCHMARK_TOTAL
    assert result["workbench_quality"]["status"] == "quality_thresholds_passed"



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


def test_mcp_server_workbench_benchmark_quality_returns_threshold_report():
    result = workbench_benchmark_quality(str(ROOT))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "workbench_benchmark_quality_report"}
    assert result["status"] == "quality_thresholds_passed"
    assert result["total_cases"] == 15
    assert all(result["seeded_gate_thresholds"].values())


def test_mcp_server_high_level_workflow_quality_returns_threshold_report():
    result = high_level_workflow_quality(str(ROOT))

    assert result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_quality_report"}
    assert result["status"] == "quality_thresholds_passed"
    assert result["total_cases"] == 14
    assert result["workflow_count"] == 6
    assert all(result["seeded_gate_thresholds"].values())


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
