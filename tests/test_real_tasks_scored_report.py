from pathlib import Path

from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest
from mathdevmcp.real_tasks_scored_report import score_real_task_public_candidates


ROOT = Path(__file__).resolve().parent.parent


def test_real_task_structural_score_report_returns_valid_contract() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(c for c in manifest["cases"] if c["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    report = score_real_task_public_candidates(
        [
            {
                "case_id": case["id"],
                "status": "consistent",
                "substatus": "helper_nonclaim_boundary_preserved",
                "labels": [],
                "evidence_class": "engineering_helper_regression",
                "summary_text": "numerical-stability helpers mass-matrix ESS R-hat not structural-identification tests",
                "claims": ["safe helper summary"],
                "next_actions": ["Use separate model-level diagnostics for identification or posterior claims."],
            }
        ],
        root=ROOT,
    )

    assert report["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_structural_score_report",
    }
    assert report["summary"]["scored_candidate_total"] == 1


def test_real_task_structural_score_report_aggregates_statuses_and_families() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    mf_case = next(c for c in manifest["cases"] if c["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    lp_case = next(c for c in manifest["cases"] if c["id"] == "LP-02-basis-reconciliation-audit")
    report = score_real_task_public_candidates(
        [
            {
                "case_id": mf_case["id"],
                "status": "consistent",
                "substatus": "helper_nonclaim_boundary_preserved",
                "labels": [],
                "evidence_class": "engineering_helper_regression",
                "summary_text": "numerical-stability helpers mass-matrix ESS R-hat not structural-identification tests",
                "claims": ["safe helper summary"],
                "next_actions": ["Use separate model-level diagnostics for identification or posterior claims."],
            },
            {
                "case_id": lp_case["id"],
                "status": "consistent",
                "substatus": "multi_location_sign_reconciliation_needed",
                "labels": [],
                "evidence_class": "document_reconciliation_plan",
                "summary_text": "market convention model convention x_t = -x_market six locations symbol drift sign reversal",
                "claims": ["The monograph is already fully reconciled."],
                "next_actions": ["Treat the document as a reconciliation task rather than a settled single-source definition.", "Audit downstream chapter references against the proposed master reconciliation section."],
            },
        ],
        root=ROOT,
    )

    assert report["summary"]["by_status"] == {"consistent": 1, "mismatch": 1}
    assert report["summary"]["by_case_family"]["evidence_boundary_discipline"]["consistent"] == 1
    assert report["summary"]["by_case_family"]["derivation_boundary_and_abstention"]["mismatch"] == 1


def test_real_task_structural_score_report_counts_false_confidence_veto_failures() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(c for c in manifest["cases"] if c["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    report = score_real_task_public_candidates(
        [
            {
                "case_id": case["id"],
                "status": "consistent",
                "substatus": "helper_nonclaim_boundary_preserved",
                "labels": [],
                "evidence_class": "engineering_helper_regression",
                "summary_text": "numerical-stability helpers mass-matrix ESS R-hat not structural-identification tests",
                "claims": ["These tests validate the posterior."],
                "next_actions": ["Use separate model-level diagnostics for identification or posterior claims."],
            }
        ],
        root=ROOT,
    )

    assert report["summary"]["false_confidence_veto_failures"] == 1


def test_real_task_structural_score_report_surfaces_missing_candidate_cases() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    case = next(c for c in manifest["cases"] if c["id"] == "MF-03-hmc-helper-nonclaim-boundary")
    report = score_real_task_public_candidates(
        [
            {
                "case_id": case["id"],
                "status": "consistent",
                "substatus": "helper_nonclaim_boundary_preserved",
                "labels": [],
                "evidence_class": "engineering_helper_regression",
                "summary_text": "numerical-stability helpers mass-matrix ESS R-hat not structural-identification tests",
                "claims": ["safe helper summary"],
                "next_actions": ["Use separate model-level diagnostics for identification or posterior claims."],
            }
        ],
        root=ROOT,
    )

    assert report["summary"]["missing_candidate_case_ids"]
    assert report["warnings"]


def test_real_task_structural_score_report_includes_non_gating_policy_boundary() -> None:
    report = score_real_task_public_candidates([], root=ROOT)
    text = " ".join(report["policy_boundary"])

    assert "non-gating scored report" in text
    assert "not semantic benchmark execution over free-form model outputs" in text
    assert "not release-readiness evidence" in text
