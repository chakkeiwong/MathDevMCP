"""Slim MCP facade tests — exercises the 3 surviving deterministic primitives.

Library-level workflow tests (proof_audit, kalman_workflows, consistency,
benchmarks, release_policy, governance, doctor) live in their own per-module
test files; they are unaffected by the MCP surface shrink.
"""

from pathlib import Path

from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_list_mcp_tools_exposes_three_deterministic_primitives():
    names = {tool["name"] for tool in list_mcp_tools()}

    assert names == {"latex_label_lookup", "check_equality", "lean_check"}


def test_list_mcp_tools_advertises_optional_capabilities():
    by_name = {tool["name"]: tool for tool in list_mcp_tools()}

    assert by_name["check_equality"]["optional_capability"] == "symbolic_backend"
    assert by_name["lean_check"]["optional_capability"] == "lean_backend"
    assert by_name["latex_label_lookup"]["optional_capability"] is None


def test_call_mcp_tool_latex_label_lookup_returns_paragraph_context():
    result = call_mcp_tool(
        "latex_label_lookup",
        {"root": str(FIXTURES), "label": "prop:transport-logdet"},
    )

    assert result["label"] == "prop:transport-logdet"
    assert result["file"] == "doc_consistency_good.tex"
    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "latex_paragraph_context"}


def test_call_mcp_tool_check_equality_certifies_normalization_match():
    result = call_mcp_tool(
        "check_equality",
        {"lhs": "a + b", "rhs": "a + b"},
    )

    assert result["status"] == "equivalent"
    assert result["evidence"][0]["severity"] == "certifying"
    assert result["ok"] is True


def test_call_mcp_tool_check_equality_certifies_sympy_simplification():
    result = call_mcp_tool(
        "check_equality",
        {"lhs": "(a + b)*(a - b)", "rhs": "a*a - b*b"},
    )

    assert result["status"] == "equivalent"
    assert result["evidence"][0]["severity"] == "certifying"


def test_call_mcp_tool_check_equality_refutes_with_counterexample():
    result = call_mcp_tool(
        "check_equality",
        {"lhs": "1 + 1", "rhs": "3"},
    )

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["severity"] == "blocking"


def test_call_mcp_tool_lean_check_returns_lean_envelope():
    # Lean is not required to be installed; we only assert the envelope shape.
    result = call_mcp_tool("lean_check", {"source": "example : 1 + 1 = 2 := rfl"})

    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_check_result"}
    assert result["status"] in {"verified", "mismatch", "inconclusive"}
    assert result["evidence"][0]["backend"] == "lean"


def test_call_mcp_tool_lean_check_refuses_placeholder_proof_in_certified_mode():
    result = call_mcp_tool(
        "lean_check",
        {"source": "example : 1 + 1 = 2 := by sorry"},
    )

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["uses_sorry"] is True


def test_call_mcp_tool_returns_structured_error_for_unknown_tool():
    result = call_mcp_tool("missing_tool", {})

    assert result == {
        "ok": False,
        "error": {"type": "unknown_tool", "message": "Unknown MathDevMCP tool: missing_tool"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }


def test_call_mcp_tool_returns_structured_error_for_invalid_arguments():
    result = call_mcp_tool("check_equality", {"lhs": "a + b"})

    assert result == {
        "ok": False,
        "error": {"type": "invalid_arguments", "message": "Missing required string argument: rhs"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }
