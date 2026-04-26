from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract
from .typed_workflows import typed_obligation_for_label


@dataclass(frozen=True)
class RouteDecision:
    status: str
    reason: str
    route: str
    label: str | None
    backend_candidates: list[str]
    missing_constraints: list[dict]
    typed_diagnostic: dict


def route_typed_diagnostic(typed_diagnostic: dict, *, label: str | None = None) -> dict:
    obligation = typed_diagnostic.get("obligation", {})
    hints = obligation.get("backend_route_hints", [])
    missing = typed_diagnostic.get("missing_constraints", [])
    candidate_backends = [hint["backend"] for hint in hints if hint.get("suitability") in {"candidate", "diagnostic_candidate", "formalization_candidate"}]
    if missing:
        status = "human_review"
        route = "human_review"
        reason = "Typed obligation has missing assumptions or dimension constraints."
    elif obligation.get("backend_suitability") in {"symbolic", "normalization"}:
        status = "routed"
        route = "symbolic"
        reason = "Typed obligation is suitable for bounded symbolic routing."
    elif any(hint.get("backend") == "lean" for hint in hints):
        status = "routed"
        route = "lean_candidate"
        reason = "Typed obligation may be formalized and checked by Lean."
    else:
        status = "human_review"
        route = "human_review"
        reason = "Typed obligation requires human review or additional formalization."
    result = RouteDecision(status, reason, route, label, candidate_backends, missing, typed_diagnostic)
    return attach_contract(asdict(result), "typed_route_decision")


def route_label_obligation(root: str, label: str, *, context_text: str = "") -> dict:
    typed = typed_obligation_for_label(root, label, context_text=context_text)
    result = route_typed_diagnostic(typed["typed_diagnostic"], label=label)
    result["doc_context"] = typed.get("doc_context", {})
    return result
