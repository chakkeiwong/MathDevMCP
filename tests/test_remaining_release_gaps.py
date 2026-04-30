import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from mathdevmcp.leandojo_backend import attempt_leandojo_tiny_theorem
from mathdevmcp.parser_benchmark import run_parser_backend
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label
from mathdevmcp.release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from mathdevmcp.release_evidence import release_evidence_metadata


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"
LEANDOJO_FIXTURE = ROOT / "tests" / "fixtures" / "leandojo_tiny_project"


def test_leandojo_fixture_files_are_pinned_and_directly_checkable(requires_lean):
    assert (LEANDOJO_FIXTURE / "lean-toolchain").read_text(encoding="utf-8").strip() == "leanprover/lean4:v4.20.0"
    assert (LEANDOJO_FIXTURE / "lakefile.lean").exists()
    source = (LEANDOJO_FIXTURE / "MathDevMCPDemo.lean").read_text(encoding="utf-8")

    result = attempt_leandojo_tiny_theorem(
        traced_repo_path=str(LEANDOJO_FIXTURE),
        theorem_name="mathdevmcp_tiny_true",
        lean_source=source,
        tactic_script=["exact Nat.add_comm a b"],
        run_dojo=False,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "leandojo_attempt_result"}
    assert result["status"] == "inconclusive"
    assert result["readiness"]["fixture_available"] is True
    if result["final_lean_check"] is not None:
        assert result["final_lean_check"]["status"] == "verified"
    assert result["readiness"]["dojo_entered"] is False


def test_leandojo_false_candidate_never_verifies_without_final_certificate(requires_lean):
    source = (LEANDOJO_FIXTURE / "MathDevMCPFalseCandidate.lean").read_text(encoding="utf-8")

    result = attempt_leandojo_tiny_theorem(
        traced_repo_path=str(LEANDOJO_FIXTURE),
        theorem_name="mathdevmcp_tiny_false_candidate",
        lean_source=source,
        tactic_script=["exact Nat.add_comm a b"],
        run_dojo=False,
    )

    assert result["status"] == "mismatch"
    assert result["readiness"]["final_lean_check_passed"] is False
    assert result["final_lean_check"]["status"] == "mismatch"


def test_leandojo_real_dojo_integration_is_opt_in():
    if os.environ.get("MATHDEVMCP_RUN_LEANDOJO_INTEGRATION") != "1":
        pytest.skip("real LeanDojo integration is opt-in")
    source = (LEANDOJO_FIXTURE / "MathDevMCPDemo.lean").read_text(encoding="utf-8")
    result = attempt_leandojo_tiny_theorem(
        traced_repo_path=str(LEANDOJO_FIXTURE),
        theorem_name="mathdevmcp_tiny_true",
        lean_source=source,
        tactic_script=["exact Nat.add_comm a b"],
        run_dojo=True,
        timeout_seconds=30,
    )

    assert result["status"] in {"verified", "inconclusive"}
    if result["status"] == "verified":
        assert result["readiness"]["dojo_entered"] is True
        assert result["readiness"]["final_lean_check_passed"] is True


def test_latexml_validation_script_reports_optional_unavailable(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")
    result = subprocess.run(
        [str(ROOT / "scripts" / "validate_latexml_backend.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "latexml_backend_validation"}
    assert payload["status"] == "unavailable"
    assert "MATHDEVMCP_LATEXML_PATH" in payload["install_hint"]


def test_latexml_validation_strict_mode_fails_when_unavailable(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")
    result = subprocess.run(
        [str(ROOT / "scripts" / "validate_latexml_backend.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "MATHDEVMCP_REQUIRE_LATEXML": "1"},
    )

    assert result.returncode == 1
    assert '"status": "unavailable"' in result.stdout


def test_clean_install_smoke_help_documents_backend_and_artifacts():
    result = subprocess.run(
        [str(ROOT / "scripts" / "clean_install_smoke.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "MATHDEVMCP_INSTALL_BACKENDS=1" in result.stdout
    assert "MATHDEVMCP_CLEAN_ARTIFACT_DIR" in result.stdout
    assert "MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY=1" in result.stdout


def test_backend_command_runner_help_documents_isolated_env():
    result = subprocess.run(
        [str(ROOT / "scripts" / "run_backend_command.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "mathdevmcp-backends" in result.stdout
    assert "MATHDEVMCP_LEAN_TOOLCHAIN" in result.stdout
    assert "conda" in (ROOT / "scripts" / "run_backend_command.sh").read_text(encoding="utf-8")


def test_latexml_setup_help_documents_strict_profile():
    result = subprocess.run(
        [str(ROOT / "scripts" / "setup_latexml_backend.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "MATHDEVMCP_REQUIRE_LATEXML=1" in result.stdout


def _private_entry(path: Path) -> dict:
    return {
        "id": "private_dsge_local",
        "domain": "dsge_macro_finance",
        "privacy_class": "private_external",
        "document_root": str(path),
        "code_roots": [str(path / "code")],
        "expected_labels": ["eq:private-euler-equation"],
        "expected_operations": ["expectation"],
        "expected_abstentions": ["calibration_review"],
        "seeded_false_confidence_cases": [],
        "required_parser_backends": ["current"],
        "release_gate_enabled": True,
        "notes": "Local private fixture path for tests.",
    }


def test_private_corpus_manifest_loads_and_redacts_paths(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    (private_root / "code").mkdir()
    manifest_path = tmp_path / "corpus.json"
    manifest_path.write_text(json.dumps({"entries": [_private_entry(private_root)]}), encoding="utf-8")

    manifest = release_corpus_manifest(FIXTURES, private_manifest=manifest_path)
    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)
    private = next(entry for entry in manifest["entries"] if entry["id"] == "private_dsge_local")

    assert manifest["private_manifest"]["status"] == "loaded"
    assert private["document_root"] is None
    assert private["code_roots"] == ["<redacted-private-path>"]
    assert validation["status"] == "consistent"


def test_private_corpus_manifest_accepts_raw_entry_list(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    (private_root / "code").mkdir()
    manifest_path = tmp_path / "corpus-list.json"
    manifest_path.write_text(json.dumps([_private_entry(private_root)]), encoding="utf-8")

    manifest = release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert manifest["private_manifest"]["status"] == "loaded"
    assert any(entry["id"] == "private_dsge_local" for entry in manifest["entries"])


def test_private_corpus_validation_rejects_checkout_paths(tmp_path):
    manifest_path = tmp_path / "corpus.json"
    manifest_path.write_text(json.dumps({"entries": [_private_entry(ROOT / "benchmarks" / "fixtures")]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "private_path_inside_checkout" for finding in validation["findings"])


def test_private_corpus_validation_rejects_missing_private_root(tmp_path):
    manifest_path = tmp_path / "corpus.json"
    manifest_path.write_text(json.dumps({"entries": [_private_entry(tmp_path / "missing-private")]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "private_document_root_missing" for finding in validation["findings"])


def test_private_corpus_validation_rejects_malformed_entry_types(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    manifest_path = tmp_path / "corpus.json"
    entry = _private_entry(private_root)
    entry["expected_labels"] = "eq:private-euler-equation"
    manifest_path.write_text(json.dumps({"entries": [entry]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert validation["manifest"]["private_manifest"]["status"] == "invalid_entries"
    assert any(finding["kind"] == "private_manifest_entry_invalid" for finding in validation["findings"])


def test_private_corpus_validation_rejects_missing_code_root(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    manifest_path = tmp_path / "corpus.json"
    entry = _private_entry(private_root)
    entry["code_roots"] = [str(tmp_path / "missing-code-root")]
    manifest_path.write_text(json.dumps({"entries": [entry]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "private_path_missing" for finding in validation["findings"])


def test_private_corpus_validation_rejects_missing_parser_backends(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    manifest_path = tmp_path / "corpus.json"
    entry = _private_entry(private_root)
    entry["required_parser_backends"] = []
    manifest_path.write_text(json.dumps({"entries": [entry]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "missing_required_parser_backends" for finding in validation["findings"])


def test_private_corpus_validation_rejects_unsupported_privacy_class(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    (private_root / "code").mkdir()
    manifest_path = tmp_path / "corpus.json"
    entry = _private_entry(private_root)
    entry["privacy_class"] = "private_unreviewed"
    manifest_path.write_text(json.dumps({"entries": [entry]}), encoding="utf-8")

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest_path)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "unsupported_privacy_class" for finding in validation["findings"])


def test_parser_benchmark_reports_environment_counts_and_scanned_files():
    result = run_parser_backend(FIXTURES, "current")

    assert result["details"]["environment_type_counts"]["equation"] >= 1
    assert "doc_macro_filter_main.tex" in result["details"]["tex_files_scanned"]
    assert result["details"]["per_file_metrics"]["doc_macro_filter_main.tex"]["include_targets"] == ["doc_macro_filter_model"]
    assert result["details"]["include_status"]["resolved"]
    assert result["details"]["macro_summary"]["total_macro_definitions"] >= 1
    assert isinstance(result["details"]["duplicate_label_findings"], list)
    assert result["details"]["section_path_quality"] == "available"
    assert result["details"]["macro_visibility"] == "textual"


def test_proof_audit_v2_marks_diagnostic_boundary_for_non_certificates():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:dept-state-space-likelihood")
    obligation = result["obligations"][0]

    assert obligation["status"] != "verified"
    assert obligation["diagnostic_only"] is True
    assert obligation["certificate"] is None
    assert "deterministic backend certificate" in obligation["verification_boundary"]


def test_proof_audit_v2_verified_obligation_carries_certificate_boundary():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:proof-audit-single")
    obligation = result["obligations"][0]

    assert obligation["status"] == "verified"
    assert obligation["diagnostic_only"] is False
    assert obligation["certificate"] is not None
    assert obligation["evidence_kind"] == "deterministic_backend"


def test_release_evidence_script_help_and_metadata(tmp_path):
    help_result = subprocess.run(
        [str(ROOT / "scripts" / "collect_release_evidence.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    metadata = release_evidence_metadata(ROOT, output_dir=tmp_path, command_line=["collect_release_evidence.sh", str(tmp_path)])

    assert help_result.returncode == 0
    assert "doctor-base.json" not in help_result.stderr
    assert "OUTPUT_DIR" in help_result.stdout
    assert "--profile" in help_result.stdout
    assert metadata["metadata"] == {"schema_version": "1.0", "contract": "release_evidence_metadata"}
    assert metadata["private_paths_redacted"] is True
    assert metadata["git_commit"]


def test_release_evidence_script_rejects_checkout_root():
    result = subprocess.run(
        [str(ROOT / "scripts" / "collect_release_evidence.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "Refusing unsafe release evidence output directory" in result.stderr


def test_release_matrix_help_documents_optional_profiles():
    result = subprocess.run(
        [str(ROOT / "scripts" / "release_matrix.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Optional profiles" in result.stdout
