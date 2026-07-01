from __future__ import annotations

"""Question-centered bounded derivation/refutation workflow."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .assumption_discovery import assumptions_required
from .counterexample_search import find_counterexample
from .contracts import attach_contract
from .math_debugging import math_question, workbench_obligation, workbench_result
from .math_debugging_router import route_math_obligation


@dataclass(frozen=True)
class DeriveOrRefuteResult:
    status: str
    reason: str
    givens: list[str]
    target: str
    lhs: str
    rhs: str
    route_decision: dict[str, Any]
    assumption_diagnostic: dict[str, Any]
    counterexample_search: dict[str, Any] | None
    workbench_result: dict[str, Any]


def _split_target(target: str, lhs: str | None, rhs: str | None) -> tuple[str, str]:
    if lhs is not None and rhs is not None:
        return lhs, rhs
    if "=" not in target:
        raise ValueError("derive_or_refute requires lhs/rhs or a target containing '='")
    left, right = target.split("=", 1)
    if not left.strip() or not right.strip():
        raise ValueError("target must contain non-empty lhs and rhs")
    return left.strip(), right.strip()


_OPAQUE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def semantic_placeholder_equality(lhs: str, rhs: str) -> bool:
    """Detect label-like semantic placeholders that need source evidence.

    Finite-domain substitution is meaningful for algebraic expressions such as
    ``x + 1 = x + 2``. It is not meaningful for opaque names like
    ``value_only_likelihood = hmc_production_readiness``; assigning arbitrary
    integers to those labels creates a fake counterexample.
    """
    if lhs == rhs:
        return False
    if not (_OPAQUE_IDENTIFIER.fullmatch(lhs.strip()) and _OPAQUE_IDENTIFIER.fullmatch(rhs.strip())):
        return False
    return "_" in lhs or "_" in rhs


def derive_or_refute(
    target: str,
    *,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
) -> dict:
    left, right = _split_target(target, lhs, rhs)
    given_list = givens or []
    assumption_list = assumptions or []
    semantic_placeholder = semantic_placeholder_equality(left, right)
    assumption_diagnostic = assumptions_required(target, provided_assumptions=assumption_list)
    if semantic_placeholder and not assumption_diagnostic.get("missing_assumptions"):
        semantic_assumption = {
            "text": "source-backed semantic assumptions linking the opaque placeholders are required",
            "status": "missing",
            "source": "semantic_placeholder_route",
            "necessity": "required_by_route",
            "used_by": ["semantic_placeholder_equality"],
        }
        assumption_diagnostic = dict(assumption_diagnostic)
        assumption_diagnostic["status"] = "missing_assumptions"
        assumption_diagnostic["reason"] = "Opaque semantic placeholders require source-backed assumptions."
        assumption_diagnostic["assumptions"] = [*assumption_diagnostic.get("assumptions", []), semantic_assumption]
        assumption_diagnostic["missing_assumptions"] = [*assumption_diagnostic.get("missing_assumptions", []), semantic_assumption]
    route = route_math_obligation(left, right, assumptions=assumption_list, backend=backend)

    counterexample = None
    if route["status"] not in {"proved", "refuted"} and not semantic_placeholder:
        counterexample = find_counterexample(left, right)

    if route["status"] == "proved":
        status = "proved"
        reason = "The bounded target obligation was certified by the routed backend."
    elif route["status"] == "refuted":
        status = "refuted"
        reason = "The bounded target obligation was refuted by the routed backend."
    elif counterexample is not None and counterexample["status"] == "refuted":
        status = "refuted"
        reason = "A bounded counterexample refuted the target obligation."
    elif assumption_diagnostic["status"] == "missing_assumptions":
        status = "missing_assumptions"
        reason = "The target has missing route-required assumptions."
    elif route["status"] in {"not_encodable", "backend_unavailable"}:
        status = route["status"]
        reason = route["reason"]
    elif semantic_placeholder:
        status = "missing_assumptions" if not assumption_list else "unknown"
        reason = "The target uses opaque semantic placeholders and needs explicit source-backed assumptions before derivation or refutation."
    else:
        status = "unknown"
        reason = "No bounded derivation or refutation was found."

    question = math_question(
        "derive_or_refute",
        target,
        givens=given_list,
        assumptions=assumption_list,
        context={"backend": backend},
    )
    obligations = [
        workbench_obligation(
            "derive-target-1",
            lhs=left,
            rhs=right,
            status=status,
            reason=reason,
            assumptions=assumption_list,
            backend_attempts=[route["backend_attempt"]] if route.get("backend_attempt") else [],
            counterexample=counterexample.get("counterexample") if counterexample else None,
            missing_assumptions=assumption_diagnostic.get("missing_assumptions", []),
        )
    ]
    backend_attempts = [route["backend_attempt"]] if route.get("backend_attempt") else []
    counterexamples = []
    if counterexample and counterexample.get("counterexample"):
        counterexamples.append(counterexample["counterexample"])
    actions = []
    if status == "missing_assumptions":
        actions.extend(assumption_diagnostic["workbench_result"].get("actions", []))
        if semantic_placeholder and not assumption_diagnostic["workbench_result"].get("actions"):
            actions.append({"kind": "supply_source_backed_assumptions", "reason": "Opaque semantic placeholders cannot be refuted by finite-domain substitution."})
    if status == "unknown":
        actions.append({"kind": "manual_derivation_or_stronger_backend", "reason": "No bounded route resolved the target."})
        if semantic_placeholder:
            actions.append({"kind": "supply_source_backed_semantic_route", "reason": "Provide a source adapter, formalization, or explicit assumptions for the semantic placeholders."})
    workbench = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=obligations,
        assumptions=assumption_diagnostic.get("assumptions", []),
        backend_attempts=backend_attempts,
        counterexamples=counterexamples,
        actions=actions,
    )
    return attach_contract(
        asdict(
            DeriveOrRefuteResult(
                status=status,
                reason=reason,
                givens=given_list,
                target=target,
                lhs=left,
                rhs=right,
                route_decision=route,
                assumption_diagnostic=assumption_diagnostic,
                counterexample_search=counterexample,
                workbench_result=workbench,
            )
        ),
        "derive_or_refute_result",
    )
