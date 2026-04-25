from pathlib import Path
import subprocess
import sys

from mathdevmcp.contracts import validate_contract_payload, validate_derivation_evidence
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import check_proof_obligation as server_check_proof_obligation
from mathdevmcp.proof_obligations import check_proof_obligation


ROOT = Path(__file__).resolve().parent.parent


def test_check_proof_obligation_certifies_exact_normalized_match():
    result = check_proof_obligation("log_pi + logdet", "log_pi + logdet")

    assert result["status"] == "equivalent"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_obligation_result"}
    assert result["evidence"][0]["kind"] == "normalized_match"
    assert result["evidence"][0]["backend_status"] == "proved"


def test_check_proof_obligation_uses_sympy_for_commutative_identity():
    result = check_proof_obligation("a + b", "b + a", backend="sympy")

    assert result["status"] == "equivalent"
    assert result["backend"] == "sympy"
    assert result["evidence"][0]["kind"] == "backend_verified"
    assert result["evidence"][0]["backend_status"] == "proved"


def test_check_proof_obligation_flags_numeric_mismatch_with_sympy():
    result = check_proof_obligation("1 + 1", "3", backend="sympy")

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["kind"] == "backend_counterexample"
    assert result["evidence"][0]["backend_status"] == "disproved"


def test_check_proof_obligation_preserves_assumptions_and_reports_unimplemented_backend():
    result = check_proof_obligation("x**2", "x", assumptions=["x is idempotent"], backend="z3")

    assert result["status"] == "inconclusive"
    assert result["assumptions"] == ["x is idempotent"]
    assert result["evidence"][0]["backend"] == "z3"
    assert result["evidence"][0]["backend_status"] == "not_encodable"


def test_check_proof_obligation_rejects_unbounded_backend_input():
    result = check_proof_obligation("__import__('os').system('true')", "0", backend="sympy")

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "backend_not_encodable"


def test_check_proof_obligation_auto_preserves_backend_not_encodable_evidence():
    result = check_proof_obligation("a + b @ c", "b + a @ c", backend="auto")

    assert result["status"] == "unverified"
    assert any(item["kind"] == "backend_not_encodable" for item in result["evidence"])


def test_proof_obligation_contract_and_evidence_validate():
    result = check_proof_obligation("a + b", "b + a", backend="sympy")

    assert validate_contract_payload({**result, "ok": True}) == []
    assert validate_derivation_evidence(result["evidence"]) == []


def test_mcp_facade_exposes_check_proof_obligation():
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool("check_proof_obligation", {"lhs": "a + b", "rhs": "b + a", "backend": "sympy"})

    assert "check_proof_obligation" in names
    assert result["status"] == "equivalent"
    assert result["ok"] is True


def test_mcp_server_check_proof_obligation_delegates():
    result = server_check_proof_obligation("a + b", "b + a", backend="sympy")

    assert result["status"] == "equivalent"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_obligation_result"}


def test_cli_check_proof_obligation_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "check-proof-obligation",
            "a + b",
            "b + a",
            "--backend",
            "sympy",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "proof_obligation_result"' in result.stdout
    assert '"status": "equivalent"' in result.stdout
