"""In-process MCP facade over the tested MathDevMCP library functions.

The facade keeps MCP tools narrow and structured. It should not grow separate
business logic from the CLI/library path; tool handlers should delegate to the
same report-producing functions used by tests and release scripts.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .benchmarks import benchmark_gate_report, build_benchmark_report, run_derivation_benchmark, run_label_consistency_benchmark, run_seeded_mismatch_benchmark, run_workflow_benchmark, summarize_benchmark_results
from .code_search import search_files
from .consistency import compare_files, compare_label_to_code
from .contracts import attach_contract, error_result, success_result
from .derivation import derive_step_for_label
from .doctor import doctor_report
from .governance import governance_policy
from .index_cache import load_or_build_index
from .implementation_audit import audit_implementation_label
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index
from .lean_check import check_lean_source
from .lean_readiness import lean_readiness
from .proof_obligations import check_proof_obligation
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_profile_analysis import release_profile_analysis
from .release_policy import release_readiness_report
from .status_taxonomy import status_taxonomy
from .typed_workflows import typed_obligation_for_label
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief

ToolHandler = Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]]


@dataclass(frozen=True)
class MCPToolSpec:
    name: str
    handler: ToolHandler
    description: str
    output_contract: str
    tier: str
    certifying_capable: bool = False
    stability: str = "stable"
    server_name: str | None = None
    optional_capability: str | None = None
    deprecated: bool = False
    replacement: str | None = None

    @property
    def exposed_server_name(self) -> str:
        return self.server_name or self.name


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


def _tool_latex_label_lookup(args: dict[str, Any]) -> dict[str, Any]:
    return attach_contract(_tool_extract_latex_neighborhood(args), "latex_paragraph_context")


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


def _tool_audit_implementation_label(args: dict[str, Any]) -> dict[str, Any]:
    return audit_implementation_label(
        _required_string(args, "root"),
        _required_string(args, "label"),
        _required_string(args, "code"),
        before=int(args.get("before", 0)),
        after=int(args.get("after", 0)),
        paragraph_context=bool(args.get("paragraph_context", False)),
        required_terms=_optional_terms(args),
        required_operations=_optional_operations(args),
        backend=str(args.get("backend", "sympy")),
        cache_path=args.get("cache") or None,
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


def _tool_check_equality(args: dict[str, Any]) -> dict[str, Any]:
    return _tool_check_proof_obligation(args)


def _tool_lean_check(args: dict[str, Any]) -> dict[str, Any]:
    return check_lean_source(
        _required_string(args, "source"),
        timeout_seconds=int(args.get("timeout_seconds", 10)),
        allow_sorry=bool(args.get("allow_sorry", False)),
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
    private_manifest = args.get("private_manifest")
    return release_corpus_manifest(root if isinstance(root, str) else None, private_manifest=private_manifest if isinstance(private_manifest, str) else None)


def _tool_validate_release_corpus(args: dict[str, Any]) -> dict[str, Any]:
    root = args.get("root")
    private_manifest = args.get("private_manifest")
    return validate_release_corpus_manifest(root if isinstance(root, str) else None, private_manifest=private_manifest if isinstance(private_manifest, str) else None)


def _tool_governance_policy(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    return governance_policy()


def _tool_release_readiness(args: dict[str, Any]) -> dict[str, Any]:
    return release_readiness_report(Path(_required_string(args, "root")), profile=str(args.get("profile", "base")))


def _tool_release_profile_analysis(args: dict[str, Any]) -> dict[str, Any]:
    return release_profile_analysis(Path(_required_string(args, "root")))


def _tool_lean_readiness(args: dict[str, Any]) -> dict[str, Any]:
    root = args.get("root")
    return lean_readiness(root if isinstance(root, str) and root else None)


def _tool_status_taxonomy(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    return status_taxonomy()


MCP_TOOL_SPECS: tuple[MCPToolSpec, ...] = (
    MCPToolSpec("search_latex", _tool_search_latex, "Search indexed LaTeX blocks with provenance.", "latex_search_results", "primitive"),
    MCPToolSpec("latex_label_lookup", _tool_latex_label_lookup, "Fetch a labeled LaTeX block with paragraph neighborhood and provenance.", "latex_paragraph_context", "primitive"),
    MCPToolSpec(
        "extract_latex_context",
        _tool_extract_latex_context,
        "Deprecated alias for label lookup with line context.",
        "latex_context",
        "primitive",
        stability="deprecated",
        deprecated=True,
        replacement="latex_label_lookup",
    ),
    MCPToolSpec(
        "extract_latex_neighborhood",
        _tool_extract_latex_neighborhood,
        "Deprecated alias for paragraph-level label lookup.",
        "latex_paragraph_context",
        "primitive",
        stability="deprecated",
        deprecated=True,
        replacement="latex_label_lookup",
    ),
    MCPToolSpec("search_code_docs", _tool_search_code_docs, "Search code and document files together.", "code_doc_search_results", "primitive"),
    MCPToolSpec("compare_doc_code", _tool_compare_doc_code, "Compare document text against code text.", "doc_code_consistency_result", "workflow", stability="experimental"),
    MCPToolSpec("audit_implementation_label", _tool_audit_implementation_label, "Audit a labeled document block against a code implementation.", "implementation_audit_result", "workflow"),
    MCPToolSpec(
        "compare_label_code",
        _tool_compare_label_code,
        "Deprecated alias for audit_implementation_label.",
        "label_consistency_result",
        "workflow",
        stability="deprecated",
        deprecated=True,
        replacement="audit_implementation_label",
    ),
    MCPToolSpec("derive_label_step", _tool_derive_label_step, "Check a derivation step against labeled document context.", "label_derivation_result", "workflow", certifying_capable=True),
    MCPToolSpec("implementation_brief", _tool_implementation_brief, "Build a document-grounded implementation brief.", "implementation_brief", "workflow"),
    MCPToolSpec(
        "check_equality",
        _tool_check_equality,
        "Check lhs == rhs with a deterministic symbolic backend when available.",
        "proof_obligation_result",
        "primitive",
        certifying_capable=True,
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "check_proof_obligation",
        _tool_check_proof_obligation,
        "Deprecated alias for check_equality.",
        "proof_obligation_result",
        "primitive",
        certifying_capable=True,
        stability="deprecated",
        optional_capability="symbolic_backend",
        deprecated=True,
        replacement="check_equality",
    ),
    MCPToolSpec(
        "lean_check",
        _tool_lean_check,
        "Compile a supplied Lean source. Certifying only when Lean exits 0 and the source has no placeholders.",
        "lean_check_result",
        "primitive",
        certifying_capable=True,
        optional_capability="lean_backend",
    ),
    MCPToolSpec(
        "audit_derivation_label",
        _tool_audit_derivation_label,
        "Audit proof obligations extracted from a labeled derivation block.",
        "proof_audit_result",
        "workflow",
        certifying_capable=True,
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "audit_derivation_v2_label",
        _tool_audit_derivation_v2_label,
        "Audit a labeled derivation with typed routing and release-readiness evidence.",
        "proof_audit_v2_result",
        "workflow",
        certifying_capable=True,
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec("audit_kalman_recursion", _tool_audit_kalman_recursion, "Audit AST-level Kalman recursion structure in Python code.", "kalman_recursion_audit", "workflow"),
    MCPToolSpec("typed_obligation_label", _tool_typed_obligation_label, "Build typed/dimensional diagnostics for a labeled math obligation.", "typed_obligation_label_diagnostic", "workflow"),
    MCPToolSpec("run_benchmarks", _tool_run_benchmarks, "Run seeded consistency benchmarks.", "benchmark_results", "operational"),
    MCPToolSpec("benchmark_gate", _tool_benchmark_gate, "Return CI-friendly benchmark gate results.", "benchmark_gate", "operational"),
    MCPToolSpec("tool_matrix", _tool_tool_matrix, "Return the current MathDevMCP tool matrix.", "tool_matrix", "informational", server_name="get_tool_matrix"),
    MCPToolSpec("status_taxonomy", _tool_status_taxonomy, "Return the current MathDevMCP status and substatus taxonomy.", "status_taxonomy", "informational"),
    MCPToolSpec("doctor", _tool_doctor, "Report external backend capabilities and environment diagnostics.", "doctor_report", "operational"),
    MCPToolSpec("release_corpus_manifest", _tool_release_corpus_manifest, "Return the release corpus manifest.", "release_corpus_manifest", "operational"),
    MCPToolSpec("validate_release_corpus", _tool_validate_release_corpus, "Validate release corpus privacy and gate metadata.", "release_corpus_validation_report", "operational"),
    MCPToolSpec("governance_policy", _tool_governance_policy, "Return security and governance policy.", "governance_policy", "informational"),
    MCPToolSpec("release_readiness", _tool_release_readiness, "Return an auditable release-readiness report.", "release_readiness_report", "operational"),
    MCPToolSpec("release_profile_analysis", _tool_release_profile_analysis, "Analyze every release profile and remaining profile gaps.", "release_profile_analysis", "operational"),
    MCPToolSpec("lean_readiness", _tool_lean_readiness, "Report direct Lean, Lake, and LeanDojo readiness separately.", "lean_readiness", "operational"),
)


TOOL_HANDLERS: dict[str, ToolHandler] = {spec.name: spec.handler for spec in MCP_TOOL_SPECS}


def list_mcp_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": spec.name,
            "server_name": spec.exposed_server_name,
            "description": spec.description,
            "output_contract": spec.output_contract,
            "tier": spec.tier,
            "stability": spec.stability,
            "certifying_capable": spec.certifying_capable,
            "optional_capability": spec.optional_capability,
            "deprecated": spec.deprecated,
            "replacement": spec.replacement,
        }
        for spec in MCP_TOOL_SPECS
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
    except Exception:
        # MCP clients need a stable public envelope. Raw tracebacks and local
        # paths belong in logs/debug sessions, not in default tool responses.
        return error_result("tool_execution_error", f"MathDevMCP tool failed during execution: {name}")
