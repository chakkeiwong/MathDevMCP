import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from mathdevmcp.contracts import validate_contract_payload
from mathdevmcp.doctor import doctor_report
from mathdevmcp.integration_versions import supported_integration_manifest
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
    for name in ["sympy", "mcp", "lean_dojo", "lean_explore", "pantograph", "leansearchv2", "jixia"]:
        assert name in result["integrations"]
        assert "supported_version" in result["integrations"][name]
        assert "version_status" in result["integrations"][name]
        assert "install_hint" in result["integrations"][name]
        assert "resolved_available" in result["integrations"][name]
        assert "resolved_scope" in result["integrations"][name]


def test_doctor_report_detects_available_core_tools():
    result = doctor_report()

    assert result["capabilities"]["pandoc"]["available"] is True
    optional = ["latexml", "lean", "lean_dojo"]
    missing = [name for name in optional if not result["capabilities"][name]["available"]]
    if missing:
        pytest.skip(f"optional backend tools unavailable: {', '.join(missing)}")
    for name in optional:
        assert result["capabilities"][name]["available"] is True


def test_doctor_uses_requested_backend_python_without_main_env_fallback(monkeypatch, tmp_path):
    fake_python = tmp_path / "python"
    fake_python.write_text(
        "#!/usr/bin/env sh\n"
        "exit 2\n",
        encoding="utf-8",
    )
    fake_python.chmod(0o755)
    monkeypatch.setenv("MATHDEVMCP_BACKEND_PYTHON", str(fake_python))

    result = doctor_report()

    assert result["capabilities"]["lean_dojo"]["available"] is False
    assert result["capabilities"]["lean_dojo"]["path"] == str(fake_python)
    assert result["capabilities"]["lean_dojo"]["detail"] == "Python module lean_dojo is not importable in backend env"
    assert result["capabilities"]["lean_dojo"]["environment_scope"] == "backend_python"
    assert result["capabilities"]["lean_dojo"]["backend_requested"] is True


def test_doctor_resolves_jixia_from_explicit_executable(monkeypatch, tmp_path):
    fake_jixia = tmp_path / "jixia"
    fake_jixia.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
    fake_jixia.chmod(0o755)
    monkeypatch.setenv("MATHDEVMCP_JIXIA_PATH", str(fake_jixia))

    result = doctor_report()
    jixia = result["integrations"]["jixia"]

    assert jixia["available"] is True
    assert jixia["path"] == str(fake_jixia)
    assert jixia["resolved_available"] is True
    assert jixia["resolved_scope"] == "executable"
    assert jixia["detail"] == "executable exists"


def test_doctor_unselected_leandojo_reports_active_python_and_backend_hint(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_BACKEND_CONDA_ENV", raising=False)
    monkeypatch.delenv("MATHDEVMCP_BACKEND_PREFIX", raising=False)
    monkeypatch.delenv("MATHDEVMCP_BACKEND_PYTHON", raising=False)
    real_find_spec = importlib.util.find_spec

    def fake_find_spec(module: str, package: str | None = None):
        if module == "lean_dojo":
            return None
        return real_find_spec(module, package)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    result = doctor_report()
    lean_dojo = result["capabilities"]["lean_dojo"]

    assert lean_dojo["available"] is False
    assert lean_dojo["environment_scope"] == "active_python"
    assert lean_dojo["backend_requested"] is False
    assert "active Python" in lean_dojo["detail"]
    assert "MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends" in lean_dojo["diagnostic_hint"]


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
    assert payload["integrations"]["lean_explore"]["supported_version"] == "1.2.1"


def test_supported_integration_manifest_records_versioned_optional_tools():
    manifest = supported_integration_manifest()

    assert manifest["schema_version"] == "1.0"
    assert manifest["contract"] == "integration_version_manifest"
    tools = {tool["name"]: tool for tool in manifest["tools"]}
    assert tools["lean_explore"]["supported_version"] == "1.2.1"
    assert tools["pantograph"]["supported_version"] == "0.3.15"
    assert tools["leansearchv2"]["git_commit"] == "94f4888cbaf9"
    assert tools["jixia"]["lean_toolchain"] == "leanprover/lean4:v4.29.0"
