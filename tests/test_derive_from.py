from mathdevmcp.derive_from import derive_from
from mathdevmcp.high_level_contracts import validate_high_level_result


def test_derive_from_proves_scoped_identity_with_backend_certificate() -> None:
    result = derive_from("a + b = b + a", givens=["a,b are scalars"])

    assert result["status"] == "proved"
    assert result["workflow"] == "derive_from"
    assert result["claim_class"] == "derivation"
    assert result["evidence_classes"] == ["backend_certificate"]
    assert result["certification_source"] == "backend"
    assert result["evidence"][0]["givens"] == ["a,b are scalars"]
    assert "givens_not_formal_assumptions" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_refutes_only_when_counterexample_artifact_exists() -> None:
    result = derive_from("A*B = B*A")

    assert result["status"] == "refuted"
    assert result["evidence_classes"] == ["backend_counterexample"]
    assert result["counterexamples"]
    assert validate_high_level_result(result) == []


def test_derive_from_does_not_promote_refutation_without_counterexample() -> None:
    result = derive_from("1 + 1 = 3")

    assert result["status"] == "inconclusive"
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_derive_from_reports_missing_assumptions_without_inserting_them() -> None:
    result = derive_from("logdet(A) = trace(A)")

    assert result["status"] == "missing_assumptions"
    assert result["assumptions"]
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_preserves_not_encodable_boundary() -> None:
    result = derive_from("not an equation")

    assert result["status"] == "not_encodable"
    assert result["certification_source"] == "none"
    assert "not_encodable_not_false" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_derive_from_records_explicit_assumptions_separately_from_givens() -> None:
    result = derive_from(
        "x / y = x * y**-1",
        givens=["we usually divide by nonzero denominators"],
        assumptions=["denominator is nonzero"],
    )

    assert result["evidence"][0]["givens"] == ["we usually divide by nonzero denominators"]
    assert result["evidence"][0]["explicit_assumptions"] == ["denominator is nonzero"]
    assert "givens_not_formal_assumptions" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []
