from pathlib import Path

from mathdevmcp.mcp_facade import MCP_TOOL_SPECS, TOOL_HANDLERS, call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import MCP_SERVER_EXPOSED_TOOLS, mcp


ROOT = Path(__file__).resolve().parent.parent
VALID_TIERS = {"primitive", "workflow", "operational", "informational"}
VALID_STABILITIES = {"stable", "experimental", "deprecated"}


def test_mcp_registry_is_facade_authority():
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}
    listed = {tool["name"] for tool in list_mcp_tools()}

    assert set(TOOL_HANDLERS) == registry_names
    assert listed == registry_names


def test_mcp_registry_classifies_every_tool():
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}
    listed_by_name = {tool["name"]: tool for tool in list_mcp_tools()}

    for spec in MCP_TOOL_SPECS:
        assert spec.description
        assert spec.output_contract
        assert spec.tier in VALID_TIERS
        assert spec.stability in VALID_STABILITIES
        assert spec.deprecated is (spec.stability == "deprecated")
        if spec.deprecated:
            assert spec.replacement in registry_names
        else:
            assert spec.replacement is None

        listed = listed_by_name[spec.name]
        assert listed["tier"] == spec.tier
        assert listed["stability"] == spec.stability
        assert listed["output_contract"] == spec.output_contract
        assert listed["certifying_capable"] is spec.certifying_capable
        assert listed["deprecated"] is spec.deprecated
        assert listed["replacement"] == spec.replacement


def test_review_packet_surface_descriptions_preserve_diagnostic_boundary():
    tools = {tool["name"]: tool for tool in list_mcp_tools()}

    assert tools["prepare_review_packet"]["certifying_capable"] is False
    assert "diagnostic only" in tools["prepare_review_packet"]["description"].lower()
    assert "not a certificate" in tools["prepare_review_packet"]["description"].lower()
    assert tools["math_review_packet"]["certifying_capable"] is False
    assert "review packet" in tools["math_review_packet"]["description"].lower()


def test_mcp_preferred_surface_stays_intentional_size():
    preferred = [spec for spec in MCP_TOOL_SPECS if spec.stability == "stable" and spec.tier != "informational"]

    assert 8 <= len(preferred) <= 20
    assert any(spec.tier == "primitive" for spec in preferred)
    assert any(spec.tier == "workflow" for spec in preferred)
    assert any(spec.tier == "operational" for spec in preferred)


def test_mcp_server_exposure_matches_registry_aliases():
    server_names = {spec.exposed_server_name for spec in MCP_TOOL_SPECS}

    assert server_names == MCP_SERVER_EXPOSED_TOOLS
    assert "tool_matrix" in {spec.name for spec in MCP_TOOL_SPECS}
    assert "get_tool_matrix" in MCP_SERVER_EXPOSED_TOOLS


def test_document_derivation_fastmcp_schema_exposes_v2_structured_content_tools():
    tool = mcp._tool_manager._tools["audit_document_derivation_tree"]
    properties = tool.parameters["properties"]

    assert properties["response_mode"]["default"] == "compact"
    assert properties["response_mode"]["enum"] == ["compact", "detailed", "artifact_only"]
    assert properties["artifact_root"]["default"] is None
    assert properties["target_limit"]["default"] is None
    assert properties["target_cursor"]["default"] is None
    assert tool.fn_metadata.output_schema is None

    resolver = mcp._tool_manager._tools["resolve_document_derivation_records"]
    resolver_properties = resolver.parameters["properties"]
    assert resolver_properties["target_id"]["default"] is None
    assert resolver_properties["offset"]["default"] == 0
    assert resolver_properties["limit"]["default"] == 100
    assert resolver.fn_metadata.output_schema is None

    registry = {spec.name: spec for spec in MCP_TOOL_SPECS}
    assert registry["audit_document_derivation_tree"].output_contract == "document_derivation_response"
    assert registry["resolve_document_derivation_records"].output_contract == "document_derivation_record_page"


def test_mcp_readme_mentions_every_registry_and_server_tool():
    text = (ROOT / "mcp" / "README.md").read_text(encoding="utf-8")

    for spec in MCP_TOOL_SPECS:
        assert f"`{spec.name}`" in text
        assert f"`{spec.exposed_server_name}`" in text
    assert "/home/chakwong" not in text


def test_mcp_readme_documents_deprecated_replacements():
    text = (ROOT / "mcp" / "README.md").read_text(encoding="utf-8")

    for spec in MCP_TOOL_SPECS:
        if spec.deprecated:
            assert spec.replacement is not None
            assert f"`{spec.name}`" in text
            assert f"`{spec.replacement}`" in text


def test_primary_docs_use_preferred_mcp_names():
    docs = [
        ROOT / "README.md",
        ROOT / "mcp" / "README.md",
        ROOT / "docs" / "mathdevmcp-operator-guide.md",
        ROOT / "docs" / "mathdevmcp-release-report.tex",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs)

    for name in ["latex_label_lookup", "check_equality", "audit_implementation_label", "lean_check"]:
        assert f"`{name}`" in combined or f"\\path{{{name}}}" in combined
    assert "paragraph_context=true" not in combined


def test_release_report_active_tool_examples_use_preferred_mcp_names():
    text = (ROOT / "docs" / "mathdevmcp-release-report.tex").read_text(encoding="utf-8")

    assert "Tool: audit_implementation_label" in text
    assert "Tool: compare_label_code" not in text
    assert "Tool: extract_latex_neighborhood" not in text


def test_mcp_unexpected_exception_returns_stable_error(monkeypatch):
    def broken_handler(_args):
        raise RuntimeError("private path /home/chakwong/secret leaked by exception")

    monkeypatch.setitem(TOOL_HANDLERS, "doctor", broken_handler)

    result = call_mcp_tool("doctor", {})

    assert result["ok"] is False
    assert result["error"] == {"type": "tool_execution_error", "message": "MathDevMCP tool failed during execution: doctor"}
    assert result["metadata"] == {"schema_version": "1.0", "contract": "error"}
    assert result["diagnostics"]["exception_type"] == "RuntimeError"
    assert "/home/chakwong/secret" not in str(result)


def test_mcp_error_diagnostics_tolerate_invalid_path_like_input(monkeypatch):
    def broken_handler(_args):
        raise RuntimeError("boom")

    monkeypatch.setitem(TOOL_HANDLERS, "doctor", broken_handler)

    result = call_mcp_tool("doctor", {"code": "bad\x00path.py"})

    assert result["ok"] is False
    assert result["error"]["type"] == "tool_execution_error"
    assert result["diagnostics"]["input_summary"]["code"]["looks_like_path"] is True
    assert result["diagnostics"]["input_summary"]["code"]["exists"] is False
