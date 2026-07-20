from __future__ import annotations

"""Source-aware derivation gap/proposal reports."""

from pathlib import Path
from typing import Any

from .contracts import attach_contract, contract_metadata
from .artifact_storage import write_bytes_safe
from .backend_route_planner import plan_backend_routes
from .derivation_gap_proposals import DERIVATION_VALIDATION_BOUNDARY, summarize_derivation_validation
from .derivation_target_extraction import extract_derivation_targets_for_label
from .derive_from import derive_from
from .high_level_contracts import action
from .latex_index import build_index


DERIVATION_AUDIT_REPORT_CONTRACT = "derivation_audit_report_result"
DERIVATION_AUDIT_REPORT_NON_CLAIM = {
    "code": "derivation_audit_report_not_applied_or_certified",
    "text": (
        "The derivation audit report is diagnostic guidance only; it does not "
        "apply edits, prove full-document correctness, or certify proposed "
        "repairs unless a scoped backend certificate or concrete counterexample "
        "is explicitly recorded."
    ),
}


def audit_derivation_extraction_boundary(
    root: str | Path,
    labels: list[str] | tuple[str, ...] | str,
    *,
    file: str | None = None,
    source_digest: str | None = None,
) -> dict[str, Any]:
    """Audit extraction identities without planning or executing backends."""
    root_path = Path(root)
    label_list = [labels] if isinstance(labels, str) else list(labels)
    index = build_index(root_path)
    label_results = [
        extract_derivation_targets_for_label(index, str(label), file=file, source_digest=source_digest)
        for label in label_list
    ]
    targets = [
        target
        for result in label_results
        for target in result.get("targets", [])
        if isinstance(target, dict) and target.get("adapter_eligible") is True
    ]
    obligations = [
        obligation
        for result in label_results
        for obligation in result.get("obligations", [])
        if isinstance(obligation, dict)
    ]
    return {
        "schema_version": "p02_derivation_audit_extraction_boundary@1",
        "status": "extracted" if obligations and len(targets) == len(obligations) else "quarantined",
        "root": str(root_path),
        "file": file,
        "source_digest": source_digest,
        "labels": label_list,
        "label_results": label_results,
        "obligations": obligations,
        "targets": targets,
        "route_plans": [],
        "target_results": [],
        "backend_request_count": 0,
        "publication_enabled": False,
        "non_claims": [
            "No mathematical backend was requested or executed.",
            "A valid extraction is not a proof, semantic interpretation, or repair proposal.",
        ],
    }


def _markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


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


def _target_source(target: dict[str, Any], *, root: str, requested_label: str) -> dict[str, Any]:
    label = target.get("label") or requested_label
    parent_label = target.get("parent_label") or requested_label
    return {
        "root": root,
        "label": label,
        "parent_label": parent_label,
        "file": target.get("file"),
        "source_digest": target.get("label_scoped_obligation", {}).get("document", {}).get("source_digest"),
        "obligation_id": target.get("obligation_id"),
        "obligation_digest": target.get("obligation_digest"),
        "line_start": target.get("line_start"),
        "line_end": target.get("line_end"),
        "section_path": target.get("section_path", []),
        "block_id": target.get("parent_block_id"),
        "target_id": target.get("id"),
        "environment": target.get("environment"),
        "row_index": target.get("row_index"),
        "extraction_status": target.get("extraction_status"),
        "context_summary": (
            f"{target.get('file', root)} > {parent_label} > {label} > "
            f"line {target.get('line_start', 'unknown')}"
        ),
    }


def _direct_source(target: str) -> dict[str, Any]:
    return {
        "target": target,
        "context_summary": target,
    }


def _normalize_labels(labels: list[str] | tuple[str, ...] | str | None) -> list[str]:
    if labels is None:
        return []
    if isinstance(labels, str):
        return [labels]
    return [str(label) for label in labels if str(label)]


def _collect_non_claims(target_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    non_claims = [DERIVATION_AUDIT_REPORT_NON_CLAIM]
    for result in target_results:
        for item in result.get("non_claims", []):
            if isinstance(item, dict) and item not in non_claims:
                non_claims.append(item)
    return non_claims


def _render_tool_uses(lines: list[str], tool_uses: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "## Tool Uses",
            "",
            "| Tool | Purpose | Status | Output | Arguments |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in tool_uses:
        lines.append(
            "| "
            f"`{_markdown_escape(item.get('tool', ''))}` | "
            f"{_markdown_escape(item.get('purpose', ''))} | "
            f"`{_markdown_escape(item.get('status', ''))}` | "
            f"`{_markdown_escape(item.get('output_contract', ''))}` | "
            f"`{_markdown_escape(item.get('arguments', {}))}` |"
        )
    lines.append("")


def _render_extracted_targets(lines: list[str], report: dict[str, Any]) -> None:
    extraction = report.get("target_extraction")
    if not isinstance(extraction, dict) or not extraction.get("label_results"):
        return
    lines.extend(
        [
            "## Extracted Targets",
            "",
            f"- Extracted target count: {report['coverage'].get('extracted_target_count', 0)}",
            f"- Full-block fallback count: {report['coverage'].get('fallback_target_count', 0)}",
            "",
        ]
    )
    for label_result in extraction.get("label_results", []):
        if not isinstance(label_result, dict):
            continue
        lines.append(f"### Parent Label: `{_markdown_escape(label_result.get('label', ''))}`")
        lines.append("")
        for target in label_result.get("targets", []):
            if not isinstance(target, dict):
                continue
            lines.extend(
                [
                    f"- Target: `{_markdown_escape(target.get('label') or target.get('id', ''))}`",
                    f"  - Location: `{_markdown_escape(target.get('file', ''))} > line {_markdown_escape(target.get('line_start', 'unknown'))}`",
                    f"  - Extraction status: `{_markdown_escape(target.get('extraction_status', ''))}`",
                    f"  - LHS: `{_markdown_escape(target.get('lhs', ''))}`",
                    f"  - RHS: `{_markdown_escape(target.get('rhs', ''))}`",
                    "",
                ]
            )


def _render_route_plans(lines: list[str], report: dict[str, Any]) -> None:
    route_plans = [plan for plan in report.get("route_plans", []) if isinstance(plan, dict)]
    if not route_plans:
        return
    lines.extend(["## Backend Route Plans", ""])
    for plan in route_plans:
        source = plan.get("source") if isinstance(plan.get("source"), dict) else {}
        selected = plan.get("selected_route") if isinstance(plan.get("selected_route"), dict) else {}
        lines.extend(
            [
                f"### {_markdown_escape(source.get('parent_label') or source.get('label') or plan.get('target', 'target'))}",
                "",
                f"- Target label: `{_markdown_escape(source.get('label', ''))}`",
                f"- Location: `{_markdown_escape(source.get('file', ''))} > line {_markdown_escape(source.get('line_start', 'unknown'))}`",
                f"- Selected route: `{_markdown_escape(selected.get('backend', 'none'))}:{_markdown_escape(selected.get('route_type', 'none'))}` with status `{_markdown_escape(selected.get('status', 'missing'))}`",
                f"- Boundary: {_markdown_escape(plan.get('boundary', ''))}",
                "",
                "| Backend | Route | Status | Tool | Evidence Contract | Reason |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for candidate in plan.get("candidates", []):
            if not isinstance(candidate, dict):
                continue
            lines.append(
                "| "
                f"`{_markdown_escape(candidate.get('backend', ''))}` | "
                f"`{_markdown_escape(candidate.get('route_type', ''))}` | "
                f"`{_markdown_escape(candidate.get('status', ''))}` | "
                f"`{_markdown_escape(candidate.get('tool', ''))}` | "
                f"`{_markdown_escape(candidate.get('evidence_contract', ''))}` | "
                f"{_markdown_escape(candidate.get('reason', ''))} |"
            )
        lines.append("")


def _render_steps(lines: list[str], title: str, steps: list[dict[str, Any]]) -> None:
    if not steps:
        return
    lines.append(f"  - {title}:")
    for step in steps:
        if not isinstance(step, dict):
            continue
        label = step.get("step") or step.get("tool") or "step"
        detail = step.get("detail") or step.get("reason") or ""
        artifact = step.get("expected_artifact")
        suffix = f" Expected artifact: `{_markdown_escape(artifact)}`." if artifact else ""
        lines.append(f"    - {_markdown_escape(label)}: {_markdown_escape(detail)}{suffix}")
    lines.append("")


def _render_assumption_repairs(lines: list[str], repairs: list[dict[str, Any]]) -> None:
    if not repairs:
        return
    lines.append("  - Linked assumption repairs:")
    for repair in repairs:
        if not isinstance(repair, dict):
            continue
        validation = repair.get("validation") if isinstance(repair.get("validation"), dict) else {}
        lines.extend(
            [
                f"    - Proposal: `{_markdown_escape(repair.get('id', ''))}`",
                f"      - Proposed assumption: {_markdown_escape(repair.get('proposal_text', ''))}",
                f"      - Validation: `{_markdown_escape(validation.get('status', 'missing'))}`; {_markdown_escape(validation.get('boundary', ''))}",
            ]
        )
        missing = repair.get("missing_assumptions")
        if isinstance(missing, list) and missing:
            lines.append("      - Mathematical missing-assumption reasoning:")
            for item in missing:
                lines.append(f"        - {_markdown_escape(item)}")
        possible_sets = repair.get("possible_assumption_sets")
        if isinstance(possible_sets, list) and possible_sets:
            lines.append("      - Possible sufficient assumption sets:")
            for item in possible_sets:
                if not isinstance(item, dict):
                    continue
                lines.append(
                    f"        - `{_markdown_escape(item.get('id', 'assumption_set'))}` "
                    f"({_markdown_escape(item.get('role', 'candidate'))}): "
                    f"{_markdown_escape(item.get('closes', ''))}"
                )
                assumptions = item.get("assumptions")
                if isinstance(assumptions, list):
                    for assumption in assumptions:
                        lines.append(f"          - {_markdown_escape(assumption)}")
        route = repair.get("derivation_route")
        if isinstance(route, list) and route:
            lines.append("      - How the derivation works under the assumptions:")
            for step in route:
                if isinstance(step, dict):
                    lines.append(f"        - {_markdown_escape(step.get('step', 'step'))}: {_markdown_escape(step.get('detail', ''))}")
    lines.append("")


def _render_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Derivation Gap/Proposal Report",
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
        f"- Certifying proposals: {report['validation']['certifying_proposal_count']}",
        "",
    ]
    coverage_gaps = report["coverage"].get("coverage_gaps", [])
    if coverage_gaps:
        lines.append("Coverage gaps:")
        for gap in coverage_gaps:
            lines.append(f"- {_markdown_escape(gap)}")
        lines.append("")
    _render_extracted_targets(lines, report)
    _render_route_plans(lines, report)
    _render_tool_uses(lines, report.get("tool_uses", []))
    lines.extend(["## Gaps And Proposals", ""])
    for target_result in report.get("target_results", []):
        if not isinstance(target_result, dict):
            continue
        source = target_result.get("source") if isinstance(target_result.get("source"), dict) else {}
        label = source.get("label") or target_result.get("question") or target_result.get("answer")
        lines.append(f"### {_markdown_escape(label)}")
        lines.append("")
        gaps_by_id = {
            gap["id"]: gap
            for gap in target_result.get("gaps", [])
            if isinstance(gap, dict) and isinstance(gap.get("id"), str)
        }
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
                    f"  - Proposed fix: {_markdown_escape(proposal.get('proposal_text', ''))}",
                    f"  - Validation: `{_markdown_escape(validation.get('status', 'missing'))}`; {_markdown_escape(validation.get('reason', ''))}; {_markdown_escape(validation.get('boundary', ''))}",
                    f"  - Evidence refs: {', '.join(f'`{_markdown_escape(ref)}`' for ref in proposal.get('evidence_refs', []))}",
                    "",
                ]
            )
            _render_steps(lines, "Derivation route", proposal.get("derivation_route", []))
            _render_steps(lines, "Backend plan", proposal.get("backend_plan", []))
            formalization = proposal.get("formalization_target")
            if isinstance(formalization, dict) and formalization.get("needed_before_claim"):
                required = formalization.get("required_fields", [])
                lines.append(
                    "  - Formalization target: "
                    + ", ".join(f"`{_markdown_escape(item)}`" for item in required if isinstance(item, str))
                )
                lines.append("")
            _render_assumption_repairs(lines, proposal.get("assumption_repairs", []))
        if not target_result.get("proposals"):
            lines.append("- No derivation proposal was generated.")
            lines.append("")
    lines.extend(["## Non-Claims", ""])
    for item in report.get("non_claims", []):
        if isinstance(item, dict):
            lines.append(f"- `{_markdown_escape(item.get('code', ''))}`: {_markdown_escape(item.get('text', ''))}")
    lines.append("")
    return "\n".join(lines)


def audit_and_propose_derivations(
    question: str,
    *,
    target: str | None = None,
    root: str | None = None,
    labels: list[str] | tuple[str, ...] | str | None = None,
    file: str | None = None,
    source_digest: str | None = None,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    backend: str = "auto",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Audit direct derivation targets or LaTeX labels and propose repairs."""
    target_results: list[dict[str, Any]] = []
    tool_uses: list[dict[str, Any]] = []
    coverage_gaps: list[str] = []
    route_plans: list[dict[str, Any]] = []
    label_extraction_results: list[dict[str, Any]] = []
    label_selection: list[dict[str, Any]] = []
    source: dict[str, Any] = {}
    given_list = list(givens or [])
    assumption_list = list(assumptions or [])

    if target:
        route_plan = plan_backend_routes(target)
        tool_uses.append(
            {
                "tool": "plan_backend_routes",
                "arguments": {"target": target},
                "purpose": "Plan deterministic backend routes for the direct target without claiming proof.",
                "status": route_plan.get("status", "unknown"),
                "output_contract": "backend_route_plan_result",
            }
        )
        route_plans.append(route_plan)
        result = derive_from(
            target,
            givens=given_list,
            assumptions=assumption_list,
            source=_direct_source(target),
            backend=backend,
        )
        target_results.append(result)
        tool_uses.extend(result.get("tool_uses", []))

    normalized_labels = _normalize_labels(labels)
    if root and normalized_labels:
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
                "purpose": "Extract LaTeX labels and source locations for derivation auditing.",
                "status": "completed",
                "output_contract": "latex_index",
            }
        )
        for label in normalized_labels:
            extraction = extract_derivation_targets_for_label(
                index,
                label,
                file=file,
                source_digest=source_digest,
            )
            label_extraction_results.append(extraction)
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
            tool_uses.append(
                {
                    "tool": "extract_derivation_targets_for_label",
                    "arguments": {
                        "root": str(root_path),
                        "label": label,
                        "file": file,
                        "source_digest": source_digest,
                    },
                    "purpose": "Extract source-local equation or align-row obligations from the label block.",
                    "status": extraction.get("status", "unknown"),
                    "output_contract": "derivation_target_extraction_result",
                }
            )
            selection_status = extraction.get("selection_status")
            if selection_status != "selected":
                if selection_status == "label_absent":
                    coverage_gaps.append(f"Label `{label}` was not found under `{root_path}`.")
                else:
                    coverage_gaps.append(
                        f"Label `{label}` selection failed with `{selection_status}` under `{root_path}`."
                    )
                continue
            extracted_targets = [item for item in extraction.get("targets", []) if isinstance(item, dict)]
            if not extracted_targets:
                if file is None and source_digest is None:
                    coverage_gaps.append(f"Label `{label}` had no extractable derivation targets.")
                else:
                    coverage_gaps.append(f"Label `{label}` was source-bound but had no supported derivation target.")
                continue
            for extracted in extracted_targets:
                source_context = _target_source(extracted, root=str(root_path), requested_label=label)
                route_plan = plan_backend_routes(extracted)
                route_plan["source"] = source_context
                route_plans.append(route_plan)
                tool_uses.append(
                    {
                        "tool": "plan_backend_routes",
                        "arguments": {
                            "target_id": extracted.get("id"),
                            "label": extracted.get("label"),
                            "parent_label": extracted.get("parent_label"),
                        },
                        "purpose": "Plan deterministic backend routes for the extracted obligation without claiming proof.",
                        "status": route_plan.get("status", "unknown"),
                        "output_contract": "backend_route_plan_result",
                    }
                )
                result = derive_from(
                    str(extracted.get("target", "")),
                    givens=given_list,
                    assumptions=assumption_list,
                    source=source_context,
                    lhs=str(extracted.get("lhs", "")) or None,
                    rhs=str(extracted.get("rhs", "")) or None,
                    backend=backend,
                )
                result["extracted_target"] = extracted
                result["backend_route_plan"] = route_plan
                target_results.append(result)
                tool_uses.extend(result.get("tool_uses", []))

    if not target_results:
        status = "needs_evidence"
        reason = "No target or source label produced derivation evidence."
    elif any(result.get("proposals") for result in target_results):
        status = "proposal_ready"
        reason = "Derivation evidence was converted into gap-linked proposals."
    else:
        status = "no_proposals"
        reason = "No derivation proposals were generated."

    gaps = [gap for result in target_results for gap in result.get("gaps", []) if isinstance(gap, dict)]
    proposals = [
        proposal
        for result in target_results
        for proposal in result.get("proposals", [])
        if isinstance(proposal, dict)
    ]
    validation = summarize_derivation_validation(proposals)
    non_claims = _collect_non_claims(target_results)
    report = {
        "status": status,
        "question": question,
        "source": source,
        "coverage": {
            "target_count": len(target_results),
            "label_count": len(normalized_labels),
            "extracted_target_count": sum(
                1
                for label_result in label_extraction_results
                for target_item in label_result.get("targets", [])
                if isinstance(target_item, dict) and target_item.get("extraction_status") != "fallback_full_block"
            ),
            "fallback_target_count": sum(
                1
                for label_result in label_extraction_results
                for target_item in label_result.get("targets", [])
                if isinstance(target_item, dict) and target_item.get("extraction_status") == "fallback_full_block"
            ),
            "gap_count": len(gaps),
            "proposal_count": len(proposals),
            "coverage_gaps": coverage_gaps,
            "label_selection": label_selection,
            "not_inspected": [
                "automatic source edits",
                "full-document derivation correctness",
                "global theorem applicability",
                "proof closure after proposed assumptions unless backend-certified",
            ],
        },
        "tool_uses": tool_uses,
        "target_extraction": {
            "label_results": label_extraction_results,
            "boundary": "Target extraction preserves source-local obligations but is not proof.",
        },
        "route_plans": route_plans,
        "target_results": target_results,
        "gaps": gaps,
        "proposals": proposals,
        "validation": validation,
        "non_claims": non_claims,
        "next_actions": [
            action("review_derivation_proposals", "Inspect proposed derivation repairs before editing."),
            action("rerun_relevant_audit", "After editing or formalizing, rerun the relevant derivation audit."),
        ],
        "output_path": str(output_path) if output_path else None,
        "agent_handoff": {
            "scoped_question": question,
            "status": status,
            "reason": reason,
            "gap_count": len(gaps),
            "proposal_count": len(proposals),
            "derivation_gap_ledger": gaps,
            "proposals": proposals,
            "validation": validation,
            "non_claim_boundary": non_claims,
            "next_actions": [
                action("review_derivation_proposals", "Inspect proposed derivation repairs before editing."),
                action("rerun_relevant_audit", "After editing or formalizing, rerun the relevant derivation audit."),
            ],
            "certification_boundary": DERIVATION_VALIDATION_BOUNDARY,
        },
        "certification_boundary": DERIVATION_VALIDATION_BOUNDARY,
        "metadata": contract_metadata(DERIVATION_AUDIT_REPORT_CONTRACT),
    }
    report["markdown"] = _render_report_markdown(report)
    if output_path:
        write_bytes_safe(Path(output_path), report["markdown"].encode("utf-8"))
    return attach_contract(report, DERIVATION_AUDIT_REPORT_CONTRACT)
