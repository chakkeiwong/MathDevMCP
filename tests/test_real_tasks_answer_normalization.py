from pathlib import Path

from mathdevmcp.real_tasks_answer_normalization import normalize_real_task_answer
from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest
from mathdevmcp.real_tasks_scoring import score_real_task_case


ROOT = Path(__file__).resolve().parent.parent


def test_real_task_answer_normalization_normalizes_mf03_free_form_answer() -> None:
    result = normalize_real_task_answer(
        "MF-03-hmc-helper-nonclaim-boundary",
        "These are numerical-stability helpers around the mass-matrix and ESS / R-hat diagnostics, not structural-identification tests.",
    )

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_answer_normalization",
    }
    assert result["status"] == "consistent"
    assert result["candidate"]["status"] == "consistent"
    assert result["candidate"]["substatus"] == "helper_nonclaim_boundary_preserved"


def test_real_task_answer_normalization_normalizes_mf04_free_form_answer() -> None:
    result = normalize_real_task_answer(
        "MF-04-short-hmc-acceptance-veto-diagnosis",
        "Classification: inconclusive. The acceptance-veto diagnosis requires trusted same-process GPU execution, trusted_execution_provenance_passed was False, and downstream launch remains not authorized. fix the diagnostic blocker or revise under Claude/Codex review.",
    )

    assert result["status"] == "consistent"
    assert result["candidate"]["status"] == "inconclusive"
    assert result["candidate"]["substatus"] == "trusted_gpu_provenance_blocked"


def test_real_task_answer_normalization_rejects_unsupported_case_id() -> None:
    result = normalize_real_task_answer("LP-01-analytical-validation-lgssm", "Some answer")

    assert result["status"] == "inconclusive"
    assert result["candidate"] is None


def test_real_task_answer_normalization_normalizes_dh06_free_form_answer() -> None:
    result = normalize_real_task_answer(
        "DH-06-densesoap-source-contract-mismatch",
        "DENSESOAP_REMAINS_DIAGNOSTIC_ONLY. The TensorFlow DenseSOAP surfaces remain diagnostic only because there is a material default mismatch, a missing official feature, a step/cadence mismatch, and no official SOAP parity claim.",
    )

    assert result["status"] == "consistent"
    assert result["candidate"]["status"] == "mismatch"
    assert result["candidate"]["substatus"] == "diagnostic_only_source_contract_mismatch"


def test_real_task_answer_normalization_fails_closed_on_missing_anchors() -> None:
    result = normalize_real_task_answer(
        "MF-03-hmc-helper-nonclaim-boundary",
        "This discusses diagnostics but does not say enough to be safe.",
    )

    assert result["status"] == "inconclusive"
    assert result["candidate"] is None
    assert result["diagnostics"]["missing_anchors"]


def test_real_task_answer_normalization_preserves_forbidden_claims_for_scoring() -> None:
    result = normalize_real_task_answer(
        "MF-03-hmc-helper-nonclaim-boundary",
        "These are numerical-stability helpers around the mass-matrix and ESS / R-hat diagnostics, not structural-identification tests. These tests validate the posterior.",
    )

    assert result["status"] == "consistent"
    assert "These tests validate the posterior." in result["candidate"]["claims"]


def test_real_task_answer_normalization_composes_with_scoring_for_safe_mf03_answer() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    normalized = normalize_real_task_answer(
        case["id"],
        "These are numerical-stability helpers around the mass-matrix and ESS / R-hat diagnostics, not structural-identification tests.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert score["status"] == "consistent"


def test_real_task_answer_normalization_composes_with_scoring_for_overclaiming_mf03_answer() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    normalized = normalize_real_task_answer(
        case["id"],
        "These are numerical-stability helpers around the mass-matrix and ESS / R-hat diagnostics, not structural-identification tests. These tests validate the posterior.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert score["status"] == "mismatch"


def test_real_task_answer_normalization_composes_with_scoring_for_safe_mf04_answer() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "MF-04-short-hmc-acceptance-veto-diagnosis")
    normalized = normalize_real_task_answer(
        case["id"],
        "Classification: inconclusive. The acceptance-veto diagnosis requires trusted same-process GPU execution, trusted_execution_provenance_passed was False, and downstream launch remains not authorized. fix the diagnostic blocker or revise under Claude/Codex review.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert score["status"] == "consistent"


def test_real_task_answer_normalization_composes_with_scoring_for_safe_dh06_answer() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "DH-06-densesoap-source-contract-mismatch")
    normalized = normalize_real_task_answer(
        case["id"],
        "DENSESOAP_REMAINS_DIAGNOSTIC_ONLY. The TensorFlow DenseSOAP surfaces remain diagnostic only because there is a material default mismatch, a missing official feature, a step/cadence mismatch, and no official SOAP parity claim. Keep both TensorFlow DenseSOAP surfaces diagnostic-only unless a new bounded optimizer plan is approved.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert score["status"] == "consistent"


def test_real_task_answer_normalization_records_exact_rejected_forbidden_claim_for_mf04() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "MF-04-short-hmc-acceptance-veto-diagnosis")
    normalized = normalize_real_task_answer(
        case["id"],
        "Classification: inconclusive. The acceptance-veto diagnosis requires trusted same-process GPU execution, trusted_execution_provenance_passed was False, and downstream launch remains not authorized. Rejected claim: short HMC pilot gate closure: authorized. fix the diagnostic blocker or revise under Claude/Codex review.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert normalized["candidate"]["claims"] == []
    assert normalized["candidate"]["rejected_claims"] == ["short HMC pilot gate closure: authorized"]
    assert score["status"] == "consistent"
    assert score["details"]["rejected_forbidden_claims"] == ["short HMC pilot gate closure: authorized"]


def test_real_task_answer_normalization_keeps_unqualified_forbidden_claim_asserted_for_mf04() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "MF-04-short-hmc-acceptance-veto-diagnosis")
    normalized = normalize_real_task_answer(
        case["id"],
        "Classification: inconclusive. The acceptance-veto diagnosis requires trusted same-process GPU execution, trusted_execution_provenance_passed was False, and downstream launch remains not authorized. short HMC pilot gate closure: authorized. fix the diagnostic blocker or revise under Claude/Codex review.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert normalized["candidate"]["claims"] == ["short HMC pilot gate closure: authorized"]
    assert normalized["candidate"]["rejected_claims"] == []
    assert score["status"] == "mismatch"


def test_real_task_answer_normalization_records_exact_rejected_forbidden_claim_for_dh06() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(case for case in manifest["cases"] if case["id"] == "DH-06-densesoap-source-contract-mismatch")
    normalized = normalize_real_task_answer(
        case["id"],
        "DENSESOAP_REMAINS_DIAGNOSTIC_ONLY. The TensorFlow DenseSOAP surfaces remain diagnostic only because there is a material default mismatch, a missing official feature, a step/cadence mismatch, and no official SOAP parity claim. It does not claim that official SOAP parity is established. Keep both TensorFlow DenseSOAP surfaces diagnostic-only unless a new bounded optimizer plan is approved.",
    )

    score = score_real_task_case(case, normalized["candidate"])

    assert normalized["candidate"]["claims"] == []
    assert normalized["candidate"]["rejected_claims"] == ["official SOAP parity is established"]
    assert score["status"] == "consistent"
    assert score["details"]["rejected_forbidden_claims"] == ["official SOAP parity is established"]
