from mathdevmcp.derivation_branch_controller import branch_expansion_records, can_derive_with_budget, rank_repair_branches


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "path": "/python", "version": "1.14.0"},
    "sage": {"available": False, "status": "unavailable"},
    "lean": {"available": False, "status": "unavailable"},
}

UNAVAILABLE_CAPABILITIES = {
    "sympy": {"available": False, "status": "unavailable"},
    "sage": {"available": False, "status": "unavailable"},
    "lean": {"available": False, "status": "unavailable"},
}

INTEGRATIONS = {
    "leansearchv2": {"resolved_available": False, "resolved_version_status": "missing"},
    "lean_explore": {"resolved_available": False, "resolved_version_status": "missing"},
    "jixia": {"resolved_available": False, "resolved_version_status": "missing"},
    "pantograph": {"resolved_available": False, "resolved_version_status": "missing"},
    "lean_dojo": {"resolved_available": False, "resolved_version_status": "missing"},
}


def test_controller_promotes_proved_only_from_certifying_attempt() -> None:
    calls = []

    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        calls.append(("algebra", backend))
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

    assert tree["metadata"]["contract"] == "derivation_search_tree_result"
    assert tree["status"] == "proved"
    assert tree["root"]["backend_attempts"][0]["evidence_kind"] == "certifying_backend"
    assert tree["controller"]["promotion"]["can_promote"] is True
    assert calls == [("algebra", "sympy")]


def test_controller_promotes_refuted_from_counterexample_after_diagnostic_algebra() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve the target.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    def counterexample(lhs, rhs):
        return {
            "status": "refuted",
            "reason": "Concrete matrix counterexample found.",
            "backend": "bounded_matrix_probe",
            "counterexample": {"assignments": {"A": [[1, 1], [0, 1]], "B": [[1, 0], [1, 1]]}},
            "metadata": {"schema_version": "1.0", "contract": "counterexample_search_result"},
        }

    tree = can_derive_with_budget(
        "A*B = B*A",
        budget_profile="standard",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        counterexample_runner=counterexample,
    )

    assert tree["status"] == "refuted"
    assert [attempt["evidence_kind"] for attempt in tree["root"]["backend_attempts"]] == ["diagnostic", "counterexample"]
    assert tree["controller"]["attempts_used"] == 2
    assert tree["controller"]["promotion"]["supported_status"] == "refuted"


def test_controller_does_not_run_when_external_tool_gate_is_blocked() -> None:
    calls = []

    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        calls.append("algebra")
        return {"status": "proved", "reason": "should not run"}

    tree = can_derive_with_budget(
        "x + 1 = 1 + x",
        capabilities=UNAVAILABLE_CAPABILITIES,
        integrations={},
        algebra_runner=algebra,
    )

    assert tree["status"] == "blocked"
    assert calls == []
    assert tree["root"]["backend_attempts"] == []
    assert tree["controller"]["reason"].startswith("External-tool-first gate is blocked")


def test_controller_budget_exhaustion_preserves_exhausted_actions_and_attempts() -> None:
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

    assert tree["status"] == "budget_exhausted"
    assert tree["controller"]["attempts_used"] == 1
    assert "counterexample_search" in tree["controller"]["exhausted_actions"]
    assert "retrieval" in tree["controller"]["exhausted_actions"]
    assert any(blocker["kind"] == "budget_exhausted" for blocker in tree["root"]["blockers"])
    assert tree["summary"]["backend_attempt_count"] == 1


def test_controller_records_lean_source_required_blocker_without_proof_claim() -> None:
    capabilities = dict(CAPABILITIES)
    capabilities["lean"] = {"available": True, "status": "available", "version": "test"}

    tree = can_derive_with_budget(
        "theorem t : True := by trivial",
        capabilities=capabilities,
        integrations=INTEGRATIONS,
        max_attempts=0,
    )

    assert tree["status"] == "budget_exhausted"
    assert any(blocker["kind"] == "formalization_required" for blocker in tree["root"]["blockers"])
    assert tree["controller"]["promotion"]["can_promote"] is False


def test_controller_runs_lean_check_when_source_supplied() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve Lean source.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    def lean(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "verified",
            "reason": "Lean accepted the source without placeholders.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    tree = can_derive_with_budget(
        "True",
        lean_source="example : True := by trivial",
        budget_profile="standard",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        lean_runner=lean,
    )

    assert tree["status"] == "proved"
    assert [attempt["tool"] for attempt in tree["root"]["backend_attempts"]] == ["sympy", "lean"]
    assert tree["root"]["backend_attempts"][-1]["evidence_kind"] == "lean_check"


def test_controller_rejects_unrelated_lean_source_as_certifying_evidence() -> None:
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

    assert tree["status"] != "proved"
    assert [attempt["tool"] for attempt in tree["root"]["backend_attempts"]] == ["sympy", "sympy_finite_domain"]
    assert any(blocker["id"] == "blocker_lean_source_target_binding_required" for blocker in tree["root"]["blockers"])


def test_controller_counterexample_runs_before_lean_when_both_are_available() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve the target.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    def counterexample(lhs, rhs):
        return {
            "status": "refuted",
            "reason": "Concrete counterexample found.",
            "backend": "bounded_matrix_probe",
            "counterexample": {"assignments": {"A": [[1, 1], [0, 1]], "B": [[1, 0], [1, 1]]}},
            "metadata": {"schema_version": "1.0", "contract": "counterexample_search_result"},
        }

    def lean(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "verified",
            "reason": "Lean accepted source.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    tree = can_derive_with_budget(
        "A*B = B*A",
        lean_source="theorem target : A*B = B*A := by sorry",
        max_attempts=2,
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        counterexample_runner=counterexample,
        lean_runner=lean,
    )

    assert tree["status"] == "refuted"
    assert [attempt["tool"] for attempt in tree["root"]["backend_attempts"]] == ["sympy", "bounded_matrix_probe"]
    assert "lean_check" not in [action["kind"] for action in tree["controller"]["actions"]]


def test_controller_adapter_error_becomes_diagnostic_blocker() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        raise RuntimeError("adapter failure")

    tree = can_derive_with_budget(
        "x = x",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
    )

    assert tree["status"] == "budget_exhausted"
    assert tree["root"]["backend_attempts"][0]["status"] == "adapter_error"
    assert any("adapter failure" in blocker["why"] for blocker in tree["root"]["blockers"])


def test_controller_catches_adapter_action_exceptions() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve the target.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    def bad_counterexample(lhs, rhs):
        raise ValueError("malformed adapter output")

    tree = can_derive_with_budget(
        "A*B = B*A",
        max_attempts=2,
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        counterexample_runner=bad_counterexample,
    )

    assert tree["root"]["backend_attempts"][-1]["status"] == "adapter_error"
    assert any("malformed adapter output" in blocker["why"] for blocker in tree["root"]["blockers"])


def test_rank_repair_branches_prefers_certified_then_specific_blocked_branch() -> None:
    certified = {
        "id": "branch_certified",
        "status": "scoped_target_proved_not_document_proof",
        "assumptions": ["x is a scalar."],
        "closes_obligations": ["algebra_identity"],
        "backend_attempts": [
            {
                "id": "sympy_cert",
                "tool": "sympy",
                "status": "proved",
                "evidence_kind": "certifying_backend",
                "certification_status": "certified",
                "input_summary": "x + 1 = 1 + x",
                "output_ref": "artifact://sympy/sympy_cert.json",
            }
        ],
        "backend_evidence": {
            "promotion": {
                "can_promote": True,
                "supported_status": "proved",
                "errors": [],
                "evidence_refs": ["sympy_cert"],
            }
        },
    }
    blocked = {
        "id": "branch_blocked",
        "status": "blocked_before_backend_certification",
        "assumptions": [
            "Conditional law is defined.",
            "Terms are integrable.",
            "Differentiation interchanges with expectation.",
        ],
        "closes_obligations": ["conditional_expectation_well_defined"],
        "backend_attempts": [{"id": "sympy_diag", "tool": "sympy", "status": "missing_assumptions", "evidence_kind": "diagnostic", "certification_status": "diagnostic"}],
        "translation_blockers": [
            {
                "id": "blocker_conditional_law",
                "kind": "conditional_law_translation_required",
                "problem": "Conditional law missing.",
                "why": "Expectation requires a law.",
                "required_next_evidence": "State a kernel.",
            },
            {
                "id": "blocker_interchange",
                "kind": "derivative_expectation_interchange_required",
                "problem": "Interchange missing.",
                "why": "Derivative under expectation needs a theorem.",
                "required_next_evidence": "State dominated convergence or finite state route.",
            },
        ],
    }

    ranking = rank_repair_branches([blocked, certified])

    assert ranking["metadata"]["contract"] == "repair_branch_ranking_result"
    assert ranking["top_branch_id"] == "branch_certified"
    assert ranking["rankings"][0]["outcome"] == "scoped_proved"
    assert ranking["rankings"][1]["outcome"] == "blocked_with_specific_next_evidence"
    assert ranking["rankings"][1]["score_components"]["specific_blocker_count"] == 2
    assert "not MCTS" in ranking["boundary"]


def test_branch_expansion_records_include_assumptions_attempts_and_blockers() -> None:
    branch = {
        "id": "branch_demo",
        "assumptions": ["A is square."],
        "derivation_route_under_assumptions": [{"step": "Check shape", "detail": "Verify conformability."}],
        "translation_attempts": [{"backend": "sage", "status": "blocked_before_execution", "blocker_ids": ["blocker_shape"], "reason": "Needs shape."}],
        "backend_attempts": [{"id": "sympy_diag", "tool": "sympy", "status": "unknown", "evidence_kind": "diagnostic", "certification_status": "diagnostic"}],
        "translation_blockers": [{"id": "blocker_shape", "kind": "missing_domain_or_shape_required", "problem": "Shape missing."}],
    }

    records = branch_expansion_records(branch)
    kinds = {record["kind"] for record in records}

    assert {"assumption_addition", "derivation_split", "formalization_route", "backend_attempt", "blocker"} <= kinds
    assert all("boundary" in record for record in records)
