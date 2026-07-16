from pathlib import Path
import subprocess
import sys

from mathdevmcp.governance import scan_subprocess_timeout_policy, validate_governance
from mathdevmcp.release_policy import release_readiness_report


ROOT = Path(__file__).resolve().parent.parent


def test_backend_environment_spec_pins_leandojo_without_latexml():
    spec = (ROOT / "environment-backends.yml").read_text(encoding="utf-8")

    assert "name: mathdevmcp-backends" in spec
    assert "python=3.11" in spec
    assert "\n  - pip\n" in spec
    assert "sympy=1.14" in spec
    assert "lean-dojo==4.20.0" in spec
    assert "latexml" not in spec


def test_backend_install_scripts_expose_release_candidate_controls():
    setup = (ROOT / "scripts" / "setup_backend_env.sh").read_text(encoding="utf-8")
    validate = (ROOT / "scripts" / "validate_backend_install.sh").read_text(encoding="utf-8")

    assert "environment-backends.yml" in setup
    assert "MATHDEVMCP_BACKEND_CONDA_ENV" in setup
    assert "MATHDEVMCP_LEAN_TOOLCHAIN" in setup
    assert "MATHDEVMCP_LATEXML_PATH" in setup
    assert "backend_env_doctor.sh" in setup
    assert "toolchain already installed" in setup
    assert "toolchain list" in setup
    assert "elan\" default" not in setup
    assert "Optional backend caveats" in validate
    assert "latexml" in validate
    assert (ROOT / "scripts" / "validate_latexml_backend.sh").exists()
    assert (ROOT / "scripts" / "setup_latexml_backend.sh").exists()
    assert (ROOT / "scripts" / "run_backend_command.sh").exists()
    assert 'required = ["pandoc", "lean", "sage", "lean_dojo"]' in validate
    assert 'optional = ["latexml", "sympy"]' in validate


def test_clean_install_smoke_help_is_lightweight():
    result = subprocess.run(
        [str(ROOT / "scripts" / "clean_install_smoke.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "MATHDEVMCP_INSTALL_BACKENDS=1" in result.stdout
    assert "MATHDEVMCP_CLEAN_ARTIFACT_DIR" in result.stdout
    assert "TARGET_DIR" in result.stdout


def test_clean_install_smoke_copies_dirty_non_ignored_checkout():
    script = (ROOT / "scripts" / "clean_install_smoke.sh").read_text(encoding="utf-8")

    assert "git -C \"$ROOT\" status --short" in script
    assert "git -C \"$ROOT\" ls-files -z --cached --others --exclude-standard" in script
    assert "copying current non-ignored checkout" in script


def test_release_readiness_records_latexml_optional_caveat_when_unavailable(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")

    report = release_readiness_report(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert any(caveat["kind"] == "latexml_optional_backend_unavailable" for caveat in report["caveats"])
    assert not any(blocker["kind"] == "latexml_missing" for blocker in report["blockers"])


def test_validate_governance_surfaces_contract_and_policy():
    result = validate_governance(ROOT)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "governance_validation_report"}
    assert result["status"] == "consistent"
    assert result["policy"]["metadata"]["contract"] == "governance_policy"
    assert result["release_corpus_validation"]["metadata"]["contract"] == "release_corpus_validation_report"
    assert result["subprocess_timeout_validation"]["metadata"]["contract"] == "subprocess_timeout_policy_report"


def test_subprocess_timeout_scan_covers_source_calls():
    result = scan_subprocess_timeout_policy(ROOT)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "subprocess_timeout_policy_report"}
    assert result["status"] == "consistent"
    assert result["findings"] == []


def test_subprocess_timeout_scan_rejects_unbounded_popen(tmp_path: Path) -> None:
    package = tmp_path / "src" / "mathdevmcp"
    package.mkdir(parents=True)
    (package / "bad.py").write_text(
        "import subprocess\n\ndef run():\n    return subprocess.Popen(['tool'])\n",
        encoding="utf-8",
    )

    result = scan_subprocess_timeout_policy(tmp_path)

    assert result["status"] == "mismatch"
    assert result["findings"][0]["call"] == "subprocess.Popen"


def test_cli_validate_governance_reports_contract():
    result = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "validate-governance", "--root", str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "governance_validation_report"' in result.stdout
