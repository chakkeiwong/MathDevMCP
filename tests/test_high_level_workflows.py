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
    assert result["evidence"][0]["backend_route_status"] == "proved"
    assert result["evidence"][0]["backend_attempt"]["status"] == "proved"
    assert result["evidence"][0]["obligation"]["id"] == "derive-target-1"
    assert result["evidence_ledger"]["provenance"] == {
        "workflow": "derive_from",
        "status": "proved",
        "certification_source": "backend",
        "evidence_classes": ["backend_certificate"],
    }
    assert validate_high_level_result(result) == []


def test_scoped_handoff_fixture_has_case_local_ledger_without_usefulness_claim() -> None:
    low_level = derive_or_refute("a + b = b + a")
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
    )

    baseline_fixture = {
        "question": result["question"],
        "status": result["status"],
        "evidence_classes": result["evidence_classes"],
    }
    ledger = result["evidence_ledger"]

    assert "evidence_ledger" not in baseline_fixture
    assert ledger["scope"] == "scoped_high_level_workflow_result"
    assert ledger["evidence_items"][0]["source"] == "backend"
    assert ledger["non_claim_codes"] == sorted(item["code"] for item in result["non_claims"])
    assert "downstream-agent usefulness" in ledger["boundary"]
    assert "not independent proof" in ledger["boundary"]
    assert validate_high_level_result(result) == []


def test_legacy_consumer_projection_tolerates_producer_emitted_evidence_ledger() -> None:
    low_level = derive_or_refute("a + b = b + a")
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
    )

    legacy_projection = {
        key: result[key]
        for key in (
            "status",
            "workflow",
            "question",
            "claim_class",
            "answer",
            "evidence",
            "evidence_classes",
            "certification_source",
            "veto_reasons",
            "assumptions",
            "counterexamples",
            "actions",
            "non_claims",
            "metadata",
        )
    }

    assert "evidence_ledger" in result
    assert validate_high_level_result(legacy_projection) == []


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
    assert result["evidence"][0]["backend_route_status"] == "refuted"
    assert result["evidence"][0]["counterexample"]["assignments"]
    assert result["evidence"][0]["counterexample"]["lhs_value"] != result["evidence"][0]["counterexample"]["rhs_value"]
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
    assert result["evidence_classes"] == ["human_review_required"]
    assert not any(item["class"] == "backend_counterexample" for item in result["evidence"])
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_kernel_does_not_promote_proof_without_backend_attempt_and_obligation() -> None:
    low_level = derive_or_refute("a + b = b + a")
    low_level["route_decision"]["backend_attempt"] = None
    low_level["workbench_result"]["backend_attempts"] = []
    low_level["workbench_result"]["obligations"] = []
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
    )

    assert result["status"] == "inconclusive"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["human_review_required"]
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_kernel_does_not_promote_proof_with_noncertifying_or_inconsistent_artifacts() -> None:
    low_level = derive_or_refute("a + b = b + a")
    low_level["route_decision"]["backend_attempt"]["severity"] = "diagnostic"
    low_level["workbench_result"]["backend_attempts"][0]["severity"] = "diagnostic"
    low_level["workbench_result"]["obligations"][0]["status"] = "unknown"
    result = package_low_level_math_result(
        low_level,
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
    )

    assert result["status"] == "inconclusive"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["human_review_required"]
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
