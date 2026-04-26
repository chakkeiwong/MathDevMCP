import subprocess

from mathdevmcp.lean_check import check_lean_source


def test_check_lean_source_verifies_nat_add_comm():
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
    source = """
theorem bad (a b : Nat) : a + b = a := by
  exact Nat.add_comm a b
"""

    result = check_lean_source(source, timeout_seconds=10)

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["kind"] == "lean_failed"
    assert result["evidence"][0]["returncode"] != 0


def test_check_lean_source_rejects_sorry_in_certified_mode():
    source = """
theorem placeholder (a b : Nat) : a + b = b + a := by
  sorry
"""

    result = check_lean_source(source, allow_sorry=False)

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_placeholder"
    assert result["evidence"][0]["uses_sorry"] is True


def test_check_lean_source_allows_sorry_without_certification():
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


def test_check_lean_source_reports_timeout_as_inconclusive(monkeypatch):
    def timeout_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=["lean"], timeout=1)

    monkeypatch.setattr(subprocess, "run", timeout_run)

    result = check_lean_source("theorem t : True := by trivial", timeout_seconds=1)

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "lean_timeout"


def test_check_lean_source_returns_reproducible_evidence():
    result = check_lean_source("theorem t : True := by trivial")

    evidence = result["evidence"][0]
    assert evidence["command"][0].endswith("lean")
    assert evidence["source_sha256"]
    assert "lean_version" in evidence
