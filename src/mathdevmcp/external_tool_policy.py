from __future__ import annotations

"""External-tool-first policy records for mathematical search workflows."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .doctor import doctor_report
from .integration_versions import SUPPORTED_INTEGRATION_TOOLS


EXTERNAL_TOOL_FIRST_PLAN_CONTRACT = "external_tool_first_plan_result"
EXTERNAL_TOOL_FIRST_BOUNDARY = (
    "This plan is a routing and governance artifact. It is not a proof, "
    "refutation, derivation, or backend certificate."
)
IN_HOUSE_GAP_REQUIRED = (
    "MathDevMCP-native search may only expand a branch after this plan records "
    "why direct external tools are unavailable, inapplicable, insufficiently "
    "scoped, or require formalization first."
)


@dataclass(frozen=True)
class ToolConsideration:
    tool: str
    role: str
    status: str
    priority: int
    reason: str
    evidence_kind: str
    certification_boundary: str
    version: str | None = None
    supported_version: str | None = None
    version_status: str | None = None
    environment_scope: str | None = None
    install_hint: str | None = None


GOAL_KIND_ALIASES: dict[str, str] = {
    "derive": "derivation",
    "derivation": "derivation",
    "proof": "formal_proof",
    "formal_proof": "formal_proof",
    "prove": "formal_proof",
    "premise": "premise_search",
    "premise_search": "premise_search",
    "assumption": "missing_assumptions",
    "assumptions": "missing_assumptions",
    "missing_assumptions": "missing_assumptions",
    "document_repair": "document_repair",
    "repair": "document_repair",
}

GOAL_TOOL_ORDER: dict[str, tuple[str, ...]] = {
    "derivation": ("sympy", "sage", "lean", "leansearchv2", "lean_explore", "jixia", "pantograph", "lean_dojo"),
    "formal_proof": ("lean", "leansearchv2", "lean_explore", "jixia", "pantograph", "lean_dojo"),
    "premise_search": ("leansearchv2", "lean_explore", "jixia"),
    "missing_assumptions": ("jixia", "leansearchv2", "lean_explore", "sympy", "sage", "lean"),
    "document_repair": ("sympy", "sage", "lean", "leansearchv2", "lean_explore", "jixia", "pantograph", "lean_dojo"),
}

TOOL_ROLES: dict[str, str] = {
    "sympy": "Deterministic symbolic algebra, scalar equality, and bounded simplification checks.",
    "sage": "Deterministic CAS route for matrix/domain algebra, calculus, and richer symbolic checks.",
    "lean": "Final formal certification for explicit Lean source.",
    "leansearchv2": "Global Lean premise retrieval and decompose-retrieve-filter-judge search evidence.",
    "lean_explore": "Summary-first Lean declaration and premise search.",
    "jixia": "Lean declaration, symbol, elaboration, AST, and proof-state/source extraction.",
    "pantograph": "Lean proof-state interaction and tactic/search stepping; final certification remains direct Lean.",
    "lean_dojo": "Lean theorem-proving environment interaction; final certification remains direct Lean.",
}

TOOL_BOUNDARIES: dict[str, str] = {
    "sympy": "Certifying only for the scoped expression class actually encoded and checked.",
    "sage": "Certifying only for the scoped Sage computation under explicit domain assumptions.",
    "lean": "Certifying only when direct Lean checking succeeds without placeholders.",
    "leansearchv2": "Retrieval evidence only; retrieved premises are not proof certificates.",
    "lean_explore": "Retrieval evidence only; retrieved declarations are not proof certificates.",
    "jixia": "Static extraction evidence only unless followed by a certifying backend check.",
    "pantograph": "Proof-state/search evidence only; final proof claims need direct Lean verification.",
    "lean_dojo": "Proof-state/search evidence only; final proof claims need direct Lean verification.",
}

LATEX_OR_DOMAIN_RE = re.compile(
    r"\\(?:E|mathbb|frac|left|right|mid|beta|star|widetilde|bar|sum|int)|"
    r"\b(?:expectation|conditional|measurable|integrable|logdet|trace|det|matrix|jacobian|foc)\b",
    re.IGNORECASE,
)
LEAN_HINT_RE = re.compile(r"\b(?:theorem|lemma|example|by|:=|∀|fun|Prop|Nat|Real)\b|->|=>")


def normalize_goal_kind(goal_kind: str) -> str:
    normalized = goal_kind.strip().lower().replace("-", "_")
    return GOAL_KIND_ALIASES.get(normalized, normalized or "derivation")


def _manifest_by_name() -> dict[str, dict[str, Any]]:
    manifest: dict[str, dict[str, Any]] = {}
    for item in SUPPORTED_INTEGRATION_TOOLS:
        manifest[item.name] = asdict(item)
    manifest["lean"] = {
        "name": "lean",
        "supported_version": None,
        "profile": "lean",
        "install_hint": "Install Lean through elan or use a validated backend environment.",
        "role": TOOL_ROLES["lean"],
    }
    manifest["sage"] = {
        "name": "sage",
        "supported_version": None,
        "profile": "backend",
        "install_hint": "Install SageMath or expose sage in the selected backend environment.",
        "role": TOOL_ROLES["sage"],
    }
    return manifest


def _status_from_reports(tool: str, capabilities: dict[str, Any], integrations: dict[str, Any]) -> dict[str, Any]:
    if tool in integrations and isinstance(integrations[tool], dict):
        integration = integrations[tool]
        return {
            "available": bool(integration.get("resolved_available", integration.get("available"))),
            "version": integration.get("resolved_version", integration.get("version")),
            "version_status": integration.get("resolved_version_status", integration.get("version_status")),
            "environment_scope": integration.get("resolved_scope", integration.get("profile")),
            "detail": integration.get("detail") or integration.get("backend_detail"),
        }
    if tool in capabilities and isinstance(capabilities[tool], dict):
        capability = capabilities[tool]
        return {
            "available": bool(capability.get("available")),
            "version": capability.get("version"),
            "version_status": capability.get("status"),
            "environment_scope": capability.get("environment_scope") or capability.get("kind"),
            "detail": capability.get("detail"),
        }
    return {
        "available": False,
        "version": None,
        "version_status": "unknown",
        "environment_scope": "unknown",
        "detail": "No doctor capability or integration status was supplied.",
    }


def _target_requires_formalization(target: str) -> bool:
    return bool(LATEX_OR_DOMAIN_RE.search(target))


def _target_looks_like_lean(target: str) -> bool:
    return bool(LEAN_HINT_RE.search(target))


def _applicability_status(tool: str, goal_kind: str, target: str, raw_available: bool) -> tuple[str, str]:
    requires_formalization = _target_requires_formalization(target)
    looks_like_lean = _target_looks_like_lean(target)
    if tool in {"sympy", "sage"}:
        if requires_formalization:
            return (
                "requires_formalization" if raw_available else "unavailable",
                f"{tool} should be considered after the LaTeX/domain target is formalized into an encodable expression.",
            )
        return (
            "available" if raw_available else "unavailable",
            f"{tool} is applicable to an already-encodable algebraic target.",
        )
    if tool == "lean":
        if looks_like_lean:
            return (
                "available" if raw_available else "unavailable",
                "The target looks like explicit Lean source, so direct Lean checking is the certification route.",
            )
        return (
            "requires_formalization" if raw_available else "unavailable",
            "Lean must be considered for certification after an explicit Lean statement/proof is available.",
        )
    if tool in {"leansearchv2", "lean_explore"}:
        if goal_kind in {"premise_search", "formal_proof", "document_repair", "derivation", "missing_assumptions"}:
            return (
                "available" if raw_available else "unavailable",
                "Premise retrieval is relevant before agent-only formalization or proof search.",
            )
    if tool == "jixia":
        if goal_kind in {"premise_search", "formal_proof", "missing_assumptions", "document_repair", "derivation"}:
            if not looks_like_lean:
                return (
                    "requires_formalization" if raw_available else "unavailable",
                    "jixia should be considered after a Lean source file or project context is available.",
                )
            return (
                "available" if raw_available else "unavailable",
                "Lean/static source extraction is relevant when a Lean project or formalization exists.",
            )
    if tool in {"pantograph", "lean_dojo"}:
        if goal_kind in {"formal_proof", "document_repair", "derivation"}:
            if not looks_like_lean:
                return (
                    "requires_formalization" if raw_available else "unavailable",
                    "Proof-state interaction should be considered after a Lean project/formalization is available.",
                )
            return (
                "available" if raw_available else "unavailable",
                "Proof-state interaction is relevant after a Lean project/formalization is available.",
            )
    return "not_applicable", "No direct role is registered for this goal kind."


def _can_select(status: str) -> bool:
    return status in {"available", "requires_formalization"}


def external_tool_first_plan(
    target: str,
    *,
    goal_kind: str = "derivation",
    capabilities: dict[str, Any] | None = None,
    integrations: dict[str, Any] | None = None,
    allow_in_house_gap: bool = False,
    gap_justification: str | None = None,
) -> dict[str, Any]:
    """Return an auditable external-tool-first consideration plan."""
    normalized_goal = normalize_goal_kind(goal_kind)
    if normalized_goal not in GOAL_TOOL_ORDER:
        normalized_goal = "derivation"
    if capabilities is None or integrations is None:
        doctor = doctor_report()
        capabilities = doctor.get("capabilities", {}) if capabilities is None else capabilities
        integrations = doctor.get("integrations", {}) if integrations is None else integrations
    manifest = _manifest_by_name()
    considerations: list[dict[str, Any]] = []
    for priority, tool in enumerate(GOAL_TOOL_ORDER[normalized_goal], start=1):
        status_info = _status_from_reports(tool, capabilities, integrations)
        raw_available = bool(status_info.get("available"))
        status, reason = _applicability_status(tool, normalized_goal, target, raw_available)
        manifest_item = manifest.get(tool, {})
        consideration = ToolConsideration(
            tool=tool,
            role=TOOL_ROLES.get(tool, str(manifest_item.get("role", ""))),
            status=status,
            priority=priority,
            reason=reason,
            evidence_kind="certifying_backend" if tool in {"sympy", "sage", "lean"} else "retrieval_or_proof_state_evidence",
            certification_boundary=TOOL_BOUNDARIES.get(tool, EXTERNAL_TOOL_FIRST_BOUNDARY),
            version=status_info.get("version"),
            supported_version=manifest_item.get("supported_version"),
            version_status=status_info.get("version_status"),
            environment_scope=status_info.get("environment_scope"),
            install_hint=manifest_item.get("install_hint"),
        )
        considerations.append(asdict(consideration))
    selected = [item for item in considerations if _can_select(str(item.get("status")))]
    unavailable = [item for item in considerations if item.get("status") == "unavailable"]
    rejected = [item for item in considerations if item.get("status") == "not_applicable"]
    in_house_allowed = bool(allow_in_house_gap and gap_justification and len(gap_justification.strip()) >= 20)
    if selected:
        status = "external_route_available"
        reason = "At least one external-tool route is available or can proceed after formalization."
    elif in_house_allowed:
        status = "in_house_gap_justified"
        reason = "No external route is currently selectable and an explicit in-house gap justification was supplied."
    else:
        status = "blocked_pending_external_tool_or_gap_justification"
        reason = "No external route is currently selectable; in-house search needs an explicit gap justification."
    result = {
        "status": status,
        "reason": reason,
        "goal_kind": normalized_goal,
        "target": target,
        "selected_external_tools": selected,
        "considered_tools": considerations,
        "unavailable_tools": unavailable,
        "rejected_tools": rejected,
        "in_house_search_gate": {
            "allowed": in_house_allowed,
            "required": not selected,
            "gap_justification": gap_justification or None,
            "rule": IN_HOUSE_GAP_REQUIRED,
        },
        "diagnostics": {
            "considered_count": len(considerations),
            "selected_count": len(selected),
            "unavailable_count": len(unavailable),
            "requires_formalization_count": sum(1 for item in considerations if item.get("status") == "requires_formalization"),
        },
        "boundary": EXTERNAL_TOOL_FIRST_BOUNDARY,
        "non_claims": [
            {
                "code": "external_tool_plan_not_certificate",
                "text": EXTERNAL_TOOL_FIRST_BOUNDARY,
            },
            {
                "code": "retrieval_and_route_plans_not_proofs",
                "text": "Retrieval hits, route plans, and proof-state traces are evidence only until a certifying backend checks the scoped claim.",
            },
        ],
    }
    return attach_contract(result, EXTERNAL_TOOL_FIRST_PLAN_CONTRACT)
