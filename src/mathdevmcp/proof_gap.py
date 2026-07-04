from __future__ import annotations

"""Localize the first unsupported or refuted step in a bounded derivation chain."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .math_debugging import math_question, workbench_result
from .prove_or_refute import prove_or_refute


@dataclass(frozen=True)
class ProofGapResult:
    status: str
    reason: str
    steps: list[str]
    step_results: list[dict[str, Any]]
    first_gap: dict[str, Any] | None
    workbench_result: dict[str, Any]


def _step_status(result: dict[str, Any]) -> str:
    status = result.get("status")
    if status == "proved":
        return "proved"
    if status == "refuted":
        return "refuted"
    if status == "missing_assumptions":
        return "missing_assumptions"
    if status in {"not_encodable", "backend_unavailable"}:
        return str(status)
    return "unknown"


def localize_proof_gap(steps: list[str], *, assumptions: list[str] | None = None, backend: str = "auto") -> dict:
    if len(steps) < 2:
        raise ValueError("localize_proof_gap requires at least two derivation steps")
    assumption_list = assumptions or []
    step_results: list[dict[str, Any]] = []
    first_gap: dict[str, Any] | None = None
    for index, (lhs, rhs) in enumerate(zip(steps, steps[1:], strict=False)):
        result = prove_or_refute(f"{lhs} = {rhs}", assumptions=assumption_list, backend=backend)
        status = _step_status(result)
        step_record = {
            "index": index,
            "lhs": lhs,
            "rhs": rhs,
            "status": status,
            "reason": result["reason"],
            "result": result,
        }
        step_results.append(step_record)
        if status != "proved":
            first_gap = step_record
            break

    if first_gap is None:
        status = "proved"
        reason = "Every adjacent derivation step was certified by bounded backend evidence."
    elif first_gap["status"] == "refuted":
        status = "refuted"
        reason = f"Step {first_gap['index']} was refuted by bounded evidence."
    elif first_gap["status"] == "missing_assumptions":
        status = "missing_assumptions"
        reason = f"Step {first_gap['index']} has missing route-required assumptions."
    else:
        status = "unknown"
        reason = f"Step {first_gap['index']} is not certified; later steps are not promoted."

    question = math_question("localize_proof_gap", " -> ".join(steps), assumptions=assumption_list)
    obligations = [record["result"]["workbench_result"]["obligations"][0] for record in step_results]
    backend_attempts = [
        attempt
        for record in step_results
        for attempt in record["result"]["workbench_result"].get("backend_attempts", [])
    ]
    counterexamples = [
        example
        for record in step_results
        for example in record["result"]["workbench_result"].get("counterexamples", [])
    ]
    actions = []
    if first_gap is not None:
        actions.append(
            {
                "kind": "repair_or_justify_first_gap",
                "step_index": first_gap["index"],
                "status": first_gap["status"],
                "reason": first_gap["reason"],
            }
        )
    workbench = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=obligations,
        backend_attempts=backend_attempts,
        counterexamples=counterexamples,
        actions=actions,
    )
    return attach_contract(
        asdict(
            ProofGapResult(
                status=status,
                reason=reason,
                steps=steps,
                step_results=step_results,
                first_gap=first_gap,
                workbench_result=workbench,
            )
        ),
        "proof_gap_result",
    )
