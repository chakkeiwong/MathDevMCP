from mathdevmcp.dependency_graph import build_dependency_graph
from mathdevmcp.math_change_impact import math_change_impact
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def test_math_change_impact_reports_downstream_graph_label() -> None:
    graph = {
        "nodes": [
            {"id": "label:eq:base", "kind": "label", "label": "eq:base"},
            {"id": "label:prop:downstream", "kind": "label", "label": "prop:downstream"},
        ],
        "edges": [{"source": "label:prop:downstream", "target": "label:eq:base", "relation": "uses_equation"}],
    }

    result = math_change_impact("eq:base", graph=graph)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_change_impact_result"}
    assert result["status"] == "impacts_found"
    assert any(item["artifact_id"] == "label:prop:downstream" for item in result["affected_artifacts"])
    assert result["dependency_paths"]


def test_math_change_impact_reports_implementation_test_mentions() -> None:
    result = math_change_impact(
        "eq:logdet",
        code_links=[{"id": "code:likelihood", "label": "eq:logdet"}],
        generated_tests=[{"id": "test:logdet", "target": "eq:logdet"}],
    )

    kinds = {item["kind"] for item in result["affected_artifacts"]}
    assert {"code_link", "generated_test"}.issubset(kinds)
    assert all(item["confidence"] == "possible_unlinked" for item in result["affected_artifacts"])


def test_math_change_impact_reports_assumption_manifest_entry() -> None:
    result = math_change_impact(
        "positive_definite",
        changed_kind="assumption",
        assumptions=[{"id": "assumption:positive_definite", "name": "positive_definite"}],
    )

    assert any(item["kind"] == "assumption_entry" for item in result["affected_artifacts"])


def test_math_change_impact_reports_claim_packet_mentions() -> None:
    result = math_change_impact(
        "eq:euler",
        claims=[{"claim_id": "claim:euler", "claim": "The identity eq:euler holds."}],
    )

    assert any(item["kind"] == "claim_packet" for item in result["affected_artifacts"])


def test_math_change_impact_missing_links_do_not_claim_no_impact() -> None:
    result = math_change_impact("eq:missing", graph=build_dependency_graph())

    assert result["status"] == "inconclusive"
    assert any(warning["kind"] == "missing_downstream_links" for warning in result["missing_link_warnings"])
    assert "not prove no impact" in result["evidence_boundary"]


def test_math_change_impact_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "math_change_impact",
        {"changed_id": "eq:euler", "claims": [{"claim_id": "claim:euler", "claim": "Uses eq:euler."}]},
    )

    assert "math_change_impact" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "math_change_impact_result"
    assert result["status"] == "impacts_found"
