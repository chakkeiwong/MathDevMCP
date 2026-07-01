from pathlib import Path
import json
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


def test_cli_workbench_benchmark_quality_module_command_passes():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "workbench-benchmark-quality",
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "workbench_benchmark_quality_report"' in result.stdout
    assert '"status": "quality_thresholds_passed"' in result.stdout


def test_cli_high_level_workflow_commands_return_contract_envelopes():
    derive = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "derive-from",
            "a + b = b + a",
            "--given",
            "a,b are scalars",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    code = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-math-to-code",
            "logdet(S)",
            "def f(S):\n    return logdet(S)\n",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert derive.returncode == 0, derive.stderr
    assert code.returncode == 0, code.stderr
    derive_payload = json.loads(derive.stdout)
    code_payload = json.loads(code.stdout)
    assert derive_payload["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert derive_payload["workflow"] == "derive_from"
    assert "givens_not_formal_assumptions" in {item["code"] for item in derive_payload["non_claims"]}
    assert code_payload["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert code_payload["workflow"] == "audit_math_to_code"
    assert code_payload["certification_source"] == "none"
    assert "structural_evidence_not_proof" in {item["code"] for item in code_payload["non_claims"]}


def test_cli_high_level_workflow_quality_module_command_passes():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "high-level-workflow-quality",
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_quality_report"}
    assert payload["status"] == "quality_thresholds_passed"
    assert payload["total_cases"] == 14


def test_release_smoke_script_passes():
    result = subprocess.run(
        [str(ROOT / "scripts" / "release_smoke.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "doctor_report"' in result.stdout
    assert '"contract": "parser_benchmark_report"' in result.stdout
    assert '"contract": "release_readiness_report"' in result.stdout


def test_release_hypotheses_script_public_mode_passes():
    result = subprocess.run(
        [str(ROOT / "scripts" / "release_hypotheses_check.sh"), str(ROOT), "--public"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "release_hypothesis_check"' in result.stdout
    assert '"publication_invariant"' in result.stdout
