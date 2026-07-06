from __future__ import annotations

"""Extract source-local derivation targets from LaTeX index blocks."""

from pathlib import Path
import re
from typing import Any

from .contracts import attach_contract
from .equation_locator import locate_equations_in_text
from .latex_index import build_index


DERIVATION_TARGET_EXTRACTION_CONTRACT = "derivation_target_extraction_result"


def _normalize_math_text(text: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\(?:nonumber|notag)\b", "", text)
    text = text.replace("&", "")
    return text.strip()


def _split_unescaped_equals(text: str) -> tuple[str, str] | None:
    for index, char in enumerate(text):
        if char != "=":
            continue
        if index > 0 and text[index - 1] == "\\":
            continue
        return text[:index].strip(), text[index + 1 :].strip()
    return None


def _target_id(parent_block_id: str, row: dict[str, Any], index: int) -> str:
    row_label = row.get("label")
    suffix = row_label or f"{row.get('environment', 'row')}_{row.get('row_index', index)}"
    safe_suffix = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(suffix)).strip("-")
    return f"{parent_block_id}:target:{safe_suffix}"


def _target_from_row(
    row: dict[str, Any],
    *,
    parent: dict[str, Any],
    row_index: int,
) -> dict[str, Any]:
    clean = _normalize_math_text(str(row.get("text", "")))
    split = _split_unescaped_equals(clean)
    uncertainty = list(row.get("uncertainty", [])) if isinstance(row.get("uncertainty"), list) else []
    if split is None:
        lhs = ""
        rhs = ""
        target = clean
        status = "needs_formalization"
        if "no_unescaped_equality" not in uncertainty:
            uncertainty.append("no_unescaped_equality")
    else:
        lhs, rhs = split
        target = f"{lhs} = {rhs}"
        status = "extracted"
    return {
        "id": _target_id(str(parent.get("block_id", "block")), row, row_index),
        "target": target,
        "lhs": lhs,
        "rhs": rhs,
        "source_text": str(row.get("source_text", "")),
        "file": parent.get("file") or row.get("file"),
        "line_start": row.get("line_start"),
        "line_end": row.get("line_end"),
        "label": row.get("label"),
        "parent_label": parent.get("label"),
        "parent_block_id": parent.get("block_id"),
        "section_path": list(parent.get("section_path", [])),
        "environment": row.get("environment"),
        "row_index": row.get("row_index", row_index),
        "extraction_status": status,
        "localization_status": row.get("localization_status"),
        "uncertainty": uncertainty,
    }


def _fallback_target(parent: dict[str, Any], *, reason: str) -> dict[str, Any]:
    target = str(parent.get("text", "")).strip()
    return {
        "id": f"{parent.get('block_id', 'block')}:target:fallback_full_block",
        "target": target,
        "lhs": "",
        "rhs": "",
        "source_text": target,
        "file": parent.get("file"),
        "line_start": parent.get("line_start"),
        "line_end": parent.get("line_end"),
        "label": parent.get("label"),
        "parent_label": parent.get("label"),
        "parent_block_id": parent.get("block_id"),
        "section_path": list(parent.get("section_path", [])),
        "environment": parent.get("kind"),
        "row_index": 0,
        "extraction_status": "fallback_full_block",
        "localization_status": "not_equation",
        "uncertainty": [reason],
    }


def extract_derivation_targets_from_block(block: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract equation-row derivation targets from one indexed LaTeX block."""
    text = str(block.get("text", ""))
    if not text.strip():
        return []
    rows = locate_equations_in_text(text, relative_path=str(block.get("file", "<memory>")))
    if not rows:
        return [_fallback_target(block, reason="no_display_equation_in_block")]
    line_offset = int(block.get("line_start") or 1) - 1
    targets: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        row_with_global_lines = dict(row)
        if isinstance(row_with_global_lines.get("line_start"), int):
            row_with_global_lines["line_start"] = row_with_global_lines["line_start"] + line_offset
        if isinstance(row_with_global_lines.get("line_end"), int):
            row_with_global_lines["line_end"] = row_with_global_lines["line_end"] + line_offset
        targets.append(_target_from_row(row_with_global_lines, parent=block, row_index=index))
    return targets


def extract_derivation_targets_for_label(index: dict[str, Any], label: str) -> dict[str, Any]:
    """Extract source-local derivation targets for one indexed label."""
    block = index.get("labels", {}).get(label) if isinstance(index.get("labels"), dict) else None
    if not isinstance(block, dict):
        return {
            "label": label,
            "status": "label_not_found",
            "reason": f"Label `{label}` was not found in the index.",
            "targets": [],
            "fallback_count": 0,
        }
    targets = extract_derivation_targets_from_block(block)
    fallback_count = sum(1 for target in targets if target.get("extraction_status") == "fallback_full_block")
    return {
        "label": label,
        "status": "extracted" if targets and fallback_count == 0 else "fallback_used" if targets else "not_extracted",
        "reason": "Extracted equation-row derivation targets." if targets and fallback_count == 0 else "Used explicit full-block fallback.",
        "parent_block": {
            "file": block.get("file"),
            "line_start": block.get("line_start"),
            "line_end": block.get("line_end"),
            "label": block.get("label"),
            "block_id": block.get("block_id"),
            "section_path": block.get("section_path", []),
        },
        "targets": targets,
        "fallback_count": fallback_count,
    }


def extract_derivation_targets(root: str | Path, labels: list[str] | tuple[str, ...] | str) -> dict[str, Any]:
    """Build an index and extract derivation targets for labels."""
    root_path = Path(root)
    label_list = [labels] if isinstance(labels, str) else list(labels)
    index = build_index(root_path)
    label_results = [extract_derivation_targets_for_label(index, str(label)) for label in label_list]
    targets = [
        target
        for label_result in label_results
        for target in label_result.get("targets", [])
        if isinstance(target, dict)
    ]
    fallback_count = sum(1 for target in targets if target.get("extraction_status") == "fallback_full_block")
    result = {
        "status": "extracted" if targets and fallback_count == 0 else "fallback_used" if targets else "not_extracted",
        "root": str(root_path),
        "labels": label_list,
        "target_count": len(targets),
        "fallback_count": fallback_count,
        "label_results": label_results,
        "targets": targets,
        "non_claims": [
            {
                "code": "target_extraction_not_proof",
                "text": "Extracted targets preserve source-local equations for downstream routing; extraction does not prove or refute them.",
            }
        ],
    }
    return attach_contract(result, DERIVATION_TARGET_EXTRACTION_CONTRACT)
