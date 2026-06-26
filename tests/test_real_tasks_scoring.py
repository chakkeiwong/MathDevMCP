from pathlib import Path

from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest
from mathdevmcp.real_tasks_scoring import score_real_task_case


ROOT = Path(__file__).resolve().parent.parent


def _candidate(
    *,
    case_id: str = "CASE-001",
    status: str | None = "consistent",
    substatus: str | None = "example",
    labels: list[str] | None = None,
    evidence_class: str | None = "example_evidence",
    summary_text: str = "example term",
    claims: list[str] | None = None,
    next_actions: list[str] | None = None,
) -> dict:
    return {
        "case_id": case_id,
        "status": status,
        "substatus": substatus,
        "labels": labels or ["example:label"],
        "evidence_class": evidence_class,
        "summary_text": summary_text,
        "claims": claims or ["safe example claim"],
        "next_actions": next_actions or ["take next step"],
    }


def _case() -> dict:
    return {
        "id": "CASE-001",
        "gold": {
            "expected_status": "consistent",
            "expected_substatus": "example",
            "expected_labels": ["example:label"],
            "required_terms": ["example term"],
            "forbidden_claims": ["forbidden example"],
            "required_next_actions": ["take next step"],
            "evidence_class": "example_evidence",
            "false_confidence_veto": True,
        },
    }


def test_real_task_case_structural_score_passes_matching_candidate() -> None:
    result = score_real_task_case(_case(), _candidate())

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_case_structural_score",
    }
    assert result["status"] == "consistent"
    assert all(result["quality_checks"].values())


def test_real_task_case_structural_score_reports_missing_required_terms() -> None:
    result = score_real_task_case(_case(), _candidate(summary_text="different text"))

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["required_terms_present"] is False
    assert result["details"]["missing_required_terms"] == ["example term"]


def test_real_task_case_structural_score_reports_forbidden_claim_hit() -> None:
    result = score_real_task_case(_case(), _candidate(claims=["forbidden example"]))

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["forbidden_claims_absent"] is False
    assert result["details"]["present_forbidden_claims"] == ["forbidden example"]


def test_real_task_case_structural_score_enforces_false_confidence_veto() -> None:
    result = score_real_task_case(_case(), _candidate(claims=["forbidden example"]))

    assert result["quality_checks"]["false_confidence_veto_clear"] is False
    assert result["status"] == "mismatch"


def test_real_task_case_structural_score_reports_label_mismatch() -> None:
    result = score_real_task_case(_case(), _candidate(labels=["wrong:label"]))

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["expected_labels_present"] is False
    assert result["details"]["missing_expected_labels"] == ["example:label"]


def test_real_task_case_structural_score_reports_next_action_mismatch() -> None:
    result = score_real_task_case(_case(), _candidate(next_actions=["different action"]))

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["required_next_actions_present"] is False
    assert result["details"]["missing_required_next_actions"] == ["take next step"]


def test_real_task_case_structural_score_returns_inconclusive_for_malformed_candidate() -> None:
    result = score_real_task_case(_case(), {"case_id": "CASE-001"})

    assert result["status"] == "inconclusive"
    assert result["quality_checks"]["expected_status_match"] is False


def test_real_task_case_structural_score_handles_committed_manifest_strings() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    lp_case = next(case for case in manifest["cases"] if case["id"] == "LP-01-analytical-validation-lgssm")
    candidate = {
        "case_id": lp_case["id"],
        "status": "consistent",
        "substatus": "analytical_test_spec_recovered",
        "labels": ["eq:av_lgssm_trans", "eq:av_lgssm_obs", "prop:av_edh_kf", "rem:av_lgssm_test"],
        "evidence_class": "analytical_gold_standard",
        "summary_text": "linear-Gaussian state-space model Kalman filter EDH recovers the Kalman filter N in {50, 100, 500, 1000} error below 10^-2 for N = 1000",
        "claims": ["safe calibration summary"],
        "next_actions": ["Use the practical test specification as a gold-standard benchmark case."],
    }

    result = score_real_task_case(lp_case, candidate)

    assert result["status"] == "consistent"
    assert result["quality_checks"]["required_terms_present"] is True


def test_real_task_case_structural_score_handles_committed_manifest_threshold_terms() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    dh_case = next(case for case in manifest["cases"] if case["id"] == "DH-01-strict-nk-convergence-audit")
    candidate = {
        "case_id": dh_case["id"],
        "status": "consistent",
        "substatus": "strict_convergence_thresholds_recovered",
        "labels": [],
        "evidence_class": "statistical_convergence_audit",
        "summary_text": "R-hat < 1.01 ESS_bulk > 400 MCSE/SD < 10% medium/overnight diagnostics not routine local smoke validation",
        "claims": ["safe convergence audit summary"],
        "next_actions": ["Use the declared thresholds as the audit contract for this case."],
    }

    result = score_real_task_case(dh_case, candidate)

    assert result["status"] == "consistent"
    assert result["quality_checks"]["required_terms_present"] is True


def test_real_task_case_structural_score_handles_committed_manifest_mismatch_case() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    soap_case = next(case for case in manifest["cases"] if case["id"] == "DH-06-densesoap-source-contract-mismatch")
    candidate = {
        "case_id": soap_case["id"],
        "status": "mismatch",
        "substatus": "diagnostic_only_source_contract_mismatch",
        "labels": [],
        "evidence_class": "diagnostic_source_contract_mismatch",
        "summary_text": "DENSESOAP_REMAINS_DIAGNOSTIC_ONLY material default mismatch missing official feature step/cadence mismatch no official SOAP parity claim",
        "claims": ["official SOAP parity is established"],
        "next_actions": ["Keep both TensorFlow DenseSOAP surfaces diagnostic-only unless a new bounded optimizer plan is approved."],
    }

    result = score_real_task_case(soap_case, candidate)

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["forbidden_claims_absent"] is False


def test_real_task_case_structural_score_handles_committed_manifest_inconclusive_case() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    mf_case = next(case for case in manifest["cases"] if case["id"] == "MF-04-short-hmc-acceptance-veto-diagnosis")
    candidate = {
        "case_id": mf_case["id"],
        "status": "inconclusive",
        "substatus": "trusted_gpu_provenance_blocked",
        "labels": [],
        "evidence_class": "diagnostic_blocked_execution_note",
        "summary_text": "Classification: inconclusive acceptance-veto diagnosis requires trusted same-process GPU execution trusted_execution_provenance_passed False not authorized",
        "claims": ["short HMC pilot gate closure: authorized"],
        "next_actions": ["fix the diagnostic blocker or revise under Claude/Codex review"],
    }

    result = score_real_task_case(mf_case, candidate)

    assert result["status"] == "mismatch"
    assert result["quality_checks"]["forbidden_claims_absent"] is False
