from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from .contracts import attach_contract
from .index_cache import load_or_build_index
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label
from .proof_obligations import check_proof_obligation


@dataclass(frozen=True)
class ProofAuditObligation:
    id: str
    lhs: str
    rhs: str
    source_text: str
    classification: str
    status: str
    reason: str
    evidence: list[dict]
    provenance: dict


@dataclass(frozen=True)
class ProofAuditReport:
    label: str
    doc_root: str
    status: str
    reason: str
    obligations: list[dict]
    counts: dict[str, int]
    doc_context: dict


_SAFE_BACKEND_EXPRESSION = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")
_DOMAIN_MARKERS = (
    "\\partial",
    "\\operatorname",
    "\\trace",
    "\\tr",
    "^{-1}",
    "'",
    "ell_t",
    "\\ell",
    "S_t",
    "v_t",
)


def _strip_latex_noise(text: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\begin\{[^}]+\*?\}", "", text)
    text = re.sub(r"\\end\{[^}]+\*?\}", "", text)
    text = text.replace("&", "")
    text = text.replace("\\left", "").replace("\\right", "")
    text = text.replace("\\,", " ")
    return text.strip()


def _line_provenance(doc_context: dict, source_line: int | None = None) -> dict:
    line_start = source_line or doc_context.get("line_start")
    return {
        "file": doc_context.get("file"),
        "line_start": line_start,
        "line_end": source_line or doc_context.get("line_end"),
        "label": doc_context.get("label"),
        "block_id": doc_context.get("block_id"),
        "section_path": doc_context.get("section_path", []),
    }


def _diagnostic_evidence(kind: str, reason: str, *, severity: str = "diagnostic") -> list[dict]:
    return [{"kind": kind, "reason": reason, "severity": severity}]


def _is_domain_notation(text: str) -> bool:
    return any(marker in text for marker in _DOMAIN_MARKERS)


def _is_backend_safe(lhs: str, rhs: str) -> bool:
    return bool(_SAFE_BACKEND_EXPRESSION.fullmatch(lhs) and _SAFE_BACKEND_EXPRESSION.fullmatch(rhs))


def _split_single_equality(row: str) -> tuple[str, str] | None:
    if row.count("=") != 1:
        return None
    lhs, rhs = [part.strip() for part in row.split("=", 1)]
    if not rhs:
        return None
    return lhs, rhs


def _source_lines(doc_context: dict, paragraph_context: bool) -> list[dict]:
    if paragraph_context:
        return [
            {"line": paragraph["line_start"], "text": paragraph["text"]}
            for paragraph in doc_context.get("paragraphs", [])
        ]
    return list(doc_context.get("excerpt", []))


def _body_lines_for_label(doc_context: dict, paragraph_context: bool) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for item in _source_lines(doc_context, paragraph_context):
        start_line = item["line"]
        for offset, line in enumerate(item["text"].splitlines()):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("\\begin") or stripped.startswith("\\end"):
                continue
            stripped = re.sub(r"\\label\{[^}]+\}", "", stripped).strip()
            if stripped:
                lines.append((start_line + offset, stripped))
    return lines


def _split_align_rows(line: str) -> list[str]:
    return [part.strip() for part in re.split(r"\\\\", line) if part.strip()]


def _extract_obligation_candidates(doc_context: dict, paragraph_context: bool) -> list[dict]:
    candidates: list[dict] = []
    previous_rhs: str | None = None
    previous_line: int | None = None
    for source_line, raw_line in _body_lines_for_label(doc_context, paragraph_context):
        for row in _split_align_rows(raw_line):
            cleaned = _strip_latex_noise(row)
            if not cleaned:
                continue
            if _is_domain_notation(cleaned):
                split = _split_single_equality(cleaned)
                lhs = split[0] if split else ""
                rhs = split[1] if split else ""
                candidates.append({"lhs": lhs, "rhs": rhs, "source_text": cleaned, "line": source_line, "classification": "human_review"})
                previous_rhs = None
                previous_line = None
                continue
            split = _split_single_equality(cleaned)
            if split is None:
                if "=" in cleaned:
                    candidates.append({"lhs": "", "rhs": "", "source_text": cleaned, "line": source_line, "classification": "not_extracted"})
                previous_rhs = None
                previous_line = None
                continue
            lhs, rhs = split
            if lhs:
                candidates.append({"lhs": lhs, "rhs": rhs, "source_text": cleaned, "line": source_line, "classification": "sympy"})
            elif previous_rhs is not None:
                candidates.append({"lhs": previous_rhs, "rhs": rhs, "source_text": cleaned, "line": source_line, "classification": "sympy"})
            previous_rhs = rhs
            previous_line = source_line
    return candidates


def _audit_candidate(candidate: dict, obligation_id: str, doc_context: dict, backend: str) -> dict:
    provenance = _line_provenance(doc_context, candidate.get("line"))
    classification = candidate["classification"]
    if classification == "not_extracted":
        obligation = ProofAuditObligation(
            id=obligation_id,
            lhs="",
            rhs="",
            source_text=candidate["source_text"],
            classification="not_extracted",
            status="inconclusive",
            reason="The derivation row was ambiguous and was not split into a proof obligation.",
            evidence=_diagnostic_evidence("not_extracted", "The row contains an ambiguous equality structure."),
            provenance=provenance,
        )
        return asdict(obligation)
    if classification == "human_review" or not _is_backend_safe(candidate["lhs"], candidate["rhs"]):
        obligation = ProofAuditObligation(
            id=obligation_id,
            lhs=candidate.get("lhs", ""),
            rhs=candidate.get("rhs", ""),
            source_text=candidate["source_text"],
            classification="human_review",
            status="inconclusive",
            reason="The obligation uses notation outside the bounded algebraic backend and needs formalization or human review.",
            evidence=_diagnostic_evidence("backend_not_encodable", "The obligation is not safe to encode for the bounded backend."),
            provenance=provenance,
        )
        return asdict(obligation)

    checked = check_proof_obligation(candidate["lhs"], candidate["rhs"], backend=backend)
    status = "verified" if checked["status"] == "equivalent" else checked["status"]
    if status == "equivalent":
        status = "verified"
    obligation = ProofAuditObligation(
        id=obligation_id,
        lhs=candidate["lhs"],
        rhs=candidate["rhs"],
        source_text=candidate["source_text"],
        classification="normalization" if checked["evidence"][0]["kind"] == "normalized_match" else "sympy",
        status=status,
        reason=checked["reason"],
        evidence=checked["evidence"],
        provenance=provenance,
    )
    return asdict(obligation)


def _empty_obligation(doc_context: dict) -> dict:
    return asdict(
        ProofAuditObligation(
            id="obligation_1",
            lhs="",
            rhs="",
            source_text="",
            classification="not_extracted",
            status="inconclusive",
            reason="No equation-like proof obligation was extracted from the labeled context.",
            evidence=_diagnostic_evidence("not_extracted", "No equation-like proof obligation was extracted."),
            provenance=_line_provenance(doc_context),
        )
    )


def _counts(obligations: list[dict]) -> dict[str, int]:
    counts = {
        "total": len(obligations),
        "verified": 0,
        "mismatched": 0,
        "unverified": 0,
        "inconclusive": 0,
        "not_encodable": 0,
        "not_extracted": 0,
    }
    for obligation in obligations:
        status = obligation["status"]
        if status == "verified":
            counts["verified"] += 1
        elif status == "mismatch":
            counts["mismatched"] += 1
        elif status == "unverified":
            counts["unverified"] += 1
        else:
            counts["inconclusive"] += 1
        if obligation["classification"] == "not_extracted":
            counts["not_extracted"] += 1
        if obligation["classification"] == "human_review":
            counts["not_encodable"] += 1
    return counts


def _aggregate_status(counts: dict[str, int]) -> tuple[str, str]:
    if counts["mismatched"]:
        return "mismatch", "At least one extracted proof obligation was refuted by a backend."
    if counts["verified"] and counts["verified"] == counts["total"]:
        return "verified", "Every extracted proof obligation was certified by a bounded backend."
    if counts["unverified"] or counts["verified"]:
        return "unverified", "Some obligations were extracted, but at least one remains unsupported."
    return "inconclusive", "No proof obligation could be certified or refuted."


def audit_derivation_for_label(
    root: str,
    label: str,
    *,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "auto",
    cache_path: str | Path | None = None,
) -> dict:
    root_path = Path(root)
    index = load_or_build_index(root_path, Path(cache_path)) if cache_path else build_index(root_path)
    doc_context = (
        extract_paragraph_context_for_label(index, label, before=before, after=after)
        if paragraph_context
        else extract_context_for_label(index, label, before=before, after=after)
    )
    candidates = _extract_obligation_candidates(doc_context, paragraph_context)
    obligations = [
        _audit_candidate(candidate, f"obligation_{idx}", doc_context, backend)
        for idx, candidate in enumerate(candidates, start=1)
    ]
    if not obligations:
        obligations = [_empty_obligation(doc_context)]
    counts = _counts(obligations)
    status, reason = _aggregate_status(counts)
    report = ProofAuditReport(
        label=label,
        doc_root=str(root_path.resolve()),
        status=status,
        reason=reason,
        obligations=obligations,
        counts=counts,
        doc_context=doc_context,
    )
    return attach_contract(asdict(report), "proof_audit_result", doc_context=doc_context)
