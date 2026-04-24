from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def test_benchmark_gate_smoke_script_passes():
    result = subprocess.run(
        [str(ROOT / "scripts" / "benchmark_gate_smoke.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "benchmark_gate"' in result.stdout
    assert '"passed": true' in result.stdout


def test_cli_benchmark_gate_module_command_passes():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "benchmark-gate",
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"failed_count": 0' in result.stdout
    assert '"name": "all_benchmarks_must_pass"' in result.stdout
