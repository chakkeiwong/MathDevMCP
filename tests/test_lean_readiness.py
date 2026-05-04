import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp.lean_readiness import lean_readiness
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import lean_readiness as server_lean_readiness


ROOT = Path(__file__).resolve().parent.parent


def test_lean_readiness_reports_separate_sections():
    result = lean_readiness(ROOT)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_readiness"}
    assert "direct_lean" in result
    assert "lake_project" in result
    assert "lean_dojo" in result
    assert "not proof" in result["certification_boundary"]


def test_lean_readiness_cli_reports_contract():
    result = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "lean-readiness", "--root", str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["metadata"]["contract"] == "lean_readiness"


def test_lean_readiness_mcp_facade_and_server():
    tools = {tool["name"] for tool in list_mcp_tools()}
    facade = call_mcp_tool("lean_readiness", {"root": str(ROOT)})
    server = server_lean_readiness(str(ROOT))

    assert "lean_readiness" in tools
    assert facade["ok"] is True
    assert facade["metadata"]["contract"] == "lean_readiness"
    assert server["metadata"]["contract"] == "lean_readiness"
