from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re

from .contracts import attach_contract
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label
from .math_normalization import normalize_math_text


@dataclass(frozen=True)
class DerivationStep:
    lhs: str
    rhs: str
    status: str
    reason: str
    evidence: list[dict]


EVIDENCE_SEVERITY = {
    "normalized_match": "certifying",
    "symbol_overlap": "supporting",
    "label_context": "supporting",
    "cited_label": "supporting",
    "symbol_mismatch": "blocking",
}


def _normalize_math(text: str) -> str:
    return normalize_math_text(text)



def _with_evidence_severity(evidence: list[dict]) -> list[dict]:
    enriched: list[dict] = []
    for item in evidence:
        enriched.append({**item, "severity": EVIDENCE_SEVERITY.get(item["kind"], "supporting")})
    return enriched



def _cited_labels_in_text(text: str) -> list[str]:
    return re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text)



def _context_supports_expression(context_text: str, expression: str) -> bool:
    return bool(expression) and _normalize_math(expression) in _normalize_math(context_text)



def _symbol_terms(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_]+", _normalize_math(text)))



def derive_step(lhs: str, rhs: str) -> dict:
    lhs_n = _normalize_math(lhs)
    rhs_n = _normalize_math(rhs)
    evidence: list[dict] = []
    if lhs_n == rhs_n:
        status = "equivalent"
        reason = "Left-hand side and right-hand side match after whitespace normalization."
        evidence.append({"kind": "normalized_match", "lhs": lhs, "rhs": rhs})
    else:
        lhs_terms = _symbol_terms(lhs_n)
        rhs_terms = _symbol_terms(rhs_n)
        if lhs_terms == rhs_terms:
            status = "unverified"
            reason = "Both sides mention the same symbolic terms, but no supporting derivation or cited equation was provided."
            evidence.append({"kind": "symbol_overlap", "symbols": sorted(lhs_terms)})
        else:
            status = "mismatch"
            reason = "The two sides use different symbolic terms, so the step needs derivation or correction."
            evidence.append({"kind": "symbol_mismatch", "lhs_symbols": sorted(lhs_terms), "rhs_symbols": sorted(rhs_terms)})
    return attach_contract(
        asdict(DerivationStep(lhs=lhs, rhs=rhs, status=status, reason=reason, evidence=_with_evidence_severity(evidence))),
        "derivation_result",
    )



def derive_step_from_files(doc_path: str, lhs: str, rhs: str) -> dict:
    result = derive_step(lhs, rhs)
    result["doc_path"] = doc_path
    return result



def derive_step_for_label(
    doc_root: str,
    label: str,
    lhs: str,
    rhs: str,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    index: dict | None = None,
) -> dict:
    index = index or build_index(Path(doc_root))
    doc_context = (
        extract_paragraph_context_for_label(index, label, before=before, after=after)
        if paragraph_context
        else extract_context_for_label(index, label, before=before, after=after)
    )
    result = derive_step(lhs, rhs)
    if paragraph_context:
        context_text = "\n\n".join(paragraph["text"] for paragraph in doc_context.get("paragraphs", []))
    else:
        context_text = "\n".join(line["text"] for line in doc_context.get("excerpt", []))
    if result["status"] == "unverified" and (_context_supports_expression(context_text, lhs) or _context_supports_expression(context_text, rhs)):
        result["reason"] = "The step remains unverified, but the cited label provides nearby supporting notation for review."
        result["evidence"].append({"kind": "label_context", "label": label, "section_path": doc_context.get("section_path", []), "severity": EVIDENCE_SEVERITY["label_context"]})
    cited_labels = _cited_labels_in_text(context_text)
    if cited_labels:
        result["evidence"].append({"kind": "cited_label", "labels": cited_labels, "severity": EVIDENCE_SEVERITY["cited_label"]})
    result["label"] = label
    result["doc_root"] = str(Path(doc_root).resolve())
    result["doc_context"] = doc_context
    result["supported_by_context"] = _context_supports_expression(context_text, lhs) or _context_supports_expression(context_text, rhs)
    result["step_chain"] = [{"label": label, "supported_by_context": result["supported_by_context"], "cited_labels": cited_labels}]
    return attach_contract(result, "label_derivation_result", doc_context=doc_context)
