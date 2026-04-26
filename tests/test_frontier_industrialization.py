from pathlib import Path

from mathdevmcp.agent_workflows import audit_likelihood_implementation
from mathdevmcp.benchmark_manifest import benchmark_manifest
from mathdevmcp.deployment import deployment_policy
from mathdevmcp.diagnostic_tests import suggest_diagnostic_tests
from mathdevmcp.notation import extract_notation_records, infer_symbol_hints
from mathdevmcp.review_packet import build_likelihood_review_packet


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_review_packet_prioritizes_missing_likelihood_operations(tmp_path):
    code = tmp_path / "bad_likelihood.py"
    code.write_text("def ll(S, v):\n    return v @ v\n", encoding="utf-8")

    packet = build_likelihood_review_packet(
        str(FIXTURES),
        "eq:proof-audit-kalman",
        str(code),
        required_operations=["logdet", "quadratic_form"],
        context_text="Kalman likelihood",
    )

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "review_packet"}
    assert packet["severity"] == "high"
    assert any(action["target"] == "logdet" for action in packet["recommended_actions"])


def test_notation_records_extract_explicit_roles_and_symbol_hints():
    records = extract_notation_records("S_t is the covariance matrix. x_t denotes the state vector.")
    hints = infer_symbol_hints(["S_t", "v_t"], context_text="Kalman covariance residual")

    assert {record["role"] for record in records["records"]} >= {"covariance_matrix", "state_vector"}
    assert hints["hints"]["S_t"]["status"] == "candidate_not_assumption"
    assert hints["hints"]["S_t"]["shape_hint"] == "matrix_candidate"


def test_diagnostic_suggestions_follow_audit_findings(tmp_path):
    code = tmp_path / "bad_likelihood.py"
    code.write_text("def ll(S, v):\n    return v @ v\n", encoding="utf-8")
    audit = audit_likelihood_implementation(
        str(FIXTURES),
        "eq:proof-audit-kalman",
        str(code),
        required_operations=["logdet", "inverse_or_solve"],
        context_text="Kalman likelihood",
    )

    suggestions = suggest_diagnostic_tests(audit)

    kinds = {suggestion["kind"] for suggestion in suggestions["suggestions"]}
    assert "synthetic_logdet_likelihood_test" in kinds
    assert "linear_solve_consistency_test" in kinds
    assert "finite_difference_gradient_check" in kinds


def test_benchmark_manifest_marks_private_corpus_external():
    manifest = benchmark_manifest()

    private = next(entry for entry in manifest["entries"] if entry["name"] == "private_department_corpus")
    assert private["privacy"] == "private"
    assert private["in_git"] is False
    assert manifest["metadata"] == {"schema_version": "1.0", "contract": "benchmark_manifest"}


def test_deployment_policy_documents_optional_backend_isolation():
    policy = deployment_policy()

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "deployment_policy"}
    assert "leandojo" in policy["optional_backend_groups"]
    assert any("separate backend environment" in item for item in policy["known_conflicts"])
