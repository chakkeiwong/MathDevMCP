from mathdevmcp.derive_from import derive_from
from mathdevmcp.high_level_contracts import validate_high_level_result


def test_derive_from_proves_scoped_identity_with_backend_certificate() -> None:
    result = derive_from("a + b = b + a", givens=["a,b are scalars"])

    assert result["status"] == "proved"
    assert result["workflow"] == "derive_from"
    assert result["claim_class"] == "derivation"
    assert result["evidence_classes"] == ["backend_certificate", "review_packet"]
    assert result["certification_source"] == "backend"
    certifying_evidence = next(item for item in result["evidence"] if item["class"] == "backend_certificate")
    route_evidence = next(item for item in result["evidence"] if item["id"] == "derive_from:route-plan")
    assert route_evidence["class"] == "review_packet"
    assert route_evidence["givens"] == ["a,b are scalars"]
    assert "givens" not in certifying_evidence
    assert route_evidence["route_plan"]["scope"] == "derive_from_route_plan"
    assert route_evidence["route_plan"]["givens"] == ["a,b are scalars"]
    assert route_evidence["route_plan"]["backend_route"]["status"] == "proved"
    assert route_evidence["route_plan"]["obligations"][0]["status"] == "proved"
    assert result["gaps"][0]["status"] == "proved"
    assert result["proposals"][0]["type"] == "accept_backend_certificate"
    assert result["proposals"][0]["validation"]["status"] == "certified_by_backend"
    assert result["validation"]["certifying_proposal_count"] == 1
    assert result["tool_uses"][0]["tool"] == "derive_or_refute"
    assert result["agent_handoff"]["derivation_gap_ledger"] == result["gaps"]
    assert "givens_not_formal_assumptions" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_refutes_only_when_counterexample_artifact_exists() -> None:
    result = derive_from("A*B = B*A")

    assert result["status"] == "refuted"
    assert result["evidence_classes"] == ["backend_counterexample", "review_packet"]
    assert result["counterexamples"]
    assert result["gaps"][0]["status"] == "refuted"
    assert result["proposals"][0]["type"] == "accept_counterexample"
    assert result["proposals"][0]["validation"]["status"] == "refuted_by_counterexample"
    assert validate_high_level_result(result) == []


def test_derive_from_does_not_promote_refutation_without_counterexample() -> None:
    result = derive_from("1 + 1 = 3")

    assert result["status"] == "inconclusive"
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert result["gaps"][0]["status"] == "refuted"
    assert result["proposals"][0]["type"] == "manual_review_with_named_gap"
    assert result["proposals"][0]["validation"]["status"] == "abstained_no_certifying_route"
    assert validate_high_level_result(result) == []


def test_derive_from_reports_missing_assumptions_without_inserting_them() -> None:
    result = derive_from("logdet(A) = trace(A)")

    assert result["status"] == "missing_assumptions"
    assert result["assumptions"]
    route_evidence = next(item for item in result["evidence"] if item["id"] == "derive_from:route-plan")
    assert route_evidence["route_plan"]["route_gaps"][0]["kind"] == "missing_assumptions"
    assert route_evidence["route_plan"]["obligations"][0]["missing_assumptions"]
    assert result["gaps"][0]["status"] == "missing_assumptions"
    assert result["gaps"][0]["assumption_gaps"]
    assert result["proposals"][0]["type"] == "add_assumptions"
    assert result["proposals"][0]["assumption_repairs"]
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_preserves_not_encodable_boundary() -> None:
    result = derive_from("not an equation")

    assert result["status"] == "not_encodable"
    assert result["certification_source"] == "none"
    assert result["gaps"][0]["status"] == "not_encodable"
    assert result["proposals"][0]["type"] == "formalize_target"
    assert result["proposals"][0]["validation"]["status"] == "blocked_by_not_encodable"
    assert "not_encodable_not_false" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_records_explicit_assumptions_separately_from_givens() -> None:
    result = derive_from(
        "x / y = x * y**-1",
        givens=["we usually divide by nonzero denominators"],
        assumptions=["denominator is nonzero"],
    )

    route_evidence = next(item for item in result["evidence"] if item["id"] == "derive_from:route-plan")
    assert route_evidence["givens"] == ["we usually divide by nonzero denominators"]
    assert route_evidence["explicit_assumptions"] == ["denominator is nonzero"]
    route_plan = route_evidence["route_plan"]
    assert route_plan["givens"] == ["we usually divide by nonzero denominators"]
    assert route_plan["explicit_assumptions"] == ["denominator is nonzero"]
    assert result["tool_uses"][0]["arguments"]["givens"] == ["we usually divide by nonzero denominators"]
    assert result["tool_uses"][0]["arguments"]["assumptions"] == ["denominator is nonzero"]
    assert "not an unchecked derivation chain" in route_plan["boundary"]
    assert "givens_not_formal_assumptions" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_unknown_returns_formalization_proposal() -> None:
    result = derive_from("A = A")

    assert result["status"] == "inconclusive"
    assert result["gaps"][0]["status"] == "unknown"
    assert result["proposals"][0]["type"] == "formalize_target"
    assert result["proposals"][0]["validation"]["status"] == "abstained_no_certifying_route"
    assert result["agent_handoff"]["proposal_count"] == len(result["proposals"])
    assert validate_high_level_result(result) == []
