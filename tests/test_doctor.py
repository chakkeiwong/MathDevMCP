import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp.contracts import validate_contract_payload
from mathdevmcp.doctor import doctor_report
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import doctor as server_doctor


ROOT = Path(__file__).resolve().parent.parent


def test_doctor_report_returns_backend_capabilities():
    result = doctor_report()

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "doctor_report"}
    assert validate_contract_payload(result) == []
    assert result["python"]["executable"]
    for name in ["latexml", "pandoc", "lean", "sage", "lean_dojo", "sympy"]:
        assert name in result["capabilities"]
        assert "available" in result["capabilities"][name]
        assert "status" in result["capabilities"][name]


def test_doctor_report_detects_available_core_tools():
    result = doctor_report()

    assert result["capabilities"]["latexml"]["available"] is True
    assert result["capabilities"]["pandoc"]["available"] is True
    assert result["capabilities"]["lean"]["available"] is True
    assert result["capabilities"]["lean_dojo"]["available"] is True


def test_mcp_facade_exposes_doctor():
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool("doctor", {})

    assert "doctor" in names
    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "doctor_report"}


def test_mcp_server_doctor_delegates():
    result = server_doctor()

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "doctor_report"}


def test_cli_doctor_reports_json_contract():
    result = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "doctor"],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "doctor_report"}
    assert payload["capabilities"]["pandoc"]["available"] is True
