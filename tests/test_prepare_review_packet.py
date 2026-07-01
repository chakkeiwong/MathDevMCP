from mathdevmcp.assumptions_for import assumptions_for
from mathdevmcp.audit_math_to_code import audit_math_to_code
from mathdevmcp.derive_from import derive_from
from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.prepare_review_packet import prepare_review_packet, score_review_packet
from mathdevmcp.prove_or_counterexample import prove_or_counterexample


def test_prepare_review_packet_preserves_proof_as_nested_evidence_not_certificate() -> None:
    nested = derive_from("a + b = b + a")
    result = prepare_review_packet("Review derivation", evidence=[nested])

    assert result["status"] == "diagnostic_only"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["review_packet"]
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
    assert result["actions"]
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_structural_boundary() -> None:
    nested = audit_math_to_code("logdet(S)", "def f(S):\n    return logdet(S)\n")
    result = prepare_review_packet("Review code audit", evidence=[nested])

    assert result["status"] == "diagnostic_only"
    assert "diagnostic_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_review_packet_rubric_fails_empty_packet_for_completeness() -> None:
    result = prepare_review_packet("Empty packet")
    rubric = score_review_packet(result)

    assert result["status"] == "diagnostic_only"
    assert rubric["status"] == "failed"
    assert rubric["checks"]["has_nested_evidence"] is False
