from pathlib import Path
import subprocess
import sys

from mathdevmcp.mcp_facade import MCP_TOOL_SPECS, TOOL_HANDLERS, call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import MCP_SERVER_EXPOSED_TOOLS, configure_mcp_profile, mcp_profile_tool_names, mcp


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


def test_mcp_server_exposure_inventory_is_derived_from_registry():
    source = (ROOT / "src" / "mathdevmcp" / "mcp_server.py").read_text(encoding="utf-8")

    assert "MCP_SERVER_EXPOSED_TOOLS = {spec.exposed_server_name for spec in MCP_TOOL_SPECS}" in source


def test_mcp_profile_rejects_unknown_profile():
    import pytest

    with pytest.raises(ValueError, match="Expected stable or all"):
        configure_mcp_profile("experimental")


def test_mcp_profile_catalog_declares_explicit_stable_boundary():
    stable = mcp_profile_tool_names("stable")
    all_tools = mcp_profile_tool_names("all")
    nonstable = all_tools - stable

    assert len(stable) == 23
    assert all_tools == MCP_SERVER_EXPOSED_TOOLS
    assert len(nonstable) == 45
    assert "doctor" in stable


def test_mcp_profile_reconfiguration_cannot_report_a_false_surface():
    # Configuration is process-scoped because FastMCP removal mutates its
    # registry; a different profile requires a fresh stdio process.
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
                "from mathdevmcp import mcp_server as s\n"
                "assert s.configure_mcp_profile('stable') == 'stable'\n"
                "assert len(s.mcp._tool_manager._tools) == 23\n"
                "try:\n"
                "    s.configure_mcp_profile('all')\n"
                "except RuntimeError as exc:\n"
                "    assert 'fresh process' in str(exc)\n"
                "else:\n"
                "    raise AssertionError('profile reconfiguration was accepted')\n",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert probe.returncode == 0


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
    assert resolver_properties["collection"]["enum"] == [
        "global_blocker_records",
        "global_evidence_ref_records",
        "global_source_ref_records",
        "blocker_records",
        "evidence_ref_records",
        "source_ref_records",
        "unresolved_assumption_records",
        "candidate_assumption_records",
        "selected_action",
        "label_scoped_obligation",
        "typed_repair_obligation",
        "math_obligation",
        "source_span",
        "target_text",
    ]
    assert resolver_properties["offset"]["default"] == 0
    assert resolver_properties["limit"]["default"] == 100
    assert resolver.fn_metadata.output_schema is None

    tree_page = mcp._tool_manager._tools["page_resumable_tree_records"]
    assert tree_page.parameters["properties"]["limit"]["default"] == 20
    tree_resolver = mcp._tool_manager._tools["resolve_resumable_tree_record"]
    assert tree_resolver.parameters["properties"]["byte_limit"]["default"] == 16384

    registry = {spec.name: spec for spec in MCP_TOOL_SPECS}
    assert registry["audit_document_derivation_tree"].output_contract == "document_derivation_response"
    assert registry["resolve_document_derivation_records"].output_contract == "document_derivation_record_page"
    assert registry["page_resumable_tree_records"].output_contract == "resumable_document_tree_page"
    assert registry["resolve_resumable_tree_record"].output_contract == "resumable_document_tree_record_resolution"

    audit_fix = mcp._tool_manager._tools["audit_and_propose_fix"]
    assert audit_fix.parameters["properties"]["response_mode"]["enum"] == ["detailed", "compact"]
    rigor = mcp._tool_manager._tools["audit_math_document_rigor"]
    assert rigor.parameters["properties"]["response_mode"]["enum"] == ["detailed", "compact"]
    assert rigor.parameters["properties"]["report_profile"]["enum"] == ["actionable", "forensic"]
    assert rigor.parameters["properties"]["prior_report"]["default"] is None
    assert rigor.parameters["properties"]["revision_manifest"]["default"] is None
    assert rigor.parameters["properties"]["obligation_metadata"]["default"] is None
    review = mcp._tool_manager._tools["prepare_review_packet"]
    assert review.parameters["properties"]["response_mode"]["enum"] == ["detailed", "compact"]


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
