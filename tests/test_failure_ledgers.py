from __future__ import annotations

from copy import deepcopy

import pytest

from mathdevmcp.failure_ledgers import (
    build_ledger_entry,
    build_ledgers,
    build_status_entry,
    classify_status,
    compare_branches,
    deduplicate_ledger_entries,
    rank_repair_branches_partial_order,
    select_next_discriminating_action,
    validate_discriminating_action,
    validate_ledger_entry,
)


def _scope(*, target: str = "x = x", conclusion: str = "x = x", span: int = 0):
    return {
        "obligation_id": "o1",
        "target": target,
        "candidate_conclusion": conclusion,
        "branch_ids": ["b1"],
        "source_spans": [{"file": "doc.tex", "start_byte": span, "end_byte": span + 5, "label": "eq:x"}],
        "closed_blocker_scope": ["gap1"],
    }


def _entry(
    *,
    ledger_kind="mathematical_validity",
    kind="missing_assumption",
    origin="origin-1",
    target="t1",
    scope=None,
    problem="An assumption is missing.",
    why="The target is not defined on the current domain.",
    source_refs=("source:1",),
    evidence_refs=("evidence:1",),
    veto_role="veto",
):
    return build_ledger_entry(
        ledger_kind=ledger_kind,
        kind=kind,
        scope=scope or _scope(),
        target_ids=[target],
        severity="error" if veto_role == "veto" else "info",
        veto_role=veto_role,
        source_refs=source_refs,
        evidence_refs=evidence_refs,
        problem=problem,
        why=why,
        smallest_discriminator={"kind": "state_assumption", "description": "State it.", "closes_scope": ["gap1"]},
        required_artifact={
            "kind": "typed_assumption",
            "schema_version": "typed_assumption@1",
            "binding_fields": ["target_id", "source_span"],
            "path_role": "assumption_evidence",
        },
        origin_ids=[origin],
        non_claims=["not proof"],
    )


@pytest.mark.parametrize("status", ["adapter_error", "timeout", "unavailable"])
def test_adapter_error_timeout_and_unavailable_enter_engineering_only(status):
    entry = build_status_entry(
        status=status,
        origin_id="attempt-1",
        target_id="t1",
        scope=_scope(),
        problem="Tool failed.",
        why="Execution did not complete.",
    )
    assert entry["ledger_kind"] == "engineering"
    assert "refutation" in " ".join(entry["non_claims"])


def test_manifest_mismatch_enters_evidence_integrity_only():
    assert classify_status("certified", evidence_state="manifest_mismatch") == "evidence_integrity"
    entry = build_status_entry(
        status="certified",
        evidence_state="manifest_mismatch",
        origin_id="manifest-1",
        target_id="t1",
        scope=_scope(),
        problem="Manifest mismatch.",
        why="The request bytes differ.",
    )
    assert entry["ledger_kind"] == "evidence_integrity"


def test_missing_assumption_and_backend_unknown_are_mathematical_not_refutation():
    assert classify_status("missing_assumption") == "mathematical_validity"
    entry = build_status_entry(
        status="unknown",
        origin_id="attempt-unknown",
        target_id="t1",
        scope=_scope(),
        problem="Outcome unknown.",
        why="The backend did not decide the target.",
    )
    assert entry["ledger_kind"] == "mathematical_validity"
    assert entry["kind"] == "unknown"


def test_interpretation_entry_cannot_supply_evidence():
    entry = _entry(ledger_kind="interpretation", kind="uncertainty", veto_role="explanatory")
    branch = _branch("b", exact=False, entries=[entry])
    assert branch["exact_verified_evidence"] is False
    assert compare_branches(branch, _branch("c", exact=True))["relation"] == "dominated_by"


def test_unknown_status_fails_closed():
    with pytest.raises(ValueError, match="unclassified status"):
        classify_status("surprisingly_good")


def test_every_veto_entry_requires_smallest_discriminator_and_artifact():
    entry = _entry()
    broken = deepcopy(entry)
    broken["required_artifact"]["binding_fields"] = []
    with pytest.raises(ValueError, match="binding_fields"):
        validate_ledger_entry(broken)


def test_changed_id_or_prose_same_scope_deduplicates_and_preserves_refs():
    one = _entry(origin="attempt-1", target="t1", source_refs=("s1",), evidence_refs=("e1",))
    two = _entry(
        origin="attempt-2",
        target="t2",
        problem="Different wording.",
        why="Still the same scoped gap.",
        source_refs=("s2",),
        evidence_refs=("e2",),
    )
    merged = deduplicate_ledger_entries([two, one])
    assert len(merged) == 1
    assert merged[0]["target_ids"] == ["t1", "t2"]
    assert merged[0]["origin_ids"] == ["attempt-1", "attempt-2"]
    assert merged[0]["source_refs"] == ["s1", "s2"]
    assert merged[0]["evidence_refs"] == ["e1", "e2"]


def test_same_prose_different_scope_is_not_deduped():
    assert len(deduplicate_ledger_entries([_entry(scope=_scope(span=0)), _entry(scope=_scope(span=8), origin="o2")])) == 2


def test_dedup_is_idempotent_and_order_independent():
    values = [_entry(origin="o2"), _entry(origin="o1")]
    once = deduplicate_ledger_entries(values)
    assert deduplicate_ledger_entries(once) == once
    assert deduplicate_ledger_entries(list(reversed(values))) == once
    ledgers = build_ledgers(values)
    assert len(ledgers["raw_entries"]) == 2
    assert len(ledgers["deduplicated_entries"]) == 1


def _branch(
    branch_id,
    *,
    exact=False,
    entries=(),
    assumptions=(),
    coverage=("g1",),
    target="x = x",
    conclusion="x = x",
    obligation="o1",
    cost=None,
):
    return {
        "id": branch_id,
        "obligation_id": obligation,
        "target": target,
        "candidate_conclusion": conclusion,
        "exact_verified_evidence": exact,
        "ledgers": list(entries),
        "typed_assumptions": list(assumptions),
        "covered_obligation_ids": list(coverage),
        "execution_cost": cost,
    }


def _assumption(name, status="supported"):
    return {"id": name, "predicate": name, "status": status}


def test_exact_valid_evidence_dominates_comparable_diagnostic_branch():
    ranking = rank_repair_branches_partial_order([_branch("weak"), _branch("exact", exact=True)])
    assert ranking["nondominated_branch_ids"] == ["exact"]
    assert ranking["unique_top_branch_id"] == "exact"


@pytest.mark.parametrize("status", ["adapter_error", "unavailable"])
def test_error_or_unavailable_never_improves_rank(status):
    adverse = build_status_entry(
        status=status,
        origin_id="a1",
        target_id="t1",
        scope=_scope(),
        problem="Tool failed.",
        why="No valid execution.",
    )
    assert compare_branches(_branch("bad", entries=[adverse]), _branch("clean"))["relation"] == "dominated_by"


def test_validity_failure_cannot_be_compensated_by_broader_coverage():
    mismatch = build_status_entry(
        status="certified",
        evidence_state="manifest_mismatch",
        origin_id="manifest-1",
        target_id="t1",
        scope=_scope(),
        problem="Manifest mismatch.",
        why="The request bytes differ.",
    )
    invalid = _branch("invalid", entries=[mismatch], coverage=["g1", "g2", "g3"])
    valid = _branch("valid", coverage=["g1"])
    relation = compare_branches(invalid, valid)
    assert relation["relation"] == "dominated_by"
    assert relation["reasons"] == ["right better on hard validity gate engineering_evidence_veto"]


def test_duplicate_blockers_and_attempts_do_not_change_rank_or_action():
    one = _entry(origin="o1")
    duplicate = _entry(origin="o2")
    ranking_one = rank_repair_branches_partial_order([_branch("b", entries=[one])])
    ranking_two = rank_repair_branches_partial_order([_branch("b", entries=[one, duplicate])])
    assert ranking_one == ranking_two
    assert select_next_discriminating_action(ranking_one, [one])["action_kind"] == select_next_discriminating_action(ranking_two, [one, duplicate])["action_kind"]


def test_distinct_assumption_coverage_tradeoffs_are_incomparable():
    fewer_assumptions = _branch("few", assumptions=[_assumption("a")], coverage=["g1"])
    more_coverage = _branch("cover", assumptions=[_assumption("a"), _assumption("b")], coverage=["g1", "g2"])
    assert compare_branches(fewer_assumptions, more_coverage)["relation"] == "incomparable"


def test_cross_target_or_conclusion_branches_are_incomparable():
    assert compare_branches(_branch("a"), _branch("b", target="y = y", conclusion="y = y"))["relation"] == "incomparable"


def test_coverage_and_assumption_comparisons_use_set_inclusion_not_counts():
    a = _branch("a", coverage=["g1", "g2"], assumptions=[_assumption("x")])
    b = _branch("b", coverage=["g1", "g3"], assumptions=[_assumption("y")])
    assert compare_branches(a, b)["relation"] == "incomparable"


def test_true_equivalents_are_tied_and_id_only_orders_serialization():
    ranking = rank_repair_branches_partial_order([_branch("z"), _branch("a")])
    assert ranking["nondominated_branch_ids"] == ["a", "z"]
    assert ranking["tie_groups"] == [["a", "z"]]
    assert ranking["unique_top_branch_id"] is None


def test_unknown_cost_does_not_receive_zero_cost_advantage():
    known = _branch("known", cost={"metric": "seconds", "value": 1, "environment_class": "cpu", "provenance": "measured"})
    unknown = _branch("unknown")
    relation = compare_branches(unknown, known)
    assert relation["relation"] == "incomparable"
    assert any("execution_cost" in reason for reason in relation["reasons"])


def test_top_action_names_artifact_and_prefers_engineering_repair():
    math = _entry()
    engineering = build_status_entry(
        status="adapter_error",
        origin_id="a1",
        target_id="t1",
        scope={**_scope(), "branch_ids": ["b"]},
        problem="Adapter broke.",
        why="Serialization failed.",
    )
    ranking = rank_repair_branches_partial_order([_branch("b", entries=[math, engineering])])
    action = select_next_discriminating_action(ranking, [math, engineering])
    assert action["action_kind"] == "repair_engineering"
    assert action["ledger_entry_ids"] == [engineering["entry_id"]]
    assert action["expected_artifact"]["binding_fields"]
    assert set(action["outcomes"]) == {"unavailable", "unsupported", "timeout", "execution_error", "malformed", "certified", "refuted", "unknown"}


def test_unavailable_route_action_is_configuration_not_math():
    entry = _entry(scope={**_scope(), "branch_ids": ["b"]})
    ranking = rank_repair_branches_partial_order([_branch("b", entries=[entry])])
    action = select_next_discriminating_action(
        ranking,
        [entry],
        tool_routes=[{"tool": "lean", "role": "certifier", "route": "lean target.lean", "availability_state": "unavailable"}],
    )
    assert action["action_kind"] == "configure_or_formalize_external_tool"


def test_incomparable_branches_return_choice_not_false_winner():
    entry = _entry(scope={**_scope(), "branch_ids": ["few", "cover"]})
    ranking = rank_repair_branches_partial_order(
        [
            _branch("few", entries=[entry], assumptions=[_assumption("a")], coverage=["g1"]),
            _branch("cover", entries=[entry], assumptions=[_assumption("a"), _assumption("b")], coverage=["g1", "g2"]),
        ]
    )
    action = select_next_discriminating_action(ranking, [entry])
    assert action["action_kind"] == "blocked_for_human_or_formalization_choice"
    assert action["ledger_entry_ids"] == ["unresolved_branch_choice"]
    assert action["expected_artifact"]["kind"] == "formalization_choice_record"


def test_action_validation_rejects_unbound_artifact_or_budget():
    entry = _entry(scope={**_scope(), "branch_ids": ["b"]})
    action = select_next_discriminating_action(rank_repair_branches_partial_order([_branch("b")]), [entry])
    broken = deepcopy(action)
    broken["expected_artifact"]["binding_fields"] = []
    with pytest.raises(ValueError, match="binding_fields"):
        validate_discriminating_action(broken)
    broken = deepcopy(action)
    broken["budget"].pop("provenance")
    with pytest.raises(ValueError, match="budget keys"):
        validate_discriminating_action(broken)


def test_action_never_borrows_a_dominated_branch_veto():
    dominated_veto = build_status_entry(
        status="adapter_error",
        origin_id="bad-attempt",
        target_id="t1",
        scope={**_scope(), "branch_ids": ["bad"]},
        problem="The dominated branch adapter failed.",
        why="The failure applies only to the dominated branch.",
    )
    ranking = rank_repair_branches_partial_order(
        [
            _branch("clean"),
            _branch("bad", entries=[dominated_veto]),
        ]
    )

    action = select_next_discriminating_action(ranking, [dominated_veto])

    assert ranking["nondominated_branch_ids"] == ["clean"]
    assert action["branch_ids"] == ["clean"]
    assert action["action_kind"] == "blocked_for_human_or_formalization_choice"
    assert action["ledger_entry_ids"] == ["unresolved_branch_choice"]
    assert dominated_veto["entry_id"] not in action["launch_vetoes"]
