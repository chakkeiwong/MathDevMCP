from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .contracts import attach_contract, contract_metadata
from .math_ir import diagnose_typed_obligation
from .numeric_diagnostics import suggest_numeric_diagnostics
from .parser_policy import decide_parser_policy
from .proof_audit import audit_derivation_for_label
from .routing import route_typed_diagnostic
from .shape_diagnostics import diagnose_shape_constraints


@dataclass(frozen=True)
class ProofAuditV2Obligation:
    id: str
    label: str
    source_text: str
    lhs: str
    rhs: str
    kind: str
    parser_backend: str | None
    parser_policy: dict
    typed_diagnostic: dict
    route_decision: dict
    shape_diagnostic: dict
    numeric_diagnostics: dict
    backend_attempts: list[dict]
    status: str
    reason: str
    actions: list[dict]
    provenance: dict
    metadata: dict[str, str]


@dataclass(frozen=True)
class ProofAuditV2Report:
    label: str
    doc_root: str
    status: str
    reason: str
    counts: dict[str, int]
    high_priority_actions: list[dict]
    obligations: list[dict]
    parser_policy: dict
    base_audit_status: str
    doc_context: dict


def _context_text(doc_context: dict) -> str:
    paragraphs = doc_context.get("paragraphs")
    if isinstance(paragraphs, list) and paragraphs:
        return "\n".join(str(item.get("text", "")) for item in paragraphs)
    excerpt = doc_context.get("excerpt", [])
    if isinstance(excerpt, list):
        return "\n".join(str(item.get("text", "")) for item in excerpt)
    return ""


def _backend_attempts(base_obligation: dict) -> list[dict]:
    attempts: list[dict] = []
    for evidence in base_obligation.get("evidence", []):
        attempts.append(
            {
                "source": "proof_audit",
                "status": base_obligation.get("status"),
                "classification": base_obligation.get("classification"),
                "evidence": evidence,
            }
        )
    return attempts


def _actions(
    *,
    base_obligation: dict,
    parser_policy: dict,
    route: dict,
    shape: dict,
    numeric: dict,
    status: str,
) -> list[dict]:
    actions: list[dict] = []
    if parser_policy.get("status") != "selected":
        actions.append(
            {
                "kind": "fix_parser_provenance_before_certification",
                "severity": "high",
                "reason": parser_policy.get("reason", "Parser policy did not select a proof-audit backend."),
            }
        )
    if base_obligation.get("classification") == "not_extracted":
        actions.append(
            {
                "kind": "split_or_rewrite_ambiguous_derivation_row",
                "severity": "high",
                "reason": "The derivation row was not split into a safe proof obligation.",
            }
        )
    for constraint in shape.get("missing_constraints", []):
        actions.append(
            {
                "kind": "state_or_verify_missing_constraint",
                "target": constraint.get("kind"),
                "severity": "high",
                "reason": constraint.get("reason", "A required shape or dimension constraint is missing."),
            }
        )
    if route.get("route") == "human_review":
        actions.append(
            {
                "kind": "human_formalization_or_review",
                "severity": "high" if status in {"unverified", "inconclusive"} else "medium",
                "reason": route.get("reason", "The obligation requires human review."),
            }
        )
    for suggestion in numeric.get("suggestions", []):
        actions.append(
            {
                "kind": suggestion.get("kind"),
                "target": suggestion.get("target"),
                "severity": suggestion.get("priority", "medium"),
                "reason": suggestion.get("reason", "Run a bounded numeric diagnostic when a safe encoding exists."),
            }
        )
    if status == "mismatch":
        actions.append(
            {
                "kind": "investigate_backend_refutation",
                "severity": "high",
                "reason": "A deterministic backend refuted the extracted obligation.",
            }
        )
    return actions


def _obligation_status_and_reason(
    *,
    base_obligation: dict,
    parser_policy: dict,
    route: dict,
    shape: dict,
) -> tuple[str, str]:
    base_status = base_obligation.get("status", "inconclusive")
    if parser_policy.get("status") != "selected":
        return "inconclusive", "Parser policy did not select a provenance-preserving backend for certification."
    if base_status == "mismatch":
        return "mismatch", base_obligation.get("reason", "A backend refuted the obligation.")
    if base_obligation.get("classification") == "not_extracted":
        return "inconclusive", "The row could not be extracted as a safe proof obligation."
    if shape.get("missing_constraints"):
        return "unverified", "The obligation has missing shape, dimension, or regularity constraints."
    if route.get("route") == "human_review":
        return "unverified", "The obligation uses notation that requires human review or manual formalization."
    if base_status == "verified":
        return "verified", "The extracted obligation was verified by a deterministic bounded backend."
    if base_status == "unverified":
        return "unverified", base_obligation.get("reason", "The obligation remains unsupported.")
    return "inconclusive", base_obligation.get("reason", "No deterministic backend evidence certified or refuted the obligation.")


def _counts(obligations: list[dict]) -> dict[str, int]:
    counts = {"total": len(obligations), "verified": 0, "mismatch": 0, "unverified": 0, "inconclusive": 0}
    for obligation in obligations:
        status = obligation.get("status", "inconclusive")
        if status in counts:
            counts[status] += 1
        else:
            counts["inconclusive"] += 1
    return counts


def _aggregate(counts: dict[str, int]) -> tuple[str, str]:
    if counts["mismatch"]:
        return "mismatch", "At least one proof-audit v2 obligation was refuted by backend evidence."
    if counts["verified"] and counts["verified"] == counts["total"]:
        return "verified", "Every proof-audit v2 obligation was verified by deterministic backend evidence."
    if counts["verified"] or counts["unverified"]:
        return "unverified", "At least one obligation remains unverified or diagnostic-only."
    return "inconclusive", "No proof-audit v2 obligation could be certified or refuted."


def _compact_obligation(obligation: dict) -> dict:
    return {
        "id": obligation["id"],
        "label": obligation["label"],
        "status": obligation["status"],
        "reason": obligation["reason"],
        "route": obligation["route_decision"].get("route"),
        "missing_constraints": obligation["shape_diagnostic"].get("missing_constraints", []),
        "actions": obligation["actions"],
        "provenance": obligation["provenance"],
        "metadata": obligation["metadata"],
    }


def audit_derivation_v2_for_label(
    root: str,
    label: str,
    *,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "sympy",
    cache_path: str | Path | None = None,
    parser_backends: list[str] | None = None,
    summary_only: bool = False,
) -> dict:
    base = audit_derivation_for_label(
        root,
        label,
        before=before,
        after=after,
        paragraph_context=paragraph_context,
        backend=backend,
        cache_path=cache_path,
    )
    parser = decide_parser_policy(root, backends=parser_backends or ["current"])
    selected_backend = parser.get("selected_backend") or "current"
    context = _context_text(base.get("doc_context", {}))
    obligations: list[dict] = []
    for base_obligation in base.get("obligations", []):
        typed = diagnose_typed_obligation(base_obligation, parser_backend=selected_backend, context_text=context)
        route = route_typed_diagnostic(typed, label=label)
        shape = diagnose_shape_constraints(typed)
        numeric = suggest_numeric_diagnostics(typed)
        status, reason = _obligation_status_and_reason(
            base_obligation=base_obligation,
            parser_policy=parser,
            route=route,
            shape=shape,
        )
        actions = _actions(
            base_obligation=base_obligation,
            parser_policy=parser,
            route=route,
            shape=shape,
            numeric=numeric,
            status=status,
        )
        obligation = ProofAuditV2Obligation(
            id=str(base_obligation.get("id", "")),
            label=label,
            source_text=str(base_obligation.get("source_text", "")),
            lhs=str(base_obligation.get("lhs", "")),
            rhs=str(base_obligation.get("rhs", "")),
            kind=typed.get("obligation", {}).get("kind", "unknown"),
            parser_backend=parser.get("selected_backend"),
            parser_policy=parser,
            typed_diagnostic=typed,
            route_decision=route,
            shape_diagnostic=shape,
            numeric_diagnostics=numeric,
            backend_attempts=_backend_attempts(base_obligation),
            status=status,
            reason=reason,
            actions=actions,
            provenance=base_obligation.get("provenance", {}),
            metadata=contract_metadata("proof_audit_v2_obligation"),
        )
        obligations.append(asdict(obligation))
    counts = _counts(obligations)
    status, reason = _aggregate(counts)
    high_priority_actions = [
        {**action, "obligation_id": obligation["id"]}
        for obligation in obligations
        for action in obligation["actions"]
        if action.get("severity") == "high"
    ]
    report_obligations = [_compact_obligation(item) for item in obligations] if summary_only else obligations
    report = ProofAuditV2Report(
        label=label,
        doc_root=str(Path(root).resolve()),
        status=status,
        reason=reason,
        counts=counts,
        high_priority_actions=high_priority_actions,
        obligations=report_obligations,
        parser_policy=parser,
        base_audit_status=base.get("status", "inconclusive"),
        doc_context=base.get("doc_context", {}),
    )
    return attach_contract(asdict(report), "proof_audit_v2_result", doc_context=base.get("doc_context", {}))
