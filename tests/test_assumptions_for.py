from mathdevmcp.assumptions_for import assumptions_for, score_assumption_set
from mathdevmcp.high_level_contracts import validate_high_level_result


def test_assumptions_for_logdet_reports_route_required_domain() -> None:
    result = assumptions_for("logdet(A)")

    assert result["status"] == "missing_assumptions"
    assert result["workflow"] == "assumptions_for"
    assert result["claim_class"] == "assumption_discovery"
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in result["non_claims"]}
    assert result["assumptions"][0]["route_categories"] == ["covariance_condition", "domain_condition"]
    assert result["evidence_ledger"]["assumption_items"][0]["route_categories"] == [
        "covariance_condition",
        "domain_condition",
    ]
    rubric = score_assumption_set(result, {"determinant domain"})
    assert rubric["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_assumptions_for_inverse_and_division_scores_by_set_terms() -> None:
    result = assumptions_for("x / y + inv(A)")

    rubric = score_assumption_set(result, {"denominator is nonzero", "invertible"})
    categories_by_text = {item["text"]: item["route_categories"] for item in result["assumptions"]}

    assert result["status"] == "missing_assumptions"
    assert categories_by_text["denominator is nonzero"] == ["domain_condition"]
    assert categories_by_text["matrix operand is square and invertible"] == ["domain_condition", "shape_condition"]
    assert rubric["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_assumptions_for_provided_assumption_does_not_claim_minimality() -> None:
    result = assumptions_for("x / y", provided_assumptions=["denominator is nonzero"])

    assert result["status"] == "inconclusive"
    assert "general_theorem_proving_not_claimed" in {item["code"] for item in result["non_claims"]}
    assert not any("minimal" in item["text"].lower() for item in result["non_claims"])
    assert validate_high_level_result(result) == []


def test_assumptions_for_unknown_route_is_inconclusive_not_proof() -> None:
    result = assumptions_for("x + y")

    assert result["status"] == "inconclusive"
    assert result["certification_source"] == "none"
    assert result["veto_reasons"]
    assert validate_high_level_result(result) == []


def test_assumption_set_rubric_reports_missing_terms() -> None:
    result = assumptions_for("logdet(A)")
    rubric = score_assumption_set(result, {"stationarity"})

    assert rubric["status"] == "failed"
    assert rubric["missing_terms"] == ["stationarity"]
