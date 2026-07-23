from pathlib import Path
import json
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def test_mcp_stdio_smoke_initializes_lists_and_calls() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "mcp_stdio_smoke.py"),
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "CUDA_VISIBLE_DEVICES": "-1", "MATHDEVMCP_MCP_PROFILE": "stable"},
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "passed"
    assert report["server_name"] == "MathDevMCP"
    assert report["tool_count"] >= 1
    assert report["doctor_called"] is True


def test_mcp_stdio_smoke_can_explicitly_opt_in_to_all_tools() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "mcp_stdio_smoke.py"),
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "CUDA_VISIBLE_DEVICES": "-1", "MATHDEVMCP_MCP_PROFILE": "all"},
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["profile"] == "all"
    assert report["tool_count"] == 71
