from mathdevmcp.assumption_discovery import assumptions_required
from mathdevmcp.derive_or_refute import derive_or_refute
from mathdevmcp.equation_code_match import code_implements_equation
from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.high_level_workflows import (
    package_assumption_result,
    package_code_audit_result,
    package_low_level_math_result,
    package_proof_gap_result,
    package_review_packet_result,
)
from mathdevmcp.math_review_packet import build_math_review_packet
from mathdevmcp.proof_gap import localize_proof_gap
from mathdevmcp.prove_or_refute import prove_or_refute


def test_kernel_packages_backend_proof_without_changing_evidence_boundary() -> None:
    low_level = derive_or_refute("a + b = b + a")
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
    )

    assert result["status"] == "proved"
    assert result["claim_class"] == "derivation"
    assert result["evidence_classes"] == ["backend_certificate"]
    assert result["certification_source"] == "backend"
    assert result["evidence"][0]["low_level"]["metadata"]["contract"] == "derive_or_refute_result"
    assert validate_high_level_result(result) == []


def test_kernel_packages_refutation_with_counterexample() -> None:
    low_level = prove_or_refute("A*B = B*A")
    result = package_low_level_math_result(
        low_level,
        workflow="prove_or_counterexample",
        question="Can we prove A*B = B*A?",
    )

    assert result["status"] == "refuted"
    assert result["evidence_classes"] == ["backend_counterexample"]
    assert result["counterexamples"]
    assert validate_high_level_result(result) == []


def test_kernel_does_not_promote_refutation_without_counterexample_artifact() -> None:
    low_level = prove_or_refute("1 + 1 = 3")
    low_level["counterexample_search"] = None
    low_level["workbench_result"]["counterexamples"] = []
    result = package_low_level_math_result(
        low_level,
        workflow="prove_or_counterexample",
        question="Can we prove 1 + 1 = 3?",
    )

    assert result["status"] == "inconclusive"
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_kernel_preserves_backend_unavailable_as_nonclaim() -> None:
    low_level = prove_or_refute("True = True", backend="lean")
    result = package_low_level_math_result(
        low_level,
        workflow="prove_or_counterexample",
        question="Can Lean prove True = True?",
    )

    assert result["status"] == "not_encodable"
    assert result["certification_source"] == "none"
    assert "not_encodable_not_false" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_kernel_packages_assumption_discovery_with_minimality_nonclaim() -> None:
    low_level = assumptions_required("logdet(A)")
    result = package_assumption_result(low_level, question="What assumptions are needed for logdet(A)?")

    assert result["status"] == "missing_assumptions"
    assert result["assumptions"]
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_kernel_packages_proof_gap_as_local_gap_not_global_failure() -> None:
    low_level = localize_proof_gap(["logdet(A)", "trace(A)", "trace(A)"])
    result = package_proof_gap_result(low_level, question="Where does this derivation fail?")

    assert result["status"] == "gap_found"
    assert result["evidence_classes"] == ["proof_gap"]
    assert "gap_localization_not_global_failure" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_kernel_packages_code_audit_as_structural_not_semantic_proof() -> None:
    low_level = code_implements_equation(
        "logdet(S)",
        "def f(S):\n    return logdet(S)\n",
    )
    result = package_code_audit_result(low_level, question="Does code implement logdet(S)?")

    assert result["status"] == "structural_match"
    assert result["certification_source"] == "none"
    assert "structural_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []


def test_kernel_packages_review_packet_as_diagnostic_only() -> None:
    evidence = [derive_or_refute("a + b = b + a")]
    low_level = build_math_review_packet("Review the derivation", evidence=evidence)
    result = package_review_packet_result(low_level, question="Prepare a review packet.")

    assert result["status"] == "diagnostic_only"
    assert result["evidence_classes"] == ["review_packet"]
    assert "diagnostic_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert validate_high_level_result(result) == []
