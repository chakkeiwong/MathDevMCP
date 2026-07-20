from pathlib import Path
import subprocess
import sys

from mathdevmcp.ast_operation_graph import build_ast_operation_graph, build_ast_operation_graph_for_file
from mathdevmcp.governance import governance_policy
from mathdevmcp.numeric_runner import run_numeric_diagnostic_plan
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label
from mathdevmcp.release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from mathdevmcp.release_policy import release_readiness_report
from mathdevmcp.semantic_alignment import align_document_to_code
from mathdevmcp.shape_semantics import analyze_shape_semantics


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_release_corpus_manifest_covers_required_domains_without_private_roots():
    report = validate_release_corpus_manifest(FIXTURES)
    manifest = release_corpus_manifest(FIXTURES)

    domains = {entry["domain"] for entry in manifest["entries"]}
    private_entries = [entry for entry in manifest["entries"] if entry["privacy_class"] == "private_external"]

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_corpus_validation_report"}
    assert report["status"] == "consistent"
    assert {"kalman_state_space", "hmc_nuts", "particle_filter", "macro_filter_state_space", "dsge_macro_finance", "ml_llm_objective"}.issubset(domains)
    assert private_entries
    assert all(entry["document_root"] is None for entry in private_entries)
    assert all(entry["expected_abstentions"] or entry["seeded_false_confidence_cases"] for entry in manifest["entries"])
    assert manifest["private_paths_redacted"] is True


def test_run_numeric_diagnostic_plan_executes_safe_artifacts_and_rejects_unsafe_imports():
    logdet = run_numeric_diagnostic_plan(
        {"kind": "logdet_domain_check", "artifact": {"matrix": [[2.0, 0.0], [0.0, 5.0]]}}
    )
    not_spd = run_numeric_diagnostic_plan(
        {"kind": "logdet_domain_check", "artifact": {"matrix": [[1.0, 2.0], [2.0, 1.0]]}}
    )
    unsafe = run_numeric_diagnostic_plan(
        {
            "kind": "finite_difference_gradient_check",
            "artifact": {"module_path": str(ROOT / "src" / "mathdevmcp" / "numeric_runner.py")},
        },
        allow_fixture_imports=True,
    )
    too_large = run_numeric_diagnostic_plan(
        {
            "kind": "linear_solve_residual_check",
            "artifact": {"matrix": [[1.0] * 9 for _ in range(9)], "vector": [1.0] * 9},
            "max_matrix_size": 8,
            "timeout_seconds": 0.5,
        }
    )

    assert logdet["metadata"] == {"schema_version": "1.0", "contract": "numeric_diagnostic_plan_result"}
    assert logdet["status"] == "verified"
    assert logdet["safety"]["executes_latex_generated_code"] is False
    assert logdet["safety"]["timeout_seconds"] == 1.0
    assert not_spd["status"] == "mismatch"
    assert unsafe["status"] == "inconclusive"
    assert unsafe["results"][0]["evidence"]["module_path"].endswith("numeric_runner.py")
    assert too_large["status"] == "inconclusive"
    assert too_large["safety"]["timeout_seconds"] == 0.5


def test_proof_audit_v2_attaches_executed_numeric_diagnostics_without_verification_upgrade():
    result = audit_derivation_v2_for_label(
        str(FIXTURES),
        "eq:dept-state-space-likelihood",
        numeric_artifacts={
            "logdet_domain_check": {"matrix": [[2.0, 0.0], [0.0, 3.0]]},
            "linear_solve_residual_check": {"matrix": [[2.0, 0.0], [0.0, 4.0]], "vector": [2.0, 8.0]},
        },
    )

    obligation = result["obligations"][0]
    executed = obligation["numeric_diagnostics"]["executed"]

    assert result["status"] == "unverified"
    assert len(executed) == 2
    assert {item["status"] for item in executed} == {"verified"}
    assert obligation["status"] == "unverified"


def test_shape_semantics_reports_batch_broadcasting_and_spd_guard_risks():
    graph = build_ast_operation_graph(
        """
def batched_solve(xs, A, b):
    ys = vmap(lambda z: A @ z)(xs)
    return solve(A, b) + ys
"""
    )

    report = analyze_shape_semantics(graph, require_batch_policy=True, require_broadcasting_policy=True)

    missing = {item["kind"] for item in report["missing_policies"]}
    assert report["metadata"] == {"schema_version": "1.0", "contract": "shape_semantic_report"}
    assert report["status"] == "unverified"
    assert {"batch_axis_policy_required", "broadcasting_policy_required", "invertibility_or_spd_guard_required"}.issubset(missing)


def test_semantic_alignment_reports_required_operation_gap_and_supporting_case():
    audit = audit_derivation_v2_for_label(str(FIXTURES), "eq:dept-state-space-likelihood")
    good_graph = build_ast_operation_graph_for_file(FIXTURES / "doc_department_state_space_jax.py")
    bad_graph = build_ast_operation_graph_for_file(FIXTURES / "doc_department_state_space_missing_solve.py")

    good = align_document_to_code(audit, good_graph, required_operations=["logdet", "inverse_or_solve", "quadratic_form"])
    bad = align_document_to_code(audit, bad_graph, required_operations=["logdet", "inverse_or_solve", "quadratic_form"])

    assert good["metadata"] == {"schema_version": "1.0", "contract": "semantic_alignment_report"}
    assert good["status"] in {"consistent", "unverified"}
    assert bad["status"] == "mismatch"
    assert any(item["kind"] == "required_operation_missing" and "inverse_or_solve" in item["reason"] for item in bad["findings"])


def test_governance_policy_records_verified_claim_and_private_corpus_rules():
    policy = governance_policy()
    payload = policy["policy"]

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "governance_policy"}
    assert payload["private_corpus_policy"]["no_private_documents_in_git"] is True
    assert payload["external_command_policy"]["timeout_required"] is True
    assert payload["verified_claim_policy"]["requires_deterministic_backend_evidence"] is True
    assert payload["artifact_policy"]["generated_lean_skeletons_are_not_certificates"] is True


def test_release_readiness_report_contains_non_recursive_gate_and_caveats():
    result = release_readiness_report(ROOT)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert result["status"] in {"ready", "ready_with_caveats"}
    assert result["benchmark_gate"]["passed"] is True
    benchmark_categories = result["benchmark_gate"]["summary"]["by_category"]
    assert "release_policy" not in benchmark_categories
    assert result["benchmark_gate"]["total"] == sum(
        item["total"] for item in benchmark_categories.values()
    )
    assert result["parser_policy"]["status"] == "selected_for_proof_audit"
    assert result["governance_policy"]["metadata"]["contract"] == "governance_policy"
    assert result["governance_validation"]["status"] == "consistent"
    assert result["release_corpus_validation"]["status"] == "consistent"
    assert isinstance(result["dirty_worktree"], bool)
    assert result["schema_version"] == "1.0"


def test_release_cli_fails_closed_for_caveated_current_readiness():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "release-readiness",
            "--root",
            str(ROOT),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 1
    assert '"contract": "release_readiness_report"' in result.stdout
    assert '"dirty_worktree"' in result.stdout
