from mathdevmcp.assumptions_for import assumptions_for
from mathdevmcp.audit_math_to_code import audit_math_to_code
from mathdevmcp.derive_from import derive_from
from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.prepare_review_packet import prepare_review_packet, score_review_packet
from mathdevmcp.prove_or_counterexample import prove_or_counterexample


def test_prepare_review_packet_preserves_proof_as_nested_evidence_not_certificate() -> None:
    nested = derive_from("a + b = b + a")
    result = prepare_review_packet("Review derivation", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["review_packet"]
    assert low_level["backend_checks"]
    assert "not recertified" in low_level["backend_checks"][0]["boundary"]
    assert score_review_packet(result)["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_refutation_blocker() -> None:
    nested = prove_or_counterexample("A*B = B*A")
    result = prepare_review_packet("Review failed proof", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert low_level["status"] == "blocked_by_refutation"
    assert low_level["evidence"][0]["counterexamples"]
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_missing_assumptions() -> None:
    nested = assumptions_for("logdet(A)")
    result = prepare_review_packet("Review assumptions", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert low_level["status"] == "needs_human_review"
    assert low_level["assumptions"]
    assert any(gap["kind"] == "missing_assumptions" for gap in low_level["residual_gaps"])
    assert result["actions"]
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_structural_boundary() -> None:
    nested = audit_math_to_code("logdet(S)", "def f(S):\n    return logdet(S)\n")
    result = prepare_review_packet("Review code audit", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert "diagnostic_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert low_level["trace_maps"]
    assert "not semantic proof" in low_level["trace_maps"][0]["boundary"]
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_compiles_route_trace_risks_and_non_claims() -> None:
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    code_audit = audit_math_to_code(
        "logdet(Sigma) + trace(Cov)",
        "def f(S):\n    return logdet(S) + trace(S)\n",
        aliases={"Sigma": "S", "Cov": "S"},
    )
    result = prepare_review_packet(
        "Review derivation and implementation context",
        evidence=[derived, code_audit],
        source={"context_summary": "Local review fixture with one derivation and one structural code audit."},
    )
    low_level = result["evidence"][0]["low_level"]
    risk_codes = {item["code"] for item in low_level["risk_register"]}
    non_claim_codes = {item["code"] for item in low_level["non_claims"]}

    assert low_level["route_plans"]
    assert low_level["route_plans"][0]["route_plan"]["givens"] == ["a,b are scalars"]
    assert low_level["trace_maps"][0]["trace_map"]["alias_collisions"] == [
        {"mapped_code_term": "S", "equation_terms": ["Cov", "Sigma"]}
    ]
    assert low_level["nested_evidence_summary"]
    assert low_level["decision_criteria"]
    assert {"route_plans_are_diagnostic", "trace_maps_are_structural"}.issubset(risk_codes)
    assert "givens_not_formal_assumptions" in non_claim_codes
    assert "diagnostic_route_and_trace_context_not_proof" in non_claim_codes
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_review_packet_rubric_fails_empty_packet_for_completeness() -> None:
    result = prepare_review_packet("Empty packet")
    rubric = score_review_packet(result)
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert any(item["code"] == "empty_packet" for item in low_level["risk_register"])
    assert rubric["status"] == "failed"
    assert rubric["checks"]["has_nested_evidence"] is False
