from pathlib import Path
import json
import os
import subprocess
import sys

from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.release_policy import RELEASE_PROFILES
from mathdevmcp.release_profile_analysis import release_profile_analysis


ROOT = Path(__file__).resolve().parent.parent


def test_release_profile_analysis_contract_and_profile_coverage(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)

    report = release_profile_analysis(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_profile_analysis"}
    assert {entry["profile"] for entry in report["profiles"]} == RELEASE_PROFILES
    assert len(report["profiles"]) == len(RELEASE_PROFILES)
    assert report["release_claims"]["base_public"]["claim_ready"] is True
    assert report["release_claims"]["base_public"]["profiles"] == ["base", "public"]
    assert report["status"] in {"ready", "ready_with_caveats"}


def test_release_profile_analysis_keeps_strict_blockers_visible(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "definitely-missing-backend-env")
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)

    report = release_profile_analysis(ROOT)
    strict = report["strict_profile_blockers"]

    assert "backend" in strict
    assert any(blocker["kind"] == "backend_lean_dojo_unavailable" for blocker in strict["backend"]["blockers"])
    assert "private-corpus" in strict
    assert any(blocker["kind"] == "private_corpus_manifest_required" for blocker in strict["private-corpus"]["blockers"])
    assert report["release_claims"]["backend"]["claim_ready"] is False
    assert report["release_claims"]["private_corpus"]["claim_ready"] is False


def test_release_profile_analysis_doctor_highlights_are_public_safe():
    report = release_profile_analysis(ROOT)
    highlights = report["doctor_highlights"]
    rendered = json.dumps(highlights)

    assert "lean" in highlights
    assert "dependency_conflicts" in highlights
    assert "/home/" not in rendered
    assert "MATHDEVMCP_PRIVATE_CORPUS_MANIFEST" not in rendered


def test_release_profile_analysis_cli_and_mcp_access():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "release-profile-analysis",
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "release_profile_analysis"}

    mcp_payload = call_mcp_tool("release_profile_analysis", {"root": str(ROOT)})
    assert mcp_payload["ok"] is True
    assert mcp_payload["metadata"] == {"schema_version": "1.0", "contract": "release_profile_analysis"}
