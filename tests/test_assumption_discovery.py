from mathdevmcp.assumption_discovery import assumptions_required
from mathdevmcp.math_debugging import validate_workbench_result


SCOPED_ROUTE_TAXONOMY_ORACLE = {
    "x / y": {
        "denominator is nonzero": ["domain_condition"],
    },
    "logdet(A) + inv(A)": {
        "matrix operand is square and invertible": ["domain_condition", "shape_condition"],
        "matrix operand is square with valid determinant domain, usually positive definite for logdet": [
            "covariance_condition",
            "domain_condition",
        ],
    },
    "sqrt(x) + grad(f) + trace(A)": {
        "square-root argument is nonnegative in the target domain": ["domain_condition"],
        "target function is differentiable on the stated domain": ["smoothness_condition"],
        "matrix dimensions are conformable for the operation": ["shape_condition"],
    },
}


def _observed_categories(result: dict) -> dict[str, list[str]]:
    return {
        item["text"]: sorted(item.get("route_categories", []))
        for item in result["missing_assumptions"]
    }


def test_assumption_discovery_flags_division_nonzero_route_requirement() -> None:
    result = assumptions_required("x / y")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "assumption_discovery_result"}
    assert result["status"] == "missing_assumptions"
    assert result["missing_assumptions"][0]["text"] == "denominator is nonzero"
    assert result["missing_assumptions"][0]["necessity"] == "required_by_route"
    assert result["missing_assumptions"][0]["route_categories"] == ["domain_condition"]
    assert result["missing_assumptions"][0]["route_category_sources"] == ["assumption_rule:division_nonzero"]
    assert validate_workbench_result(result["workbench_result"]) == []


def test_assumption_discovery_marks_provided_route_assumption_without_minimality_claim() -> None:
    result = assumptions_required("x / y", provided_assumptions=["denominator is nonzero"])

    assert result["status"] == "unknown"
    assert result["assumptions"][0]["status"] == "provided"
    assert result["assumptions"][0]["necessity"] == "required_by_route"
    assert "minimal" not in result["reason"].lower()
    assert "prove" in result["reason"].lower()


def test_exact_latex_denominator_assumption_discharges_expression_requirement() -> None:
    target = r"dTV = \frac{rho*dCF_next}{r_{\mathrm{disc}}+\lambda_{\mathrm{attrition}}+q}"
    supplied = "r_disc + lambda_attrition + q != 0"

    result = assumptions_required(target, provided_assumptions=[supplied])

    assumption = result["assumptions"][0]
    assert assumption["status"] == "provided"
    assert assumption["requirement_expression"] == r"r_{\mathrm{disc}}+\lambda_{\mathrm{attrition}}+q"
    assert assumption["discharged_by"] == supplied
    assert result["missing_assumptions"] == []


def test_wrong_nonzero_expression_does_not_discharge_denominator() -> None:
    target = "dTV = rho*dCF_next/(r_disc + lambda_attrition + q)"

    result = assumptions_required(target, provided_assumptions=["r_disc != 0"])

    assert result["missing_assumptions"]


def test_assumption_discovery_flags_logdet_and_inverse_conditions() -> None:
    result = assumptions_required("logdet(A) + inv(A)")

    texts = {item["text"] for item in result["missing_assumptions"]}

    assert "matrix operand is square and invertible" in texts
    assert "matrix operand is square with valid determinant domain, usually positive definite for logdet" in texts
    assert _observed_categories(result) == SCOPED_ROUTE_TAXONOMY_ORACLE["logdet(A) + inv(A)"]
    assert result["status"] == "missing_assumptions"


def test_assumption_discovery_flags_sqrt_derivative_and_shape_requirements() -> None:
    result = assumptions_required("sqrt(x) + grad(f) + trace(A)")
    texts = {item["text"] for item in result["missing_assumptions"]}

    assert "square-root argument is nonnegative in the target domain" in texts
    assert "target function is differentiable on the stated domain" in texts
    assert "matrix dimensions are conformable for the operation" in texts
    assert _observed_categories(result) == SCOPED_ROUTE_TAXONOMY_ORACLE["sqrt(x) + grad(f) + trace(A)"]


def test_assumption_discovery_unknown_when_no_bounded_rule_applies() -> None:
    result = assumptions_required("x + y")

    assert result["status"] == "unknown"
    assert result["missing_assumptions"] == []
    assert result["workbench_result"]["status"] == "unknown"
