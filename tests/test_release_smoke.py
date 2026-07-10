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


def test_cli_prepare_review_packet_preserves_phase6_packet_fields(tmp_path):
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

    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(f"[{derive.stdout}, {code.stdout}]", encoding="utf-8")
    packet = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "prepare-review-packet",
            "Review CLI packet",
            "--evidence",
            str(evidence_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert packet.returncode == 0, packet.stderr
    payload = json.loads(packet.stdout)
    low_level = payload["evidence"][0]["low_level"]
    assert payload["status"] == "diagnostic_only"
    assert payload["certification_source"] == "none"
    assert low_level["backend_checks"]
    assert low_level["agent_handoff"]["scoped_question"] == "Review CLI packet"
    assert low_level["agent_handoff"]["evidence_ledger"]
    assert low_level["agent_handoff"]["non_claim_boundary"]
    assert payload["agent_handoff"] == low_level["agent_handoff"]
    assert low_level["nested_evidence_summary"]
    assert low_level["route_plans"]
    assert low_level["trace_maps"]
    assert low_level["decision_criteria"]
    assert any(item["code"] == "diagnostic_route_and_trace_context_not_proof" for item in low_level["non_claims"])

    handoff_packet = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "prepare-review-packet",
            "Review CLI packet",
            "--evidence",
            str(evidence_path),
            "--handoff",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert handoff_packet.returncode == 0, handoff_packet.stderr
    handoff = json.loads(handoff_packet.stdout)
    assert handoff["scoped_question"] == "Review CLI packet"
    assert handoff["evidence_ledger"]
    assert handoff["non_claim_boundary"]
    assert "not a proof certificate" in handoff["certification_boundary"]
    assert "metadata" not in handoff


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


def test_cli_external_tool_first_plan_returns_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "external-tool-first-plan",
            "a + b = b + a",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "external_tool_first_plan_result"}
    assert payload["considered_tools"]
    assert "external_tool_plan_not_certificate" in {item["code"] for item in payload["non_claims"]}


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
