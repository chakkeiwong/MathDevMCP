from __future__ import annotations

"""Generic document-to-derivation-tree workflow.

This module bridges LaTeX document targets into the lower-level tree
controller.  It deliberately builds semantic work packets before backend
attempts so agents get assumptions, derivation routes, and blockers rather
than a bare "not encodable" answer.
"""

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from .actionable_abstentions import build_actionable_abstention_payload
from .agent_hypothesis_expansion import propose_hypothesis_expansions
from .assumption_discovery import assumptions_required
from .contracts import attach_contract
from .context_evidence import compact_context_only_packet, render_context_only_packet_markdown
from .derivation_branch_controller import branch_expansion_records, can_derive_with_budget, rank_repair_branches
from .derivation_search_tree import PROMOTION_BOUNDARY, branch_promotion_report
from .derivation_target_extraction import build_proposition_context_packet, extract_derivation_targets_for_label
from .derivation_tree_expansion import expand_tree_with_hypotheses
from .derivation_tree_report import render_derivation_tree_report
from .document_evidence_binding import build_document_evidence_binding
from .doctor import doctor_report
from .equation_locator import DISPLAY_ENVIRONMENTS, locate_equations_in_file, summarize_equation_localization
from .latex_index import build_index, extract_paragraph_context_for_label
from .label_scoped_obligation import FROZEN_CORPUS_VERSION
from .math_ir import typed_repair_obligation_from_packet
from .math_document_rigor import _classify_equation, _label_ref_hygiene, _section_map, _section_path_for_line
from .role_obligations import build_role_specific_obligations, has_role_specific_builder


DOCUMENT_DERIVATION_TREE_CONTRACT = "document_derivation_tree_audit"
DOCUMENT_READY_REPAIR_PROPOSAL_CONTRACT = "context_aware_executable_repair_proposal"
DOCUMENT_GAP_REPORT_CONTRACT = "document_gap_report"
DOCUMENT_PARTIAL_EVIDENCE_REPORT_CONTRACT = "document_partial_evidence_report"
TOOL_GROUNDED_PROPOSAL_COMPILER_CONTRACT = "tool_grounded_proposal_compiler_result"
STRICT_GROUNDING_POLICY = "strict"
DEFAULT_LABEL_LIMIT = 30
PARALLEL_EXECUTION_CONTRACT = "document_derivation_tree_parallel_execution"
DOCUMENT_PUBLICATION_MODE = "disabled"
DOCUMENT_PUBLICATION_ENABLED = False
DOCUMENT_CLAIM_ELIGIBILITY = "ineligible"
DOCUMENT_EVIDENCE_SCHEMA_VERSION = "0-legacy"
DOCUMENT_INTEGRITY_BINDING_STATUS = "unbound_legacy_evidence"
DOCUMENT_PUBLICATION_VETO_ID = "document_repair_publication_quarantined"
LEGACY_BINDING_VETO_ID = "legacy_unbound_document_evidence"
EDIT_TARGET_MISMATCH_VETO_ID = "edit_target_mismatch"
DOCUMENT_TOOL_DISABLED_STATUS = "document_derivation_tree_disabled_pending_publication_safety"
DOCUMENT_TOOL_DISABLE_ENV = "MATHDEVMCP_DISABLE_DOCUMENT_DERIVATION_TREE"
DOCUMENT_DERIVATION_TREE_TOOL_ENABLED = True
BRANCH_EXECUTION_PENDING = "branch_execution_pending"
FORMALIZATION_BLOCKED = "formalization_blocked"


def compile_context_only_report(packet: dict[str, Any]) -> dict[str, Any]:
    """Expose the P03 backend-free report contract to legacy document consumers."""
    return {
        "compact": compact_context_only_packet(packet),
        "markdown": render_context_only_packet_markdown(packet),
    }

_LATEX_COMMANDS_NOT_SYMBOLS = {
    "begin",
    "end",
    "label",
    "left",
    "right",
    "mid",
    "middle",
    "mathrm",
    "text",
    "quad",
    "qquad",
    "nonumber",
    "approx",
    "in",
    "sum",
    "max",
    "min",
    "frac",
    "partial",
}


@contextmanager
def _backend_env_scope(backend_env: str | None):
    old_env = os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV")
    old_toolchain = os.environ.get("MATHDEVMCP_LEAN_TOOLCHAIN")
    if backend_env:
        os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = backend_env
    if backend_env and not os.environ.get("MATHDEVMCP_LEAN_TOOLCHAIN"):
        os.environ["MATHDEVMCP_LEAN_TOOLCHAIN"] = "leanprover/lean4:v4.20.0"
    try:
        yield
    finally:
        if old_env is None:
            os.environ.pop("MATHDEVMCP_BACKEND_CONDA_ENV", None)
        else:
            os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = old_env
        if old_toolchain is None:
            os.environ.pop("MATHDEVMCP_LEAN_TOOLCHAIN", None)
        else:
            os.environ["MATHDEVMCP_LEAN_TOOLCHAIN"] = old_toolchain


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower() or "target"


def _sentence(value: Any) -> str:
    text = " ".join(str(value or "").split())
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else f"{text}."


def _effective_document_promotion(
    raw_promotion: dict[str, Any] | None = None,
    *,
    current_binding: bool = False,
) -> dict[str, Any]:
    raw = raw_promotion if isinstance(raw_promotion, dict) else {}
    if current_binding:
        return {
            "can_promote": False,
            "supported_status": None,
            "reason": "Document promotion is disabled; current evidence identity does not establish claim eligibility.",
            "errors": [DOCUMENT_PUBLICATION_VETO_ID],
            "evidence_refs": [str(ref) for ref in raw.get("evidence_refs", []) if str(ref)],
            "boundary": (
                "Current source, obligation, branch, tool, input, and result binding establishes replayable identity only. "
                "Mathematical closure, scientific validity, edit approval, and publication authority remain separate gates."
            ),
        }
    return {
        "can_promote": False,
        "supported_status": None,
        "reason": "Document promotion is disabled because current backend evidence has no exact Phase 01 binding.",
        "errors": [LEGACY_BINDING_VETO_ID, DOCUMENT_PUBLICATION_VETO_ID],
        "evidence_refs": [str(ref) for ref in raw.get("evidence_refs", []) if str(ref)],
        "boundary": (
            "Raw lower-level evidence is diagnostic history only. Exact source, target, assumptions, "
            "branch, native input, result, tool/version, and edit binding are required before document promotion."
        ),
    }


def _legacy_document_integrity_binding() -> dict[str, Any]:
    """Describe document evidence without granting mathematical authority."""
    return {
        "evidence_schema_version": DOCUMENT_EVIDENCE_SCHEMA_VERSION,
        "integrity_binding_status": DOCUMENT_INTEGRITY_BINDING_STATUS,
        "integrity_binding_verified": False,
        "claim_eligibility": DOCUMENT_CLAIM_ELIGIBILITY,
        "publication_enabled": DOCUMENT_PUBLICATION_ENABLED,
    }


def _current_document_integrity_binding(binding: dict[str, Any]) -> dict[str, Any]:
    """Project a verified binding without duplicating its full evidence payload."""
    return {
        "evidence_schema_version": str(binding.get("schema_version", "1.0")),
        "integrity_binding_status": binding.get("integrity_binding_status"),
        "integrity_binding_verified": binding.get("integrity_binding_verified") is True,
        "claim_eligibility": DOCUMENT_CLAIM_ELIGIBILITY,
        "publication_enabled": DOCUMENT_PUBLICATION_ENABLED,
        "document_evidence_binding_ref": {
            "binding_id": binding.get("binding_id"),
            "binding_digest": binding.get("binding_digest"),
        },
    }


def _integrity_from(value: dict[str, Any]) -> dict[str, Any]:
    binding = value.get("document_evidence_binding")
    if (
        isinstance(binding, dict)
        and isinstance(binding.get("binding_id"), str)
        and isinstance(binding.get("binding_digest"), str)
    ):
        return _current_document_integrity_binding(binding)
    if value.get("evidence_schema_version") == "1.0" and value.get("integrity_binding_verified") is True:
        return {
            key: value[key]
            for key in (
                "evidence_schema_version",
                "integrity_binding_status",
                "integrity_binding_verified",
                "claim_eligibility",
                "publication_enabled",
                "document_evidence_binding_ref",
            )
            if key in value
        }
    return _legacy_document_integrity_binding()


def _document_attempt_view(attempt: dict[str, Any]) -> dict[str, Any]:
    view = dict(attempt)
    view.update(
        {
            **_legacy_document_integrity_binding(),
            "document_evidence_binding": "legacy_unbound",
            "applicable_to_document_branch": False,
            "binding_missing_components": [
                "source_span",
                "target",
                "assumptions",
                "branch",
                "native_input",
                "result",
                "tool_version",
                "edit",
            ],
            "veto_ids": [LEGACY_BINDING_VETO_ID],
        }
    )
    return view


def _document_tool_disabled() -> bool:
    value = os.environ.get(DOCUMENT_TOOL_DISABLE_ENV, "").strip().lower()
    return not DOCUMENT_DERIVATION_TREE_TOOL_ENABLED or value in {"1", "true", "yes", "on"}


def _split_target(text: str) -> tuple[str | None, str | None, str]:
    target = str(text or "").replace("&=", "=").strip().rstrip(",.")
    if "=" not in target:
        return None, None, target
    lhs, rhs = target.split("=", 1)
    return lhs.strip() or None, rhs.strip() or None, f"{lhs.strip()} = {rhs.strip()}"


def _line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _display_pattern() -> re.Pattern[str]:
    envs = "|".join(DISPLAY_ENVIRONMENTS)
    return re.compile(
        rf"\\begin\{{(?P<env>{envs})\*?\}}(?P<body>.*?)\\end\{{(?P=env)\*?\}}",
        re.DOTALL,
    )


def _strip_display_markup(source: str) -> str:
    text = re.sub(r"\\begin\{[^}]+\*?\}", "", source)
    text = re.sub(r"\\end\{[^}]+\*?\}", "", text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\nonumber\b", "", text)
    return text.strip()


def _operator_inventory(text: str) -> list[str]:
    operators: list[str] = []
    checks = [
        ("equality", r"="),
        ("conditional_expectation", r"\\E\b|\\mathbb\{E\}"),
        ("conditional_bar", r"\\mid|\\middle\|"),
        ("summation", r"\\sum(?![A-Za-z])"),
        ("maximum", r"\\max(?![A-Za-z])"),
        ("minimum", r"\\min(?![A-Za-z])"),
        ("derivative", r"\\partial|\\frac\s*\{d|\\frac\s*\{\\partial"),
        ("indicator", r"\\1\{"),
        ("transpose", r"\\top\b"),
        ("integral", r"\\int\b"),
    ]
    for name, pattern in checks:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            operators.append(name)
    return operators


def _symbol_inventory(text: str) -> dict[str, list[str]]:
    macros = sorted(
        {
            f"\\{match.group(1)}"
            for match in re.finditer(r"\\([A-Za-z]+)", text)
            if match.group(1) not in _LATEX_COMMANDS_NOT_SYMBOLS
        }
    )
    identifiers = sorted(
        {
            item
            for item in re.findall(r"(?<!\\)\b[A-Za-z][A-Za-z0-9_]*\b", re.sub(r"\\[A-Za-z]+", " ", text))
            if len(item) <= 40
        }
    )
    return {"macros": macros, "identifiers": identifiers}


def _conditioning_object(text: str) -> str | None:
    patterns = [
        r"\\middle\s*\\?\|\s*([^\]\n]+)",
        r"\\mid(?![A-Za-z])\s*([^\]\n]+)",
        r"(?<!\\)\|\s*([^\]\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = _clean_conditioning_object(match.group(1))
            if value:
                return value
    return None


def _clean_conditioning_object(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"^(?:\\[,;!]|\\quad|\\qquad|\s)+", "", cleaned)
    cleaned = re.sub(r"\\right\s*[\]\)\}\|.]?\s*$", "", cleaned).strip()
    cleaned = cleaned.rstrip(".,;")
    return cleaned.strip()


def _random_terms(text: str) -> list[str]:
    terms: list[str] = []
    stop_terms = {
        "Delta",
        "NPV",
        "E",
        "H",
        "C",
        "TV",
        "CF",
        "For",
        "Under",
        "The",
    }
    for pattern in (
        r"\\Delta\s+[A-Za-z][A-Za-z0-9_]*(?:_\{[^}]+\}|_[A-Za-z0-9]+)?",
        r"\\Delta\s+[A-Za-z][A-Za-z0-9_]*(?:_\{[^}]+\}|_[A-Za-z0-9]+)?\([^)]*\)",
        r"\\Delta\s+[A-Za-z][A-Za-z0-9_]*(?:_\{[^}]+\}|_[A-Za-z0-9]+)?(?:\([^)]*\))?",
        r"[A-Za-z][A-Za-z0-9_]*(?:_\{[^}]+\}|_[A-Za-z0-9]+)?\([^)]*(?:'|t\+h|t\+1)[^)]*\)",
    ):
        for match in re.finditer(pattern, text):
            candidate = " ".join(match.group(0).split())
            candidate = re.sub(r"^\\Delta\s+", r"\\Delta ", candidate)
            if candidate in stop_terms:
                continue
            if candidate and candidate not in terms and len(candidate) <= 80:
                terms.append(candidate)
            if len(terms) >= 6:
                return terms
    return terms


def _snippet(text: Any, limit: int = 220) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _contains_pattern(text: str, patterns: list[str] | tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def _source_ref(
    *,
    file: Any = None,
    line_start: Any = None,
    line_end: Any = None,
    label: Any = None,
    kind: str,
    evidence_ref: Any = None,
    snippet: Any = "",
) -> dict[str, Any]:
    return {
        "file": file,
        "line_start": line_start,
        "line_end": line_end,
        "label": label,
        "kind": kind,
        "evidence_ref": str(evidence_ref or label or kind),
        "snippet": _snippet(snippet),
    }


def _packet_source_ref(packet: dict[str, Any], *, kind: str, snippet: Any = "") -> dict[str, Any]:
    span = packet.get("source_span") if isinstance(packet.get("source_span"), dict) else {}
    return _source_ref(
        file=packet.get("file") or span.get("file"),
        line_start=packet.get("line_start") or span.get("line_start"),
        line_end=packet.get("line_end") or span.get("line_end"),
        label=packet.get("label") or span.get("label"),
        kind=kind,
        evidence_ref=packet.get("block_id") or packet.get("id") or span.get("label"),
        snippet=snippet or packet.get("source_text", ""),
    )


def _target_ref(target: dict[str, Any], *, kind: str) -> dict[str, Any]:
    return _source_ref(
        file=target.get("file"),
        line_start=target.get("line_start"),
        line_end=target.get("line_end"),
        label=target.get("label"),
        kind=kind,
        evidence_ref=target.get("id") or target.get("label"),
        snippet=target.get("source_text") or target.get("target"),
    )


def _packet_paragraphs(packet: dict[str, Any]) -> list[dict[str, Any]]:
    context = packet.get("paragraph_context")
    if not isinstance(context, dict):
        return []
    paragraphs = context.get("paragraphs")
    if not isinstance(paragraphs, list):
        return []
    return [item for item in paragraphs if isinstance(item, dict)]


def _nearby_paragraphs(packet: dict[str, Any]) -> list[dict[str, Any]]:
    source_start = int(packet.get("line_start") or 0)
    source_end = int(packet.get("line_end") or source_start)
    nearby: list[dict[str, Any]] = []
    for paragraph in _packet_paragraphs(packet):
        start = int(paragraph.get("line_start") or 0)
        end = int(paragraph.get("line_end") or start)
        if source_start and end >= source_start and start <= source_end:
            continue
        nearby.append(paragraph)
    return nearby


def _paragraph_refs(packet: dict[str, Any], patterns: list[str] | tuple[str, ...], *, kind: str) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for paragraph in _packet_paragraphs(packet):
        text = str(paragraph.get("text", ""))
        if not _contains_pattern(text, patterns):
            continue
        refs.append(
            _source_ref(
                file=packet.get("file") or packet.get("source_span", {}).get("file") if isinstance(packet.get("source_span"), dict) else packet.get("file"),
                line_start=paragraph.get("line_start"),
                line_end=paragraph.get("line_end"),
                label=packet.get("label") or packet.get("source_span", {}).get("label") if isinstance(packet.get("source_span"), dict) else packet.get("label"),
                kind=kind,
                evidence_ref=f"{packet.get('label') or packet.get('row_id') or packet.get('id')}:paragraph:{paragraph.get('line_start')}",
                snippet=text,
            )
        )
    return refs


def _local_statement_status(
    packet: dict[str, Any],
    *,
    current_text: str,
    context_text: str,
    patterns: list[str] | tuple[str, ...],
    current_ref: dict[str, Any],
) -> tuple[str | None, str, list[dict[str, Any]]]:
    if _contains_pattern(current_text, patterns):
        return "stated", "The condition is stated in the target source span.", [current_ref]
    refs = _paragraph_refs(packet, patterns, kind="context_statement")
    if refs or _contains_pattern(context_text, patterns):
        return "nearby_stated", "The condition is stated in the local paragraph/proposition context.", refs or [current_ref]
    return None, "", []


def _node(
    node_id: str,
    *,
    kind: str,
    status: str,
    summary: str,
    mathematical_role: str,
    why_status: str,
    source_refs: list[dict[str, Any]] | None = None,
    required_next_evidence: str = "",
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    refs = source_refs or []
    return {
        "id": node_id,
        "kind": kind,
        "status": status,
        "summary": summary,
        "mathematical_role": mathematical_role,
        "why_status": why_status,
        "source_refs": refs,
        "required_next_evidence": required_next_evidence,
        "evidence_refs": evidence_refs or [str(ref.get("evidence_ref", "")) for ref in refs if ref.get("evidence_ref")],
    }


def _add_unique_node(nodes: list[dict[str, Any]], node: dict[str, Any]) -> None:
    if any(existing.get("id") == node.get("id") for existing in nodes):
        return
    nodes.append(node)


def _requirement_status(
    *,
    current_text: str,
    nearby_text: str,
    stated_patterns: list[str],
    unresolved_if_patterns: list[str] | None = None,
) -> tuple[str, str]:
    if _contains_pattern(current_text, stated_patterns):
        return "stated", "The condition is stated in the target source span."
    if _contains_pattern(nearby_text, stated_patterns):
        return "nearby_stated", "The condition is stated in nearby local context, not in the target span."
    if unresolved_if_patterns and _contains_pattern(current_text + "\n" + nearby_text, unresolved_if_patterns):
        return "unresolved", "The local source contains related notation or a proof step, but not the required condition itself."
    return "missing", "No matching local source evidence states the required condition."


def _operator_refs(packet: dict[str, Any], patterns: list[str]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for target in packet.get("equation_targets", []):
        if not isinstance(target, dict):
            continue
        text = "\n".join(str(target.get(key, "")) for key in ("source_text", "target", "rhs", "lhs"))
        if _contains_pattern(text, patterns):
            refs.append(_target_ref(target, kind="operator_occurrence"))
    if refs:
        return refs
    text = "\n".join(
        str(packet.get(key, ""))
        for key in ("source_text", "full_display_source", "grouped_target", "target")
    )
    if _contains_pattern(text, patterns):
        refs.append(_packet_source_ref(packet, kind="operator_occurrence", snippet=text))
    return refs


def _dedupe_source_refs(refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in refs:
        key = json.dumps(ref, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ref)
    return deduped


def _definition_nodes(packet: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for paragraph in _nearby_paragraphs(packet):
        text = str(paragraph.get("text", ""))
        ref = _source_ref(
            file=packet.get("file"),
            line_start=paragraph.get("line_start"),
            line_end=paragraph.get("line_end"),
            label=packet.get("label"),
            kind="nearby_context",
            evidence_ref=f"{packet.get('label', 'target')}:paragraph:{paragraph.get('line_start')}",
            snippet=text,
        )
        if _contains_pattern(text, (r"\bdefine\b.*\\bar e", r"\\bar e\s*=")):
            nodes.append(
                _node(
                    "definition_bar_e_current_cash_flow",
                    kind="definition",
                    status="nearby_stated",
                    summary="The nearby text defines the interior current-cash-flow object `\\bar e`.",
                    mathematical_role="definition of the cash-flow term used in the FOC rows",
                    why_status="The definition appears in the local paragraph preceding the proposition.",
                    source_refs=[ref],
                    required_next_evidence="Carry this definition into typed FOC obligations.",
                )
            )
        if _contains_pattern(text, (r"m\(e\)\s*=", r"m\(e\).*marginal value")):
            nodes.append(
                _node(
                    "definition_marginal_cash_value_m",
                    kind="definition",
                    status="nearby_stated",
                    summary="The nearby text defines `m(e)` as the marginal value of current cash flow.",
                    mathematical_role="definition of the multiplier in the FOC rows",
                    why_status="The definition appears in the local paragraph preceding the proposition.",
                    source_refs=[ref],
                    required_next_evidence="Carry this definition into typed FOC obligations.",
                )
            )
        if _contains_pattern(text, (r"All terms.*evaluated at", r"are evaluated at")):
            nodes.append(
                _node(
                    "notation_evaluation_point",
                    kind="notation_declaration",
                    status="nearby_stated",
                    summary="The nearby text states the evaluation point for the cash-flow derivative terms.",
                    mathematical_role="notation declaration for derivative terms appearing in FOC rows",
                    why_status="The declaration appears immediately before the proposition.",
                    source_refs=[ref],
                    required_next_evidence="Carry the evaluation point into typed obligations to avoid free-symbol drift.",
                )
            )
    return nodes


def build_local_context_graph(packet: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic local context graph for a document target packet."""
    label = str(packet.get("label") or packet.get("row_id") or packet.get("id") or "target")
    source_text = str(packet.get("source_text", ""))
    hypotheses = [str(item) for item in packet.get("hypotheses", []) if str(item).strip()]
    target_texts = [
        str(packet.get(key, ""))
        for key in ("target", "grouped_target", "full_display_source")
        if str(packet.get(key, "")).strip()
    ]
    for target in packet.get("equation_targets", []):
        if isinstance(target, dict):
            target_texts.append(str(target.get("source_text") or target.get("target") or ""))
    nearby_text = "\n".join(str(item.get("text", "")) for item in _nearby_paragraphs(packet))
    paragraph_text = "\n".join(str(item.get("text", "")) for item in _packet_paragraphs(packet))
    current_text = "\n".join([source_text, *hypotheses, *target_texts])
    context_text = "\n".join([paragraph_text, nearby_text])
    all_text = "\n".join([current_text, context_text])
    source_ref = _packet_source_ref(packet, kind="target_source", snippet=source_text or current_text)
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for index, hypothesis in enumerate(hypotheses, start=1):
        _add_unique_node(
            nodes,
            _node(
                f"hypothesis_{index}",
                kind="hypothesis",
                status="stated",
                summary=hypothesis,
                mathematical_role="source-stated hypothesis",
                why_status="The proposition hypothesis sentence states this condition.",
                source_refs=[source_ref],
                required_next_evidence="Translate the hypothesis into the typed obligation rather than re-proposing it as missing.",
            ),
        )

    stated_status, stated_why, stated_refs = _local_statement_status(
        packet,
        current_text=current_text,
        context_text=context_text,
        patterns=(r"continuation state",),
        current_ref=source_ref,
    )
    if stated_status:
        _add_unique_node(
            nodes,
            _node(
                "assumption_continuation_state",
                kind="candidate_assumption",
                status=stated_status,
                summary="The current state is a continuation state.",
                mathematical_role="rules out default/terminal regimes for the local FOC route",
                why_status=stated_why,
                source_refs=stated_refs,
                required_next_evidence="Carry this stated condition into the typed FOC obligation.",
            ),
        )
    stated_status, stated_why, stated_refs = _local_statement_status(
        packet,
        current_text=current_text,
        context_text=context_text,
        patterns=(r"\binterior\b",),
        current_ref=source_ref,
    )
    if stated_status:
        _add_unique_node(
            nodes,
            _node(
                "assumption_interior_action",
                kind="candidate_assumption",
                status=stated_status,
                summary="The optimal action is interior.",
                mathematical_role="permits first-order conditions instead of inequality/KKT boundary conditions",
                why_status=stated_why,
                source_refs=stated_refs,
                required_next_evidence="Carry this stated condition into the typed FOC obligation.",
            ),
        )
    stated_status, stated_why, stated_refs = _local_statement_status(
        packet,
        current_text=current_text,
        context_text=context_text,
        patterns=(r"\bdifferentiable\b", r"differentiat"),
        current_ref=source_ref,
    )
    if stated_status:
        _add_unique_node(
            nodes,
            _node(
                "assumption_relevant_functions_differentiable",
                kind="candidate_assumption",
                status=stated_status,
                summary="The relevant functions are differentiable.",
                mathematical_role="supports local derivative notation in the FOC route",
                why_status=stated_why,
                source_refs=stated_refs,
                required_next_evidence=(
                    "Use this as differentiability evidence, but do not treat it as "
                    "integrability or derivative-expectation interchange evidence."
                ),
            ),
        )

    for definition_node in _definition_nodes(packet):
        _add_unique_node(nodes, definition_node)

    for target in packet.get("equation_targets", []):
        if not isinstance(target, dict):
            continue
        label_ref = str(target.get("label") or target.get("id") or "equation")
        _add_unique_node(
            nodes,
            _node(
                f"referenced_equation_{_slug(label_ref)}",
                kind="referenced_equation",
                status="stated",
                summary=f"Equation target `{label_ref}` is localized in the proposition.",
                mathematical_role="display equation target for the local derivation graph",
                why_status="The proposition context packet links this equation row to the proposition.",
                source_refs=[_target_ref(target, kind="equation_target")],
                required_next_evidence="Convert this row into a typed repair obligation in the next phase.",
            ),
        )

    operators = _operator_inventory(all_text)
    for operator in operators:
        patterns = {
            "conditional_expectation": [r"\\E\b", r"\\mathbb\{E\}"],
            "derivative": [r"\\partial", r"\\frac\s*\{d", r"V\^\\star_[kb]"],
            "equality": [r"="],
            "summation": [r"\\sum"],
            "maximum": [r"\\max"],
            "minimum": [r"\\min"],
            "transpose": [r"\\top"],
            "integral": [r"\\int"],
            "indicator": [r"\\1\{"],
            "conditional_bar": [r"\\mid", r"\\middle\|"],
        }.get(operator, [re.escape(operator)])
        refs = _operator_refs(packet, patterns) or [source_ref]
        _add_unique_node(
            nodes,
            _node(
                f"operator_{_slug(operator)}",
                kind="operator",
                status="inferred_candidate",
                summary=f"Operator `{operator}` appears in the local target text.",
                mathematical_role="operator that induces route-required assumptions",
                why_status="The operator is detected syntactically from source-local LaTeX.",
                source_refs=refs,
                required_next_evidence="Typed IR should decide whether this operator can be encoded for a backend.",
            ),
        )

    symbols = _symbol_inventory(all_text)
    if symbols.get("macros") or symbols.get("identifiers"):
        _add_unique_node(
            nodes,
            _node(
                "symbol_inventory",
                kind="symbol_inventory",
                status="inferred_candidate",
                summary=(
                    f"Macros: {symbols.get('macros', [])[:12]}; "
                    f"identifiers: {symbols.get('identifiers', [])[:12]}."
                ),
                mathematical_role="source-local symbol inventory for typed obligation construction",
                why_status="Symbols are extracted syntactically and still need type/domain assignment.",
                source_refs=[source_ref],
                required_next_evidence="Assign scalar/vector/function/random-variable roles in typed IR.",
            ),
        )

    expectation_refs = _operator_refs(packet, [r"\\E\b", r"\\mathbb\{E\}", r"\\mid"])
    derivative_refs = _operator_refs(packet, [r"\\partial", r"\\frac\s*\{d", r"V\^\\star_[kb]", r"d\\bar e"])
    if expectation_refs:
        status, why = _requirement_status(
            current_text=current_text,
            nearby_text=context_text,
            stated_patterns=[
                r"conditional (?:probability )?law",
                r"conditional distribution",
                r"transition (?:law|kernel|probabilit)",
                r"kernel\s+Q",
                r"Q\(d?z'",
                r"P\(z'\s*\\mid\s*z\)",
            ],
            unresolved_if_patterns=[r"\\mid\s*z", r"z'"],
        )
        _add_unique_node(
            nodes,
            _node(
                "requirement_conditional_law_defined",
                kind="candidate_assumption",
                status=status,
                summary="A conditional law for the expectation is defined.",
                mathematical_role="well-definedness condition for conditional expectation",
                why_status=why,
                source_refs=expectation_refs,
                required_next_evidence="Cite or add the transition kernel/probability law used by the conditional expectation.",
            ),
        )
        status, why = _requirement_status(
            current_text=current_text,
            nearby_text=context_text,
            stated_patterns=[r"\bintegrab", r"finite (?:conditional )?(?:first )?moment", r"finite support", r"\bbounded\b", r"dominated"],
            unresolved_if_patterns=[r"\\E\b", r"\\mathbb\{E\}", r"value derivative", r"payoff"],
        )
        _add_unique_node(
            nodes,
            _node(
                "requirement_conditional_integrability",
                kind="candidate_assumption",
                status=status,
                summary="Random terms inside the conditional expectation are measurable and integrable.",
                mathematical_role="finite-scalar condition for expectation-valued equations",
                why_status=why,
                source_refs=expectation_refs,
                required_next_evidence="Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.",
            ),
        )
    if expectation_refs and derivative_refs:
        status, why = _requirement_status(
            current_text=current_text,
            nearby_text=context_text,
            stated_patterns=[r"differentiat(?:e|ion).*under.*expectation", r"interchange.*(?:derivative|differentiation).*expectation"],
            unresolved_if_patterns=[r"expected derivative", r"derivative of the continuation term", r"\bdifferentiable\b"],
        )
        _add_unique_node(
            nodes,
            _node(
                "requirement_expectation_derivative_interchange",
                kind="candidate_assumption",
                status=status,
                summary="Differentiation may pass through the conditional expectation.",
                mathematical_role="justifies replacing the derivative of expected continuation value with expected value derivatives",
                why_status=why,
                source_refs=_dedupe_source_refs([*expectation_refs, *derivative_refs]),
                required_next_evidence=(
                    "State a finite-state sum route or a dominated/Leibniz interchange "
                    "condition for the continuation-value derivatives."
                ),
            ),
        )
        status, why = _requirement_status(
            current_text=current_text,
            nearby_text=context_text,
            stated_patterns=[
                r"transition (?:law|kernel).*independent",
                r"law of z'.*independent",
                r"does not depend on\s*\(?k'",
                r"does not depend on\s*\(?b'",
            ],
            unresolved_if_patterns=[r"\\mid\s*z", r"z'"],
        )
        _add_unique_node(
            nodes,
            _node(
                "requirement_choice_independent_transition_law",
                kind="candidate_assumption",
                status=status,
                summary="The conditional law does not add choice-derivative terms.",
                mathematical_role="rules out omitted transition-kernel derivative terms in the FOC",
                why_status=why,
                source_refs=expectation_refs,
                required_next_evidence=(
                    "State that the conditional law of `z'` given `z` is independent "
                    "of `k'` and `b'`, or include the missing kernel derivative terms."
                ),
            ),
        )

    for assumption in packet.get("route_required_assumptions", []):
        if not isinstance(assumption, dict):
            continue
        text = str(assumption.get("text", "")).strip()
        if not text:
            continue
        node_id = f"route_assumption_{_slug(text)}"
        if any(existing.get("id") == node_id for existing in nodes):
            continue
        status = "stated" if assumption.get("status") == "provided" else "missing"
        why_status = (
            "The low-level route detector marked this assumption as provided."
            if status == "stated"
            else "The low-level route detector marked this assumption as missing."
        )
        refs = [source_ref]
        if "differentiable" in text.lower():
            detected_status, detected_why, detected_refs = _local_statement_status(
                packet,
                current_text=current_text,
                context_text=context_text,
                patterns=(r"\bdifferentiable\b", r"differentiat"),
                current_ref=source_ref,
            )
            if detected_status:
                status = detected_status
                why_status = detected_why + " This reconciles the low-level route requirement with local source evidence."
                refs = detected_refs
        elif "interior" in text.lower():
            detected_status, detected_why, detected_refs = _local_statement_status(
                packet,
                current_text=current_text,
                context_text=context_text,
                patterns=(r"\binterior\b",),
                current_ref=source_ref,
            )
            if detected_status:
                status = detected_status
                why_status = detected_why + " This reconciles the low-level route requirement with local source evidence."
                refs = detected_refs
        _add_unique_node(
            nodes,
            _node(
                node_id,
                kind="candidate_assumption",
                status=status,
                summary=text,
                mathematical_role="route-required assumption from assumption_discovery",
                why_status=why_status,
                source_refs=refs,
                required_next_evidence="Resolve this assumption in typed IR before backend proof attempts.",
                evidence_refs=[str(item) for item in assumption.get("route_category_sources", [])],
            ),
        )

    for node in nodes:
        if node.get("kind") == "operator":
            for requirement in nodes:
                if requirement.get("kind") == "candidate_assumption" and requirement.get("id", "").startswith("requirement_"):
                    edges.append(
                        {
                            "source": node["id"],
                            "target": requirement["id"],
                            "relation": "operator_requires_condition",
                        }
                    )

    status_counts: dict[str, int] = {}
    for node in nodes:
        status_counts[str(node.get("status", "unknown"))] = status_counts.get(str(node.get("status", "unknown")), 0) + 1
    return {
        "id": f"context_graph_{_slug(label)}",
        "target_label": label,
        "status": "context_graph_ready" if nodes else "context_graph_empty",
        "source_scope": {
            "file": packet.get("file") or packet.get("source_span", {}).get("file") if isinstance(packet.get("source_span"), dict) else packet.get("file"),
            "line_start": packet.get("line_start") or (packet.get("source_span", {}) or {}).get("line_start") if isinstance(packet.get("source_span"), dict) else packet.get("line_start"),
            "line_end": packet.get("line_end") or (packet.get("source_span", {}) or {}).get("line_end") if isinstance(packet.get("source_span"), dict) else packet.get("line_end"),
            "label": label,
            "nearby_paragraph_count": len(_nearby_paragraphs(packet)),
        },
        "status_counts": status_counts,
        "nodes": nodes,
        "edges": edges,
        "non_claim": "The context graph is deterministic source-evidence accounting; it is not a proof certificate or sufficiency proof.",
    }


def _external_tool_ledger(plan: dict[str, Any]) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    considered = plan.get("considered_tools", [])
    if not isinstance(considered, list):
        return ledger
    for item in considered:
        if not isinstance(item, dict):
            continue
        ledger.append(
            {
                "tool": item.get("tool"),
                "role": item.get("role"),
                "status": item.get("status"),
                "version": item.get("version"),
                "version_status": item.get("version_status"),
                "environment_scope": item.get("environment_scope"),
                "selected_route": item in plan.get("selected_external_tools", []),
                "why_not_used_now": (
                    "Selected for controller/backend attempt."
                    if item in plan.get("selected_external_tools", [])
                    else item.get("reason")
                ),
                "certification_boundary": item.get("certification_boundary"),
            }
        )
    return ledger


def _unsupported_for_symbolic(packet: dict[str, Any]) -> list[str]:
    unsupported: list[str] = []
    operators = set(packet.get("operator_inventory", []))
    if "conditional_expectation" in operators:
        unsupported.append("conditional expectation requires a probability kernel/integrability formalization")
    if "maximum" in operators or "minimum" in operators:
        unsupported.append("optimization operator requires feasible-set and attainment formalization")
    if "derivative" in operators:
        unsupported.append("derivative/interchange step requires differentiability and domain formalization")
    symbol_inventory = packet.get("symbol_inventory", {})
    if symbol_inventory.get("macros") or symbol_inventory.get("latex_commands"):
        unsupported.append("LaTeX macros require translation to backend symbols")
    return list(dict.fromkeys(unsupported))


def _formalization_stubs(packet: dict[str, Any], branch: dict[str, Any]) -> list[dict[str, Any]]:
    target = str(packet.get("grouped_target") or packet.get("target") or "")
    assumptions = branch.get("assumptions", [])
    unsupported = _unsupported_for_symbolic(packet)
    base = {
        "target": target,
        "encoded_assumptions": assumptions,
        "source_span": packet.get("display_source_span") or packet.get("source_span", {}),
        "evidence_refs": [packet["id"], branch["id"]],
        "certification_boundary": "Formalization stubs are next-check artifacts only; they do not certify the target.",
    }
    stubs = [
        {
            **base,
            "id": f"formalization_{branch['id']}_sympy",
            "backend": "sympy",
            "status": "requires_manual_translation" if unsupported else "candidate_stub",
            "stub": "# Translate the LaTeX equality into SymPy expressions lhs, rhs, then check simplify(lhs - rhs) == 0 under the encoded assumptions.",
            "unsupported_constructs": unsupported,
        },
        {
            **base,
            "id": f"formalization_{branch['id']}_sage",
            "backend": "sage",
            "status": "requires_manual_translation" if unsupported else "candidate_stub",
            "stub": "# Translate the LaTeX equality into Sage symbolic expressions lhs, rhs, then check bool((lhs - rhs).simplify_full() == 0) under the encoded assumptions.",
            "unsupported_constructs": unsupported,
        },
        {
            **base,
            "id": f"formalization_{branch['id']}_lean",
            "backend": "lean",
            "status": "skeleton_contains_sorry_not_certifying",
            "stub": (
                "theorem document_obligation_under_assumptions : True := by\n"
                "  -- Replace True with the translated source equality and encode the branch assumptions.\n"
                "  trivial"
            ),
            "unsupported_constructs": unsupported + ["Lean theorem statement for the LaTeX equality has not been generated"],
        },
    ]
    return stubs


def _formalization_blockers(branch: dict[str, Any]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for stub in branch.get("formalization_stubs", []):
        if not isinstance(stub, dict):
            continue
        unsupported = stub.get("unsupported_constructs", [])
        if not unsupported:
            continue
        blockers.append(
            {
                "id": f"blocker_{stub.get('id', 'formalization_stub')}",
                "kind": "formalization_required",
                "problem": f"{stub.get('backend', 'backend')} stub is not yet a certifying formalization.",
                "why": "; ".join(str(item) for item in unsupported),
                "required_next_evidence": "Translate the source-local equality and branch assumptions into the backend language, then run the backend check.",
                "source": "document_derivation_tree_formalization_stub",
                "evidence_refs": stub.get("evidence_refs", []),
            }
        )
    return blockers


_CONSTRUCT_BLOCKER_DETAILS: dict[str, tuple[str, str, str]] = {
    "expectation": (
        "conditional_expectation_translation_required",
        "The expectation operator cannot be translated as a scalar algebraic expression yet.",
        "A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.",
    ),
    "conditional": (
        "conditioning_scope_translation_required",
        "The conditional bar has no backend-level conditioning object yet.",
        "The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.",
    ),
    "conditional_law": (
        "conditional_law_translation_required",
        "The conditional law required by the expectation is not stated as an encodable object.",
        "Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.",
    ),
    "integrability": (
        "integrability_translation_required",
        "Integrability of the random payoff/value terms is not established.",
        "Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.",
    ),
    "derivative_expectation_interchange": (
        "derivative_expectation_interchange_required",
        "The derivative-under-expectation step is not justified as an encodable theorem instance.",
        "The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.",
    ),
    "choice_independent_transition_law": (
        "choice_independent_transition_law_required",
        "The transition law has not been shown independent of the differentiated choice variables.",
        "If the law depends on the choice, differentiating the conditional expectation creates omitted kernel-derivative terms.",
    ),
}


def _branch_translation_blockers(packet: dict[str, Any], branch: dict[str, Any]) -> list[dict[str, Any]]:
    typed = packet.get("typed_repair_obligation") if isinstance(packet.get("typed_repair_obligation"), dict) else {}
    encodability = branch.get("typed_encodability") if isinstance(branch.get("typed_encodability"), dict) else {}
    constructs = list(
        dict.fromkeys(
            [
                *[str(item) for item in branch.get("typed_unresolved_constructs", []) if str(item)],
                *[str(item) for item in encodability.get("unsupported_constructs", []) if str(item)],
            ]
        )
    )
    blockers: list[dict[str, Any]] = []
    evidence_refs = [str(packet.get("id", "")), *[str(item) for item in branch.get("typed_obligation_ids", []) if item]]
    for construct in constructs:
        detail = _CONSTRUCT_BLOCKER_DETAILS.get(construct)
        if not detail:
            continue
        kind, problem, why = detail
        blockers.append(
            {
                "id": f"blocker_{branch['id']}_{kind}",
                "kind": kind,
                "problem": problem,
                "why": why,
                "required_next_evidence": "State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.",
                "source": "typed_repair_obligation",
                "evidence_refs": evidence_refs,
            }
        )
    blocked_ids = [str(item) for item in encodability.get("blocked_by_assumption_ids", []) if str(item)]
    if blocked_ids:
        blockers.append(
            {
                "id": f"blocker_{branch['id']}_missing_typed_assumptions",
                "kind": "missing_domain_or_assumption_required",
                "problem": "The branch still has missing or unresolved typed assumptions.",
                "why": f"Typed encodability is blocked by `{blocked_ids}`.",
                "required_next_evidence": "Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.",
                "source": "typed_repair_obligation",
                "evidence_refs": evidence_refs,
            }
        )
    macros = []
    symbol_inventory = packet.get("symbol_inventory")
    if isinstance(symbol_inventory, dict):
        raw_macros = symbol_inventory.get("macros", symbol_inventory.get("latex_commands", []))
        if isinstance(raw_macros, list):
            macros = [str(item) for item in raw_macros if str(item)]
    if macros:
        blockers.append(
            {
                "id": f"blocker_{branch['id']}_latex_macro_translation_required",
                "kind": "macro_translation_required",
                "problem": "LaTeX macros must be translated into backend symbols before execution.",
                "why": f"The source span contains macros `{macros[:12]}` whose mathematical types and backend names are not fixed.",
                "required_next_evidence": "Map each macro used by the target to a typed backend symbol or definition and rerun the translator.",
                "source": "semantic_work_packet_symbol_inventory",
                "evidence_refs": evidence_refs,
            }
        )
    constraints = []
    math_obligation = typed.get("math_obligation") if isinstance(typed.get("math_obligation"), dict) else {}
    for constraint in math_obligation.get("dimension_constraints", []) if isinstance(math_obligation, dict) else []:
        if isinstance(constraint, dict) and constraint.get("status") == "missing_assumption":
            constraints.append(constraint)
    if constraints:
        blockers.append(
            {
                "id": f"blocker_{branch['id']}_missing_domain_constraints",
                "kind": "missing_domain_or_shape_required",
                "problem": "The backend translation lacks required domain, dimension, or conformability constraints.",
                "why": "; ".join(str(item.get("reason", "")) for item in constraints),
                "required_next_evidence": "Declare the missing domain/shape constraints or split the obligation before backend execution.",
                "source": "typed_repair_obligation_dimension_constraints",
                "evidence_refs": evidence_refs,
            }
        )
    return blockers


def _attempt_matches_backend(attempt: dict[str, Any], backend: str) -> bool:
    tool = str(attempt.get("tool", ""))
    if backend == "sympy":
        return tool.startswith("sympy") or tool == "bounded_counterexample"
    if backend == "sage":
        return tool == "sage"
    if backend == "lean":
        return tool == "lean"
    return tool == backend


def _branch_backend_attempts(
    branch: dict[str, Any],
    root: dict[str, Any],
) -> list[dict[str, Any]]:
    _ = root
    branch_id = str(branch.get("id", ""))
    return [
        _document_attempt_view(item)
        for item in branch.get("backend_attempts", [])
        if isinstance(item, dict)
        and item.get("branch_id") == branch_id
        and item.get("request_ref")
        and item.get("result_ref")
    ]


def _branch_execution_blocker(packet: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"blocker_{branch['id']}_branch_bound_execution_required",
        "kind": "branch_bound_backend_execution_required",
        "problem": "This assumption branch has no branch-bound backend request/result evidence.",
        "why": (
            "Root attempts bind only the original root target. They do not bind this branch's "
            "assumptions, formalization request, or result and therefore cannot close the branch."
        ),
        "required_next_evidence": (
            "Create and execute an exact branch request that binds the target, typed assumptions, "
            "branch id, native input, tool/version, and result."
        ),
        "source": "document_derivation_tree_phase04_branch_boundary",
        "evidence_refs": [str(packet.get("id", "")), str(branch.get("id", ""))],
    }


def _branch_translation_attempts(
    packet: dict[str, Any],
    branch: dict[str, Any],
    backend_attempts: list[dict[str, Any]],
    translation_blockers: list[dict[str, Any]],
    formalization_blockers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    encodability = branch.get("typed_encodability") if isinstance(branch.get("typed_encodability"), dict) else {}
    blocker_ids = [str(item.get("id", "")) for item in translation_blockers if isinstance(item, dict) and item.get("id")]
    lean_formalization_ids = [
        str(item.get("id", ""))
        for item in formalization_blockers
        if isinstance(item, dict) and item.get("id") and "lean" in str(item.get("id", "")).lower()
    ]
    target = str(packet.get("grouped_target") or packet.get("target") or "")
    candidate_backends = [str(item) for item in encodability.get("candidate_backends", []) if str(item)]
    attempts: list[dict[str, Any]] = []
    for backend in ("sympy", "sage", "lean"):
        matching = [attempt for attempt in backend_attempts if _attempt_matches_backend(attempt, backend)]
        if matching:
            status = "executed"
            reason = f"{backend} has bounded attempt evidence attached to this branch."
            backend_attempt_ids = [str(item.get("id", "")) for item in matching if item.get("id")]
        elif blocker_ids:
            status = "blocked_before_execution"
            reason = f"{backend} translation is blocked by typed/source translation blockers."
            backend_attempt_ids = []
        elif backend == "lean":
            status = "requires_formalization"
            reason = "Lean requires explicit Lean source before direct checking can certify this branch."
            backend_attempt_ids = []
        elif backend in candidate_backends or not candidate_backends:
            status = "not_attempted_in_current_budget"
            reason = f"{backend} was not attempted in the current bounded branch-controller budget."
            backend_attempt_ids = []
        else:
            status = "not_selected_by_typed_route"
            reason = f"{backend} was not selected by the typed route hints for this branch."
            backend_attempt_ids = []
        attempts.append(
            {
                "id": f"translation_{branch['id']}_{backend}",
                "backend": backend,
                "status": status,
                "input_summary": target,
                "backend_attempt_ids": backend_attempt_ids,
                "blocker_ids": blocker_ids
                if status == "blocked_before_execution"
                else lean_formalization_ids
                if backend == "lean" and status == "requires_formalization"
                else [],
                "expected_next_artifact": (
                    "Scoped backend attempt/certificate for the encoded equality."
                    if status in {"not_attempted_in_current_budget", "requires_formalization"}
                    else "Recorded in backend_attempt_ids or blocker_ids."
                ),
                "reason": reason,
                "certification_boundary": PROMOTION_BOUNDARY,
            }
        )
    return attempts


def _attach_branch_backend_evidence(packet: dict[str, Any], branch: dict[str, Any], root: dict[str, Any]) -> None:
    backend_attempts = _branch_backend_attempts(branch, root)
    translation_blockers = _branch_translation_blockers(packet, branch)
    branch["backend_attempts"] = backend_attempts
    branch["translation_blockers"] = translation_blockers
    formalization_blockers = _formalization_blockers(branch)
    branch["blockers"] = [*translation_blockers, *formalization_blockers]
    if not backend_attempts:
        branch["blockers"].append(_branch_execution_blocker(packet, branch))
    branch["translation_attempts"] = _branch_translation_attempts(
        packet,
        branch,
        backend_attempts,
        translation_blockers,
        formalization_blockers,
    )
    promotion_status = str(branch.get("status", "partial"))
    raw_promotion = branch_promotion_report({"status": promotion_status, "backend_attempts": backend_attempts})
    effective_promotion = _effective_document_promotion(raw_promotion)
    if raw_promotion.get("can_promote") and raw_promotion.get("supported_status") in {"proved", "refuted"}:
        branch["status"] = f"legacy_{raw_promotion['supported_status']}_evidence_unbound"
        branch["validation_status"] = "legacy_unbound_partial_evidence"
    elif translation_blockers:
        branch["status"] = "blocked_before_backend_certification"
        branch["validation_status"] = "typed_translation_blocked"
    elif backend_attempts:
        branch["status"] = "diagnostic_backend_attempt_recorded"
        branch["validation_status"] = "diagnostic_backend_attempt_only"
    else:
        branch["status"] = "unexecuted_branch_pending_bound_request"
        branch["validation_status"] = "branch_execution_not_attempted"
    engineering_error = any(str(item.get("status", "")).endswith("error") for item in backend_attempts)
    if engineering_error:
        failure_classification = "engineering_error"
    elif raw_promotion.get("can_promote"):
        failure_classification = "evidence_binding_error"
    elif not backend_attempts:
        failure_classification = BRANCH_EXECUTION_PENDING
    else:
        failure_classification = "mathematical_blocked"
    branch["backend_evidence"] = {
        **_legacy_document_integrity_binding(),
        "status": branch["validation_status"],
        "binding_status": "legacy_unbound" if backend_attempts else "no_branch_evidence",
        "failure_classification": failure_classification,
        "veto_ids": [LEGACY_BINDING_VETO_ID, DOCUMENT_PUBLICATION_VETO_ID],
        "backend_attempt_count": len(backend_attempts),
        "translation_attempt_count": len(branch["translation_attempts"]),
        "translation_blocker_count": len(translation_blockers),
        "raw_promotion": raw_promotion,
        "effective_document_promotion": effective_promotion,
        "boundary": PROMOTION_BOUNDARY,
    }
    branch["agent_hypothesis_expansions"] = [
        propose_hypothesis_expansions(
            blocker,
            source_context={
                "id": packet.get("id"),
                "label": packet.get("label"),
                "location": packet.get("location"),
            },
            typed_obligation=packet.get("typed_repair_obligation")
            if isinstance(packet.get("typed_repair_obligation"), dict)
            else None,
        )
        for blocker in translation_blockers[:3]
        if isinstance(blocker, dict)
    ]
    branch["expansion_records"] = branch_expansion_records(branch)


def _labels_in_text(text: str) -> list[str]:
    return re.findall(r"\\label\{([^}]+)\}", text)


def _display_index(tex_path: Path, text: str, *, root: Path | None = None) -> list[dict[str, Any]]:
    root = root.resolve() if root is not None else tex_path.parent.resolve()
    try:
        relative_path = str(tex_path.resolve().relative_to(root))
    except ValueError:
        relative_path = str(tex_path)
    displays: list[dict[str, Any]] = []
    for index, match in enumerate(_display_pattern().finditer(text)):
        source = match.group(0)
        body = match.group("body")
        line_start = _line_number_at(text, match.start())
        line_end = _line_number_at(text, match.end())
        target = _strip_display_markup(source)
        displays.append(
            {
                "id": f"{relative_path}:{line_start}:{match.group('env')}:display:{index}",
                "environment": match.group("env"),
                "file": relative_path,
                "line_start": line_start,
                "line_end": line_end,
                "labels": _labels_in_text(source),
                "full_display_source": source.strip(),
                "display_body": body.strip(),
                "grouped_source_target": target,
                "operator_inventory": _operator_inventory(target),
                "symbol_inventory": _symbol_inventory(target),
            }
        )
    return displays


def _display_for_row(row: dict[str, Any], displays: list[dict[str, Any]]) -> dict[str, Any] | None:
    row_file = row.get("file")
    row_start = int(row.get("line_start", 0) or 0)
    row_end = int(row.get("line_end", row_start) or row_start)
    candidates = [
        display
        for display in displays
        if display.get("file") == row_file
        and int(display.get("line_start", 0)) <= row_start
        and int(display.get("line_end", 0)) >= row_end
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda display: int(display.get("line_end", 0)) - int(display.get("line_start", 0)))
    return candidates[0]


def _obligation_ids(packet: dict[str, Any], closes: str) -> list[str]:
    close_text = str(closes or "").lower()
    matched: list[str] = []
    for obligation in packet.get("missing_obligations", []):
        if not isinstance(obligation, dict):
            continue
        haystack = " ".join(
            str(obligation.get(key, ""))
            for key in ("id", "kind", "mathematically_missing", "why_missing", "closes")
        ).lower()
        if close_text and any(word for word in close_text.split() if len(word) > 4 and word in haystack):
            matched.append(str(obligation.get("id", "missing_obligation")))
    if matched:
        return list(dict.fromkeys(matched))
    return [str(item.get("id", "missing_obligation")) for item in packet.get("missing_obligations", []) if isinstance(item, dict)]


def _branch_route(packet: dict[str, Any], assumption_set: dict[str, Any]) -> list[dict[str, Any]]:
    conditioning = _conditioning_object(str(packet.get("grouped_target") or packet.get("target") or ""))
    terms = _random_terms(str(packet.get("grouped_target") or packet.get("target") or ""))
    steps: list[dict[str, Any]] = []
    for index, step in enumerate(packet.get("how_derivation_can_work", []), start=1):
        if not isinstance(step, dict):
            continue
        detail = str(step.get("detail", ""))
        if conditioning and "conditional" in detail.lower():
            detail = f"{detail} In this source span, the conditioning object is `{conditioning}`."
        if terms and any(token in detail.lower() for token in ("payoff", "value", "term", "cash")):
            detail = f"{detail} Candidate source-local random terms include `{', '.join(terms[:4])}`."
        steps.append(
            {
                "id": f"{assumption_set.get('id', 'assumption_branch')}_route_{index}",
                "step": step.get("step", f"route step {index}"),
                "detail": detail,
                "source": "semantic_work_packet",
                "evidence_refs": [packet["id"]],
            }
        )
    return steps


def _assumption_branch(packet: dict[str, Any], assumption_set: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    branch_id = f"branch_{packet['id']}_{_slug(str(assumption_set.get('id', 'assumption_set')))}"
    typed_obligation = packet.get("typed_repair_obligation") if isinstance(packet.get("typed_repair_obligation"), dict) else {}
    closes = _obligation_ids(packet, str(assumption_set.get("closes", "")))
    assumptions = [_sentence(item) for item in assumption_set.get("assumptions", []) if str(item).strip()]
    conditioning = _conditioning_object(str(packet.get("grouped_target") or packet.get("target") or ""))
    if conditioning and "conditional" in str(assumption_set.get("id", "")).lower():
        assumptions.append(f"The conditioning object `{conditioning}` is defined as a sigma-field, information set, state, or conditioning variable for this equality.")
    route = _branch_route(packet, assumption_set)
    why = (
        f"This branch closes `{assumption_set.get('closes', 'the detected obligation')}` "
        "by making the operators and objects in the displayed equality well-defined before backend certification."
    )
    return {
        "id": branch_id,
        "status": "proposed_sufficient_not_minimal",
        "role": assumption_set.get("role", "candidate sufficient condition"),
        "assumptions": list(dict.fromkeys(assumptions)),
        "closes_obligations": closes,
        "mathematical_why": why,
        "typed_obligation_ids": [typed_obligation.get("id")] if typed_obligation.get("id") else [],
        "typed_unresolved_constructs": typed_obligation.get("unresolved_constructs", []),
        "typed_backend_route_hints": typed_obligation.get("route_hints", []),
        "typed_encodability": typed_obligation.get("encodability", {}),
        "derivation_route_under_assumptions": route,
        "external_tool_first_ledger": _external_tool_ledger(plan),
        "validation_status": "diagnostic_pending_backend_or_formalization",
        "evidence_refs": [packet["id"], *[str(item.get("evidence_ref", "")) for item in packet.get("missing_obligations", []) if isinstance(item, dict)]],
        "non_claim": "This branch proposes a sufficient route; it is not a proof certificate and not a globally minimal assumption set.",
    }


def _patch_text_for_branch(packet: dict[str, Any], branch: dict[str, Any]) -> str:
    label = packet.get("label") or packet.get("row_id") or "the displayed equality"
    location = packet.get("location", "the cited source span")
    assumptions = " ".join(_sentence(item) for item in branch.get("assumptions", []))
    route_bits = []
    for step in branch.get("derivation_route_under_assumptions", [])[:3]:
        if isinstance(step, dict):
            route_bits.append(_sentence(f"{step.get('step', 'Step')}: {step.get('detail', '')}"))
    route = " ".join(route_bits)
    return (
        f"Near `{label}` at {location}, add an assumptions paragraph: "
        f'"For this displayed equality, assume: {assumptions} '
        f'Under these assumptions, the derivation route is: {route}"'
    )


def _latex_sentence(value: Any) -> str:
    text = _sentence(value)
    text = re.sub(r"`([^`]+)`", r"\\(\1\\)", text)
    return text


def _latex_itemize(items: list[Any]) -> list[str]:
    lines = ["\\begin{itemize}"]
    for item in items:
        text = _latex_sentence(item)
        if text:
            lines.append(f"  \\item {text}")
    lines.append("\\end{itemize}")
    return lines


def _proposal_latex_for_branch(packet: dict[str, Any], branch: dict[str, Any]) -> str:
    label = str(packet.get("label") or packet.get("row_id") or "target")
    assumptions = [item for item in branch.get("assumptions", []) if str(item).strip()]
    route = [item for item in branch.get("derivation_route_under_assumptions", []) if isinstance(item, dict)]
    lines = [
        f"\\paragraph{{Repair assumptions for \\texttt{{{label}}}.}}",
        "Use the following local assumptions for this displayed equality:",
        *_latex_itemize(assumptions),
        "",
        "Under these assumptions, the derivation should be checked by the following route:",
        "\\begin{enumerate}",
    ]
    for step in route[:6]:
        step_name = str(step.get("step", "Derivation step")).strip() or "Derivation step"
        detail = _latex_sentence(step.get("detail", ""))
        lines.append(f"  \\item \\textbf{{{step_name}.}} {detail}")
    lines.extend(
        [
            "\\end{enumerate}",
            "",
            (
                "This paragraph is blocked candidate text only: do not apply it. Rerun the listed backend "
                "or formalization checks and establish exact evidence binding before treating the display as certified."
            ),
        ]
    )
    return "\n".join(lines)


def _patch_candidate_for_branch(packet: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    source_span = packet.get("display_source_span") if isinstance(packet.get("display_source_span"), dict) and packet.get("display_source_span") else packet.get("source_span", {})
    return {
        "id": f"patch_{branch['id']}",
        "kind": "blocked_candidate_repair",
        "status": "non_applicable_publication_quarantine",
        "applicable": False,
        "location": source_span,
        "candidate_text_blocked": _patch_text_for_branch(packet, branch),
        "blocked_reason": "Document repair publication is disabled and the branch evidence is legacy/unbound.",
        "rationale": branch.get("mathematical_why", ""),
        "validation_status": "blocked_non_applicable",
        "failure_classification": "evidence_binding_error",
        "veto_ids": [LEGACY_BINDING_VETO_ID, DOCUMENT_PUBLICATION_VETO_ID],
        "evidence_refs": branch.get("evidence_refs", []),
    }


def _branch_by_id(branches: list[dict[str, Any]], branch_id: str | None) -> dict[str, Any] | None:
    if not branch_id:
        return None
    for branch in branches:
        if isinstance(branch, dict) and branch.get("id") == branch_id:
            return branch
    return None


def _source_refs_from_assumptions(typed: dict[str, Any], statuses: set[str]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for assumption in typed.get("assumptions", []) if isinstance(typed, dict) else []:
        if not isinstance(assumption, dict) or assumption.get("status") not in statuses:
            continue
        for ref in assumption.get("source_refs", []):
            if isinstance(ref, dict):
                refs.append(ref)
    return _dedupe_source_refs(refs)


def _proposal_problem(packet: dict[str, Any], branch: dict[str, Any], typed: dict[str, Any]) -> str:
    missing = [
        str(item.get("id", "assumption"))
        for item in typed.get("assumptions", [])
        if isinstance(item, dict) and item.get("status") in {"missing", "unresolved"}
    ]
    constructs = [str(item) for item in typed.get("unresolved_constructs", []) if str(item)]
    if missing or constructs:
        return (
            "The target is not yet a certifiable derivation because missing or unresolved "
            f"assumptions {missing[:6]} block constructs {constructs[:6]}."
        )
    if branch.get("backend_evidence", {}).get("raw_promotion", {}).get("can_promote"):
        return "The scoped target has raw backend evidence, but it is legacy/unbound and cannot support a document edit."
    return "The target remains diagnostic because no branch has enough evidence for certification."


def _proposal_why(packet: dict[str, Any], branch: dict[str, Any], typed: dict[str, Any]) -> str:
    why_parts: list[str] = []
    encodability = typed.get("encodability") if isinstance(typed.get("encodability"), dict) else {}
    if encodability.get("why"):
        why_parts.append(str(encodability["why"]))
    if branch.get("mathematical_why"):
        why_parts.append(str(branch["mathematical_why"]))
    blockers = [
        item for item in branch.get("translation_blockers", [])
        if isinstance(item, dict) and item.get("why")
    ]
    for blocker in blockers[:3]:
        why_parts.append(str(blocker["why"]))
    return " ".join(_sentence(item) for item in why_parts if str(item).strip())


def _branch_context_for_report(
    packet: dict[str, Any],
    root: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    branches = [item for item in root.get("assumption_branches", []) if isinstance(item, dict)]
    ranking = root.get("branch_ranking") if isinstance(root.get("branch_ranking"), dict) else {}
    nondominated_ids = [
        str(item)
        for item in ranking.get("nondominated_branch_ids", [])
        if isinstance(item, str) and item
    ]
    context_branch_id = ranking.get("top_branch_id")
    selection_authority = "unique_nondominated"
    if not context_branch_id and nondominated_ids:
        context_branch_id = nondominated_ids[0]
        selection_authority = "serialization_only_nondominated_context"
    context_branch = _branch_by_id(branches, context_branch_id) or (branches[0] if branches else None)
    if context_branch is None:
        return None, {}, {}, [], [], []
    typed = packet.get("typed_repair_obligation") if isinstance(packet.get("typed_repair_obligation"), dict) else {}
    context_ranking = None
    for item in ranking.get("rankings", []) if isinstance(ranking.get("rankings"), list) else []:
        if isinstance(item, dict) and item.get("branch_id") == context_branch.get("id"):
            context_ranking = dict(item)
            break
    context_ranking = context_ranking or {}
    context_ranking.update(
        {
            "context_selection_authority": selection_authority,
            "nondominated_branch_ids": nondominated_ids,
            "selected_action_id": (
                ranking.get("selected_action", {}).get("action_id")
                if isinstance(ranking.get("selected_action"), dict)
                else None
            ),
        }
    )
    missing_or_unresolved = [
        {
            "id": item.get("id"),
            "status": item.get("status"),
            "text": item.get("text"),
            "role": item.get("role"),
            "evidence_refs": item.get("evidence_refs", []),
        }
        for item in typed.get("assumptions", []) if isinstance(item, dict) and item.get("status") in {"missing", "unresolved"}
    ]
    already_stated = [
        {
            "id": item.get("id"),
            "status": item.get("status"),
            "text": item.get("text"),
            "role": item.get("role"),
            "evidence_refs": item.get("evidence_refs", []),
        }
        for item in typed.get("assumptions", []) if isinstance(item, dict) and item.get("status") in {"stated", "nearby_stated"}
    ]
    remaining_blockers: list[dict[str, Any]] = []
    seen_blocker_ids: set[str] = set()
    for blocker in [
        *[item for item in context_branch.get("translation_blockers", []) if isinstance(item, dict)],
        *[item for item in context_branch.get("blockers", []) if isinstance(item, dict)],
    ]:
        blocker_id = str(blocker.get("id", ""))
        if blocker_id and blocker_id in seen_blocker_ids:
            continue
        if blocker_id:
            seen_blocker_ids.add(blocker_id)
        remaining_blockers.append(
            {
                "id": blocker.get("id"),
                "kind": blocker.get("kind"),
                "problem": blocker.get("problem"),
                "why": blocker.get("why"),
                "required_next_evidence": blocker.get("required_next_evidence"),
                "evidence_refs": blocker.get("evidence_refs", []),
            }
        )
    return context_branch, typed, context_ranking, missing_or_unresolved, already_stated, remaining_blockers


def _quarantine_branch_ranking(ranking: dict[str, Any], branches: list[dict[str, Any]]) -> dict[str, Any]:
    branch_by_id = {str(branch.get("id")): branch for branch in branches if branch.get("id")}
    current_binding = bool(branches) and all(
        branch.get("integrity_binding_verified") is True for branch in branches
    )
    quarantined = dict(ranking)
    quarantined_rankings: list[dict[str, Any]] = []
    for item in ranking.get("rankings", []) if isinstance(ranking.get("rankings"), list) else []:
        if not isinstance(item, dict):
            continue
        entry = dict(item)
        branch = branch_by_id.get(str(entry.get("branch_id")), {})
        evidence = branch.get("backend_evidence") if isinstance(branch.get("backend_evidence"), dict) else {}
        raw = evidence.get("raw_promotion") if isinstance(evidence.get("raw_promotion"), dict) else {}
        entry_current_binding = evidence.get("integrity_binding_verified") is True
        entry["promotion"] = _effective_document_promotion(raw, current_binding=entry_current_binding)
        if raw.get("can_promote"):
            if entry_current_binding:
                entry["outcome"] = "identity_bound_claim_ineligible"
                entry["explanation"] = (
                    "Raw lower-level backend evidence affected diagnostic ordering and has replayable identity, "
                    "but identity binding does not establish claim or publication authority; the effective "
                    "promotion decision is false."
                )
            else:
                entry["outcome"] = "legacy_evidence_unbound"
                entry["explanation"] = (
                    "Raw lower-level backend evidence affected diagnostic ordering, but exact document binding "
                    "is absent; the effective promotion decision is false."
                )
        quarantined_rankings.append(entry)
    quarantined["rankings"] = quarantined_rankings
    quarantined["publication_mode"] = DOCUMENT_PUBLICATION_MODE
    binding_boundary = (
        "Current evidence has replayable identity, but document-level promotion remains quarantined because "
        "identity binding does not establish mathematical closure, claim eligibility, edit approval, or "
        "publication authority."
        if current_binding
        else "Document-level promotion is quarantined until exact binding exists."
    )
    quarantined["boundary"] = f"{ranking.get('boundary', '')} {binding_boundary}".strip()
    return quarantined


def _branch_closure_status(branch: dict[str, Any], remaining_blockers: list[dict[str, Any]]) -> str:
    promotion = branch.get("backend_evidence", {}).get("raw_promotion", {})
    if isinstance(promotion, dict) and promotion.get("can_promote"):
        supported = str(promotion.get("supported_status") or "backend")
        if supported == "refuted":
            return "legacy_refutation_evidence_unbound"
        if remaining_blockers:
            return "legacy_backend_evidence_with_open_requirements"
        return "legacy_backend_evidence_unbound"
    backend_attempts = [item for item in branch.get("backend_attempts", []) if isinstance(item, dict)]
    certifying_attempts = [
        item
        for item in backend_attempts
        if item.get("certification_status") in {"certified", "certifying", "verified", "proved"}
        or item.get("evidence_kind") in {"certifying_backend", "lean_check", "symbolic_identity", "sage_check"}
    ]
    if certifying_attempts and remaining_blockers:
        return "legacy_backend_evidence_with_open_requirements"
    if remaining_blockers:
        return "blocked_at_exact_node"
    return "source_assumption_gap_only"


def _document_backend_evidence_view(branch: dict[str, Any]) -> dict[str, Any]:
    evidence = branch.get("backend_evidence") if isinstance(branch.get("backend_evidence"), dict) else {}
    raw = evidence.get("raw_promotion") if isinstance(evidence.get("raw_promotion"), dict) else {}
    return {
        **_integrity_from(evidence),
        "status": evidence.get("status"),
        "binding_status": evidence.get("binding_status", "no_branch_evidence"),
        "failure_classification": evidence.get("failure_classification"),
        "veto_ids": list(evidence.get("veto_ids", [])),
        "backend_attempt_count": evidence.get("backend_attempt_count", 0),
        "translation_attempt_count": evidence.get("translation_attempt_count", 0),
        "translation_blocker_count": evidence.get("translation_blocker_count", 0),
        "promotion": _effective_document_promotion(
            raw,
            current_binding=evidence.get("integrity_binding_verified") is True,
        ),
        "raw_evidence_refs": [str(ref) for ref in raw.get("evidence_refs", []) if str(ref)],
        "boundary": evidence.get("boundary", PROMOTION_BOUNDARY),
    }


def _document_failure_classifications(
    branch: dict[str, Any],
    remaining_blockers: list[dict[str, Any]],
    missing_or_unresolved: list[dict[str, Any]],
) -> list[str]:
    attempts = [item for item in branch.get("backend_attempts", []) if isinstance(item, dict)]
    raw = branch.get("backend_evidence", {}).get("raw_promotion", {})
    classifications: list[str] = []
    if any(str(item.get("status", "")).endswith("error") for item in attempts):
        classifications.append("engineering_error")
    if isinstance(raw, dict) and raw.get("can_promote"):
        classifications.append("evidence_binding_error")
    execution_pending = any(
        str(item.get("kind", "")) == "branch_bound_backend_execution_required"
        for item in remaining_blockers
    )
    formalization_blockers = [
        item
        for item in remaining_blockers
        if str(item.get("kind", ""))
        in {
            "formalization_required",
            "macro_translation_required",
            "conditional_expectation_translation_required",
            "conditioning_scope_translation_required",
            "conditional_law_translation_required",
            "integrability_translation_required",
            "derivative_expectation_interchange_required",
            "choice_independent_transition_law_required",
        }
    ]
    mathematical_blockers = [
        item
        for item in remaining_blockers
        if str(item.get("kind", ""))
        not in {
            "adapter_error",
            "target_worker_exception",
            "parallel_worker_exception",
            "evidence_binding_required",
            "branch_bound_backend_execution_required",
            *{
                str(blocker.get("kind", ""))
                for blocker in formalization_blockers
            },
        }
    ]
    if mathematical_blockers or missing_or_unresolved:
        classifications.append("mathematical_blocked")
    if execution_pending:
        classifications.append(BRANCH_EXECUTION_PENDING)
    if formalization_blockers:
        classifications.append(FORMALIZATION_BLOCKED)
    if not classifications:
        classifications.append(BRANCH_EXECUTION_PENDING)
    return classifications


def _binding_blocker(branch: dict[str, Any]) -> dict[str, Any]:
    raw = branch.get("backend_evidence", {}).get("raw_promotion", {})
    return {
        "id": f"blocker_{branch.get('id', 'branch')}_{LEGACY_BINDING_VETO_ID}",
        "kind": "evidence_binding_required",
        "problem": "The backend attempt is copied legacy evidence and is not exactly bound to this document branch or edit.",
        "why": "A matching attempt id or successful calculation does not bind source span, target, assumptions, branch, native input, result, tool version, and candidate edit.",
        "required_next_evidence": "Create and verify the Phase 01 content-addressed evidence manifest before reconsidering document promotion.",
        "evidence_refs": [str(ref) for ref in raw.get("evidence_refs", []) if str(ref)],
    }


def _common_document_repair_payload(
    packet: dict[str, Any],
    branch: dict[str, Any],
    typed: dict[str, Any],
    ranking: dict[str, Any],
    missing_or_unresolved: list[dict[str, Any]],
    already_stated: list[dict[str, Any]],
    remaining_blockers: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        **_integrity_from(branch),
        "target_label": packet.get("label"),
        "location": packet.get("location"),
        "source_span": packet.get("display_source_span") or packet.get("source_span", {}),
        "context_branch_id": branch.get("id"),
        "context_branch_selection_authority": ranking.get("context_selection_authority"),
        "nondominated_branch_ids": ranking.get("nondominated_branch_ids", []),
        "selected_action_id": ranking.get("selected_action_id"),
        "ranking": ranking,
        "problem": _proposal_problem(packet, branch, typed),
        "why": _proposal_why(packet, branch, typed),
        "already_stated_assumptions": already_stated,
        "missing_or_unresolved_assumptions": missing_or_unresolved,
        "proposed_assumptions": branch.get("assumptions", []),
        "derivation_route_under_assumptions": branch.get("derivation_route_under_assumptions", []),
        "backend_evidence": _document_backend_evidence_view(branch),
        "translation_attempts": branch.get("translation_attempts", []),
        "remaining_blockers_before_certification": remaining_blockers,
        "required_next_evidence": list(
            dict.fromkeys(
                str(blocker.get("required_next_evidence", ""))
                for blocker in remaining_blockers
                if isinstance(blocker, dict) and blocker.get("required_next_evidence")
            )
        ),
        "evidence_refs": list(
            dict.fromkeys(
                [
                    str(packet.get("id", "")),
                    str(branch.get("id", "")),
                    *[str(ref) for ref in branch.get("evidence_refs", [])],
                ]
            )
        ),
        "source_refs_for_missing_or_unresolved": _source_refs_from_assumptions(typed, {"missing", "unresolved"}),
        "source_refs_for_already_stated": _source_refs_from_assumptions(typed, {"stated", "nearby_stated"}),
    }


def _document_ready_repair_proposals(packet: dict[str, Any], root: dict[str, Any]) -> list[dict[str, Any]]:
    _ = packet, root
    return []


def _document_partial_evidence_reports(packet: dict[str, Any], root: dict[str, Any]) -> list[dict[str, Any]]:
    context_branch, typed, context_ranking, missing_or_unresolved, already_stated, remaining_blockers = _branch_context_for_report(packet, root)
    if context_branch is None:
        return []
    raw = context_branch.get("backend_evidence", {}).get("raw_promotion", {})
    if not isinstance(raw, dict) or not raw.get("can_promote"):
        return []
    blockers = [*remaining_blockers, _binding_blocker(context_branch)]
    classifications = _document_failure_classifications(context_branch, blockers, missing_or_unresolved)
    report = {
        "id": f"document_partial_evidence_{context_branch.get('id', 'branch')}",
        **_common_document_repair_payload(
            packet,
            context_branch,
            typed,
            context_ranking,
            missing_or_unresolved,
            already_stated,
            blockers,
        ),
        "status": "partial_evidence_non_repair",
        "closure_status": _branch_closure_status(context_branch, remaining_blockers),
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classification": classifications[0],
        "failure_classifications": classifications,
        "veto_ids": [LEGACY_BINDING_VETO_ID, DOCUMENT_PUBLICATION_VETO_ID],
        "candidate_edit_blocked": {
            "kind": "blocked_candidate_repair",
            "applicable": False,
            "reason": "Raw backend evidence is legacy/unbound and repair publication is quarantined.",
            "blocked_latex": _proposal_latex_for_branch(packet, context_branch),
        },
        "validation": {
            "status": "evidence_binding_veto",
            "source": "document_publication_quarantine",
            "contract": DOCUMENT_PARTIAL_EVIDENCE_REPORT_CONTRACT,
        },
        "non_claims": [
            "This is partial diagnostic evidence, not a repair proposal or document certificate.",
            "Backend success does not close missing assumptions or establish exact evidence-to-edit binding.",
            "The blocked candidate text must not be applied.",
        ],
    }
    return [attach_contract(report, DOCUMENT_PARTIAL_EVIDENCE_REPORT_CONTRACT)]


def _document_gap_reports(packet: dict[str, Any], root: dict[str, Any]) -> list[dict[str, Any]]:
    context_branch, typed, context_ranking, missing_or_unresolved, already_stated, remaining_blockers = _branch_context_for_report(packet, root)
    if context_branch is None:
        return []
    closure_status = _branch_closure_status(context_branch, remaining_blockers)
    raw = context_branch.get("backend_evidence", {}).get("raw_promotion", {})
    if isinstance(raw, dict) and raw.get("can_promote"):
        return []
    ranking = root.get("branch_ranking") if isinstance(root.get("branch_ranking"), dict) else {}
    classifications = _document_failure_classifications(
        context_branch, remaining_blockers, missing_or_unresolved
    )
    gap_reason_parts: list[str] = []
    if "mathematical_blocked" in classifications:
        gap_reason_parts.append("typed mathematical assumptions or domain conditions remain unresolved")
    if FORMALIZATION_BLOCKED in classifications:
        gap_reason_parts.append("backend formalization or translation remains incomplete")
    if BRANCH_EXECUTION_PENDING in classifications:
        gap_reason_parts.append("the exact branch-bound backend action has not been executed")
    gap_reason = "; ".join(gap_reason_parts) or "the branch remains open"
    report = {
        "id": f"document_gap_report_{context_branch.get('id', 'branch')}",
        **_common_document_repair_payload(
            packet,
            context_branch,
            typed,
            context_ranking,
            missing_or_unresolved,
            already_stated,
            remaining_blockers,
        ),
        "status": "blocked_gap_report",
        "closure_status": closure_status,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classification": classifications[0],
        "failure_classifications": classifications,
        "veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "candidate_edit_blocked": {
            "kind": "blocked_candidate_repair",
            "applicable": False,
            "reason": f"The serialization-only context branch is reported as a gap because {gap_reason}.",
            "blocked_latex": _proposal_latex_for_branch(packet, context_branch),
        },
        "validation": {
            "status": context_branch.get("validation_status"),
            "source": "strict_proposal_gate",
            "contract": DOCUMENT_GAP_REPORT_CONTRACT,
            "ranking_boundary": ranking.get("boundary", ""),
        },
        "non_claims": [
            "This is a gap report, not a repair proposal.",
            "No proposed edit should be applied until the remaining blockers are closed by source evidence or a certifying backend.",
            "The context branch is a serialization aid, not a scientific winner, global optimum, or minimal route.",
        ],
    }
    return [attach_contract(report, DOCUMENT_GAP_REPORT_CONTRACT)]


def _as_dicts(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _proposal_evidence_refs(item: dict[str, Any]) -> list[str]:
    refs = [str(ref) for ref in item.get("evidence_refs", []) if str(ref)]
    backend = item.get("backend_evidence") if isinstance(item.get("backend_evidence"), dict) else {}
    promotion = backend.get("promotion") if isinstance(backend.get("promotion"), dict) else {}
    refs.extend(str(ref) for ref in promotion.get("evidence_refs", []) if str(ref))
    for attempt in _as_dicts(item.get("translation_attempts")):
        refs.extend(str(ref) for ref in attempt.get("backend_attempt_ids", []) if str(ref))
        refs.extend(str(ref) for ref in attempt.get("blocker_ids", []) if str(ref))
    for blocker in _as_dicts(item.get("remaining_blockers_before_certification")):
        refs.extend(str(ref) for ref in blocker.get("evidence_refs", []) if str(ref))
    return list(dict.fromkeys(refs))


def _edit_target_mismatch(item: dict[str, Any]) -> bool:
    proposed_edit = item.get("proposed_edit")
    if not isinstance(proposed_edit, dict):
        return False
    report_target = str(item.get("target_label", "")).strip()
    edit_target = str(proposed_edit.get("target_label", "")).strip()
    return report_target != edit_target


def _validate_ready_proposal(proposal: dict[str, Any]) -> list[str]:
    errors: list[str] = ["document repair publication is disabled"]
    contract = proposal.get("metadata", {}).get("contract") if isinstance(proposal.get("metadata"), dict) else None
    if contract != DOCUMENT_READY_REPAIR_PROPOSAL_CONTRACT:
        errors.append("repair proposal contract is invalid")
    closure_status = str(proposal.get("closure_status", ""))
    if closure_status != "closed_by_exact_manifest":
        errors.append("repair proposal closure_status must be closed_by_exact_manifest")
    if not isinstance(proposal.get("proposed_edit"), dict) or not proposal.get("proposed_edit", {}).get("latex"):
        errors.append("repair proposal must include proposed_edit.latex")
    if _edit_target_mismatch(proposal):
        errors.append(f"{EDIT_TARGET_MISMATCH_VETO_ID}: proposed_edit.target_label must match target_label")
    if proposal.get("remaining_blockers_before_certification"):
        errors.append("closed_by_exact_manifest repair proposal must not carry remaining blockers")
    decision = proposal.get("promotion_decision")
    try:
        from .promotion_policy import verify_phase06_promotion_decision

        verified_decision = verify_phase06_promotion_decision(decision)
    except (TypeError, ValueError):
        verified_decision = None
        errors.append("repair proposal requires a verified Phase 06 promotion decision")
    if verified_decision is not None:
        if verified_decision.get("authority") == (
            "internal_consistency_only_requires_native_evidence_reevaluation"
        ):
            errors.append(
                "persisted Phase 06 decisions cannot authorize a repair without "
                "native evidence reevaluation"
            )
        if verified_decision.get("claim_eligibility") != "exact_manifest_eligible":
            errors.append("repair proposal requires exact_manifest_eligible claim status")
        if verified_decision.get("branch_id") != proposal.get("context_branch_id"):
            errors.append("repair proposal promotion branch binding mismatch")
    if not _proposal_evidence_refs(proposal):
        errors.append("repair proposal must include evidence refs")
    for field in ("location", "problem", "why"):
        if not str(proposal.get(field, "")).strip():
            errors.append(f"repair proposal must include {field}")
    return errors


def _validate_gap_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    contract = report.get("metadata", {}).get("contract") if isinstance(report.get("metadata"), dict) else None
    if contract != DOCUMENT_GAP_REPORT_CONTRACT:
        errors.append("gap report contract is invalid")
    closure_status = str(report.get("closure_status", ""))
    if closure_status == "closed_by_exact_manifest":
        errors.append("gap report cannot use exact-manifest closure_status")
    if "proposed_edit" in report:
        errors.append("gap report must not include proposed_edit")
    if not isinstance(report.get("candidate_edit_blocked"), dict):
        errors.append("gap report must include candidate_edit_blocked")
    if not _as_dicts(report.get("remaining_blockers_before_certification")):
        errors.append("gap report must include exact remaining blockers")
    if not _proposal_evidence_refs(report):
        errors.append("gap report must include evidence refs")
    for field in ("location", "problem", "why"):
        if not str(report.get(field, "")).strip():
            errors.append(f"gap report must include {field}")
    return errors


def _validate_partial_evidence_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    contract = report.get("metadata", {}).get("contract") if isinstance(report.get("metadata"), dict) else None
    if contract != DOCUMENT_PARTIAL_EVIDENCE_REPORT_CONTRACT:
        errors.append("partial evidence report contract is invalid")
    if report.get("publication_mode") != DOCUMENT_PUBLICATION_MODE:
        errors.append("partial evidence report must keep publication disabled")
    if "proposed_edit" in report or "proposed_text" in report:
        errors.append("partial evidence report must not include an applicable edit field")
    blocked = report.get("candidate_edit_blocked")
    if not isinstance(blocked, dict) or blocked.get("applicable") is not False:
        errors.append("partial evidence report must include a non-applicable blocked candidate")
    if LEGACY_BINDING_VETO_ID not in report.get("veto_ids", []):
        errors.append("partial evidence report must include the legacy binding veto")
    if not _as_dicts(report.get("remaining_blockers_before_certification")):
        errors.append("partial evidence report must list remaining blockers")
    if not _proposal_evidence_refs(report):
        errors.append("partial evidence report must include evidence refs")
    return errors


def _compiled_item(
    item: dict[str, Any],
    *,
    item_type: str,
    publishable: bool,
    validation_errors: list[str],
) -> dict[str, Any]:
    _ = publishable
    mismatch = _edit_target_mismatch(item)
    errors = list(validation_errors)
    mismatch_error = f"{EDIT_TARGET_MISMATCH_VETO_ID}: proposed_edit.target_label must match target_label"
    if mismatch and mismatch_error not in errors:
        errors.append(mismatch_error)

    classifications = [str(value) for value in item.get("failure_classifications", []) if str(value)]
    if mismatch and "evidence_binding_error" not in classifications:
        classifications.append("evidence_binding_error")
    primary_classification = item.get("failure_classification")
    if mismatch:
        primary_classification = "evidence_binding_error"

    veto_ids = [str(value) for value in item.get("veto_ids", []) if str(value)]
    for veto_id in (DOCUMENT_PUBLICATION_VETO_ID, EDIT_TARGET_MISMATCH_VETO_ID if mismatch else None):
        if veto_id and veto_id not in veto_ids:
            veto_ids.append(veto_id)

    return {
        **_integrity_from(item),
        "id": item.get("id"),
        "type": item_type,
        "target_label": item.get("target_label"),
        "location": item.get("location"),
        "closure_status": item.get("closure_status"),
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "publishable_as_repair": False,
        "publishable_as_gap_report": item_type == "gap_report" and not errors,
        "reportable_as_partial_evidence": item_type == "partial_evidence" and not errors,
        "failure_classification": primary_classification,
        "failure_classifications": classifications,
        "veto_ids": veto_ids,
        "context_branch_id": item.get("context_branch_id"),
        "context_branch_selection_authority": item.get("context_branch_selection_authority"),
        "nondominated_branch_ids": item.get("nondominated_branch_ids", []),
        "selected_action_id": item.get("selected_action_id"),
        "evidence_refs": _proposal_evidence_refs(item),
        "remaining_blocker_ids": [
            str(blocker.get("id", ""))
            for blocker in _as_dicts(item.get("remaining_blockers_before_certification"))
            if blocker.get("id")
        ],
        "validation_errors": errors,
        "contract": item.get("metadata", {}).get("contract") if isinstance(item.get("metadata"), dict) else "",
    }


_COMPILER_DERIVED_ROOT_FIELDS = frozenset(
    {
        "tool_grounded_proposal_compiler",
        "document_ready_repair_proposals",
        "document_gap_reports",
        "document_partial_evidence_reports",
    }
)


def _walk_recursive_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = [node]
    for child in node.get("children", []) if isinstance(node.get("children"), list) else []:
        if isinstance(child, dict):
            nodes.extend(_walk_recursive_nodes(child))
    return nodes


def _recursive_expansion_ranking(root: dict[str, Any]) -> dict[str, Any]:
    nodes = _walk_recursive_nodes(root)[1:]
    ordered = sorted(
        nodes,
        key=lambda node: (
            len(_walk_recursive_nodes(node)),
            str(node.get("generator", {}).get("kind", "unknown")),
            str(node.get("id", "")),
        ),
    )
    rankings = [
        {
            "rank": index,
            "node_id": node.get("id"),
            "parent_node_id": node.get("parent_node_id"),
            "status": node.get("status"),
            "generator_kind": node.get("generator", {}).get("kind")
            if isinstance(node.get("generator"), dict)
            else None,
            "backend_attempt_count": len(
                [item for item in node.get("backend_attempts", []) if isinstance(item, dict)]
            ),
            "blocker_count": len([item for item in node.get("blockers", []) if isinstance(item, dict)]),
            "execution_status": "unexecuted"
            if not node.get("backend_attempts")
            else "branch_bound_attempts_recorded",
        }
        for index, node in enumerate(ordered, start=1)
    ]
    return {
        "status": "ranked_unexecuted_candidates" if rankings else "no_expanded_candidates",
        "ranked_node_ids": [str(item["node_id"]) for item in rankings if item.get("node_id")],
        "rankings": rankings,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "boundary": (
            "Expanded-node ordering is deterministic exploratory triage. Rule-generated and unexecuted "
            "nodes carry no mathematical or document-repair authority."
        ),
    }


def _document_final_tree_projection(tree: dict[str, Any]) -> dict[str, Any]:
    root = tree.get("root") if isinstance(tree.get("root"), dict) else {}
    projected_root = {
        key: value
        for key, value in root.items()
        if key not in _COMPILER_DERIVED_ROOT_FIELDS
    }
    recursive_expansion = (
        dict(tree.get("recursive_expansion", {}))
        if isinstance(tree.get("recursive_expansion"), dict)
        else {}
    )
    recursive_expansion.pop("tree", None)
    return {
        "status": tree.get("status"),
        "target": tree.get("target"),
        "controller": tree.get("controller", {}),
        "root": projected_root,
        "recursive_expansion": recursive_expansion,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
    }


def _document_final_tree_digest(tree: dict[str, Any]) -> str:
    payload = json.dumps(
        _document_final_tree_projection(tree),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _compile_tool_grounded_proposal_report(
    packet: dict[str, Any],
    tree: dict[str, Any],
    *,
    grounding_policy: str = STRICT_GROUNDING_POLICY,
) -> dict[str, Any]:
    """Compile ranked-branch outputs into strict repair/gap ledgers."""
    root = tree.get("root") if isinstance(tree.get("root"), dict) else {}
    final_nodes = _walk_recursive_nodes(root) if root else []
    final_tree_digest = _document_final_tree_digest(tree)
    final_tree_node_ids = [str(node.get("id", "")) for node in final_nodes if node.get("id")]
    expanded_node_ids = [str(node.get("id", "")) for node in final_nodes[1:] if node.get("id")]
    ready = _document_ready_repair_proposals(packet, root)
    partials = _document_partial_evidence_reports(packet, root)
    gaps = _document_gap_reports(packet, root)
    compiled_items: list[dict[str, Any]] = []
    validation_errors: list[dict[str, Any]] = []
    for proposal in ready:
        errors = _validate_ready_proposal(proposal)
        compiled_items.append(
            _compiled_item(
                proposal,
                item_type="repair_proposal",
                publishable=True,
                validation_errors=errors,
            )
        )
        if errors:
            validation_errors.append({"id": proposal.get("id"), "type": "repair_proposal", "errors": errors})
    for report in partials:
        errors = _validate_partial_evidence_report(report)
        compiled_items.append(
            _compiled_item(
                report,
                item_type="partial_evidence",
                publishable=False,
                validation_errors=errors,
            )
        )
        if errors:
            validation_errors.append({"id": report.get("id"), "type": "partial_evidence", "errors": errors})
    for report in gaps:
        errors = _validate_gap_report(report)
        compiled_items.append(
            _compiled_item(
                report,
                item_type="gap_report",
                publishable=False,
                validation_errors=errors,
            )
        )
        if errors:
            validation_errors.append({"id": report.get("id"), "type": "gap_report", "errors": errors})
    repair_count = sum(1 for item in compiled_items if item["publishable_as_repair"])
    gap_count = sum(1 for item in compiled_items if item["publishable_as_gap_report"])
    partial_count = sum(1 for item in compiled_items if item["reportable_as_partial_evidence"])
    if validation_errors:
        status = "invalid_compiler_output"
    elif repair_count or gap_count or partial_count:
        status = "compiled"
    else:
        status = "no_publishable_items"
    result = {
        **_integrity_from(root),
        "status": status,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "publication_veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "grounding_policy": grounding_policy,
        "target_label": packet.get("label"),
        "final_tree_digest": final_tree_digest,
        "final_tree_node_ids": list(final_tree_node_ids),
        "expanded_node_ids": list(expanded_node_ids),
        "compiled_after_recursive_expansion": True,
        "unique_top_branch_id": root.get("branch_ranking", {}).get("top_branch_id")
        if isinstance(root.get("branch_ranking"), dict) else None,
        "nondominated_branch_ids": root.get("branch_ranking", {}).get("nondominated_branch_ids", [])
        if isinstance(root.get("branch_ranking"), dict) else [],
        "selected_action_id": (
            root.get("branch_ranking", {}).get("selected_action", {}).get("action_id")
            if isinstance(root.get("branch_ranking", {}).get("selected_action"), dict)
            else None
        ),
        "repair_proposal_count": repair_count,
        "gap_report_count": gap_count,
        "partial_evidence_count": partial_count,
        "blocked_candidate_count": len(gaps) + len(partials),
        "document_ready_repair_proposals": [
            proposal
            for proposal in ready
            if any(
                compiled.get("id") == proposal.get("id") and compiled.get("publishable_as_repair")
                for compiled in compiled_items
            )
        ],
        "document_gap_reports": [
            report
            for report in gaps
            if any(
                compiled.get("id") == report.get("id") and compiled.get("publishable_as_gap_report")
                for compiled in compiled_items
            )
        ],
        "document_partial_evidence_reports": [
            report
            for report in partials
            if any(
                compiled.get("id") == report.get("id") and compiled.get("reportable_as_partial_evidence")
                for compiled in compiled_items
            )
        ],
        "compiled_items": compiled_items,
        "validation_errors": validation_errors,
        "boundary": (
            "Document repair publication is disabled. Legacy backend closure is partial evidence only; "
            "blocked paths are gap reports and all candidate edit text remains non-applicable."
        ),
        "non_claims": [
            "The compiler emits no repair proposals while publication is quarantined.",
            "Partial-order membership alone never makes a branch publishable as a repair.",
            "Rule-generated or unexecuted expanded nodes are exploratory candidates only.",
            "Gap reports are actionable blockers, not proposed edits.",
            "Partial evidence is diagnostic and cannot be applied as an edit.",
        ],
    }
    return attach_contract(result, TOOL_GROUNDED_PROPOSAL_COMPILER_CONTRACT)


def _requested_equation_labels(
    rows: list[dict[str, Any]],
    *,
    focus_labels: list[str] | None,
    max_labels: int | None,
) -> list[str]:
    labeled = [str(row["label"]) for row in rows if isinstance(row.get("label"), str) and row.get("label")]
    available = set(labeled)
    if focus_labels:
        selected: list[str] = []
        seen: set[str] = set()
        for label in focus_labels:
            if label in available and label not in seen:
                selected.append(label)
                seen.add(label)
        return selected
    labels = list(dict.fromkeys(labeled))
    limit = max_labels if max_labels is not None else DEFAULT_LABEL_LIMIT
    if limit is not None and limit > 0:
        labels = labels[:limit]
    return labels


def _select_label_scoped_targets(
    path: Path,
    rows: list[dict[str, Any]],
    *,
    focus_labels: list[str] | None,
    max_labels: int | None,
    index: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    labels = _requested_equation_labels(rows, focus_labels=focus_labels, max_labels=max_labels)
    selected: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    seen_target_labels: set[str] = set()
    for label in labels:
        result = extract_derivation_targets_for_label(index, label, file=path.name)
        candidates = [
            item
            for item in result.get("targets", [])
            if isinstance(item, dict)
            and item.get("label") == label
            and item.get("adapter_eligible") is True
            and isinstance(item.get("label_scoped_obligation"), dict)
        ]
        accepted: list[dict[str, Any]] = []
        if result.get("status") == "extracted" and len(candidates) == 1 and label not in seen_target_labels:
            accepted = candidates
            selected.extend(candidates)
            seen_target_labels.add(label)
        diagnostics.append(
            {
                "label": label,
                "status": result.get("status"),
                "reason": result.get("reason"),
                "candidate_target_count": len(candidates),
                "accepted_target_count": len(accepted),
                "obligation_ids": [item.get("obligation_id") for item in accepted],
                "obligation_digests": [item.get("obligation_digest") for item in accepted],
                "ambiguities": result.get("ambiguities", []),
            }
        )
    failed = [item for item in diagnostics if item["accepted_target_count"] != 1]
    return selected, {
        "method": "validated_label_scoped_obligation",
        "requested_equation_labels": labels,
        "selected_target_labels": [str(item.get("label")) for item in selected],
        "selected_target_count": len(selected),
        "failure_count": len(failed),
        "failures": failed,
        "results": diagnostics,
        "fallback_to_locator_row": False,
        "non_claim": "Validated target extraction establishes source ownership, not mathematical truth.",
    }


def _location(tex_path: Path, row: dict[str, Any], sections: list[dict[str, Any]]) -> str:
    parts = [tex_path.name]
    parts.extend(_section_path_for_line(sections, int(row.get("line_start", 0))))
    if row.get("label"):
        parts.append(str(row["label"]))
    parts.append(f"line {row.get('line_start', 'unknown')}")
    return " > ".join(parts)


def _semantic_text(row: dict[str, Any], claim_type: str) -> str:
    return "\n".join(
        item
        for item in (
            str(row.get("text", "")),
            str(row.get("source_text", "")),
            claim_type,
        )
        if item
    )


def _semantic_packet(
    row: dict[str, Any],
    *,
    tex_path: Path,
    sections: list[dict[str, Any]],
    rows_for_label: list[dict[str, Any]],
    rows_for_environment: list[dict[str, Any]],
    paragraph_context: dict[str, Any] | None = None,
    display: dict[str, Any] | None = None,
) -> dict[str, Any]:
    claim_type = _classify_equation(row)
    grouped_source_target = str(display.get("grouped_source_target", "")) if isinstance(display, dict) else str(row.get("text", ""))
    text = "\n".join(
        item
        for item in (
            _semantic_text(row, claim_type),
            grouped_source_target if grouped_source_target != str(row.get("text", "")) else "",
        )
        if item
    )
    abstention = build_actionable_abstention_payload(
        text=text,
        problem=f"Build a semantic derivation route for `{row.get('label')}` before backend certification.",
        why_not_concrete="Raw LaTeX rows are not sufficient proof obligations.",
        location=_location(tex_path, row, sections),
        kind=claim_type,
        evidence_refs=[str(row.get("id", row.get("label", "row")))],
    )
    assumptions = assumptions_required(str(row.get("text", "")))
    lhs, rhs, target = _split_target(str(row.get("text", "")))
    grouped_lhs, grouped_rhs, grouped_target = _split_target(grouped_source_target)
    display_source_span = {
        "file": display.get("file"),
        "line_start": display.get("line_start"),
        "line_end": display.get("line_end"),
        "labels": display.get("labels", []),
        "environment": display.get("environment"),
        "section_path": _section_path_for_line(sections, int(display.get("line_start", row.get("line_start", 0)))),
    } if isinstance(display, dict) else {}
    packet = {
        "id": f"semantic_packet_{_slug(str(row.get('label') or row.get('id')))}_{row.get('row_index', 0)}",
        "label": row.get("label"),
        "row_id": row.get("id"),
        "location": _location(tex_path, row, sections),
        "source_span": {
            "file": row.get("file"),
            "line_start": row.get("line_start"),
            "line_end": row.get("line_end"),
            "label": row.get("label"),
            "section_path": _section_path_for_line(sections, int(row.get("line_start", 0))),
        },
        "claim_type": claim_type,
        "target": target,
        "lhs": lhs,
        "rhs": rhs,
        "grouped_target": grouped_target,
        "grouped_lhs": grouped_lhs,
        "grouped_rhs": grouped_rhs,
        "lhs_rhs_candidates": [
            {
                "source": "row",
                "lhs": lhs,
                "rhs": rhs,
                "target": target,
                "line_start": row.get("line_start"),
                "line_end": row.get("line_end"),
            },
            {
                "source": "full_display",
                "lhs": grouped_lhs,
                "rhs": grouped_rhs,
                "target": grouped_target,
                "line_start": display_source_span.get("line_start"),
                "line_end": display_source_span.get("line_end"),
            },
        ],
        "source_text": row.get("text", ""),
        "paragraph_context": paragraph_context or {},
        "full_display_source": display.get("full_display_source", "") if isinstance(display, dict) else "",
        "display_source_span": display_source_span,
        "display_labels": display.get("labels", []) if isinstance(display, dict) else [],
        "display_row_count": sum(
            1
            for item in rows_for_environment
            if isinstance(display, dict)
            and item.get("file") == display.get("file")
            and int(display.get("line_start", 0)) <= int(item.get("line_start", 0) or 0)
            and int(display.get("line_end", 0)) >= int(item.get("line_end", 0) or 0)
        ),
        "operator_inventory": display.get("operator_inventory", _operator_inventory(str(row.get("text", "")))) if isinstance(display, dict) else _operator_inventory(str(row.get("text", ""))),
        "symbol_inventory": display.get("symbol_inventory", _symbol_inventory(str(row.get("text", "")))) if isinstance(display, dict) else _symbol_inventory(str(row.get("text", ""))),
        "source_environment": row.get("environment"),
        "uncertainty": list(row.get("uncertainty", [])),
        "label_row_count": len(rows_for_label),
        "semantic_domains": abstention.get("domains", []),
        "missing_obligations": abstention.get("missing_obligations", []),
        "possible_assumption_sets": abstention.get("possible_assumption_sets", []),
        "how_derivation_can_work": abstention.get("how_derivation_can_work", []),
        "route_required_assumptions": assumptions.get("assumptions", []),
        "missing_route_assumptions": assumptions.get("missing_assumptions", []),
        "next_audit": abstention.get("next_audit", {}),
        "evidence_refs": [str(row.get("id", row.get("label", "row"))), "actionable_abstention_payload", "assumption_discovery_result"],
        "non_claim": "Semantic work packets are deterministic guidance for proof search; they are not proof certificates.",
    }
    packet["context_graph"] = build_local_context_graph(packet)
    packet["typed_repair_obligation"] = typed_repair_obligation_from_packet(packet)
    return packet


def _semantic_packet_from_label_scoped_target(
    target_record: dict[str, Any],
    *,
    tex_path: Path,
    sections: list[dict[str, Any]],
    paragraph_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a semantic packet from one validated, source-owned obligation."""
    obligation = target_record.get("label_scoped_obligation")
    if not isinstance(obligation, dict):
        raise ValueError("label-scoped target is missing its obligation record")
    normalized = obligation.get("normalized_target")
    if not isinstance(normalized, dict) or normalized.get("complete_lhs_rhs") is not True:
        raise ValueError("label-scoped target is not a complete canonical relation")
    if target_record.get("obligation_id") != obligation.get("obligation_id"):
        raise ValueError("label-scoped target obligation id does not match its source record")
    if target_record.get("obligation_digest") != obligation.get("obligation_digest"):
        raise ValueError("label-scoped target obligation digest does not match its source record")

    label = str(obligation.get("label", target_record.get("label", "")))
    target = str(normalized.get("display_text", ""))
    lhs = str(target_record.get("lhs", ""))
    rhs = str(target_record.get("rhs", ""))
    equality_like = normalized.get("kind") in {"equality", "equality_chain", "aligned_definition"}
    if not label or not target or (equality_like and (not lhs or not rhs)):
        raise ValueError("label-scoped target lacks required canonical relation fields")
    owned_rows = [item for item in obligation.get("owned_rows", []) if isinstance(item, dict)]
    owned_spans = [item for item in obligation.get("owned_spans", []) if isinstance(item, dict)]
    if not owned_rows or not owned_spans:
        raise ValueError("label-scoped target lacks exact owned rows or spans")

    source_math = str(obligation.get("source_math", ""))
    document = obligation.get("document") if isinstance(obligation.get("document"), dict) else {}
    environment = obligation.get("environment") if isinstance(obligation.get("environment"), dict) else {}
    source_span = {
        "file": document.get("file") or target_record.get("source_file") or target_record.get("file"),
        "line_start": owned_spans[0].get("line_start"),
        "line_end": owned_spans[-1].get("line_end"),
        "label": label,
        "section_path": _section_path_for_line(sections, int(owned_spans[0].get("line_start", 0))),
        "start_byte": owned_spans[0].get("start_byte"),
        "end_byte": owned_spans[-1].get("end_byte"),
        "source_digest": document.get("source_digest"),
        "obligation_id": obligation.get("obligation_id"),
        "obligation_digest": obligation.get("obligation_digest"),
    }
    location_row = {
        "file": target_record.get("file") or tex_path.name,
        "line_start": source_span["line_start"],
        "label": label,
    }
    routing_role = target_record.get("routing_role") if isinstance(target_record.get("routing_role"), dict) else {}
    claim_type = str(routing_role.get("role", "unsupported_or_ambiguous"))
    packet_id = f"semantic_packet_{_slug(label)}_{str(obligation['obligation_digest'])[:16]}"
    if has_role_specific_builder(routing_role, target=target):
        role_obligations = build_role_specific_obligations(
            target=target,
            normalized_target={**normalized, "operator_inventory": obligation.get("operator_inventory", [])},
            routing_role=routing_role,
            evidence_refs=[str(obligation["obligation_id"]), str(obligation["obligation_digest"])],
        )
        semantic_domains = [f"role:{role_obligations['role']}", f"relation:{role_obligations['relation_kind']}"]
        local_obligations = role_obligations.get("local_obligations", [])
        downstream_obligations = role_obligations.get("downstream_integration_obligations", [])
        possible_sets = role_obligations.get("possible_assumption_sets", [])
        derivation_route = role_obligations.get("derivation_route", [])
        next_audit = role_obligations.get("next_audit", {})
    else:
        generic = build_actionable_abstention_payload(
            text="\n".join(item for item in (source_math, target, claim_type) if item),
            problem=f"Build a semantic derivation route for `{label}` before backend certification.",
            why_not_concrete="A validated source obligation still requires explicit assumptions and backend evidence.",
            location=_location(tex_path, location_row, sections),
            kind=claim_type,
            evidence_refs=[str(obligation["obligation_id"]), str(obligation["obligation_digest"])],
        )
        role_obligations = None
        semantic_domains = generic.get("domains", [])
        local_obligations = generic.get("missing_obligations", [])
        downstream_obligations = []
        possible_sets = generic.get("possible_assumption_sets", [])
        derivation_route = generic.get("how_derivation_can_work", [])
        next_audit = generic.get("next_audit", {})
    assumptions = assumptions_required(target)
    scoped_symbols = obligation.get("symbol_inventory") if isinstance(obligation.get("symbol_inventory"), dict) else {}
    compatibility_symbols = {
        "macros": list(scoped_symbols.get("latex_commands", [])),
        "identifiers": list(scoped_symbols.get("bare_identifiers", [])),
    }
    packet = {
        "id": packet_id,
        "label": label,
        "row_id": owned_rows[0].get("row_id"),
        "location": _location(tex_path, location_row, sections),
        "source_span": source_span,
        "claim_type": claim_type,
        "target": target,
        "lhs": lhs,
        "rhs": rhs,
        "grouped_target": target,
        "grouped_lhs": lhs,
        "grouped_rhs": rhs,
        "lhs_rhs_candidates": [
            {
                "source": "row",
                "binding": "label_scoped_obligation",
                "lhs": lhs,
                "rhs": rhs,
                "target": target,
                "line_start": source_span["line_start"],
                "line_end": source_span["line_end"],
            },
            {
                "source": "full_display",
                "binding": "label_scoped_owned_source",
                "lhs": lhs,
                "rhs": rhs,
                "target": target,
                "line_start": source_span["line_start"],
                "line_end": source_span["line_end"],
            },
        ],
        "source_text": source_math,
        "paragraph_context": paragraph_context or {},
        "full_display_source": source_math,
        "display_source_span": {
            **source_span,
            "labels": [label],
            "environment": environment.get("kind"),
        },
        "display_labels": [label],
        "display_row_count": len(owned_rows),
        "operator_inventory": list(obligation.get("operator_inventory", [])),
        "symbol_inventory": scoped_symbols,
        "symbol_inventory_compatibility": compatibility_symbols,
        "source_environment": environment.get("kind"),
        "uncertainty": list(obligation.get("uncertainties", [])),
        "label_row_count": len(owned_rows),
        "semantic_domains": semantic_domains,
        "missing_obligations": local_obligations,
        "local_obligations": local_obligations,
        "downstream_integration_obligations": downstream_obligations,
        "possible_assumption_sets": possible_sets,
        "how_derivation_can_work": derivation_route,
        "route_required_assumptions": assumptions.get("assumptions", []),
        "missing_route_assumptions": assumptions.get("missing_assumptions", []),
        "next_audit": next_audit,
        "obligation_id": obligation["obligation_id"],
        "obligation_digest": obligation["obligation_digest"],
        "owned_spans": owned_spans,
        "excluded_spans": list(obligation.get("excluded_spans", [])),
        "normalized_target": normalized,
        "routing_role": routing_role,
        "specialist_execution": target_record.get("specialist_execution"),
        "role_obligation_contract": role_obligations,
        "label_scoped_obligation": obligation,
        "target_ingress": "validated_label_scoped_obligation",
        "evidence_refs": [
            str(obligation["obligation_id"]),
            str(obligation["obligation_digest"]),
            "actionable_abstention_payload",
            "assumption_discovery_result",
        ],
        "non_claim": "Semantic work packets are deterministic guidance for proof search; they are not proof certificates.",
    }
    packet["context_graph"] = build_local_context_graph(packet)
    packet["typed_repair_obligation"] = typed_repair_obligation_from_packet(packet)
    return packet


def _blocker_from_obligation(packet: dict[str, Any], obligation: dict[str, Any]) -> dict[str, Any]:
    obligation_id = str(obligation.get("id", "missing_obligation"))
    return {
        "id": f"blocker_{packet['id']}_{_slug(obligation_id)}",
        "kind": str(obligation.get("kind", "semantic_obligation_missing")),
        "problem": str(obligation.get("mathematically_missing") or "A semantic obligation is missing."),
        "why": str(obligation.get("why_missing") or "The derivation route needs this obligation before certification."),
        "required_next_evidence": str(obligation.get("closes") or "State or verify this obligation, then rerun the tree audit."),
        "source": "semantic_work_packet",
        "evidence_refs": [str(obligation.get("evidence_ref", packet["id"]))],
    }


def _augment_tree(tree: dict[str, Any], packet: dict[str, Any], *, source_path: Path) -> None:
    root = tree.get("root", {})
    root["source_span"] = packet["source_span"]
    root.setdefault("semantic_work_packet", packet)
    specialist = packet.get("specialist_execution")
    if isinstance(specialist, dict):
        root["specialist_execution"] = specialist
        backend_attempt = specialist.get("result", {}).get("backend_attempt")
        if isinstance(backend_attempt, dict):
            root.setdefault("specialist_backend_evidence", []).append(
                {
                    **backend_attempt,
                    "label": packet.get("label"),
                    "obligation_digest": packet.get("obligation_digest"),
                    "claim_eligibility": "ineligible",
                    "publication_enabled": False,
                    "promotion_boundary": "diagnostic specialist evidence cannot promote a branch",
                }
            )
    if isinstance(packet.get("context_graph"), dict):
        root.setdefault("context_graph", packet["context_graph"])
    if isinstance(packet.get("typed_repair_obligation"), dict):
        root.setdefault("typed_repair_obligations", [packet["typed_repair_obligation"]])
    plan = root.get("external_tool_first_plan", {})
    branches = root.setdefault("assumption_branches", [])
    assumptions = root.setdefault("assumptions", [])
    for item in packet.get("possible_assumption_sets", []):
        branch = _assumption_branch(packet, item, plan if isinstance(plan, dict) else {})
        branch["formalization_stubs"] = _formalization_stubs(packet, branch)
        _attach_branch_backend_evidence(packet, branch, root)
        if isinstance(specialist, dict):
            branch["specialist_execution"] = specialist
        branches.append(branch)
        assumptions.append(
            {
                "id": item.get("id", "assumption_set"),
                "assumptions": item.get("assumptions", []),
                "status": "proposed_sufficient",
                "source": "semantic_work_packet",
                "closes": branch.get("closes_obligations", []),
                "branch_id": branch["id"],
                "mathematical_why": branch["mathematical_why"],
                "derivation_route_under_assumptions": branch["derivation_route_under_assumptions"],
                "external_tool_first_ledger": branch["external_tool_first_ledger"],
                "evidence_refs": [packet["id"]],
            }
        )
        root.setdefault("patch_candidates", []).append(_patch_candidate_for_branch(packet, branch))
        root.setdefault("blockers", []).extend(branch.get("blockers", []))
    for item in packet.get("route_required_assumptions", []):
        assumptions.append(
            {
                "id": f"route_assumption_{_slug(str(item.get('source', item.get('text', 'assumption'))))}",
                "assumptions": [item.get("text", "")],
                "status": item.get("status", "diagnostic"),
                "source": "assumption_discovery",
                "closes": item.get("used_by", []),
                "evidence_refs": item.get("route_category_sources", []),
            }
        )
    steps = root.setdefault("derivation_steps", [])
    for index, step in enumerate(packet.get("how_derivation_can_work", []), start=1):
        steps.append(
            {
                "id": f"{packet['id']}_route_step_{index}",
                "claim": step.get("step", ""),
                "justification": step.get("detail", ""),
                "checker": "semantic_work_packet",
                "checker_status": "diagnostic_route",
                "evidence_refs": [packet["id"]],
            }
        )
    blockers = root.setdefault("blockers", [])
    for obligation in packet.get("missing_obligations", []):
        blockers.append(_blocker_from_obligation(packet, obligation))
    if packet.get("uncertainty"):
        blockers.append(
            {
                "id": f"blocker_{packet['id']}_source_extraction_uncertainty",
                "kind": "source_extraction_uncertainty",
                "problem": "The localized source row has extraction uncertainty.",
                "why": f"Equation locator reported: {', '.join(str(item) for item in packet.get('uncertainty', []))}.",
                "required_next_evidence": "Recover a complete source-local obligation before promoting a derivation.",
                "source": "locate_equations_in_file",
                "evidence_refs": [str(packet.get("row_id"))],
            }
        )
    if packet.get("target_ingress") != "validated_label_scoped_obligation" and max(
        int(packet.get("label_row_count", 1)),
        int(packet.get("display_row_count", 1)),
    ) > 1:
        blockers.append(
            {
                "id": f"blocker_{packet['id']}_grouped_multiline_obligation_required",
                "kind": "grouped_multiline_obligation_required",
                "problem": "The label or its reconstructed display spans multiple localized equation rows.",
                "why": "A single-row tree attempt cannot certify a full multiline align environment.",
                "required_next_evidence": "Group all rows for the label into one formal obligation or split them into separately labeled obligations.",
                "source": "locate_equations_in_file",
                "evidence_refs": [str(packet.get("label"))],
            }
        )
    display_span = packet.get("display_source_span")
    if not isinstance(display_span, dict) or not display_span:
        blockers.append(
            {
                "id": f"blocker_{packet['id']}_full_display_source_required",
                "kind": "full_display_source_required",
                "problem": "The packet does not contain a reconstructed full display environment.",
                "why": "Concrete repair text and backend formalization need the full local display, not only one localized row.",
                "required_next_evidence": "Recover the complete display source around the localized row before proposing replacement text.",
                "source": "document_derivation_tree",
                "evidence_refs": [str(packet.get("row_id"))],
            }
        )
    expansion_result = expand_tree_with_hypotheses(
        tree,
        budget={"max_depth": 1, "max_nodes": 2, "max_agent_expansions_per_blocker": 1},
    )
    tree["recursive_expansion"] = {
        key: value
        for key, value in expansion_result.items()
        if key != "tree"
    }
    root["branch_ranking"] = _quarantine_branch_ranking(rank_repair_branches(branches), branches)
    root["recursive_expansion_ranking"] = _recursive_expansion_ranking(root)
    corpus_version = packet.get("label_scoped_obligation", {}).get("document", {}).get("corpus_version")
    if (
        packet.get("routing_role", {}).get("authority") == "source_evidenced_role"
        and corpus_version == FROZEN_CORPUS_VERSION
    ):
        binding = build_document_evidence_binding(
            packet,
            branches,
            source_path=source_path,
        )
        root["document_evidence_binding"] = binding
        root.update(_current_document_integrity_binding(binding))
        for evidence in root.get("specialist_backend_evidence", []):
            if isinstance(evidence, dict):
                evidence.update(_current_document_integrity_binding(binding))
        for branch in branches:
            branch.update(_current_document_integrity_binding(binding))
            evidence = branch.get("backend_evidence")
            if isinstance(evidence, dict):
                evidence.update(_current_document_integrity_binding(binding))
                evidence["binding_status"] = "verified_current_evidence"
                evidence["veto_ids"] = [DOCUMENT_PUBLICATION_VETO_ID]
                evidence["effective_document_promotion"] = _effective_document_promotion(
                    evidence.get("raw_promotion"),
                    current_binding=True,
                )
        root["branch_ranking"] = _quarantine_branch_ranking(
            rank_repair_branches(branches),
            branches,
        )
    compiler = _compile_tool_grounded_proposal_report(packet, tree)
    root["tool_grounded_proposal_compiler"] = compiler
    root["document_ready_repair_proposals"] = compiler.get("document_ready_repair_proposals", [])
    root["document_gap_reports"] = compiler.get("document_gap_reports", [])
    root["document_partial_evidence_reports"] = compiler.get("document_partial_evidence_reports", [])
    tree["final_tree_digest"] = compiler["final_tree_digest"]


def _quarantine_report_sections(
    rendered: dict[str, Any],
    *,
    current_binding: bool = False,
) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for section in rendered.get("sections", []) if isinstance(rendered.get("sections"), list) else []:
        if not isinstance(section, dict):
            continue
        item = dict(section)
        raw = item.get("promotion") if isinstance(item.get("promotion"), dict) else {}
        item["promotion"] = _effective_document_promotion(
            raw,
            current_binding=current_binding,
        )
        if raw.get("can_promote"):
            item["status"] = "partial_evidence"
        patches: list[dict[str, Any]] = []
        for patch in item.get("proposed_patches", []) if isinstance(item.get("proposed_patches"), list) else []:
            if not isinstance(patch, dict):
                continue
            blocked = dict(patch)
            text = blocked.pop("proposed_text", None)
            if text and "candidate_text_blocked" not in blocked:
                blocked["candidate_text_blocked"] = text
            blocked.update(
                {
                    "kind": "blocked_candidate_repair",
                    "status": "non_applicable_publication_quarantine",
                    "applicable": False,
                    "validation_status": "blocked_non_applicable",
                    "veto_ids": [LEGACY_BINDING_VETO_ID, DOCUMENT_PUBLICATION_VETO_ID],
                }
            )
            patches.append(blocked)
        item["proposed_patches"] = patches
        sections.append(item)
    return sections


def _compact_tree(tree: dict[str, Any], rendered: dict[str, Any]) -> dict[str, Any]:
    root = tree.get("root", {})
    controller = tree.get("controller", {})
    raw_controller_promotion = controller.get("promotion") if isinstance(controller.get("promotion"), dict) else {}
    compact_status = "partial_evidence" if raw_controller_promotion.get("can_promote") else tree.get("status")
    engineering_error = any(
        str(attempt.get("status", "")).endswith("error")
        for attempt in root.get("backend_attempts", [])
        if isinstance(attempt, dict)
    )
    failure_classifications = {
        str(value)
        for branch in root.get("assumption_branches", [])
        if isinstance(branch, dict)
        for value in [branch.get("backend_evidence", {}).get("failure_classification")]
        if value
    }
    for report_key in ("document_partial_evidence_reports", "document_gap_reports"):
        for report in root.get(report_key, []):
            if not isinstance(report, dict):
                continue
            failure_classifications.update(
                str(value) for value in report.get("failure_classifications", []) if str(value)
            )
    if engineering_error:
        failure_classifications.add("engineering_error")
    integrity = _integrity_from(root)
    current_binding = root.get("integrity_binding_verified") is True
    return {
        **integrity,
        "status": compact_status,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classifications": sorted(failure_classifications),
        "veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "summary": tree.get("summary"),
        "controller": {
            "status": compact_status,
            "raw_status": controller.get("status"),
            "reason": "Document promotion is quarantined; raw controller status is diagnostic history only.",
            "raw_reason": controller.get("reason"),
            "attempts_used": controller.get("attempts_used"),
            "exhausted_actions": controller.get("exhausted_actions", []),
            "promotion": _effective_document_promotion(
                raw_controller_promotion,
                current_binding=current_binding,
            ),
            "validation_errors": controller.get("validation_errors", []),
        },
        "backend_attempts": [
            _document_attempt_view(attempt)
            for attempt in root.get("backend_attempts", [])
            if isinstance(attempt, dict)
        ],
        "specialist_execution": root.get("specialist_execution", {}),
        "specialist_backend_evidence": root.get("specialist_backend_evidence", []),
        "document_evidence_binding": root.get("document_evidence_binding", {}),
        "context_graph": root.get("context_graph", {}),
        "typed_repair_obligations": root.get("typed_repair_obligations", []),
        "assumptions": root.get("assumptions", []),
        "derivation_steps": root.get("derivation_steps", []),
        "blockers": root.get("blockers", []),
        "assumption_branches": root.get("assumption_branches", []),
        "branch_ranking": root.get("branch_ranking", {}),
        "recursive_expansion_ranking": root.get("recursive_expansion_ranking", {}),
        "final_tree_digest": tree.get("final_tree_digest"),
        "tool_grounded_proposal_compiler": root.get("tool_grounded_proposal_compiler", {}),
        "document_ready_repair_proposals": root.get("document_ready_repair_proposals", []),
        "document_gap_reports": root.get("document_gap_reports", []),
        "document_partial_evidence_reports": root.get("document_partial_evidence_reports", []),
        "recursive_expansion": {
            "status": tree.get("recursive_expansion", {}).get("status"),
            "expanded_node_count": tree.get("recursive_expansion", {}).get("expanded_node_count", 0),
            "expanded_blocker_count": tree.get("recursive_expansion", {}).get("expanded_blocker_count", 0),
            "budget_exhausted": tree.get("recursive_expansion", {}).get("budget_exhausted", False),
            "budget": tree.get("recursive_expansion", {}).get("budget", {}),
            "validation_errors": tree.get("recursive_expansion", {}).get("validation_errors", []),
            "boundary": tree.get("recursive_expansion", {}).get("boundary", ""),
        },
        "patch_candidates": root.get("patch_candidates", []),
        "report_sections": _quarantine_report_sections(
            rendered,
            current_binding=current_binding,
        ),
    }


def _tool_use(tool: str, purpose: str, status: str, output_contract: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool": tool,
        "purpose": purpose,
        "status": status,
        "output_contract": output_contract,
        "arguments": arguments,
    }


def _source_ref_summary(refs: list[dict[str, Any]]) -> list[str]:
    summaries: list[str] = []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        file = ref.get("file")
        line_start = ref.get("line_start")
        line_end = ref.get("line_end")
        label = ref.get("label")
        parts = [str(item) for item in (file, label) if item]
        if line_start:
            line = f"line {line_start}"
            if line_end and line_end != line_start:
                line += f"-{line_end}"
            parts.append(line)
        if parts:
            summaries.append(" > ".join(parts))
    return list(dict.fromkeys(summaries))


def _render_document_ready_proposals(lines: list[str], proposals: list[dict[str, Any]]) -> None:
    lines.extend(["", "Document-ready repair proposals:"])
    if not proposals:
        lines.append("- None generated from the ranked branch evidence.")
        return
    for proposal in proposals:
        if not isinstance(proposal, dict):
            continue
        metadata = proposal.get("metadata") if isinstance(proposal.get("metadata"), dict) else {}
        ranking = proposal.get("ranking") if isinstance(proposal.get("ranking"), dict) else {}
        validation = proposal.get("validation") if isinstance(proposal.get("validation"), dict) else {}
        backend = proposal.get("backend_evidence") if isinstance(proposal.get("backend_evidence"), dict) else {}
        edit = proposal.get("proposed_edit") if isinstance(proposal.get("proposed_edit"), dict) else {}
        lines.append(f"- `{_md(proposal.get('id', 'proposal'))}`")
        lines.append(f"  - Contract: `{_md(metadata.get('contract', ''))}`")
        lines.append(f"  - Location: `{_md(proposal.get('location', ''))}`")
        lines.append(f"  - Context branch: `{_md(proposal.get('context_branch_id', ''))}`")
        lines.append(f"  - Context selection authority: `{_md(proposal.get('context_branch_selection_authority', ''))}`")
        lines.append(f"  - Nondominated branches: `{_md(proposal.get('nondominated_branch_ids', []))}`")
        if ranking:
            lines.append(f"  - Context branch outcome: `{_md(ranking.get('outcome', ''))}`")
        lines.append(f"  - Problem: {_md(proposal.get('problem', ''))}")
        lines.append(f"  - Why this is a derivation problem: {_md(proposal.get('why', ''))}")
        stated = proposal.get("already_stated_assumptions", [])
        if isinstance(stated, list) and stated:
            lines.append("  - Already stated or nearby stated assumptions:")
            for assumption in stated[:6]:
                if isinstance(assumption, dict):
                    lines.append(
                        f"    - `{_md(assumption.get('id', 'assumption'))}` "
                        f"status `{_md(assumption.get('status', ''))}`: {_md(assumption.get('text', ''))}"
                    )
        missing = proposal.get("missing_or_unresolved_assumptions", [])
        if isinstance(missing, list) and missing:
            lines.append("  - Missing or unresolved assumptions:")
            for assumption in missing[:8]:
                if isinstance(assumption, dict):
                    lines.append(
                        f"    - `{_md(assumption.get('id', 'assumption'))}` "
                        f"status `{_md(assumption.get('status', ''))}`: {_md(assumption.get('text', ''))}"
                    )
        proposed = proposal.get("proposed_assumptions", [])
        if isinstance(proposed, list) and proposed:
            lines.append("  - Proposed assumption set:")
            for assumption in proposed:
                lines.append(f"    - {_md(assumption)}")
        route = proposal.get("derivation_route_under_assumptions", [])
        if isinstance(route, list) and route:
            lines.append("  - Derivation route after adding assumptions:")
            for step in route[:6]:
                if isinstance(step, dict):
                    lines.append(f"    - {_md(step.get('step', 'step'))}: {_md(step.get('detail', ''))}")
        if edit:
            lines.append(f"  - Proposed edit placement: {_md(edit.get('placement', ''))}")
            lines.extend(["  - Proposed LaTeX:", "", "```tex", str(edit.get("latex", "")).strip(), "```"])
        blockers = proposal.get("remaining_blockers_before_certification", [])
        if isinstance(blockers, list) and blockers:
            lines.append("  - Remaining blockers before certification:")
            for blocker in blockers[:6]:
                if isinstance(blocker, dict):
                    lines.append(
                        f"    - `{_md(blocker.get('kind', 'blocker'))}`: "
                        f"{_md(blocker.get('problem', ''))} Required next evidence: "
                        f"{_md(blocker.get('required_next_evidence', ''))}"
                    )
        refs = _source_ref_summary(proposal.get("source_refs_for_missing_or_unresolved", []))
        if refs:
            lines.append(f"  - Source refs for missing/unresolved evidence: `{_md(refs)}`")
        lines.append(f"  - Backend evidence status: `{_md(backend.get('status', ''))}`")
        lines.append(f"  - Validation: `{_md(validation.get('status', ''))}` from `{_md(validation.get('source', ''))}`")
        lines.append(f"  - Non-claims: `{_md(proposal.get('non_claims', []))}`")


def _render_document_gap_reports(lines: list[str], reports: list[dict[str, Any]]) -> None:
    lines.extend(["", "Document gap reports:"])
    if not reports:
        lines.append("- None generated from the ranked branch evidence.")
        return
    for report in reports:
        if not isinstance(report, dict):
            continue
        metadata = report.get("metadata") if isinstance(report.get("metadata"), dict) else {}
        ranking = report.get("ranking") if isinstance(report.get("ranking"), dict) else {}
        validation = report.get("validation") if isinstance(report.get("validation"), dict) else {}
        backend = report.get("backend_evidence") if isinstance(report.get("backend_evidence"), dict) else {}
        blocked = report.get("candidate_edit_blocked") if isinstance(report.get("candidate_edit_blocked"), dict) else {}
        lines.append(f"- `{_md(report.get('id', 'gap_report'))}`")
        lines.append(f"  - Contract: `{_md(metadata.get('contract', ''))}`")
        lines.append(f"  - Closure status: `{_md(report.get('closure_status', ''))}`")
        lines.append(f"  - Location: `{_md(report.get('location', ''))}`")
        lines.append(f"  - Context branch: `{_md(report.get('context_branch_id', ''))}`")
        lines.append(f"  - Context selection authority: `{_md(report.get('context_branch_selection_authority', ''))}`")
        lines.append(f"  - Nondominated branches: `{_md(report.get('nondominated_branch_ids', []))}`")
        if ranking:
            lines.append(f"  - Context branch outcome: `{_md(ranking.get('outcome', ''))}`")
        lines.append(f"  - Problem: {_md(report.get('problem', ''))}")
        lines.append(f"  - Why this is a derivation problem: {_md(report.get('why', ''))}")
        missing = report.get("missing_or_unresolved_assumptions", [])
        if isinstance(missing, list) and missing:
            lines.append("  - Missing or unresolved assumptions:")
            for assumption in missing[:8]:
                if isinstance(assumption, dict):
                    lines.append(
                        f"    - `{_md(assumption.get('id', 'assumption'))}` "
                        f"status `{_md(assumption.get('status', ''))}`: {_md(assumption.get('text', ''))}"
                    )
        proposed = report.get("proposed_assumptions", [])
        if isinstance(proposed, list) and proposed:
            lines.append("  - Candidate assumption set that remains blocked:")
            for assumption in proposed:
                lines.append(f"    - {_md(assumption)}")
        route = report.get("derivation_route_under_assumptions", [])
        if isinstance(route, list) and route:
            lines.append("  - Candidate derivation route that remains blocked:")
            for step in route[:6]:
                if isinstance(step, dict):
                    lines.append(f"    - {_md(step.get('step', 'step'))}: {_md(step.get('detail', ''))}")
        blockers = report.get("remaining_blockers_before_certification", [])
        if isinstance(blockers, list) and blockers:
            lines.append("  - Exact blockers before this can become a repair proposal:")
            for blocker in blockers[:8]:
                if isinstance(blocker, dict):
                    lines.append(
                        f"    - `{_md(blocker.get('kind', 'blocker'))}`: "
                        f"{_md(blocker.get('problem', ''))} Required next evidence: "
                        f"{_md(blocker.get('required_next_evidence', ''))}"
                    )
        refs = _source_ref_summary(report.get("source_refs_for_missing_or_unresolved", []))
        if refs:
            lines.append(f"  - Source refs for missing/unresolved evidence: `{_md(refs)}`")
        if blocked:
            lines.append(f"  - Why no proposed edit is emitted: {_md(blocked.get('reason', ''))}")
        lines.append(f"  - Backend evidence status: `{_md(backend.get('status', ''))}`")
        lines.append(f"  - Validation: `{_md(validation.get('status', ''))}` from `{_md(validation.get('source', ''))}`")
        lines.append(f"  - Non-claims: `{_md(report.get('non_claims', []))}`")


def _render_document_partial_evidence_reports(lines: list[str], reports: list[dict[str, Any]]) -> None:
    lines.extend(["", "Document partial-evidence reports (non-repair):"])
    if not reports:
        lines.append("- None generated from the ranked branch evidence.")
        return
    for report in reports:
        if not isinstance(report, dict):
            continue
        blocked = report.get("candidate_edit_blocked") if isinstance(report.get("candidate_edit_blocked"), dict) else {}
        lines.append(f"- `{_md(report.get('id', 'partial_evidence'))}`")
        lines.append(f"  - Contract: `{_md(report.get('metadata', {}).get('contract', ''))}`")
        lines.append(f"  - Status: `{_md(report.get('status', ''))}`")
        lines.append(f"  - Publication mode: `{_md(report.get('publication_mode', ''))}`")
        lines.append(f"  - Closure status: `{_md(report.get('closure_status', ''))}`")
        lines.append(f"  - Failure classifications: `{_md(report.get('failure_classifications', []))}`")
        lines.append(f"  - Veto ids: `{_md(report.get('veto_ids', []))}`")
        lines.append(f"  - Problem: {_md(report.get('problem', ''))}")
        lines.append(f"  - Why: {_md(report.get('why', ''))}")
        missing = report.get("missing_or_unresolved_assumptions", [])
        if isinstance(missing, list) and missing:
            lines.append("  - Missing or unresolved assumptions retained:")
            for assumption in missing[:8]:
                if isinstance(assumption, dict):
                    lines.append(
                        f"    - `{_md(assumption.get('id', 'assumption'))}` "
                        f"status `{_md(assumption.get('status', ''))}`: {_md(assumption.get('text', ''))}"
                    )
        blockers = report.get("remaining_blockers_before_certification", [])
        if isinstance(blockers, list):
            for blocker in blockers[:8]:
                if isinstance(blocker, dict):
                    lines.append(
                        f"  - Blocker `{_md(blocker.get('kind', 'blocker'))}`: "
                        f"{_md(blocker.get('problem', ''))} Next: {_md(blocker.get('required_next_evidence', ''))}"
                    )
        if blocked:
            lines.append(f"  - Candidate text applicable: `{_md(blocked.get('applicable', False))}`")
            lines.append(f"  - Why candidate text is blocked: {_md(blocked.get('reason', ''))}")
        lines.append(f"  - Non-claims: `{_md(report.get('non_claims', []))}`")


def _render_tool_grounded_proposal_compiler(lines: list[str], compiler: dict[str, Any]) -> None:
    lines.extend(["", "Tool-grounded proposal compiler:"])
    if not isinstance(compiler, dict) or not compiler:
        lines.append("- No compiler result recorded.")
        return
    metadata = compiler.get("metadata") if isinstance(compiler.get("metadata"), dict) else {}
    lines.append(f"- Contract: `{_md(metadata.get('contract', ''))}`")
    lines.append(f"- Status: `{_md(compiler.get('status', ''))}`")
    lines.append(f"- Publication mode: `{_md(compiler.get('publication_mode', ''))}`")
    lines.append(f"- Grounding policy: `{_md(compiler.get('grounding_policy', ''))}`")
    lines.append(f"- Repair proposal count: `{_md(compiler.get('repair_proposal_count', 0))}`")
    lines.append(f"- Gap report count: `{_md(compiler.get('gap_report_count', 0))}`")
    lines.append(f"- Partial-evidence count: `{_md(compiler.get('partial_evidence_count', 0))}`")
    lines.append(f"- Boundary: {_md(compiler.get('boundary', ''))}")
    items = compiler.get("compiled_items", [])
    if isinstance(items, list) and items:
        lines.append("- Compiled items:")
        for item in items:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"  - `{_md(item.get('id', 'item'))}` type `{_md(item.get('type', ''))}`, "
                f"closure `{_md(item.get('closure_status', ''))}`, "
                f"publishable_as_repair=`{_md(item.get('publishable_as_repair', False))}`, "
                f"publishable_as_gap_report=`{_md(item.get('publishable_as_gap_report', False))}`, "
                f"reportable_as_partial_evidence=`{_md(item.get('reportable_as_partial_evidence', False))}`"
            )
            lines.append(f"    - Failure classifications: `{_md(item.get('failure_classifications', []))}`")
            lines.append(f"    - Veto ids: `{_md(item.get('veto_ids', []))}`")
            lines.append(f"    - Evidence refs: `{_md(item.get('evidence_refs', []))}`")
            lines.append(f"    - Remaining blocker ids: `{_md(item.get('remaining_blocker_ids', []))}`")
            if item.get("validation_errors"):
                lines.append(f"    - Validation errors: `{_md(item.get('validation_errors', []))}`")
    else:
        lines.append("- No compiled items.")
    errors = compiler.get("validation_errors", [])
    if isinstance(errors, list) and errors:
        lines.append(f"- Compiler validation errors: `{_md(errors)}`")


def _context_packets_for_missing_focus(
    path: Path,
    focus_labels: list[str] | None,
    selected_rows: list[dict[str, Any]],
    *,
    index: dict[str, Any],
) -> list[dict[str, Any]]:
    if not focus_labels:
        return []
    selected_labels = {str(row.get("label")) for row in selected_rows if row.get("label")}
    missing = [label for label in focus_labels if label not in selected_labels]
    if not missing:
        return []
    packets: list[dict[str, Any]] = []
    for label in missing:
        result = build_proposition_context_packet(index, label)
        packet = result.get("context_packet") if isinstance(result, dict) else None
        if isinstance(packet, dict) and result.get("status") == "context_packet_ready":
            packet = dict(packet)
            packet["source_contract"] = result.get("metadata", {}).get("contract")
            packet["context_graph"] = build_local_context_graph(packet)
            packet["typed_repair_obligation"] = typed_repair_obligation_from_packet(packet)
            packets.append(packet)
    return packets


def _target_failure_result(row: dict[str, Any], exc: Exception, *, index: int) -> dict[str, Any]:
    label = row.get("label")
    row_id = row.get("id")
    blocker = {
        "id": f"blocker_parallel_target_{index}_worker_exception",
        "kind": "target_worker_exception",
        "failure_classification": "engineering_error",
        "problem": "A target worker failed before producing a derivation-tree result.",
        "why": f"{type(exc).__name__}: {exc}",
        "required_next_evidence": "Rerun this target in serial mode or inspect the exception before treating the target as audited.",
        "source": "document_derivation_tree_parallel_executor",
        "evidence_refs": [str(row_id or label or index)],
    }
    return {
        **_legacy_document_integrity_binding(),
        "label": label,
        "row_id": row_id,
        "row_index": row.get("row_index"),
        "location": str(row.get("file", "")),
        "claim_type": "worker_failure",
        "status": "blocked",
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classification": "engineering_error",
        "failure_classifications": ["engineering_error"],
        "veto_ids": ["target_worker_exception", DOCUMENT_PUBLICATION_VETO_ID],
        "promotion": _effective_document_promotion(),
        "semantic_work_packet": {},
        "tree": {
            **_legacy_document_integrity_binding(),
            "status": "blocked",
            "publication_mode": DOCUMENT_PUBLICATION_MODE,
            "failure_classifications": ["engineering_error"],
            "veto_ids": ["target_worker_exception", DOCUMENT_PUBLICATION_VETO_ID],
            "summary": {"node_count": 0},
            "controller": {
                "status": "blocked",
                "reason": "Target worker failed before target audit completed.",
                "promotion": _effective_document_promotion(),
                "validation_errors": ["target worker failed"],
            },
            "backend_attempts": [],
            "context_graph": {},
            "typed_repair_obligations": [],
            "assumptions": [],
            "derivation_steps": [],
            "blockers": [blocker],
            "assumption_branches": [],
            "branch_ranking": {},
            "tool_grounded_proposal_compiler": attach_contract(
                {
                    **_legacy_document_integrity_binding(),
                    "status": "no_publishable_items",
                    "publication_mode": DOCUMENT_PUBLICATION_MODE,
                    "publication_veto_ids": [DOCUMENT_PUBLICATION_VETO_ID, "target_worker_exception"],
                    "grounding_policy": STRICT_GROUNDING_POLICY,
                    "target_label": label,
                    "repair_proposal_count": 0,
                    "gap_report_count": 0,
                    "partial_evidence_count": 0,
                    "blocked_candidate_count": 0,
                    "document_ready_repair_proposals": [],
                    "document_gap_reports": [],
                    "document_partial_evidence_reports": [],
                    "compiled_items": [],
                    "validation_errors": [{"id": blocker["id"], "type": "worker_failure", "errors": [blocker["why"]]}],
                    "boundary": "Parallel worker failures are blockers, not refutations or repairs.",
                    "non_claims": ["A parallel worker failure does not audit or refute the target."],
                },
                TOOL_GROUNDED_PROPOSAL_COMPILER_CONTRACT,
            ),
            "document_ready_repair_proposals": [],
            "document_gap_reports": [],
            "document_partial_evidence_reports": [],
            "recursive_expansion": {},
            "patch_candidates": [],
            "report_sections": [],
        },
    }


def _target_result_for_row(
    row: dict[str, Any],
    *,
    path: Path,
    sections: list[dict[str, Any]],
    rows_by_label: dict[str, list[dict[str, Any]]],
    rows_by_environment: dict[str, list[dict[str, Any]]],
    latex_index: dict[str, Any],
    displays: list[dict[str, Any]],
    budget_profile: str,
    max_attempts: int,
    capabilities: dict[str, Any],
    integrations: dict[str, Any],
) -> dict[str, Any]:
    label = str(row.get("label", ""))
    paragraph_context = (
        extract_paragraph_context_for_label(latex_index, label, before=1, after=1)
        if label
        else None
    )
    if isinstance(row.get("label_scoped_obligation"), dict):
        packet = _semantic_packet_from_label_scoped_target(
            row,
            tex_path=path,
            sections=sections,
            paragraph_context=paragraph_context,
        )
    else:
        packet = _semantic_packet(
            row,
            tex_path=path,
            sections=sections,
            rows_for_label=rows_by_label.get(label, [row]),
            rows_for_environment=rows_by_environment.get(str(row.get("environment_id", "")), [row]),
            paragraph_context=paragraph_context,
            display=_display_for_row(row, displays),
        )
    tree = can_derive_with_budget(
        packet["target"],
        lhs=packet.get("lhs"),
        rhs=packet.get("rhs"),
        budget_profile=budget_profile,
        max_attempts=max_attempts,
        capabilities=capabilities,
        integrations=integrations,
    )
    _augment_tree(tree, packet, source_path=path)
    rendered = render_derivation_tree_report(tree)
    raw_promotion = tree.get("controller", {}).get("promotion", {})
    compact_tree = _compact_tree(tree, rendered)
    classifications = list(compact_tree.get("failure_classifications", []))
    if any(
        str(attempt.get("status", "")).endswith("error")
        for attempt in compact_tree.get("backend_attempts", [])
        if isinstance(attempt, dict)
    ) and "engineering_error" not in classifications:
        classifications.append("engineering_error")
    return {
        **_integrity_from(compact_tree),
        "label": packet.get("label"),
        "row_id": packet.get("row_id"),
        "row_index": row.get("row_index"),
        "obligation_id": packet.get("obligation_id"),
        "obligation_digest": packet.get("obligation_digest"),
        "location": packet["location"],
        "claim_type": packet["claim_type"],
        "status": compact_tree.get("status"),
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classifications": classifications,
        "veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "promotion": _effective_document_promotion(
            raw_promotion,
            current_binding=compact_tree.get("integrity_binding_verified") is True,
        ),
        "semantic_work_packet": packet,
        "tree": compact_tree,
    }


def _ordered_target_results(
    selected_rows: list[dict[str, Any]],
    *,
    path: Path,
    sections: list[dict[str, Any]],
    rows_by_label: dict[str, list[dict[str, Any]]],
    rows_by_environment: dict[str, list[dict[str, Any]]],
    latex_index: dict[str, Any],
    displays: list[dict[str, Any]],
    budget_profile: str,
    max_attempts: int,
    capabilities: dict[str, Any],
    integrations: dict[str, Any],
    workers: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    normalized_workers = max(1, int(workers or 1))
    execution = {
        "mode": "serial" if normalized_workers == 1 or len(selected_rows) <= 1 else "parallel",
        "workers_requested": workers,
        "workers_used": 1,
        "target_count": len(selected_rows),
        "failure_count": 0,
        "failures": [],
        "deterministic_order": "validated selected-target order",
        "boundary": "Parallel execution changes scheduling only; logical output is restored to selected-target order.",
    }
    if execution["mode"] == "serial":
        results: list[tuple[int, dict[str, Any]]] = []
        for index, row in enumerate(selected_rows):
            try:
                target = _target_result_for_row(
                    row,
                    path=path,
                    sections=sections,
                    rows_by_label=rows_by_label,
                    rows_by_environment=rows_by_environment,
                    latex_index=latex_index,
                    displays=displays,
                    budget_profile=budget_profile,
                    max_attempts=max_attempts,
                    capabilities=capabilities,
                    integrations=integrations,
                )
            except Exception as exc:  # pragma: no cover - serial failure guard mirrors parallel path.
                target = _target_failure_result(row, exc, index=index)
                execution["failure_count"] += 1
                execution["failures"].append({"index": index, "label": row.get("label"), "error": f"{type(exc).__name__}: {exc}"})
            results.append((index, target))
        return [target for _, target in results], attach_contract(execution, PARALLEL_EXECUTION_CONTRACT)

    execution["workers_used"] = min(normalized_workers, len(selected_rows))
    results = []
    with ThreadPoolExecutor(max_workers=execution["workers_used"]) as executor:
        future_to_item = {
            executor.submit(
                _target_result_for_row,
                row,
                path=path,
                sections=sections,
                rows_by_label=rows_by_label,
                rows_by_environment=rows_by_environment,
                latex_index=latex_index,
                displays=displays,
                budget_profile=budget_profile,
                max_attempts=max_attempts,
                capabilities=capabilities,
                integrations=integrations,
            ): (index, row)
            for index, row in enumerate(selected_rows)
        }
        for future in as_completed(future_to_item):
            index, row = future_to_item[future]
            try:
                target = future.result()
            except Exception as exc:  # pragma: no cover - protects deterministic parent behavior.
                target = _target_failure_result(row, exc, index=index)
                execution["failure_count"] += 1
                execution["failures"].append({"index": index, "label": row.get("label"), "error": f"{type(exc).__name__}: {exc}"})
            results.append((index, target))
    results.sort(key=lambda item: item[0])
    return [target for _, target in results], attach_contract(execution, PARALLEL_EXECUTION_CONTRACT)


def _disabled_document_derivation_tree_result(tex_path: str | Path) -> dict[str, Any]:
    result = {
        **_legacy_document_integrity_binding(),
        "status": DOCUMENT_TOOL_DISABLED_STATUS,
        "tex_path": str(tex_path),
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "failure_classification": "engineering_error",
        "failure_classifications": ["engineering_error"],
        "veto_ids": [DOCUMENT_TOOL_DISABLED_STATUS, DOCUMENT_PUBLICATION_VETO_ID],
        "promotion": _effective_document_promotion(),
        "execution": attach_contract(
            {
                "mode": "disabled",
                "workers_requested": 0,
                "workers_used": 0,
                "target_count": 0,
                "failure_count": 0,
                "failures": [],
                "pipeline_entered": False,
                "boundary": "The emergency kill switch returned before source access or pipeline execution.",
            },
            PARALLEL_EXECUTION_CONTRACT,
        ),
        "coverage": {
            "status": "not_run_tool_disabled",
            "promoted_count": 0,
            "raw_promoted_count": 0,
            "document_ready_repair_proposal_count": 0,
            "document_gap_report_count": 0,
            "document_partial_evidence_report_count": 0,
            "tool_grounded_compiler_validation_error_count": 0,
            "semantic_packet_count": 0,
        },
        "tool_uses": [],
        "targets": [],
        "context_targets": [],
        "non_claims": [
            {
                "code": "tool_disabled_not_audit",
                "text": "The document derivation-tree tool is disabled; this response does not inspect or audit the source.",
            }
        ],
    }
    result = attach_contract(result, DOCUMENT_DERIVATION_TREE_CONTRACT)
    result["markdown"] = (
        "# Document Derivation Tree Audit\n\n"
        f"Status: `{DOCUMENT_TOOL_DISABLED_STATUS}`\n\n"
        f"Publication mode: `{DOCUMENT_PUBLICATION_MODE}`\n\n"
        "Failure classification: `engineering_error`\n\n"
        "The emergency kill switch returned before source access or pipeline execution.\n"
    )
    return result


def extract_document_derivation_obligations(
    tex_path: str | Path,
    *,
    focus_labels: list[str] | tuple[str, ...] | str,
) -> dict[str, Any]:
    """Expose validated obligations without entering semantic/backend work."""
    path = Path(tex_path).resolve()
    label_list = [focus_labels] if isinstance(focus_labels, str) else list(focus_labels)
    index = build_index(path.parent)
    label_results = [
        extract_derivation_targets_for_label(index, str(label), file=path.name)
        for label in label_list
    ]
    obligations = [
        obligation
        for result in label_results
        for obligation in result.get("obligations", [])
        if isinstance(obligation, dict)
    ]
    targets = [
        target
        for result in label_results
        for target in result.get("targets", [])
        if isinstance(target, dict) and target.get("adapter_eligible") is True
    ]
    blocked = [result for result in label_results if result.get("status") != "extracted"]
    return {
        "schema_version": "p02_document_extraction_boundary@1",
        "status": "extracted" if obligations and not blocked else "quarantined" if blocked else "not_extracted",
        "tex_path": str(path),
        "requested_labels": label_list,
        "label_results": label_results,
        "obligations": obligations,
        "targets": targets,
        "obligation_count": len(obligations),
        "adapter_eligible_target_count": len(targets),
        "backend_request_count": 0,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "publication_enabled": DOCUMENT_PUBLICATION_ENABLED,
        "claim_eligibility": DOCUMENT_CLAIM_ELIGIBILITY,
        "non_claims": [
            "Extraction establishes source ownership only; it does not prove, refute, route, or repair an obligation.",
            "Publication remains disabled and no mathematical backend was requested.",
        ],
    }


def audit_document_derivation_tree(
    tex_path: str | Path,
    *,
    output_md: str | Path | None = None,
    output_json: str | Path | None = None,
    focus_labels: list[str] | None = None,
    max_labels: int | None = DEFAULT_LABEL_LIMIT,
    budget_profile: str = "standard",
    max_attempts: int = 3,
    backend_env: str = "mathdevmcp-backends",
    search_mode: str = "agent_guided",
    grounding_policy: str = STRICT_GROUNDING_POLICY,
    workers: int = 1,
) -> dict[str, Any]:
    """Run the generic semantic-packet -> tree-controller document workflow."""
    if _document_tool_disabled():
        return _disabled_document_derivation_tree_result(tex_path)
    if search_mode not in {"agent_guided"}:
        raise ValueError("search_mode must be 'agent_guided'")
    if grounding_policy != STRICT_GROUNDING_POLICY:
        raise ValueError("grounding_policy must be 'strict'")
    path = Path(tex_path)
    text = path.read_text(encoding="utf-8")
    sections = _section_map(text)
    rows = locate_equations_in_file(path, root=path.parent)
    displays = _display_index(path, text, root=path.parent)
    latex_index = build_index(path.parent)
    selected_rows, target_extraction = _select_label_scoped_targets(
        path,
        rows,
        focus_labels=focus_labels,
        max_labels=max_labels,
        index=latex_index,
    )
    context_targets = _context_packets_for_missing_focus(path, focus_labels, selected_rows, index=latex_index)
    rows_by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows_by_environment: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("label"):
            rows_by_label[str(row["label"])].append(row)
        if row.get("environment_id"):
            rows_by_environment[str(row["environment_id"])].append(row)
    with _backend_env_scope(backend_env):
        doctor = doctor_report()
        capabilities = doctor.get("capabilities", {})
        integrations = doctor.get("integrations", {})

    target_results, execution = _ordered_target_results(
        selected_rows,
        path=path,
        sections=sections,
        rows_by_label=rows_by_label,
        rows_by_environment=rows_by_environment,
        latex_index=latex_index,
        displays=displays,
        budget_profile=budget_profile,
        max_attempts=max_attempts,
        capabilities=capabilities,
        integrations=integrations,
        workers=workers,
    )

    context_labels = {str(packet.get("label")) for packet in context_targets if packet.get("label")}
    context_graphs = [
        packet.get("context_graph")
        for packet in context_targets
        if isinstance(packet.get("context_graph"), dict)
    ] + [
        item.get("semantic_work_packet", {}).get("context_graph")
        for item in target_results
        if isinstance(item.get("semantic_work_packet", {}).get("context_graph"), dict)
    ]
    context_graph_status_counts: dict[str, int] = {}
    for graph in context_graphs:
        if not isinstance(graph, dict):
            continue
        for status, count in graph.get("status_counts", {}).items():
            context_graph_status_counts[str(status)] = context_graph_status_counts.get(str(status), 0) + int(count)
    typed_obligations = [
        packet.get("typed_repair_obligation")
        for packet in context_targets
        if isinstance(packet.get("typed_repair_obligation"), dict)
    ] + [
        item.get("semantic_work_packet", {}).get("typed_repair_obligation")
        for item in target_results
        if isinstance(item.get("semantic_work_packet", {}).get("typed_repair_obligation"), dict)
    ]
    typed_obligation_status_counts: dict[str, int] = {}
    for obligation in typed_obligations:
        if not isinstance(obligation, dict):
            continue
        status = str(obligation.get("diagnostic_status", "unknown"))
        typed_obligation_status_counts[status] = typed_obligation_status_counts.get(status, 0) + 1
    raw_promoted_count = sum(
        1
        for item in target_results
        if branch_promotion_report(
            {
                "status": str(item.get("tree", {}).get("controller", {}).get("raw_status", "partial")),
                "backend_attempts": [
                    attempt
                    for attempt in item.get("tree", {}).get("backend_attempts", [])
                    if isinstance(attempt, dict)
                ],
            }
        ).get("can_promote")
        is True
    )
    failure_classification_counts: dict[str, int] = {}
    for item in target_results:
        for classification in item.get("failure_classifications", []):
            key = str(classification)
            failure_classification_counts[key] = failure_classification_counts.get(key, 0) + 1
    coverage = {
        "status": "partial_coverage",
        "target_file_only": True,
        "selected_rows": len(selected_rows),
        "available_labeled_rows": len([row for row in rows if row.get("label")]),
        "available_equation_rows": len(rows),
        "missing_focus_labels": [
            label
            for label in focus_labels or []
            if not any(row.get("label") == label for row in selected_rows) and label not in context_labels
        ],
        "context_target_count": len(context_targets),
        "context_target_labels": sorted(context_labels),
        "context_graph_count": len(context_graphs),
        "context_graph_status_counts": context_graph_status_counts,
        "typed_repair_obligation_count": len(typed_obligations),
        "typed_repair_obligation_status_counts": typed_obligation_status_counts,
        "ranked_branch_count": sum(
            int(item["tree"].get("branch_ranking", {}).get("branch_count", 0))
            for item in target_results
        ),
        "promoted_count": 0,
        "raw_promoted_count": raw_promoted_count,
        "failure_classification_counts": failure_classification_counts,
        "blocker_count": sum(len(item["tree"].get("blockers", [])) for item in target_results),
        "document_ready_repair_proposal_count": sum(
            len(item["tree"].get("document_ready_repair_proposals", []))
            for item in target_results
        ),
        "document_gap_report_count": sum(
            len(item["tree"].get("document_gap_reports", []))
            for item in target_results
        ),
        "document_partial_evidence_report_count": sum(
            len(item["tree"].get("document_partial_evidence_reports", []))
            for item in target_results
        ),
        "tool_grounded_compiler_status_counts": {},
        "tool_grounded_compiler_validation_error_count": 0,
        "semantic_packet_count": len(target_results),
    }
    for item in target_results:
        compiler = item["tree"].get("tool_grounded_proposal_compiler", {})
        if not isinstance(compiler, dict):
            continue
        status = str(compiler.get("status", "unknown"))
        coverage["tool_grounded_compiler_status_counts"][status] = (
            coverage["tool_grounded_compiler_status_counts"].get(status, 0) + 1
        )
        errors = compiler.get("validation_errors", [])
        coverage["tool_grounded_compiler_validation_error_count"] += (
            len(errors) if isinstance(errors, list) else 0
        )
    current_targets = [
        item
        for item in target_results
        if item.get("evidence_schema_version") == "1.0"
        and item.get("integrity_binding_verified") is True
    ]
    aggregate_integrity = (
        {
            "evidence_schema_version": "1.0",
            "integrity_binding_status": "verified_current_evidence",
            "integrity_binding_verified": True,
            "claim_eligibility": DOCUMENT_CLAIM_ELIGIBILITY,
            "publication_enabled": DOCUMENT_PUBLICATION_ENABLED,
            "document_evidence_binding_refs": [
                item.get("document_evidence_binding_ref", {}) for item in current_targets
            ],
        }
        if target_results and len(current_targets) == len(target_results)
        else _legacy_document_integrity_binding()
    )
    result = {
        **aggregate_integrity,
        "tex_path": str(path),
        "backend_env": backend_env,
        "search_mode": search_mode,
        "grounding_policy": grounding_policy,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "publication_veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "veto_ids": [DOCUMENT_PUBLICATION_VETO_ID],
        "failure_classifications": sorted(failure_classification_counts),
        "promotion": _effective_document_promotion(
            current_binding=aggregate_integrity.get("integrity_binding_verified") is True,
        ),
        "execution": execution,
        "document_inventory": {
            "line_count": len(text.splitlines()),
            "section_count": len(sections),
            "equation_localization": summarize_equation_localization(rows),
            "label_ref_hygiene": _label_ref_hygiene(text),
        },
        "coverage": coverage,
        "target_extraction": target_extraction,
        "tool_uses": [
            _tool_use(
                "locate_equations_in_file",
                "Localize source rows in the exact target file.",
                "completed",
                "equation_rows",
                {"tex_path": str(path), "root": str(path.parent)},
            ),
            _tool_use(
                "extract_derivation_targets_for_label",
                "Bind each selected equation label to one complete validated source-owned obligation.",
                "completed" if target_extraction["failure_count"] == 0 else "quarantined",
                "derivation_target_extraction_result",
                {
                    "requested_equation_labels": target_extraction["requested_equation_labels"],
                    "selected_target_count": target_extraction["selected_target_count"],
                    "failure_count": target_extraction["failure_count"],
                    "fallback_to_locator_row": False,
                },
            ),
            _tool_use(
                "build_proposition_context_packet",
                "Localize proposition labels that are not display-equation rows and attach equation targets/context.",
                "completed" if context_targets else "not_needed",
                "proposition_context_packet_result",
                {"context_target_count": len(context_targets), "focus_labels": focus_labels or []},
            ),
            _tool_use(
                "build_semantic_work_packet",
                "Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes.",
                "completed",
                "semantic_work_packet",
                {"selected_rows": len(selected_rows)},
            ),
            _tool_use(
                "assumptions_required",
                "Detect route-required assumptions before backend proof attempts.",
                "completed",
                "assumption_discovery_result",
                {"selected_rows": len(selected_rows)},
            ),
            _tool_use(
                "build_local_context_graph",
                "Classify local source evidence as stated, nearby stated, inferred, missing, or unresolved before proposing repairs.",
                "completed" if context_graphs else "not_needed",
                "local_context_graph",
                {
                    "context_graph_count": len(context_graphs),
                    "status_counts": context_graph_status_counts,
                },
            ),
            _tool_use(
                "typed_repair_obligation_from_packet",
                "Convert context graph and semantic packet evidence into typed repair obligations before branch/report generation.",
                "completed" if typed_obligations else "not_needed",
                "typed_repair_obligation",
                {
                    "typed_repair_obligation_count": len(typed_obligations),
                    "status_counts": typed_obligation_status_counts,
                },
            ),
            _tool_use(
                "doctor_report",
                "Record external backend capability provenance.",
                "available" if doctor.get("ok") else "diagnostic",
                "doctor_report",
                {"backend_env": backend_env},
            ),
            _tool_use(
                "can_derive_with_budget",
                "Run the external-tool-first branch controller on semantic packet targets.",
                "completed",
                "derivation_search_tree_result",
                {
                    "budget_profile": budget_profile,
                    "max_attempts": max_attempts,
                    "selected_rows": len(selected_rows),
                    "execution_mode": execution["mode"],
                    "workers_used": execution["workers_used"],
                },
            ),
            _tool_use(
                "rank_repair_branches",
                "Rank assumption branches by recorded backend evidence, blocker specificity, source support, closure strength, and non-minimality.",
                "completed",
                "repair_branch_ranking_result",
                {"ranked_branch_count": coverage["ranked_branch_count"]},
            ),
            _tool_use(
                "tool_grounded_proposal_compiler",
                "Quarantine repair publication, compile legacy closure as partial evidence, and keep blocked branches as exact gap reports.",
                "completed" if coverage["tool_grounded_compiler_validation_error_count"] == 0 else "validation_error",
                TOOL_GROUNDED_PROPOSAL_COMPILER_CONTRACT,
                {
                    "grounding_policy": STRICT_GROUNDING_POLICY,
                    "search_mode": search_mode,
                    "repair_proposal_count": coverage["document_ready_repair_proposal_count"],
                    "gap_report_count": coverage["document_gap_report_count"],
                    "partial_evidence_count": coverage["document_partial_evidence_report_count"],
                    "validation_error_count": coverage["tool_grounded_compiler_validation_error_count"],
                },
            ),
            _tool_use(
                "render_derivation_tree_report",
                "Render each derivation tree into structured evidence sections.",
                "completed",
                "derivation_tree_report_result",
                {"rendered_trees": len(target_results)},
            ),
        ],
        "backend_provenance": {
            "doctor": doctor,
            "certification_boundary": (
                "Current evidence identity is replayable, but scoped backend evidence remains diagnostic at the "
                "document boundary because identity binding does not establish mathematical closure, scientific "
                "validity, claim eligibility, or publication authority."
                if aggregate_integrity.get("integrity_binding_verified") is True
                else "Raw scoped backend evidence remains diagnostic at the document boundary until exact Phase 01 binding exists."
            ),
        },
        "targets": target_results,
        "context_targets": context_targets,
        "non_claims": [
            {
                "code": "document_tree_audit_not_document_proof",
                "text": "This workflow is a semantic gap and tree-evidence report; it does not prove the whole document.",
            },
            {
                "code": "semantic_packets_not_certificates",
                "text": "Missing obligations, assumption sets, and derivation routes are deterministic guidance, not proof certificates.",
            },
            {
                "code": "proof_search_not_final_certificate",
                "text": "LeanDojo, Pantograph, retrieval, route plans, and static extraction are diagnostic until direct Lean or another certifying backend checks the scoped target.",
            },
            {
                "code": "document_repair_publication_quarantined",
                "text": "No returned candidate is an applicable document edit while publication mode is disabled.",
            },
        ],
    }
    result = attach_contract(result, DOCUMENT_DERIVATION_TREE_CONTRACT)
    markdown = render_document_derivation_tree_markdown(result)
    result["markdown"] = markdown
    if output_md is not None:
        Path(output_md).write_text(markdown, encoding="utf-8")
        result["output_md"] = str(output_md)
    if output_json is not None:
        serializable = dict(result)
        serializable.pop("markdown", None)
        Path(output_json).write_text(json.dumps(serializable, indent=2, sort_keys=True), encoding="utf-8")
        result["output_json"] = str(output_json)
    return result


def render_document_derivation_tree_markdown(result: dict[str, Any]) -> str:
    """Render an agent-consumable generic document tree audit."""
    lines = [
        "# Document Derivation Tree Audit",
        "",
        f"Target: `{result.get('tex_path', '')}`",
        f"Search mode: `{_md(result.get('search_mode', ''))}`",
        f"Grounding policy: `{_md(result.get('grounding_policy', ''))}`",
        f"Publication mode: `{_md(result.get('publication_mode', ''))}`",
        f"Execution: `{_md(result.get('execution', {}).get('mode', ''))}` with `{_md(result.get('execution', {}).get('workers_used', 1))}` worker(s)",
        "",
        "## Executive Summary",
        "",
        f"- Selected source rows: `{result.get('coverage', {}).get('selected_rows', 0)}`",
        f"- Semantic packets: `{result.get('coverage', {}).get('semantic_packet_count', 0)}`",
        f"- Proposition/context packets: `{result.get('coverage', {}).get('context_target_count', 0)}`",
        f"- Context graphs: `{result.get('coverage', {}).get('context_graph_count', 0)}`",
        f"- Context graph statuses: `{_md(result.get('coverage', {}).get('context_graph_status_counts', {}))}`",
        f"- Typed repair obligations: `{result.get('coverage', {}).get('typed_repair_obligation_count', 0)}`",
        f"- Typed repair obligation statuses: `{_md(result.get('coverage', {}).get('typed_repair_obligation_status_counts', {}))}`",
        f"- Ranked branches: `{result.get('coverage', {}).get('ranked_branch_count', 0)}`",
        f"- Effective promoted branches: `{result.get('coverage', {}).get('promoted_count', 0)}`",
        f"- Raw promoted branches (diagnostic only): `{result.get('coverage', {}).get('raw_promoted_count', 0)}`",
        f"- Document-ready repair proposals: `{result.get('coverage', {}).get('document_ready_repair_proposal_count', 0)}`",
        f"- Document gap reports: `{result.get('coverage', {}).get('document_gap_report_count', 0)}`",
        f"- Document partial-evidence reports: `{result.get('coverage', {}).get('document_partial_evidence_report_count', 0)}`",
        f"- Failure classifications: `{_md(result.get('coverage', {}).get('failure_classification_counts', {}))}`",
        f"- Tool-grounded compiler statuses: `{_md(result.get('coverage', {}).get('tool_grounded_compiler_status_counts', {}))}`",
        f"- Tool-grounded compiler validation errors: `{result.get('coverage', {}).get('tool_grounded_compiler_validation_error_count', 0)}`",
        f"- Parallel execution failures: `{_md(result.get('execution', {}).get('failure_count', 0))}`",
        f"- Blockers: `{result.get('coverage', {}).get('blocker_count', 0)}`",
        f"- Missing focus labels: `{_md(result.get('coverage', {}).get('missing_focus_labels', []))}`",
        "- This report is generic and document-local; it is not tied to a card-NPV-specific plan.",
        "",
        "## Tools Used",
        "",
        "| Tool | Purpose | Status | Contract | Arguments |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in result.get("tool_uses", []):
        lines.append(
            f"| `{_md(item.get('tool', ''))}` | {_md(item.get('purpose', ''))} | `{_md(item.get('status', ''))}` | `{_md(item.get('output_contract', ''))}` | `{_md(json.dumps(item.get('arguments', {}), sort_keys=True))}` |"
        )
    context_targets = result.get("context_targets", [])
    if context_targets:
        lines.extend(["", "## Proposition/Context Packets", ""])
        for packet in context_targets:
            lines.extend(
                [
                    f"### `{_md(packet.get('label', 'context'))}`",
                    "",
                    f"- Kind: `{_md(packet.get('kind', ''))}`",
                    f"- Location: `{_md(packet.get('file', ''))}:{_md(packet.get('line_start', ''))}-{_md(packet.get('line_end', ''))}`",
                    f"- Section path: `{_md(packet.get('section_path', []))}`",
                    f"- Equation targets: `{_md([target.get('label') for target in packet.get('equation_targets', []) if isinstance(target, dict)])}`",
                    f"- Hypotheses: `{_md(packet.get('hypotheses', []))}`",
                    f"- Non-claim: {_md(packet.get('non_claim', ''))}",
                    "",
                    "Source proposition:",
                    "",
                    "```tex",
                    str(packet.get("source_text", "")).strip(),
                    "```",
                    "",
                ]
            )
            graph = packet.get("context_graph")
            if isinstance(graph, dict):
                lines.extend(
                    [
                        "Local context graph:",
                        "",
                        f"- Status counts: `{_md(graph.get('status_counts', {}))}`",
                    ]
                )
                for node in graph.get("nodes", []):
                    if not isinstance(node, dict):
                        continue
                    if node.get("kind") not in {"candidate_assumption", "definition", "notation_declaration"}:
                        continue
                    refs = [
                        f"{ref.get('file')}:{ref.get('line_start')}-{ref.get('line_end')}"
                        for ref in node.get("source_refs", [])
                        if isinstance(ref, dict)
                    ]
                    lines.append(f"- `{_md(node.get('id', 'node'))}` status `{_md(node.get('status', ''))}`")
                    lines.append(f"  - Role: {_md(node.get('mathematical_role', ''))}")
                    lines.append(f"  - What: {_md(node.get('summary', ''))}")
                    lines.append(f"  - Why status: {_md(node.get('why_status', ''))}")
                    lines.append(f"  - Required next evidence: {_md(node.get('required_next_evidence', ''))}")
                    lines.append(f"  - Source refs: `{_md(refs)}`")
                lines.append("")
            typed = packet.get("typed_repair_obligation")
            if isinstance(typed, dict):
                lines.extend(
                    [
                        "Typed repair obligation:",
                        "",
                        f"- ID: `{_md(typed.get('id', ''))}`",
                        f"- Diagnostic status: `{_md(typed.get('diagnostic_status', ''))}`",
                        f"- Unresolved constructs: `{_md(typed.get('unresolved_constructs', []))}`",
                        f"- Encodability: `{_md(typed.get('encodability', {}))}`",
                        f"- Route hints: `{_md(typed.get('route_hints', []))}`",
                        f"- Boundary: {_md(typed.get('certification_boundary', ''))}",
                        "",
                    ]
                )
    lines.extend(["", "## Target Packets And Trees", ""])
    for index, target in enumerate(result.get("targets", []), start=1):
        packet = target.get("semantic_work_packet", {})
        tree = target.get("tree", {})
        promotion = target.get("promotion", {})
        lines.extend(
            [
                f"### {index}. `{_md(target.get('label', target.get('row_id', 'target')))}`",
                "",
                f"- Location: `{_md(target.get('location', ''))}`",
                f"- Claim type: `{_md(target.get('claim_type', ''))}`",
                f"- Tree status: `{_md(target.get('status', ''))}`",
                f"- Promotion guard: `can_promote={_md(promotion.get('can_promote', False))}`",
                f"- Semantic domains: `{_md(packet.get('semantic_domains', []))}`",
                f"- Extraction uncertainty: `{_md(packet.get('uncertainty', []))}`",
                f"- Full display span: `{_md(packet.get('display_source_span', {}))}`",
                f"- Operators: `{_md(packet.get('operator_inventory', []))}`",
                f"- Symbols: `{_md(packet.get('symbol_inventory', {}))}`",
                f"- Context graph statuses: `{_md(packet.get('context_graph', {}).get('status_counts', {}))}`",
                f"- Typed repair obligation: `{_md(packet.get('typed_repair_obligation', {}).get('id', ''))}`",
                f"- Typed obligation status: `{_md(packet.get('typed_repair_obligation', {}).get('diagnostic_status', ''))}`",
                f"- Typed unresolved constructs: `{_md(packet.get('typed_repair_obligation', {}).get('unresolved_constructs', []))}`",
                "",
                "Source row target:",
                "",
                "```tex",
                str(packet.get("source_text", "")).strip(),
                "```",
                "",
                "Full display target:",
                "",
                "```tex",
                str(packet.get("full_display_source", "")).strip() or "(full display source not reconstructed)",
                "```",
                "",
                "Mathematically missing obligations:",
            ]
        )
        obligations = packet.get("missing_obligations", [])
        if obligations:
            for obligation in obligations:
                lines.append(
                    f"- `{_md(obligation.get('id', 'obligation'))}` ({_md(obligation.get('kind', 'condition'))}): {_md(obligation.get('mathematically_missing', ''))}"
                )
                lines.append(f"  Why: {_md(obligation.get('why_missing', ''))}")
                lines.append(f"  Closes: {_md(obligation.get('closes', ''))}")
        else:
            lines.append("- None detected by the deterministic packet builder.")
        graph = packet.get("context_graph")
        lines.extend(["", "Local context graph:"])
        if isinstance(graph, dict) and graph.get("nodes"):
            for node in graph.get("nodes", []):
                if not isinstance(node, dict):
                    continue
                if node.get("kind") not in {"candidate_assumption", "definition", "notation_declaration"}:
                    continue
                refs = [
                    f"{ref.get('file')}:{ref.get('line_start')}-{ref.get('line_end')}"
                    for ref in node.get("source_refs", [])
                    if isinstance(ref, dict)
                ]
                lines.append(f"- `{_md(node.get('id', 'node'))}` status `{_md(node.get('status', ''))}`")
                lines.append(f"  Role: {_md(node.get('mathematical_role', ''))}")
                lines.append(f"  What: {_md(node.get('summary', ''))}")
                lines.append(f"  Why status: {_md(node.get('why_status', ''))}")
                lines.append(f"  Required next evidence: {_md(node.get('required_next_evidence', ''))}")
                lines.append(f"  Source refs: `{_md(refs)}`")
        else:
            lines.append("- No context graph was generated.")
        typed = packet.get("typed_repair_obligation")
        lines.extend(["", "Typed repair obligation:"])
        if isinstance(typed, dict) and typed:
            lines.append(f"- ID: `{_md(typed.get('id', ''))}`")
            lines.append(f"  Diagnostic status: `{_md(typed.get('diagnostic_status', ''))}`")
            lines.append(f"  Encodability: `{_md(typed.get('encodability', {}))}`")
            lines.append(f"  Unresolved constructs: `{_md(typed.get('unresolved_constructs', []))}`")
            lines.append(f"  Route hints: `{_md(typed.get('route_hints', []))}`")
            assumptions = typed.get("assumptions", [])
            if isinstance(assumptions, list) and assumptions:
                lines.append("  Assumption statuses:")
                for assumption in assumptions:
                    if isinstance(assumption, dict):
                        lines.append(
                            f"  - `{_md(assumption.get('id', 'assumption'))}` "
                            f"status `{_md(assumption.get('status', ''))}`: "
                            f"{_md(assumption.get('text', ''))}"
                        )
            lines.append(f"  Boundary: {_md(typed.get('certification_boundary', ''))}")
        else:
            lines.append("- No typed repair obligation was generated.")
        _render_tool_grounded_proposal_compiler(lines, tree.get("tool_grounded_proposal_compiler", {}))
        _render_document_ready_proposals(lines, tree.get("document_ready_repair_proposals", []))
        _render_document_partial_evidence_reports(lines, tree.get("document_partial_evidence_reports", []))
        _render_document_gap_reports(lines, tree.get("document_gap_reports", []))
        lines.extend(["", "Possible sufficient assumption sets:"])
        sets = packet.get("possible_assumption_sets", [])
        if sets:
            for item in sets:
                lines.append(f"- `{_md(item.get('id', 'assumption_set'))}`: {_md(item.get('closes', ''))}")
                assumptions = item.get("assumptions", [])
                if isinstance(assumptions, list):
                    for assumption in assumptions:
                        lines.append(f"  - {_md(assumption)}")
        else:
            lines.append("- None proposed by deterministic templates.")
        branches = tree.get("assumption_branches", [])
        ranking = tree.get("branch_ranking", {})
        lines.extend(["", "Branch ranking:"])
        if isinstance(ranking, dict) and ranking.get("rankings"):
            lines.append(f"- Contract: `{_md(ranking.get('metadata', {}).get('contract', ''))}`")
            lines.append(f"- Nondominated branches: `{_md(ranking.get('nondominated_branch_ids', []))}`")
            lines.append(f"- Unique top branch, only if one exists: `{_md(ranking.get('top_branch_id', ''))}`")
            lines.append(f"- Selected discriminating action: `{_md(ranking.get('selected_action', {}))}`")
            for item in ranking.get("rankings", []):
                if not isinstance(item, dict):
                    continue
                lines.append(
                    f"- Serialization position `{_md(item.get('serialization_position', ''))}`: "
                    f"`{_md(item.get('branch_id', ''))}` outcome `{_md(item.get('outcome', ''))}`, "
                    f"nondominated `{_md(item.get('nondominated', False))}`"
                )
                lines.append(f"  - Decision dimensions: `{_md(item.get('decision_dimensions', {}))}`")
                lines.append(f"  - Explanation: {_md(item.get('explanation', ''))}")
        else:
            lines.append("- No branch ranking was generated.")
        lines.extend(["", "Candidate assumption branches:"])
        if branches:
            for branch in branches:
                lines.append(f"- `{_md(branch.get('id', 'branch'))}` status `{_md(branch.get('status', ''))}`")
                lines.append(f"  - Closes obligations: `{_md(branch.get('closes_obligations', []))}`")
                lines.append(f"  - Typed obligation ids: `{_md(branch.get('typed_obligation_ids', []))}`")
                lines.append(f"  - Typed unresolved constructs: `{_md(branch.get('typed_unresolved_constructs', []))}`")
                lines.append(f"  - Typed encodability: `{_md(branch.get('typed_encodability', {}))}`")
                evidence = branch.get("backend_evidence", {})
                if isinstance(evidence, dict) and evidence:
                    lines.append(f"  - Backend evidence status: `{_md(evidence.get('status', ''))}`")
                    lines.append(f"  - Raw backend promotion history (diagnostic only): `{_md(evidence.get('raw_promotion', {}))}`")
                    lines.append(f"  - Effective document promotion: `{_md(evidence.get('effective_document_promotion', {}))}`")
                    lines.append(f"  - Evidence binding: `{_md(evidence.get('binding_status', ''))}`")
                    lines.append(f"  - Failure classification: `{_md(evidence.get('failure_classification', ''))}`")
                lines.append(f"  - Why: {_md(branch.get('mathematical_why', ''))}")
                assumptions = branch.get("assumptions", [])
                if isinstance(assumptions, list):
                    lines.append(f"  - Proposed assumptions: {_md(assumptions)}")
                route = branch.get("derivation_route_under_assumptions", [])
                if isinstance(route, list) and route:
                    lines.append("  - Route under assumptions:")
                    for step in route[:4]:
                        if isinstance(step, dict):
                            lines.append(f"    - {_md(step.get('step', 'step'))}: {_md(step.get('detail', ''))}")
                expansions = branch.get("expansion_records", [])
                if isinstance(expansions, list) and expansions:
                    lines.append("  - Expansion records:")
                    for record in expansions[:8]:
                        if isinstance(record, dict):
                            lines.append(
                                f"    - `{_md(record.get('kind', 'expansion'))}` "
                                f"status `{_md(record.get('status', ''))}`: "
                                f"{_md(record.get('summary', ''))}"
                            )
                ledger = branch.get("external_tool_first_ledger", [])
                if isinstance(ledger, list) and ledger:
                    tools = [
                        f"{item.get('tool')}:{item.get('status')}"
                        for item in ledger
                        if isinstance(item, dict)
                    ]
                    lines.append(f"  - External-tool ledger: `{_md(tools)}`")
                branch_attempts = branch.get("backend_attempts", [])
                if isinstance(branch_attempts, list) and branch_attempts:
                    lines.append("  - Branch backend attempts:")
                    for attempt in branch_attempts:
                        if isinstance(attempt, dict):
                            lines.append(
                                f"    - `{_md(attempt.get('id', 'attempt'))}` with `{_md(attempt.get('tool', 'tool'))}`: "
                                f"status `{_md(attempt.get('status', ''))}`, evidence `{_md(attempt.get('evidence_kind', ''))}`, "
                                f"certification `{_md(attempt.get('certification_status', ''))}`"
                            )
                translation_attempts = branch.get("translation_attempts", [])
                if isinstance(translation_attempts, list) and translation_attempts:
                    lines.append("  - Translation attempts:")
                    for attempt in translation_attempts:
                        if isinstance(attempt, dict):
                            lines.append(
                                f"    - `{_md(attempt.get('backend', 'backend'))}` "
                                f"status `{_md(attempt.get('status', ''))}`; "
                                f"attempt ids `{_md(attempt.get('backend_attempt_ids', []))}`; "
                                f"blockers `{_md(attempt.get('blocker_ids', []))}`"
                            )
                translation_blockers = branch.get("translation_blockers", [])
                if isinstance(translation_blockers, list) and translation_blockers:
                    lines.append("  - Translation blockers:")
                    for blocker in translation_blockers:
                        if isinstance(blocker, dict):
                            lines.append(
                                f"    - `{_md(blocker.get('id', 'blocker'))}` ({_md(blocker.get('kind', ''))}): "
                                f"{_md(blocker.get('problem', ''))}"
                            )
                            lines.append(f"      Why: {_md(blocker.get('why', ''))}")
                            lines.append(f"      Required next evidence: {_md(blocker.get('required_next_evidence', ''))}")
                stubs = branch.get("formalization_stubs", [])
                if isinstance(stubs, list) and stubs:
                    lines.append("  - Formalization stubs:")
                    for stub in stubs:
                        if isinstance(stub, dict):
                            lines.append(
                                f"    - `{_md(stub.get('backend', 'backend'))}` "
                                f"status `{_md(stub.get('status', ''))}`; "
                                f"unsupported: `{_md(stub.get('unsupported_constructs', []))}`"
                            )
        else:
            lines.append("- None generated.")
        lines.extend(["", "How the derivation can work:"])
        route = packet.get("how_derivation_can_work", [])
        if route:
            for step in route:
                lines.append(f"- `{_md(step.get('step', 'step'))}`: {_md(step.get('detail', ''))}")
        else:
            lines.append("- No route proposed.")
        lines.extend(["", "Backend attempts:"])
        attempts = tree.get("backend_attempts", [])
        if attempts:
            for attempt in attempts:
                lines.append(
                    f"- `{_md(attempt.get('id', 'attempt'))}` with `{_md(attempt.get('tool', 'tool'))}`: "
                    f"status `{_md(attempt.get('status', ''))}`, evidence `{_md(attempt.get('evidence_kind', ''))}`, "
                    f"certification `{_md(attempt.get('certification_status', ''))}`"
                )
        else:
            lines.append("- None recorded.")
        patches = tree.get("patch_candidates", [])
        lines.extend(["", "Blocked patch candidates (non-applicable):"])
        if patches:
            for patch in patches:
                lines.append(f"- `{_md(patch.get('id', 'patch'))}` status `{_md(patch.get('validation_status', ''))}`")
                lines.append(f"  Applicable: `{_md(patch.get('applicable', False))}`")
                lines.append(f"  Blocked candidate text: {_md(patch.get('candidate_text_blocked', ''))}")
                lines.append(f"  Blocked reason: {_md(patch.get('blocked_reason', ''))}")
                lines.append(f"  Rationale: {_md(patch.get('rationale', ''))}")
        else:
            lines.append("- None recorded.")
        lines.extend(["", "Remaining blockers:"])
        blockers = tree.get("blockers", [])
        if blockers:
            for blocker in blockers:
                lines.append(f"- `{_md(blocker.get('id', 'blocker'))}` ({_md(blocker.get('kind', ''))})")
                lines.append(f"  Problem: {_md(blocker.get('problem', ''))}")
                lines.append(f"  Why: {_md(blocker.get('why', ''))}")
                lines.append(f"  Required next evidence: {_md(blocker.get('required_next_evidence', ''))}")
        else:
            lines.append("- None recorded.")
        next_audit = packet.get("next_audit")
        if isinstance(next_audit, dict) and next_audit:
            lines.append("")
            lines.append(f"Smallest next audit: `{_md(next_audit.get('tool', ''))}` - {_md(next_audit.get('purpose', ''))}")
        lines.append("")
    lines.extend(["## Non-Claims", ""])
    for item in result.get("non_claims", []):
        lines.append(f"- `{_md(item.get('code', ''))}`: {_md(item.get('text', ''))}")
    lines.append("")
    return "\n".join(lines)


def render_compact_document_derivation_tree_markdown(result: dict[str, Any]) -> str:
    """Render an all-target summary while details remain artifact-resolvable."""
    coverage = result.get("coverage") if isinstance(result.get("coverage"), dict) else {}
    lines = [
        "# Compact Document Derivation Tree Audit",
        "",
        f"Source: `{result.get('tex_path', '')}`",
        f"Publication mode: `{result.get('publication_mode', DOCUMENT_PUBLICATION_MODE)}`",
        f"Targets: `{coverage.get('semantic_packet_count', 0)}`; gaps: `{coverage.get('document_gap_report_count', 0)}`; repairs: `{coverage.get('document_ready_repair_proposal_count', 0)}`",
        "",
        "This is a bounded transport summary. Exact detailed records remain in the digest-bound document artifact and page-token resolver.",
        "",
        "| Label | Relation | Source role | Tree status | Specialist | Binding | Local obligations | Next action |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for target in result.get("targets", []):
        if not isinstance(target, dict):
            continue
        packet = target.get("semantic_work_packet") if isinstance(target.get("semantic_work_packet"), dict) else {}
        tree = target.get("tree") if isinstance(target.get("tree"), dict) else {}
        normalized = packet.get("normalized_target") if isinstance(packet.get("normalized_target"), dict) else {}
        role = packet.get("routing_role") if isinstance(packet.get("routing_role"), dict) else {}
        specialist = packet.get("specialist_execution") if isinstance(packet.get("specialist_execution"), dict) else {}
        ranking = tree.get("branch_ranking") if isinstance(tree.get("branch_ranking"), dict) else {}
        action = ranking.get("selected_action") if isinstance(ranking.get("selected_action"), dict) else {}
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_md(target.get('label', ''))}`",
                    f"`{_md(normalized.get('kind', 'unavailable'))}`",
                    f"`{_md(role.get('role', 'unsupported_or_ambiguous'))}`",
                    f"`{_md(target.get('status', ''))}`",
                    f"`{_md(specialist.get('status', 'not_run'))}`",
                    f"`{_md(target.get('integrity_binding_status', DOCUMENT_INTEGRITY_BINDING_STATUS))}`",
                    str(len(packet.get("local_obligations", []))),
                    f"`{_md(action.get('action_kind', 'none'))}`",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Exact Targets", ""])
    for target in result.get("targets", []):
        if not isinstance(target, dict):
            continue
        packet = target.get("semantic_work_packet") if isinstance(target.get("semantic_work_packet"), dict) else {}
        specialist = packet.get("specialist_execution") if isinstance(packet.get("specialist_execution"), dict) else {}
        specialist_result = specialist.get("result") if isinstance(specialist.get("result"), dict) else {}
        lines.extend(
            [
                f"### `{_md(target.get('label', 'target'))}`",
                "",
                f"- Source digest: `{_md(packet.get('source_span', {}).get('source_digest', ''))}`",
                f"- Obligation: `{_md(packet.get('obligation_id', ''))}` / `{_md(packet.get('obligation_digest', ''))}`",
                f"- Binding: `{_md(target.get('document_evidence_binding_ref', {}))}`",
                f"- Specialist: `{_md(specialist.get('status', 'not_run'))}`; tool `{_md(specialist.get('selected_tool'))}`; result `{_md(specialist_result.get('status', ''))}`",
                f"- Remaining local obligations: `{_md([item.get('id') for item in packet.get('local_obligations', []) if isinstance(item, dict)])}`",
                "",
                "```tex",
                str(packet.get("target", "")).strip(),
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundaries",
            "",
            "- Current evidence binding establishes source/evidence identity and replay, not mathematical or scientific truth.",
            "- Specialist CAS checks are scoped diagnostics; typed abstentions are not refutations.",
            "- No candidate edit is applicable while publication mode is disabled.",
            "- This selected-label audit does not establish whole-document correctness.",
            "",
        ]
    )
    rendered = "\n".join(lines)
    if len(rendered.encode("utf-8")) > 30_720:
        raise ValueError("compact document derivation Markdown exceeds the transport budget")
    return rendered
