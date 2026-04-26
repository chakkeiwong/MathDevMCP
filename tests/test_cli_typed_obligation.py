from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_cli_typed_obligation_label_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "typed-obligation-label",
            "eq:dept-state-space-likelihood",
            "--root",
            str(FIXTURES),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "typed_obligation_label_diagnostic"' in result.stdout
    assert '"contract": "typed_math_obligation_diagnostic"' in result.stdout
    assert '"status": "unverified"' in result.stdout
