from mathdevmcp.math_debugging import validate_workbench_result
from mathdevmcp.math_debugging_router import route_math_obligation


def test_router_routes_commutative_scalar_identity_to_sympy_certificate() -> None:
    result = route_math_obligation("a + b", "b + a")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_debugging_route_decision"}
    assert result["route"] == "symbolic"
    assert result["status"] == "proved"
    assert result["backend_attempt"]["severity"] == "certifying"
    assert validate_workbench_result(result["result"]) == []


def test_router_routes_scalar_false_identity_to_refutation() -> None:
    result = route_math_obligation("1 + 1", "3")

    assert result["route"] == "symbolic"
    assert result["status"] == "refuted"
    assert result["backend_attempt"]["severity"] == "blocking"
    assert result["result"]["status"] == "refuted"


def test_router_abstains_on_unsafe_syntax_without_refutation() -> None:
    result = route_math_obligation("__import__('os')", "0")

    assert result["route"] == "human_review"
    assert result["status"] == "not_encodable"
    assert result["backend_attempt"]["severity"] == "diagnostic"
    assert result["result"]["status"] == "not_encodable"


def test_router_sends_matrix_like_expression_to_human_review() -> None:
    result = route_math_obligation("logdet(A)", "trace(A)")

    assert result["route"] == "human_review"
    assert result["status"] == "unknown"
    assert "matrix/domain review" in result["reason"]


def test_router_reports_sage_unavailable_as_diagnostic_not_refutation() -> None:
    result = route_math_obligation("a + b", "b + a", backend="sage")

    assert result["route"] == "sage"
    assert result["status"] in {"backend_unavailable", "unknown"}
    assert result["backend_attempt"]["severity"] == "diagnostic"
    assert result["status"] != "refuted"


def test_router_requires_explicit_lean_source() -> None:
    result = route_math_obligation("True", "True", backend="lean")

    assert result["route"] == "lean"
    assert result["status"] == "not_encodable"
    assert result["backend_attempt"]["severity"] == "diagnostic"
