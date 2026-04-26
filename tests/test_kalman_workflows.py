from pathlib import Path

from mathdevmcp.kalman_workflows import audit_kalman_likelihood, audit_kalman_recursion, build_kalman_review_packet
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


def test_audit_kalman_recursion_reports_unverified_without_shape_guards(tmp_path):
    code = tmp_path / "kalman_recursion.py"
    code.write_text(
        """
def step(F, H, Q, R, x, P, y):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
    x_filt = x_pred + K @ innovation
    P_filt = P_pred - K @ H @ P_pred
    return x_filt, P_filt
""",
        encoding="utf-8",
    )

    result = audit_kalman_recursion(str(code))

    assert result["status"] == "unverified"
    assert result["missing_operations"] == []
    assert result["shape_diagnostics"]["status"] == "missing_guards"
    assert "shape_guard" in result["shape_diagnostics"]["missing_guards"]
    assert result["metadata"] == {"schema_version": "1.0", "contract": "kalman_recursion_audit"}
    assert "ast_operation_graph" in result


def test_audit_kalman_recursion_detects_missing_covariance_update(tmp_path):
    code = tmp_path / "kalman_recursion_bad.py"
    code.write_text(
        """
def step(F, H, Q, R, x, P, y):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
    x_filt = x_pred + K @ innovation
    return x_filt, P_pred
""",
        encoding="utf-8",
    )

    result = audit_kalman_recursion(str(code))

    assert result["status"] == "mismatch"
    assert result["missing_operations"] == ["covariance_update"]
    assert any(action["target"] == "covariance_update" for action in result["recommended_actions"])


def test_audit_kalman_recursion_uses_explicit_shape_and_covariance_guards(tmp_path):
    code = tmp_path / "kalman_recursion_guarded.py"
    code.write_text(
        """
def step(F, H, Q, R, x, P, y):
    assert F.shape[0] == F.shape[1]
    assert P.shape[0] == P.shape[1]
    assert is_symmetric(P) and is_positive_semidefinite(P)
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
    x_filt = x_pred + K @ innovation
    P_filt = P_pred - K @ H @ P_pred
    return x_filt, P_filt
""",
        encoding="utf-8",
    )

    result = audit_kalman_recursion(str(code))

    assert result["status"] == "consistent"
    assert result["shape_diagnostics"]["missing_guards"] == []
    assert {item["operation"] for item in result["shape_diagnostics"]["evidence"]} >= {"shape_guard", "covariance_guard"}
