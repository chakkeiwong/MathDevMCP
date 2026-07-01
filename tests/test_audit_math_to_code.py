from mathdevmcp.audit_math_to_code import audit_math_to_code
from mathdevmcp.high_level_contracts import validate_high_level_result


def test_audit_math_to_code_reports_structural_match_not_proof() -> None:
    result = audit_math_to_code(
        "logdet(S) + solve(S, v)",
        "def f(S, v):\n    return logdet(S) + solve(S, v)\n",
    )

    assert result["status"] == "structural_match"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["structural_match"]
    assert "structural_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_audit_math_to_code_reports_structural_mismatch() -> None:
    result = audit_math_to_code(
        "logdet(S) + solve(S, v)",
        "def f(S, v):\n    return solve(S, v)\n",
    )

    assert result["status"] == "structural_mismatch"
    assert result["evidence_classes"] == ["structural_mismatch"]
    assert result["actions"]
    assert validate_high_level_result(result) == []


def test_audit_math_to_code_preserves_alias_support() -> None:
    result = audit_math_to_code(
        "logdet(Sigma)",
        "def f(S):\n    return logdet(S)\n",
        aliases={"Sigma": "S"},
    )

    assert result["status"] == "structural_match"
    assert result["evidence"][0]["low_level"]["matched_terms"]
    assert validate_high_level_result(result) == []


def test_audit_math_to_code_extra_terms_are_audit_only() -> None:
    result = audit_math_to_code(
        "solve(S, v)",
        "def f(S, v, lam):\n    return solve(S, v) + lam\n",
    )

    assert result["status"] == "structural_match"
    assert "lam" in result["evidence"][0]["low_level"]["extra_code_terms"]
    assert result["status"] != "proved"
    assert validate_high_level_result(result) == []
