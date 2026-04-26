from pathlib import Path
import subprocess
import sys

from mathdevmcp.contracts import validate_contract_payload, validate_derivation_evidence
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_derivation_label as server_audit_derivation_label
from mathdevmcp.proof_audit import audit_derivation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_audit_derivation_extracts_single_equation_obligation():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")

    assert result["status"] == "verified"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_result"}
    assert result["counts"]["verified"] == 1
    assert result["counts"]["total"] == 1
    assert result["obligations"][0]["lhs"] == "a + b"
    assert result["obligations"][0]["rhs"] == "b + a"
    assert result["obligations"][0]["status"] == "verified"
    assert result["obligations"][0]["provenance"]["label"] == "eq:proof-audit-single"


def test_audit_derivation_extracts_adjacent_align_obligations_only():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-chain", backend="sympy")

    assert result["status"] == "unverified"
    assert result["counts"]["total"] == 2
    assert [(item["lhs"], item["rhs"]) for item in result["obligations"]] == [
        ("f", "a + b"),
        ("a + b", "b + a"),
    ]
    assert result["obligations"][0]["status"] == "unverified"
    assert result["obligations"][1]["status"] == "verified"
    assert all(item["source_text"] for item in result["obligations"])


def test_audit_derivation_marks_ambiguous_multiequality_inconclusive():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-ambiguous", backend="sympy")

    assert result["status"] == "inconclusive"
    assert result["counts"]["not_extracted"] == 1
    assert result["obligations"][0]["status"] == "inconclusive"
    assert result["obligations"][0]["classification"] == "not_extracted"


def test_audit_derivation_nearby_context_does_not_count_as_proof():
    result = audit_derivation_for_label(str(FIXTURES), "prop:proof-audit-nearby", paragraph_context=True, backend="sympy")

    assert result["status"] == "inconclusive"
    assert result["counts"]["verified"] == 0
    assert result["counts"]["not_extracted"] == 1


def test_audit_derivation_reports_numeric_false_identity_as_mismatch():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-false", backend="sympy")

    assert result["status"] == "mismatch"
    assert result["counts"]["mismatched"] == 1
    assert result["obligations"][0]["evidence"][0]["kind"] == "backend_counterexample"


def test_audit_derivation_abstains_on_kalman_hessian_style_notation():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-kalman", backend="sympy")

    assert result["status"] == "inconclusive"
    assert result["counts"]["not_encodable"] == 1
    assert result["obligations"][0]["classification"] == "human_review"
    assert result["obligations"][0]["status"] == "inconclusive"


def test_proof_audit_contract_and_evidence_validate():
    result = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")

    assert validate_contract_payload({**result, "ok": True}) == []
    for obligation in result["obligations"]:
        assert validate_derivation_evidence(obligation["evidence"]) == []


def test_mcp_facade_exposes_audit_derivation_label():
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "audit_derivation_label",
        {"root": str(FIXTURES), "label": "eq:proof-audit-single", "backend": "sympy"},
    )

    assert "audit_derivation_label" in names
    assert result["ok"] is True
    assert result["status"] == "verified"


def test_mcp_server_audit_derivation_label_delegates():
    result = server_audit_derivation_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")

    assert result["status"] == "verified"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_result"}


def test_cli_audit_derivation_label_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-derivation-label",
            "eq:proof-audit-single",
            "--root",
            str(FIXTURES),
            "--backend",
            "sympy",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "proof_audit_result"' in result.stdout
    assert '"status": "verified"' in result.stdout
