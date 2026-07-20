import json
from pathlib import Path

from mathdevmcp.real_tasks_manifest import (
    load_real_task_public_manifest,
    validate_real_task_public_manifest,
)


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "benchmarks" / "real_tasks" / "manifests" / "public_cases.json"


def _valid_case_dict() -> dict:
    return {
        "id": "CASE-001",
        "family": "evidence_boundary_discipline",
        "repo": "MathDevMCP",
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


def test_real_task_public_manifest_loads_valid_contract() -> None:
    manifest = load_real_task_public_manifest(ROOT)

    assert manifest["status"] == "consistent"
    assert manifest["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_public_case_manifest",
    }
    assert manifest["manifest_metadata"]["contract"] == "real_task_public_case_manifest"
    assert len(manifest["cases"]) == 12


def test_real_task_public_manifest_validator_accepts_committed_manifest() -> None:
    validation = validate_real_task_public_manifest(ROOT)

    assert validation["status"] == "consistent"
    assert validation["metadata"] == {
        "schema_version": "1.0",
        "contract": "real_task_public_case_validation_report",
    }
    assert validation["findings"] == []


def test_real_task_public_manifest_case_ids_are_unique() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    ids = [case["id"] for case in manifest["cases"]]

    assert len(ids) == len(set(ids))


def test_real_task_public_manifest_preserves_expected_semantics_for_representative_cases() -> None:
    manifest = load_real_task_public_manifest(ROOT)
    by_id = {case["id"]: case for case in manifest["cases"]}

    assert by_id["MF-02-large-scale-lgssm-missing-data-policy"]["gold"]["expected_status"] == "unverified"
    assert by_id["MF-04-short-hmc-acceptance-veto-diagnosis"]["gold"]["expected_status"] == "inconclusive"
    assert by_id["DH-06-densesoap-source-contract-mismatch"]["gold"]["expected_status"] == "mismatch"
    assert "current_neutra_runner_migrated" in by_id["DH-07-neutra-real-nk-migration-not-complete"]["gold"]["required_terms"]
    assert "value_score_authority == unavailable" in by_id["DH-02-bayesfilter-qr-value-parity"]["gold"]["required_terms"]
    assert "error below 10^-2 for N = 1000" in by_id["LP-01-analytical-validation-lgssm"]["gold"]["required_terms"]


def test_real_task_public_manifest_paths_are_relative_and_resolve() -> None:
    manifest = load_real_task_public_manifest(ROOT)

    for case in manifest["cases"]:
        for field in ("document_roots", "document_files", "code_roots", "code_files"):
            for raw_path in case[field]:
                path_obj = Path(raw_path)
                assert not path_obj.is_absolute()
                assert (ROOT / raw_path).exists(), (case["id"], field, raw_path)


def test_real_task_public_manifest_rejects_absolute_paths(tmp_path: Path) -> None:
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

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "absolute_path_not_allowed" for finding in validation["findings"])


def test_real_task_public_manifest_rejects_missing_referenced_files(tmp_path: Path) -> None:
    case = _valid_case_dict()
    case["code_files"] = ["src/mathdevmcp/does_not_exist.py"]
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

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "referenced_path_missing" for finding in validation["findings"])


def test_real_task_public_manifest_rejects_arbitrary_existing_escape(tmp_path: Path) -> None:
    case = _valid_case_dict()
    outside = tmp_path.parent / "manifest_escape_probe.py"
    outside.write_text("# probe\n", encoding="utf-8")
    import os

    case["document_files"] = [os.path.relpath(outside, ROOT)]
    manifest_path = tmp_path / "public_cases.json"
    manifest_path.write_text(json.dumps({"metadata": {"schema_version": "1.0", "contract": "real_task_public_case_manifest"}, "cases": [case]}), encoding="utf-8")
    try:
        validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)
    finally:
        outside.unlink()
    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "referenced_path_escapes_declared_repo" for finding in validation["findings"])


def test_real_task_public_manifest_rejects_path_like_repository_identifier(tmp_path: Path) -> None:
    case = _valid_case_dict()
    case["repo"] = ".."
    case["document_files"] = ["../DynareMCP/README.md"]
    manifest_path = tmp_path / "public_cases.json"
    manifest_path.write_text(json.dumps({
        "metadata": {"schema_version": "1.0", "contract": "real_task_public_case_manifest"},
        "cases": [case],
    }), encoding="utf-8")

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "unsupported_repository_identifier" for finding in validation["findings"])


def test_real_task_public_manifest_requires_gold_fields(tmp_path: Path) -> None:
    case = _valid_case_dict()
    del case["gold"]["required_terms"]
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

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "inconclusive"
    assert validation["manifest"]["status"] == "inconclusive"
    assert any(finding["kind"] == "real_task_case_invalid" for finding in validation["findings"])


def test_real_task_public_manifest_requires_list_of_strings_fields(tmp_path: Path) -> None:
    case = _valid_case_dict()
    case["gold"]["required_terms"] = "not-a-list"
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

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "inconclusive"
    assert any(finding["kind"] == "real_task_case_invalid" for finding in validation["findings"])


def test_real_task_public_manifest_rejects_duplicate_case_ids(tmp_path: Path) -> None:
    case_a = _valid_case_dict()
    case_b = _valid_case_dict()
    manifest_path = tmp_path / "public_cases.json"
    manifest_path.write_text(
        json.dumps({
            "metadata": {
                "schema_version": "1.0",
                "contract": "real_task_public_case_manifest",
            },
            "cases": [case_a, case_b],
        }),
        encoding="utf-8",
    )

    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "duplicate_case_id" for finding in validation["findings"])


def test_real_task_public_manifest_rejects_malformed_cases_payload(tmp_path: Path) -> None:
    manifest_path = tmp_path / "public_cases.json"
    manifest_path.write_text(
        json.dumps({
            "metadata": {
                "schema_version": "1.0",
                "contract": "real_task_public_case_manifest",
            },
            "cases": {"bad": "shape"},
        }),
        encoding="utf-8",
    )

    manifest = load_real_task_public_manifest(ROOT, manifest_path=manifest_path)
    validation = validate_real_task_public_manifest(ROOT, manifest_path=manifest_path)

    assert manifest["status"] == "inconclusive"
    assert validation["status"] == "inconclusive"
    assert any(finding["kind"] == "manifest_cases_not_list" for finding in validation["findings"])
