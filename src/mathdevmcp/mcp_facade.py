from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .benchmarks import benchmark_gate_report, build_benchmark_report, run_derivation_benchmark, run_label_consistency_benchmark, run_seeded_mismatch_benchmark, run_workflow_benchmark, summarize_benchmark_results
from .code_search import search_files
from .consistency import compare_files, compare_label_to_code
from .contracts import error_result, success_result
from .derivation import derive_step_for_label
from .doctor import doctor_report
from .governance import governance_policy
from .index_cache import load_or_build_index
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index
from .proof_obligations import check_proof_obligation
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_policy import release_readiness_report
from .typed_workflows import typed_obligation_for_label
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief

ToolHandler = Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]]


def _required_string(args: dict[str, Any], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing required string argument: {name}")
    return value


def _index_for_args(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    cache = args.get("cache")
    return load_or_build_index(root, Path(cache)) if isinstance(cache, str) and cache else build_index(root)


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
    index = _index_for_args(args)
    return search_index(index, _required_string(args, "query"), limit=int(args.get("limit", 10)))


def _tool_extract_latex_context(args: dict[str, Any]) -> dict[str, Any]:
    index = _index_for_args(args)
    return extract_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 2)),
        after=int(args.get("after", 2)),
    )


def _tool_extract_latex_neighborhood(args: dict[str, Any]) -> dict[str, Any]:
    index = _index_for_args(args)
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
        index=_index_for_args(args),
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
        index=_index_for_args(args),
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
        cache_path=args.get("cache") or None,
    )


def _tool_check_proof_obligation(args: dict[str, Any]) -> dict[str, Any]:
    assumptions = args.get("assumptions")
    if assumptions is None:
        assumptions = args.get("assumption")
    if assumptions is None:
        assumption_list = None
    elif isinstance(assumptions, str):
        assumption_list = [assumptions]
    elif isinstance(assumptions, list) and all(isinstance(item, str) for item in assumptions):
        assumption_list = assumptions
    else:
        raise ValueError("assumptions must be a string or list of strings")
    return check_proof_obligation(
        _required_string(args, "lhs"),
        _required_string(args, "rhs"),
        assumptions=assumption_list,
        backend=str(args.get("backend", "auto")),
    )


def _tool_audit_derivation_label(args: dict[str, Any]) -> dict[str, Any]:
    return audit_derivation_for_label(
        _required_string(args, "root"),
        _required_string(args, "label"),
        before=int(args.get("before", 0)),
        after=int(args.get("after", 0)),
        paragraph_context=bool(args.get("paragraph_context", False)),
        backend=str(args.get("backend", "auto")),
        cache_path=args.get("cache") or None,
    )


def _tool_audit_derivation_v2_label(args: dict[str, Any]) -> dict[str, Any]:
    return audit_derivation_v2_for_label(
        _required_string(args, "root"),
        _required_string(args, "label"),
        before=int(args.get("before", 0)),
        after=int(args.get("after", 0)),
        paragraph_context=bool(args.get("paragraph_context", False)),
        backend=str(args.get("backend", "sympy")),
        cache_path=args.get("cache") or None,
        summary_only=bool(args.get("summary_only", False)),
    )


def _optional_operations(args: dict[str, Any]) -> list[str] | None:
    operations = args.get("required_operations")
    if operations is None:
        operations = args.get("required_operation")
    if operations is None:
        return None
    if isinstance(operations, str):
        return [item.strip() for item in operations.split(",") if item.strip()]
    if isinstance(operations, list) and all(isinstance(item, str) for item in operations):
        return operations
    raise ValueError("required_operations must be a comma-separated string or list of strings")


def _tool_audit_kalman_recursion(args: dict[str, Any]) -> dict[str, Any]:
    return audit_kalman_recursion(
        _required_string(args, "code"),
        required_operations=_optional_operations(args),
    )


def _tool_typed_obligation_label(args: dict[str, Any]) -> dict[str, Any]:
    context_text = args.get("context_text")
    return typed_obligation_for_label(
        _required_string(args, "root"),
        _required_string(args, "label"),
        backend=str(args.get("backend", "sympy")),
        context_text=context_text if isinstance(context_text, str) else "",
    )


def _tool_run_benchmarks(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return build_benchmark_report(root)



def _tool_benchmark_gate(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return benchmark_gate_report(root)


def _tool_tool_matrix(args: dict[str, Any]) -> list[dict[str, Any]]:
    return tool_matrix()



def _tool_doctor(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    return doctor_report()


def _tool_release_corpus_manifest(args: dict[str, Any]) -> dict[str, Any]:
    root = args.get("root")
    return release_corpus_manifest(root if isinstance(root, str) else None)


def _tool_validate_release_corpus(args: dict[str, Any]) -> dict[str, Any]:
    root = args.get("root")
    return validate_release_corpus_manifest(root if isinstance(root, str) else None)


def _tool_governance_policy(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    return governance_policy()


def _tool_release_readiness(args: dict[str, Any]) -> dict[str, Any]:
    return release_readiness_report(Path(_required_string(args, "root")))


TOOL_HANDLERS: dict[str, ToolHandler] = {
    "search_latex": _tool_search_latex,
    "extract_latex_context": _tool_extract_latex_context,
    "extract_latex_neighborhood": _tool_extract_latex_neighborhood,
    "search_code_docs": _tool_search_code_docs,
    "compare_doc_code": _tool_compare_doc_code,
    "compare_label_code": _tool_compare_label_code,
    "derive_label_step": _tool_derive_label_step,
    "implementation_brief": _tool_implementation_brief,
    "check_proof_obligation": _tool_check_proof_obligation,
    "audit_derivation_label": _tool_audit_derivation_label,
    "audit_derivation_v2_label": _tool_audit_derivation_v2_label,
    "audit_kalman_recursion": _tool_audit_kalman_recursion,
    "typed_obligation_label": _tool_typed_obligation_label,
    "run_benchmarks": _tool_run_benchmarks,
    "benchmark_gate": _tool_benchmark_gate,
    "tool_matrix": _tool_tool_matrix,
    "doctor": _tool_doctor,
    "release_corpus_manifest": _tool_release_corpus_manifest,
    "validate_release_corpus": _tool_validate_release_corpus,
    "governance_policy": _tool_governance_policy,
    "release_readiness": _tool_release_readiness,
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
            ("check_proof_obligation", "Check a bounded derivation/proof obligation with optional backend assistance."),
            ("audit_derivation_label", "Audit proof obligations extracted from a labeled derivation block."),
            ("audit_derivation_v2_label", "Audit a labeled derivation with typed routing and release-readiness evidence."),
            ("audit_kalman_recursion", "Audit AST-level Kalman recursion structure in Python code."),
            ("typed_obligation_label", "Build typed/dimensional diagnostics for a labeled math obligation."),
            ("run_benchmarks", "Run seeded consistency benchmarks."),
            ("benchmark_gate", "Return CI-friendly benchmark gate results."),
            ("tool_matrix", "Return the current MathDevMCP tool matrix."),
            ("doctor", "Report external backend capabilities and environment diagnostics."),
            ("release_corpus_manifest", "Return the release corpus manifest."),
            ("validate_release_corpus", "Validate release corpus privacy and gate metadata."),
            ("governance_policy", "Return security and governance policy."),
            ("release_readiness", "Return an auditable release-readiness report."),
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
