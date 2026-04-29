from pathlib import Path

from mathdevmcp.mcp_facade import MCP_TOOL_SPECS, TOOL_HANDLERS, call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import MCP_SERVER_EXPOSED_TOOLS


ROOT = Path(__file__).resolve().parent.parent


def test_mcp_registry_is_facade_authority():
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}
    listed = {tool["name"] for tool in list_mcp_tools()}

    assert set(TOOL_HANDLERS) == registry_names
    assert listed == registry_names


def test_mcp_server_exposure_matches_registry_aliases():
    server_names = {spec.exposed_server_name for spec in MCP_TOOL_SPECS}

    assert server_names == MCP_SERVER_EXPOSED_TOOLS
    assert "tool_matrix" in {spec.name for spec in MCP_TOOL_SPECS}
    assert "get_tool_matrix" in MCP_SERVER_EXPOSED_TOOLS


def test_mcp_readme_mentions_every_registry_and_server_tool():
    text = (ROOT / "mcp" / "README.md").read_text(encoding="utf-8")

    for spec in MCP_TOOL_SPECS:
        assert f"`{spec.name}`" in text
        assert f"`{spec.exposed_server_name}`" in text
    assert "/home/chakwong" not in text


def test_mcp_unexpected_exception_returns_stable_error(monkeypatch):
    def broken_handler(_args):
        raise RuntimeError("private path /home/chakwong/secret leaked by exception")

    monkeypatch.setitem(TOOL_HANDLERS, "doctor", broken_handler)

    result = call_mcp_tool("doctor", {})

    assert result == {
        "ok": False,
        "error": {"type": "tool_execution_error", "message": "MathDevMCP tool failed during execution: doctor"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }

