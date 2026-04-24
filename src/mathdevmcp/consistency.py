from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re

from .contracts import attach_contract
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label
from .math_normalization import normalize_math_tokens


@dataclass(frozen=True)
class ConsistencyFinding:
    status: str
    reason: str
    doc_terms: list[str]
    code_terms: list[str]
    missing_in_code: list[str]
    findings: list[dict]


INCIDENTAL_DOC_TERMS = {
    "begin",
    "end",
    "label",
    "prop",
    "proposition",
    "theorem",
    "lemma",
    "corollary",
    "definition",
    "remark",
    "example",
    "proof",
    "transport",
    "identity",
    "transformed",
    "log",
    "density",
}


def extract_terms(text: str) -> list[str]:
    normalized = normalize_math_tokens(text)
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", normalized)
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "into", "code", "text",
        "equation", "algorithm", "document", "implementation", "where", "when", "then",
    }
    terms: list[str] = []
    for token in tokens:
        lower = token.lower()
        if lower not in stop and lower not in terms:
            terms.append(lower)
    return terms



def _normalized_token_set(text: str) -> set[str]:
    return set(extract_terms(text))



def _build_findings(doc_terms: list[str], code_terms: list[str], missing: list[str]) -> list[dict]:
    code_term_set = set(code_terms)
    findings: list[dict] = []
    for term in doc_terms:
        findings.append(
            {
                "kind": "missing_term" if term in missing else "matched_term",
                "term": term,
                "present_in_code": term in code_term_set,
                "severity": "required",
            }
        )
    return findings



def _contextual_doc_terms(doc_text: str) -> list[str]:
    terms = extract_terms(doc_text)
    filtered = [term for term in terms if term not in INCIDENTAL_DOC_TERMS]
    return filtered or terms



def compare_doc_to_code(doc_text: str, code_text: str, required_terms: list[str] | None = None) -> dict:
    doc_terms = required_terms or _contextual_doc_terms(doc_text)
    code_terms = extract_terms(code_text)
    code_term_set = set(code_terms)
    missing = [term for term in doc_terms if term.lower() not in code_term_set]
    findings = _build_findings(doc_terms, code_terms, missing)
    doc_token_set = _normalized_token_set(doc_text)
    code_token_set = _normalized_token_set(code_text)
    extra_in_code = sorted(code_token_set - doc_token_set)
    if extra_in_code:
        findings.append({"kind": "extra_code_terms", "terms": extra_in_code, "severity": "audit_only"})
    if not doc_terms:
        status = "inconclusive"
        reason = "No document terms were available for comparison."
    elif missing:
        status = "mismatch"
        reason = "Some required document terms were not found in the code text."
    else:
        status = "consistent"
        reason = "All required document terms were found in the code text."
    result = asdict(
        ConsistencyFinding(
            status=status,
            reason=reason,
            doc_terms=doc_terms,
            code_terms=code_terms,
            missing_in_code=missing,
            findings=findings,
        )
    )
    result["extra_in_code"] = extra_in_code
    return attach_contract(result, "consistency_result")



def compare_files(doc_path: str, code_path: str, required_terms: list[str] | None = None) -> dict:
    doc_text = Path(doc_path).read_text(encoding="utf-8")
    code_text = Path(code_path).read_text(encoding="utf-8")
    result = compare_doc_to_code(doc_text, code_text, required_terms=required_terms)
    result["doc_path"] = doc_path
    result["code_path"] = code_path
    return result



def compare_label_to_code(doc_root: str, label: str, code_path: str, before: int = 0, after: int = 0, paragraph_context: bool = False, required_terms: list[str] | None = None) -> dict:
    index = build_index(Path(doc_root))
    doc_context = (
        extract_paragraph_context_for_label(index, label, before=before, after=after)
        if paragraph_context
        else extract_context_for_label(index, label, before=before, after=after)
    )
    if paragraph_context:
        doc_text = "\n\n".join(paragraph["text"] for paragraph in doc_context.get("paragraphs", []))
    else:
        doc_text = "\n".join(line["text"] for line in doc_context.get("excerpt", []))
    result = compare_doc_to_code(doc_text, Path(code_path).read_text(encoding="utf-8"), required_terms=required_terms)
    result["label"] = label
    result["doc_root"] = str(Path(doc_root).resolve())
    result["code_path"] = code_path
    result["doc_context"] = doc_context
    return attach_contract(result, "label_consistency_result", doc_context=doc_context)
