import json
from pathlib import Path

from mathdevmcp.real_tasks_report import real_task_public_report


ROOT = Path(__file__).resolve().parent.parent


def _valid_case_dict() -> dict:
    return {
        "id": "CASE-001",
        "family": "evidence_boundary_discipline",
        "repo": "ExampleRepo",
        "task_type": "example_audit",
        "difficulty": "easy",
        "public": True,
        "document_roots": ["benchmarks/real_tasks"],
        "document_files": ["benchmarks/real_tasks/README.md"],
        "code_roots": ["src"],
        "code_files": ["src/mathdevmcp/contracts.py"],
        "labels": ["example:label"],
        "prompt": "Summarize the benchmark case.",
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
        "notes": "Example notes.",
    }


def test_real_task_public_report_returns_valid_contract() -> None:
    report = real_task_public_report(ROOT)

    assert report["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_public_report",
    }
    assert report["status"] == "consistent"


def test_real_task_public_report_summarizes_committed_manifest() -> None:
    report = real_task_public_report(ROOT)

    assert report["manifest_status"] == "consistent"
    assert report["validation_status"] == "consistent"
    assert report["public_case_total"] == 12
    assert report["summary"]["false_confidence_veto_cases"] == 12


def test_real_task_public_report_counts_cases_by_family() -> None:
    report = real_task_public_report(ROOT)

    assert report["summary"]["by_family"] == {
        "numerical_oracle_parity": 2,
        "evidence_boundary_discipline": 5,
        "code_document_consistency": 3,
        "retrieval_and_provenance": 1,
        "derivation_boundary_and_abstention": 1,
    }


def test_real_task_public_report_counts_cases_by_repo() -> None:
    report = real_task_public_report(ROOT)

    assert report["summary"]["by_repo"] == {
        "MacroFinance": 3,
        "dsge_hmc": 6,
        "latex-papers": 2,
        "MacroFinance/ResearchAssistant": 1,
    }


def test_real_task_public_report_counts_cases_by_difficulty() -> None:
    report = real_task_public_report(ROOT)

    assert report["summary"]["by_difficulty"] == {
        "medium": 5,
        "easy": 2,
        "hard": 5,
    }


def test_real_task_public_report_counts_cases_by_expected_status() -> None:
    report = real_task_public_report(ROOT)

    assert report["summary"]["by_expected_status"] == {
        "unverified": 2,
        "consistent": 6,
        "inconclusive": 1,
        "mismatch": 3,
    }


def test_real_task_public_report_surfaces_manifest_validation_findings(tmp_path: Path) -> None:
    case = _valid_case_dict()
    case["document_files"] = [str(ROOT / "benchmarks" / "real_tasks" / "README.md")]
    manifest_path = tmp_path / "public_cases.json"
    manifest_path.write_text(
        json.dumps({
            "metadata": {
                "schema_version": "1.0",
                "contract": "real_task_public_case_manifest",
            },
            "cases": [case],
        }),
        encoding="utf-8",
    )

    report = real_task_public_report(ROOT, manifest_path=manifest_path)

    assert report["status"] == "mismatch"
    assert any(finding["kind"] == "absolute_path_not_allowed" for finding in report["findings"])
    assert report["warnings"]


def test_real_task_public_report_includes_non_gating_policy_note() -> None:
    report = real_task_public_report(ROOT)
    text = " ".join(report["policy_boundary"])

    assert "not benchmark execution evidence" in text
    assert "not holdout-local or private-external evaluation evidence" in text
    assert "not release-readiness evidence" in text
    assert "No pass/fail gate is implied" in text
