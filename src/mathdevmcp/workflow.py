from __future__ import annotations

from pathlib import Path

from .consistency import compare_label_to_code
from .contracts import attach_contract, success_result
from .derivation import derive_step_for_label
from .index_cache import load_or_build_index
from .latex_index import build_index, extract_paragraph_context_for_label, search_index


def _partial_certification_summary(brief: dict) -> dict:
    consistency = brief.get("checks", {}).get("consistency")
    derivation = brief.get("checks", {}).get("derivation")
    certified: list[str] = []
    not_certified: list[str] = []
    diagnostic_only: list[str] = []
    tool_failures: list[str] = []

    if brief.get("search_results"):
        diagnostic_only.append("label search")
    if brief.get("doc_context"):
        context_status = brief["doc_context"].get("status")
        diagnostic_only.append("fallback label context" if context_status == "fallback_text_context" else "label context")
    if consistency is not None:
        if consistency.get("status") == "mismatch":
            not_certified.append("full LaTeX/code contract")
        elif consistency.get("status") == "consistent":
            diagnostic_only.append("code/document term comparison")
        else:
            not_certified.append("code/document term comparison")
    if derivation is not None:
        if derivation.get("status") == "equivalent":
            certified.append("scoped derivation equality")
        elif derivation.get("status") == "mismatch":
            not_certified.append("scoped derivation equality")
        else:
            diagnostic_only.append("scoped derivation equality")
    for name, check in brief.get("checks", {}).items():
        if isinstance(check, dict) and check.get("ok") is False:
            tool_failures.append(name)

    if certified and (not_certified or diagnostic_only or tool_failures):
        overall_status = "partial_certification"
    elif not_certified or tool_failures:
        overall_status = "not_certified"
    elif certified:
        overall_status = "certified_subclaims"
    else:
        overall_status = "diagnostic_only"
    recommended_next_tool = "audit_temporal_contract" if not_certified else "audit_derivation_v2_label"
    return {
        "overall_status": overall_status,
        "certified": certified,
        "not_certified": not_certified,
        "diagnostic_only": diagnostic_only,
        "tool_failures": tool_failures,
        "recommended_next_tool": recommended_next_tool,
    }


def build_implementation_brief(
    doc_root: str,
    query: str,
    code_path: str,
    label: str | None = None,
    required_terms: list[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    limit: int = 3,
    cache_path: str | Path | None = None,
) -> dict:
    root = Path(doc_root)
    index = load_or_build_index(root, Path(cache_path)) if cache_path else build_index(root)
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
        "cache": index.get("cache", {"path": None, "hit": False}),
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
        index=index,
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
            index=index,
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
    brief["partial_certification_summary"] = _partial_certification_summary(brief)
    return success_result(attach_contract(brief, "implementation_brief", doc_context=brief.get("doc_context")))
