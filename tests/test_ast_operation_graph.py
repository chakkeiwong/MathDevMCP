from mathdevmcp.ast_operation_graph import build_ast_operation_graph


def test_ast_operation_graph_detects_likelihood_linear_algebra():
    source = """
import numpy as np

def ll(S, v):
    sign, logdet = np.linalg.slogdet(S)
    alpha = np.linalg.solve(S, v)
    return -0.5 * (logdet + v @ alpha)
"""

    graph = build_ast_operation_graph(source, source_path="likelihood.py")

    assert graph["status"] == "consistent"
    assert graph["metadata"] == {"schema_version": "1.0", "contract": "ast_operation_graph"}
    assert {"logdet", "inverse_or_solve", "quadratic_form", "matmul"}.issubset(set(graph["operations"]))
    assert any(node["operation"] == "logdet" and node["line"] == 5 for node in graph["nodes"])


def test_ast_operation_graph_detects_kalman_recursion_assignments():
    source = """
def step(F, H, Q, R, x, P, y):
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    innovation = y - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ solve(S, eye(S.shape[0]))
    x_filt = x_pred + K @ innovation
    P_filt = P_pred - K @ H @ P_pred
    return x_filt, P_filt
"""

    graph = build_ast_operation_graph(source)

    assert "prediction_update" in graph["operations"]
    assert "innovation_update" in graph["operations"]
    assert "innovation_covariance" in graph["operations"]
    assert "kalman_gain" in graph["operations"]
    assert "state_update" in graph["operations"]
    assert "covariance_update" in graph["operations"]


def test_ast_operation_graph_reports_syntax_errors_as_inconclusive():
    graph = build_ast_operation_graph("def broken(:\n    pass\n")

    assert graph["status"] == "inconclusive"
    assert graph["operations"] == []
    assert graph["diagnostics"][0]["kind"] == "python_syntax_error"
