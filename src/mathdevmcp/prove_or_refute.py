from __future__ import annotations

"""Bounded prove/refute workflow for identities and explicitly supplied Lean claims."""

from dataclasses import asdict, dataclass
from typing import Any

from .counterexample_search import find_counterexample
from .contracts import attach_contract
from .derive_or_refute import _split_target, semantic_placeholder_equality
from .math_debugging import math_question, workbench_obligation, workbench_result
from .math_debugging_router import route_math_obligation


@dataclass(frozen=True)
class ProveOrRefuteResult:
    status: str
    reason: str
    claim: str
    lhs: str
    rhs: str
    route_decision: dict[str, Any]
    counterexample_search: dict[str, Any] | None
    workbench_result: dict[str, Any]


def prove_or_refute(
    claim: str,
    *,
    assumptions: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
) -> dict:
    left, right = _split_target(claim, lhs, rhs)
    assumption_list = assumptions or []
    semantic_placeholder = semantic_placeholder_equality(left, right)
    route = route_math_obligation(left, right, assumptions=assumption_list, backend=backend, lean_source=lean_source)
    counterexample = None
    if route["status"] not in {"proved", "refuted", "backend_unavailable"} and not semantic_placeholder:
        counterexample = find_counterexample(left, right)

    if route["status"] == "proved":
        status = "proved"
        reason = "The scoped claim was certified by the routed backend."
    elif route["status"] == "refuted":
        status = "refuted"
        reason = "The scoped claim was refuted by the routed backend."
    elif counterexample is not None and counterexample["status"] == "refuted":
        status = "refuted"
        reason = "A bounded counterexample refuted the scoped claim."
    elif route["status"] in {"backend_unavailable", "not_encodable"}:
        status = route["status"]
        reason = route["reason"]
    elif semantic_placeholder:
        status = "unknown"
        reason = "The claim uses opaque semantic placeholders and needs explicit source or formal evidence before proof or refutation."
    else:
        status = "unknown"
        reason = "No bounded proof or refutation was found."

    question = math_question("prove_or_refute", claim, assumptions=assumption_list, context={"backend": backend})
    obligation = workbench_obligation(
        "prove-target-1",
        lhs=left,
        rhs=right,
        status=status,
        reason=reason,
        assumptions=assumption_list,
        backend_attempts=[route["backend_attempt"]] if route.get("backend_attempt") else [],
        counterexample=counterexample.get("counterexample") if counterexample else None,
    )
    counterexamples = [counterexample["counterexample"]] if counterexample and counterexample.get("counterexample") else []
    workbench = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=[obligation],
        backend_attempts=[route["backend_attempt"]] if route.get("backend_attempt") else [],
        counterexamples=counterexamples,
        actions=[] if status in {"proved", "refuted"} else [
            {
                "kind": "supply_source_backed_semantic_route" if semantic_placeholder else "manual_formalization_or_backend_review",
                "reason": "Opaque semantic placeholders cannot be refuted by finite-domain substitution."
                if semantic_placeholder
                else "No bounded proof or refutation was found.",
            }
        ],
    )
    return attach_contract(
        asdict(
            ProveOrRefuteResult(
                status=status,
                reason=reason,
                claim=claim,
                lhs=left,
                rhs=right,
                route_decision=route,
                counterexample_search=counterexample,
                workbench_result=workbench,
            )
        ),
        "prove_or_refute_result",
    )
