from __future__ import annotations

"""Render derivation search trees into agent-consumable repair reports."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .derivation_search_tree import branch_promotion_report, summarize_search_tree


DERIVATION_TREE_REPORT_CONTRACT = "derivation_tree_report_result"
DERIVATION_TREE_REPORT_BOUNDARY = (
    "This report renders existing derivation-search tree evidence. It does not "
    "invent assumptions, apply patches, or certify claims beyond the tree's "
    "promotion guard."
)


@dataclass(frozen=True)
class TreeReportSection:
    id: str
    status: str
    location: str
    problem: str
    mathematical_why: str
    assumptions: list[dict[str, Any]]
    derivation_steps: list[dict[str, Any]]
    tools_used: list[dict[str, Any]]
    proposed_patches: list[dict[str, Any]]
    blockers: list[dict[str, Any]]
    warnings: list[str]
    promotion: dict[str, Any]


def _markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _location_from_span(span: dict[str, Any] | None) -> str:
    if not isinstance(span, dict) or not span:
        return "unknown location"
    parts: list[str] = []
    if span.get("file"):
        parts.append(str(span["file"]))
    section_path = span.get("section_path")
    if isinstance(section_path, list):
        parts.extend(str(item) for item in section_path if item)
    if span.get("label"):
        parts.append(str(span["label"]))
    if span.get("line_start"):
        line = f"line {span['line_start']}"
        if span.get("line_end") and span.get("line_end") != span.get("line_start"):
            line += f"-{span['line_end']}"
        parts.append(line)
    return " > ".join(parts) if parts else "unknown location"


def _location_from_patch(patch: dict[str, Any]) -> str | None:
    location = patch.get("location")
    if isinstance(location, dict) and location:
        return _location_from_span(location)
    return None


def _tools_used(node: dict[str, Any]) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for attempt in node.get("backend_attempts", []):
        if not isinstance(attempt, dict):
            continue
        tools.append(
            {
                "id": attempt.get("id"),
                "tool": attempt.get("tool"),
                "status": attempt.get("status"),
                "evidence_kind": attempt.get("evidence_kind"),
                "certification_status": attempt.get("certification_status"),
                "output_ref": attempt.get("output_ref"),
                "boundary": attempt.get("boundary"),
            }
        )
    return tools


def _problem_for_node(node: dict[str, Any], promotion: dict[str, Any]) -> str:
    status = str(node.get("status", "unknown"))
    target = str(node.get("target", "target"))
    if status == "proved" and promotion.get("can_promote") is True:
        return f"The target `{target}` has scoped certifying evidence in this branch."
    if status == "proved":
        return f"The target `{target}` is marked proved, but the promotion guard does not support that claim."
    if status == "refuted" and promotion.get("can_promote") is True:
        return f"The target `{target}` has scoped refuting evidence in this branch."
    if status == "refuted":
        return f"The target `{target}` is marked refuted, but the promotion guard does not support that claim."
    if status == "blocked":
        return f"The target `{target}` is blocked before derivation search can proceed."
    if status == "budget_exhausted":
        return f"The target `{target}` exhausted the branch-search budget before proof or refutation."
    return f"The target `{target}` remains partially resolved or diagnostic-only."


def _why_for_node(node: dict[str, Any], promotion: dict[str, Any]) -> str:
    status = str(node.get("status", "unknown"))
    if status in {"proved", "refuted"} and promotion.get("can_promote") is True:
        return str(promotion.get("reason") or "Promotion guard accepted scoped backend evidence.")
    if status in {"proved", "refuted"}:
        errors = promotion.get("errors")
        return f"Promotion guard rejected the status: {errors or ['no promotable backend evidence']}"
    blockers = [item for item in node.get("blockers", []) if isinstance(item, dict)]
    if blockers:
        first = blockers[0]
        return str(first.get("why") or first.get("problem") or "A blocker remains in the tree evidence.")
    attempts = [item for item in node.get("backend_attempts", []) if isinstance(item, dict)]
    if attempts:
        return "Existing backend attempts are diagnostic only and do not satisfy the promotion guard."
    return "No backend evidence has been recorded for this branch."


def _patch_warnings(node: dict[str, Any]) -> list[str]:
    patches = [item for item in node.get("patch_candidates", []) if isinstance(item, dict)]
    warnings: list[str] = []
    if not patches and node.get("status") not in {"proved", "refuted"}:
        warnings.append("No patch candidate is present in the tree; the renderer will not invent one.")
    for patch in patches:
        if not patch.get("location"):
            warnings.append(f"Patch `{patch.get('id', 'unknown')}` lacks a location.")
        if not patch.get("proposed_text"):
            warnings.append(f"Patch `{patch.get('id', 'unknown')}` lacks proposed text.")
        if not patch.get("rationale"):
            warnings.append(f"Patch `{patch.get('id', 'unknown')}` lacks rationale.")
    return warnings


def _section_for_node(node: dict[str, Any]) -> dict[str, Any]:
    promotion = branch_promotion_report(node)
    patches = [item for item in node.get("patch_candidates", []) if isinstance(item, dict)]
    location = _location_from_span(node.get("source_span"))
    if location == "unknown location" and patches:
        location = _location_from_patch(patches[0]) or location
    section = TreeReportSection(
        id=str(node.get("id", "root")),
        status=str(node.get("status", "unknown")),
        location=location,
        problem=_problem_for_node(node, promotion),
        mathematical_why=_why_for_node(node, promotion),
        assumptions=[item for item in node.get("assumptions", []) if isinstance(item, dict)],
        derivation_steps=[item for item in node.get("derivation_steps", []) if isinstance(item, dict)],
        tools_used=_tools_used(node),
        proposed_patches=patches,
        blockers=[item for item in node.get("blockers", []) if isinstance(item, dict)],
        warnings=_patch_warnings(node),
        promotion=promotion,
    )
    return asdict(section)


def _walk_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = [node]
    children = node.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                nodes.extend(_walk_nodes(child))
    return nodes


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Derivation Tree Evidence Report",
        "",
        f"Status: `{_markdown_escape(report.get('status', 'unknown'))}`",
        "",
        "## Summary",
        "",
    ]
    summary = report.get("summary", {})
    for key in ("node_count", "blocker_count", "backend_attempt_count", "patch_candidate_count"):
        lines.append(f"- {key}: `{_markdown_escape(summary.get(key, 0))}`")
    lines.append("")
    lines.extend(["## Branch Sections", ""])
    for section in report.get("sections", []):
        lines.extend(
            [
                f"### `{_markdown_escape(section.get('id', 'node'))}`",
                "",
                f"- Status: `{_markdown_escape(section.get('status', 'unknown'))}`",
                f"- Location: `{_markdown_escape(section.get('location', 'unknown location'))}`",
                f"- Problem: {_markdown_escape(section.get('problem', ''))}",
                f"- Why: {_markdown_escape(section.get('mathematical_why', ''))}",
                f"- Promotion guard: `can_promote={_markdown_escape(section.get('promotion', {}).get('can_promote', False))}`",
                f"- Promotion evidence refs: `{_markdown_escape(section.get('promotion', {}).get('evidence_refs', []))}`",
                f"- Promotion errors: `{_markdown_escape(section.get('promotion', {}).get('errors', []))}`",
                "",
                "Tools used:",
            ]
        )
        tools = section.get("tools_used", [])
        if tools:
            for tool in tools:
                lines.append(
                    f"- `{_markdown_escape(tool.get('id', ''))}`: "
                    f"`{_markdown_escape(tool.get('tool', ''))}` "
                    f"status `{_markdown_escape(tool.get('status', ''))}`, "
                    f"evidence `{_markdown_escape(tool.get('evidence_kind', ''))}`, "
                    f"certification `{_markdown_escape(tool.get('certification_status', ''))}`"
                )
        else:
            lines.append("- No backend/tool attempts recorded.")
        lines.append("")
        assumptions = section.get("assumptions", [])
        lines.append("Assumptions/routes:")
        if assumptions:
            for assumption in assumptions:
                lines.append(
                    f"- `{_markdown_escape(assumption.get('id', 'assumption'))}` "
                    f"status `{_markdown_escape(assumption.get('status', ''))}`: "
                    f"{_markdown_escape(assumption.get('assumptions', []))}"
                )
        else:
            lines.append("- No assumption set recorded.")
        lines.append("")
        steps = section.get("derivation_steps", [])
        lines.append("Derivation evidence:")
        if steps:
            for step in steps:
                lines.append(
                    f"- `{_markdown_escape(step.get('id', 'step'))}`: "
                    f"{_markdown_escape(step.get('claim', ''))} "
                    f"({ _markdown_escape(step.get('checker_status', '')) })"
                )
        else:
            lines.append("- No derivation steps recorded.")
        lines.append("")
        patches = section.get("proposed_patches", [])
        lines.append("Proposed patches:")
        if patches:
            for patch in patches:
                lines.extend(
                    [
                        f"- `{_markdown_escape(patch.get('id', 'patch'))}` ({_markdown_escape(patch.get('validation_status', ''))})",
                        f"  - Location: `{_markdown_escape(_location_from_patch(patch) or 'unknown location')}`",
                        f"  - Proposed fix: {_markdown_escape(patch.get('proposed_text', ''))}",
                        f"  - Rationale: {_markdown_escape(patch.get('rationale', ''))}",
                    ]
                )
        else:
            lines.append("- No patch candidate supplied by the tree.")
        lines.append("")
        blockers = section.get("blockers", [])
        lines.append("Remaining blockers:")
        if blockers:
            for blocker in blockers:
                lines.extend(
                    [
                        f"- `{_markdown_escape(blocker.get('id', 'blocker'))}` ({_markdown_escape(blocker.get('kind', ''))})",
                        f"  - Problem: {_markdown_escape(blocker.get('problem', ''))}",
                        f"  - Required next evidence: {_markdown_escape(blocker.get('required_next_evidence', ''))}",
                    ]
                )
        else:
            lines.append("- None recorded.")
        warnings = section.get("warnings", [])
        if warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in warnings:
                lines.append(f"- {_markdown_escape(warning)}")
        lines.append("")
    lines.extend(["## Non-Claims", ""])
    for item in report.get("non_claims", []):
        if isinstance(item, dict):
            lines.append(f"- `{_markdown_escape(item.get('code', 'non_claim'))}`: {_markdown_escape(item.get('text', ''))}")
        else:
            lines.append(f"- {_markdown_escape(item)}")
    return "\n".join(lines).rstrip() + "\n"


def render_derivation_tree_report(tree: dict[str, Any]) -> dict[str, Any]:
    """Render a derivation search tree into structured sections and Markdown."""
    root = tree.get("root") if isinstance(tree, dict) else None
    if not isinstance(root, dict):
        result = {
            "status": "invalid",
            "reason": "Tree is missing a root node.",
            "summary": summarize_search_tree({}),
            "sections": [],
            "markdown": "",
            "non_claims": [{"code": "invalid_tree_not_report", "text": DERIVATION_TREE_REPORT_BOUNDARY}],
            "boundary": DERIVATION_TREE_REPORT_BOUNDARY,
        }
        result["markdown"] = _render_markdown(result)
        return attach_contract(result, DERIVATION_TREE_REPORT_CONTRACT)
    sections = [_section_for_node(node) for node in _walk_nodes(root)]
    non_claims = list(tree.get("non_claims", []))
    non_claims.append({"code": "tree_report_not_patch_or_proof", "text": DERIVATION_TREE_REPORT_BOUNDARY})
    result = {
        "status": str(tree.get("status") or root.get("status", "unknown")),
        "reason": "Rendered derivation-search tree evidence into an agent-consumable report.",
        "summary": summarize_search_tree(tree),
        "sections": sections,
        "markdown": "",
        "non_claims": non_claims,
        "boundary": DERIVATION_TREE_REPORT_BOUNDARY,
    }
    result["markdown"] = _render_markdown(result)
    return attach_contract(result, DERIVATION_TREE_REPORT_CONTRACT)
