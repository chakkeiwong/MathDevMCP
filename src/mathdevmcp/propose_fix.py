from __future__ import annotations

"""High-level diagnostic fix proposal workflow."""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .contracts import attach_contract, contract_metadata
from .high_level_contracts import (
    action,
    default_non_claims,
    evidence_entry,
    high_level_result,
    refresh_evidence_ledger,
    validate_high_level_result,
    veto_reason,
)
from .prepare_review_packet import prepare_review_packet, review_packet_agent_handoff
from .workflow import build_implementation_brief


FIX_PROPOSAL_CONTRACT = "fix_proposal_result"
REPAIR_NON_CLAIM_CODE = "fix_proposal_not_applied_or_verified"
REPAIR_NON_CLAIM_TEXT = (
    "Proposed fixes are diagnostic guidance only; they are not applied edits, proof certificates, "
    "or semantic implementation verification."
)


@dataclass(frozen=True)
class ProposedChange:
    kind: str
    target: str
    summary: str
    rationale: str
    evidence_refs: list[str]
    confidence: str
    requires_human_review: bool = True


@dataclass(frozen=True)
class FixProposal:
    status: str
    question: str
    source: dict[str, Any]
    proposed_changes: list[dict[str, Any]]
    rationale: list[str]
    evidence: list[dict[str, Any]]
    assumptions: list[dict[str, Any]]
    non_claims: list[dict[str, Any]]
    next_actions: list[dict[str, Any]]
    agent_handoff: dict[str, Any]
    implementation_brief: dict[str, Any] | None
    certification_boundary: str
    metadata: dict[str, str]


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _compact(value: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: value[field] for field in fields if field in value and value[field] not in (None, [], {})}


def _source_context(source: dict[str, Any] | None, label: str | None, code_path: str | None) -> dict[str, Any]:
    result = dict(source or {})
    if label and "label" not in result:
        result["label"] = label
    if code_path and "code_path" not in result:
        result["code_path"] = code_path
    return result


def _target_from_action(item: dict[str, Any], fallback: str) -> str:
    for key in ("target", "obligation_id", "source"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value
    return fallback


def _dedupe_changes(changes: list[ProposedChange]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for change in changes:
        key = (change.kind, change.target, change.summary)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(asdict(change))
    return deduped


def _proposal_from_action(item: dict[str, Any], *, evidence_ref: str, fallback_target: str) -> ProposedChange | None:
    kind = str(item.get("kind") or item.get("code") or "").strip()
    reason = str(item.get("reason") or item.get("description") or "Nested evidence recommends a repair step.").strip()
    target = _target_from_action(item, fallback_target)
    severity = str(item.get("severity") or "medium")
    confidence = "medium" if severity == "high" else "low"

    if kind in {"state_or_verify_missing_constraint", "review_shape_dimension_assumptions"}:
        return ProposedChange(
            kind="add_or_verify_assumption",
            target=target,
            summary=f"State or verify the missing constraint `{target}` near the affected claim.",
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence=confidence,
        )
    if kind == "split_or_rewrite_ambiguous_derivation_row":
        return ProposedChange(
            kind="split_derivation_step",
            target=target,
            summary="Split the ambiguous derivation row into smaller labeled obligations.",
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence=confidence,
        )
    if kind in {"human_formalization_or_review", "human_review"}:
        return ProposedChange(
            kind="add_review_boundary",
            target=target,
            summary="Add a local review boundary before treating this claim as derived or implemented.",
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence=confidence,
        )
    if kind == "fix_parser_provenance_before_certification":
        return ProposedChange(
            kind="fix_parser_provenance",
            target=target,
            summary="Fix parser provenance before using this artifact for certification.",
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence=confidence,
        )
    if kind in {"logdet_domain_check", "linear_solve_residual_check", "finite_difference_gradient_check", "trace_shape_check"}:
        return ProposedChange(
            kind="add_diagnostic_check",
            target=target,
            summary=f"Add or run `{kind}` as a bounded diagnostic.",
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence=confidence,
        )
    if kind in {"supply_more_evidence", "formalize_claim", "configure_backend"}:
        return ProposedChange(
            kind="collect_more_evidence",
            target=target,
            summary=str(item.get("description") or reason),
            rationale=reason,
            evidence_refs=[evidence_ref],
            confidence="low",
        )
    return None


def _proposals_from_proof_audit(audit: dict[str, Any]) -> list[ProposedChange]:
    changes: list[ProposedChange] = []
    label = str(audit.get("label") or "source label")
    for item in _as_dict_list(audit.get("high_priority_actions")):
        obligation_id = item.get("obligation_id")
        evidence_ref = f"proof_audit_v2:{label}:{obligation_id}" if isinstance(obligation_id, str) and obligation_id else f"proof_audit_v2:{label}"
        change = _proposal_from_action(item, evidence_ref=evidence_ref, fallback_target=label)
        if change is not None:
            changes.append(change)
    for obligation in _as_dict_list(audit.get("obligations")):
        obligation_ref = f"proof_audit_v2:{label}:{obligation.get('id', 'obligation')}"
        target = str(obligation.get("id") or label)
        for constraint in _as_dict_list(obligation.get("missing_constraints")):
            kind = str(constraint.get("kind") or "missing_constraint")
            changes.append(
                ProposedChange(
                    kind="add_or_verify_assumption",
                    target=target,
                    summary=f"State or verify `{kind}` for `{target}`.",
                    rationale=str(constraint.get("reason") or obligation.get("reason") or "A typed obligation reports a missing constraint."),
                    evidence_refs=[obligation_ref],
                    confidence="medium",
                )
            )
        for action_item in _as_dict_list(obligation.get("actions")):
            change = _proposal_from_action(action_item, evidence_ref=obligation_ref, fallback_target=target)
            if change is not None:
                changes.append(change)
    return changes


def _proposals_from_review_packet(packet: dict[str, Any]) -> list[ProposedChange]:
    changes: list[ProposedChange] = []
    handoff = review_packet_agent_handoff(packet)
    for gap in _as_dict_list(handoff.get("assumption_gap_ledger")):
        kind = str(gap.get("kind") or "")
        reason = str(gap.get("reason") or "Review packet reported a residual gap.")
        target = str(gap.get("source") or gap.get("obligation") or "review packet")
        if "missing" in kind or "assumption" in kind:
            changes.append(
                ProposedChange(
                    kind="add_or_verify_assumption",
                    target=target,
                    summary="Add explicit assumptions or shape constraints for this residual gap.",
                    rationale=reason,
                    evidence_refs=["prepare_review_packet:agent_handoff"],
                    confidence="medium",
                )
            )
        elif kind in {"proof_gap", "gap_found", "obligation_not_proved"}:
            changes.append(
                ProposedChange(
                    kind="split_derivation_step",
                    target=target,
                    summary="Break the unsupported derivation into smaller obligations and retry bounded checks.",
                    rationale=reason,
                    evidence_refs=["prepare_review_packet:agent_handoff"],
                    confidence="medium",
                )
            )
        elif kind in {"structural_mismatch", "mismatch"}:
            changes.append(
                ProposedChange(
                    kind="repair_structural_mismatch",
                    target=target,
                    summary="Align the document formula and implementation structure, then rerun the audit.",
                    rationale=reason,
                    evidence_refs=["prepare_review_packet:agent_handoff"],
                    confidence="medium",
                )
            )
        elif kind in {"backend_unavailable", "not_encodable", "inconclusive"}:
            changes.append(
                ProposedChange(
                    kind="collect_more_evidence",
                    target=target,
                    summary="Formalize the claim or configure a backend before asking for stronger evidence.",
                    rationale=reason,
                    evidence_refs=["prepare_review_packet:agent_handoff"],
                    confidence="low",
                )
            )
    for item in _as_dict_list(handoff.get("next_actions")):
        change = _proposal_from_action(item, evidence_ref="prepare_review_packet:agent_handoff", fallback_target="review packet")
        if change is not None:
            changes.append(change)
    return changes


def _proposals_from_implementation_brief(brief: dict[str, Any] | None) -> list[ProposedChange]:
    if not isinstance(brief, dict):
        return []
    changes: list[ProposedChange] = []
    status = str(brief.get("status") or "")
    selected_label = str(brief.get("selected_label") or "selected label")
    if status == "mismatch":
        changes.append(
            ProposedChange(
                kind="repair_structural_mismatch",
                target=selected_label,
                summary="Repair the code/document mismatch identified by the implementation brief.",
                rationale=str(brief.get("reason") or "At least one document-grounded implementation check failed."),
                evidence_refs=["implementation_brief"],
                confidence="medium",
            )
        )
    elif status == "unverified":
        changes.append(
            ProposedChange(
                kind="collect_more_evidence",
                target=selected_label,
                summary="Add derivation support or assumptions before treating the implementation brief as verified.",
                rationale=str(brief.get("reason") or "The implementation brief remains unverified."),
                evidence_refs=["implementation_brief"],
                confidence="low",
            )
        )
    for check_name, check in (brief.get("checks") or {}).items():
        if isinstance(check, dict) and check.get("status") == "mismatch":
            changes.append(
                ProposedChange(
                    kind="repair_structural_mismatch",
                    target=str(check.get("label") or selected_label),
                    summary=f"Repair the `{check_name}` mismatch and rerun the implementation brief.",
                    rationale=str(check.get("reason") or "A nested implementation check reported mismatch."),
                    evidence_refs=[f"implementation_brief:{check_name}"],
                    confidence="medium",
                )
            )
    return changes


def _is_coarse_proof_audit_gap(change: ProposedChange) -> bool:
    return (
        change.kind == "collect_more_evidence"
        and change.target == "proof_audit_v2_result"
        and "prepare_review_packet:agent_handoff" in change.evidence_refs
    )


def _proposal_status(proposed_changes: list[dict[str, Any]], evidence_items: list[dict[str, Any]]) -> tuple[str, str]:
    if proposed_changes:
        return "proposal_ready", "Diagnostic evidence was translated into proposed repair steps."
    if evidence_items:
        return "no_proposal", "Evidence was aggregated, but no concrete repair proposal could be derived safely."
    return "needs_evidence", "No evidence was supplied, so only evidence-collection guidance is available."


def _build_agent_handoff(
    *,
    question: str,
    status: str,
    proposed_changes: list[dict[str, Any]],
    next_actions: list[dict[str, Any]],
    evidence_summary: list[dict[str, Any]],
    non_claims: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "scoped_question": question,
        "status": status,
        "proposed_changes": proposed_changes[:8],
        "evidence_ledger": evidence_summary[:8],
        "next_actions": next_actions[:8],
        "non_claim_boundary": [_compact(item, ("code", "text")) for item in non_claims[:8]],
        "next_artifact": (
            "Apply no edit automatically. Use proposed_changes as a repair checklist, then rerun the relevant "
            "audit or review-packet workflow."
        ),
        "certification_boundary": REPAIR_NON_CLAIM_TEXT,
    }


def build_fix_proposal(
    question: str,
    *,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    implementation_brief: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence_items = evidence or []
    if not all(isinstance(item, dict) for item in evidence_items):
        raise ValueError("evidence must be a list of objects")
    if implementation_brief is not None and not isinstance(implementation_brief, dict):
        raise ValueError("implementation_brief must be an object when supplied")

    review = prepare_review_packet(question, evidence=evidence_items, source=source)
    changes: list[ProposedChange] = []
    proof_audit_changes: list[ProposedChange] = []
    for item in evidence_items:
        metadata = item.get("metadata")
        contract = metadata.get("contract") if isinstance(metadata, dict) else None
        if contract == "proof_audit_v2_result":
            proof_audit_changes.extend(_proposals_from_proof_audit(item))
    changes.extend(proof_audit_changes)
    review_changes = _proposals_from_review_packet(review)
    if proof_audit_changes:
        review_changes = [change for change in review_changes if not _is_coarse_proof_audit_gap(change)]
    changes.extend(review_changes)
    changes.extend(_proposals_from_implementation_brief(implementation_brief))
    proposed_changes = _dedupe_changes(changes)

    status, reason = _proposal_status(proposed_changes, evidence_items)
    evidence_summary = [
        _compact(
            {
                "contract": item.get("metadata", {}).get("contract") if isinstance(item.get("metadata"), dict) else None,
                "status": item.get("status"),
                "label": item.get("label"),
                "question": item.get("question"),
                "workflow": item.get("workflow"),
                "reason": item.get("reason") or item.get("answer"),
            },
            ("contract", "status", "label", "question", "workflow", "reason"),
        )
        for item in evidence_items
    ]
    evidence_summary.append(
        {
            "contract": "high_level_workflow_result",
            "workflow": "prepare_review_packet",
            "status": review["status"],
            "reason": review["answer"],
        }
    )
    if implementation_brief is not None:
        evidence_summary.append(
            _compact(
                {
                    "contract": implementation_brief.get("metadata", {}).get("contract") if isinstance(implementation_brief.get("metadata"), dict) else None,
                    "status": implementation_brief.get("status"),
                    "label": implementation_brief.get("selected_label"),
                    "reason": implementation_brief.get("reason"),
                },
                ("contract", "status", "label", "reason"),
            )
        )

    non_claims = default_non_claims(extra_codes={"diagnostic_evidence_not_proof"})
    if not any(item.get("code") == REPAIR_NON_CLAIM_CODE for item in non_claims):
        non_claims.append({"code": REPAIR_NON_CLAIM_CODE, "text": REPAIR_NON_CLAIM_TEXT})
    next_actions = [
        {
            "code": "human_review",
            "description": "Review proposed changes before applying edits.",
        },
        {
            "code": "rerun_relevant_audit",
            "description": "After any manual repair, rerun the derivation, review-packet, or implementation audit that produced the evidence.",
        },
    ]
    if status == "needs_evidence":
        next_actions.insert(0, {"code": "supply_more_evidence", "description": "Supply audit or review-packet evidence before requesting fix guidance."})

    packet = FixProposal(
        status=status,
        question=question,
        source=dict(source or {}),
        proposed_changes=proposed_changes,
        rationale=[
            reason,
            "Proposal generation preserves nested evidence boundaries and does not certify the repaired artifact.",
        ],
        evidence=evidence_summary,
        assumptions=[],
        non_claims=non_claims,
        next_actions=next_actions,
        agent_handoff=_build_agent_handoff(
            question=question,
            status=status,
            proposed_changes=proposed_changes,
            next_actions=next_actions,
            evidence_summary=evidence_summary,
            non_claims=non_claims,
        ),
        implementation_brief=implementation_brief,
        certification_boundary=REPAIR_NON_CLAIM_TEXT,
        metadata=contract_metadata(FIX_PROPOSAL_CONTRACT),
    )
    return attach_contract(asdict(packet), FIX_PROPOSAL_CONTRACT)


def proposal_agent_handoff(result: dict[str, Any]) -> dict[str, Any]:
    handoff = result.get("agent_handoff")
    if isinstance(handoff, dict):
        return handoff
    return {
        "scoped_question": str(result.get("question", "")),
        "status": str(result.get("status", "")),
        "proposed_changes": result.get("proposed_changes") if isinstance(result.get("proposed_changes"), list) else [],
        "evidence_ledger": result.get("evidence") if isinstance(result.get("evidence"), list) else [],
        "next_actions": result.get("next_actions") if isinstance(result.get("next_actions"), list) else [],
        "non_claim_boundary": result.get("non_claims") if isinstance(result.get("non_claims"), list) else [],
        "next_artifact": "Inspect the full proposal before applying edits.",
        "certification_boundary": REPAIR_NON_CLAIM_TEXT,
    }


def propose_fix(
    question: str,
    *,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    doc_root: str | None = None,
    query: str | None = None,
    code_path: str | None = None,
    label: str | None = None,
    required_terms: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    limit: int = 3,
    cache_path: str | Path | None = None,
) -> dict[str, Any]:
    """Propose conservative repair steps from existing diagnostics."""
    implementation_brief = None
    if code_path:
        if not doc_root or not query:
            raise ValueError("doc_root and query are required when code_path is supplied")
        implementation_brief = build_implementation_brief(
            doc_root,
            query,
            code_path,
            label=label,
            required_terms=required_terms,
            lhs=lhs,
            rhs=rhs,
            limit=limit,
            cache_path=cache_path,
        )

    result = build_fix_proposal(
        question,
        evidence=evidence,
        source=_source_context(source, label, code_path),
        implementation_brief=implementation_brief,
    )

    high_level = high_level_result(
        status="diagnostic_only",
        workflow="propose_fix",
        question=question,
        claim_class="fix_proposal",
        answer=str(result.get("rationale", ["Fix proposal prepared."])[0]),
        evidence=[
            evidence_entry(
                id="propose_fix:fix-proposal",
                evidence_class="fix_proposal",
                source="fix_proposal_builder",
                summary=str(result.get("rationale", ["Fix proposal prepared."])[0]),
                extra={"low_level": result},
            )
        ],
        certification_source="none",
        veto_reasons=[] if result["proposed_changes"] else [veto_reason("proposal_requires_more_evidence", "No concrete proposed change could be derived from the supplied evidence.")],
        actions=[action(item["code"], item["description"]) for item in result["next_actions"]],
        non_claims=result["non_claims"],
    )
    high_level["agent_handoff"] = proposal_agent_handoff(result)
    refresh_evidence_ledger(high_level)
    errors = validate_high_level_result(high_level)
    if errors:
        raise ValueError(f"invalid propose_fix result: {errors}")
    return high_level
