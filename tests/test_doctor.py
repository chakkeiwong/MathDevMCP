import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from mathdevmcp.contracts import validate_contract_payload
from mathdevmcp.doctor import doctor_report


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


def test_cli_doctor_reports_json_contract(requires_pandoc):
    result = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "doctor"],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "doctor_report"}
    assert payload["capabilities"]["pandoc"]["available"] is True
