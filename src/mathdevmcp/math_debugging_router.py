from __future__ import annotations

"""Conservative backend routing for math debugging obligations."""

from dataclasses import asdict, dataclass
from importlib.util import find_spec
import re
from typing import Any

from .contracts import attach_contract
from .lean_check import check_lean_source
from .math_debugging import backend_attempt_record, math_question, workbench_obligation, workbench_result
from .proof_obligations import check_proof_obligation


_MATRIX_HINT = re.compile(r"\\|@|\b(det|logdet|trace|tr|inv|solve|transpose|matrix)\b|[A-Z][A-Za-z0-9_]*")
_UNSAFE_HINT = re.compile(r"__|;|`|\[|\]|\{|\}|=")


@dataclass(frozen=True)
class RouteDecision:
    route: str
    status: str
    reason: str
    backend_attempt: dict[str, Any] | None
    obligation: dict[str, Any] | None
    result: dict[str, Any]


def _status_from_proof_obligation(status: str) -> str:
    if status == "equivalent":
        return "proved"
    if status == "mismatch":
        return "refuted"
    if status == "inconclusive":
        return "not_encodable"
    return "unknown"


def _severity_from_workbench_status(status: str) -> str:
    if status == "proved":
        return "certifying"
    if status == "refuted":
        return "blocking"
    return "diagnostic"


def _module_available(name: str) -> bool:
    try:
        return find_spec(name) is not None
    except ModuleNotFoundError:
        return False


def _route_result(route: str, status: str, reason: str, *, lhs: str, rhs: str, backend_attempt: dict[str, Any] | None = None) -> dict:
    question = math_question("route_obligation", f"{lhs} == {rhs}", context={"route": route})
    obligation = workbench_obligation(
        "route-obligation-1",
        lhs=lhs,
        rhs=rhs,
        status=status,
        reason=reason,
        backend_attempts=[backend_attempt] if backend_attempt else [],
    )
    result = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=[obligation],
        backend_attempts=[backend_attempt] if backend_attempt else [],
        actions=[] if status in {"proved", "refuted"} else [{"kind": "review_or_reencode", "route": route}],
    )
    return attach_contract(
        asdict(
            RouteDecision(
                route=route,
                status=status,
                reason=reason,
                backend_attempt=backend_attempt,
                obligation=obligation,
                result=result,
            )
        ),
        "math_debugging_route_decision",
    )


def route_math_obligation(
    lhs: str,
    rhs: str,
    *,
    assumptions: list[str] | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
) -> dict:
    assumption_list = assumptions or []
    if backend == "lean" or lean_source is not None:
        if not lean_source:
            attempt = backend_attempt_record(
                backend="lean",
                status="not_encodable",
                reason="Lean route requires explicit Lean source.",
                severity="diagnostic",
            )
            return _route_result("lean", "not_encodable", attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)
        lean = check_lean_source(lean_source, allow_sorry=False)
        evidence = lean.get("evidence", [])
        if lean.get("status") == "verified":
            status = "proved"
            severity = "certifying"
        elif lean.get("status") == "mismatch":
            status = "refuted"
            severity = "blocking"
        else:
            status = "backend_unavailable" if any(item.get("kind") == "lean_unavailable" for item in evidence) else "unknown"
            severity = "diagnostic"
        attempt = backend_attempt_record(
            backend="lean",
            status=status,
            reason=lean.get("reason", "Lean route completed without a certificate."),
            evidence=evidence,
            severity=severity,
        )
        return _route_result("lean", status, attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)

    if backend == "sage":
        sage_available = _module_available("sageall") or _module_available("sage.all")
        attempt = backend_attempt_record(
            backend="sage",
            status="unknown" if sage_available else "backend_unavailable",
            reason="Sage route is available for future bounded adapters." if sage_available else "Sage Python module is not importable.",
            severity="diagnostic",
        )
        status = "unknown" if sage_available else "backend_unavailable"
        return _route_result("sage", status, attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)

    if backend == "z3":
        attempt = backend_attempt_record(
            backend="z3",
            status="not_encodable",
            reason="Z3 route is not implemented for this bounded workbench slice.",
            severity="diagnostic",
        )
        return _route_result("z3", "not_encodable", attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)

    if _UNSAFE_HINT.search(lhs) or _UNSAFE_HINT.search(rhs):
        attempt = backend_attempt_record(
            backend="router",
            status="not_encodable",
            reason="Expression contains syntax outside the conservative router grammar.",
            severity="diagnostic",
        )
        return _route_result("human_review", "not_encodable", attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)

    if _MATRIX_HINT.search(lhs) or _MATRIX_HINT.search(rhs):
        attempt = backend_attempt_record(
            backend="router",
            status="unknown",
            reason="Expression appears to require matrix/domain review before scalar symbolic routing.",
            severity="diagnostic",
        )
        return _route_result("human_review", "unknown", attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)

    proof = check_proof_obligation(lhs, rhs, assumptions=assumption_list, backend="sympy" if backend in {"auto", "sympy"} else backend)
    status = _status_from_proof_obligation(proof.get("status", "inconclusive"))
    attempt = backend_attempt_record(
        backend=str(proof.get("backend", "sympy")),
        status=status,
        reason=str(proof.get("reason", "Backend attempt completed.")),
        evidence=proof.get("evidence", []),
        severity=_severity_from_workbench_status(status),
    )
    route = "symbolic" if status in {"proved", "refuted", "unknown"} else "human_review"
    return _route_result(route, status, attempt["reason"], lhs=lhs, rhs=rhs, backend_attempt=attempt)
