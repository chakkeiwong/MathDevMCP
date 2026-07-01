from mathdevmcp.equation_code_match import code_implements_equation
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def test_equation_code_match_reports_consistent_structural_terms() -> None:
    result = code_implements_equation(
        "logdet(S) + solve(S, v)",
        "def f(S, v):\n    return logdet(S) + solve(S, v)\n",
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "equation_code_match_result"}
    assert result["status"] == "consistent"
    assert {"logdet", "solve", "S", "v"}.issubset(set(result["matched_terms"]))
    assert result["workbench_result"]["status"] == "unknown"


def test_equation_code_match_reports_missing_logdet() -> None:
    result = code_implements_equation(
        "logdet(S) + solve(S, v)",
        "def f(S, v):\n    return solve(S, v)\n",
    )

    assert result["status"] == "mismatch"
    assert "logdet" in result["missing_terms"]


def test_equation_code_match_reports_extra_regularizer_as_audit_only() -> None:
    result = code_implements_equation(
        "solve(S, v)",
        "def f(S, v, lam):\n    return solve(S, v) + lam\n",
    )

    assert result["status"] == "consistent"
    assert "lam" in result["extra_code_terms"]


def test_equation_code_match_reports_transpose_conflict() -> None:
    result = code_implements_equation(
        "transpose(A) * x",
        "def f(A, x):\n    return A * x\n",
    )

    assert result["status"] == "mismatch"
    assert result["conflicts"][0]["kind"] == "transpose_mismatch"


def test_equation_code_match_uses_alias_map() -> None:
    result = code_implements_equation(
        "logdet(Sigma)",
        "def f(S):\n    return logdet(S)\n",
        aliases={"Sigma": "S"},
    )

    assert result["status"] == "consistent"
    assert "S" in result["matched_terms"]


def test_equation_code_match_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "code_implements_equation",
        {"equation": "logdet(S)", "code": "def f(S):\n    return logdet(S)\n"},
    )

    assert "code_implements_equation" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "equation_code_match_result"
    assert result["status"] == "consistent"
