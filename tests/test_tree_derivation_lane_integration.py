from mathdevmcp.derivation_branch_controller import can_derive_with_budget
from mathdevmcp.derivation_tree_report import render_derivation_tree_report


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "version": "1.14.0"},
    "sage": {"available": False, "status": "unavailable"},
    "lean": {"available": False, "status": "unavailable"},
}

INTEGRATIONS = {
    "leansearchv2": {"resolved_available": False},
    "lean_explore": {"resolved_available": False},
    "jixia": {"resolved_available": False},
    "pantograph": {"resolved_available": False},
    "lean_dojo": {"resolved_available": False},
}


def test_tree_derivation_lane_proved_report_names_tool_and_promotion_guard() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "proved",
            "reason": "Scoped symbolic backend certified the equality.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    tree = can_derive_with_budget(
        "a + b = b + a",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
    )
    report = render_derivation_tree_report(tree)
    markdown = report["markdown"]

    assert tree["status"] == "proved"
    assert report["sections"][0]["promotion"]["can_promote"] is True
    assert "`sympy_algebra_attempt`" in markdown
    assert "can_promote=True" in markdown
    assert "`tree_report_not_patch_or_proof`" in markdown


def test_tree_derivation_lane_budget_report_preserves_blockers_and_no_fake_patch() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve the target.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    tree = can_derive_with_budget(
        "x + 1 = 1 + x",
        max_attempts=1,
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        retrieval_hits={"leansearchv2": [{"name": "Nat.add_comm"}]},
    )
    report = render_derivation_tree_report(tree)
    markdown = report["markdown"]

    assert tree["status"] == "budget_exhausted"
    assert any(blocker["kind"] == "budget_exhausted" for blocker in tree["root"]["blockers"])
    assert report["sections"][0]["proposed_patches"] == []
    assert "No patch candidate supplied by the tree." in markdown
    assert "budget_exhausted" in markdown
    assert "counterexample_search" in tree["controller"]["exhausted_actions"]
    assert "retrieval" in tree["controller"]["exhausted_actions"]


def test_tree_derivation_lane_unrelated_lean_source_does_not_prove_report() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve the target.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    def lean(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "verified",
            "reason": "Lean accepted unrelated source.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    tree = can_derive_with_budget(
        "x + 1 = 1 + x",
        lean_source="example : True := by trivial",
        budget_profile="standard",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        lean_runner=lean,
    )
    report = render_derivation_tree_report(tree)
    markdown = report["markdown"]

    assert tree["status"] != "proved"
    assert "blocker_lean_source_target_binding_required" in markdown
    assert "can_promote=False" in markdown
    assert "Lean source was supplied without an exact valid branch-target binding" in markdown
