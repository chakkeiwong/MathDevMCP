from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.prove_or_counterexample import prove_or_counterexample


def test_prove_or_counterexample_proves_scoped_identity() -> None:
    result = prove_or_counterexample("a + b = b + a")

    assert result["status"] == "proved"
    assert result["workflow"] == "prove_or_counterexample"
    assert result["claim_class"] == "proof"
    assert result["evidence_classes"] == ["backend_certificate"]
    assert validate_high_level_result(result) == []


def test_prove_or_counterexample_refutes_with_counterexample() -> None:
    result = prove_or_counterexample("A*B = B*A")

    assert result["status"] == "refuted"
    assert result["evidence_classes"] == ["backend_counterexample"]
    assert result["counterexamples"]
    assert validate_high_level_result(result) == []


def test_prove_or_counterexample_does_not_disprove_without_counterexample_artifact() -> None:
    result = prove_or_counterexample("1 + 1 = 3")

    assert result["status"] == "inconclusive"
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_prove_or_counterexample_preserves_backend_or_encoding_boundaries() -> None:
    result = prove_or_counterexample("True = True", backend="lean")

    assert result["status"] in {"backend_unavailable", "not_encodable"}
    assert result["certification_source"] == "none"
    non_claim_codes = {item["code"] for item in result["non_claims"]}
    assert {"backend_unavailable_not_refutation", "not_encodable_not_false"} & non_claim_codes
    assert validate_high_level_result(result) == []


def test_prove_or_counterexample_malformed_claim_is_not_encodable_not_false() -> None:
    result = prove_or_counterexample("informal theorem with no equality")

    assert result["status"] == "not_encodable"
    assert result["certification_source"] == "none"
    assert "not_encodable_not_false" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_prove_or_counterexample_records_assumptions_without_claiming_completeness() -> None:
    result = prove_or_counterexample("x / y = x * y**-1", assumptions=["denominator is nonzero"])

    assert result["status"] in {"proved", "inconclusive", "not_encodable"}
    assert result["actions"]
    assert validate_high_level_result(result) == []
