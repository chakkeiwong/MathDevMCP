from __future__ import annotations

"""Audit a document target and write a conservative fix-proposal report."""

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Any

from .contracts import attach_contract, contract_metadata, success_result
from .high_level_contracts import (
    action,
    default_non_claims,
    evidence_entry,
    high_level_result,
    refresh_evidence_ledger,
    validate_high_level_result,
    veto_reason,
)
from .latex_index import build_index
from .math_debugging import backend_attempt_record
from .math_debugging_router import route_math_obligation
from .proof_audit_v2 import audit_derivation_v2_for_label
from .propose_fix import REPAIR_NON_CLAIM_CODE, REPAIR_NON_CLAIM_TEXT, proposal_agent_handoff, propose_fix


AUDIT_FIX_REPORT_CONTRACT = "audit_fix_report_result"
AUDIT_FIX_REPORT_NON_CLAIM_CODE = "audit_fix_report_not_applied_or_certified"
AUDIT_FIX_REPORT_NON_CLAIM_TEXT = (
    "The audit-and-fix report is diagnostic guidance only; it does not apply edits, "
    "verify repaired text, or certify mathematical correctness."
)
DEFAULT_DISCOVERY_LABEL_KINDS = (
    "proposition",
    "theorem",
    "lemma",
    "corollary",
    "equation",
    "align",
    "alignat",
    "gather",
    "multline",
)
DEFAULT_VALIDATION_BACKEND_ORDER = ("lean", "sage", "sympy")
VALIDATION_BACKENDS = {"lean", "sage", "sympy"}
VALIDATION_POLICY_REQUIRE_ATTEMPT = "require_attempt_when_encodable"


@dataclass(frozen=True)
class ToolUseRecord:
    tool: str
    arguments: dict[str, Any]
    purpose: str
    status: str
    output_contract: str | None = None


@dataclass(frozen=True)
class AuditFixReport:
    status: str
    question: str
    source: dict[str, Any]
    coverage: dict[str, Any]
    tool_uses: list[dict[str, Any]]
    audited_evidence: list[dict[str, Any]]
    proposal_changes: list[dict[str, Any]]
    proposal_details: list[dict[str, Any]]
    validation: dict[str, Any]
    proposal: dict[str, Any]
    markdown: str
    output_path: str | None
    non_claims: list[dict[str, Any]]
    next_actions: list[dict[str, Any]]
    agent_handoff: dict[str, Any]
    certification_boundary: str
    metadata: dict[str, str]


def _label_audit_failure(root: str, label: str, reason: str) -> dict[str, Any]:
    return attach_contract(
        {
            "label": label,
            "doc_root": str(Path(root).resolve()),
            "status": "inconclusive",
            "reason": reason,
            "counts": {"total": 0, "verified": 0, "mismatch": 0, "unverified": 0, "inconclusive": 0},
            "substatus_counts": {},
            "high_priority_actions": [],
            "obligations": [],
            "parser_policy": {},
            "base_audit_status": "inconclusive",
            "doc_context": {},
        },
        "proof_audit_v2_result",
    )


def _audit_label_task(task: tuple[int, str, str, bool, int, int, bool, str, str, str | None, str | None]) -> dict[str, Any]:
    index, root, label, paragraph_context, context_before, context_after, summary_only, backend, task_context, file, source_digest = task
    args = {
        "root": root,
        "label": label,
        "paragraph_context": paragraph_context,
        "before": context_before,
        "after": context_after,
        "summary_only": summary_only,
        "backend": backend,
        "task_context": task_context,
        "file": file,
        "source_digest": source_digest,
    }
    try:
        audit = audit_derivation_v2_for_label(
            root,
            label,
            before=context_before,
            after=context_after,
            paragraph_context=paragraph_context,
            summary_only=summary_only,
            backend=backend,
            task_context=task_context,
            file=file,
            source_digest=source_digest,
        )
    except Exception as exc:  # pragma: no cover - exercised through structured failure contract.
        audit = _label_audit_failure(root, label, f"audit_derivation_v2_label failed: {exc}")
    return {
        "index": index,
        "audit": audit,
        "tool_use": asdict(
            ToolUseRecord(
                tool="audit_derivation_v2_label",
                arguments=args,
                purpose=f"Generate local derivation audit evidence for `{label}`.",
                status=str(audit.get("status", "unknown")),
                output_contract=_metadata_contract(audit),
            )
        ),
    }


def _ordered_label_audits(
    root: str,
    labels: list[str],
    *,
    paragraph_context: bool,
    context_before: int,
    context_after: int,
    summary_only: bool,
    backend: str,
    task_context: str,
    workers: int,
    file: str | None = None,
    source_digest: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not labels:
        return [], []
    normalized_workers = max(1, int(workers or 1))
    tasks = [
        (index, root, label, paragraph_context, context_before, context_after, summary_only, backend, task_context, file, source_digest)
        for index, label in enumerate(labels)
    ]
    if normalized_workers == 1 or len(tasks) == 1:
        results = [_audit_label_task(task) for task in tasks]
    else:
        results = []
        with ProcessPoolExecutor(max_workers=min(normalized_workers, len(tasks))) as executor:
            future_to_task = {executor.submit(_audit_label_task, task): task for task in tasks}
            for future in as_completed(future_to_task):
                index, task_root, label, _, _, _, _, _, _, task_file, task_digest = future_to_task[future]
                try:
                    results.append(future.result())
                except Exception as exc:  # pragma: no cover - protects deterministic parent behavior.
                    audit = _label_audit_failure(task_root, label, f"audit worker failed: {exc}")
                    args = {
                        "root": task_root,
                        "label": label,
                        "paragraph_context": paragraph_context,
                        "before": context_before,
                        "after": context_after,
                        "summary_only": summary_only,
                        "backend": backend,
                        "task_context": task_context,
                        "file": task_file,
                        "source_digest": task_digest,
                    }
                    results.append(
                        {
                            "index": index,
                            "audit": audit,
                            "tool_use": asdict(
                                ToolUseRecord(
                                    tool="audit_derivation_v2_label",
                                    arguments=args,
                                    purpose=f"Generate local derivation audit evidence for `{label}`.",
                                    status=str(audit.get("status", "unknown")),
                                    output_contract=_metadata_contract(audit),
                                )
                            ),
                        }
                    )
    ordered = sorted(results, key=lambda item: int(item.get("index", 0)))
    return [item["audit"] for item in ordered], [item["tool_use"] for item in ordered]


def _metadata_contract(payload: dict[str, Any]) -> str | None:
    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return None


def _compact(value: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: value[field] for field in fields if field in value and value[field] not in (None, [], {})}


def _markdown_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _report_status(proposed_changes: list[dict[str, Any]], audited_evidence: list[dict[str, Any]]) -> str:
    if proposed_changes:
        return "proposal_ready"
    if audited_evidence:
        return "no_proposal"
    return "needs_evidence"


def _source_context(source: dict[str, Any] | None, root: str | None, labels: list[str]) -> dict[str, Any]:
    result = dict(source or {})
    if root and "root" not in result:
        result["root"] = root
    if labels and "labels" not in result:
        result["labels"] = labels
    return result


def _normalize_label_kinds(label_kinds: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if label_kinds is None:
        return DEFAULT_DISCOVERY_LABEL_KINDS
    normalized = tuple(str(item).strip() for item in label_kinds if str(item).strip())
    return normalized or DEFAULT_DISCOVERY_LABEL_KINDS


def _discover_audit_labels(
    root: str,
    *,
    target_file: str | None = None,
    source_digest: str | None = None,
    label_kinds: list[str] | tuple[str, ...] | None = None,
    label_limit: int | None = None,
) -> tuple[list[str], dict[str, Any]]:
    kinds = _normalize_label_kinds(label_kinds)
    root_path = Path(root).resolve()
    index = build_index(root_path)
    target_rel: str | None = None
    if target_file:
        target_path = Path(target_file)
        if not target_path.is_absolute():
            target_path = root_path / target_path
        target_rel = str(target_path.resolve().relative_to(root_path))
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for block in index.get("blocks", []):
        if not isinstance(block, dict):
            continue
        label = block.get("label")
        kind = block.get("kind")
        if target_rel and block.get("file") != target_rel:
            continue
        if not isinstance(label, str) or not label or kind not in kinds or label in seen:
            continue
        seen.add(label)
        candidates.append(
            _compact(
                {
                    "label": label,
                    "kind": kind,
                    "file": block.get("file"),
                    "line_start": block.get("line_start"),
                    "section_path": block.get("section_path"),
                    "title": block.get("title"),
                },
                ("label", "kind", "file", "line_start", "section_path", "title"),
            )
        )
    effective_limit = None if label_limit is None or label_limit <= 0 else label_limit
    selected = candidates if effective_limit is None else candidates[:effective_limit]
    skipped = candidates[len(selected) :]
    coverage = {
        "mode": "whole_document",
        "root": str(root_path),
        "target_file": target_rel,
        "label_kinds": list(kinds),
        "discovered_label_count": len(candidates),
        "audited_label_count": len(selected),
        "skipped_label_count": len(skipped),
        "audit_complete": len(skipped) == 0,
        "limit": effective_limit,
        "audited_labels": selected,
        "skipped_labels_preview": skipped[:10],
        "index": _compact(
            {
                "n_blocks": index.get("n_blocks"),
                "n_labels": index.get("n_labels"),
                "n_equation_rows": index.get("n_equation_rows"),
                "diagnostics": index.get("diagnostics"),
            },
            ("n_blocks", "n_labels", "n_equation_rows", "diagnostics"),
        ),
    }
    return [str(item["label"]) for item in selected], coverage


def _explicit_coverage(
    root: str | None,
    labels: list[str],
    *,
    target_file: str | None = None,
    source_digest: str | None = None,
) -> dict[str, Any]:
    return {
        "mode": "explicit_labels",
        "root": str(Path(root).resolve()) if root else None,
        "target_file": target_file,
        "source_digest": source_digest,
        "discovered_label_count": len(labels),
        "audited_label_count": len(labels),
        "skipped_label_count": 0,
        "audit_complete": True,
        "limit": None,
        "audited_labels": [{"label": label} for label in labels],
        "skipped_labels_preview": [],
    }


def _summarize_audit(evidence: dict[str, Any]) -> dict[str, Any]:
    extraction = evidence.get("target_extraction")
    targets = extraction.get("targets", []) if isinstance(extraction, dict) else []
    canonical = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
    return _compact(
        {
            "label": evidence.get("label"),
            "status": evidence.get("status"),
            "contract": _metadata_contract(evidence),
            "reason": evidence.get("reason") or evidence.get("answer"),
            "canonical_target": _compact(
                {
                    "target": canonical.get("target"),
                    "file": canonical.get("file"),
                    "label": canonical.get("label"),
                    "line_start": canonical.get("line_start"),
                    "line_end": canonical.get("line_end"),
                    "obligation_id": canonical.get("obligation_id"),
                    "obligation_digest": canonical.get("obligation_digest"),
                    "source_digest": canonical.get("label_scoped_obligation", {}).get("document", {}).get("source_digest"),
                    "normalized_target": canonical.get("normalized_target"),
                    "routing_role": canonical.get("routing_role"),
                    "specialist_execution": canonical.get("specialist_execution"),
                    "target_ingress": "validated_label_scoped_obligation",
                },
                ("target", "file", "label", "line_start", "line_end", "obligation_id", "obligation_digest", "source_digest", "normalized_target", "routing_role", "specialist_execution", "target_ingress"),
            ) if canonical else None,
        },
        ("label", "status", "contract", "reason", "canonical_target"),
    )


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _split_proof_audit_ref(ref: str) -> tuple[str | None, str | None]:
    prefix = "proof_audit_v2:"
    if not ref.startswith(prefix):
        return None, None
    tail = ref[len(prefix) :]
    if ":obligation_" in tail:
        label, _, obligation_id = tail.rpartition(":")
        return label, obligation_id
    return tail, None


def _problem_text(kind: str, target: str, summary: str, rationale: str, source_text: str) -> str:
    if kind == "add_or_verify_assumption":
        return f"Missing constraint `{target}`."
    if kind == "split_derivation_step":
        return "The derivation row is not split into a safe proof obligation."
    if kind == "add_review_boundary":
        return "The claim still needs human review before certification."
    if kind == "add_diagnostic_check":
        return f"No bounded diagnostic has been added for `{target}`."
    if kind == "fix_parser_provenance":
        return "Parser provenance is not strong enough for certification."
    if kind == "collect_more_evidence":
        return "The available evidence is not enough for a concrete repair yet."
    return source_text or rationale or summary or "Review this line carefully."


def _detail_is_evidence_only(kind: str) -> bool:
    return kind == "collect_more_evidence"


def _is_latex_math_fragment(text: str) -> bool:
    stripped = str(text or "").strip()
    if not stripped:
        return False
    if stripped in {r"\begin{align}", r"\begin{equation}", r"\end{align}", r"\end{equation}", r"\[", r"\]"}:
        return False
    if stripped.startswith((r"\begin{", r"\end{")):
        return False
    if stripped.startswith("where ") or stripped.startswith(r"\text"):
        return False
    return any(marker in stripped for marker in ("\\", "=", "^", "_", "+", "-", r"\max", r"\E"))


def _source_lines_from_doc_context(evidence: dict[str, Any]) -> list[tuple[int, str]]:
    doc_context = evidence.get("doc_context") if isinstance(evidence.get("doc_context"), dict) else {}
    paragraphs = doc_context.get("paragraphs")
    if isinstance(paragraphs, list) and paragraphs:
        lines: list[tuple[int, str]] = []
        for paragraph in paragraphs:
            if not isinstance(paragraph, dict):
                continue
            start = paragraph.get("line_start")
            text = paragraph.get("text")
            if not isinstance(start, int) or not isinstance(text, str):
                continue
            for offset, line in enumerate(text.splitlines()):
                lines.append((start + offset, line))
        return lines
    excerpt = doc_context.get("excerpt")
    if isinstance(excerpt, list):
        return [
            (item.get("line", 0), str(item.get("text", "")))
            for item in excerpt
            if isinstance(item, dict) and isinstance(item.get("line"), int)
        ]
    return []


def _clean_math_line(line: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", line).strip()
    text = text.replace("&", "").strip()
    text = text.rstrip(",.")
    return text.strip()


def _reconstruct_split_align_equation(
    evidence: dict[str, Any],
    obligation: dict[str, Any],
) -> dict[str, Any] | None:
    provenance = obligation.get("provenance") if isinstance(obligation.get("provenance"), dict) else {}
    line_start = provenance.get("line_start")
    if not isinstance(line_start, int):
        return None
    lines = _source_lines_from_doc_context(evidence)
    line_map = {line_no: text for line_no, text in lines}
    if line_start not in line_map:
        root_value = evidence.get("doc_root")
        file_value = provenance.get("file")
        if isinstance(root_value, str) and isinstance(file_value, str):
            root_path = Path(root_value).resolve()
            source_path = (root_path / file_value).resolve()
            if source_path.is_file() and (source_path == root_path or root_path in source_path.parents):
                line_map = {
                    index: text
                    for index, text in enumerate(source_path.read_text(encoding="utf-8").splitlines(), start=1)
                }
    if line_start not in line_map:
        return None
    operator = _clean_math_line(line_map[line_start])
    if operator != "=":
        return None
    previous_terms: list[str] = []
    for line_no in range(line_start - 1, min(line_start - 5, 0), -1):
        cleaned = _clean_math_line(line_map.get(line_no, ""))
        if not cleaned:
            continue
        if cleaned in {r"\begin{align}", r"\begin{equation}", r"\[", "="}:
            continue
        previous_terms.insert(0, cleaned)
        break
    following_terms: list[str] = []
    for line_no in range(line_start + 1, line_start + 8):
        raw = line_map.get(line_no)
        if raw is None:
            continue
        if "\\\\" in raw or r"\end{align}" in raw or r"\end{equation}" in raw:
            break
        cleaned = _clean_math_line(raw)
        if not cleaned or cleaned in {"=", r"\begin{align}", r"\begin{equation}"}:
            continue
        following_terms.append(cleaned)
        if len(following_terms) >= 3 and not any(marker in " ".join(following_terms) for marker in (r"\left[", r"\left(", r"\left\{")):
            break
    if not previous_terms or not following_terms:
        return None
    lhs = previous_terms[-1]
    rhs = "\n  ".join(following_terms)
    equation = f"{lhs} = {rhs}"
    replacement = "\\begin{equation}\n  " + lhs + "\n  =\n  " + "\n  ".join(following_terms) + "\n\\end{equation}"
    label = str(evidence.get("label") or "")
    if label == "prop:interior-foc":
        derivation_obligation = (
            f"Differentiate the local objective with respect to the corresponding interior choice and show `{equation}`."
        )
    else:
        derivation_obligation = f"Justify the reconstructed equality `{equation}` from the surrounding proposition/proof context."
    return {
        "lhs": lhs,
        "rhs": rhs,
        "equation": equation,
        "replacement_latex": replacement,
        "derivation_obligation": derivation_obligation,
        "certification_boundary": (
            "This is a context reconstruction for review; the equality still needs a derivation "
            "or a stronger symbolic/formal backend."
        ),
    }


def _math_fix_text(math_fix: dict[str, Any] | None, fallback: str) -> str:
    if not isinstance(math_fix, dict):
        return fallback
    equation = math_fix.get("equation")
    obligation = math_fix.get("derivation_obligation")
    if equation and obligation:
        return f"Replace the split row with `{equation}`. Then prove: {obligation}"
    if equation:
        return f"Replace the split row with `{equation}`."
    return fallback


def _source_line_for_obligation(evidence: dict[str, Any] | None, obligation: dict[str, Any] | None) -> str:
    if not isinstance(evidence, dict) or not isinstance(obligation, dict):
        return ""
    provenance = obligation.get("provenance") if isinstance(obligation.get("provenance"), dict) else {}
    line_start = provenance.get("line_start")
    if not isinstance(line_start, int):
        return ""
    line_map = {line_no: text for line_no, text in _source_lines_from_doc_context(evidence)}
    return str(line_map.get(line_start, "")).strip()


def _display_source_text(source_text: str, *, kind: str, has_math_fix: bool = False) -> str:
    text = str(source_text or "").strip()
    if not text:
        return ""
    if kind == "split_derivation_step" or has_math_fix:
        if _clean_math_line(text) == "=":
            return ""
        if text == "The row could not be extracted as a safe proof obligation.":
            return ""
    return text


def _resolve_proof_audit_obligation(
    audited_evidence: list[dict[str, Any]],
    ref: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    label, obligation_id = _split_proof_audit_ref(ref)
    if not label:
        return None, None
    for evidence in audited_evidence:
        if not isinstance(evidence, dict) or evidence.get("label") != label:
            continue
        if not obligation_id:
            return evidence, None
        obligations = evidence.get("obligations") if isinstance(evidence.get("obligations"), list) else []
        for obligation in obligations:
            if isinstance(obligation, dict) and obligation.get("id") == obligation_id:
                return evidence, obligation
        return evidence, None
    return None, None


def _gap_status_text(obligation: dict[str, Any]) -> str:
    status = str(obligation.get("status") or "unknown")
    substatus = str(obligation.get("substatus") or "unknown")
    route = str(obligation.get("route") or "unknown")
    matrix_status = str(obligation.get("matrix_ir_status") or "unknown")
    reason = str(obligation.get("reason") or "No reason was recorded.")
    return (
        f"Proof-audit v2 returned `{status}` with substatus `{substatus}` on route `{route}` "
        f"and matrix-IR status `{matrix_status}`. {reason}"
    )


def _proof_target_from_detail(detail: dict[str, Any], obligation: dict[str, Any]) -> str:
    math_fix = detail.get("math_fix")
    if isinstance(math_fix, dict) and math_fix.get("equation"):
        return str(math_fix["equation"])
    lhs = str(obligation.get("lhs") or "").strip()
    rhs = str(obligation.get("rhs") or "").strip()
    if lhs and rhs:
        return f"{lhs} = {rhs}"
    return str(detail.get("source_text") or "").strip()


def _derivation_plan_for_gap(evidence: dict[str, Any], detail: dict[str, Any], obligation: dict[str, Any]) -> str:
    label = str(evidence.get("label") or obligation.get("label") or "")
    proof_target = _proof_target_from_detail(detail, obligation)
    if label == "prop:interior-foc":
        variable = "k'" if "dk'" in proof_target or "V^\\star_k" in proof_target else "b'" if "db'" in proof_target or "V^\\star_b" in proof_target else "the interior choice"
        return (
            "Add a local derivation with objective "
            "`J(k',b')=\\bar e(k,k',b,b',z)+\\eta(\\bar e(k,k',b,b',z))"
            "+\\beta \\E[V^\\star(k',b',z')\\mid z]`. "
            f"Use interiority to set `\\partial J/\\partial {variable}=0`, use "
            "`1+\\eta'(\\bar e)=m(\\bar e)`, and justify differentiating the conditional "
            f"expectation so the target becomes `{proof_target}`."
        )
    if label == "prop:risky-pricing":
        return (
            "Add a proof step defining the lender payoff as "
            "`D(k',b',z')R(k',z')+(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))`. "
            "Then impose the zero-profit condition `b'(1+r)=\\E[payoff\\mid z]` "
            f"to obtain `{proof_target}`."
        )
    math_fix = detail.get("math_fix")
    if isinstance(math_fix, dict) and math_fix.get("derivation_obligation"):
        return str(math_fix["derivation_obligation"])
    return "Formalize this local proof obligation with explicit assumptions, then rerun proof-audit v2 on the same label."


def _non_actionable_problem(detail: dict[str, Any], obligation: dict[str, Any] | None) -> str:
    kind = str(detail.get("kind") or "")
    if kind == "add_or_verify_assumption":
        return (
            "The audit reports a missing assumption or shape constraint, but the current tools have not "
            "derived the exact assumption statement to insert here."
        )
    if kind == "add_review_boundary":
        return (
            "The audit reports that this claim needs formalization or human review; that is a certification "
            "gap, not a document edit by itself."
        )
    if kind == "fix_parser_provenance":
        return "Parser provenance must be fixed before a concrete document repair can be proposed."
    if obligation is not None and not _is_latex_math_fragment(_proof_target_from_detail(detail, obligation)):
        return "The localized source is prose or an incomplete fragment, so no concrete mathematical replacement is available."
    return "The report entry is not concrete enough to appear as an applied-document repair."


def _detail_has_concrete_fix(detail: dict[str, Any]) -> bool:
    if not isinstance(detail, dict) or detail.get("evidence_only"):
        return False
    kind = str(detail.get("kind") or "")
    math_fix = detail.get("math_fix")
    if isinstance(math_fix, dict) and math_fix.get("replacement_latex"):
        return True
    if detail.get("replacement_latex") or detail.get("assumption_statement"):
        return True
    return False


def _normalize_backend_order(backend_order: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if backend_order is None:
        return DEFAULT_VALIDATION_BACKEND_ORDER
    normalized: list[str] = []
    for item in backend_order:
        backend = str(item).strip().lower()
        if backend in VALIDATION_BACKENDS and backend not in normalized:
            normalized.append(backend)
    return tuple(normalized or DEFAULT_VALIDATION_BACKEND_ORDER)


def _validation_target_from_detail(detail: dict[str, Any]) -> dict[str, Any]:
    math_fix = detail.get("math_fix") if isinstance(detail.get("math_fix"), dict) else {}
    lhs = str(math_fix.get("lhs") or "").strip()
    rhs = str(math_fix.get("rhs") or "").strip()
    proof_target = str(detail.get("proof_target") or math_fix.get("equation") or "").strip()
    if lhs and rhs:
        return {"status": "target_ready", "source": "math_fix", "lhs": lhs, "rhs": rhs, "proof_target": proof_target or f"{lhs} = {rhs}"}
    if proof_target and "=" in proof_target:
        left, right = proof_target.split("=", 1)
        lhs = left.strip()
        rhs = right.strip()
        if lhs and rhs:
            return {"status": "target_ready", "source": "proof_target", "lhs": lhs, "rhs": rhs, "proof_target": proof_target}
    return {
        "status": "not_encodable",
        "source": "none",
        "lhs": "",
        "rhs": "",
        "proof_target": proof_target,
        "reason": "No structured lhs/rhs proof target was available for backend validation.",
    }


def _lean_source_from_detail(detail: dict[str, Any]) -> str | None:
    lean_source = detail.get("lean_source")
    if isinstance(lean_source, str) and lean_source.strip():
        return lean_source
    math_fix = detail.get("math_fix") if isinstance(detail.get("math_fix"), dict) else {}
    lean_source = math_fix.get("lean_source")
    if isinstance(lean_source, str) and lean_source.strip():
        return lean_source
    return None


def _not_encodable_attempt(backend: str, reason: str) -> dict[str, Any]:
    return backend_attempt_record(
        backend=backend,
        status="not_encodable",
        reason=reason,
        severity="diagnostic",
    )


def _validation_attempts_for_target(
    detail: dict[str, Any],
    target: dict[str, Any],
    backend_order: tuple[str, ...],
) -> list[dict[str, Any]]:
    if target.get("status") != "target_ready":
        return [
            _not_encodable_attempt(
                backend,
                str(target.get("reason") or "No structured lhs/rhs proof target was available for backend validation."),
            )
            for backend in backend_order
        ]
    lhs = str(target.get("lhs") or "")
    rhs = str(target.get("rhs") or "")
    attempts: list[dict[str, Any]] = []
    for backend in backend_order:
        if backend == "lean":
            lean_source = _lean_source_from_detail(detail)
            if not lean_source:
                attempts.append(
                    _not_encodable_attempt(
                        "lean",
                        "Lean validation requires explicit placeholder-free Lean source; this pass does not synthesize Lean proof scripts.",
                    )
                )
                continue
            route = route_math_obligation(lhs, rhs, backend="lean", lean_source=lean_source)
            if isinstance(route.get("backend_attempt"), dict):
                attempts.append(route["backend_attempt"])
            continue
        if backend == "sage":
            route = route_math_obligation(lhs, rhs, backend="sage")
            attempt = route.get("backend_attempt") if isinstance(route, dict) else None
            if isinstance(attempt, dict):
                attempts.append(
                    {
                        **attempt,
                        "severity": "diagnostic",
                        "reason": (
                            f"{attempt.get('reason', 'Sage route completed.')} "
                            "Sage is recorded as attempted only; this pass has no certifying Sage proof adapter."
                        ),
                    }
                )
            continue
        if backend == "sympy":
            route = route_math_obligation(lhs, rhs, backend="sympy")
            attempt = route.get("backend_attempt") if isinstance(route, dict) else None
            if isinstance(attempt, dict) and attempt.get("backend") == "sympy":
                attempts.append(attempt)
            elif isinstance(attempt, dict):
                attempts.append(
                    backend_attempt_record(
                        backend="sympy",
                        status=str(route.get("status", "not_encodable")),
                        reason=f"SymPy validation was not attempted: {attempt.get('reason', 'router rejected the target')}",
                        evidence=[attempt],
                        severity="diagnostic",
                    )
                )
    return attempts


def _validation_status(attempts: list[dict[str, Any]]) -> tuple[str, str]:
    for attempt in attempts:
        if attempt.get("status") == "refuted" and attempt.get("severity") == "blocking":
            return "refuted", str(attempt.get("reason") or "A deterministic backend refuted the target.")
    for attempt in attempts:
        if attempt.get("status") == "proved" and attempt.get("severity") == "certifying":
            return "verified", str(attempt.get("reason") or "A deterministic backend certified the target.")
    if not attempts:
        return "not_encodable", "No backend validation attempt was produced."
    if all(attempt.get("status") == "not_encodable" for attempt in attempts):
        return "not_encodable", "No configured backend could encode this proposed fix target."
    return "attempted_not_certified", "Configured backends were attempted, but none certified or refuted this proposed fix target."


def _validate_proposal_details(
    proposal_details: list[dict[str, Any]],
    *,
    certifier_policy: str,
    backend_order: tuple[str, ...],
) -> dict[str, Any]:
    counts: dict[str, int] = {}
    validated = 0
    for detail in proposal_details:
        if not isinstance(detail, dict):
            continue
        if not (_detail_has_concrete_fix(detail) or detail.get("proof_target") or isinstance(detail.get("math_fix"), dict)):
            continue
        target = _validation_target_from_detail(detail)
        attempts = _validation_attempts_for_target(detail, target, backend_order)
        status, reason = _validation_status(attempts)
        validation = {
            "policy": certifier_policy,
            "target": target,
            "backend_order": list(backend_order),
            "backend_attempts": attempts,
            "status": status,
            "reason": reason,
            "certification_boundary": (
                "Only certifying deterministic backend evidence validates a proposed fix. "
                "Lean certifies only explicit placeholder-free Lean source. Sage is attempted only in this pass."
            ),
        }
        detail["validation"] = validation
        counts[status] = counts.get(status, 0) + 1
        validated += 1
    return {
        "enabled": True,
        "policy": certifier_policy,
        "backend_order": list(backend_order),
        "validated_detail_count": validated,
        "status_counts": counts,
    }


def _build_non_actionable_gap_details(
    audited_evidence: list[dict[str, Any]],
    proposal_details: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for detail in proposal_details:
        if not isinstance(detail, dict) or detail.get("evidence_only") or _detail_has_concrete_fix(detail):
            continue
        ref = str(detail.get("evidence_ref") or "")
        evidence, obligation = _resolve_proof_audit_obligation(audited_evidence, ref)
        if not isinstance(evidence, dict):
            continue
        provenance = obligation.get("provenance", {}) if isinstance(obligation, dict) else {}
        canonical_proof_target = (
            isinstance(obligation, dict)
            and provenance.get("target_ingress") == "validated_label_scoped_obligation"
            and bool(obligation.get("lhs"))
            and bool(obligation.get("rhs"))
        )
        if canonical_proof_target:
            proof_target = _proof_target_from_detail(detail, obligation)
            problem = "The complete source-bound target is localized but remains uncertified."
            key = (ref, problem)
            if key in seen:
                continue
            seen.add(key)
            gaps.append(
                {
                    "kind": "prove_reconstructed_obligation",
                    "target": detail.get("target", obligation.get("id", "obligation")),
                    "label": detail.get("label", evidence.get("label", "source")),
                    "location": detail.get("location", "local context"),
                    "line_start": detail.get("line_start"),
                    "section_path": detail.get("section_path", []),
                    "problem": problem,
                    "summary": "Prove the complete canonical source obligation before treating it as verified.",
                    "rationale": _gap_status_text(obligation),
                    "source_text": detail.get("source_text", ""),
                    "action": "Prove or formalize the canonical source obligation.",
                    "proposed_fix": (
                        "Formalize the exact source-bound target, rerun a suitable deterministic backend, "
                        f"and retain the source digest and obligation digest for `{evidence.get('label', '')}`."
                    ),
                    "proof_target": proof_target,
                    "derivation_plan": _derivation_plan_for_gap(evidence, detail, obligation),
                    "math_fix": None,
                    "evidence_only": True,
                    "evidence_ref": ref,
                }
            )
            continue
        problem = _non_actionable_problem(detail, obligation)
        key = (ref, problem)
        if key in seen:
            continue
        seen.add(key)
        proof_target = _proof_target_from_detail(detail, obligation) if isinstance(obligation, dict) else str(detail.get("source_text") or "")
        gap = {
            "kind": "concretize_before_fix",
            "target": detail.get("target", "obligation"),
            "label": detail.get("label", evidence.get("label", "source")),
            "location": detail.get("location", "local context"),
            "line_start": detail.get("line_start"),
            "section_path": detail.get("section_path", []),
            "problem": problem,
            "summary": "Concretize this diagnostic before presenting it as a repair.",
            "rationale": _gap_status_text(obligation) if isinstance(obligation, dict) else str(detail.get("rationale") or ""),
            "source_text": detail.get("source_text", ""),
            "action": "Derive an explicit assumption, replacement equation, or proof target first.",
            "proposed_fix": (
                "Do not edit the document from this item alone. First produce a concrete assumption statement, "
                "replacement LaTeX, or proof obligation tied to the source line."
            ),
            "proof_target": proof_target if _is_latex_math_fragment(proof_target) else "",
            "derivation_plan": (
                "Use the referenced proof-audit obligation to derive a concrete local obligation; if the source "
                "is prose, refine the parser/provenance before proposing an edit."
            ),
            "evidence_only": True,
            "evidence_ref": ref,
        }
        gaps.append(gap)
    return gaps


def _build_evidence_gap_details(
    audited_evidence: list[dict[str, Any]],
    proposal_details: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for detail in proposal_details:
        if not isinstance(detail, dict) or detail.get("evidence_only") or not _detail_has_concrete_fix(detail):
            continue
        ref = str(detail.get("evidence_ref") or "")
        evidence, obligation = _resolve_proof_audit_obligation(audited_evidence, ref)
        if not isinstance(evidence, dict) or not isinstance(obligation, dict):
            continue
        status = str(obligation.get("status") or "")
        if status in {"verified", "mismatch"}:
            continue
        key = (ref, str(detail.get("target") or ""))
        if key in seen:
            continue
        seen.add(key)
        proof_target = _proof_target_from_detail(detail, obligation)
        safe_proof_target = proof_target if _is_latex_math_fragment(proof_target) else ""
        derivation_plan = _derivation_plan_for_gap(evidence, detail, obligation)
        proposed_fix = (
            "Add the derivation step described below, with the stated regularity/interiority assumptions, "
            f"then rerun `audit_derivation_v2_label` for `{evidence.get('label', '')}`."
        )
        source_line = _display_source_text(
            _source_line_for_obligation(evidence, obligation),
            kind=str(detail.get("kind") or ""),
            has_math_fix=isinstance(detail.get("math_fix"), dict),
        )
        gaps.append(
            {
                "kind": "prove_reconstructed_obligation",
                "target": detail.get("target", obligation.get("id", "obligation")),
                "label": detail.get("label", obligation.get("label", "source")),
                "location": detail.get("location", "local context"),
                "line_start": detail.get("line_start"),
                "section_path": detail.get("section_path", []),
                "problem": (
                    "The report has a concrete proof target, but proof-audit v2 has not certified the "
                    "derivation for that target."
                ),
                "summary": "Prove the reconstructed local obligation before treating the repair as verified.",
                "rationale": _gap_status_text(obligation),
                "source_text": source_line or detail.get("source_text", ""),
                "action": "Prove or formalize the reconstructed obligation.",
                "proposed_fix": proposed_fix,
                "proof_target": safe_proof_target,
                "derivation_plan": derivation_plan,
                "math_fix": detail.get("math_fix"),
                "evidence_only": True,
                "evidence_ref": ref,
            }
        )
    return gaps


def _build_plain_language_details(
    audited_evidence: list[dict[str, Any]],
    proposed_changes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    evidence_index = {item.get("label"): item for item in audited_evidence if isinstance(item, dict) and isinstance(item.get("label"), str)}
    seen: set[tuple[str, str, str, str]] = set()
    priority = {"split_derivation_step": 0, "add_or_verify_assumption": 1, "add_diagnostic_check": 2}
    ordered_changes = [
        item[1]
        for item in sorted(
            enumerate(proposed_changes),
            key=lambda item: (priority.get(str(item[1].get("kind", "")), 10), item[0]),
        )
    ]
    for change in ordered_changes:
        if not isinstance(change, dict):
            continue
        refs = change.get("evidence_refs") if isinstance(change.get("evidence_refs"), list) else []
        chosen: dict[str, Any] | None = None
        chosen_evidence: dict[str, Any] | None = None
        chosen_ref = ""
        target = str(change.get("target", "target"))
        for ref in refs:
            if not isinstance(ref, str) or not ref:
                continue
            label, obligation_id = _split_proof_audit_ref(ref)
            evidence = evidence_index.get(label or "")
            if not isinstance(evidence, dict):
                continue
            if obligation_id and isinstance(evidence.get("obligations"), list):
                for obligation in evidence["obligations"]:
                    if isinstance(obligation, dict) and obligation.get("id") == obligation_id:
                        chosen = obligation
                        chosen_evidence = evidence
                        chosen_ref = ref
                        break
            if chosen is None:
                chosen = evidence
                chosen_evidence = evidence
                chosen_ref = ref
            if chosen is not None:
                break
        if chosen is None:
            for item in evidence_index.values():
                if not isinstance(item, dict):
                    continue
                obligations = item.get("obligations") if isinstance(item.get("obligations"), list) else []
                for obligation in obligations:
                    if isinstance(obligation, dict) and obligation.get("id") == target:
                        chosen = obligation
                        chosen_evidence = item
                        chosen_ref = f"proof_audit_v2:{item.get('label', 'source')}:{target}"
                        break
                if chosen is not None:
                    break
        kind = str(change.get("kind", "change"))
        summary = str(change.get("summary", ""))
        rationale = str(change.get("rationale", ""))
        if kind == "split_derivation_step":
            action_text = "Split the row into smaller claims before proving it."
        elif kind == "add_or_verify_assumption":
            action_text = f"State or verify the missing assumption `{target}` here."
        elif kind == "add_review_boundary":
            action_text = "Pause here and treat the claim as needing human review."
        elif kind == "add_diagnostic_check":
            action_text = f"Run the bounded diagnostic for `{target}`."
        elif kind == "collect_more_evidence":
            action_text = "Formalize the claim or supply more evidence before asking for a repair."
        elif kind == "fix_parser_provenance":
            action_text = "Fix the parser provenance before using this line for certification."
        else:
            action_text = summary or rationale or "Review this line carefully."

        if chosen is None:
            location = str(target or "proposal")
            line_start = None
            section_path = []
            source_text = rationale or summary
            label_text = str(change.get("target") or "source")
        else:
            provenance = chosen.get("provenance") if isinstance(chosen.get("provenance"), dict) else {}
            section_path = provenance.get("section_path", []) if isinstance(provenance, dict) else []
            line_start = provenance.get("line_start") if isinstance(provenance, dict) else None
            location_bits = [str(provenance.get("file"))] if isinstance(provenance, dict) and provenance.get("file") else []
            location_bits.extend(str(item) for item in section_path if item)
            if line_start:
                location_bits.append(f"line {line_start}")
            location = " > ".join(location_bits) if location_bits else str(chosen.get("label") or "local context")
            source_text = str(chosen.get("source_text") or chosen.get("reason") or "")
            if not source_text and isinstance(chosen.get("provenance"), dict):
                source_text = str(chosen["provenance"].get("label") or "")
            source_text = _source_line_for_obligation(chosen_evidence, chosen) or source_text
            label_text = str(chosen.get("label") or change.get("target") or "source")

        key = (kind, location, target, action_text)
        if key in seen:
            continue
        seen.add(key)
        supplied_math_fix = change.get("math_fix") if isinstance(change.get("math_fix"), dict) else None
        math_fix = _reconstruct_split_align_equation(chosen_evidence, chosen) if kind == "split_derivation_step" and isinstance(chosen, dict) and isinstance(chosen_evidence, dict) else None
        if math_fix is None and isinstance(supplied_math_fix, dict):
            math_fix = supplied_math_fix
        proposed_fix = _math_fix_text(math_fix, summary or action_text)
        problem_text = _problem_text(kind, target, summary, rationale, source_text)
        source_text = _display_source_text(source_text, kind=kind, has_math_fix=isinstance(math_fix, dict))
        details.append(
            {
                "kind": kind,
                "target": target,
                "label": label_text,
                "location": location,
                "line_start": line_start,
                "section_path": section_path,
                "problem": problem_text,
                "summary": summary,
                "rationale": rationale,
                "source_text": source_text,
                "action": action_text,
                "proposed_fix": proposed_fix,
                "math_fix": math_fix,
                "evidence_only": _detail_is_evidence_only(kind),
                "evidence_ref": chosen_ref,
            }
        )
    return details


def _proposal_changes_from_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    changes = report.get("proposal_changes")
    if isinstance(changes, list):
        return _as_dict_list(changes)
    proposal = report.get("proposal")
    if isinstance(proposal, dict):
        evidence_items = proposal.get("evidence") if isinstance(proposal.get("evidence"), list) else []
        for item in evidence_items:
            if not isinstance(item, dict):
                continue
            low_level = item.get("low_level")
            if isinstance(low_level, dict) and isinstance(low_level.get("proposed_changes"), list):
                return _as_dict_list(low_level.get("proposed_changes"))
    evidence_items = report.get("evidence") if isinstance(report.get("evidence"), list) else []
    for item in evidence_items:
        if not isinstance(item, dict):
            continue
        low_level = item.get("low_level")
        if isinstance(low_level, dict) and isinstance(low_level.get("proposed_changes"), list):
            return _as_dict_list(low_level.get("proposed_changes"))
    return []


def _proposal_details_from_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    details = report.get("proposal_details")
    if isinstance(details, list):
        return _as_dict_list(details)
    audited = report.get("audited_evidence")
    audited_evidence = audited if isinstance(audited, list) else []
    return _build_plain_language_details(audited_evidence, _proposal_changes_from_report(report))


def _detail_to_markdown(detail: dict[str, Any], index: int | None = None) -> str:
    prefix = f"{index}. " if index is not None else "- "
    lines = [f"{prefix}`{_markdown_escape(detail.get('kind', 'change'))}` for `{_markdown_escape(detail.get('target', 'target'))}`"]
    lines.append(f"   Location: `{_markdown_escape(detail.get('location', 'local context'))}`")
    lines.append(f"   Problem: {_markdown_escape(detail.get('problem', detail.get('summary', 'Review this line carefully.')))}")
    lines.append(f"   Why: {_markdown_escape(detail.get('rationale', ''))}")
    lines.append(f"   Proposed fix: {_markdown_escape(detail.get('proposed_fix', detail.get('summary', '')))}")
    math_fix = detail.get("math_fix")
    if isinstance(math_fix, dict):
        if math_fix.get("replacement_latex"):
            lines.append("   Replacement LaTeX:")
            lines.append("   ```latex")
            for raw_line in str(math_fix.get("replacement_latex", "")).splitlines():
                lines.append(f"   {raw_line}")
            lines.append("   ```")
        if math_fix.get("derivation_obligation"):
            lines.append(f"   Derivation obligation: {_markdown_escape(math_fix.get('derivation_obligation'))}")
        if math_fix.get("certification_boundary"):
            lines.append(f"   Boundary: {_markdown_escape(math_fix.get('certification_boundary'))}")
    if detail.get("proof_target"):
        lines.append(f"   Proof target: `{_markdown_escape(detail.get('proof_target'))}`")
    if detail.get("derivation_plan"):
        lines.append(f"   Derivation plan: {_markdown_escape(detail.get('derivation_plan'))}")
    validation = detail.get("validation")
    if isinstance(validation, dict):
        lines.append(f"   Validation: `{_markdown_escape(validation.get('status', 'unknown'))}` - {_markdown_escape(validation.get('reason', ''))}")
        attempts = validation.get("backend_attempts") if isinstance(validation.get("backend_attempts"), list) else []
        if attempts:
            attempt_text = "; ".join(
                f"{attempt.get('backend', 'backend')}={attempt.get('status', 'unknown')} ({attempt.get('severity', 'diagnostic')})"
                for attempt in attempts
                if isinstance(attempt, dict)
            )
            lines.append(f"   Backend attempts: {_markdown_escape(attempt_text)}")
    if detail.get("source_text"):
        lines.append(f"   Source: {_markdown_escape(detail.get('source_text'))}")
    refs = detail.get("evidence_refs")
    if isinstance(refs, list) and refs:
        lines.append(f"   Evidence refs: {', '.join(_markdown_escape(ref) for ref in refs if ref)}")
    elif detail.get("evidence_ref"):
        lines.append(f"   Evidence refs: {_markdown_escape(detail.get('evidence_ref'))}")
    return "\n".join(lines)


def render_audit_fix_markdown(report: dict[str, Any]) -> str:
    """Render the structured audit/fix report as deterministic Markdown."""
    lines: list[str] = [
        "# MathDevMCP Audit And Fix Proposal",
        "",
        f"Question: {report.get('question', '')}",
        f"Status: {report.get('status', '')}",
        "",
        "## Certification Boundary",
        "",
        str(report.get("certification_boundary", AUDIT_FIX_REPORT_NON_CLAIM_TEXT)),
        "",
    ]
    coverage = report.get("coverage") if isinstance(report.get("coverage"), dict) else {}
    if coverage:
        lines.extend(
            [
                "## Audit Coverage",
                "",
                f"Mode: `{coverage.get('mode', 'unknown')}`",
                f"Audited labels: {coverage.get('audited_label_count', 0)} / {coverage.get('discovered_label_count', 0)}",
                f"Skipped labels: {coverage.get('skipped_label_count', 0)}",
                f"Complete for selected scope: {coverage.get('audit_complete', False)}",
            ]
        )
        if coverage.get("target_file"):
            lines.append(f"Target file: `{coverage.get('target_file')}`")
        if coverage.get("limit") is not None:
            lines.append(f"Label limit: {coverage.get('limit')}")
        audited_labels = coverage.get("audited_labels") if isinstance(coverage.get("audited_labels"), list) else []
        if audited_labels:
            label_text = ", ".join(
                f"`{item.get('label')}`" if isinstance(item, dict) else f"`{item}`" for item in audited_labels[:20]
            )
            if len(audited_labels) > 20:
                label_text += f", ... ({len(audited_labels) - 20} more)"
            lines.append(f"Audited label list: {label_text}")
        skipped = coverage.get("skipped_labels_preview") if isinstance(coverage.get("skipped_labels_preview"), list) else []
        if skipped:
            skipped_text = ", ".join(
                f"`{item.get('label')}`" if isinstance(item, dict) else f"`{item}`" for item in skipped[:10]
            )
            lines.append(f"Skipped preview: {skipped_text}")
        lines.append("")
    lines.extend(
        [
        "## Tool Uses",
        "",
        "| Tool | Purpose | Status | Output contract | Arguments |",
        "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in report.get("tool_uses", []):
        if not isinstance(item, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_markdown_escape(item.get('tool', ''))}`",
                    _markdown_escape(item.get("purpose", "")),
                    _markdown_escape(item.get("status", "")),
                    _markdown_escape(item.get("output_contract", "")),
                    f"`{_markdown_escape(item.get('arguments', {}))}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Audited Evidence", ""])
    evidence = report.get("audited_evidence", [])
    if evidence:
        for item in evidence:
            if isinstance(item, dict):
                label = item.get("label", item.get("contract", "evidence"))
                reason = item.get("reason", "")
                lines.append(f"- `{label}`: {item.get('status', 'unknown')} - {reason}")
    else:
        lines.append("- No audit evidence was supplied or generated.")

    proposal_changes = _proposal_changes_from_report(report)
    plain_language_details = _proposal_details_from_report(report)
    concrete_details = [item for item in plain_language_details if _detail_has_concrete_fix(item)]
    evidence_gap_details = [item for item in plain_language_details if isinstance(item, dict) and item.get("evidence_only")]
    validation = report.get("validation") if isinstance(report.get("validation"), dict) else {}
    if validation:
        lines.extend(["", "## Proposed Fix Validation", ""])
        lines.append(f"Enabled: {validation.get('enabled', False)}")
        lines.append(f"Policy: `{validation.get('policy', '')}`")
        lines.append(f"Backend order: `{validation.get('backend_order', [])}`")
        lines.append(f"Validated details: {validation.get('validated_detail_count', 0)}")
        status_counts = validation.get("status_counts") if isinstance(validation.get("status_counts"), dict) else {}
        if status_counts:
            status_text = ", ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
            lines.append(f"Status counts: {status_text}")
    lines.extend(["", "## Proposed Changes", ""])
    if concrete_details:
        for index, detail in enumerate(concrete_details, start=1):
            lines.append(f"{index}. `{detail.get('kind', 'change')}` for `{detail.get('target', 'target')}`")
            lines.append(f"   Summary: {detail.get('summary') or detail.get('proposed_fix', '')}")
            lines.append(f"   Rationale: {detail.get('rationale', '')}")
            if detail.get("evidence_ref"):
                lines.append(f"   Evidence refs: {detail.get('evidence_ref')}")
    else:
        lines.append("- No concrete proposed change could be derived safely.")
    if concrete_details:
        lines.extend(["", "### Proposed Fixes", ""])
        for index, detail in enumerate(concrete_details, start=1):
            lines.append(_detail_to_markdown(detail, index=index))

    if evidence_gap_details:
        lines.extend(["", "## Evidence Gaps", ""])
        for index, detail in enumerate(evidence_gap_details, start=1):
            lines.append(_detail_to_markdown(detail, index=index))

    actions = report.get("next_actions", [])
    lines.extend(["", "## Next Actions", ""])
    if actions:
        for item in actions:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('code', 'action')}`: {item.get('description', '')}")
    else:
        lines.append("- No next action was recorded.")

    lines.extend(["", "## Non-Claims", ""])
    for item in report.get("non_claims", []):
        if isinstance(item, dict):
            lines.append(f"- `{item.get('code', 'non_claim')}`: {item.get('text', '')}")
    lines.append("")
    return "\n".join(lines)


def build_audit_fix_report(
    question: str,
    *,
    root: str | None = None,
    labels: list[str] | None = None,
    whole_document: bool = False,
    target_file: str | None = None,
    source_digest: str | None = None,
    label_limit: int | None = None,
    label_kinds: list[str] | tuple[str, ...] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    paragraph_context: bool = True,
    context_before: int = 4,
    context_after: int = 1,
    summary_only: bool = True,
    backend: str = "sympy",
    task_context: str = "general_math_audit",
    validate_proposed_fixes: bool = False,
    certifier_policy: str = VALIDATION_POLICY_REQUIRE_ATTEMPT,
    backend_order: list[str] | tuple[str, ...] | None = None,
    workers: int = 1,
    output_path: str | Path | None = None,
    precomputed_label_audits: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Collect audit evidence, propose repairs, and optionally write Markdown."""
    labels = labels or []
    if (labels or whole_document) and not root:
        raise ValueError("root is required when labels or whole_document are supplied")
    if evidence is not None and not all(isinstance(item, dict) for item in evidence):
        raise ValueError("evidence must be a list of objects")
    if whole_document:
        discovered_labels, coverage = _discover_audit_labels(
            str(root),
            target_file=target_file,
            source_digest=source_digest,
            label_kinds=label_kinds,
            label_limit=label_limit,
        )
        if labels:
            explicit = list(dict.fromkeys(labels))
            discovered_set = set(discovered_labels)
            labels = [*discovered_labels, *[label for label in explicit if label not in discovered_set]]
            coverage = {
                **coverage,
                "mode": "whole_document_plus_explicit_labels",
                "explicit_labels": explicit,
                "audited_label_count": len(labels),
                "audited_labels": [*coverage.get("audited_labels", []), *[{"label": label, "source": "explicit"} for label in explicit if label not in discovered_set]],
            }
        else:
            labels = discovered_labels
    else:
        coverage = _explicit_coverage(
            root,
            labels,
            target_file=target_file,
            source_digest=source_digest,
        )

    tool_uses: list[ToolUseRecord] = []
    audited_evidence: list[dict[str, Any]] = list(evidence or [])
    if precomputed_label_audits is not None:
        if [item.get("label") for item in precomputed_label_audits] != labels:
            raise ValueError("precomputed label audits must exactly match requested label order")
        if any(item.get("metadata", {}).get("contract") != "proof_audit_v2_result" for item in precomputed_label_audits):
            raise ValueError("precomputed label audit contract mismatch")
        audited_evidence.extend(precomputed_label_audits)
        tool_uses.extend(
            ToolUseRecord(
                tool="audit_derivation_v2_label",
                arguments={"label": label, "reused_exact_evidence": True},
                purpose=f"Reuse exact derivation audit evidence for `{label}`.",
                status=str(audit.get("status", "unknown")),
                output_contract=_metadata_contract(audit),
            )
            for label, audit in zip(labels, precomputed_label_audits, strict=True)
        )
    elif labels:
        label_audits, label_tool_uses = _ordered_label_audits(
            str(root),
            labels,
            paragraph_context=paragraph_context,
            context_before=context_before,
            context_after=context_after,
            summary_only=summary_only,
            backend=backend,
            task_context=task_context,
            workers=workers,
            file=target_file,
            source_digest=source_digest,
        )
        audited_evidence.extend(label_audits)
        tool_uses.extend(ToolUseRecord(**item) for item in label_tool_uses)

    proposal_source = _source_context(source, root, labels)
    if target_file is not None:
        proposal_source.setdefault("file", target_file)
    if source_digest is not None:
        proposal_source.setdefault("source_digest", source_digest)
    proposal = propose_fix(question, evidence=audited_evidence, source=proposal_source)
    tool_uses.append(
        ToolUseRecord(
            tool="propose_fix",
            arguments={
                "question": question,
                "evidence_count": len(audited_evidence),
                "source": proposal_source,
            },
            purpose="Translate audit evidence into conservative repair proposals.",
            status=str(proposal.get("status", "unknown")),
            output_contract=_metadata_contract(proposal),
        )
    )
    proposed_changes = _proposal_changes_from_report(proposal)
    proposal_details = _build_plain_language_details(audited_evidence, proposed_changes)
    proposal_details.extend(_build_non_actionable_gap_details(audited_evidence, proposal_details))
    proposal_details.extend(_build_evidence_gap_details(audited_evidence, proposal_details))
    validation_summary: dict[str, Any] = {
        "enabled": False,
        "policy": certifier_policy,
        "backend_order": list(_normalize_backend_order(backend_order)),
        "validated_detail_count": 0,
        "status_counts": {},
    }
    if validate_proposed_fixes:
        normalized_backend_order = _normalize_backend_order(backend_order)
        validation_summary = _validate_proposal_details(
            proposal_details,
            certifier_policy=certifier_policy,
            backend_order=normalized_backend_order,
        )
        tool_uses.append(
            ToolUseRecord(
                tool="validate_proposed_fixes",
                arguments={
                    "policy": certifier_policy,
                    "backend_order": list(normalized_backend_order),
                    "detail_count": validation_summary["validated_detail_count"],
                },
                purpose="Attach deterministic backend-attempt accountability to concrete proposed fixes.",
                status="completed",
                output_contract="proposal_fix_validation_summary",
            )
        )
    non_claims = default_non_claims(extra_codes={"diagnostic_evidence_not_proof"})
    for code, text in (
        (REPAIR_NON_CLAIM_CODE, REPAIR_NON_CLAIM_TEXT),
        (AUDIT_FIX_REPORT_NON_CLAIM_CODE, AUDIT_FIX_REPORT_NON_CLAIM_TEXT),
    ):
        if not any(item.get("code") == code for item in non_claims):
            non_claims.append({"code": code, "text": text})
    next_actions = [
        action("human_review", "Review proposed changes before applying edits."),
        action("rerun_relevant_audit", "After any manual repair, rerun the audit evidence that produced the proposal."),
    ]
    concrete_details = [item for item in proposal_details if _detail_has_concrete_fix(item)]
    status = _report_status(concrete_details, audited_evidence)
    evidence_summaries = [_summarize_audit(item) for item in audited_evidence]
    coverage["label_ledger"] = [
        {
            "label": item.get("label"),
            "status": item.get("status"),
            "coverage_status": "canonical_target" if isinstance(item.get("canonical_target"), dict) else "typed_abstention",
            "canonical_target": item.get("canonical_target"),
        }
        for item in evidence_summaries
    ]
    low_level = AuditFixReport(
        status=status,
        question=question,
        source=proposal_source,
        coverage=coverage,
        tool_uses=[asdict(item) for item in tool_uses],
        audited_evidence=evidence_summaries,
        proposal_changes=proposed_changes,
        proposal_details=proposal_details,
        validation=validation_summary,
        proposal=proposal,
        markdown="",
        output_path=str(output_path) if output_path is not None else None,
        non_claims=non_claims,
        next_actions=next_actions,
        agent_handoff={
            "scoped_question": question,
            "status": status,
            "report_path": str(output_path) if output_path is not None else None,
            "coverage": coverage,
            "tool_uses": [asdict(item) for item in tool_uses],
            "proposed_changes": proposed_changes,
            "proposal_details": proposal_details,
            "validation": validation_summary,
            "next_actions": next_actions,
            "certification_boundary": AUDIT_FIX_REPORT_NON_CLAIM_TEXT,
        },
        certification_boundary=AUDIT_FIX_REPORT_NON_CLAIM_TEXT,
        metadata=contract_metadata(AUDIT_FIX_REPORT_CONTRACT),
    )
    report = attach_contract(asdict(low_level), AUDIT_FIX_REPORT_CONTRACT)
    report["markdown"] = render_audit_fix_markdown(report)
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report["markdown"], encoding="utf-8")
    return report


def audit_and_propose_fix(
    question: str,
    *,
    root: str | None = None,
    labels: list[str] | None = None,
    whole_document: bool = False,
    target_file: str | None = None,
    source_digest: str | None = None,
    label_limit: int | None = None,
    label_kinds: list[str] | tuple[str, ...] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    paragraph_context: bool = True,
    context_before: int = 4,
    context_after: int = 1,
    summary_only: bool = True,
    backend: str = "sympy",
    task_context: str = "general_math_audit",
    validate_proposed_fixes: bool = False,
    certifier_policy: str = VALIDATION_POLICY_REQUIRE_ATTEMPT,
    backend_order: list[str] | tuple[str, ...] | None = None,
    workers: int = 1,
    output_path: str | Path | None = None,
    precomputed_label_audits: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a high-level envelope for an audit-plus-fix Markdown report."""
    report = build_audit_fix_report(
        question,
        root=root,
        labels=labels,
        whole_document=whole_document,
        target_file=target_file,
        source_digest=source_digest,
        label_limit=label_limit,
        label_kinds=label_kinds,
        evidence=evidence,
        source=source,
        paragraph_context=paragraph_context,
        context_before=context_before,
        context_after=context_after,
        summary_only=summary_only,
        backend=backend,
        task_context=task_context,
        validate_proposed_fixes=validate_proposed_fixes,
        certifier_policy=certifier_policy,
        backend_order=backend_order,
        workers=workers,
        output_path=output_path,
        precomputed_label_audits=precomputed_label_audits,
    )
    high_level = high_level_result(
        status="diagnostic_only",
        workflow="audit_and_propose_fix",
        question=question,
        claim_class="fix_report",
        answer=f"Audit-and-fix report prepared with status `{report['status']}`.",
        evidence=[
            evidence_entry(
                id="audit_and_propose_fix:report",
                evidence_class="fix_report",
                source="audit_fix_report_builder",
                summary=f"Audit-and-fix report prepared with {len(report['tool_uses'])} tool uses.",
                extra={"low_level": report},
            )
        ],
        certification_source="none",
        veto_reasons=[] if report["status"] != "needs_evidence" else [veto_reason("audit_fix_report_requires_evidence", "No evidence was supplied or generated for a fix proposal.")],
        actions=report["next_actions"],
        non_claims=report["non_claims"],
    )
    high_level["agent_handoff"] = report["agent_handoff"]
    refresh_evidence_ledger(high_level)
    errors = validate_high_level_result(high_level)
    if errors:
        raise ValueError(f"invalid audit_and_propose_fix result: {errors}")
    return high_level


def write_audit_fix_report_markdown(
    question: str,
    output_path: str | Path,
    *,
    root: str | None = None,
    labels: list[str] | None = None,
    whole_document: bool = False,
    target_file: str | None = None,
    source_digest: str | None = None,
    label_limit: int | None = None,
    label_kinds: list[str] | tuple[str, ...] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    source: dict[str, Any] | None = None,
    paragraph_context: bool = True,
    context_before: int = 4,
    context_after: int = 1,
    summary_only: bool = True,
    backend: str = "sympy",
    task_context: str = "general_math_audit",
    validate_proposed_fixes: bool = False,
    certifier_policy: str = VALIDATION_POLICY_REQUIRE_ATTEMPT,
    backend_order: list[str] | tuple[str, ...] | None = None,
    workers: int = 1,
) -> dict[str, Any]:
    """Write the Markdown report and return the structured low-level artifact."""
    report = build_audit_fix_report(
        question,
        root=root,
        labels=labels,
        whole_document=whole_document,
        target_file=target_file,
        source_digest=source_digest,
        label_limit=label_limit,
        label_kinds=label_kinds,
        evidence=evidence,
        source=source,
        paragraph_context=paragraph_context,
        context_before=context_before,
        context_after=context_after,
        summary_only=summary_only,
        backend=backend,
        task_context=task_context,
        validate_proposed_fixes=validate_proposed_fixes,
        certifier_policy=certifier_policy,
        backend_order=backend_order,
        workers=workers,
        output_path=output_path,
    )
    return success_result({"output": str(output_path), "report": report}, contract="audit_fix_report_markdown")
