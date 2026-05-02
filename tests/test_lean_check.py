import subprocess

import pytest

from mathdevmcp.doctor import doctor_report
from mathdevmcp.lean_check import _uses_placeholder, check_lean_source


def _requires_lean():
    if not doctor_report()["capabilities"]["lean"]["available"]:
        pytest.skip("Lean executable is unavailable")


def test_check_lean_source_verifies_nat_add_comm():
    _requires_lean()
    source = """
theorem add_comm_smoke (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
"""

    result = check_lean_source(source, timeout_seconds=10)

    assert result["status"] == "verified"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_check_result"}
    assert result["evidence"][0]["kind"] == "lean_verified"
    assert result["evidence"][0]["uses_sorry"] is False
    assert result["evidence"][0]["returncode"] == 0


def test_check_lean_source_rejects_false_proof():
    _requires_lean()
    source = """
theorem bad (a b : Nat) : a + b = a := by
  exact Nat.add_comm a b
"""

    result = check_lean_source(source, timeout_seconds=10)

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["kind"] == "lean_failed"
    assert result["evidence"][0]["returncode"] != 0


def test_check_lean_source_rejects_sorry_in_certified_mode():
    _requires_lean()
    source = """
theorem placeholder (a b : Nat) : a + b = b + a := by
  sorry
"""

    result = check_lean_source(source, allow_sorry=False)

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_placeholder"
    assert result["evidence"][0]["uses_sorry"] is True


def test_placeholder_scanner_ignores_comments_strings_and_identifiers():
    source = '''
-- sorry in a line comment
/- admit in a block comment -/
def sorryCount := 1
def admitTheoremName := 2
#eval "sorry and admit in a string"
theorem ok : True := by
  trivial
'''

    assert _uses_placeholder(source) is False


def test_placeholder_scanner_detects_placeholder_tokens():
    assert _uses_placeholder("theorem t : True := by\n  sorry\n") is True
    assert _uses_placeholder("theorem t : True := by\n  admit\n") is True
    assert _uses_placeholder("/- outer /- nested sorry -/ still comment -/\ntheorem t : True := by trivial") is False


def test_check_lean_source_allows_sorry_without_certification():
    _requires_lean()
    source = """
theorem placeholder (a b : Nat) : a + b = b + a := by
  sorry
"""

    result = check_lean_source(source, allow_sorry=True)

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_placeholder"
    assert result["evidence"][0]["returncode"] == 0


def test_check_lean_source_reports_unavailable_lean_as_inconclusive(monkeypatch):
    def missing_run(*args, **kwargs):
        raise FileNotFoundError("lean")

    monkeypatch.setattr(subprocess, "run", missing_run)

    result = check_lean_source("theorem t : True := by trivial")

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_unavailable"


def test_check_lean_source_reports_toolchain_download_failure_as_inconclusive(monkeypatch, tmp_path):
    lean = tmp_path / "lean"
    lean.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    lean.chmod(0o755)
    monkeypatch.setenv("MATHDEVMCP_LEAN_PATH", str(lean))

    def failed_toolchain_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, "", "error: error during download")

    monkeypatch.setattr(subprocess, "run", failed_toolchain_run)

    result = check_lean_source("theorem t : True := by trivial")

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_unavailable"


def test_check_lean_source_reports_timeout_as_inconclusive(monkeypatch):
    _requires_lean()
    def timeout_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=["lean"], timeout=1)

    monkeypatch.setattr(subprocess, "run", timeout_run)

    result = check_lean_source("theorem t : True := by trivial", timeout_seconds=1)

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_timeout"


def test_check_lean_source_returns_reproducible_evidence():
    _requires_lean()
    result = check_lean_source("theorem t : True := by trivial")

    evidence = result["evidence"][0]
    assert evidence["command"][0].endswith("lean")
    assert evidence["source_sha256"]
    assert "lean_version" in evidence
