from __future__ import annotations

"""Bounded prove/refute workflow for identities and explicitly supplied Lean claims."""

from dataclasses import asdict, dataclass
from typing import Any

from .counterexample_search import find_counterexample
from .contracts import attach_contract
from .claim_semantics import source_role_controls_routing, validate_claim_semantics
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
    claim_semantics: dict[str, Any]


def prove_or_refute(
    claim: str,
    *,
    assumptions: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
    claim_semantics: dict[str, Any] | None = None,
) -> dict:
    left, right = _split_target(claim, lhs, rhs)
    assumption_list = assumptions or []
    routed_target = claim if lhs is None and rhs is None else f"{left} = {right}"
    semantics = validate_claim_semantics(claim_semantics, routed_target=routed_target)
    semantic_placeholder = semantic_placeholder_equality(left, right)
    source_role_route = source_role_controls_routing(semantics)
    role_blocked = semantics["routing_effect"] == "block_pending_source_role_evidence"
    if source_role_route or role_blocked:
        route = {
            "route": "source_semantics",
            "status": "source_defined" if source_role_route else "inconclusive",
            "reason": semantics["reason"],
            "backend_attempt": {
                "backend": "source_semantics",
                "status": "source_defined" if source_role_route else "inconclusive",
                "reason": semantics["reason"],
                "evidence": [semantics],
                "severity": "diagnostic",
            },
        }
    else:
        route = route_math_obligation(left, right, assumptions=assumption_list, backend=backend, lean_source=lean_source)
    counterexample = None
    if (
        route["status"] not in {"proved", "refuted", "backend_unavailable"}
        and not semantic_placeholder
        and not source_role_route
        and not role_blocked
    ):
        counterexample = find_counterexample(left, right)

    if source_role_route:
        status = "source_defined"
        reason = "The exact source establishes this target as a definition or identity; theorem refutation is inapplicable, and domain validation remains separate."
    elif role_blocked:
        status = "inconclusive"
        reason = semantics["reason"]
    elif route["status"] == "proved":
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

    question = math_question("prove_or_refute", claim, assumptions=assumption_list, context={"backend": backend, "claim_semantics": semantics})
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
                "kind": "formalize_source_definition_domain"
                if source_role_route
                else "supply_source_role_evidence"
                if role_blocked
                else "supply_source_backed_semantic_route"
                if semantic_placeholder
                else "manual_formalization_or_backend_review",
                "reason": reason,
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
                claim_semantics=semantics,
            )
        ),
        "prove_or_refute_result",
    )
