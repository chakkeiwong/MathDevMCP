from pathlib import Path

from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from test_context_and_fixtures import EXPECTED_BENCHMARK_SUMMARY, EXPECTED_BENCHMARK_TOTAL


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent


def test_list_mcp_tools_includes_implementation_brief():
    names = {tool["name"] for tool in list_mcp_tools()}

    assert "implementation_brief" in names
    assert "compare_label_code" in names
    assert "benchmark_gate" in names



def test_call_mcp_tool_compare_label_code_returns_traceable_result():
    result = call_mcp_tool(
        "compare_label_code",
        {
            "root": str(FIXTURES),
            "label": "prop:transport-mismatch",
            "code": str(FIXTURES / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
        },
    )

    assert result["status"] == "mismatch"
    assert result["doc_context"]["file"] == "doc_consistency_bad.tex"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert result["provenance"]["label"] == "prop:transport-mismatch"
    assert result["ok"] is True



def test_call_mcp_tool_implementation_brief_returns_consistent_result():
    result = call_mcp_tool(
        "implementation_brief",
        {
            "root": str(FIXTURES),
            "query": "transport log-determinant identity",
            "code": str(FIXTURES / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
        },
    )

    assert result["status"] == "consistent"
    assert result["selected_label"] == "prop:transport-logdet"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"}
    assert result["ok"] is True



def test_call_mcp_tool_run_benchmarks_aggregates_results():
    result = call_mcp_tool("run_benchmarks", {"root": str(ROOT)})

    assert result["total"] == EXPECTED_BENCHMARK_TOTAL
    assert result["passed"] == EXPECTED_BENCHMARK_TOTAL
    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert all("details" in item for item in result["results"])
    assert result["summary"] == EXPECTED_BENCHMARK_SUMMARY
    assert result["ok"] is True



def test_call_mcp_tool_benchmark_gate_returns_ci_shape():
    result = call_mcp_tool("benchmark_gate", {"root": str(ROOT)})

    assert result == {
        "ok": True,
        "passed": True,
        "total": EXPECTED_BENCHMARK_TOTAL,
        "passed_count": EXPECTED_BENCHMARK_TOTAL,
        "failed_count": 0,
        "summary": EXPECTED_BENCHMARK_SUMMARY,
        "policy": {
            "name": "all_benchmarks_must_pass",
            "required_pass_rate": 1.0,
            "allow_category_failures": {},
            "description": "Every benchmark case must pass; no category-specific failure budget is currently allowed.",
        },
        "metadata": {"schema_version": "1.0", "contract": "benchmark_gate"},
    }



def test_call_mcp_tool_returns_structured_error_for_unknown_tool():
    result = call_mcp_tool("missing_tool", {})

    assert result == {
        "ok": False,
        "error": {"type": "unknown_tool", "message": "Unknown MathDevMCP tool: missing_tool"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }



def test_call_mcp_tool_returns_structured_error_for_invalid_arguments():
    result = call_mcp_tool("compare_label_code", {"root": str(FIXTURES), "label": "prop:transport-mismatch"})

    assert result == {
        "ok": False,
        "error": {"type": "invalid_arguments", "message": "Missing required string argument: code"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }
