from dataclasses import replace
import hashlib
import os

import pytest

from mathdevmcp.derivation_search_tree import branch_promotion_report
from mathdevmcp.external_tool_adapters import (
    adapt_lean_check,
    adapt_proof_state_evidence,
    adapt_retrieval_evidence,
    adapt_static_extraction_evidence,
)
from mathdevmcp.lean_check import (
    LeanDiagnosticContext,
    LeanTargetBinding,
    _uses_placeholder,
    lean_execution_matches_binding,
    validate_lean_diagnostic_context,
    validate_lean_target_binding,
)


SOURCE = """import Mathlib

theorem add_comm_bound (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
"""


def _project(tmp_path):
    project = tmp_path / "project"
    project.mkdir(parents=True)
    (project / "lean-toolchain").write_text("leanprover/lean4:v4.29.1\n", encoding="utf-8")
    executable = tmp_path / "lean"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    lean_file = project / "Bound.lean"
    lean_file.write_text(SOURCE, encoding="utf-8")
    return project, executable, lean_file


def _binding(tmp_path, **updates):
    project, executable, _ = _project(tmp_path)
    value = LeanTargetBinding(
        branch_id="root",
        normalized_target="a + b = b + a",
        typed_assumptions=(
            {
                "id": "nat_variables",
                "kind": "domain",
                "lean_binder": "(a b : Nat)",
            },
        ),
        theorem_name="add_comm_bound",
        theorem_binders=("(a b : Nat)",),
        theorem_statement="a + b = b + a",
        imports=("Mathlib",),
        source_sha256=hashlib.sha256(SOURCE.encode()).hexdigest(),
        project_root=str(project),
        lean_toolchain="leanprover/lean4:v4.29.1",
        executable_path=str(executable),
        executable_version="Lean (version 4.29.1)",
    )
    return replace(value, **updates) if updates else value


def _node(attempt):
    return {
        "id": "node",
        "target": "a + b = b + a",
        "status": "proved" if attempt["status"] == "proved" else "partial",
        "backend_attempts": [attempt],
    }


def test_exact_target_binding_is_deterministic_and_noncertifying_by_itself(tmp_path) -> None:
    binding = _binding(tmp_path)
    first = validate_lean_target_binding(SOURCE, binding)
    second = validate_lean_target_binding(SOURCE, binding)
    assert first == second
    assert first["status"] == "bound"
    assert first["can_certify"] is True
    assert first["record"]["binding_digest"] == second["record"]["binding_digest"]
    assert "not a certificate" in first["boundary"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ({"normalized_target": "a + b = a"}, "theorem_statement"),
        ({"theorem_statement": "True"}, "theorem_statement"),
        ({"theorem_name": "other"}, "declaration head"),
        ({"theorem_binders": ("(a : Nat)",)}, "assumption binders"),
        ({"imports": ("Std",)}, "import list"),
        ({"source_sha256": "0" * 64}, "source digest"),
        ({"lean_toolchain": "leanprover/lean4:v4.28.0"}, "lean-toolchain"),
        ({"executable_version": ""}, "executable_version"),
    ],
)
def test_binding_mutations_are_rejected(tmp_path, mutation, message) -> None:
    validation = validate_lean_target_binding(SOURCE, _binding(tmp_path, **mutation))
    assert validation["status"] == "binding_error"
    assert any(message in error for error in validation["errors"])


def test_assumption_mutation_changes_binding_and_is_rejected_if_binder_changes(tmp_path) -> None:
    binding = _binding(tmp_path)
    mutated = replace(
        binding,
        typed_assumptions=(
            {"id": "int_variables", "kind": "domain", "lean_binder": "(a b : Int)"},
        ),
    )
    validation = validate_lean_target_binding(SOURCE, mutated)
    assert validation["can_certify"] is False
    assert "typed assumption binders" in "; ".join(validation["errors"])


def test_changed_source_and_extra_or_commented_theorem_do_not_bind(tmp_path) -> None:
    binding = _binding(tmp_path)
    for source in (
        SOURCE.replace("Nat.add_comm", "Nat.add_comm -- changed"),
        SOURCE + "\ntheorem unrelated : True := by trivial\n",
        "-- theorem add_comm_bound (a b : Nat) : a + b = b + a := by\n"
        "--   exact Nat.add_comm a b\n"
        "def onlyAComment := 1\n",
    ):
        validation = validate_lean_target_binding(source, binding)
        assert validation["can_certify"] is False


@pytest.mark.parametrize(
    "source",
    [
        SOURCE.replace("exact Nat.add_comm a b", "sorry"),
        SOURCE.replace("exact Nat.add_comm a b", "admit"),
        SOURCE.replace("exact Nat.add_comm a b", "exact?"),
        SOURCE.replace("exact Nat.add_comm a b", "simp?"),
    ],
)
def test_reviewed_placeholder_constructs_block_binding(tmp_path, source) -> None:
    binding = replace(_binding(tmp_path), source_sha256=hashlib.sha256(source.encode()).hexdigest())
    validation = validate_lean_target_binding(source, binding)
    assert validation["can_certify"] is False
    assert _uses_placeholder(source) is True


def test_missing_project_toolchain_or_executable_blocks_binding(tmp_path) -> None:
    binding = _binding(tmp_path)
    project = tmp_path / "project"
    (project / "lean-toolchain").unlink()
    assert validate_lean_target_binding(SOURCE, binding)["can_certify"] is False

    (project / "lean-toolchain").write_text(binding.lean_toolchain, encoding="utf-8")
    os.chmod(binding.executable_path, 0o644)
    assert validate_lean_target_binding(SOURCE, binding)["can_certify"] is False


def test_raw_execution_must_match_every_bound_process_field(tmp_path) -> None:
    record = validate_lean_target_binding(SOURCE, _binding(tmp_path))["record"]
    evidence = {
        "kind": "lean_verified",
        "returncode": 0,
        "uses_sorry": False,
        "source_sha256": record["source_sha256"],
        "command": [record["executable_path"], "/tmp/Check.lean"],
        "executable_realpath": record["executable_path"],
        "lean_version": record["executable_version"],
        "project_root": record["project_root"],
        "lean_toolchain": record["lean_toolchain"],
    }
    raw = {"status": "verified", "evidence": [evidence]}
    assert lean_execution_matches_binding(raw, record) is True
    for key, value in (
        ("source_sha256", "0" * 64),
        ("lean_version", "stale"),
        ("project_root", "/tmp/wrong"),
        ("lean_toolchain", "wrong"),
        ("executable_realpath", "/bin/false"),
    ):
        changed = {**evidence, key: value}
        assert lean_execution_matches_binding({"status": "verified", "evidence": [changed]}, record) is False


def test_fake_verified_lean_result_remains_diagnostic_without_live_binding(tmp_path) -> None:
    def fake(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "verified",
            "reason": "Synthetic verified label.",
            "evidence": [],
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check(SOURCE, runner=fake, target_binding=_binding(tmp_path))
    attempt = result["attempt"]
    assert attempt["status"] == "diagnostic"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["live_execution_binding_verified"] is False
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_lean_rejection_is_not_mathematical_refutation() -> None:
    def fake(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "mismatch",
            "reason": "Lean rejected this proof term.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check(SOURCE, runner=fake)
    assert result["attempt"]["status"] == "diagnostic"
    assert result["attempt"]["evidence_kind"] == "diagnostic"
    assert result["attempt"]["certification_status"] == "diagnostic"


def _diagnostic_context(tmp_path):
    project, _, lean_file = _project(tmp_path)
    goal = "a + b = b + a"
    return LeanDiagnosticContext(
        lean_file=str(lean_file),
        source_sha256=hashlib.sha256(SOURCE.encode()).hexdigest(),
        project_root=str(project),
        lean_toolchain="leanprover/lean4:v4.29.1",
        goal=goal,
        goal_digest=hashlib.sha256(goal.encode()).hexdigest(),
    )


def test_diagnostic_context_binds_local_file_project_toolchain_and_goal(tmp_path) -> None:
    context = _diagnostic_context(tmp_path)
    valid = validate_lean_diagnostic_context(context)
    assert valid["can_execute_diagnostic_route"] is True

    stale = replace(context, source_sha256="0" * 64)
    wrong_goal = replace(context, goal_digest="0" * 64)
    assert validate_lean_diagnostic_context(stale)["can_execute_diagnostic_route"] is False
    assert validate_lean_diagnostic_context(wrong_goal)["can_execute_diagnostic_route"] is False


def test_diagnostic_routes_require_context_and_can_never_promote(tmp_path) -> None:
    missing = (
        adapt_retrieval_evidence(tool="leansearchv2", query="goal", hits=[{"name": "h"}]),
        adapt_static_extraction_evidence(tool="jixia", target="Bound.lean", extracted={"x": 1}),
        adapt_proof_state_evidence(tool="pantograph", target="goal", trace=[{"state": "g"}]),
    )
    assert {item["status"] for item in missing} == {"precondition_missing"}
    assert all(item["can_promote"] is False for item in missing)
    assert all(item["attempt"]["output_ref"] is None for item in missing)

    context = _diagnostic_context(tmp_path / "valid")
    allowed = (
        adapt_retrieval_evidence(
            tool="leansearchv2", query="goal", hits=[{"name": "h"}], lean_context=context
        ),
        adapt_static_extraction_evidence(
            tool="jixia", target="Bound.lean", extracted={"x": 1}, lean_context=context
        ),
        adapt_proof_state_evidence(
            tool="pantograph", target="goal", trace=[{"state": "g"}], lean_context=context
        ),
    )
    assert {item["status"] for item in allowed} == {"retrieved", "extracted", "explored"}
    assert all(item["execution_mode"] == "record_only" for item in allowed)
    assert all(item["can_promote"] is False for item in allowed)
