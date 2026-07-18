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
    assert result["trace_map"]["matched_terms"] == result["matched_terms"]
    assert "not semantic proof" in result["trace_map"]["boundary"]
    assert result["workbench_result"]["status"] == "unknown"
    assert result["trace_map"]["scope_diagnostic"]["status"] == "scope_covered_structurally"


def test_equation_code_match_reports_missing_logdet() -> None:
    result = code_implements_equation(
        "logdet(S) + solve(S, v)",
        "def f(S, v):\n    return solve(S, v)\n",
    )

    assert result["status"] == "mismatch"
    assert "logdet" in result["missing_terms"]
    assert "logdet" in result["trace_map"]["missing_terms"]


def test_equation_code_match_reports_extra_regularizer_as_audit_only() -> None:
    result = code_implements_equation(
        "solve(S, v)",
        "def f(S, v, lam):\n    return solve(S, v) + lam\n",
    )

    assert result["status"] == "consistent"
    assert "lam" in result["extra_code_terms"]
    assert "lam" in result["trace_map"]["extra_code_terms"]


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
    assert result["trace_map"]["alias_map"] == {"Sigma": "S"}
    assert "S" in result["trace_map"]["mapped_terms"]
    assert {"equation_term": "Sigma", "mapped_code_term": "S", "matched": True, "source": "alias_map"} in result["trace_map"]["term_traces"]


def test_equation_code_match_trace_map_records_alias_collisions() -> None:
    result = code_implements_equation(
        "logdet(Sigma) + trace(Cov)",
        "def f(S):\n    return logdet(S) + trace(S)\n",
        aliases={"Sigma": "S", "Cov": "S"},
    )

    assert result["status"] == "consistent"
    assert result["trace_map"]["alias_collisions"] == [
        {"mapped_code_term": "S", "equation_terms": ["Cov", "Sigma"]}
    ]
    assert {item["equation_term"] for item in result["trace_map"]["term_traces"]} >= {"Sigma", "Cov"}


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


def test_scope_diagnostic_distinguishes_no_callable_boundary_from_missing_term() -> None:
    result = code_implements_equation(
        "K_P(theta)-K_D(theta) = ell_P(theta)-ell_D(theta)",
        "kernel_residual = (k_p - k_d) - (ell_p - ell_d)\n",
        aliases={"K_P": "k_p", "K_D": "k_d", "ell_P": "ell_p", "ell_D": "ell_d"},
    )

    assert result["status"] == "mismatch"
    assert result["missing_terms"] == ["theta"]
    assert result["trace_map"]["scope_diagnostic"]["status"] == "scope_unverifiable_no_callable_boundary"
    assert result["trace_map"]["scope_diagnostic"]["missing_scope_terms"] == ["theta"]


def test_scope_diagnostic_reports_not_applicable_and_limited_separately() -> None:
    scalar = code_implements_equation("x = y + z", "x = y + z\n")
    limited = code_implements_equation(
        "Q(theta, data) = theta + data",
        "def q(data):\n    return data\n",
        aliases={"Q": "q"},
    )

    assert scalar["trace_map"]["scope_diagnostic"]["status"] == "not_applicable"
    assert limited["status"] == "scope_limited"
    assert limited["trace_map"]["scope_diagnostic"]["missing_scope_terms"] == ["theta"]


def test_missing_required_operator_takes_precedence_over_scope_limitation() -> None:
    result = code_implements_equation(
        "logdet(S) + solve(S, innovation)",
        "def likelihood(S, innovation):\n    return logdet(S)\n",
    )

    assert result["status"] == "mismatch"
    assert "solve" in result["missing_terms"]
    assert result["trace_map"]["scope_diagnostic"]["status"] == "scope_covered_structurally"
