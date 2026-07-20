from __future__ import annotations

"""High-level assumption discovery workflow."""

from pathlib import Path
from typing import Any

from .assumption_gap_proposals import (
    build_assumption_gaps,
    build_assumption_proposals,
    build_assumption_tool_uses,
    build_unknown_route_gap,
    build_unknown_route_proposal,
    summarize_assumption_validation,
)
from .artifact_storage import write_bytes_safe
from .assumption_discovery import assumptions_required
from .contracts import attach_contract, contract_metadata
from .derivation_target_extraction import extract_derivation_targets_for_label
from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_assumption_result
from .latex_index import build_index
from .role_obligations import build_role_specific_obligations, has_role_specific_builder


ASSUMPTION_REPORT_CONTRACT = "audit_assumption_report_result"
ASSUMPTION_REPORT_NON_CLAIM = {
    "code": "assumption_report_not_proof_certificate",
    "text": "The assumption report proposes route conditions only; it does not prove the target or certify global minimality.",
}


def _source_summary(source: dict[str, Any] | None) -> str:
    if not isinstance(source, dict):
        return ""
    for key in ("context_summary", "summary", "label", "file", "path"):
        value = source.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _assumption_agent_handoff(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "scoped_question": result.get("question", ""),
        "status": result.get("status", ""),
        "reason": result.get("answer", ""),
        "source_context": _source_summary(result.get("source")),
        "gap_count": len(result.get("gaps", [])) if isinstance(result.get("gaps"), list) else 0,
        "proposal_count": len(result.get("proposals", [])) if isinstance(result.get("proposals"), list) else 0,
        "assumption_gap_ledger": result.get("gaps", []) if isinstance(result.get("gaps"), list) else [],
        "proposals": result.get("proposals", []) if isinstance(result.get("proposals"), list) else [],
        "validation": result.get("validation", {}) if isinstance(result.get("validation"), dict) else {},
        "non_claim_boundary": result.get("non_claims", []) if isinstance(result.get("non_claims"), list) else [],
        "next_actions": result.get("actions", []) if isinstance(result.get("actions"), list) else [],
        "next_artifact": "Inspect the assumption proposals before editing text or retrying proof/derivation checks.",
        "certification_boundary": (
            "Assumption proposals are diagnostic route repairs, not proof certificates, "
            "not applied edits, and not globally minimal assumption sets."
        ),
    }


def assumptions_for(
    target: str,
    *,
    provided_assumptions: list[str] | None = None,
    source: dict[str, Any] | None = None,
    role_obligation_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return route-required assumptions for a scoped target."""
    low_level = assumptions_required(target, provided_assumptions=provided_assumptions)
    result = package_assumption_result(low_level, question=f"What assumptions are required for {target}?")
    gaps = build_assumption_gaps(target, low_level.get("assumptions", []), source=source)
    proposals = build_assumption_proposals(gaps)
    if isinstance(role_obligation_packet, dict):
        gaps, proposals = _role_specific_assumption_gap_and_proposal(
            target,
            source=source,
            packet=role_obligation_packet,
        )
    if not gaps and low_level.get("status") == "unknown" and not low_level.get("assumptions"):
        unknown_gap = build_unknown_route_gap(target, source=source)
        gaps = [unknown_gap]
        proposals = [build_unknown_route_proposal(unknown_gap)]
    result["source"] = dict(source or {"target": target})
    result["coverage"] = {
        "target": target,
        "provided_assumption_count": len(provided_assumptions or []),
        "detected_assumption_count": len(low_level.get("assumptions", [])),
        "missing_assumption_count": len(low_level.get("missing_assumptions", [])),
        "gap_count": len(gaps),
        "proposal_count": len(proposals),
        "inspected": ["direct_target"],
        "not_inspected": [
            "global minimality",
            "full theorem applicability",
            "source-wide assumption consistency",
            "proof closure after adding assumptions",
        ],
    }
    result["tool_uses"] = build_assumption_tool_uses(target, provided_assumptions=provided_assumptions)
    if isinstance(role_obligation_packet, dict):
        result["tool_uses"].append(
            {
                "tool": "build_role_specific_obligations",
                "arguments": {
                    "role": role_obligation_packet.get("role"),
                    "relation_kind": role_obligation_packet.get("relation_kind"),
                },
                "purpose": "Replace generic string-route gaps with source-role-local mathematical obligations.",
                "status": role_obligation_packet.get("status", "completed"),
                "output_contract": "role_specific_obligation_result",
            }
        )
        result["source"]["assumption_route"] = "source_role_specific"
        result["source"]["role_obligations"] = role_obligation_packet
    result["gaps"] = gaps
    result["proposals"] = proposals
    result["validation"] = summarize_assumption_validation(proposals)
    result["actions"].append(
        action(
            "human_review",
            "Review whether route-required assumptions are sufficient for the intended mathematical setting.",
        )
    )
    if proposals:
        result["actions"].append(
            action(
                "review_assumption_proposals",
                "Inspect gap-linked assumption proposals before editing the document or retrying a derivation.",
            )
        )
    result["agent_handoff"] = _assumption_agent_handoff(result)
    refresh_evidence_ledger(result)
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid assumptions_for result: {errors}")
    return result


def _role_specific_assumption_gap_and_proposal(
    target: str,
    *,
    source: dict[str, Any] | None,
    packet: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Package one source-role-local gap without duplicating every obligation."""
    source_context = dict(source or {})
    role = str(packet.get("role", "unsupported_or_ambiguous"))
    local = [item for item in packet.get("local_obligations", []) if isinstance(item, dict)]
    digest = str(source_context.get("obligation_digest", "unbound"))
    gap_id = f"assumption_gap_{digest[:16]}_role_{role}"
    location = str(source_context.get("context_summary") or source_context.get("file") or target)
    evidence_refs = list(dict.fromkeys(
        [str(item) for item in packet.get("evidence_refs", []) if item]
        + [str(item.get("evidence_ref")) for item in local if item.get("evidence_ref")]
    ))
    gap = {
        "id": gap_id,
        "location": location,
        "problem": f"The source-evidenced `{role}` target has {len(local)} undischarged local obligations.",
        "why": (
            "A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. "
            "These local obligations must be bound or discharged before claim promotion."
        ),
        "affected_terms": [target] if target else [],
        "route_categories": sorted({str(item.get("kind")) for item in local if item.get("kind")}),
        "route_kind": role,
        "source": "build_role_specific_obligations",
        "source_context": source_context,
        "evidence_refs": evidence_refs,
        "severity": "high" if role in {"identification_assumption", "statistical_estimator"} else "medium",
        "local_obligations": local,
    }
    missing = [
        (
            f"{item.get('id')} ({item.get('kind')}): {item.get('mathematically_missing')} "
            f"Why missing: {item.get('why_missing')}"
        )
        for item in local
    ]
    proposal = {
        "id": f"assumption_proposal_{digest[:16]}_role_{role}",
        "gap_ids": [gap_id],
        "type": "bind_role_specific_assumptions",
        "location": location,
        "proposal_text": (
            f"State, source-bind, or discharge the {len(local)} local obligations for the source-evidenced "
            f"`{role}` route; do not import downstream conditions as local correctness requirements."
        ),
        "rationale": "The proposal follows the exact source role and normalized relation instead of a generic lexical route.",
        "missing_assumptions": missing,
        "possible_assumption_sets": list(packet.get("possible_assumption_sets", [])),
        "derivation_route": list(packet.get("derivation_route", [])),
        "route_kind": role,
        "local_obligations": local,
        "downstream_integration_obligations": list(packet.get("downstream_integration_obligations", [])),
        "evidence_refs": evidence_refs,
        "application_status": "not_applied",
        "validation": {
            "policy": "source_role_obligation_builder_v1",
            "status": "validated_by_source_role_rule",
            "certifying": False,
            "reason": "The obligation set was selected by an exact source-evidenced routing role.",
            "backend_attempts": [
                {
                    "backend": "build_role_specific_obligations",
                    "status": "diagnostic_only",
                    "severity": "diagnostic",
                    "reason": "Role routing selects relevant checks but cannot establish assumption truth or sufficiency.",
                }
            ],
            "boundary": "Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.",
            "gap_id": gap_id,
        },
    }
    proposal["validation"]["proposal_id"] = proposal["id"]
    return [gap], [proposal]


def score_assumption_set(result: dict[str, Any], expected_terms: set[str]) -> dict[str, Any]:
    """Score assumptions by set containment rather than brittle exact strings."""
    observed = {str(item.get("text", "")).lower() for item in result.get("assumptions", []) if isinstance(item, dict)}
    expected = {term.lower() for term in expected_terms}
    matched = sorted(term for term in expected if any(term in item for item in observed))
    missing = sorted(expected - set(matched))
    return {
        "status": "passed" if not missing else "failed",
        "matched_terms": matched,
        "missing_terms": missing,
        "observed_assumptions": sorted(observed),
        "metadata": {"schema_version": "1.0", "contract": "assumption_set_rubric"},
    }


def _label_source(block: dict[str, Any], *, root: str, label: str) -> dict[str, Any]:
    return {
        "root": root,
        "label": label,
        "file": block.get("file"),
        "line_start": block.get("line_start"),
        "line_end": block.get("line_end"),
        "section_path": block.get("section_path", []),
        "context_summary": f"{block.get('file', root)} > {label} > line {block.get('line_start', 'unknown')}",
    }


def _markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _render_assumption_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Assumption Gap/Proposal Report",
        "",
        f"Question: {report['question']}",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Coverage",
        "",
        f"- Targets inspected: {report['coverage']['target_count']}",
        f"- Gaps: {report['coverage']['gap_count']}",
        f"- Proposals: {report['coverage']['proposal_count']}",
        "",
        "## Tool Uses",
        "",
        "| Tool | Purpose | Status |",
        "| --- | --- | --- |",
    ]
    for item in report["tool_uses"]:
        lines.append(f"| `{_markdown_escape(item.get('tool', ''))}` | {_markdown_escape(item.get('purpose', ''))} | `{_markdown_escape(item.get('status', ''))}` |")
    lines.extend(["", "## Gaps And Proposals", ""])
    for target_result in report["target_results"]:
        label = target_result.get("source", {}).get("label") or target_result.get("target")
        lines.append(f"### {_markdown_escape(label)}")
        lines.append("")
        gaps_by_id = {gap["id"]: gap for gap in target_result.get("gaps", []) if isinstance(gap, dict) and isinstance(gap.get("id"), str)}
        for proposal in target_result.get("proposals", []):
            if not isinstance(proposal, dict):
                continue
            gap = gaps_by_id.get(proposal.get("gap_ids", [""])[0], {})
            validation = proposal.get("validation") if isinstance(proposal.get("validation"), dict) else {}
            lines.extend(
                [
                    f"- Proposal: `{_markdown_escape(proposal.get('id', ''))}`",
                    f"  - Location: `{_markdown_escape(proposal.get('location', gap.get('location', '')))}`",
                    f"  - Problem: {_markdown_escape(gap.get('problem', ''))}",
                    f"  - Why: {_markdown_escape(gap.get('why', ''))}",
                    f"  - Proposed assumption: {_markdown_escape(proposal.get('proposal_text', ''))}",
                    f"  - Validation: `{_markdown_escape(validation.get('status', 'missing'))}`; {_markdown_escape(validation.get('boundary', ''))}",
                    f"  - Evidence refs: {', '.join(f'`{_markdown_escape(ref)}`' for ref in proposal.get('evidence_refs', []))}",
                    "",
                ]
            )
            missing_assumptions = proposal.get("missing_assumptions")
            if isinstance(missing_assumptions, list) and missing_assumptions:
                lines.append("  - Mathematical missing-assumption reasoning:")
                for item in missing_assumptions:
                    lines.append(f"    - {_markdown_escape(item)}")
                lines.append("")
            possible_sets = proposal.get("possible_assumption_sets")
            if isinstance(possible_sets, list) and possible_sets:
                lines.append("  - Possible sufficient assumption sets:")
                for item in possible_sets:
                    if not isinstance(item, dict):
                        continue
                    lines.append(f"    - `{_markdown_escape(item.get('id', 'assumption_set'))}` ({_markdown_escape(item.get('role', 'candidate'))}): {_markdown_escape(item.get('closes', ''))}")
                    assumptions = item.get("assumptions")
                    if isinstance(assumptions, list):
                        for assumption in assumptions:
                            lines.append(f"      - {_markdown_escape(assumption)}")
                lines.append("")
            derivation_route = proposal.get("derivation_route")
            if isinstance(derivation_route, list) and derivation_route:
                lines.append("  - How the derivation works under the assumptions:")
                for item in derivation_route:
                    if isinstance(item, dict):
                        lines.append(f"    - {_markdown_escape(item.get('step', 'step'))}: {_markdown_escape(item.get('detail', ''))}")
                lines.append("")
        if not target_result.get("proposals"):
            lines.append("- No concrete assumption proposal was generated.")
            lines.append("")
    lines.extend(
        [
            "## Non-Claims",
            "",
        ]
    )
    for item in report["non_claims"]:
        lines.append(f"- `{item['code']}`: {item['text']}")
    lines.append("")
    return "\n".join(lines)


def audit_and_propose_assumptions(
    question: str,
    *,
    target: str | None = None,
    root: str | None = None,
    labels: list[str] | None = None,
    file: str | None = None,
    source_digest: str | None = None,
    provided_assumptions: list[str] | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Audit direct targets or document labels and propose assumption repairs."""
    target_results: list[dict[str, Any]] = []
    tool_uses: list[dict[str, Any]] = []
    source: dict[str, Any] = {}
    coverage_gaps: list[str] = []
    label_selection: list[dict[str, Any]] = []

    if target:
        target_result = assumptions_for(target, provided_assumptions=provided_assumptions)
        target_results.append(target_result)
        tool_uses.extend(target_result.get("tool_uses", []))
    if root and labels:
        root_path = Path(root)
        index = build_index(root_path)
        source["root"] = str(root_path)
        if file is not None:
            source["file"] = file
        if source_digest is not None:
            source["source_digest"] = source_digest
        tool_uses.append(
            {
                "tool": "build_index",
                "arguments": {"root": str(root_path)},
                "purpose": "Extract LaTeX labels and source locations for assumption auditing.",
                "status": "completed",
                "output_contract": "latex_index",
            }
        )
        for label in labels:
            if file is not None or source_digest is not None:
                extraction = extract_derivation_targets_for_label(
                    index,
                    label,
                    file=file,
                    source_digest=source_digest,
                )
                label_selection.append(
                    {
                        "label": label,
                        "selection_status": extraction.get("selection_status", extraction.get("status")),
                        "extraction_status": extraction.get("status"),
                        "source_binding": extraction.get("source_binding"),
                        "target_count": len(extraction.get("targets", [])),
                        "obligation_count": len(extraction.get("obligations", [])),
                    }
                )
                selection_status = extraction.get("selection_status")
                if selection_status != "selected":
                    coverage_gaps.append(
                        f"Label `{label}` selection failed with `{selection_status}` under `{root}`."
                    )
                    continue
                extracted_targets = [item for item in extraction.get("targets", []) if isinstance(item, dict)]
                if not extracted_targets:
                    coverage_gaps.append(
                        f"Label `{label}` was source-bound but had no supported assumption target."
                    )
                    continue
                for extracted in extracted_targets:
                    label_source = {
                        "root": str(root_path),
                        "label": extracted.get("label") or label,
                        "parent_label": extracted.get("parent_label") or label,
                        "file": extraction.get("source_binding", {}).get("file") or extracted.get("file"),
                        "source_digest": extraction.get("source_binding", {}).get("source_digest"),
                        "line_start": extracted.get("line_start"),
                        "line_end": extracted.get("line_end"),
                        "obligation_id": extracted.get("obligation_id"),
                        "obligation_digest": extracted.get("obligation_digest"),
                        "normalized_target": extracted.get("normalized_target"),
                        "routing_role": extracted.get("routing_role"),
                        "context_summary": (
                            f"{extracted.get('file', root)} > {label} > "
                            f"line {extracted.get('line_start', 'unknown')}"
                        ),
                    }
                    normalized_target = extracted.get("normalized_target", {})
                    routing_role = extracted.get("routing_role", {})
                    role_packet = None
                    if (
                        isinstance(normalized_target, dict)
                        and isinstance(routing_role, dict)
                        and has_role_specific_builder(routing_role, target=str(extracted.get("target", "")))
                    ):
                        role_packet = build_role_specific_obligations(
                            target=str(extracted.get("target", "")),
                            normalized_target=normalized_target,
                            routing_role=routing_role,
                            evidence_refs=[
                                f"source:{label_source.get('source_digest')}:{label_source.get('obligation_digest')}",
                                f"routing_role:{routing_role.get('role_id', routing_role.get('role', 'unknown'))}",
                            ],
                        )
                    target_result = assumptions_for(
                        str(extracted.get("target", "")),
                        provided_assumptions=provided_assumptions,
                        source=label_source,
                        role_obligation_packet=role_packet,
                    )
                    target_result["extracted_target"] = extracted
                    target_results.append(target_result)
                    tool_uses.extend(target_result.get("tool_uses", []))
                continue
            block = index.get("labels", {}).get(label)
            if not isinstance(block, dict):
                coverage_gaps.append(f"Label `{label}` was not found under `{root}`.")
                continue
            label_source = _label_source(block, root=str(root_path), label=label)
            target_text = str(block.get("text", "")).strip()
            if not target_text:
                coverage_gaps.append(f"Label `{label}` had no extractable text.")
                continue
            target_result = assumptions_for(
                target_text,
                provided_assumptions=provided_assumptions,
                source=label_source,
            )
            target_results.append(target_result)
            tool_uses.extend(target_result.get("tool_uses", []))
    if not target_results:
        status = "needs_evidence"
        reason = "No target or source label produced assumption evidence."
    elif any(result.get("gaps") for result in target_results):
        status = "proposal_ready"
        reason = "Assumption gaps were converted into concrete proposals."
    else:
        status = "no_missing_assumptions_detected"
        reason = "No missing route-required assumptions were detected by the bounded rule set."

    gaps = [gap for result in target_results for gap in result.get("gaps", []) if isinstance(gap, dict)]
    proposals = [proposal for result in target_results for proposal in result.get("proposals", []) if isinstance(proposal, dict)]
    validation = summarize_assumption_validation(proposals)
    non_claims = [ASSUMPTION_REPORT_NON_CLAIM]
    for result in target_results:
        for item in result.get("non_claims", []):
            if isinstance(item, dict) and item not in non_claims:
                non_claims.append(item)
    report = {
        "status": status,
        "question": question,
        "source": source,
        "coverage": {
            "target_count": len(target_results),
            "gap_count": len(gaps),
            "proposal_count": len(proposals),
            "coverage_gaps": coverage_gaps,
            "label_selection": label_selection,
            "not_inspected": [
                "global minimality",
                "proof closure after proposed assumptions",
                "full-document assumption consistency unless labels were supplied",
            ],
        },
        "tool_uses": tool_uses,
        "target_results": target_results,
        "gaps": gaps,
        "proposals": proposals,
        "validation": validation,
        "non_claims": non_claims,
        "next_actions": [
            action("review_assumption_proposals", "Inspect proposed assumptions before applying edits."),
            action("rerun_relevant_audit", "After editing assumptions, rerun the derivation or proof audit that exposed the gap."),
        ],
        "output_path": str(output_path) if output_path else None,
        "metadata": contract_metadata(ASSUMPTION_REPORT_CONTRACT),
    }
    report["markdown"] = _render_assumption_markdown(report)
    report["agent_handoff"] = {
        "scoped_question": question,
        "status": status,
        "reason": reason,
        "gap_count": len(gaps),
        "proposal_count": len(proposals),
        "assumption_gap_ledger": gaps,
        "proposals": proposals,
        "validation": validation,
        "non_claim_boundary": non_claims,
        "next_actions": report["next_actions"],
        "next_artifact": "Review the Markdown report or structured proposals before editing.",
        "certification_boundary": ASSUMPTION_REPORT_NON_CLAIM["text"],
    }
    if output_path:
        write_bytes_safe(Path(output_path), report["markdown"].encode("utf-8"))
    return attach_contract(report, ASSUMPTION_REPORT_CONTRACT)
