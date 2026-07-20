from __future__ import annotations

"""Deterministic branch-local orchestration with injected execution only."""

from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import asdict, dataclass
import time
from typing import Any

from .contracts import attach_contract
from .derivation_search_tree import (
    P04_TERMINAL_BRANCH_STATES,
    branch_tree_semantic_digest,
    transition_branch,
    validate_branch_record,
    validate_branch_tree,
)
from .evidence_manifest import canonical_json_bytes, content_digest
from .backend_protocol import (
    P04_BOUNDARY,
    P04_EVENT_SCHEMA,
    P04_ORCHESTRATOR_CONTRACT,
    P04_REQUEST_SCHEMA,
    P04_RESULT_SCHEMA,
)
from .external_adapter_contract import (
    validate_external_adapter_result,
    verify_live_adapter_manifest,
)


P04_RESULT_RESERVATION_MULTIPLIER = 4
P04_RESULT_RESERVATION_OVERHEAD_BYTES = 65_536
P04_MAX_RESULT_OBSERVATIONS = 2
# The executor's full canonical output is capped before parsing. Reserving four
# times that cap plus fixed record overhead safely covers two normalized records.
P04_BUDGET_KEYS = frozenset(
    {
        "max_targets",
        "max_depth",
        "max_nodes",
        "max_attempts_total",
        "max_attempts_per_branch",
        "max_wall_time_seconds",
        "max_tool_timeout_seconds",
        "max_retrieval_calls",
        "max_agent_calls",
        "max_input_bytes",
        "max_output_bytes_per_attempt",
        "max_artifact_bytes",
    }
)


@dataclass(frozen=True)
class BranchSearchBudget:
    max_targets: int = 1
    max_depth: int = 1
    max_nodes: int = 3
    max_attempts_total: int = 2
    max_attempts_per_branch: int = 1
    max_wall_time_seconds: float = 30.0
    max_tool_timeout_seconds: float = 10.0
    max_retrieval_calls: int = 0
    max_agent_calls: int = 0
    max_input_bytes: int = 262_144
    max_output_bytes_per_attempt: int = 262_144
    max_artifact_bytes: int = 5_242_880


P04_BUDGET_PROFILES = {
    "smoke": BranchSearchBudget(),
    "standard": BranchSearchBudget(
        max_targets=6,
        max_depth=2,
        max_nodes=12,
        max_attempts_total=18,
        max_attempts_per_branch=3,
        max_wall_time_seconds=180.0,
        max_tool_timeout_seconds=30.0,
        max_retrieval_calls=8,
        max_agent_calls=0,
        max_input_bytes=1_048_576,
        max_output_bytes_per_attempt=1_048_576,
        max_artifact_bytes=52_428_800,
    ),
}


def normalize_branch_search_budget(
    budget: BranchSearchBudget | Mapping[str, Any] | str | None,
) -> dict[str, int | float]:
    if budget is None:
        value = asdict(P04_BUDGET_PROFILES["smoke"])
    elif isinstance(budget, str):
        if budget not in P04_BUDGET_PROFILES:
            raise ValueError(f"unknown Phase 04 budget profile: {budget}")
        value = asdict(P04_BUDGET_PROFILES[budget])
    elif isinstance(budget, BranchSearchBudget):
        value = asdict(budget)
    elif isinstance(budget, Mapping):
        if set(budget) != P04_BUDGET_KEYS:
            raise ValueError(
                f"Phase 04 budget keys must be exactly {sorted(P04_BUDGET_KEYS)}"
            )
        value = dict(budget)
    else:
        raise TypeError("unsupported Phase 04 budget")
    if set(value) != P04_BUDGET_KEYS:
        raise ValueError("Phase 04 budget profile is incomplete")
    zero_allowed = {"max_depth", "max_attempts_total", "max_attempts_per_branch", "max_retrieval_calls", "max_agent_calls"}
    float_fields = {"max_wall_time_seconds", "max_tool_timeout_seconds"}
    for key, item in value.items():
        if key in float_fields:
            if not isinstance(item, (int, float)) or isinstance(item, bool) or float(item) <= 0:
                raise ValueError(f"Phase 04 {key} must be positive")
            value[key] = float(item)
        else:
            if type(item) is not int or item < (0 if key in zero_allowed else 1):
                raise ValueError(f"Phase 04 {key} is invalid")
    return value


def _walk_branches(root: dict[str, Any]) -> list[dict[str, Any]]:
    result = [root]
    for child in root.get("children", []):
        if isinstance(child, dict):
            result.extend(_walk_branches(child))
    return result


def _replace_branch(root: dict[str, Any], replacement: dict[str, Any]) -> dict[str, Any]:
    if root.get("id") == replacement.get("id"):
        return deepcopy(replacement)
    result = deepcopy(root)
    result["children"] = [
        _replace_branch(child, replacement) if isinstance(child, dict) else child
        for child in root.get("children", [])
    ]
    return result


def _find_branch(root: dict[str, Any], branch_id: str) -> dict[str, Any] | None:
    return next((item for item in _walk_branches(root) if item.get("id") == branch_id), None)


def _event_payload(event: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in event.items() if key != "event_digest"}


def _append_event(
    events: list[dict[str, Any]],
    *,
    kind: str,
    branch: dict[str, Any] | None,
    reason: str,
    request_ref: str | None = None,
    result_ref: str | None = None,
    budget_dimension: str | None = None,
) -> None:
    previous = events[-1]["event_digest"] if events else None
    event = {
        "schema_version": P04_EVENT_SCHEMA,
        "sequence": len(events) + 1,
        "previous_event_digest": previous,
        "kind": kind,
        "branch_id": branch.get("id") if isinstance(branch, dict) else None,
        "reason": reason,
        "request_ref": request_ref,
        "result_ref": result_ref,
        "budget_dimension": budget_dimension,
        "branch_snapshot": deepcopy(branch) if isinstance(branch, dict) else None,
    }
    event["event_digest"] = content_digest(_event_payload(event))
    events.append(event)


def replay_branch_events(
    initial_root: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Replay the exact branch snapshots in a validated semantic event chain."""
    root = deepcopy(initial_root)
    previous: str | None = None
    for sequence, event in enumerate(events, start=1):
        if not isinstance(event, dict) or event.get("schema_version") != P04_EVENT_SCHEMA:
            raise ValueError("Phase 04 event schema mismatch")
        if event.get("sequence") != sequence or event.get("previous_event_digest") != previous:
            raise ValueError("Phase 04 event chain mismatch")
        if event.get("event_digest") != content_digest(_event_payload(event)):
            raise ValueError("Phase 04 event digest mismatch")
        snapshot = event.get("branch_snapshot")
        if snapshot is not None:
            if not isinstance(snapshot, dict) or validate_branch_record(snapshot):
                raise ValueError("Phase 04 event branch snapshot is invalid")
            if _find_branch(root, str(snapshot.get("id"))) is None:
                raise ValueError("Phase 04 event references an absent branch")
            root = _replace_branch(root, snapshot)
        previous = event["event_digest"]
    errors = validate_branch_tree(root)
    if errors:
        raise ValueError("replayed Phase 04 tree is invalid: " + "; ".join(errors))
    return root


def _request_for_branch(
    branch: dict[str, Any],
    budget: Mapping[str, int | float],
) -> dict[str, Any]:
    plan = branch["formalization_plan"]
    requested_timeout = plan.get("timeout_seconds", budget["max_tool_timeout_seconds"])
    if not isinstance(requested_timeout, (int, float)) or isinstance(requested_timeout, bool) or requested_timeout <= 0:
        raise ValueError("formalization plan timeout_seconds must be positive")
    timeout_ms = int(
        min(float(requested_timeout), float(budget["max_tool_timeout_seconds"])) * 1000
    )
    native_input = plan.get("native_input", branch["target"])
    if not isinstance(native_input, str):
        raise ValueError("formalization plan native_input must be a string")
    request = {
        "schema_version": P04_REQUEST_SCHEMA,
        "branch_id": branch["id"],
        "branch_lineage": list(branch["lineage"]),
        "obligation_digest": branch["obligation_digest"],
        "target": branch["target"],
        "typed_assumption_digests": list(branch["typed_assumption_digests"]),
        "action_kind": str(plan.get("action_kind", "backend")),
        "backend": str(plan.get("backend", "injected")),
        "native_input": native_input,
        "native_input_digest": content_digest(native_input.encode("utf-8")),
        "timeout_ms": timeout_ms,
        "max_output_bytes": int(budget["max_output_bytes_per_attempt"]),
        "max_artifact_bytes": int(budget["max_artifact_bytes"]),
        "formalization_plan_digest": content_digest(plan),
    }
    request["request_digest"] = content_digest(request)
    request["request_ref"] = f"artifact://p04/request/{request['request_digest']}"
    return request


def _action_signature(branch: dict[str, Any], request: dict[str, Any]) -> str:
    return content_digest(
        [
            branch["target"],
            branch["typed_assumption_digests"],
            request["action_kind"],
            request["backend"],
            request["native_input_digest"],
            request["formalization_plan_digest"],
        ]
    )


def _result_record(request: dict[str, Any], raw_result: Any) -> dict[str, Any]:
    if not isinstance(raw_result, dict):
        raise ValueError("injected executor result must be an object")
    if raw_result.get("branch_id") != request["branch_id"]:
        raise ValueError("executor result branch binding mismatch")
    if raw_result.get("request_digest") != request["request_digest"]:
        raise ValueError("executor result request binding mismatch")
    status = raw_result.get("status")
    if status not in {"proved", "refuted", "diagnostic", "failed", "timeout"}:
        raise ValueError("executor result status is invalid")
    closed = raw_result.get("closed_blocker_ids", [])
    if not isinstance(closed, list) or any(not isinstance(item, str) or not item for item in closed):
        raise ValueError("executor closed_blocker_ids must be a list of ids")
    test_only = raw_result.get("test_only") is True
    adapter_result = raw_result.get("adapter_result")
    live_tool_executed = False
    manifest_verified = False
    adapter_result_digest = None
    live_manifest_verification = None
    if adapter_result is not None:
        try:
            adapter_result = validate_external_adapter_result(adapter_result)
        except ValueError as exc:
            raise ValueError(f"executor adapter result is invalid: {exc}") from exc
        adapter_request = adapter_result["request"]
        if adapter_request["branch_id"] != request["branch_id"]:
            raise ValueError("executor adapter result branch binding mismatch")
        if adapter_request["branch_lineage"] != request["branch_lineage"]:
            raise ValueError("executor adapter result lineage binding mismatch")
        if adapter_request["obligation_digest"] != request["obligation_digest"]:
            raise ValueError("executor adapter result obligation binding mismatch")
        if adapter_request["normalized_target"] != request["target"]:
            raise ValueError("executor adapter result target binding mismatch")
        if adapter_request["native_input_digest"] != request["native_input_digest"]:
            raise ValueError("executor adapter result native-input binding mismatch")
        adapter_assumption_digests = [
            content_digest(item) for item in adapter_request["typed_assumptions"]
        ]
        if adapter_assumption_digests != request["typed_assumption_digests"]:
            raise ValueError("executor adapter result typed-assumption binding mismatch")
        adapter_limits = adapter_request["resource_limits"]
        if adapter_limits["timeout_ms"] != request["timeout_ms"]:
            raise ValueError("executor adapter result timeout binding mismatch")
        if adapter_limits["max_output_bytes"] != request["max_output_bytes"]:
            raise ValueError("executor adapter result output-limit binding mismatch")
        if adapter_limits["max_artifact_bytes"] > request["max_artifact_bytes"]:
            raise ValueError("executor adapter result artifact-limit exceeds the branch budget")
        adapter_tool = adapter_request["tool"]["name"]
        if not test_only and request["backend"] != adapter_tool:
            raise ValueError("live adapter tool does not match the branch backend")
        live_tool_executed = adapter_result["live_tool_executed"] is True
        manifest_verified = adapter_result["evidence"]["manifest_verified"] is True
        adapter_result_digest = adapter_result["result_digest"]
        if raw_result.get("adapter_result_digest") != adapter_result_digest:
            raise ValueError("executor adapter result digest binding mismatch")
        if raw_result.get("output_ref") != adapter_result["evidence"]["output_ref"]:
            raise ValueError("executor output reference does not match adapter evidence")
        if live_tool_executed and manifest_verified:
            try:
                live_manifest_verification = verify_live_adapter_manifest(adapter_result)
            except ValueError as exc:
                raise ValueError(f"executor live manifest is invalid: {exc}") from exc
            if raw_result.get("live_manifest_verification") != live_manifest_verification:
                raise ValueError("executor live manifest verification binding mismatch")
    if not test_only and status in {"proved", "refuted"}:
        expected_adapter_status = "certified" if status == "proved" else "refuted"
        if (
            adapter_result is None
            or adapter_result["status"] != expected_adapter_status
            or adapter_result["can_promote"] is not True
            or not live_tool_executed
            or not manifest_verified
        ):
            raise ValueError(
                "live proved/refuted result requires exact promotable adapter evidence and a verified manifest"
            )
    record = {
        "schema_version": P04_RESULT_SCHEMA,
        "branch_id": request["branch_id"],
        "request_digest": request["request_digest"],
        "status": status,
        "evidence_kind": str(raw_result.get("evidence_kind", "diagnostic")),
        "certification_status": str(raw_result.get("certification_status", "diagnostic")),
        "closed_blocker_ids": list(closed),
        "reason": str(raw_result.get("reason", "Injected executor returned no reason.")),
        "output_ref": raw_result.get("output_ref"),
        "raw_result_digest": content_digest(raw_result),
        "test_only": test_only,
        "live_tool_executed": live_tool_executed,
        "manifest_verified": manifest_verified,
        "adapter_result_digest": adapter_result_digest,
        "live_manifest_verification": live_manifest_verification,
    }
    record["result_digest"] = content_digest(record)
    record["result_ref"] = f"artifact://p04/result/{record['result_digest']}"
    return record


def _state_for_result(branch: dict[str, Any], result: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    blocker_ids = {str(item.get("id")) for item in branch["blockers"] if isinstance(item, dict)}
    closed = set(result["closed_blocker_ids"])
    if not closed <= blocker_ids:
        return "failed", deepcopy(branch["blockers"])
    remaining = [item for item in branch["blockers"] if item.get("id") not in closed]
    if result["status"] == "timeout":
        return "budget_exhausted", remaining
    if result["status"] == "failed":
        return "failed", remaining
    if result["status"] == "proved":
        evidence_authorized = result["test_only"] or (
            result["live_tool_executed"]
            and result["manifest_verified"]
            and isinstance(result["adapter_result_digest"], str)
            and bool(result["adapter_result_digest"])
        )
        certifying = (
            result["evidence_kind"] in {"certifying_backend", "lean_check", "symbolic_identity", "sage_check"}
            and result["certification_status"] in {"certifying", "certified", "verified", "proved"}
            and isinstance(result["output_ref"], str)
            and bool(result["output_ref"])
            and evidence_authorized
        )
        return ("proved" if certifying and not remaining else "diagnostic"), remaining
    if result["status"] == "refuted":
        evidence_authorized = result["test_only"] or (
            result["live_tool_executed"]
            and result["manifest_verified"]
            and isinstance(result["adapter_result_digest"], str)
            and bool(result["adapter_result_digest"])
        )
        refuting = (
            result["evidence_kind"] in {"counterexample", "scoped_contradiction"}
            and result["certification_status"] in {"blocking", "counterexample", "refuting", "refuted"}
            and isinstance(result["output_ref"], str)
            and bool(result["output_ref"])
            and evidence_authorized
        )
        return ("refuted" if refuting and not remaining else "diagnostic"), remaining
    return "diagnostic", remaining


def _execute_injected_action(
    executor: Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]],
    request: dict[str, Any],
) -> tuple[dict[str, Any] | list[dict[str, Any]], int]:
    try:
        raw_result = executor(deepcopy(request))
        return raw_result, len(canonical_json_bytes(raw_result))
    except Exception as exc:
        raw_result = {
            "branch_id": request["branch_id"],
            "request_digest": request["request_digest"],
            "status": "failed",
            "reason": f"Injected executor raised {type(exc).__name__}: {exc}",
            "evidence_kind": "diagnostic",
            "certification_status": "diagnostic",
            "closed_blocker_ids": [],
            "output_ref": None,
            "test_only": True,
        }
        return raw_result, len(canonical_json_bytes(raw_result))


def _result_records(
    request: dict[str, Any],
    raw_result: dict[str, Any] | list[dict[str, Any]],
) -> list[dict[str, Any]]:
    observations = raw_result if isinstance(raw_result, list) else [raw_result]
    if not observations:
        raise ValueError("injected executor returned no result observations")
    if len(observations) > P04_MAX_RESULT_OBSERVATIONS:
        raise ValueError(
            f"injected executor returned more than {P04_MAX_RESULT_OBSERVATIONS} observations"
        )
    return [_result_record(request, observation) for observation in observations]


def _result_decision_digest(result: dict[str, Any]) -> str:
    return content_digest(
        {
            "status": result["status"],
            "evidence_kind": result["evidence_kind"],
            "certification_status": result["certification_status"],
            "closed_blocker_ids": sorted(result["closed_blocker_ids"]),
            "output_ref": result.get("output_ref"),
            "test_only": result.get("test_only") is True,
            "live_tool_executed": result.get("live_tool_executed") is True,
            "manifest_verified": result.get("manifest_verified") is True,
            "adapter_result_digest": result.get("adapter_result_digest"),
            "live_manifest_verification": result.get("live_manifest_verification"),
        }
    )


def _results_conflict(results: list[dict[str, Any]]) -> bool:
    return len({_result_decision_digest(result) for result in results}) > 1


def _exhaust_branch(
    root: dict[str, Any],
    branch: dict[str, Any],
    events: list[dict[str, Any]],
    exhaustions: list[dict[str, Any]],
    *,
    dimension: str,
    reason: str,
) -> dict[str, Any]:
    if branch["state"] in P04_TERMINAL_BRANCH_STATES:
        return root
    exhausted = transition_branch(branch, "budget_exhausted", reason=reason)
    root = _replace_branch(root, exhausted)
    exhaustions.append({"branch_id": branch["id"], "dimension": dimension, "reason": reason})
    _append_event(
        events,
        kind="budget_exhausted",
        branch=exhausted,
        reason=reason,
        budget_dimension=dimension,
    )
    return root


def _reserve_branch_action(
    root: dict[str, Any],
    branch: dict[str, Any],
    *,
    budget: Mapping[str, int | float],
    usage: dict[str, int],
    attempts_by_branch: dict[str, int],
    artifacts: dict[str, dict[str, Any]],
    events: list[dict[str, Any]],
    exhaustions: list[dict[str, Any]],
    failed_signatures: set[str],
    start: float,
    clock: Callable[[], float],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    live = _find_branch(root, branch["id"])
    if live is None or live["state"] != "ready":
        return root, None
    if clock() - start >= float(budget["max_wall_time_seconds"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_wall_time_seconds",
                reason="Phase 04 wall-time budget was exhausted before the next action.",
            ),
            None,
        )
    if usage["attempts_total"] >= int(budget["max_attempts_total"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_attempts_total",
                reason="Total Phase 04 attempt budget was exhausted.",
            ),
            None,
        )
    if attempts_by_branch.get(live["id"], 0) >= int(budget["max_attempts_per_branch"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_attempts_per_branch",
                reason="Per-branch Phase 04 attempt budget was exhausted.",
            ),
            None,
        )
    try:
        request = _request_for_branch(live, budget)
    except ValueError as exc:
        failed = transition_branch(live, "failed", reason=str(exc))
        root = _replace_branch(root, failed)
        _append_event(events, kind="request_invalid", branch=failed, reason=str(exc))
        return root, None
    action_kind = request["action_kind"]
    if action_kind == "retrieval" and usage["retrieval_calls"] >= int(budget["max_retrieval_calls"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_retrieval_calls",
                reason="Phase 04 retrieval-call budget was exhausted.",
            ),
            None,
        )
    if action_kind == "agent" and usage["agent_calls"] >= int(budget["max_agent_calls"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_agent_calls",
                reason="Phase 04 agent-call budget was exhausted.",
            ),
            None,
        )
    input_bytes = len(request["native_input"].encode("utf-8"))
    if usage["input_bytes"] + input_bytes > int(budget["max_input_bytes"]):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_input_bytes",
                reason="Phase 04 aggregate native-input budget was exhausted.",
            ),
            None,
        )
    request_bytes = len(canonical_json_bytes(request))
    result_reservation_bytes = (
        P04_RESULT_RESERVATION_MULTIPLIER * int(budget["max_output_bytes_per_attempt"])
        + P04_RESULT_RESERVATION_OVERHEAD_BYTES
    )
    if (
        usage["artifact_bytes"]
        + usage["artifact_reserved_bytes"]
        + request_bytes
        + result_reservation_bytes
        > int(budget["max_artifact_bytes"])
    ):
        return (
            _exhaust_branch(
                root,
                live,
                events,
                exhaustions,
                dimension="max_artifact_bytes",
                reason="Phase 04 artifact budget cannot admit the bound request.",
            ),
            None,
        )
    signature = _action_signature(live, request)
    if signature in failed_signatures:
        duplicate = transition_branch(
            live,
            "diagnostic",
            reason="An equivalent failed action signature is already recorded.",
        )
        root = _replace_branch(root, duplicate)
        _append_event(
            events,
            kind="duplicate_failed_signature",
            branch=duplicate,
            reason="An equivalent failed action signature is already recorded.",
        )
        return root, None

    running = transition_branch(
        live,
        "running",
        reason="Exact branch request and shared resources reserved before injected execution.",
        request_ref=request["request_ref"],
    )
    root = _replace_branch(root, running)
    artifacts[request["request_ref"]] = deepcopy(request)
    usage["artifact_bytes"] += request_bytes
    usage["artifact_reserved_bytes"] += result_reservation_bytes
    usage["input_bytes"] += input_bytes
    usage["attempts_total"] += 1
    attempts_by_branch[live["id"]] = attempts_by_branch.get(live["id"], 0) + 1
    if action_kind == "retrieval":
        usage["retrieval_calls"] += 1
    if action_kind == "agent":
        usage["agent_calls"] += 1
    _append_event(
        events,
        kind="request_bound",
        branch=running,
        reason="Exact branch request and shared resources reserved before injected execution.",
        request_ref=request["request_ref"],
    )
    return root, {
        "branch_id": live["id"],
        "request": request,
        "signature": signature,
        "result_reservation_bytes": result_reservation_bytes,
    }


def _settle_branch_action(
    root: dict[str, Any],
    reservation: dict[str, Any],
    raw_result: dict[str, Any] | list[dict[str, Any]],
    output_bytes: int,
    *,
    budget: Mapping[str, int | float],
    usage: dict[str, int],
    artifacts: dict[str, dict[str, Any]],
    events: list[dict[str, Any]],
    exhaustions: list[dict[str, Any]],
    failed_signatures: set[str],
    expander: Callable[[dict[str, Any], dict[str, Any]], list[dict[str, Any]]] | None,
) -> dict[str, Any]:
    request = reservation["request"]
    signature = reservation["signature"]
    running = _find_branch(root, reservation["branch_id"])
    if running is None or running["state"] != "running":
        raise ValueError("reserved Phase 04 branch is no longer running")
    usage["output_bytes"] += output_bytes
    result_reservation_bytes = int(reservation["result_reservation_bytes"])
    if output_bytes > int(budget["max_output_bytes_per_attempt"]):
        exhausted = transition_branch(
            running,
            "budget_exhausted",
            reason="Injected result exceeded the per-attempt output budget.",
        )
        root = _replace_branch(root, exhausted)
        exhaustions.append(
            {
                "branch_id": running["id"],
                "dimension": "max_output_bytes_per_attempt",
                "reason": "Injected result exceeded the per-attempt output budget.",
            }
        )
        failed_signatures.add(signature)
        usage["artifact_reserved_bytes"] -= result_reservation_bytes
        _append_event(
            events,
            kind="budget_exhausted",
            branch=exhausted,
            reason="Injected result exceeded the per-attempt output budget.",
            request_ref=request["request_ref"],
            budget_dimension="max_output_bytes_per_attempt",
        )
        return root
    try:
        results = sorted(
            _result_records(request, raw_result),
            key=lambda item: item["result_ref"],
        )
    except ValueError as exc:
        failed = transition_branch(running, "failed", reason=str(exc))
        root = _replace_branch(root, failed)
        failed_signatures.add(signature)
        usage["artifact_reserved_bytes"] -= result_reservation_bytes
        _append_event(
            events,
            kind="result_binding_failure",
            branch=failed,
            reason=str(exc),
            request_ref=request["request_ref"],
        )
        return root
    result_bytes = sum(len(canonical_json_bytes(result)) for result in results)
    usage["artifact_reserved_bytes"] -= result_reservation_bytes
    if (
        usage["artifact_bytes"]
        + usage["artifact_reserved_bytes"]
        + result_bytes
        > int(budget["max_artifact_bytes"])
    ):
        exhausted = transition_branch(
            running,
            "budget_exhausted",
            reason="Phase 04 artifact budget cannot admit the result record.",
        )
        root = _replace_branch(root, exhausted)
        exhaustions.append(
            {
                "branch_id": running["id"],
                "dimension": "max_artifact_bytes",
                "reason": "Phase 04 artifact budget cannot admit the result record.",
            }
        )
        failed_signatures.add(signature)
        _append_event(
            events,
            kind="budget_exhausted",
            branch=exhausted,
            reason="Phase 04 artifact budget cannot admit the result record.",
            request_ref=request["request_ref"],
            budget_dimension="max_artifact_bytes",
        )
        return root
    for result in results:
        artifacts[result["result_ref"]] = deepcopy(result)
    usage["artifact_bytes"] += result_bytes
    if _results_conflict(results):
        for result in results:
            _append_event(
                events,
                kind="conflicting_result_observation",
                branch=None,
                reason="Conflicting repeated observation retained for the exact request.",
                request_ref=request["request_ref"],
                result_ref=result["result_ref"],
            )
        failed = transition_branch(
            running,
            "failed",
            reason="Conflicting repeated results were returned for one exact branch request.",
        )
        root = _replace_branch(root, failed)
        failed_signatures.add(signature)
        _append_event(
            events,
            kind="conflicting_repeated_results",
            branch=failed,
            reason="Conflicting repeated results were returned for one exact branch request.",
            request_ref=request["request_ref"],
        )
        return root

    result = results[0]
    for repeated in results[1:]:
        _append_event(
            events,
            kind="consistent_repeated_result",
            branch=None,
            reason="A consistent repeated observation was retained for the exact request.",
            request_ref=request["request_ref"],
            result_ref=repeated["result_ref"],
        )
    result_state, remaining_blockers = _state_for_result(running, result)
    updated = deepcopy(running)
    updated["blockers"] = remaining_blockers
    updated = transition_branch(
        updated,
        result_state,
        reason=result["reason"],
        result_ref=result["result_ref"],
        blocker_ids=result["closed_blocker_ids"],
    )
    root = _replace_branch(root, updated)
    _append_event(
        events,
        kind="result_recorded",
        branch=updated,
        reason=result["reason"],
        request_ref=request["request_ref"],
        result_ref=result["result_ref"],
    )
    if result_state not in {"proved", "refuted"}:
        failed_signatures.add(signature)
    if expander is not None and result_state == "diagnostic":
        children = expander(deepcopy(updated), deepcopy(result))
        if not isinstance(children, list):
            raise ValueError("expander must return a list of branch records")
        parent = deepcopy(updated)
        known = {item["id"] for item in parent["children"]}
        added_children = 0
        for child in children:
            child_errors = validate_branch_record(child)
            if child_errors:
                raise ValueError("expander returned invalid branch: " + "; ".join(child_errors))
            if child.get("parent_id") != parent["id"] or child.get("lineage", [])[:-1] != parent["lineage"]:
                raise ValueError("expander child lineage mismatch")
            if child["id"] in known:
                continue
            if child["depth"] > int(budget["max_depth"]):
                exhaustions.append(
                    {
                        "branch_id": child["id"],
                        "dimension": "max_depth",
                        "reason": "Expanded child exceeds the Phase 04 depth budget.",
                    }
                )
                continue
            if len(_walk_branches(root)) + added_children + 1 > int(budget["max_nodes"]):
                exhaustions.append(
                    {
                        "branch_id": child["id"],
                        "dimension": "max_nodes",
                        "reason": "Expanded child exceeds the Phase 04 node budget.",
                    }
                )
                continue
            parent["children"].append(deepcopy(child))
            known.add(child["id"])
            added_children += 1
        if parent["children"] != updated["children"]:
            root = _replace_branch(root, parent)
            usage["nodes"] = len(_walk_branches(root))
            _append_event(
                events,
                kind="children_expanded",
                branch=parent,
                reason="Validated child branches were attached to the exact parent.",
                result_ref=result["result_ref"],
            )
    return root


def _rank_branches(root: dict[str, Any]) -> list[str]:
    rank = {
        "proved": 0,
        "refuted": 1,
        "diagnostic": 2,
        "ready": 3,
        "open": 4,
        "formalization_blocked": 5,
        "failed": 6,
        "budget_exhausted": 7,
        "running": 8,
    }
    return [
        item["id"]
        for item in sorted(
            _walk_branches(root),
            key=lambda item: (rank.get(item["state"], 99), item["depth"], item["id"]),
        )
    ]


def run_branch_search(
    root: dict[str, Any],
    *,
    executor: Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]],
    formalizer: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    expander: Callable[[dict[str, Any], dict[str, Any]], list[dict[str, Any]]] | None = None,
    compiler: Callable[[dict[str, Any], str], dict[str, Any]] | None = None,
    budget: BranchSearchBudget | Mapping[str, Any] | str | None = None,
    schedule: str = "serial",
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Execute an injected branch-local loop; never launches an external tool."""
    if not callable(executor):
        raise TypeError("executor must be callable")
    if schedule not in {"serial", "reverse", "parallel"}:
        raise ValueError("schedule must be serial, reverse, or parallel")
    budget_value = normalize_branch_search_budget(budget)
    initial_root = deepcopy(root)
    errors = validate_branch_tree(initial_root)
    if errors:
        raise ValueError("invalid initial Phase 04 tree: " + "; ".join(errors))
    working = deepcopy(initial_root)
    events: list[dict[str, Any]] = []
    artifacts: dict[str, dict[str, Any]] = {}
    exhaustions: list[dict[str, Any]] = []
    failed_signatures: set[str] = set()
    attempts_by_branch: dict[str, int] = {}
    usage = {
        "targets": len({item["obligation_digest"] for item in _walk_branches(working)}),
        "nodes": len(_walk_branches(working)),
        "attempts_total": 0,
        "retrieval_calls": 0,
        "agent_calls": 0,
        "input_bytes": 0,
        "output_bytes": 0,
        "artifact_bytes": 0,
        "artifact_reserved_bytes": 0,
    }
    start = clock()

    allowed_targets = sorted({item["obligation_digest"] for item in _walk_branches(working)})[
        : int(budget_value["max_targets"])
    ]
    for branch in list(_walk_branches(working)):
        if branch["obligation_digest"] not in allowed_targets:
            working = _exhaust_branch(
                working,
                branch,
                events,
                exhaustions,
                dimension="max_targets",
                reason="Target lies beyond the Phase 04 target budget.",
            )
    for branch in list(_walk_branches(working)):
        live = _find_branch(working, branch["id"])
        if live is None or live["state"] in P04_TERMINAL_BRANCH_STATES:
            continue
        if live["depth"] > int(budget_value["max_depth"]):
            working = _exhaust_branch(
                working,
                live,
                events,
                exhaustions,
                dimension="max_depth",
                reason="Branch lies beyond the Phase 04 depth budget.",
            )
    ordered_nodes = sorted(_walk_branches(working), key=lambda item: (item["depth"], item["id"]))
    for branch in ordered_nodes[int(budget_value["max_nodes"]) :]:
        live = _find_branch(working, branch["id"])
        if live is not None:
            working = _exhaust_branch(
                working,
                live,
                events,
                exhaustions,
                dimension="max_nodes",
                reason="Branch lies beyond the Phase 04 node budget.",
            )

    while True:
        runnable = [item for item in _walk_branches(working) if item["state"] in {"open", "ready"}]
        runnable.sort(key=lambda item: (item["depth"], item["id"]), reverse=schedule == "reverse")
        if not runnable:
            break
        open_branches = [item for item in runnable if item["state"] == "open"]
        if open_branches:
            branch = open_branches[0]
            if clock() - start >= float(budget_value["max_wall_time_seconds"]):
                working = _exhaust_branch(
                    working,
                    branch,
                    events,
                    exhaustions,
                    dimension="max_wall_time_seconds",
                    reason="Phase 04 wall-time budget was exhausted before formalization.",
                )
                continue
            formalized = formalizer(deepcopy(branch)) if formalizer is not None else {"status": "ready"}
            if not isinstance(formalized, dict) or formalized.get("status") not in {"ready", "blocked"}:
                raise ValueError("formalizer must return status ready or blocked")
            if formalized["status"] == "blocked":
                blocked = deepcopy(branch)
                blocker = formalized.get("blocker")
                if isinstance(blocker, dict):
                    blocked["blockers"].append(deepcopy(blocker))
                blocked = transition_branch(
                    blocked,
                    "formalization_blocked",
                    reason=str(formalized.get("reason", "Formalization is blocked.")),
                    blocker_ids=[str(blocker.get("id"))]
                    if isinstance(blocker, dict) and blocker.get("id")
                    else [],
                )
                working = _replace_branch(working, blocked)
                _append_event(
                    events,
                    kind="formalization_blocked",
                    branch=blocked,
                    reason=str(formalized.get("reason", "Formalization is blocked.")),
                )
                continue
            ready = transition_branch(
                branch,
                "ready",
                reason="Branch formalization validated for injected execution.",
            )
            working = _replace_branch(working, ready)
            _append_event(
                events,
                kind="formalization_ready",
                branch=ready,
                reason="Branch formalization validated for injected execution.",
            )
            continue

        ready_branches = [item for item in runnable if item["state"] == "ready"]
        candidates = ready_branches if schedule == "parallel" else ready_branches[:1]
        reservations: list[dict[str, Any]] = []
        for branch in candidates:
            working, reservation = _reserve_branch_action(
                working,
                branch,
                budget=budget_value,
                usage=usage,
                attempts_by_branch=attempts_by_branch,
                artifacts=artifacts,
                events=events,
                exhaustions=exhaustions,
                failed_signatures=failed_signatures,
                start=start,
                clock=clock,
            )
            if reservation is not None:
                reservations.append(reservation)
        if not reservations:
            continue

        executed: dict[str, tuple[dict[str, Any] | list[dict[str, Any]], int]] = {}
        if schedule == "parallel" and len(reservations) > 1:
            with ThreadPoolExecutor(max_workers=len(reservations)) as pool:
                futures = {
                    reservation["branch_id"]: pool.submit(
                        _execute_injected_action,
                        executor,
                        reservation["request"],
                    )
                    for reservation in reservations
                }
                for branch_id, future in futures.items():
                    executed[branch_id] = future.result()
        else:
            for reservation in reservations:
                executed[reservation["branch_id"]] = _execute_injected_action(
                    executor,
                    reservation["request"],
                )
        for reservation in reservations:
            raw_result, output_bytes = executed[reservation["branch_id"]]
            working = _settle_branch_action(
                working,
                reservation,
                raw_result,
                output_bytes,
                budget=budget_value,
                usage=usage,
                artifacts=artifacts,
                events=events,
                exhaustions=exhaustions,
                failed_signatures=failed_signatures,
                expander=expander,
            )

    validation_errors = validate_branch_tree(working)
    if validation_errors:
        raise ValueError("invalid final Phase 04 tree: " + "; ".join(validation_errors))
    replayed = replay_branch_events(initial_root, events)
    final_digest = branch_tree_semantic_digest(working)
    replay_digest = branch_tree_semantic_digest(replayed)
    if replay_digest != final_digest:
        raise ValueError("Phase 04 event replay does not reconstruct the final tree")
    compilation = (
        compiler(deepcopy(working), final_digest)
        if compiler is not None
        else {
            "status": "compiled_final_tree",
            "final_tree_digest": final_digest,
            "publication_mode": "disabled",
            "ranked_branch_ids": _rank_branches(working),
        }
    )
    if not isinstance(compilation, dict):
        raise ValueError("compiler must return an object")
    if compilation.get("final_tree_digest") != final_digest:
        raise ValueError("compiler did not bind the final Phase 04 tree digest")
    if compilation.get("publication_mode") != "disabled":
        raise ValueError("Phase 04 compilation must keep publication disabled")
    result = {
        "status": "pass" if not validation_errors else "invalid",
        "initial_tree": initial_root,
        "final_tree": working,
        "final_tree_digest": final_digest,
        "event_log": events,
        "event_log_terminal_digest": events[-1]["event_digest"] if events else None,
        "replay_tree_digest": replay_digest,
        "artifacts": artifacts,
        "budget": budget_value,
        "usage": usage,
        "budget_exhaustions": exhaustions,
        "failed_action_signatures": sorted(failed_signatures),
        "ranking": _rank_branches(working),
        "compilation": compilation,
        "publication_mode": "disabled",
        "backend_execution_mode": "injected_parallel" if schedule == "parallel" else "injected_only",
        "validation_errors": validation_errors,
        "boundary": P04_BOUNDARY,
        "non_claims": [
            "Injected executor outcomes are not mathematical certification.",
            "Budget exhaustion and timeout are not mathematical refutation.",
            "No live backend, model, network, source edit, or publication action is performed.",
        ],
    }
    return attach_contract(result, P04_ORCHESTRATOR_CONTRACT)
