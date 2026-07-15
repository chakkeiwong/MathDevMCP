import hashlib

from mathdevmcp.derivation_branch_controller import branch_expansion_records, can_derive_with_budget, rank_repair_branches
from mathdevmcp.external_tool_adapters import EvidenceContext


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


def test_controller_requires_explicit_binding_before_lean_action() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "unknown",
            "reason": "Algebra backend did not resolve Lean source.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    lean_calls = []

    def lean(source, *, timeout_seconds=10, allow_sorry=False):
        lean_calls.append(source)
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

    assert tree["status"] == "partial"
    assert [attempt["tool"] for attempt in tree["root"]["backend_attempts"]] == ["sympy"]
    assert lean_calls == []
    assert any(
        blocker["id"] == "blocker_lean_source_target_binding_required"
        for blocker in tree["root"]["blockers"]
    )


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


def test_rank_repair_branches_uses_validity_gated_partial_order_without_scores() -> None:
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
    assert ranking["nondominated_branch_ids"] == ["branch_certified"]
    assert ranking["rankings"][0]["nondominated"] is True
    assert ranking["rankings"][1]["outcome"] == "blocked_with_specific_next_evidence"
    assert ranking["ledgers"]["deduplicated_entries"]
    assert all(item["ledger_entry_ids"] for item in ranking["rankings"])
    assert all("ledgers" not in item for item in ranking["rankings"])
    assert ranking["selected_action"]["branch_ids"] == ["branch_certified"]
    selected_entry_id = ranking["selected_action"]["ledger_entry_ids"][0]
    selected_entry = next(
        entry
        for entry in ranking["ledgers"]["deduplicated_entries"]
        if entry["entry_id"] == selected_entry_id
    )
    assert selected_entry["scope"]["branch_ids"] == ["branch_certified"]
    assert ranking["selected_action"]["action_kind"] == "repair_evidence_integrity"
    assert all("score" not in item and "score_components" not in item for item in ranking["rankings"])
    assert ranking["serialization_order_authority"] == "diagnostic_only"
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


def test_controller_records_compact_verified_attachment_only_with_explicit_context_and_root(tmp_path) -> None:
    target = "x + 1 = 1 + x"
    source = target.encode()
    context = EvidenceContext(
        source_logical_id="synthetic/source.tex",
        source_file="synthetic/source.tex",
        source_label="eq:test",
        source_bytes=source,
        source_spans=({"start_byte": 0, "end_byte": len(source)},),
        parser_version="synthetic-1",
        obligation_digest=hashlib.sha256(target.encode()).hexdigest(),
        normalized_target=target,
        branch_id="root",
        branch_lineage=("root",),
        typed_assumptions=({"id": "scalar", "kind": "domain", "statement": "x is real."},),
        native_input_bytes=target.encode(),
        native_input_media_type="text/plain",
        tool_name="sympy",
        adapter_version="p01-test",
        backend_version="fake",
        executable_id="fake_runner",
        timeout_ms=1000,
        max_output_bytes=4096,
        expected_result_class="synthetic_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=(
            "no_real_document_extraction",
            "no_backend_conformance",
            "no_mathematical_certification",
            "no_branch_local_scheduler",
            "no_publication_eligibility",
            "no_source_document_edit",
            "no_multiprocess_support",
            "no_release_readiness",
        ),
        policy_version="p01-test",
    )

    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {"status": "proved", "reason": "Synthetic fake-runner result."}

    tree = can_derive_with_budget(
        target,
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
        algebra_runner=algebra,
        evidence_contexts={"algebra_check": context},
        artifact_root=tmp_path / "evidence",
    )
    attachment = tree["root"]["evidence_attachments"][0]
    attempt = tree["root"]["backend_attempts"][0]
    assert attachment["integrity_state"] == "verified"
    assert attachment["claim_eligibility"] == "ineligible"
    assert attachment["publication_enabled"] is False
    assert attempt["evidence_schema_version"] == "1.0"
    assert tree["controller"]["validation_errors"] == []
