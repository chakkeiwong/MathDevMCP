from mathdevmcp.assumption_discovery import assumptions_required
from mathdevmcp.math_debugging import validate_workbench_result


def test_assumption_discovery_flags_division_nonzero_route_requirement() -> None:
    result = assumptions_required("x / y")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "assumption_discovery_result"}
    assert result["status"] == "missing_assumptions"
    assert result["missing_assumptions"][0]["text"] == "denominator is nonzero"
    assert result["missing_assumptions"][0]["necessity"] == "required_by_route"
    assert validate_workbench_result(result["workbench_result"]) == []


def test_assumption_discovery_marks_provided_route_assumption_without_minimality_claim() -> None:
    result = assumptions_required("x / y", provided_assumptions=["denominator is nonzero"])

    assert result["status"] == "proved"
    assert result["assumptions"][0]["status"] == "provided"
    assert result["assumptions"][0]["necessity"] == "required_by_route"
    assert "minimal" not in result["reason"].lower()
    assert "necessary" not in result["reason"].lower()


def test_assumption_discovery_flags_logdet_and_inverse_conditions() -> None:
    result = assumptions_required("logdet(A) + inv(A)")

    texts = {item["text"] for item in result["missing_assumptions"]}

    assert "matrix operand is square and invertible" in texts
    assert "matrix operand is square with valid determinant domain, usually positive definite for logdet" in texts
    assert result["status"] == "missing_assumptions"


def test_assumption_discovery_flags_sqrt_derivative_and_shape_requirements() -> None:
    result = assumptions_required("sqrt(x) + grad(f) + trace(A)")
    texts = {item["text"] for item in result["missing_assumptions"]}

    assert "square-root argument is nonnegative in the target domain" in texts
    assert "target function is differentiable on the stated domain" in texts
    assert "matrix dimensions are conformable for the operation" in texts


def test_assumption_discovery_unknown_when_no_bounded_rule_applies() -> None:
    result = assumptions_required("x + y")

    assert result["status"] == "unknown"
    assert result["missing_assumptions"] == []
    assert result["workbench_result"]["status"] == "unknown"
