from copy import deepcopy
import json

import pytest

from mathdevmcp.derivation_search_tree import (
    AssumptionSet,
    BackendAttempt,
    PatchCandidate,
    SourceSpan,
    branch_can_be_promoted,
    branch_promotion_report,
    build_initial_search_tree,
    branch_tree_semantic_digest,
    build_branch_record,
    certifying_backend_attempt,
    counterexample_backend_attempt,
    make_search_node,
    summarize_search_tree,
    transition_branch,
    validate_branch_generator,
    validate_branch_record,
    validate_branch_tree,
    validate_search_tree,
)
from mathdevmcp.external_tool_policy import external_tool_first_plan


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "path": "/python", "version": "1.14.0"},
    "sage": {"available": False, "status": "unavailable", "path": None, "version": None},
    "lean": {"available": False, "status": "unavailable", "path": None, "version": None},
}

UNAVAILABLE_CAPABILITIES = {
    "sympy": {"available": False, "status": "unavailable"},
    "sage": {"available": False, "status": "unavailable"},
    "lean": {"available": False, "status": "unavailable"},
}

INTEGRATIONS = {
    "leansearchv2": {
        "resolved_available": True,
        "resolved_version": "0.1.0",
        "resolved_version_status": "match",
        "resolved_scope": "backend_python",
    },
    "lean_explore": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
    "pantograph": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
    "lean_dojo": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
    "jixia": {
        "resolved_available": False,
        "resolved_version": None,
        "resolved_version_status": "missing",
        "resolved_scope": "unavailable",
    },
}


def test_initial_tree_embeds_external_tool_plan_and_contract() -> None:
    tree = build_initial_search_tree(
        "a + b = b + a",
        source_span=SourceSpan(file="paper.tex", line_start=10, line_end=12, label="eq:test"),
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )

    assert tree["metadata"] == {"schema_version": "1.0", "contract": "derivation_search_tree_result"}
    assert tree["root"]["external_tool_first_plan"]["metadata"]["contract"] == "external_tool_first_plan_result"
    assert tree["root"]["external_tool_first_plan"]["selected_external_tools"][0]["tool"] == "sympy"
    assert tree["root"]["source_span"]["file"] == "paper.tex"
    assert tree["root"]["status"] == "planned"
    assert "search_tree_not_proof" in {item["code"] for item in tree["non_claims"]}
    assert validate_search_tree(tree) == []


def test_initial_tree_serialization_is_deterministic_with_supplied_reports() -> None:
    first = build_initial_search_tree(
        "x + 1 = 1 + x",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )
    second = build_initial_search_tree(
        "x + 1 = 1 + x",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )

    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_missing_external_route_creates_blocker_without_proof_claim() -> None:
    tree = build_initial_search_tree(
        "x + 1 = 1 + x",
        capabilities=UNAVAILABLE_CAPABILITIES,
        integrations={},
    )

    assert tree["status"] == "blocked"
    blocker = tree["root"]["blockers"][0]
    assert blocker["kind"] == "external_tool_or_gap_justification_required"
    assert "external-tool-first policy" in blocker["why"]
    assert tree["summary"]["blocker_count"] == 1
    assert branch_can_be_promoted(tree["root"]) == (False, [])
    assert validate_search_tree(tree) == []


def test_route_retrieval_and_formalization_evidence_do_not_promote_branch() -> None:
    plan = external_tool_first_plan(
        r"0 = \beta \E[V_k(k',z') \mid z]",
        goal_kind="document_repair",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )
    node = make_search_node(
        node_id="obligation_1",
        target=plan["target"],
        status="proved",
        external_tool_plan=plan,
        backend_attempts=[
            BackendAttempt(
                id="route_plan_1",
                tool="external_tool_first_plan",
                status="planned",
                evidence_kind="route_plan",
                certification_status="diagnostic",
                input_summary="planned route only",
            ),
            BackendAttempt(
                id="retrieval_1",
                tool="leansearchv2",
                status="retrieved",
                evidence_kind="retrieval",
                certification_status="diagnostic",
                input_summary="retrieved premise candidates",
                output_ref="leansearch://candidate",
            ),
            BackendAttempt(
                id="formalization_1",
                tool="lean",
                status="requires_formalization",
                evidence_kind="formalization_required",
                certification_status="diagnostic",
                input_summary="LaTeX target needs Lean source",
            ),
            BackendAttempt(
                id="static_extraction_1",
                tool="jixia",
                status="extracted",
                evidence_kind="static_extraction",
                certification_status="diagnostic",
                input_summary="extracted declarations from Lean source",
                output_ref="jixia://declaration",
            ),
            BackendAttempt(
                id="proof_state_1",
                tool="pantograph",
                status="explored",
                evidence_kind="proof_state",
                certification_status="diagnostic",
                input_summary="explored proof-state transitions",
                output_ref="pantograph://trace",
            ),
        ],
    )

    can_promote, errors = branch_can_be_promoted(node)

    assert can_promote is False
    assert "proved status requires scoped certifying backend evidence" in errors
    assert "diagnostic evidence cannot promote a branch" in errors


def test_conflicting_branch_status_cannot_promote_from_opposite_evidence() -> None:
    plan = external_tool_first_plan("A*B = B*A", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="obligation_conflicting",
        target="A*B = B*A",
        status="proved",
        external_tool_plan=plan,
        backend_attempts=[
            counterexample_backend_attempt(
                attempt_id="counterexample_conflict",
                tool="sympy",
                input_summary="2x2 integer matrix counterexample search",
                output_ref="artifact://counterexample/counterexample_conflict.json",
            )
        ],
    )

    report = branch_promotion_report(node)

    assert report["can_promote"] is False
    assert report["supported_status"] is None
    assert "proved status requires scoped certifying backend evidence" in report["errors"]


def test_certifying_backend_attempt_can_promote_proof_branch() -> None:
    plan = external_tool_first_plan("a + b = b + a", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="obligation_2",
        target="a + b = b + a",
        status="proved",
        external_tool_plan=plan,
        backend_attempts=[
            certifying_backend_attempt(
                attempt_id="sympy_cert_1",
                tool="sympy",
                status="proved",
                input_summary="simplify((a + b) - (b + a)) == 0",
                output_ref="artifact://sympy/sympy_cert_1.json",
                version="1.14.0",
            )
        ],
    )

    report = branch_promotion_report(node)

    assert report["can_promote"] is True
    assert report["supported_status"] == "proved"
    assert report["evidence_refs"] == ["sympy_cert_1"]
    assert validate_search_tree({"metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"}, "root": node}) == []


def test_counterexample_attempt_can_promote_refutation_branch() -> None:
    plan = external_tool_first_plan("A*B = B*A", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="obligation_3",
        target="A*B = B*A",
        status="refuted",
        external_tool_plan=plan,
        backend_attempts=[
            counterexample_backend_attempt(
                attempt_id="counterexample_1",
                tool="sympy",
                input_summary="2x2 integer matrix counterexample search",
                output_ref="artifact://counterexample/counterexample_1.json",
            )
        ],
    )

    assert branch_promotion_report(node)["can_promote"] is True
    assert validate_search_tree({"metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"}, "root": node}) == []


def test_backend_unavailable_is_not_refutation() -> None:
    plan = external_tool_first_plan("x + 1 = 1 + x", capabilities=UNAVAILABLE_CAPABILITIES, integrations={})
    node = make_search_node(
        node_id="obligation_4",
        target="x + 1 = 1 + x",
        status="refuted",
        external_tool_plan=plan,
        backend_attempts=[
            BackendAttempt(
                id="sympy_unavailable",
                tool="sympy",
                status="unavailable",
                evidence_kind="backend_unavailable",
                certification_status="diagnostic",
                input_summary="SymPy missing in environment",
            )
        ],
    )

    can_promote, errors = branch_can_be_promoted(node)

    assert can_promote is False
    assert "refuted status requires a concrete counterexample or scoped contradiction" in errors


def test_patch_candidate_carries_location_rationale_and_evidence() -> None:
    plan = external_tool_first_plan(
        r"\E[X \mid z]",
        goal_kind="missing_assumptions",
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )
    patch = PatchCandidate(
        id="patch_conditional_integrability",
        kind="add_assumption",
        location={"file": "paper.tex", "line_start": 770, "label": "prop:interior-foc"},
        proposed_text=(
            "Assume the conditional law of next-period shocks is defined given "
            "the current state and that all payoff derivatives inside the "
            "conditional expectation are integrable."
        ),
        rationale=(
            "Conditional expectations are finite scalar objects only after the "
            "conditioning law and integrability of random terms are specified."
        ),
        validation_status="diagnostic_pending_backend_or_source_check",
        evidence_refs=["assumption_rule:conditional_expectation_integrability"],
    )
    node = make_search_node(
        node_id="obligation_5",
        target=plan["target"],
        status="partial",
        external_tool_plan=plan,
        assumptions=[
            AssumptionSet(
                id="conditional_integrability",
                assumptions=[
                    "The conditional shock law given the current state is defined.",
                    "Random payoff derivative terms have finite conditional first moments.",
                ],
                status="proposed",
                source="assumption_rule",
                closes=["conditional_expectation_well_defined"],
                evidence_refs=["assumption_rule:conditional_expectation_integrability"],
            )
        ],
        patch_candidates=[patch],
    )
    tree = {"metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"}, "root": node}

    assert validate_search_tree(tree) == []
    assert summarize_search_tree(tree)["patch_candidate_count"] == 1
    assert node["patch_candidates"][0]["location"]["line_start"] == 770
    assert "Conditional expectations" in node["patch_candidates"][0]["rationale"]


def _p04_root(**updates) -> dict:
    arguments = {
        "obligation_digest": "a" * 64,
        "target": "x + 1 = 1 + x",
        "typed_assumptions": [{"id": "asm-real", "predicate": "x is real"}],
        "generator": {"kind": "root"},
        "formalization_plan": {"backend": "synthetic", "route": "injected"},
        "state": "ready",
    }
    arguments.update(updates)
    return build_branch_record(**arguments)


def test_child_branch_id_changes_with_assumptions_lineage_and_formalization() -> None:
    root = _p04_root()
    generator = {"kind": "rule_generated", "rule_id": "split", "source_refs": ["blocker:1"]}
    baseline = build_branch_record(
        obligation_digest="a" * 64,
        target="x = x",
        typed_assumptions=[{"id": "a1", "predicate": "x is real"}],
        generator=generator,
        formalization_plan={"backend": "synthetic", "route": "one"},
        parent=root,
    )
    changed_assumption = build_branch_record(
        obligation_digest="a" * 64,
        target="x = x",
        typed_assumptions=[{"id": "a1", "predicate": "x is nonzero"}],
        generator=generator,
        formalization_plan={"backend": "synthetic", "route": "one"},
        parent=root,
    )
    changed_plan = build_branch_record(
        obligation_digest="a" * 64,
        target="x = x",
        typed_assumptions=[{"id": "a1", "predicate": "x is real"}],
        generator=generator,
        formalization_plan={"backend": "synthetic", "route": "two"},
        parent=root,
    )
    other_root = _p04_root(target="y + 1 = 1 + y")
    changed_lineage = build_branch_record(
        obligation_digest="a" * 64,
        target="x = x",
        typed_assumptions=[{"id": "a1", "predicate": "x is real"}],
        generator=generator,
        formalization_plan={"backend": "synthetic", "route": "one"},
        parent=other_root,
    )

    assert len({baseline["id"], changed_assumption["id"], changed_plan["id"], changed_lineage["id"]}) == 4
    assert validate_branch_record(baseline) == []


def test_parent_lineage_is_immutable_and_shared_ledgers_are_rejected() -> None:
    root = _p04_root()
    child = build_branch_record(
        obligation_digest="a" * 64,
        target="x = x",
        typed_assumptions=[],
        generator={"kind": "rule_generated", "rule_id": "split", "source_refs": []},
        formalization_plan={"backend": "synthetic"},
        parent=root,
    )
    root["children"].append(child)
    assert validate_branch_tree(root) == []

    child["lineage"][0] = "branch_wrong"
    assert any("lineage" in error for error in validate_branch_tree(root))
    child["lineage"][0] = root["id"]
    child["attempt_refs"] = root["attempt_refs"]
    assert any("shared mutable ledger" in error for error in validate_branch_tree(root))


def test_branch_state_transition_table_rejects_unrecorded_jump() -> None:
    branch = _p04_root()
    running = transition_branch(
        branch,
        "running",
        reason="Synthetic request started.",
        request_ref="artifact://p04/request/one",
    )
    proved = transition_branch(
        running,
        "proved",
        reason="Injected exact-branch result was certifying.",
        result_ref="artifact://p04/result/one",
    )

    assert validate_branch_record(proved) == []
    with pytest.raises(ValueError, match="illegal branch transition"):
        transition_branch(branch, "proved", reason="Skipped request execution.")

    mutated = deepcopy(proved)
    mutated["state"] = "refuted"
    assert "branch state does not match final transition" in validate_branch_record(mutated)


def test_agent_generated_requires_execution_provenance() -> None:
    invalid = {
        "kind": "agent_generated",
        "executor": "synthetic-agent",
        "provider": None,
        "model": None,
        "request_digest": "1" * 64,
        "response_digest": "2" * 64,
        "timestamp": "not-a-time",
        "budget": {},
        "source_refs": [],
    }
    errors = validate_branch_generator(invalid)
    assert "agent_generated timestamp must be UTC second precision" in errors
    assert "agent_generated budget must be a non-empty object" in errors


def test_serial_parallel_child_order_has_same_semantic_tree_digest() -> None:
    def tree(order: tuple[str, str]) -> dict:
        root = _p04_root()
        children = {
            label: build_branch_record(
                obligation_digest="a" * 64,
                target=f"{label} = {label}",
                typed_assumptions=[{"id": label}],
                generator={"kind": "rule_generated", "rule_id": label, "source_refs": []},
                formalization_plan={"backend": "synthetic"},
                parent=root,
            )
            for label in ("x", "y")
        }
        root["children"] = [children[label] for label in order]
        return root

    assert branch_tree_semantic_digest(tree(("x", "y"))) == branch_tree_semantic_digest(tree(("y", "x")))
