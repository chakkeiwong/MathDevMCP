"""High-level mathematical rigor audit workflow for LaTeX documents."""

from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from .actionable_abstentions import build_actionable_abstention_payload
from .audit_and_propose_fix import audit_and_propose_fix
from .contracts import attach_contract
from .doctor import doctor_report
from .equation_locator import locate_equations_in_file, summarize_equation_localization
from .lean_readiness import lean_readiness
from .derivation_target_extraction import extract_derivation_targets_for_label
from .latex_index import build_index
from .role_obligations import build_role_specific_obligations, has_role_specific_builder


RIGOR_AUDIT_CONTRACT = "math_document_rigor_audit"
RIGOR_PLAN_CONTRACT = "math_document_rigor_audit_plan"
DEFAULT_LABEL_LIMIT = 30
CONCRETE_REPAIR_CLASS = "concrete_repair"
DIAGNOSTIC_ABSTENTION_CLASS = "diagnostic_abstention"
NON_CONCRETE_KINDS = {
    "add_review_boundary",
    "collect_more_evidence",
    "concretize_before_fix",
    "fix_parser_provenance",
    "prove_reconstructed_obligation",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_path_for_line(sections: list[dict[str, Any]], line: int) -> list[str]:
    current: list[str] = []
    for section in sections:
        if int(section["line"]) > line:
            break
        level = int(section["level"])
        current = current[: level - 1] + [str(section["title"])]
    return current


def _section_map(text: str) -> list[dict[str, Any]]:
    pattern = re.compile(r"\\(?P<kind>section|subsection|subsubsection|paragraph)\*?\{(?P<title>[^}]*)\}")
    levels = {"section": 1, "subsection": 2, "subsubsection": 3, "paragraph": 4}
    sections: list[dict[str, Any]] = []
    for index, line in enumerate(text.splitlines(), start=1):
        match = pattern.search(line)
        if match:
            sections.append(
                {
                    "line": index,
                    "kind": match.group("kind"),
                    "level": levels[match.group("kind")],
                    "title": match.group("title").strip(),
                }
            )
    return sections


def _label_ref_hygiene(text: str) -> dict[str, Any]:
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    refs = re.findall(r"\\(?:eqref|ref|autoref|cref|Cref)\{([^}]+)\}", text)
    counts = Counter(labels)
    duplicates = sorted(label for label, count in counts.items() if count > 1)
    missing = sorted(ref for ref in refs if ref not in counts)
    return {
        "label_count": len(labels),
        "unique_label_count": len(counts),
        "duplicate_labels": duplicates,
        "ref_count": len(refs),
        "missing_refs": missing,
    }


def _classify_equation(row: dict[str, Any]) -> str:
    text = str(row.get("text", ""))
    lowered = text.lower()
    if "\\mathbb{e}" in lowered or "\\operatorname{e}" in lowered or "expect" in lowered or "\\e[" in lowered:
        return "stochastic_expectation"
    if "\\arg" in lowered or "\\max" in lowered or "\\min" in lowered or "\\sup" in lowered:
        return "optimization_or_policy"
    if "npv" in lowered or "\\delta" in lowered or "cash" in lowered:
        return "valuation_identity_or_definition"
    if "itt" in lowered or "late" in lowered or "treatment" in lowered or "random" in lowered:
        return "causal_estimand_or_identification"
    if "calibration" in lowered or "uncertainty" in lowered or "draw" in lowered:
        return "validation_or_uncertainty"
    if "=" in text:
        return "identity_or_definition"
    return "unclassified_math"


def _row_location(tex_path: Path, row: dict[str, Any], sections: list[dict[str, Any]]) -> str:
    section_path = _section_path_for_line(sections, int(row.get("line_start", 0)))
    parts = [tex_path.name]
    parts.extend(section_path)
    label = row.get("label")
    if label:
        parts.append(str(label))
    parts.append(f"line {row.get('line_start', 'unknown')}")
    return " > ".join(parts)


def _select_rows(
    rows: list[dict[str, Any]],
    *,
    focus_labels: list[str] | None,
    max_labels: int | None,
) -> list[dict[str, Any]]:
    labeled = [row for row in rows if isinstance(row.get("label"), str) and row.get("label")]
    if focus_labels:
        selected: list[dict[str, Any]] = []
        seen: set[str] = set()
        for label in focus_labels:
            if label in seen:
                continue
            seen.add(label)
            match = next((row for row in labeled if row.get("label") == label), None)
            if match is not None:
                selected.append(match)
        return selected
    limit = max_labels if max_labels is not None else DEFAULT_LABEL_LIMIT
    deduped: list[dict[str, Any]] = []
    seen_labels: set[str] = set()
    for row in labeled:
        label = str(row.get("label"))
        if label in seen_labels:
            continue
        seen_labels.add(label)
        deduped.append(row)
    if limit is not None and limit <= 0:
        return deduped
    return deduped[:limit]


def _target_entries(tex_path: Path, rows: list[dict[str, Any]], sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index = build_index(tex_path.parent)
    entries: list[dict[str, Any]] = []
    for row in rows:
        label = str(row.get("label", ""))
        extraction = extract_derivation_targets_for_label(index, label, file=tex_path.name) if label else {}
        targets = extraction.get("targets", []) if isinstance(extraction, dict) else []
        canonical = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
        routing_role = canonical.get("routing_role", {}) if isinstance(canonical, dict) else {}
        role_obligations: dict[str, Any] | None = None
        if (
            isinstance(canonical, dict)
            and isinstance(routing_role, dict)
            and has_role_specific_builder(routing_role, target=str(canonical.get("target", "")))
        ):
            role_obligations = build_role_specific_obligations(
                target=str(canonical.get("target", "")),
                normalized_target=canonical.get("normalized_target", {}),
                routing_role=routing_role,
                evidence_refs=[
                    f"source:{canonical.get('label_scoped_obligation', {}).get('document', {}).get('source_digest')}:{canonical.get('obligation_digest')}",
                    f"routing_role:{routing_role.get('role_id', routing_role.get('role', 'unknown'))}",
                ],
            )
        entries.append(
            {
                "label": label,
                "location": _row_location(tex_path, canonical or row, sections),
                "line_start": canonical.get("line_start") if canonical else row.get("line_start"),
                "line_end": canonical.get("line_end") if canonical else row.get("line_end"),
                "environment": canonical.get("environment") if canonical else row.get("environment"),
                "claim_type": routing_role.get("role", "unsupported_or_ambiguous"),
                "text": canonical.get("target") if canonical else row.get("text"),
                "normalized_target": canonical.get("normalized_target") if canonical else None,
                "routing_role": routing_role or None,
                "obligation_id": canonical.get("obligation_id") if canonical else None,
                "obligation_digest": canonical.get("obligation_digest") if canonical else None,
                "local_obligations": role_obligations.get("local_obligations", []) if role_obligations else [],
                "downstream_integration_obligations": role_obligations.get("downstream_integration_obligations", []) if role_obligations else [],
                "possible_assumption_sets": role_obligations.get("possible_assumption_sets", []) if role_obligations else [],
                "role_derivation_route": role_obligations.get("derivation_route", []) if role_obligations else [],
                "role_obligation_non_claims": role_obligations.get("non_claims", []) if role_obligations else [],
                "uncertainty": row.get("uncertainty", []),
            }
        )
    return entries


def _tool_use(tool: str, purpose: str, status: str, output_contract: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool": tool,
        "purpose": purpose,
        "status": status,
        "output_contract": output_contract,
        "arguments": arguments,
    }


@contextmanager
def _backend_env_scope(backend_env: str | None):
    old = os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV")
    if backend_env:
        os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = backend_env
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("MATHDEVMCP_BACKEND_CONDA_ENV", None)
        else:
            os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = old


def _backend_provenance(tex_path: Path, *, backend_env: str | None) -> dict[str, Any]:
    with _backend_env_scope(backend_env):
        doctor = doctor_report()
        readiness = lean_readiness(tex_path.parent)
    return {
        "doctor": doctor,
        "lean_readiness": readiness,
        "certification_boundary": (
            "LeanDojo availability is proof-search evidence only. A proof is certified only by direct "
            "Lean checking with no placeholders, or by another certifying backend under the scoped contract."
        ),
    }


def plan_math_document_rigor_audit(
    tex_path: str | Path,
    *,
    focus_labels: list[str] | None = None,
    max_labels: int | None = DEFAULT_LABEL_LIMIT,
) -> dict[str, Any]:
    """Plan a focused rigor audit for a single LaTeX file."""
    path = Path(tex_path)
    text = _read_text(path)
    rows = locate_equations_in_file(path, root=path.parent)
    sections = _section_map(text)
    selected = _select_rows(rows, focus_labels=focus_labels, max_labels=max_labels)
    target_entries = _target_entries(path, selected, sections)
    labeled_rows = [row for row in rows if row.get("label")]
    result = {
        "tex_path": str(path),
        "document_inventory": {
            "line_count": len(text.splitlines()),
            "sections": sections,
            "section_count": len(sections),
            "equation_localization": summarize_equation_localization(rows),
            "label_ref_hygiene": _label_ref_hygiene(text),
            "labeled_equation_count": len(labeled_rows),
        },
        "target_selection": {
            "mode": "focus_labels" if focus_labels else "first_labeled_equations",
            "requested_focus_labels": list(focus_labels or []),
            "max_labels": max_labels,
            "selected_count": len(target_entries),
            "available_labeled_equation_count": len(labeled_rows),
            "partial_coverage": len(target_entries) < len(labeled_rows),
            "targets": target_entries,
        },
        "tool_uses": [
            _tool_use(
                "locate_equations_in_file",
                "Localize display equations in the exact target file.",
                "completed",
                "equation_rows",
                {"tex_path": str(path), "root": str(path.parent)},
            ),
            _tool_use(
                "summarize_equation_localization",
                "Summarize equation localization uncertainty.",
                "completed",
                "equation_localization_summary",
                {"row_count": len(rows)},
            ),
        ],
        "non_claims": [
            {
                "code": "plan_not_audit",
                "text": "This planning result selects audit targets; it does not prove or repair the document.",
            },
            {
                "code": "partial_coverage_when_limited",
                "text": "When selected_count is below available_labeled_equation_count, the plan is not a full-document audit.",
            },
        ],
    }
    return attach_contract(result, RIGOR_PLAN_CONTRACT)


def _default_gap_for_target(target: dict[str, Any]) -> dict[str, Any]:
    label = str(target.get("label", "unlabeled"))
    claim_type = str(target.get("claim_type", "unclassified_math"))
    return {
        "id": f"rigor_gap_{_slug(label)}",
        "label": label,
        "location": target.get("location", label),
        "problem": f"The `{claim_type}` claim needs an explicit rigor classification and assumption/derivation route.",
        "why_mathematically_problematic": (
            "A displayed mathematical claim can function as a definition, identity, stochastic object, "
            "optimization condition, estimand, or validation statistic. Without an explicit route and assumptions, "
            "an agent cannot tell whether to prove it, assume it, estimate it, or treat it as a diagnostic."
        ),
        "proposed_fix": (
            "Add or verify a local statement classifying the claim, its required assumptions, and the evidence route "
            "before using it as a derivation step or implementation contract."
        ),
        "assumptions_needed": [],
        "possible_assumption_sets": [],
        "derivation_route": {
            "status": "not_attempted_in_mvp",
            "reason": "The MVP delegates concrete label repair to audit_and_propose_fix and records remaining classification gaps.",
        },
        "backend_evidence": {"status": "not_certified", "reason": "No certifying backend evidence is attached to this default gap."},
        "evidence_refs": [f"target_selection:{label}"],
    }


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower() or "target"


def _proposal_from_gap(gap: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"proposal_{gap['id']}",
        "gap_ids": [gap["id"]],
        "label": gap.get("label"),
        "kind": gap.get("kind"),
        "substantive_classification": gap.get("substantive_classification", DIAGNOSTIC_ABSTENTION_CLASS),
        "why_not_concrete": gap.get("why_not_concrete", ""),
        "location": gap["location"],
        "problem": gap["problem"],
        "why_mathematically_problematic": gap["why_mathematically_problematic"],
        "proposed_fix": gap["proposed_fix"],
        "assumptions_needed": gap.get("assumptions_needed", []),
        "possible_assumption_sets": gap.get("possible_assumption_sets", []),
        "replacement_latex": gap.get("replacement_latex", ""),
        "proof_target": gap.get("proof_target", ""),
        "derivation_plan": gap.get("derivation_plan", ""),
        "math_fix": gap.get("math_fix"),
        "required_evidence_before_repair": gap.get("required_evidence_before_repair", []),
        "smallest_next_audit": gap.get("smallest_next_audit", {}),
        "actionable_abstention": gap.get("actionable_abstention", {}),
        "derivation_route": gap.get("derivation_route", {}),
        "backend_evidence": gap.get("backend_evidence", {}),
        "evidence_refs": gap.get("evidence_refs", []),
    }


def _normalize_evidence_refs(item: dict[str, Any], *, fallback: str) -> list[str]:
    refs: list[str] = []
    for key in ("evidence_refs", "evidence_ref"):
        raw = item.get(key)
        if isinstance(raw, list):
            refs.extend(str(ref) for ref in raw if ref)
        elif isinstance(raw, str) and raw:
            refs.append(raw)
    deduped: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref not in seen:
            deduped.append(ref)
            seen.add(ref)
    return deduped or [fallback]


def _backend_evidence_from_item(item: dict[str, Any]) -> dict[str, Any]:
    for key in ("validation", "backend_evidence"):
        raw = item.get(key)
        if isinstance(raw, dict) and raw:
            return raw
    return {
        "status": "not_certified",
        "reason": "No structured backend validation evidence was attached to this proposal detail.",
        "certification_boundary": (
            "Only certifying deterministic backend evidence validates a proposed fix. "
            "Missing validation metadata is diagnostic, not proof."
        ),
    }


def _math_fix_from_item(item: dict[str, Any]) -> dict[str, Any]:
    raw = item.get("math_fix")
    return raw if isinstance(raw, dict) else {}


def _text_field(item: dict[str, Any], key: str) -> str:
    raw = item.get(key)
    return raw.strip() if isinstance(raw, str) else ""


def _replacement_latex_from_item(item: dict[str, Any]) -> str:
    math_fix = _math_fix_from_item(item)
    raw = math_fix.get("replacement_latex") or item.get("replacement_latex")
    return raw.strip() if isinstance(raw, str) else ""


def _proof_target_from_item(item: dict[str, Any]) -> str:
    math_fix = _math_fix_from_item(item)
    raw = item.get("proof_target") or math_fix.get("equation")
    return raw.strip() if isinstance(raw, str) else ""


def _derivation_plan_from_item(item: dict[str, Any]) -> str:
    math_fix = _math_fix_from_item(item)
    raw = item.get("derivation_plan") or math_fix.get("derivation_obligation")
    return raw.strip() if isinstance(raw, str) else ""


def _latex_dynamic_delimiters_balanced(text: str) -> bool:
    return text.count(r"\left") == text.count(r"\right")


def _latex_environment_balanced(text: str, environment: str) -> bool:
    return text.count(rf"\begin{{{environment}}}") == text.count(rf"\end{{{environment}}}")


def _latex_payload_safe(text: str) -> bool:
    if not text:
        return False
    if not _latex_dynamic_delimiters_balanced(text):
        return False
    for environment in ("equation", "align", "alignat", "gather", "multline"):
        if not _latex_environment_balanced(text, environment):
            return False
    return True


def _safe_wording_from_item(item: dict[str, Any]) -> str:
    for key in ("safe_wording", "proposed_safe_wording", "replacement_text"):
        raw = item.get(key)
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def _assumption_statement_from_item(item: dict[str, Any]) -> str:
    for key in ("proposed_assumption", "assumption_statement"):
        raw = item.get(key)
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    assumptions = item.get("assumptions_needed")
    if isinstance(assumptions, list):
        exact = [str(value).strip() for value in assumptions if str(value).strip()]
        if len(exact) == 1 and len(exact[0].split()) > 3:
            return exact[0]
    return ""


def _detail_substance(item: dict[str, Any]) -> dict[str, Any]:
    kind = _text_field(item, "kind")
    evidence_only = bool(item.get("evidence_only"))
    replacement_latex = _replacement_latex_from_item(item)
    proof_target = _proof_target_from_item(item)
    derivation_plan = _derivation_plan_from_item(item)
    safe_wording = _safe_wording_from_item(item)
    assumption_statement = _assumption_statement_from_item(item)
    replacement_safe = bool(replacement_latex and _latex_payload_safe(replacement_latex))
    proof_target_safe = bool(proof_target and _latex_payload_safe(proof_target))
    has_derivation_route = bool(proof_target_safe and derivation_plan)
    has_actionable_payload = bool(replacement_safe or safe_wording or assumption_statement or has_derivation_route)
    if evidence_only and replacement_latex and not replacement_safe:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "The source detail is evidence-only and its reconstructed replacement LaTeX failed conservative structure checks."
    elif evidence_only and proof_target and not proof_target_safe:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "The source detail is evidence-only and its proof target failed conservative LaTeX structure checks."
    elif evidence_only:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit."
    elif replacement_latex and not replacement_safe:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "The reconstructed replacement LaTeX failed conservative structure checks."
    elif proof_target and not proof_target_safe:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "The proof target failed conservative LaTeX structure checks."
    elif kind in NON_CONCRETE_KINDS and not (replacement_safe or safe_wording or assumption_statement):
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = f"`{kind}` is a certification or evidence gap unless it includes exact replacement text or an assumption statement."
    elif replacement_safe or safe_wording or assumption_statement:
        classification = CONCRETE_REPAIR_CLASS
        reason = "The detail includes exact replacement text or an exact local statement."
    elif has_derivation_route:
        classification = CONCRETE_REPAIR_CLASS
        reason = "The detail includes both a proof target and a derivation route."
    elif proof_target:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "A proof target alone is not a repair; it needs replacement text, exact assumptions, or a derivation route."
    else:
        classification = DIAGNOSTIC_ABSTENTION_CLASS
        reason = "No exact replacement text, assumption statement, safe wording, or derivation route was attached."
    return {
        "kind": kind,
        "classification": classification,
        "reason": reason,
        "evidence_only": evidence_only,
        "has_actionable_payload": has_actionable_payload,
        "replacement_latex_safe": replacement_safe,
        "proof_target_safe": proof_target_safe,
        "replacement_latex": replacement_latex,
        "proof_target": proof_target,
        "derivation_plan": derivation_plan,
        "safe_wording": safe_wording,
        "assumption_statement": assumption_statement,
        "math_fix": _math_fix_from_item(item) or None,
    }


def _proposed_fix_from_substance(item: dict[str, Any], substance: dict[str, Any]) -> str:
    if substance["classification"] == CONCRETE_REPAIR_CLASS:
        if substance.get("replacement_latex"):
            return (
                "Replace the affected displayed math with the replacement LaTeX below, "
                "then rerun the referenced audit before treating the edit as certified."
            )
        if substance.get("assumption_statement"):
            return "Insert or verify the exact local assumption statement below, then rerun the referenced audit."
        if substance.get("safe_wording"):
            return "Use the exact safe wording below and keep the non-certification boundary visible."
        if substance.get("proof_target") and substance.get("derivation_plan"):
            return "Add the local derivation route below, then rerun the referenced audit on the same label."
    fallback = _text_field(item, "proposed_fix") or _text_field(item, "summary")
    if fallback and fallback.startswith("Do not edit the document from this item alone."):
        return fallback
    return "Do not edit the document from this item alone; first satisfy the required evidence before repair."


def _required_evidence_from_substance(item: dict[str, Any], substance: dict[str, Any]) -> list[str]:
    if substance["classification"] == CONCRETE_REPAIR_CLASS:
        return []
    requirements: list[str] = []
    if not substance.get("replacement_latex") and not substance.get("safe_wording"):
        requirements.append("Exact replacement LaTeX or exact safe wording tied to the cited source line.")
    if substance.get("proof_target") and not substance.get("derivation_plan"):
        requirements.append("A derivation route showing why the proof target follows from local assumptions.")
    if _text_field(item, "kind") == "add_or_verify_assumption" and not substance.get("assumption_statement"):
        requirements.append("An explicit assumption statement, not only an assumption category or target name.")
    if not requirements:
        requirements.append("A concrete repair payload that can be checked by the next audit.")
    return requirements


def _proof_audit_label_from_refs(refs: list[str]) -> str:
    prefix = "proof_audit_v2:"
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith(prefix):
            continue
        tail = ref[len(prefix) :]
        if ":obligation_" in tail:
            label, _, _obligation = tail.rpartition(":obligation_")
            return label
        return tail
    return ""


def _smallest_next_audit_from_substance(item: dict[str, Any], substance: dict[str, Any]) -> dict[str, Any]:
    refs = _normalize_evidence_refs(item, fallback="audit_fix_report:proposal_detail")
    label = _proof_audit_label_from_refs(refs)
    if substance["classification"] == CONCRETE_REPAIR_CLASS:
        return {
            "tool": "audit_derivation_v2_label",
            "label": label,
            "purpose": "Rerun the local derivation audit after applying or formalizing the proposed repair.",
        }
    return {
        "tool": "audit_and_propose_fix",
        "label": label,
        "purpose": "Regenerate the proposal after adding the required concrete payload.",
    }


def _extract_fix_report(high_level: dict[str, Any]) -> dict[str, Any]:
    for item in high_level.get("evidence", []):
        if isinstance(item, dict) and isinstance(item.get("low_level"), dict):
            return item["low_level"]
    return {}


def _validated_reused_fix_result(
    high_level: dict[str, Any],
    *,
    path: Path,
    target_labels: list[str],
) -> dict[str, Any]:
    if high_level.get("workflow") != "audit_and_propose_fix":
        raise ValueError("reused audit/fix evidence must be an audit_and_propose_fix workflow result")
    low = _extract_fix_report(high_level)
    source = low.get("source") if isinstance(low.get("source"), dict) else {}
    expected_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if source.get("source_digest") != expected_digest:
        raise ValueError("reused audit/fix evidence source digest does not match the target document")
    source_file = source.get("file") or source.get("target_file")
    if not isinstance(source_file, str) or Path(source_file).name != path.name:
        raise ValueError("reused audit/fix evidence source file does not match the target document")
    coverage = low.get("coverage") if isinstance(low.get("coverage"), dict) else {}
    audited = coverage.get("audited_labels")
    audited_labels = {
        str(item.get("label"))
        for item in audited
        if isinstance(item, dict) and item.get("label")
    } if isinstance(audited, list) else set()
    if audited_labels != set(target_labels) or coverage.get("audit_complete") is not True:
        raise ValueError("reused audit/fix evidence does not exactly cover the requested labels")
    return high_level


def _gaps_from_fix_report(fix_report: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    gaps: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    proposal_details = fix_report.get("agent_handoff", {}).get("proposal_details", [])
    if not isinstance(proposal_details, list):
        proposal_details = []
    for index, item in enumerate(proposal_details, start=1):
        if not isinstance(item, dict):
            continue
        substance = _detail_substance(item)
        evidence_refs = _normalize_evidence_refs(item, fallback=f"audit_fix_report:proposal_detail:{index}")
        actionable_abstention: dict[str, Any] = {}
        if substance["classification"] != CONCRETE_REPAIR_CLASS:
            actionable_abstention = build_actionable_abstention_payload(
                text="\n".join(
                    value
                    for value in (
                        substance.get("proof_target", ""),
                        substance.get("replacement_latex", ""),
                        _text_field(item, "source_text"),
                        _text_field(item, "rationale"),
                    )
                    if value
                ),
                problem=str(item.get("problem") or item.get("summary") or ""),
                why_not_concrete=substance["reason"],
                location=str(item.get("location") or item.get("target") or ""),
                kind=str(item.get("kind") or ""),
                evidence_refs=evidence_refs,
            )
        gap_id = f"audit_fix_gap_{index}_{_slug(str(item.get('target', item.get('location', 'target'))))}"
        gap = {
            "id": gap_id,
            "label": item.get("target"),
            "kind": item.get("kind"),
            "substantive_classification": substance["classification"],
            "why_not_concrete": "" if substance["classification"] == CONCRETE_REPAIR_CLASS else substance["reason"],
            "location": item.get("location") or item.get("target") or "unknown",
            "problem": item.get("problem") or item.get("summary") or "A concrete repair opportunity was found.",
            "why_mathematically_problematic": item.get("why") or item.get("rationale") or "The audit found a derivation or evidence gap that must be resolved before treating the claim as rigorous.",
            "proposed_fix": _proposed_fix_from_substance(item, substance),
            "assumptions_needed": item.get("assumptions_needed", []),
            "possible_assumption_sets": item.get("possible_assumption_sets", []),
            "replacement_latex": substance["replacement_latex"],
            "proof_target": substance["proof_target"],
            "derivation_plan": substance["derivation_plan"],
            "safe_wording": substance["safe_wording"],
            "assumption_statement": substance["assumption_statement"],
            "math_fix": substance["math_fix"],
            "required_evidence_before_repair": _required_evidence_from_substance(item, substance),
            "smallest_next_audit": _smallest_next_audit_from_substance(item, substance),
            "actionable_abstention": actionable_abstention,
            "derivation_route": item.get("derivation_route", {}) or {
                "proof_target": substance["proof_target"],
                "derivation_plan": substance["derivation_plan"],
            },
            "backend_evidence": _backend_evidence_from_item(item),
            "evidence_refs": evidence_refs,
        }
        gaps.append(gap)
        proposals.append(_proposal_from_gap(gap))
    return gaps, proposals


def _proposal_ledgers(proposals: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    concrete = [
        proposal
        for proposal in proposals
        if proposal.get("substantive_classification") == CONCRETE_REPAIR_CLASS
    ]
    diagnostic = [
        proposal
        for proposal in proposals
        if proposal.get("substantive_classification") != CONCRETE_REPAIR_CLASS
    ]
    return {
        "concrete_repairs": concrete,
        "diagnostic_abstentions": diagnostic,
    }


def audit_math_document_rigor(
    tex_path: str | Path,
    *,
    output_md: str | Path | None = None,
    output_json: str | Path | None = None,
    focus_labels: list[str] | None = None,
    max_labels: int | None = DEFAULT_LABEL_LIMIT,
    backend_env: str = "mathdevmcp-backends",
    validation_backends: list[str] | None = None,
    audit_fix_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run a focused document-rigor audit and optionally write Markdown/JSON artifacts."""
    path = Path(tex_path)
    plan = plan_math_document_rigor_audit(path, focus_labels=focus_labels, max_labels=max_labels)
    target_labels = [str(item["label"]) for item in plan["target_selection"]["targets"] if item.get("label")]
    tool_uses = list(plan.get("tool_uses", []))
    backend = _backend_provenance(path, backend_env=backend_env)
    tool_uses.append(
        _tool_use(
            "doctor_report",
            "Record active/backend Python and external backend capability provenance.",
            backend.get("doctor", {}).get("capabilities", {}).get("lean_dojo", {}).get("status", "completed"),
            "doctor_report",
            {},
        )
    )
    tool_uses.append(
        _tool_use(
            "lean_readiness",
            "Record direct Lean, Lake, and LeanDojo readiness without promoting readiness to proof.",
            backend.get("lean_readiness", {}).get("status", "completed"),
            "lean_readiness",
            {"root": str(path.parent)},
        )
    )

    fix_high_level: dict[str, Any] | None = None
    fix_report: dict[str, Any] = {}
    if target_labels:
        source_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if audit_fix_result is not None:
            fix_high_level = _validated_reused_fix_result(
                audit_fix_result,
                path=path,
                target_labels=target_labels,
            )
        else:
            fix_high_level = audit_and_propose_fix(
                "Audit selected document labels for mathematical rigor gaps and proposed repairs",
                root=str(path.parent),
                labels=target_labels,
                target_file=path.name,
                source_digest=source_digest,
                backend="sympy",
                validate_proposed_fixes=True,
                backend_order=validation_backends or ["lean", "sage", "sympy"],
                output_path=None,
            )
        fix_report = _extract_fix_report(fix_high_level)
        tool_uses.append(
            _tool_use(
                "audit_and_propose_fix",
                "Reuse exact audit/fix evidence for rigor synthesis."
                if audit_fix_result is not None
                else "Audit selected labels and propose concrete derivation/evidence repairs.",
                fix_report.get("status", fix_high_level.get("status", "unknown")),
                "high_level_workflow_result",
                {
                    "root": str(path.parent),
                    "target_file": path.name,
                    "source_digest": source_digest,
                    "labels": target_labels,
                    "validate_proposed_fixes": True,
                    "reused_exact_evidence": audit_fix_result is not None,
                },
            )
        )
        tool_uses.extend(fix_report.get("tool_uses", []))

    gaps, proposals = _gaps_from_fix_report(fix_report)
    if not gaps:
        gaps = [_default_gap_for_target(target) for target in plan["target_selection"]["targets"]]
        proposals = [_proposal_from_gap(gap) for gap in gaps]
    ledgers = _proposal_ledgers(proposals)

    coverage = {
        "status": "partial_coverage" if plan["target_selection"]["partial_coverage"] else "selected_scope_complete",
        "selected_count": plan["target_selection"]["selected_count"],
        "available_labeled_equation_count": plan["target_selection"]["available_labeled_equation_count"],
        "partial_coverage": plan["target_selection"]["partial_coverage"],
        "gap_count": len(gaps),
        "proposal_count": len(proposals),
        "concrete_repair_count": len(ledgers["concrete_repairs"]),
        "diagnostic_abstention_count": len(ledgers["diagnostic_abstentions"]),
        "target_file_only": True,
        "target_file": path.name,
    }
    result = {
        "tex_path": str(path),
        "source": {"file": path.name, "source_digest": hashlib.sha256(path.read_bytes()).hexdigest()},
        "backend_env": backend_env,
        "backend_provenance": backend,
        "document_inventory": plan["document_inventory"],
        "target_selection": plan["target_selection"],
        "tool_uses": tool_uses,
        "coverage": coverage,
        "gaps": gaps,
        "proposals": proposals,
        "proposal_ledgers": ledgers,
        "source_reports": {"audit_and_propose_fix": fix_report} if fix_report else {},
        "non_claims": [
            {
                "code": "document_rigor_audit_not_document_proof",
                "text": "The report is a rigor gap/proposal ledger, not a proof of the document.",
            },
            {
                "code": "partial_coverage_not_exhaustive",
                "text": "Limited target selection is not an exhaustive full-document audit.",
            },
            {
                "code": "leandojo_not_certificate",
                "text": "LeanDojo proof search is not a certificate unless the reconstructed Lean source passes direct Lean checking without placeholders.",
            },
        ],
    }
    result = attach_contract(result, RIGOR_AUDIT_CONTRACT)
    markdown = render_math_document_rigor_markdown(result)
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


def render_math_document_rigor_markdown(result: dict[str, Any]) -> str:
    """Render a human/agent-readable Markdown rigor report."""
    lines = [
        "# Math Document Rigor Audit",
        "",
        f"Target: `{result.get('tex_path', '')}`",
        "",
        "## Executive Summary",
        "",
        f"- Coverage status: `{result.get('coverage', {}).get('status', '')}`",
        f"- Selected targets: {result.get('coverage', {}).get('selected_count', 0)} / {result.get('coverage', {}).get('available_labeled_equation_count', 0)} labeled equation rows",
        f"- Gaps: {result.get('coverage', {}).get('gap_count', 0)}",
        f"- Proposals: {result.get('coverage', {}).get('proposal_count', 0)}",
        f"- Concrete repairs: {result.get('coverage', {}).get('concrete_repair_count', 0)}",
        f"- Diagnostic abstentions: {result.get('coverage', {}).get('diagnostic_abstention_count', 0)}",
        "- This report is diagnostic and proposal-oriented; it is not a proof of the document.",
        "",
        "## Backend Provenance",
        "",
    ]
    doctor = result.get("backend_provenance", {}).get("doctor", {})
    lean_dojo = doctor.get("capabilities", {}).get("lean_dojo", {}) if isinstance(doctor, dict) else {}
    lines.extend(
        [
            f"- Active Python: `{doctor.get('python', {}).get('executable', '') if isinstance(doctor, dict) else ''}`",
            f"- LeanDojo status: `{lean_dojo.get('status', '')}`",
            f"- LeanDojo environment scope: `{lean_dojo.get('environment_scope', '')}`",
            f"- LeanDojo backend env: `{lean_dojo.get('backend_env', '')}`",
            f"- Certification boundary: {result.get('backend_provenance', {}).get('certification_boundary', '')}",
            "",
            "## Document Inventory",
            "",
        ]
    )
    inventory = result.get("document_inventory", {})
    equation_summary = inventory.get("equation_localization", {})
    hygiene = inventory.get("label_ref_hygiene", {})
    lines.extend(
        [
            f"- Lines: {inventory.get('line_count', 0)}",
            f"- Sections: {inventory.get('section_count', 0)}",
            f"- Equation rows: {equation_summary.get('row_count', 0)}",
            f"- Labeled equation rows: {inventory.get('labeled_equation_count', 0)}",
            f"- Duplicate labels: {len(hygiene.get('duplicate_labels', []))}",
            f"- Missing refs: {len(hygiene.get('missing_refs', []))}",
            "",
            "## Tool Uses",
            "",
            "| Tool | Purpose | Status | Output contract | Arguments |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in result.get("tool_uses", []):
        args = json.dumps(item.get("arguments", {}), sort_keys=True)
        lines.append(
            f"| `{_md(item.get('tool', ''))}` | {_md(item.get('purpose', ''))} | `{_md(item.get('status', ''))}` | `{_md(item.get('output_contract', ''))}` | `{_md(args)}` |"
        )
    ledgers = result.get("proposal_ledgers", {}) if isinstance(result.get("proposal_ledgers"), dict) else {}
    concrete_repairs = ledgers.get("concrete_repairs") if isinstance(ledgers.get("concrete_repairs"), list) else []
    diagnostic_abstentions = ledgers.get("diagnostic_abstentions") if isinstance(ledgers.get("diagnostic_abstentions"), list) else []
    lines.extend(["", "## Concrete Repair Ledger", ""])
    if concrete_repairs:
        for index, proposal in enumerate(concrete_repairs, start=1):
            _append_proposal_markdown(lines, proposal, index=index)
    else:
        lines.append("- No concrete repair payload met the substantive proposal contract.")

    lines.extend(["", "## Diagnostic Abstention Ledger", ""])
    if diagnostic_abstentions:
        for index, proposal in enumerate(diagnostic_abstentions, start=1):
            _append_proposal_markdown(lines, proposal, index=index, diagnostic=True)
    else:
        lines.append("- No diagnostic abstentions were recorded.")

    lines.extend(["", "## Gap And Proposal Ledger", ""])
    proposals_by_gap: dict[str, list[dict[str, Any]]] = {}
    for proposal in result.get("proposals", []):
        for gap_id in proposal.get("gap_ids", []):
            proposals_by_gap.setdefault(str(gap_id), []).append(proposal)
    for index, gap in enumerate(result.get("gaps", []), start=1):
        lines.extend(
            [
                f"### {index}. `{_md(gap.get('label', gap.get('id', 'gap')))}`",
                "",
                f"- Location: `{_md(gap.get('location', ''))}`",
                f"- Classification: `{_md(gap.get('substantive_classification', DIAGNOSTIC_ABSTENTION_CLASS))}`",
                f"- Problem: {_md(gap.get('problem', ''))}",
                f"- Why mathematically problematic: {_md(gap.get('why_mathematically_problematic', gap.get('why', '')))}",
                f"- Evidence refs: {', '.join(f'`{_md(ref)}`' for ref in gap.get('evidence_refs', []))}",
                "",
            ]
        )
        for proposal in proposals_by_gap.get(str(gap.get("id")), []):
            lines.extend(
                [
                    f"- Proposed fix: {_md(proposal.get('proposed_fix', ''))}",
                    f"- Backend evidence: `{_md(proposal.get('backend_evidence', {}).get('status', 'not_certified') if isinstance(proposal.get('backend_evidence'), dict) else 'not_certified')}`",
                    "",
                ]
            )
    lines.extend(["## Non-Claims", ""])
    for item in result.get("non_claims", []):
        lines.append(f"- `{_md(item.get('code', ''))}`: {_md(item.get('text', ''))}")
    lines.append("")
    return "\n".join(lines)


def render_compact_math_document_rigor_markdown(
    result: dict[str, Any],
    *,
    artifact: dict[str, Any] | None = None,
) -> str:
    """Render a bounded all-target rigor summary with detailed artifact linkage."""
    coverage = result.get("coverage") if isinstance(result.get("coverage"), dict) else {}
    source = result.get("source") if isinstance(result.get("source"), dict) else {}
    lines = [
        "# Compact Math Document Rigor Audit",
        "",
        f"Source: `{source.get('file', Path(str(result.get('tex_path', ''))).name)}`",
        f"Source SHA-256: `{source.get('source_digest', '')}`",
        f"Coverage: `{coverage.get('status', '')}`; targets `{coverage.get('selected_count', 0)}`; gaps `{coverage.get('gap_count', 0)}`; concrete repairs `{coverage.get('concrete_repair_count', 0)}`; diagnostic abstentions `{coverage.get('diagnostic_abstention_count', 0)}`",
        "",
        "This is a bounded transport summary. Exact detailed records remain available through `resolve_agent_report`.",
    ]
    if isinstance(artifact, dict):
        lines.extend(
            [
                f"Detailed artifact: `{artifact.get('sha256', '')}` ({artifact.get('byte_count', 0)} bytes; state `{artifact.get('state', '')}`).",
                "",
            ]
        )
    lines.extend(
        [
            "| Label | Relation | Source role | Line |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for target in result.get("target_selection", {}).get("targets", []):
        if not isinstance(target, dict):
            continue
        normalized = target.get("normalized_target") if isinstance(target.get("normalized_target"), dict) else {}
        role = target.get("routing_role") if isinstance(target.get("routing_role"), dict) else {}
        lines.append(
            f"| `{_md(target.get('label', ''))}` | `{_md(normalized.get('kind', 'unavailable'))}` | "
            f"`{_md(role.get('role', target.get('claim_type', 'unsupported_or_ambiguous')) )}` | {target.get('line_start', '')} |"
        )
    lines.extend(["", "## Gap Ledger", "", "| Label | Classification | Problem | Evidence |", "| --- | --- | --- | --- |"])
    for gap in result.get("gaps", []):
        if not isinstance(gap, dict):
            continue
        refs = ", ".join(str(item) for item in gap.get("evidence_refs", []))
        lines.append(
            f"| `{_md(gap.get('label', gap.get('id', '')))}` | "
            f"`{_md(gap.get('substantive_classification', DIAGNOSTIC_ABSTENTION_CLASS))}` | "
            f"{_md(gap.get('problem', ''))} | `{_md(refs)}` |"
        )
    lines.extend(["", "## Role-Specific Obligation Ledger", ""])
    for target in result.get("target_selection", {}).get("targets", []):
        if not isinstance(target, dict):
            continue
        local = [item for item in target.get("local_obligations", []) if isinstance(item, dict)]
        downstream = [item for item in target.get("downstream_integration_obligations", []) if isinstance(item, dict)]
        lines.extend(
            [
                f"### `{_md(target.get('label', 'target'))}`",
                "",
                f"- Local obligations: `{_md([item.get('id') for item in local])}`",
                f"- Downstream-only integration obligations: `{_md([item.get('id') for item in downstream])}`",
                "- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.",
                "",
            ]
        )
    lines.extend(["", "## Boundaries", ""])
    for item in result.get("non_claims", []):
        if isinstance(item, dict):
            lines.append(f"- `{_md(item.get('code', ''))}`: {_md(item.get('text', ''))}")
    lines.append("")
    rendered = "\n".join(lines)
    if len(rendered.encode("utf-8")) > 30_720:
        raise ValueError("compact rigor Markdown exceeds the transport budget")
    return rendered


def _append_proposal_markdown(lines: list[str], proposal: dict[str, Any], *, index: int, diagnostic: bool = False) -> None:
    title = proposal.get("label") or proposal.get("id", "proposal")
    lines.extend(
        [
            f"### {index}. `{_md(title)}`",
            "",
            f"- Location: `{_md(proposal.get('location', ''))}`",
            f"- Problem: {_md(proposal.get('problem', ''))}",
            f"- Why mathematically problematic: {_md(proposal.get('why_mathematically_problematic', ''))}",
            f"- Proposed fix: {_md(proposal.get('proposed_fix', ''))}",
        ]
    )
    if diagnostic:
        lines.append(f"- Why not concrete: {_md(proposal.get('why_not_concrete', ''))}")
        requirements = proposal.get("required_evidence_before_repair")
        if isinstance(requirements, list) and requirements:
            lines.append("- Required evidence before repair:")
            for requirement in requirements:
                lines.append(f"  - {_md(requirement)}")
        _append_actionable_abstention_markdown(lines, proposal.get("actionable_abstention"))
    if proposal.get("assumption_statement"):
        lines.extend(["- Assumption statement:", "", "```latex", str(proposal.get("assumption_statement", "")).strip(), "```"])
    if proposal.get("replacement_latex"):
        lines.extend(["- Replacement LaTeX:", "", "```latex", str(proposal.get("replacement_latex", "")).strip(), "```"])
    if proposal.get("proof_target"):
        lines.append(f"- Proof target: `{_md(proposal.get('proof_target', ''))}`")
    if proposal.get("derivation_plan"):
        lines.append(f"- Derivation route: {_md(proposal.get('derivation_plan', ''))}")
    next_audit = proposal.get("smallest_next_audit")
    if isinstance(next_audit, dict) and next_audit:
        lines.append(
            f"- Smallest next audit: `{_md(next_audit.get('tool', ''))}`"
            f" on `{_md(next_audit.get('label', ''))}` - {_md(next_audit.get('purpose', ''))}"
        )
    backend = proposal.get("backend_evidence")
    if isinstance(backend, dict):
        lines.append(f"- Backend evidence: `{_md(backend.get('status', 'not_certified'))}` - {_md(backend.get('reason', ''))}")
    refs = proposal.get("evidence_refs")
    if isinstance(refs, list) and refs:
        lines.append(f"- Evidence refs: {', '.join(f'`{_md(ref)}`' for ref in refs)}")
    lines.append("")


def _append_actionable_abstention_markdown(lines: list[str], payload: Any) -> None:
    if not isinstance(payload, dict) or not payload:
        return
    lines.append(f"- Blocker kind: `{_md(payload.get('blocker_kind', ''))}`")
    safe_wording = payload.get("safe_wording")
    if safe_wording:
        lines.append(f"- Safe wording: {_md(safe_wording)}")
    obligations = payload.get("missing_obligations")
    if isinstance(obligations, list) and obligations:
        lines.append("- Mathematically missing obligations:")
        for obligation in obligations:
            if not isinstance(obligation, dict):
                continue
            lines.append(
                f"  - `{_md(obligation.get('id', 'obligation'))}`"
                f" ({_md(obligation.get('kind', 'condition'))}): {_md(obligation.get('mathematically_missing', ''))}"
            )
            lines.append(f"    Why missing: {_md(obligation.get('why_missing', ''))}")
            lines.append(f"    Closes: {_md(obligation.get('closes', ''))}")
    assumption_sets = payload.get("possible_assumption_sets")
    if isinstance(assumption_sets, list) and assumption_sets:
        lines.append("- Possible sufficient assumption sets:")
        for item in assumption_sets:
            if not isinstance(item, dict):
                continue
            lines.append(f"  - `{_md(item.get('id', 'assumption_set'))}` ({_md(item.get('role', 'candidate'))}): {_md(item.get('closes', ''))}")
            assumptions = item.get("assumptions")
            if isinstance(assumptions, list):
                for assumption in assumptions:
                    lines.append(f"    - {_md(assumption)}")
    route = payload.get("how_derivation_can_work")
    if isinstance(route, list) and route:
        lines.append("- How the derivation can work under the assumptions:")
        for step in route:
            if isinstance(step, dict):
                lines.append(f"  - {_md(step.get('step', 'step'))}: {_md(step.get('detail', ''))}")
    next_audit = payload.get("next_audit")
    if isinstance(next_audit, dict) and next_audit:
        lines.append(f"- Actionable abstention next audit: `{_md(next_audit.get('tool', ''))}` - {_md(next_audit.get('purpose', ''))}")
    non_claim = payload.get("non_claim")
    if non_claim:
        lines.append(f"- Abstention non-claim: {_md(non_claim)}")


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
