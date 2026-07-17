from __future__ import annotations

"""Extract source-local derivation targets from LaTeX index blocks."""

import hashlib
from functools import lru_cache
from pathlib import Path
import re
from typing import Any

from .contracts import attach_contract
from .equation_locator import locate_equations_in_text
from .label_scoped_obligation import (
    FIXTURE_CORPUS_VERSION,
    FROZEN_CORPUS_VERSION,
    extract_label_scoped_obligations,
    lookup_label_scoped_obligation,
)
from .latex_index import build_index, extract_paragraph_context_for_label, resolve_label_occurrences
from .source_routing_role import infer_source_routing_role
from .specialist_execution import execute_source_bound_specialist


DERIVATION_TARGET_EXTRACTION_CONTRACT = "derivation_target_extraction_result"
PROPOSITION_CONTEXT_PACKET_CONTRACT = "proposition_context_packet_result"
FROZEN_SOURCE_REFS = frozenset(
    {
        "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex",
        "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
    }
)


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


def _workspace_root(path: Path) -> Path:
    current = path.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def _workspace_source(index: dict[str, Any], occurrence: dict[str, Any]) -> tuple[Path, str, str]:
    index_root = Path(index["root"]).resolve()
    source_path = (index_root / str(occurrence["file"])).resolve()
    workspace = _workspace_root(index_root)
    try:
        source_ref = source_path.relative_to(workspace).as_posix()
    except ValueError:
        source_ref = source_path.relative_to(index_root).as_posix()
    corpus_version = FROZEN_CORPUS_VERSION if source_ref in FROZEN_SOURCE_REFS else FIXTURE_CORPUS_VERSION
    return source_path, source_ref, corpus_version


def _resolve_occurrence(index: dict[str, Any], label: str, file: str | None) -> dict[str, Any]:
    if file is None:
        return resolve_label_occurrences(index, label)
    direct = resolve_label_occurrences(index, label, file=file)
    if direct["status"] != "label_not_found":
        return direct
    matches: list[dict[str, Any]] = []
    for occurrence in index.get("label_occurrences", {}).get(label, []):
        if not isinstance(occurrence, dict):
            continue
        _, source_ref, _ = _workspace_source(index, occurrence)
        if source_ref == file:
            matches.append(occurrence)
    if len(matches) == 1:
        return {"status": "resolved", "label": label, "file": file, "occurrence": matches[0], "occurrences": matches}
    if len(matches) > 1:
        return {"status": "ambiguous", "label": label, "file": file, "occurrence": None, "occurrences": matches}
    return direct


def _obligation_for_occurrence(index: dict[str, Any], occurrence: dict[str, Any], label: str) -> dict[str, Any]:
    source_path, source_ref, corpus_version = _workspace_source(index, occurrence)
    source_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    obligations = list(
        _cached_source_obligations(
            str(source_path),
            source_ref,
            corpus_version,
            source_digest,
        )
    )
    return lookup_label_scoped_obligation(obligations, label, file=source_ref)


@lru_cache(maxsize=16)
def _cached_source_obligations(
    source_path: str,
    source_ref: str,
    corpus_version: str,
    source_digest: str,
) -> tuple[dict[str, Any], ...]:
    raw = Path(source_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != source_digest:
        raise ValueError("source bytes changed while building the obligation cache")
    return tuple(
        extract_label_scoped_obligations(
            raw,
            source_ref=source_ref,
            corpus_version=corpus_version,
        )
    )


def _target_from_obligation(
    obligation: dict[str, Any],
    *,
    parent: dict[str, Any],
    routing_role: dict[str, Any],
    specialist_execution: dict[str, Any],
) -> dict[str, Any]:
    normalized = obligation["normalized_target"]
    members = list(normalized["members"])
    equality_like = normalized["kind"] in {"equality", "equality_chain", "aligned_definition"}
    lhs = members[0] if equality_like and members else ""
    delimiter = r" \coloneqq " if normalized["kind"] == "aligned_definition" else " = "
    rhs = delimiter.join(members[1:]) if equality_like and len(members) > 1 else ""
    rows = obligation["owned_rows"]
    return {
        "id": f"{parent.get('block_id', obligation['document']['file'])}:target:{obligation['label']}",
        "target": normalized["display_text"],
        "lhs": lhs,
        "rhs": rhs,
        "source_text": obligation["source_math"],
        "file": parent.get("file") or obligation["document"]["file"],
        "source_file": obligation["document"]["file"],
        "line_start": rows[0]["line_start"] if rows else obligation["environment"]["line_start"],
        "line_end": rows[-1]["line_end"] if rows else obligation["environment"]["line_end"],
        "label": obligation["label"],
        "parent_label": parent.get("label"),
        "parent_block_id": parent.get("block_id"),
        "section_path": list(parent.get("section_path", [])),
        "environment": obligation["environment"]["kind"],
        "row_index": rows[0]["row_index"] if rows else None,
        "extraction_status": "extracted",
        "localization_status": "label_scoped_valid_complete",
        "uncertainty": (
            ["alignment_markers_preserved"]
            if obligation["environment"]["kind"] in {"align", "alignat", "aligned"}
            else []
        ),
        "adapter_eligible": True,
        "obligation_id": obligation["obligation_id"],
        "obligation_digest": obligation["obligation_digest"],
        "owned_spans": obligation["owned_spans"],
        "excluded_spans": obligation["excluded_spans"],
        "normalized_target": normalized,
        "operator_inventory": obligation["operator_inventory"],
        "symbol_inventory": obligation["symbol_inventory"],
        "label_scoped_obligation": obligation,
        "routing_role": routing_role,
        "specialist_execution": specialist_execution,
    }


def _parent_block(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "file": block.get("file"),
        "line_start": block.get("line_start"),
        "line_end": block.get("line_end"),
        "label": block.get("label"),
        "block_id": block.get("block_id"),
        "section_path": block.get("section_path", []),
    }


def extract_derivation_targets_for_label(
    index: dict[str, Any],
    label: str,
    *,
    file: str | None = None,
    source_digest: str | None = None,
) -> dict[str, Any]:
    """Extract validated label-scoped targets without fallback routing."""
    resolution = _resolve_occurrence(index, label, file)
    if resolution["status"] == "ambiguous":
        return {
            "label": label,
            "status": "ambiguous",
            "selection_status": "ambiguous_label",
            "reason": "The label has multiple source occurrences; exact file identity is required.",
            "parent_block": None,
            "targets": [],
            "obligations": [],
            "fallback_count": 0,
            "ambiguities": [
                {
                    "code": "duplicate_label_across_files",
                    "candidate_files": [str(item.get("file")) for item in resolution["occurrences"]],
                    "required_discriminator": "supply the exact workspace-relative source file",
                }
            ],
        }
    block = resolution.get("occurrence")
    if not isinstance(block, dict):
        return {
            "label": label,
            "status": "label_not_found",
            "selection_status": "label_absent",
            "reason": f"Label `{label}` was not found in the index.",
            "parent_block": None,
            "targets": [],
            "obligations": [],
            "fallback_count": 0,
            "ambiguities": [],
        }

    source_path, source_ref, _ = _workspace_source(index, block)
    observed_source_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    source_binding = {
        "status": "accepted",
        "file": source_ref,
        "source_digest": observed_source_digest,
        "required_source_digest": source_digest,
    }
    if source_digest is not None and source_digest != observed_source_digest:
        source_binding["status"] = "rejected_digest_mismatch"
        return {
            "label": label,
            "status": "source_digest_mismatch",
            "selection_status": "source_digest_mismatch",
            "reason": "The selected source bytes do not match the required source digest.",
            "parent_block": _parent_block(block),
            "targets": [],
            "obligations": [],
            "fallback_count": 0,
            "ambiguities": [],
            "source_binding": source_binding,
        }

    child_labels: list[str]
    if block.get("kind") in {"theorem", "proposition", "lemma", "corollary", "definition", "assumption"}:
        child_labels = []
        for row in index.get("equation_rows", []):
            if (
                row.get("file") == block.get("file")
                and int(block.get("line_start", 0)) <= int(row.get("line_start", -1))
                and int(row.get("line_end", -1)) <= int(block.get("line_end", 0))
            ):
                for child in row.get("explicit_labels", []):
                    if child not in child_labels:
                        child_labels.append(child)
    else:
        child_labels = [label]

    obligations: list[dict[str, Any]] = []
    routing_roles: dict[str, dict[str, Any]] = {}
    specialist_executions: dict[str, dict[str, Any]] = {}
    ambiguities: list[dict[str, Any]] = []
    for child_label in child_labels:
        child_resolution = _resolve_occurrence(index, child_label, str(block.get("file")))
        child_occurrence = child_resolution.get("occurrence")
        if not isinstance(child_occurrence, dict):
            ambiguities.append({"code": "child_label_not_uniquely_resolved", "label": child_label})
            continue
        lookup = _obligation_for_occurrence(index, child_occurrence, child_label)
        obligation = lookup.get("obligation")
        if isinstance(obligation, dict):
            obligations.append(obligation)
            source_path, _, _ = _workspace_source(index, child_occurrence)
            routing_roles[obligation["obligation_digest"]] = infer_source_routing_role(source_path, obligation)
            specialist_executions[obligation["obligation_digest"]] = execute_source_bound_specialist(
                source_path=source_path,
                obligation=obligation,
                routing_role=routing_roles[obligation["obligation_digest"]],
            )
        else:
            ambiguities.extend(lookup.get("ambiguities", []))

    parent = dict(block)
    parent["label"] = label
    targets = [
        _target_from_obligation(
            obligation,
            parent=parent,
            routing_role=routing_roles[obligation["obligation_digest"]],
            specialist_execution=specialist_executions[obligation["obligation_digest"]],
        )
        for obligation in obligations
        if obligation["adapter_eligible"] and obligation["extraction_state"] == "valid_complete"
    ]
    blocked = [obligation for obligation in obligations if not obligation["adapter_eligible"]]
    status = "extracted" if targets and not blocked and not ambiguities else "quarantined" if blocked or ambiguities else "not_extracted"
    return {
        "label": label,
        "status": status,
        "selection_status": "selected",
        "reason": (
            "Extracted validated label-scoped obligations."
            if status == "extracted"
            else "No adapter target was emitted for ambiguous, orphaned, invalid, or incomplete extraction."
        ),
        "parent_block": _parent_block(parent),
        "targets": targets,
        "obligations": obligations,
        "fallback_count": 0,
        "ambiguities": ambiguities + [item for obligation in blocked for item in obligation["ambiguities"]],
        "source_binding": source_binding,
    }


def _label_refs(text: str) -> list[str]:
    refs = re.findall(r"\\(?:cref|Cref|ref|eqref)\{([^}]+)\}", text)
    labels: list[str] = []
    for ref in refs:
        labels.extend(item.strip() for item in ref.split(",") if item.strip())
    return list(dict.fromkeys(labels))


def _proposition_hypotheses(text: str) -> list[str]:
    hypotheses: list[str] = []
    for match in re.finditer(r"\b(?:Suppose|Assume|For|If)\b([^.]*)\.", text, flags=re.IGNORECASE | re.DOTALL):
        item = " ".join(match.group(0).split())
        if item and item not in hypotheses:
            hypotheses.append(item)
    return hypotheses


def build_proposition_context_packet(index: dict[str, Any], label: str) -> dict[str, Any]:
    """Build a source-local context packet for a proposition-like label."""
    block = index.get("labels", {}).get(label) if isinstance(index.get("labels"), dict) else None
    if not isinstance(block, dict):
        return attach_contract(
            {
                "label": label,
                "status": "label_not_found",
                "reason": f"Label `{label}` was not found in the index.",
                "context_packet": None,
                "non_claims": [
                    {
                        "code": "context_packet_not_proof",
                        "text": "Context extraction is source localization only; it does not prove or repair the target.",
                    }
                ],
            },
            PROPOSITION_CONTEXT_PACKET_CONTRACT,
        )
    target_result = extract_derivation_targets_for_label(index, label)
    paragraph_context = extract_paragraph_context_for_label(index, label, before=1, after=1)
    text = str(block.get("text", ""))
    packet = {
        "id": f"proposition_context_packet:{label}",
        "label": label,
        "kind": block.get("kind"),
        "title": block.get("title"),
        "file": block.get("file"),
        "line_start": block.get("line_start"),
        "line_end": block.get("line_end"),
        "block_id": block.get("block_id"),
        "section_path": block.get("section_path", []),
        "source_text": text,
        "paragraph_context": paragraph_context,
        "hypotheses": _proposition_hypotheses(text),
        "referenced_labels": _label_refs(text),
        "equation_targets": target_result.get("targets", []),
        "target_count": target_result.get("target_count", len(target_result.get("targets", []))),
        "fallback_count": target_result.get("fallback_count", 0),
        "uncertainty": [
            item
            for target in target_result.get("targets", [])
            for item in target.get("uncertainty", [])
            if isinstance(target, dict)
        ],
        "evidence_refs": [str(block.get("block_id", label)), "derivation_target_extraction_result"],
        "non_claim": "This proposition context packet localizes source evidence; it is not a proof certificate or repair.",
    }
    status = "context_packet_ready" if packet["equation_targets"] else "context_packet_without_equation_targets"
    return attach_contract(
        {
            "label": label,
            "status": status,
            "reason": "Built proposition context packet with source-local equation targets.",
            "context_packet": packet,
            "non_claims": [
                {
                    "code": "context_packet_not_proof",
                    "text": "Context extraction is source localization only; it does not prove or repair the target.",
                }
            ],
        },
        PROPOSITION_CONTEXT_PACKET_CONTRACT,
    )


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
