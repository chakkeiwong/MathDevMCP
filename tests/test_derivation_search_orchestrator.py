from __future__ import annotations

from copy import deepcopy
import hashlib
from threading import Barrier, Lock

import pytest

from mathdevmcp.derivation_search_orchestrator import (
    BranchSearchBudget,
    normalize_branch_search_budget,
    replay_branch_events,
    run_branch_search,
)
from mathdevmcp.external_adapter_contract import (
    build_external_adapter_request,
    build_external_adapter_result,
    p04_injected_result_from_adapter,
)
from mathdevmcp.derivation_search_tree import (
    branch_tree_semantic_digest,
    build_branch_record,
    validate_branch_tree,
)


OBLIGATION = "a" * 64


def _blocker(label: str) -> dict:
    return {
        "id": f"blocker_{label}",
        "kind": "synthetic_requirement",
        "problem": f"Synthetic requirement {label} is open.",
        "why": "The injected state-machine test needs one exact blocker.",
        "required_next_evidence": "Return an exact branch-local injected result.",
        "source": "test",
        "evidence_refs": [f"test:{label}"],
    }


def _root_with_children(*labels: str, obligation: str = OBLIGATION) -> dict:
    root = build_branch_record(
        obligation_digest=obligation,
        target="root target",
        typed_assumptions=[],
        generator={"kind": "root"},
        formalization_plan={"backend": "injected", "action_kind": "backend"},
        state="formalization_blocked",
        blockers=[_blocker("root")],
    )
    for label in labels:
        child = build_branch_record(
            obligation_digest=obligation,
            target=f"{label} = {label}",
            typed_assumptions=[{"id": f"asm-{label}", "predicate": f"{label} is scalar"}],
            generator={"kind": "rule_generated", "rule_id": label, "source_refs": [f"test:{label}"]},
            formalization_plan={
                "backend": "injected",
                "action_kind": "backend",
                "native_input": f"check {label}",
            },
            state="ready",
            parent=root,
            blockers=[_blocker(label)],
        )
        root["children"].append(child)
    assert validate_branch_tree(root) == []
    return root


def _result(request: dict, *, status: str = "proved", close: bool = True, **updates) -> dict:
    label = request["target"].split(" = ", 1)[0]
    value = {
        "branch_id": request["branch_id"],
        "request_digest": request["request_digest"],
        "status": status,
        "reason": f"Injected {status} result for {label}.",
        "evidence_kind": "certifying_backend" if status == "proved" else "diagnostic",
        "certification_status": "certified" if status == "proved" else "diagnostic",
        "closed_blocker_ids": [f"blocker_{label}"] if close else [],
        "output_ref": f"artifact://synthetic/{label}" if status == "proved" else None,
        "test_only": True,
    }
    value.update(updates)
    return value


def test_child_executes_after_expansion_and_updates_exact_child_only() -> None:
    root = _root_with_children("x", "y")
    child_ids = {child["target"]: child["id"] for child in root["children"]}

    def executor(request: dict) -> dict:
        if request["target"] == "x = x":
            return _result(request)
        return _result(request, status="diagnostic", close=False)

    result = run_branch_search(root, executor=executor, budget="smoke")
    final = result["final_tree"]
    by_target = {child["target"]: child for child in final["children"]}

    assert result["status"] == "pass"
    assert final["state"] == "formalization_blocked"
    assert final["attempt_refs"] == final["result_refs"] == []
    assert by_target["x = x"]["id"] == child_ids["x = x"]
    assert by_target["x = x"]["state"] == "proved"
    assert by_target["x = x"]["result_refs"]
    assert by_target["y = y"]["state"] == "diagnostic"
    assert by_target["y = y"]["result_refs"]
    assert set(by_target["x = x"]["result_refs"]).isdisjoint(by_target["y = y"]["result_refs"])
    assert result["publication_mode"] == "disabled"
    assert result["backend_execution_mode"] == "injected_only"
    assert result["usage"]["artifact_reserved_bytes"] == 0


def _adapter_result_for_request(
    request: dict,
    *,
    execution_kind: str,
    manifest_verified: bool,
) -> dict:
    executable = "/usr/bin/sage"
    label = request["target"].split(" = ", 1)[0]
    typed_assumptions = [
        {"id": f"asm-{label}", "predicate": f"{label} is scalar"}
    ]
    adapter_request = build_external_adapter_request(
        branch_id=request["branch_id"],
        branch_lineage=request.get("branch_lineage", [request["branch_id"]]),
        obligation_digest=request["obligation_digest"],
        normalized_target=request["target"],
        typed_assumptions=typed_assumptions,
        native_input_bytes=request["native_input"].encode("utf-8"),
        native_input_media_type="text/x-sage",
        tool_name="sage",
        adapter_version="p05-orchestrator-test",
        backend_version="9.5",
        requested_executable=executable,
        resolved_executable=executable,
        timeout_ms=request["timeout_ms"],
        max_output_bytes=request["max_output_bytes"],
        max_artifact_bytes=request["max_artifact_bytes"],
        expected_result_class="synthetic_orchestrator_fixture",
        backend_role="scoped_specialist_certificate",
        unsupported_conclusions=("no_general_sage_soundness", "no_publication"),
    )
    output_ref = "artifact://p05/sage/manifest"
    return build_external_adapter_result(
        request=adapter_request,
        status="certified",
        reason="Bound Sage adapter certificate.",
        execution={
            "kind": execution_kind,
            "runner_id": "p05-orchestrator-test",
            "command": [executable, "input.sage"] if execution_kind == "subprocess" else [],
            "executable_path": executable if execution_kind == "subprocess" else None,
            "resolved_executable_path": executable if execution_kind == "subprocess" else None,
            "exit_code": 0 if execution_kind == "subprocess" else None,
            "timed_out": False,
            "stdout_bytes": 2,
            "stderr_bytes": 0,
            "stdout_sha256": hashlib.sha256(b"ok").hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        },
        evidence_kind="sage_polynomial_identity",
        evidence_details={"fixture": "process-shaped-not-live-evidence"},
        output_ref=output_ref,
        manifest_ref=output_ref if manifest_verified else None,
        manifest_sha256=hashlib.sha256(b"manifest").hexdigest() if manifest_verified else None,
        manifest_verified=manifest_verified,
        refutation_witness=None,
        next_discriminator="Inspect the exact fixture manifest.",
        non_claims=list(adapter_request["unsupported_conclusions"]),
    )


def test_phase05_fake_adapter_drives_only_synthetic_test_lane() -> None:
    root = _root_with_children("x")
    child = root["children"][0]
    child["formalization_plan"] = {
        **child["formalization_plan"],
        "backend": "sage",
    }
    # Rebuild because the formalization plan is semantic identity.
    root["children"][0] = build_branch_record(
        obligation_digest=child["obligation_digest"],
        target=child["target"],
        typed_assumptions=child["typed_assumptions"],
        generator=child["generator"],
        formalization_plan=child["formalization_plan"],
        state="ready",
        parent=root,
        blockers=child["blockers"],
    )

    def executor(request: dict) -> dict:
        adapter = _adapter_result_for_request(
            request, execution_kind="fake_runner", manifest_verified=False
        )
        return p04_injected_result_from_adapter(
            adapter, request, closed_blocker_ids=["blocker_x"]
        )

    result = run_branch_search(root, executor=executor, budget="smoke")
    recorded = next(
        value for key, value in result["artifacts"].items() if "/result/" in key
    )
    assert result["final_tree"]["children"][0]["state"] == "proved"
    assert recorded["test_only"] is True
    assert recorded["live_tool_executed"] is False
    assert recorded["manifest_verified"] is False


def test_phase05_process_shaped_result_cannot_advance_without_real_verified_manifest() -> None:
    root = _root_with_children("x")
    child = root["children"][0]
    root["children"][0] = build_branch_record(
        obligation_digest=child["obligation_digest"],
        target=child["target"],
        typed_assumptions=child["typed_assumptions"],
        generator=child["generator"],
        formalization_plan={**child["formalization_plan"], "backend": "sage"},
        state="ready",
        parent=root,
        blockers=child["blockers"],
    )

    def unverified(request: dict) -> dict:
        adapter = _adapter_result_for_request(
            request, execution_kind="subprocess", manifest_verified=False
        )
        return p04_injected_result_from_adapter(
            adapter, request, closed_blocker_ids=["blocker_x"]
        )

    diagnostic = run_branch_search(root, executor=unverified, budget="smoke")
    assert diagnostic["final_tree"]["children"][0]["state"] == "diagnostic"

    def verified(request: dict) -> dict:
        adapter = _adapter_result_for_request(
            request, execution_kind="subprocess", manifest_verified=True
        )
        return p04_injected_result_from_adapter(
            adapter, request, closed_blocker_ids=["blocker_x"]
        )

    rejected = run_branch_search(root, executor=verified, budget="smoke")
    assert rejected["final_tree"]["children"][0]["state"] == "failed"
    failed_record = next(
        value for key, value in rejected["artifacts"].items() if "/result/" in key
    )
    assert failed_record["status"] == "failed"
    assert "manifest verification failed" in failed_record["reason"]


def test_bare_live_promotion_flags_cannot_bypass_embedded_adapter_validation() -> None:
    root = _root_with_children("x")

    def forged(request: dict) -> dict:
        return {
            **_result(request),
            "test_only": False,
            "live_tool_executed": True,
            "manifest_verified": True,
            "adapter_result_digest": "a" * 64,
        }

    result = run_branch_search(root, executor=forged, budget="smoke")
    assert result["final_tree"]["children"][0]["state"] == "failed"
    assert any(event["kind"] == "result_binding_failure" for event in result["event_log"])


def test_event_log_replay_reconstructs_final_tree() -> None:
    root = _root_with_children("x", "y")
    result = run_branch_search(root, executor=_result, budget="smoke")
    replayed = replay_branch_events(result["initial_tree"], result["event_log"])

    assert branch_tree_semantic_digest(replayed) == result["final_tree_digest"]
    assert result["replay_tree_digest"] == result["final_tree_digest"]
    assert [event["sequence"] for event in result["event_log"]] == list(
        range(1, len(result["event_log"]) + 1)
    )


def test_result_binding_failure_vetoes_exact_branch() -> None:
    root = _root_with_children("x")

    def wrong_branch(request: dict) -> dict:
        return _result(request, branch_id="branch_wrong")

    result = run_branch_search(root, executor=wrong_branch, budget="smoke")
    child = result["final_tree"]["children"][0]

    assert child["state"] == "failed"
    assert child["result_refs"] == []
    assert result["usage"]["artifact_reserved_bytes"] == 0
    assert any(event["kind"] == "result_binding_failure" for event in result["event_log"])


def test_failed_signature_is_not_repeated_on_equivalent_child() -> None:
    root = _root_with_children("x")
    calls = []

    def executor(request: dict) -> dict:
        calls.append(request["request_digest"])
        return _result(request, status="diagnostic", close=False)

    def expander(parent: dict, _result_record: dict) -> list[dict]:
        child = build_branch_record(
            obligation_digest=parent["obligation_digest"],
            target=parent["target"],
            typed_assumptions=parent["typed_assumptions"],
            generator={"kind": "rule_generated", "rule_id": "retry", "source_refs": []},
            formalization_plan=parent["formalization_plan"],
            state="ready",
            parent=parent,
            blockers=[_blocker("x")],
        )
        return [child]

    result = run_branch_search(
        root,
        executor=executor,
        expander=expander,
        budget=BranchSearchBudget(max_depth=2, max_nodes=4, max_attempts_total=3),
    )
    grandchild = result["final_tree"]["children"][0]["children"][0]

    assert len(calls) == 1
    assert grandchild["state"] == "diagnostic"
    assert grandchild["attempt_refs"] == []
    assert any(event["kind"] == "duplicate_failed_signature" for event in result["event_log"])


def test_serial_parallel_schedules_have_same_final_tree_digest() -> None:
    root = _root_with_children("x", "y")
    budget = BranchSearchBudget(max_attempts_total=2)
    serial = run_branch_search(root, executor=_result, budget=budget, schedule="serial")
    barrier = Barrier(2)
    active = 0
    max_active = 0
    lock = Lock()

    def concurrent_result(request: dict) -> dict:
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        barrier.wait(timeout=2)
        value = _result(request)
        with lock:
            active -= 1
        return value

    parallel = run_branch_search(
        root,
        executor=concurrent_result,
        budget=budget,
        schedule="parallel",
    )

    assert max_active == 2
    assert serial["final_tree_digest"] == parallel["final_tree_digest"]
    assert serial["ranking"] == parallel["ranking"]
    assert serial["event_log_terminal_digest"] != parallel["event_log_terminal_digest"]
    assert parallel["backend_execution_mode"] == "injected_parallel"


def test_parallel_reservations_do_not_oversubscribe_shared_attempt_budget() -> None:
    root = _root_with_children("x", "y")
    calls = []

    def executor(request: dict) -> dict:
        calls.append(request["branch_id"])
        return _result(request)

    result = run_branch_search(
        root,
        executor=executor,
        budget=BranchSearchBudget(max_attempts_total=1),
        schedule="parallel",
    )
    children = result["final_tree"]["children"]

    assert len(calls) == 1
    assert result["usage"]["attempts_total"] == 1
    assert sum(child["state"] == "proved" for child in children) == 1
    assert sum(child["state"] == "budget_exhausted" for child in children) == 1
    assert any(
        item["dimension"] == "max_attempts_total"
        for item in result["budget_exhaustions"]
    )


def test_parallel_reservations_do_not_oversubscribe_shared_byte_budgets() -> None:
    root = _root_with_children("x", "y")

    for dimension, budget in (
        (
            "max_input_bytes",
            BranchSearchBudget(max_attempts_total=2, max_input_bytes=10),
        ),
        (
            "max_artifact_bytes",
            BranchSearchBudget(max_attempts_total=2, max_artifact_bytes=1_500_000),
        ),
    ):
        calls = []

        def executor(request: dict) -> dict:
            calls.append(request["branch_id"])
            return _result(request)

        result = run_branch_search(
            root,
            executor=executor,
            budget=budget,
            schedule="parallel",
        )

        assert len(calls) == 1
        assert result["usage"]["attempts_total"] == 1
        assert result["usage"]["artifact_reserved_bytes"] == 0
        assert any(
            item["dimension"] == dimension
            for item in result["budget_exhaustions"]
        )


def test_conflicting_repeated_execution_vetoes_exact_branch() -> None:
    root = _root_with_children("x")

    def conflicting(request: dict) -> list[dict]:
        return [
            _result(request),
            _result(
                request,
                status="refuted",
                evidence_kind="counterexample",
                certification_status="counterexample",
                output_ref="artifact://synthetic/x-counterexample",
            ),
        ]

    result = run_branch_search(root, executor=conflicting, budget="smoke")
    child = result["final_tree"]["children"][0]

    assert child["state"] == "failed"
    assert child["result_refs"] == []
    assert result["usage"]["artifact_reserved_bytes"] == 0
    assert len([key for key in result["artifacts"] if "/result/" in key]) == 2
    assert any(event["kind"] == "conflicting_repeated_results" for event in result["event_log"])
    assert child["id"] in result["ranking"]


def test_multi_child_expansion_respects_shared_node_budget() -> None:
    root = _root_with_children("x")

    def diagnostic(request: dict) -> dict:
        return _result(request, status="diagnostic", close=False)

    def expander(parent: dict, _result_record: dict) -> list[dict]:
        return [
            build_branch_record(
                obligation_digest=parent["obligation_digest"],
                target=f"{label} = {label}",
                typed_assumptions=[{"id": label, "predicate": f"{label} is scalar"}],
                generator={"kind": "rule_generated", "rule_id": label, "source_refs": []},
                formalization_plan={"backend": "injected", "action_kind": "backend"},
                state="ready",
                parent=parent,
                blockers=[_blocker(label)],
            )
            for label in ("y", "z")
        ]

    result = run_branch_search(
        root,
        executor=diagnostic,
        expander=expander,
        budget=BranchSearchBudget(max_depth=2, max_nodes=3, max_attempts_total=1),
    )
    child = result["final_tree"]["children"][0]

    assert len(child["children"]) == 1
    assert result["usage"]["nodes"] == 3
    assert any(item["dimension"] == "max_nodes" for item in result["budget_exhaustions"])


def test_compiler_observes_final_tree_and_is_bound_to_final_digest() -> None:
    root = _root_with_children("x")
    observed = {}

    def compiler(final_tree: dict, final_digest: str) -> dict:
        observed["states"] = [child["state"] for child in final_tree["children"]]
        return {
            "status": "compiled_final_tree",
            "final_tree_digest": final_digest,
            "publication_mode": "disabled",
        }

    result = run_branch_search(root, executor=_result, compiler=compiler, budget="smoke")

    assert observed["states"] == ["proved"]
    assert result["compilation"]["final_tree_digest"] == result["final_tree_digest"]
    assert result["compilation"]["publication_mode"] == "disabled"


def test_timeout_stops_branch_and_is_not_refutation() -> None:
    root = _root_with_children("x")

    def timeout(request: dict) -> dict:
        return _result(request, status="timeout", close=False)

    result = run_branch_search(root, executor=timeout, budget="smoke")
    child = result["final_tree"]["children"][0]

    assert child["state"] == "budget_exhausted"
    assert child["state"] != "refuted"
    assert result["usage"]["attempts_total"] == 1
    assert result["usage"]["artifact_reserved_bytes"] == 0


@pytest.mark.parametrize(
    ("dimension", "tree_factory", "budget", "plan_update"),
    [
        (
            "max_targets",
            lambda: _root_with_children("x", "y"),
            BranchSearchBudget(max_targets=1),
            None,
        ),
        (
            "max_depth",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_depth=0),
            None,
        ),
        (
            "max_nodes",
            lambda: _root_with_children("x", "y"),
            BranchSearchBudget(max_nodes=2),
            None,
        ),
        (
            "max_attempts_total",
            lambda: _root_with_children("x", "y"),
            BranchSearchBudget(max_attempts_total=1),
            None,
        ),
        (
            "max_attempts_per_branch",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_attempts_per_branch=0),
            None,
        ),
        (
            "max_retrieval_calls",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_retrieval_calls=0),
            {"action_kind": "retrieval"},
        ),
        (
            "max_agent_calls",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_agent_calls=0),
            {"action_kind": "agent"},
        ),
        (
            "max_input_bytes",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_input_bytes=1),
            {"native_input": "too large"},
        ),
        (
            "max_artifact_bytes",
            lambda: _root_with_children("x"),
            BranchSearchBudget(max_artifact_bytes=1),
            None,
        ),
    ],
)
def test_budget_dimension_exhaustion_is_explicit_and_non_refuting(
    dimension: str,
    tree_factory,
    budget: BranchSearchBudget,
    plan_update: dict | None,
) -> None:
    root = tree_factory()
    if dimension == "max_targets":
        root["children"][1] = build_branch_record(
            obligation_digest="b" * 64,
            target="y = y",
            typed_assumptions=[],
            generator={"kind": "rule_generated", "rule_id": "y-other", "source_refs": []},
            formalization_plan={"backend": "injected", "action_kind": "backend"},
            state="ready",
            parent=root,
            blockers=[_blocker("y")],
        )
    if plan_update:
        # Rebuild the branch because formalization plan is part of its semantic id.
        old = root["children"][0]
        plan = {**old["formalization_plan"], **plan_update}
        root["children"][0] = build_branch_record(
            obligation_digest=old["obligation_digest"],
            target=old["target"],
            typed_assumptions=old["typed_assumptions"],
            generator=old["generator"],
            formalization_plan=plan,
            state="ready",
            parent=root,
            blockers=old["blockers"],
        )
    assert validate_branch_tree(root) == []

    result = run_branch_search(root, executor=_result, budget=budget)

    assert any(item["dimension"] == dimension for item in result["budget_exhaustions"])
    assert all(item["state"] != "refuted" for item in result["final_tree"]["children"])


def test_wall_time_budget_exhaustion_is_explicit() -> None:
    root = _root_with_children("x")
    ticks = iter([0.0, 31.0])
    result = run_branch_search(root, executor=_result, budget="smoke", clock=lambda: next(ticks))

    assert result["budget_exhaustions"][0]["dimension"] == "max_wall_time_seconds"
    assert result["final_tree"]["children"][0]["state"] == "budget_exhausted"


def test_tool_timeout_is_clamped_to_budget() -> None:
    root = _root_with_children("x")
    old = root["children"][0]
    root["children"][0] = build_branch_record(
        obligation_digest=old["obligation_digest"],
        target=old["target"],
        typed_assumptions=old["typed_assumptions"],
        generator=old["generator"],
        formalization_plan={**old["formalization_plan"], "timeout_seconds": 999},
        state="ready",
        parent=root,
        blockers=old["blockers"],
    )
    observed = []

    def executor(request: dict) -> dict:
        observed.append(request["timeout_ms"])
        return _result(request)

    run_branch_search(root, executor=executor, budget="smoke")
    assert observed == [10_000]


def test_oversize_output_cannot_certify_branch() -> None:
    root = _root_with_children("x")

    def executor(request: dict) -> dict:
        return _result(request, reason="x" * 4096)

    budget = BranchSearchBudget(max_output_bytes_per_attempt=512)
    result = run_branch_search(root, executor=executor, budget=budget)

    assert result["final_tree"]["children"][0]["state"] == "budget_exhausted"
    assert result["final_tree"]["children"][0]["result_refs"] == []
    assert result["usage"]["artifact_reserved_bytes"] == 0
    assert any(item["dimension"] == "max_output_bytes_per_attempt" for item in result["budget_exhaustions"])


def test_budget_schema_is_closed() -> None:
    with pytest.raises(ValueError, match="budget keys"):
        normalize_branch_search_budget({"max_nodes": 3})

    assert normalize_branch_search_budget("standard")["max_nodes"] == 12
