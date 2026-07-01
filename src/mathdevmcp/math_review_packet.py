from __future__ import annotations

"""Aggregate math debugging evidence into a human-review packet."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .math_debugging import CERTIFICATION_BOUNDARY


@dataclass(frozen=True)
class MathReviewPacket:
    packet_id: str
    question: str
    status: str
    reason: str
    source: dict[str, Any]
    obligations: list[dict[str, Any]]
    assumptions: list[dict[str, Any]]
    backend_attempts: list[dict[str, Any]]
    counterexamples: list[dict[str, Any]]
    code_links: list[dict[str, Any]]
    notation_conflicts: list[dict[str, Any]]
    generated_diagnostics: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    actions: list[dict[str, Any]]
    certification_boundary: str


def _contract(evidence: dict[str, Any]) -> str:
    metadata = evidence.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return "untyped"


def _status(evidence: dict[str, Any]) -> str:
    value = evidence.get("status")
    return value if isinstance(value, str) else ""


def _extend_from_workbench(target: list[dict[str, Any]], evidence: dict[str, Any], key: str) -> None:
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get(key), list):
        target.extend(item for item in workbench[key] if isinstance(item, dict))


def _route_backend_attempt(evidence: dict[str, Any]) -> dict[str, Any] | None:
    route = evidence.get("route_decision")
    if isinstance(route, dict) and isinstance(route.get("backend_attempt"), dict):
        return route["backend_attempt"]
    return None


def _actions_from_evidence(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    actions = evidence.get("actions")
    if isinstance(actions, list):
        return [item for item in actions if isinstance(item, dict)]
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get("actions"), list):
        return [item for item in workbench["actions"] if isinstance(item, dict)]
    next_action = evidence.get("next_action")
    if isinstance(next_action, str) and next_action:
        return [{"kind": next_action, "source": _contract(evidence)}]
    return []


def build_math_review_packet(
    question: str,
    *,
    source: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    packet_id: str | None = None,
) -> dict:
    evidence_items = evidence or []
    if not all(isinstance(item, dict) for item in evidence_items):
        raise ValueError("evidence must be a list of objects")

    obligations: list[dict[str, Any]] = []
    assumptions: list[dict[str, Any]] = []
    backend_attempts: list[dict[str, Any]] = []
    counterexamples: list[dict[str, Any]] = []
    code_links: list[dict[str, Any]] = []
    notation_conflicts: list[dict[str, Any]] = []
    generated_diagnostics: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []

    for item in evidence_items:
        _extend_from_workbench(obligations, item, "obligations")
        _extend_from_workbench(assumptions, item, "assumptions")
        _extend_from_workbench(backend_attempts, item, "backend_attempts")
        _extend_from_workbench(counterexamples, item, "counterexamples")
        route_attempt = _route_backend_attempt(item)
        if route_attempt is not None and route_attempt not in backend_attempts:
            backend_attempts.append(route_attempt)
        if item.get("counterexample"):
            counterexamples.append(item["counterexample"])
        if _contract(item) == "equation_code_match_result":
            code_links.append(item)
        if _contract(item) == "notation_reconciliation_result":
            notation_conflicts.extend(item.get("conflicts", []))
            notation_conflicts.extend(item.get("unresolved_symbols", []))
        if _contract(item) == "math_test_generation_result":
            generated_diagnostics.extend(item.get("artifacts", []))
        actions.extend(_actions_from_evidence(item))

    statuses = [_status(item) for item in evidence_items]
    if any(status == "refuted" for status in statuses) or counterexamples:
        status = "blocked_by_refutation"
        reason = "At least one nested evidence record contains a refutation or counterexample."
    elif notation_conflicts:
        status = "needs_human_review"
        reason = "Notation conflicts or unresolved notation decisions require human review."
    elif any(status in {"missing_assumptions", "backend_unavailable", "not_encodable", "mismatch"} for status in statuses):
        status = "needs_human_review"
        reason = "At least one nested evidence record is blocked, unavailable, not encodable, or mismatched."
    else:
        status = "review_ready"
        reason = "Evidence is aggregated for review without changing nested meanings."

    packet = MathReviewPacket(
        packet_id=packet_id or f"math-review:{abs(hash(question)) % 10_000_000}",
        question=question,
        status=status,
        reason=reason,
        source=source or {},
        obligations=obligations,
        assumptions=assumptions,
        backend_attempts=backend_attempts,
        counterexamples=counterexamples,
        code_links=code_links,
        notation_conflicts=notation_conflicts,
        generated_diagnostics=generated_diagnostics,
        evidence=evidence_items,
        actions=actions,
        certification_boundary=(
            "This packet is an evidence bundle, not a proof certificate. "
            f"{CERTIFICATION_BOUNDARY}"
        ),
    )
    return attach_contract(asdict(packet), "math_review_packet")
