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
from .assumption_discovery import assumptions_required
from .contracts import attach_contract, contract_metadata
from .high_level_contracts import action, refresh_evidence_ledger, validate_high_level_result
from .high_level_workflows import package_assumption_result
from .latex_index import build_index


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
) -> dict[str, Any]:
    """Return route-required assumptions for a scoped target."""
    low_level = assumptions_required(target, provided_assumptions=provided_assumptions)
    result = package_assumption_result(low_level, question=f"What assumptions are required for {target}?")
    gaps = build_assumption_gaps(target, low_level.get("assumptions", []), source=source)
    proposals = build_assumption_proposals(gaps)
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
    provided_assumptions: list[str] | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Audit direct targets or document labels and propose assumption repairs."""
    target_results: list[dict[str, Any]] = []
    tool_uses: list[dict[str, Any]] = []
    source: dict[str, Any] = {}
    coverage_gaps: list[str] = []

    if target:
        target_result = assumptions_for(target, provided_assumptions=provided_assumptions)
        target_results.append(target_result)
        tool_uses.extend(target_result.get("tool_uses", []))
    if root and labels:
        root_path = Path(root)
        index = build_index(root_path)
        source["root"] = str(root_path)
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
        Path(output_path).write_text(report["markdown"], encoding="utf-8")
    return attach_contract(report, ASSUMPTION_REPORT_CONTRACT)
