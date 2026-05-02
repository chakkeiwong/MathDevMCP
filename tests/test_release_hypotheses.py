from pathlib import Path
import subprocess
import sys

from mathdevmcp.release_hypotheses import release_hypothesis_check


ROOT = Path(__file__).resolve().parent.parent


def test_public_release_hypothesis_check_passes_without_private_secret(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)
    monkeypatch.delenv("MATHDEVMCP_BACKEND_CONDA_ENV", raising=False)

    report = release_hypothesis_check(ROOT, public=True)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_hypothesis_check"}
    assert report["status"] == "consistent"
    assert {check["name"] for check in report["checks"]} == {
        "publication_invariant",
        "ci_hypothesis_gate",
        "evidence_boundary",
        "strict_full_reproducibility",
    }
    strict = next(check for check in report["checks"] if check["name"] == "strict_full_reproducibility")
    assert any(finding["kind"] == "strict_full_check_not_requested" for finding in strict["findings"])
    assert report["blockers"] == []


def test_strict_canonical_hypothesis_requires_canonical_backend(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "mathdev-lean")
    monkeypatch.setenv("MATHDEVMCP_REQUIRE_LATEXML", "1")
    monkeypatch.setenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", "/tmp/missing-private-manifest.json")

    report = release_hypothesis_check(ROOT, strict_full=True, require_canonical_backend=True)

    assert report["status"] == "mismatch"
    blockers = {finding["kind"] for finding in report["blockers"]}
    assert "canonical_backend_env_not_selected" in blockers


def test_release_hypothesis_check_cli_public_mode():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "release-hypothesis-check",
            "--root",
            str(ROOT),
            "--public",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "release_hypothesis_check"' in result.stdout
    assert '"publication_invariant"' in result.stdout


def test_release_hypotheses_script_help():
    result = subprocess.run(
        [str(ROOT / "scripts" / "release_hypotheses_check.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--strict-full" in result.stdout
    assert "--require-canonical-backend" in result.stdout
