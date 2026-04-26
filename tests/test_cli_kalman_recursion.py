from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_cli_audit_kalman_recursion_reports_missing_covariance_update():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-kalman-recursion",
            str(FIXTURES / "doc_kalman_recursion_bad.py"),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "kalman_recursion_audit"' in result.stdout
    assert '"covariance_update"' in result.stdout
    assert '"status": "mismatch"' in result.stdout
