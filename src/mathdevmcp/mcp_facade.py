from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .benchmarks import benchmark_gate_report, build_benchmark_report, run_derivation_benchmark, run_label_consistency_benchmark, run_seeded_mismatch_benchmark, run_workflow_benchmark, summarize_benchmark_results
from .code_search import search_files
from .consistency import compare_files, compare_label_to_code
from .contracts import error_result, success_result
from .derivation import derive_step_for_label
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief

ToolHandler = Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]]


def _required_string(args: dict[str, Any], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing required string argument: {name}")
    return value


def _optional_terms(args: dict[str, Any]) -> list[str] | None:
    terms = args.get("required_terms")
    if terms is None:
        return None
    if isinstance(terms, str):
        return [term.strip() for term in terms.split(",") if term.strip()]
    if isinstance(terms, list) and all(isinstance(term, str) for term in terms):
        return terms
    raise ValueError("required_terms must be a comma-separated string or list of strings")


def _tool_search_latex(args: dict[str, Any]) -> list[dict[str, Any]]:
    index = build_index(Path(_required_string(args, "root")))
    return search_index(index, _required_string(args, "query"), limit=int(args.get("limit", 10)))


def _tool_extract_latex_context(args: dict[str, Any]) -> dict[str, Any]:
    index = build_index(Path(_required_string(args, "root")))
    return extract_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 2)),
        after=int(args.get("after", 2)),
    )


def _tool_extract_latex_neighborhood(args: dict[str, Any]) -> dict[str, Any]:
    index = build_index(Path(_required_string(args, "root")))
    return extract_paragraph_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 1)),
        after=int(args.get("after", 1)),
    )


def _tool_search_code_docs(args: dict[str, Any]) -> list[dict[str, Any]]:
    return search_files(Path(_required_string(args, "root")), _required_string(args, "query"), limit=int(args.get("limit", 20)))


def _tool_compare_doc_code(args: dict[str, Any]) -> dict[str, Any]:
    return compare_files(_required_string(args, "doc"), _required_string(args, "code"), required_terms=_optional_terms(args))


def _tool_compare_label_code(args: dict[str, Any]) -> dict[str, Any]:
    return compare_label_to_code(
        _required_string(args, "root"),
        _required_string(args, "label"),
        _required_string(args, "code"),
        before=int(args.get("before", 0)),
        after=int(args.get("after", 0)),
        paragraph_context=bool(args.get("paragraph_context", False)),
        required_terms=_optional_terms(args),
    )


def _tool_derive_label_step(args: dict[str, Any]) -> dict[str, Any]:
    return derive_step_for_label(
        _required_string(args, "root"),
        _required_string(args, "label"),
        _required_string(args, "lhs"),
        _required_string(args, "rhs"),
        before=int(args.get("before", 0)),
        after=int(args.get("after", 0)),
        paragraph_context=bool(args.get("paragraph_context", False)),
    )


def _tool_implementation_brief(args: dict[str, Any]) -> dict[str, Any]:
    return build_implementation_brief(
        _required_string(args, "root"),
        _required_string(args, "query"),
        _required_string(args, "code"),
        label=args.get("label") or None,
        required_terms=_optional_terms(args),
        lhs=args.get("lhs") or None,
        rhs=args.get("rhs") or None,
        limit=int(args.get("limit", 3)),
    )


def _tool_run_benchmarks(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return build_benchmark_report(root)



def _tool_benchmark_gate(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return benchmark_gate_report(root)


def _tool_tool_matrix(args: dict[str, Any]) -> list[dict[str, Any]]:
    return tool_matrix()


TOOL_HANDLERS: dict[str, ToolHandler] = {
    "search_latex": _tool_search_latex,
    "extract_latex_context": _tool_extract_latex_context,
    "extract_latex_neighborhood": _tool_extract_latex_neighborhood,
    "search_code_docs": _tool_search_code_docs,
    "compare_doc_code": _tool_compare_doc_code,
    "compare_label_code": _tool_compare_label_code,
    "derive_label_step": _tool_derive_label_step,
    "implementation_brief": _tool_implementation_brief,
    "run_benchmarks": _tool_run_benchmarks,
    "benchmark_gate": _tool_benchmark_gate,
    "tool_matrix": _tool_tool_matrix,
}


def list_mcp_tools() -> list[dict[str, Any]]:
    return [
        {"name": name, "description": description}
        for name, description in [
            ("search_latex", "Search indexed LaTeX blocks with provenance."),
            ("extract_latex_context", "Extract line context around a LaTeX label."),
            ("extract_latex_neighborhood", "Extract paragraph neighborhood around a LaTeX label."),
            ("search_code_docs", "Search code and document files together."),
            ("compare_doc_code", "Compare document text against code text."),
            ("compare_label_code", "Compare a labeled document block against code."),
            ("derive_label_step", "Check a derivation step against labeled document context."),
            ("implementation_brief", "Build a document-grounded implementation brief."),
            ("run_benchmarks", "Run seeded consistency benchmarks."),
            ("benchmark_gate", "Return CI-friendly benchmark gate results."),
            ("tool_matrix", "Return the current MathDevMCP tool matrix."),
        ]
    ]


def _wrap_tool_result(result: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any] | list[dict[str, Any]]:
    if isinstance(result, dict) and "ok" not in result:
        return success_result(result)
    return result



def call_mcp_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any] | list[dict[str, Any]]:
    try:
        handler = TOOL_HANDLERS[name]
    except KeyError:
        return error_result("unknown_tool", f"Unknown MathDevMCP tool: {name}")
    try:
        return _wrap_tool_result(handler(arguments))
    except ValueError as exc:
        return error_result("invalid_arguments", str(exc))
