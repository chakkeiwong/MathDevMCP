from mathdevmcp.backend_route_planner import plan_backend_routes
from mathdevmcp.external_tool_policy import external_tool_first_plan
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "path": "/python", "version": "1.14.0"},
    "sage": {"available": False, "status": "unavailable", "path": None, "version": None},
    "lean": {"available": False, "status": "unavailable", "path": None, "version": None},
}

INTEGRATIONS = {
    "leansearchv2": {
        "resolved_available": True,
        "resolved_version": "0.1.0",
        "resolved_version_status": "match",
        "resolved_scope": "backend_python",
    },
    "lean_explore": {
        "resolved_available": True,
        "resolved_version": "1.2.1",
        "resolved_version_status": "match",
        "resolved_scope": "backend_python",
    },
    "pantograph": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
    "lean_dojo": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
    "jixia": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "not_applicable",
        "resolved_scope": "unavailable",
    },
}


def test_external_tool_first_plan_prefers_available_external_backend() -> None:
    result = external_tool_first_plan(
        "a + b = b + a",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "external_tool_first_plan_result"}
    assert result["status"] == "external_route_available"
    assert result["selected_external_tools"][0]["tool"] == "sympy"
    assert result["selected_external_tools"][0]["status"] == "available"
    assert result["in_house_search_gate"]["allowed"] is False
    assert result["in_house_search_gate"]["required"] is False
    assert "external_tool_plan_not_certificate" in {item["code"] for item in result["non_claims"]}


def test_external_tool_first_plan_blocks_in_house_search_without_gap_justification() -> None:
    unavailable = {
        "sympy": {"available": False, "status": "unavailable"},
        "sage": {"available": False, "status": "unavailable"},
        "lean": {"available": False, "status": "unavailable"},
    }

    result = external_tool_first_plan(
        "x + 1 = 1 + x",
        capabilities=unavailable,
        integrations={},
    )

    assert result["status"] == "blocked_pending_external_tool_or_gap_justification"
    assert result["selected_external_tools"] == []
    assert result["in_house_search_gate"]["allowed"] is False
    assert result["in_house_search_gate"]["required"] is True
    assert "gap justification" in result["reason"]


def test_external_tool_first_plan_allows_in_house_only_with_explicit_gap() -> None:
    unavailable = {
        "sympy": {"available": False, "status": "unavailable"},
        "sage": {"available": False, "status": "unavailable"},
        "lean": {"available": False, "status": "unavailable"},
    }

    result = external_tool_first_plan(
        "x + 1 = 1 + x",
        capabilities=unavailable,
        integrations={},
        allow_in_house_gap=True,
        gap_justification="All configured external tools are unavailable in this offline test fixture.",
    )

    assert result["status"] == "in_house_gap_justified"
    assert result["in_house_search_gate"]["allowed"] is True
    assert result["in_house_search_gate"]["gap_justification"]


def test_external_tool_first_plan_formalization_route_is_selected_but_not_certifying() -> None:
    result = external_tool_first_plan(
        r"0 = \beta \E[V_k(k',z') \mid z]",
        goal_kind="document_repair",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )

    by_tool = {item["tool"]: item for item in result["considered_tools"]}
    assert by_tool["sympy"]["status"] == "requires_formalization"
    assert by_tool["leansearchv2"]["status"] == "available"
    assert by_tool["jixia"]["status"] == "unavailable"
    assert result["diagnostics"]["requires_formalization_count"] >= 1
    assert "Retrieval evidence only" in by_tool["leansearchv2"]["certification_boundary"]


def test_backend_route_plan_embeds_external_tool_first_ledger() -> None:
    result = plan_backend_routes("a + b = b + a", capabilities=CAPABILITIES, integrations=INTEGRATIONS)

    plan = result["external_tool_first_plan"]
    assert plan["metadata"]["contract"] == "external_tool_first_plan_result"
    assert plan["selected_external_tools"][0]["tool"] == "sympy"
    assert plan["boundary"].startswith("This plan is a routing")


def test_external_tool_first_plan_is_exposed_to_mcp_facade() -> None:
    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "external_tool_first_plan",
        {
            "target": "a + b = b + a",
            "capabilities": CAPABILITIES,
            "integrations": INTEGRATIONS,
        },
    )

    assert "external_tool_first_plan" in tools
    assert tools["external_tool_first_plan"]["output_contract"] == "external_tool_first_plan_result"
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "external_tool_first_plan_result"
    assert result["status"] == "external_route_available"
