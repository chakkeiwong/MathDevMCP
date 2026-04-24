from __future__ import annotations

from pathlib import Path

from .consistency import compare_label_to_code
from .contracts import attach_contract, success_result
from .derivation import derive_step_for_label
from .latex_index import build_index, extract_paragraph_context_for_label, search_index


def build_implementation_brief(
    doc_root: str,
    query: str,
    code_path: str,
    label: str | None = None,
    required_terms: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    limit: int = 3,
) -> dict:
    root = Path(doc_root)
    index = build_index(root)
    search_results = search_index(index, query, limit=limit)
    selected_label = label
    if selected_label is None:
        selected_label = next((result.get("label") for result in search_results if result.get("label")), None)

    brief: dict = {
        "query": query,
        "doc_root": str(root.resolve()),
        "code_path": code_path,
        "search_results": search_results,
        "selected_label": selected_label,
        "status": "inconclusive",
        "checks": {},
    }
    if selected_label is None:
        brief["reason"] = "No labeled document block was found for the query."
        return success_result(attach_contract(brief, "implementation_brief"))

    brief["doc_context"] = extract_paragraph_context_for_label(index, selected_label, before=1, after=1)
    consistency = compare_label_to_code(
        str(root),
        selected_label,
        code_path,
        before=1,
        after=1,
        paragraph_context=True,
        required_terms=required_terms,
    )
    brief["checks"]["consistency"] = consistency

    derivation = None
    if lhs is not None and rhs is not None:
        derivation = derive_step_for_label(
            str(root),
            selected_label,
            lhs,
            rhs,
            before=1,
            after=1,
            paragraph_context=True,
        )
        brief["checks"]["derivation"] = derivation

    if consistency["status"] == "mismatch" or (derivation and derivation["status"] == "mismatch"):
        brief["status"] = "mismatch"
        brief["reason"] = "At least one document-grounded implementation check failed."
    elif derivation and derivation["status"] == "unverified":
        brief["status"] = "unverified"
        brief["reason"] = "Code-document terms matched, but the derivation step still needs explicit support."
    elif consistency["status"] == "consistent":
        brief["status"] = "consistent"
        brief["reason"] = "The selected document context is consistent with the checked code terms."
    else:
        brief["reason"] = "The implementation brief could not reach a definitive status."
    return success_result(attach_contract(brief, "implementation_brief", doc_context=brief.get("doc_context")))
