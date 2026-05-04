from pathlib import Path
import subprocess
import sys

from mathdevmcp.leandojo_backend import attempt_leandojo_tiny_theorem
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_derivation_v2_label
from mathdevmcp.numeric_runner import check_finite_difference_gradient, check_logdet_domain, check_solve_residual
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_proof_audit_v2_scalar_verified_includes_release_spine_evidence():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:proof-audit-single")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_v2_result"}
    assert result["status"] == "verified"
    assert result["counts"]["verified"] == 1
    obligation = result["obligations"][0]
    assert obligation["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_v2_obligation"}
    assert obligation["substatus"] == "verified:deterministic_backend"
    assert result["substatus_counts"]["verified:deterministic_backend"] == 1
    assert obligation["route_decision"]["route"] == "symbolic"
    assert obligation["typed_diagnostic"]["metadata"]["contract"] == "typed_math_obligation_diagnostic"
    assert obligation["matrix_ir"]["metadata"]["contract"] == "matrix_ir"
    assert obligation["shape_diagnostic"]["metadata"]["contract"] == "shape_diagnostic_result"
    assert obligation["numeric_diagnostics"]["status"] == "not_applicable"
    assert obligation["backend_attempts"][0]["evidence"]["severity"] == "certifying"


def test_proof_audit_v2_false_claim_is_mismatch_with_refutation_action():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:proof-audit-false")

    assert result["status"] == "mismatch"
    assert result["counts"]["mismatch"] == 1
    assert result["obligations"][0]["substatus"] == "mismatch:likely_formula_error"
    assert any(action["kind"] == "investigate_backend_refutation" for action in result["high_priority_actions"])


def test_proof_audit_v2_state_space_reports_missing_constraints_and_numeric_actions():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:dept-state-space-likelihood")

    assert result["status"] == "unverified"
    obligation = result["obligations"][0]
    assert obligation["route_decision"]["route"] == "human_review"
    assert obligation["substatus"] in {"unverified:missing_shape", "unverified:missing_assumption"}
    assert {item["kind"] for item in obligation["shape_diagnostic"]["missing_constraints"]} >= {"invertibility_required", "square_matrix_required"}
    kinds = {action["kind"] for action in result["high_priority_actions"]}
    assert {"state_or_verify_missing_constraint", "human_formalization_or_review", "logdet_domain_check", "linear_solve_residual_check"}.issubset(kinds)
    assert obligation["status"] != "verified"


def test_proof_audit_v2_summary_only_keeps_compact_obligation_shape():
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:dept-hmc-leapfrog", summary_only=True)

    obligation = result["obligations"][0]
    assert result["status"] == "unverified"
    assert "route" in obligation
    assert "substatus" in obligation
    assert "matrix_ir_status" in obligation
    assert "typed_diagnostic" not in obligation
    assert obligation["metadata"] == {"schema_version": "1.0", "contract": "proof_audit_v2_obligation"}


def test_cli_audit_derivation_v2_label_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-derivation-v2-label",
            "eq:dept-state-space-likelihood",
            "--root",
            str(FIXTURES),
            "--summary-only",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "proof_audit_v2_result"' in result.stdout
    assert '"status": "unverified"' in result.stdout


def test_mcp_facade_and_server_expose_proof_audit_v2():
    names = {tool["name"] for tool in list_mcp_tools()}
    facade = call_mcp_tool(
        "audit_derivation_v2_label",
        {"root": str(FIXTURES), "label": "eq:proof-audit-single", "summary_only": True},
    )
    server = audit_derivation_v2_label(str(FIXTURES), "eq:proof-audit-single", summary_only=True)

    assert "audit_derivation_v2_label" in names
    assert facade["ok"] is True
    assert facade["metadata"]["contract"] == "proof_audit_v2_result"
    assert server["metadata"]["contract"] == "proof_audit_v2_result"
    assert server["status"] == "verified"


def test_numeric_runner_executes_only_explicit_safe_diagnostics():
    logdet = check_logdet_domain([[2.0, 0.0], [0.0, 3.0]])
    not_spd = check_logdet_domain([[1.0, 2.0], [2.0, 1.0]])
    solve = check_solve_residual([[2.0, 0.0], [0.0, 4.0]], [2.0, 8.0])
    grad_bad = check_finite_difference_gradient(lambda x: x * x, lambda x: 3.0 * x, 2.0)
    grad_missing = check_finite_difference_gradient(None, None, 1.0)

    assert logdet["status"] == "verified"
    assert not_spd["status"] == "mismatch"
    assert solve["status"] == "verified"
    assert grad_bad["status"] == "mismatch"
    assert grad_missing["status"] == "inconclusive"
    assert logdet["metadata"] == {"schema_version": "1.0", "contract": "numeric_diagnostic_result"}


def test_leandojo_backend_boundary_stays_inconclusive_without_real_dojo_request():
    result = attempt_leandojo_tiny_theorem(
        lean_source="theorem t : 1 = 1 := rfl\n",
        tactic_script=["rfl"],
        run_dojo=False,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "leandojo_attempt_result"}
    assert result["status"] == "inconclusive"
    assert "direct Lean final check artifact" in result["required_artifacts"]
    assert result["final_lean_check"] is None or result["final_lean_check"]["metadata"]["contract"] == "lean_check_result"


def test_leandojo_backend_boundary_records_configured_target_and_timeout(monkeypatch, tmp_path):
    monkeypatch.setenv("MATHDEVMCP_LEANDOJO_FIXTURE", str(tmp_path))
    monkeypatch.setenv("MATHDEVMCP_LEANDOJO_THEOREM", "MathDevMCP.Tiny")
    monkeypatch.setenv("MATHDEVMCP_LEANDOJO_TIMEOUT_SECONDS", "2")

    result = attempt_leandojo_tiny_theorem(
        lean_source="theorem t : True := by trivial\n",
        tactic_script=["trivial"],
        run_dojo=True,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "leandojo_attempt_result"}
    assert result["status"] == "inconclusive"
    assert result["dojo_requested"] is True
    assert result["timeout_seconds"] == 2.0
    assert result["traced_repo_target"] == {"path": str(tmp_path), "theorem": "MathDevMCP.Tiny"}
    assert result["final_lean_check"] is None or result["final_lean_check"]["metadata"]["contract"] == "lean_check_result"
