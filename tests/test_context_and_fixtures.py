from pathlib import Path

from mathdevmcp.benchmarks import (
    benchmark_gate_report,
    benchmark_cases,
    build_workbench_benchmark_quality_report,
    build_benchmark_report,
    build_high_level_workflow_quality_report,
    run_derivation_benchmark,
    run_ast_corpus_benchmark,
    run_industrial_review_benchmark,
    run_kalman_recursion_benchmark,
    run_label_consistency_benchmark,
    run_high_level_math_workflow_benchmark,
    run_math_debugging_workbench_benchmark,
    run_parser_corpus_benchmark,
    run_proof_audit_benchmark,
    run_proof_audit_v2_benchmark,
    run_release_corpus_benchmark,
    run_release_policy_benchmark,
    run_seeded_mismatch_benchmark,
    run_typed_ir_benchmark,
    run_workflow_benchmark,
    summarize_benchmark_results,
    write_benchmark_report,
)
from mathdevmcp.consistency import compare_files, compare_label_to_code
from mathdevmcp.latex_index import build_index, extract_context_for_label, search_index


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"

EXPECTED_BENCHMARK_SUMMARY = {
    "by_category": {
        "consistency": {"total": 5, "passed": 5, "expected_abstentions": 0},
        "derivation": {"total": 6, "passed": 6, "expected_abstentions": 5},
        "workflow": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "proof_audit": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "proof_audit_v2": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "kalman_recursion": {"total": 2, "passed": 2, "expected_abstentions": 1},
        "parser_corpus": {"total": 3, "passed": 3, "expected_abstentions": 0},
        "ast_corpus": {"total": 11, "passed": 11, "expected_abstentions": 0},
        "typed_ir": {"total": 2, "passed": 2, "expected_abstentions": 2},
        "industrial_review": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "release_corpus": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "release_policy": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "math_debugging_workbench": {"total": 15, "passed": 15, "expected_abstentions": 11},
        "high_level_math_workflows": {"total": 14, "passed": 14, "expected_abstentions": 9},
    },
    "by_focus": {
        "status_regression": {"total": 2, "passed": 2, "expected_abstentions": 0},
        "provenance_correctness": {"total": 2, "passed": 2, "expected_abstentions": 0},
        "abstention_quality": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "false_confidence_control": {"total": 6, "passed": 6, "expected_abstentions": 0},
        "realistic_fixture": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "realistic_abstention": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "multilabel_provenance": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "long_document_provenance": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "repeat_label_stability": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workflow_contract": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "proof_audit_routing": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "proof_audit_abstention": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "release_spine_verified": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "release_spine_abstention": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "ast_recursion_abstention": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "realistic_parser_provenance": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "multifile_macro_parser_provenance": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "sanitized_domain_parser_provenance": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "realistic_ast_operation_coverage": {"total": 3, "passed": 3, "expected_abstentions": 0},
        "sanitized_domain_ast_operation_coverage": {"total": 6, "passed": 6, "expected_abstentions": 0},
        "typed_dimension_diagnostics": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "typed_stochastic_diagnostics": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "agent_review_packet": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "release_corpus_manifest": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "release_readiness_contract": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "workbench_proof_refutation": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "workbench_false_confidence_control": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "workbench_backend_boundary": {"total": 2, "passed": 2, "expected_abstentions": 2},
        "workbench_gap_localization": {"total": 1, "passed": 1, "expected_abstentions": 0},
        "workbench_missing_assumptions": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_structural_boundary": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_notation_conflict": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_diagnostic_generation": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_packet_boundary": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_impact_boundary": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "workbench_applicability_boundary": {"total": 2, "passed": 2, "expected_abstentions": 2},
        "hlf_backend_certificate": {"total": 2, "passed": 2, "expected_abstentions": 0},
        "hlf_false_confidence_control": {"total": 3, "passed": 3, "expected_abstentions": 1},
        "hlf_backend_boundary": {"total": 1, "passed": 1, "expected_abstentions": 1},
        "hlf_missing_assumptions": {"total": 2, "passed": 2, "expected_abstentions": 2},
        "hlf_gap_localization": {"total": 2, "passed": 2, "expected_abstentions": 1},
        "hlf_structural_boundary": {"total": 2, "passed": 2, "expected_abstentions": 2},
        "hlf_packet_boundary": {"total": 2, "passed": 2, "expected_abstentions": 2},
    },
    "expected_abstentions": 32,
}

EXPECTED_BENCHMARK_TOTAL = 70


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



def test_multilabel_kalman_fixture_keeps_score_provenance_distinct():
    index = build_index(FIXTURES)

    results = search_index(index, "multilabel kalman derivative chain partial_i ell_t trace residual", limit=5)
    context = extract_context_for_label(index, "eq:kalman-score-contribution", before=1, after=1)

    assert results[0]["label"] == "eq:kalman-score-contribution"
    assert context["file"] == "doc_multilabel_kalman_chain.tex"
    assert context["label"] == "eq:kalman-score-contribution"
    assert context["section_path"] == ["Kalman derivative chain"]
    assert any(block.get("label") == "eq:kalman-innovation-covariance" for block in results[1:])



def test_longdoc_kalman_fixture_retrieves_score_not_nearby_smoothing_labels():
    index = build_index(FIXTURES)

    results = search_index(index, "score contribution trace residual derivative observed information smoothing gain", limit=8)
    context = extract_context_for_label(index, "eq:longdoc-score-contribution", before=1, after=1)

    assert results[0]["label"] == "eq:longdoc-score-contribution"
    assert context["file"] == "doc_longdoc_kalman_retrieval.tex"
    assert context["label"] == "eq:longdoc-score-contribution"
    assert context["section_path"] == ["Likelihood derivative notes"]
    assert any(block.get("label") == "eq:longdoc-smoothing-gain" for block in results[1:])
    assert any(block.get("label") == "eq:longdoc-observed-information" for block in results[1:])



def test_repeat_label_kalman_fixture_preserves_target_score_provenance():
    index = build_index(FIXTURES)

    results = search_index(index, "repeat-kalman-target-score target likelihood derivative block", limit=8)
    context = extract_context_for_label(index, "eq:repeat-kalman-target-score", before=1, after=1)

    assert results[0]["label"] == "eq:repeat-kalman-target-score"
    assert context["file"] == "doc_repeat_label_kalman_scale.tex"
    assert context["label"] == "eq:repeat-kalman-target-score"
    assert context["section_path"] == ["Target likelihood derivative block"]
    assert index["n_labels"] >= 18
    repeated = search_index(index, "repeat kalman covariance smoothing", limit=8)
    assert any((block.get("label") or "").startswith("eq:repeat-kalman-covariance-") for block in repeated)


def test_department_corpus_fixtures_preserve_labels_and_sections():
    index = build_index(FIXTURES)

    state = extract_context_for_label(index, "eq:dept-state-space-recursion", before=0, after=0)
    hmc = extract_context_for_label(index, "eq:dept-hmc-leapfrog", before=0, after=0)
    macro_filter = extract_context_for_label(index, "eq:macro-filter-likelihood", before=0, after=0)

    assert state["file"] == "doc_department_state_space.tex"
    assert state["section_path"] == ["Sanitized state-space audit slice"]
    assert hmc["file"] == "doc_department_bayesian_hmc.tex"
    assert hmc["section_path"] == ["Sanitized Bayesian computation audit slice"]
    assert macro_filter["file"] == "doc_macro_filter_model.tex"
    assert macro_filter["section_path"] == ["State equations"]



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

    assert {result["id"] for result in results} == {
        "derivation_context_support",
        "derivation_symbol_mismatch",
        "derivation_realistic_kalman_hessian_abstention",
        "derivation_multilabel_kalman_score_abstention",
        "derivation_longdoc_kalman_score_abstention",
        "derivation_repeat_label_kalman_score_abstention",
    }
    assert {result["evaluation_focus"] for result in results} == {
        "abstention_quality",
        "false_confidence_control",
        "realistic_abstention",
        "multilabel_provenance",
        "long_document_provenance",
        "repeat_label_stability",
    }
    assert all(result["quality_checks"]["supported_by_context_match"] for result in results)
    assert all(result["quality_checks"]["provenance_match"] for result in results)
    assert all(result["passed"] for result in results)
    expected_abstention = {result["id"]: result["expected_abstention"] for result in results}
    assert expected_abstention == {
        "derivation_context_support": True,
        "derivation_symbol_mismatch": False,
        "derivation_realistic_kalman_hessian_abstention": True,
        "derivation_multilabel_kalman_score_abstention": True,
        "derivation_longdoc_kalman_score_abstention": True,
        "derivation_repeat_label_kalman_score_abstention": True,
    }
    realistic = next(result for result in results if result["id"] == "derivation_realistic_kalman_hessian_abstention")
    longdoc = next(result for result in results if result["id"] == "derivation_longdoc_kalman_score_abstention")
    repeat = next(result for result in results if result["id"] == "derivation_repeat_label_kalman_score_abstention")
    assert realistic["details"]["doc_context"]["file"] == "doc_realistic_kalman_hessian.tex"
    assert longdoc["details"]["doc_context"]["section_path"] == ["Likelihood derivative notes"]
    assert repeat["details"]["doc_context"]["section_path"] == ["Target likelihood derivative block"]
    assert realistic["quality_checks"]["expected_abstention_match"] is True
    assert longdoc["quality_checks"]["expected_abstention_match"] is True
    assert repeat["quality_checks"]["expected_abstention_match"] is True



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



def test_benchmark_cases_cover_consistency_derivation_workflow_and_proof_audit_categories():
    root = FIXTURES.parent.parent

    cases = benchmark_cases(root)

    assert len(cases) == EXPECTED_BENCHMARK_TOTAL
    assert {case["category"] for case in cases} == {"consistency", "derivation", "workflow", "proof_audit", "proof_audit_v2", "kalman_recursion", "parser_corpus", "ast_corpus", "typed_ir", "industrial_review", "release_corpus", "release_policy", "math_debugging_workbench", "high_level_math_workflows"}



def test_proof_audit_benchmark_runner_reports_routing_and_abstention_checks():
    root = FIXTURES.parent.parent

    results = run_proof_audit_benchmark(root)

    assert {result["id"] for result in results} == {
        "proof_audit_single_verified",
        "proof_audit_false_mismatch",
        "proof_audit_kalman_abstention",
    }
    assert all(result["quality_checks"]["obligation_provenance_match"] for result in results)
    assert all(result["passed"] for result in results)
    expected_abstention = {result["id"]: result["expected_abstention"] for result in results}
    assert expected_abstention == {
        "proof_audit_single_verified": False,
        "proof_audit_false_mismatch": False,
        "proof_audit_kalman_abstention": True,
    }


def test_proof_audit_v2_benchmark_runner_reports_release_spine_checks():
    root = FIXTURES.parent.parent

    results = run_proof_audit_v2_benchmark(root)

    assert {result["id"] for result in results} == {
        "proof_audit_v2_scalar_verified",
        "proof_audit_v2_false_mismatch",
        "proof_audit_v2_state_space_abstention",
    }
    assert all(result["category"] == "proof_audit_v2" for result in results)
    assert all(result["quality_checks"]["contract_match"] for result in results)
    assert all(result["quality_checks"]["obligation_contract_match"] for result in results)
    assert all(result["quality_checks"]["route_match"] for result in results)
    assert all(result["passed"] for result in results)
    expected_abstention = {result["id"]: result["expected_abstention"] for result in results}
    assert expected_abstention == {
        "proof_audit_v2_scalar_verified": False,
        "proof_audit_v2_false_mismatch": False,
        "proof_audit_v2_state_space_abstention": True,
    }


def test_kalman_recursion_benchmark_runner_reports_ast_and_abstention_checks():
    root = FIXTURES.parent.parent

    results = run_kalman_recursion_benchmark(root)

    assert {result["id"] for result in results} == {
        "kalman_recursion_structural_unverified",
        "kalman_recursion_missing_covariance_update",
    }
    assert all(result["category"] == "kalman_recursion" for result in results)
    assert all(result["quality_checks"]["ast_contract_match"] for result in results)
    assert all(result["passed"] for result in results)
    expected_abstention = {result["id"]: result["expected_abstention"] for result in results}
    assert expected_abstention == {
        "kalman_recursion_structural_unverified": True,
        "kalman_recursion_missing_covariance_update": False,
    }


def test_parser_corpus_benchmark_runner_reports_department_fixture_labels():
    root = FIXTURES.parent.parent

    results = run_parser_corpus_benchmark(root)

    assert {result["id"] for result in results} == {
        "parser_corpus_department_current",
        "parser_corpus_macro_filter_multifile",
        "parser_corpus_sanitized_public_domains",
    }
    assert all(result["category"] == "parser_corpus" for result in results)
    assert all(result["quality_checks"]["expected_labels_preserved"] for result in results)
    assert all(result["passed"] for result in results)


def test_ast_corpus_benchmark_runner_reports_realistic_operation_coverage():
    root = FIXTURES.parent.parent

    results = run_ast_corpus_benchmark(root)

    assert {result["id"] for result in results} == {
        "ast_corpus_state_space_jax",
        "ast_corpus_hmc_jax",
        "ast_corpus_particle_filter",
        "ast_corpus_state_space_missing_solve",
        "ast_corpus_macro_filter_missing_gain",
        "ast_corpus_dsge_macro_finance",
        "ast_corpus_stochastic_volatility",
        "ast_corpus_sde_pde_numerics",
        "ast_corpus_ml_llm_objective",
        "ast_corpus_bayesian_elbo_vi",
        "ast_corpus_computational_physics_mcmc",
    }
    assert all(result["category"] == "ast_corpus" for result in results)
    assert all(result["quality_checks"]["graph_contract_match"] for result in results)
    assert all(result["passed"] for result in results)
    missing = next(result for result in results if result["id"] == "ast_corpus_state_space_missing_solve")
    assert missing["observed_status"] == "mismatch"
    assert missing["details"]["missing_operations"] == ["inverse_or_solve"]
    macro_missing = next(result for result in results if result["id"] == "ast_corpus_macro_filter_missing_gain")
    assert macro_missing["observed_status"] == "mismatch"
    assert macro_missing["details"]["missing_operations"] == ["kalman_gain", "state_update", "covariance_update"]


def test_typed_ir_benchmark_runner_reports_missing_dimension_diagnostics():
    root = FIXTURES.parent.parent

    results = run_typed_ir_benchmark(root)

    assert {result["id"] for result in results} == {
        "typed_ir_state_space_likelihood",
        "typed_ir_hmc_leapfrog",
    }
    assert all(result["category"] == "typed_ir" for result in results)
    assert all(result["expected_abstention"] for result in results)
    assert all(result["quality_checks"]["contract_match"] for result in results)
    assert all(result["passed"] for result in results)


def test_industrial_review_benchmark_runner_reports_agent_packet_actions():
    root = FIXTURES.parent.parent

    results = run_industrial_review_benchmark(root)

    assert {result["id"] for result in results} == {"industrial_review_state_space_packet"}
    assert all(result["category"] == "industrial_review" for result in results)
    assert all(result["expected_abstention"] for result in results)
    assert all(result["quality_checks"]["actions_match"] for result in results)
    assert all(result["passed"] for result in results)


def test_math_debugging_workbench_benchmark_runner_reports_boundary_checks():
    root = FIXTURES.parent.parent

    results = run_math_debugging_workbench_benchmark(root)

    assert len(results) == 15
    assert all(result["category"] == "math_debugging_workbench" for result in results)
    assert all(result["quality_checks"]["oracle_class_supported"] for result in results)
    assert all(result["quality_checks"]["boundary_preserved"] for result in results)
    assert all(result["passed"] for result in results)
    assert sum(1 for result in results if result["quality_checks"]["negative_control"]) >= 6


def test_high_level_math_workflow_benchmark_runner_reports_boundary_checks():
    root = FIXTURES.parent.parent

    results = run_high_level_math_workflow_benchmark(root)

    assert len(results) == 14
    assert all(result["category"] == "high_level_math_workflows" for result in results)
    assert all(result["quality_checks"]["contract_match"] for result in results)
    assert all(result["quality_checks"]["boundary_preserved"] for result in results)
    assert all(result["passed"] for result in results)
    assert sum(1 for result in results if result["quality_checks"]["negative_control"]) >= 6


def test_workbench_benchmark_quality_report_uses_actual_seeded_results():
    root = FIXTURES.parent.parent

    report = build_workbench_benchmark_quality_report(root)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "workbench_benchmark_quality_report"}
    assert report["status"] == "quality_thresholds_passed"
    assert report["total_cases"] == 15
    assert report["total_results"] == 15
    assert report["negative_control_rate"] >= 0.40
    assert all(report["seeded_gate_thresholds"].values())
    assert all(report["mutation_results"].values())
    assert report["determinism"]["stable"] is True
    assert report["missing_tools"] == []
    assert report["missing_oracle_classes"] == []
    assert "complete adversarial benchmark" in report["non_claims"][0]


def test_high_level_workflow_quality_report_uses_actual_seeded_results():
    root = FIXTURES.parent.parent

    report = build_high_level_workflow_quality_report(root)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_quality_report"}
    assert report["status"] == "quality_thresholds_passed"
    assert report["total_cases"] == 14
    assert report["total_results"] == 14
    assert report["negative_control_rate"] >= 0.40
    assert all(report["seeded_gate_thresholds"].values())
    assert all(report["mutation_results"].values())
    assert report["determinism"]["stable"] is True
    assert "not established by pass rate alone" in report["boundary"]


def test_release_corpus_benchmark_runner_reports_privacy_gate():
    root = FIXTURES.parent.parent

    results = run_release_corpus_benchmark(root)

    assert {result["id"] for result in results} == {"release_corpus_manifest_privacy_gate"}
    assert all(result["category"] == "release_corpus" for result in results)
    assert all(result["quality_checks"]["private_entries_external"] for result in results)
    assert all(result["passed"] for result in results)


def test_release_policy_benchmark_runner_reports_readiness_contract():
    root = FIXTURES.parent.parent

    results = run_release_policy_benchmark(root)

    assert {result["id"] for result in results} == {"release_policy_readiness_report"}
    assert all(result["category"] == "release_policy" for result in results)
    assert all(result["quality_checks"]["benchmark_gate_passed"] for result in results)
    assert all(result["quality_checks"]["governance_contract_match"] for result in results)
    assert all(result["passed"] for result in results)



def test_build_benchmark_report_returns_contract_and_typed_results():
    root = FIXTURES.parent.parent

    report = build_benchmark_report(root)

    assert report["ok"] is True
    assert report["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert report["total"] == EXPECTED_BENCHMARK_TOTAL
    assert report["passed"] == EXPECTED_BENCHMARK_TOTAL
    assert all("details" in result for result in report["results"])
    assert report["workbench_quality"]["status"] == "quality_thresholds_passed"
    assert report["high_level_quality"]["status"] == "quality_thresholds_passed"
    assert all(report["workbench_quality"]["seeded_gate_thresholds"].values())
    assert all(report["high_level_quality"]["seeded_gate_thresholds"].values())


def test_release_readiness_uses_non_recursive_gate():
    root = FIXTURES.parent.parent

    report = build_benchmark_report(root, include_release_policy=False)
    gate = benchmark_gate_report(root, include_release_policy=False)

    assert report["total"] == EXPECTED_BENCHMARK_TOTAL - 1
    assert "release_policy" not in report["summary"]["by_category"]
    assert gate["passed"] is True
    assert gate["total"] == EXPECTED_BENCHMARK_TOTAL - 1



def test_write_benchmark_report_writes_json(tmp_path):
    root = FIXTURES.parent.parent
    output = tmp_path / "benchmark_report.json"

    result = write_benchmark_report(root, output)

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_report"}
    assert result["report"]["workbench_quality"]["status"] == "quality_thresholds_passed"
    assert output.exists()



def test_benchmark_gate_report_is_ci_friendly():
    root = FIXTURES.parent.parent

    gate = benchmark_gate_report(root)

    assert gate == {
        "ok": True,
        "passed": True,
        "total": EXPECTED_BENCHMARK_TOTAL,
        "passed_count": EXPECTED_BENCHMARK_TOTAL,
        "failed_count": 0,
        "summary": EXPECTED_BENCHMARK_SUMMARY,
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
        + run_proof_audit_benchmark(root)
        + run_proof_audit_v2_benchmark(root)
        + run_kalman_recursion_benchmark(root)
        + run_parser_corpus_benchmark(root)
        + run_ast_corpus_benchmark(root)
        + run_typed_ir_benchmark(root)
        + run_industrial_review_benchmark(root)
        + run_release_corpus_benchmark(root)
        + run_math_debugging_workbench_benchmark(root)
        + run_high_level_math_workflow_benchmark(root)
        + run_release_policy_benchmark(root)
    )
    summary = summarize_benchmark_results(results)

    assert summary == EXPECTED_BENCHMARK_SUMMARY
