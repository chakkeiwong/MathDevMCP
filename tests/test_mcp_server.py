"""Slim MCP server tests — exercises the 3 surviving deterministic primitives.

Workflow behaviors that used to live behind the MCP server (compare/audit/
benchmark/release/governance/doctor) are tested at the library level in their
own per-module test files; the FastMCP wrappers here only confirm the
parameters get marshalled correctly into the facade.
"""

from pathlib import Path

from mathdevmcp.mcp_server import check_equality, latex_label_lookup, lean_check


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_mcp_server_latex_label_lookup_returns_label_metadata():
    result = latex_label_lookup(str(FIXTURES), "prop:transport-logdet")

    assert result["label"] == "prop:transport-logdet"
    assert result["file"] == "doc_consistency_good.tex"
    assert result["ok"] is True


def test_mcp_server_check_equality_certifies_normalization_match():
    result = check_equality("a + b", "a + b")

    assert result["status"] == "equivalent"
    assert result["evidence"][0]["severity"] == "certifying"


def test_mcp_server_check_equality_refutes_with_counterexample():
    result = check_equality("1 + 1", "3")

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["severity"] == "blocking"


def test_mcp_server_lean_check_returns_lean_envelope():
    result = lean_check("example : 1 + 1 = 2 := rfl")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_check_result"}
    assert result["status"] in {"verified", "mismatch", "inconclusive"}


def test_mcp_server_lean_check_refuses_placeholder_proof():
    result = lean_check("example : 1 + 1 = 2 := by sorry")

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["uses_sorry"] is True
