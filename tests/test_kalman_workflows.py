from pathlib import Path

from mathdevmcp.kalman_workflows import audit_kalman_likelihood, build_kalman_review_packet
from mathdevmcp.notation import infer_symbol_hints


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_kalman_symbol_hints_are_candidates_not_assumptions():
    hints = infer_symbol_hints(["S_t", "v_t", "F_t", "H_t"], context_text="Kalman covariance residual transition observation")

    assert hints["hints"]["S_t"] == {"role_hint": "covariance_candidate", "shape_hint": "matrix_candidate", "status": "candidate_not_assumption"}
    assert hints["hints"]["v_t"]["role_hint"] == "residual_candidate"
    assert hints["hints"]["F_t"]["role_hint"] == "transition_matrix_candidate"
    assert hints["hints"]["H_t"]["role_hint"] == "observation_matrix_candidate"


def test_audit_kalman_likelihood_detects_missing_logdet_and_solve(tmp_path):
    code = tmp_path / "kalman.py"
    code.write_text("def ll(S, v):\n    return v @ v\n", encoding="utf-8")

    result = audit_kalman_likelihood(str(FIXTURES), "eq:proof-audit-kalman", str(code))

    assert result["status"] == "mismatch"
    missing = set(result["likelihood_audit"]["operation_consistency"]["missing_operations"])
    assert "logdet" in missing
    assert "inverse_or_solve" in missing
    assert result["metadata"] == {"schema_version": "1.0", "contract": "kalman_likelihood_audit"}


def test_audit_kalman_likelihood_unverified_when_operations_present_but_assumptions_missing(tmp_path):
    code = tmp_path / "kalman.py"
    code.write_text("def ll(S, v):\n    return slogdet(S)[1] + v @ solve(S, v)\n", encoding="utf-8")

    result = audit_kalman_likelihood(str(FIXTURES), "eq:proof-audit-kalman", str(code))

    assert result["status"] == "unverified"
    assert result["likelihood_audit"]["operation_consistency"]["missing_operations"] == []
    assert result["likelihood_audit"]["assumption_diagnostic"]["status"] == "missing_assumptions"


def test_build_kalman_review_packet_includes_actions_and_diagnostics(tmp_path):
    code = tmp_path / "kalman.py"
    code.write_text("def ll(S, v):\n    return v @ v\n", encoding="utf-8")

    packet = build_kalman_review_packet(str(FIXTURES), "eq:proof-audit-kalman", str(code))

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "kalman_review_packet"}
    assert packet["severity"] == "high"
    assert packet["source_label"] == "eq:proof-audit-kalman"
    kinds = {action["kind"] for action in packet["recommended_actions"]}
    assert "fix_or_explain_missing_operation" in kinds
    assert "synthetic_logdet_likelihood_test" in kinds
