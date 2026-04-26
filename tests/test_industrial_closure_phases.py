from pathlib import Path

from mathdevmcp.ast_operation_graph import build_ast_operation_graph_for_file
from mathdevmcp.corpus_roadmap import department_corpus_roadmap
from mathdevmcp.deployment import deployment_policy
from mathdevmcp.industrial_review import build_industrial_review_packet
from mathdevmcp.leandojo_policy import leandojo_backend_policy
from mathdevmcp.numeric_diagnostics import suggest_numeric_diagnostics
from mathdevmcp.parser_policy import decide_parser_policy
from mathdevmcp.routing import route_label_obligation
from mathdevmcp.shape_diagnostics import diagnose_shape_constraints
from mathdevmcp.typed_workflows import typed_obligation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_typed_route_sends_simple_algebra_to_symbolic():
    result = route_label_obligation(str(FIXTURES), "eq:proof-audit-single")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "typed_route_decision"}
    assert result["status"] == "routed"
    assert result["route"] == "symbolic"
    assert "sympy" in result["backend_candidates"]


def test_typed_route_sends_state_space_missing_constraints_to_human_review():
    result = route_label_obligation(str(FIXTURES), "eq:dept-state-space-likelihood")

    assert result["status"] == "human_review"
    assert result["route"] == "human_review"
    assert {item["kind"] for item in result["missing_constraints"]} >= {"invertibility_required", "square_matrix_required"}


def test_shape_diagnostics_reports_ast_guard_evidence_as_supporting_not_proof():
    typed = typed_obligation_for_label(str(FIXTURES), "eq:dept-state-space-likelihood")
    graph = build_ast_operation_graph_for_file(FIXTURES / "doc_department_state_space_jax.py")

    result = diagnose_shape_constraints(typed["typed_diagnostic"], ast_graph=graph)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "shape_diagnostic_result"}
    assert result["status"] == "partially_supported"
    assert result["missing_constraints"]
    assert any(item["operation"] == "shape_guard" for item in result["ast_evidence"])


def test_numeric_diagnostics_suggest_logdet_solve_and_gradient_checks():
    state = typed_obligation_for_label(str(FIXTURES), "eq:dept-state-space-likelihood")
    hmc = typed_obligation_for_label(str(FIXTURES), "eq:dept-hmc-leapfrog")

    state_suggestions = suggest_numeric_diagnostics(state["typed_diagnostic"])
    hmc_suggestions = suggest_numeric_diagnostics(hmc["typed_diagnostic"])

    assert {item["kind"] for item in state_suggestions["suggestions"]} >= {"logdet_domain_check", "linear_solve_residual_check"}
    assert any(item["kind"] == "finite_difference_gradient_check" for item in hmc_suggestions["suggestions"])


def test_department_corpus_roadmap_records_private_policy_and_false_confidence_seeds():
    roadmap = department_corpus_roadmap()

    assert roadmap["metadata"] == {"schema_version": "1.0", "contract": "department_corpus_roadmap"}
    categories = {entry["category"]: entry for entry in roadmap["entries"]}
    assert "kalman_state_space" in categories
    assert "ml_llm_objectives" in categories
    assert categories["kalman_state_space"]["required_false_confidence_seed"] == "missing_solve_or_covariance_update"
    assert "private" in categories["dsge_macro_finance"]["privacy"]


def test_parser_policy_selects_current_parser_when_labels_and_provenance_are_preserved():
    policy = decide_parser_policy(str(FIXTURES), backends=["current"])

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "parser_policy_decision"}
    assert policy["status"] == "selected"
    assert policy["selected_backend"] == "current"
    assert policy["benchmark_report"]["summary"]["label_preserving"] == 1


def test_leandojo_policy_distinguishes_import_smoke_from_dojo_readiness():
    policy = leandojo_backend_policy(traced_repo_available=False)

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "leandojo_backend_policy"}
    assert policy["status"] in {"inconclusive", "dojo_ready_candidate"}
    assert "direct Lean final check" in policy["final_certificate_policy"]
    assert "traced Lean repository target" in policy["required_artifacts"]


def test_industrial_review_packet_collects_actions_without_verification_claims():
    packet = build_industrial_review_packet(str(FIXTURES), "eq:dept-state-space-likelihood")

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "industrial_review_packet"}
    assert packet["status"] == "unverified"
    assert packet["severity"] == "high"
    kinds = {action["kind"] for action in packet["recommended_actions"]}
    assert "state_or_verify_missing_constraint" in kinds
    assert "logdet_domain_check" in kinds
    assert packet["evidence"]["route_decision"]["status"] == "human_review"


def test_deployment_policy_records_optional_worker_isolation():
    policy = deployment_policy()

    assert "optional_worker_recommendations" in policy
    assert "leandojo_worker" in policy["optional_worker_recommendations"]
    assert "sandboxing" in policy["resource_policy"]
