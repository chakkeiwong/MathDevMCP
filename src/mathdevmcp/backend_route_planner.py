from __future__ import annotations

"""Non-certifying backend route plans for extracted derivation targets."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .doctor import doctor_report
from .external_tool_policy import external_tool_first_plan


BACKEND_ROUTE_PLAN_CONTRACT = "backend_route_plan_result"
BACKEND_ROUTE_PLAN_BOUNDARY = (
    "Route planning is diagnostic only. A route candidate is not a proof, "
    "refutation, or validated derivation unless a scoped backend certificate "
    "or concrete counterexample is recorded by a downstream tool."
)


@dataclass(frozen=True)
class RouteCandidate:
    id: str
    backend: str
    route_type: str
    status: str
    purpose: str
    reason: str
    tool: str
    evidence_contract: str
    deterministic: bool
    expected_artifact: str
    validation_boundary: str
    capability: dict[str, Any] | None = None


_SCALAR_SYMBOLIC = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")
_MATRIX_OR_DOMAIN = re.compile(
    r"\\(?:E|mathbb|frac|left|right|mid|beta|star|widetilde|bar)|"
    r"\b(?:logdet|trace|tr|det|matrix|conditional|expectation)\b|"
    r"[A-Z][A-Za-z0-9_]*|['^]"
)
_FORMALIZATION_HINT = re.compile(r"\\|\\E|\\frac|\\mid|\\star|\\widetilde|\\bar")


def _status_from_capability(capability: dict[str, Any] | None) -> str:
    if not capability:
        return "unavailable"
    return "available" if capability.get("available") else "unavailable"


def _candidate(
    *,
    backend: str,
    route_type: str,
    status: str,
    purpose: str,
    reason: str,
    tool: str,
    evidence_contract: str,
    expected_artifact: str,
    capability: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate = RouteCandidate(
        id=f"{backend}:{route_type}",
        backend=backend,
        route_type=route_type,
        status=status,
        purpose=purpose,
        reason=reason,
        tool=tool,
        evidence_contract=evidence_contract,
        deterministic=True,
        expected_artifact=expected_artifact,
        validation_boundary=BACKEND_ROUTE_PLAN_BOUNDARY,
        capability=capability,
    )
    return asdict(candidate)


def _target_parts(target: dict[str, Any] | str, lhs: str | None, rhs: str | None) -> tuple[str, str, str]:
    if isinstance(target, dict):
        target_text = str(target.get("target", ""))
        left = str(lhs if lhs is not None else target.get("lhs", ""))
        right = str(rhs if rhs is not None else target.get("rhs", ""))
    else:
        target_text = str(target)
        left = lhs or ""
        right = rhs or ""
    if not left and not right and "=" in target_text:
        left, right = target_text.split("=", 1)
    return target_text.strip(), left.strip(), right.strip()


def _selected_route(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    for status in ("ready_to_attempt", "available", "requires_formalization", "unavailable"):
        for candidate in candidates:
            if candidate.get("status") == status:
                return candidate
    return candidates[0] if candidates else None


def _symbolic_candidate(lhs: str, rhs: str, *, sympy_capability: dict[str, Any] | None) -> dict[str, Any]:
    if _MATRIX_OR_DOMAIN.search(lhs) or _MATRIX_OR_DOMAIN.search(rhs):
        status = "not_applicable"
        reason = "Matrix/domain hints require review before scalar symbolic routing."
    elif _SCALAR_SYMBOLIC.fullmatch(lhs) and _SCALAR_SYMBOLIC.fullmatch(rhs):
        status = "ready_to_attempt" if _status_from_capability(sympy_capability) == "available" else "unavailable"
        reason = (
            "The lhs/rhs are inside the conservative scalar grammar for SymPy."
            if status == "ready_to_attempt"
            else "The lhs/rhs are scalar-looking, but SymPy is unavailable."
        )
    else:
        status = "not_applicable"
        reason = "The lhs/rhs use notation outside the conservative scalar grammar."
    return _candidate(
        backend="sympy",
        route_type="symbolic_identity",
        status=status,
        purpose="Try bounded symbolic equivalence/refutation for scalar algebra.",
        reason=reason,
        tool="derive_or_refute",
        evidence_contract="derive_or_refute_result",
        expected_artifact="backend_attempt with certifying/blocking evidence only if the backend resolves the scoped obligation",
        capability=sympy_capability,
    )


def _counterexample_candidate(lhs: str, rhs: str, *, sympy_capability: dict[str, Any] | None) -> dict[str, Any]:
    if lhs and rhs and (_SCALAR_SYMBOLIC.fullmatch(lhs) and _SCALAR_SYMBOLIC.fullmatch(rhs) or {lhs.replace(" ", ""), rhs.replace(" ", "")} == {"A*B", "B*A"}):
        status = "ready_to_attempt" if _status_from_capability(sympy_capability) == "available" else "unavailable"
        reason = (
            "A bounded finite-domain or fixed matrix counterexample search can be attempted."
            if status == "ready_to_attempt"
            else "Counterexample search depends on SymPy for scalar finite-domain probes and it is unavailable."
        )
    elif lhs and rhs:
        status = "requires_formalization"
        reason = "The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it."
    else:
        status = "not_applicable"
        reason = "Counterexample search needs non-empty lhs and rhs."
    return _candidate(
        backend="bounded_counterexample",
        route_type="counterexample_search",
        status=status,
        purpose="Search for a scoped concrete counterexample before accepting unknown equality.",
        reason=reason,
        tool="find_counterexample",
        evidence_contract="counterexample_search_result",
        expected_artifact="concrete counterexample object for any promoted refutation",
        capability=sympy_capability,
    )


def _sage_candidate(lhs: str, rhs: str, *, sage_capability: dict[str, Any] | None) -> dict[str, Any]:
    status = _status_from_capability(sage_capability)
    if not (_MATRIX_OR_DOMAIN.search(lhs) or _MATRIX_OR_DOMAIN.search(rhs)):
        route_status = "not_applicable"
        reason = "No matrix/domain notation was detected for a Sage-oriented route."
    elif _FORMALIZATION_HINT.search(lhs) or _FORMALIZATION_HINT.search(rhs):
        route_status = "requires_formalization" if status == "available" else "unavailable"
        reason = (
            "Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized."
            if route_status == "requires_formalization"
            else "Matrix/domain notation suggests Sage could help after formalization, but Sage is unavailable in this environment."
        )
    else:
        route_status = "available" if status == "available" else "unavailable"
        reason = (
            "Matrix/domain notation suggests a Sage route may be useful."
            if route_status == "available"
            else "Matrix/domain notation suggests Sage could help, but Sage is unavailable in this environment."
        )
    return _candidate(
        backend="sage",
        route_type="matrix_domain_symbolic",
        status=route_status,
        purpose="Use a deterministic CAS route for matrix/domain algebra when formalized.",
        reason=reason,
        tool="derive_or_refute",
        evidence_contract="derive_or_refute_result",
        expected_artifact="backend_attempt recording Sage availability or a scoped Sage result",
        capability=sage_capability,
    )


def _lean_candidate(target_text: str, lhs: str, rhs: str, *, lean_capability: dict[str, Any] | None) -> dict[str, Any]:
    needs_formalization = bool(_FORMALIZATION_HINT.search(target_text) or not (lhs and rhs))
    route_status = "requires_formalization" if needs_formalization else _status_from_capability(lean_capability)
    reason = (
        "The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything."
        if needs_formalization
        else "Lean is available for explicit Lean source."
        if route_status == "available"
        else "Lean would require explicit Lean source, and the executable is unavailable."
    )
    return _candidate(
        backend="lean",
        route_type="formal_proof",
        status=route_status,
        purpose="Check an explicit formalization when a Lean statement/proof is supplied.",
        reason=reason,
        tool="lean_check",
        evidence_contract="lean_check_result",
        expected_artifact="Lean source hash and lean_verified evidence before any formal proof claim",
        capability=lean_capability,
    )


def plan_backend_routes(
    target: dict[str, Any] | str,
    *,
    lhs: str | None = None,
    rhs: str | None = None,
    capabilities: dict[str, Any] | None = None,
    integrations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Plan deterministic backend routes without executing proof attempts."""
    target_text, left, right = _target_parts(target, lhs, rhs)
    if capabilities is None:
        doctor = doctor_report()
        capability_report = doctor.get("capabilities", {})
        integration_report = integrations if integrations is not None else doctor.get("integrations", {})
    else:
        capability_report = capabilities
        integration_report = integrations if integrations is not None else {}
    sympy_capability = capability_report.get("sympy") if isinstance(capability_report, dict) else None
    sage_capability = capability_report.get("sage") if isinstance(capability_report, dict) else None
    lean_capability = capability_report.get("lean") if isinstance(capability_report, dict) else None
    external_policy_plan = external_tool_first_plan(
        target_text,
        goal_kind="derivation",
        capabilities=capability_report if isinstance(capability_report, dict) else {},
        integrations=integration_report if isinstance(integration_report, dict) else {},
    )
    candidates = [
        _symbolic_candidate(left, right, sympy_capability=sympy_capability),
        _counterexample_candidate(left, right, sympy_capability=sympy_capability),
        _sage_candidate(left, right, sage_capability=sage_capability),
        _lean_candidate(target_text, left, right, lean_capability=lean_capability),
    ]
    selected = _selected_route(candidates)
    diagnostics = {
        "candidate_count": len(candidates),
        "ready_count": sum(1 for candidate in candidates if candidate["status"] in {"ready_to_attempt", "available"}),
        "unavailable_count": sum(1 for candidate in candidates if candidate["status"] == "unavailable"),
        "requires_formalization_count": sum(1 for candidate in candidates if candidate["status"] == "requires_formalization"),
    }
    result = {
        "status": "planned" if candidates else "not_planned",
        "target": target_text,
        "lhs": left,
        "rhs": right,
        "selected_route": selected,
        "candidates": candidates,
        "external_tool_first_plan": external_policy_plan,
        "diagnostics": diagnostics,
        "boundary": BACKEND_ROUTE_PLAN_BOUNDARY,
        "non_claims": [
            {
                "code": "route_plan_not_certificate",
                "text": BACKEND_ROUTE_PLAN_BOUNDARY,
            }
        ],
    }
    return attach_contract(result, BACKEND_ROUTE_PLAN_CONTRACT)
