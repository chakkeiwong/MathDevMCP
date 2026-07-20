import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_security_scan_records_unavailable_tools_without_passing_them(tmp_path: Path) -> None:
    output = tmp_path / "security.json"
    result = subprocess.run(
        [str(ROOT / "scripts" / "security_scan.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHON_BIN": "/usr/bin/python3", "MATHDEVMCP_SECURITY_ARTIFACT": str(output)},
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["scope"] == "engineering_supply_chain_only"
    assert all(item["status"] == "not_available" for item in report["checks"].values())
    assert report["claims"]["mathematical_correctness"] == "not_evaluated"


def test_security_scan_fails_shell_gate_when_scanner_fails(tmp_path: Path) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    scanner = fake_bin / "pip-audit"
    scanner.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
    scanner.chmod(0o755)
    output = tmp_path / "security.json"
    result = subprocess.run(
        [str(ROOT / "scripts" / "security_scan.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={
            "PATH": f"{fake_bin}:/usr/bin:/bin",
            "PYTHON_BIN": "/usr/bin/python3",
            "MATHDEVMCP_SECURITY_ARTIFACT": str(output),
        },
    )
    assert result.returncode == 1
    assert json.loads(output.read_text(encoding="utf-8"))["checks"]["pip_audit"]["status"] == "failed"
