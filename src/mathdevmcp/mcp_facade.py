"""In-process MCP facade over the tested MathDevMCP library functions.

The facade keeps MCP tools narrow and structured. It should not grow separate
business logic from the CLI/library path; tool handlers should delegate to the
same report-producing functions used by tests and release scripts.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from .assumptions_for import audit_and_propose_assumptions as high_level_audit_and_propose_assumptions
from .assumptions_for import assumptions_for as high_level_assumptions_for
from .audit_and_propose_fix import audit_and_propose_fix as high_level_audit_and_propose_fix
from .audit_math_to_code import audit_math_to_code as high_level_audit_math_to_code
from .benchmarks import benchmark_gate_report, build_benchmark_report, build_high_level_workflow_quality_report, build_workbench_benchmark_quality_report, run_derivation_benchmark, run_label_consistency_benchmark, run_seeded_mismatch_benchmark, run_workflow_benchmark, summarize_benchmark_results
from .code_search import search_files
from .consistency import compare_files, compare_label_to_code
from .contracts import attach_contract, error_result, success_result
from .derivation import derive_step_for_label
from .derivation_audit_report import audit_and_propose_derivations as high_level_audit_and_propose_derivations
from .debug_derivation import debug_derivation as high_level_debug_derivation
from .derive_from import derive_from as high_level_derive_from
from .derive_or_refute import derive_or_refute
from .document_derivation_tree import audit_document_derivation_tree as high_level_audit_document_derivation_tree
from .doctor import doctor_report
from .equation_code_match import code_implements_equation
from .external_tool_policy import external_tool_first_plan as high_level_external_tool_first_plan
from .governance import governance_policy
from .index_cache import load_or_build_index
from .implementation_audit import audit_implementation_label
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index_filtered
from .lean_check import check_lean_source
from .lean_readiness import lean_readiness
from .literature_local_audit import literature_local_audit
from .math_claim_classifier import classify_math_claim
from .math_change_impact import math_change_impact
from .math_document_rigor import audit_math_document_rigor as high_level_audit_math_document_rigor
from .math_document_rigor import plan_math_document_rigor_audit as high_level_plan_math_document_rigor_audit
from .report_claim_boundary import audit_report_claim_boundary as high_level_audit_report_claim_boundary
from .math_review_packet import build_math_review_packet
from .math_to_tests import generate_math_tests
from .notation_reconciliation import reconcile_notation
from .proof_obligations import check_proof_obligation
from .prepare_review_packet import prepare_review_packet as high_level_prepare_review_packet, review_packet_agent_handoff
from .propose_fix import propose_fix as high_level_propose_fix, proposal_agent_handoff
from .prove_or_counterexample import prove_or_counterexample as high_level_prove_or_counterexample
from .prove_or_refute import prove_or_refute
from .proof_gap import localize_proof_gap
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_profile_analysis import release_profile_analysis
from .release_policy import release_readiness_report
from .status_taxonomy import status_taxonomy
from .temporal_contracts import audit_temporal_contract
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


def _looks_like_path(value: str) -> bool:
    return (
        "/" in value
        or "\\" in value
        or value.startswith(".")
        or bool(re.search(r"\.(py|tex|md|json|txt|lean)\b", value))
    )


def _path_exists_for_summary(value: str) -> bool:
    try:
        return Path(value).exists()
    except (OSError, ValueError):
        return False


def _redacted_input_summary(arguments: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key, value in arguments.items():
        if isinstance(value, str):
            looks_like_path = _looks_like_path(value)
            summary[key] = {
                "type": "str",
                "chars": len(value),
                "looks_like_path": looks_like_path,
                "exists": _path_exists_for_summary(value) if looks_like_path else False,
            }
        elif isinstance(value, list):
            summary[key] = {"type": "list", "items": len(value)}
        elif value is None:
            summary[key] = {"type": "null"}
        else:
            summary[key] = {"type": type(value).__name__}
    return summary


def _failure_stage(exc: Exception) -> str:
    if isinstance(exc, KeyError):
        return "retrieve_label"
    if isinstance(exc, FileNotFoundError):
        return "read_code"
    if isinstance(exc, SyntaxError):
        return "parse_code"
    message = str(exc).lower()
    if "label" in message:
        return "retrieve_label"
    if "latex" in message or "tex" in message:
        return "parse_latex"
    if "sympy" in message or "backend" in message:
        return "backend"
    return "compare"


def _suggested_action(stage: str) -> str:
    suggestions = {
        "retrieve_label": "Verify the label with search_latex or rebuild the LaTeX index/cache.",
        "read_code": "Check that the code argument is an existing readable file path.",
        "parse_code": "Check that the code file is valid Python for AST-based audit.",
        "parse_latex": "Inspect the LaTeX source and retry with a fresh index/cache.",
        "backend": "Retry with a supported backend or inspect backend readiness diagnostics.",
        "compare": "Check the tool arguments and narrow the requested comparison.",
    }
    return suggestions.get(stage, "Check the tool arguments and retry with a narrower request.")


def _tool_failure_diagnostics(exc: Exception, arguments: dict[str, Any]) -> dict[str, Any]:
    stage = _failure_stage(exc)
    return {
        "stage": stage,
        "exception_type": exc.__class__.__name__,
        "recoverable": True,
        "suggested_action": _suggested_action(stage),
        "input_summary": _redacted_input_summary(arguments),
    }


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
    return search_index_filtered(
        index,
        _required_string(args, "query"),
        limit=int(args.get("limit", 10)),
        file=args.get("file") if isinstance(args.get("file"), str) else None,
        include_globs=_optional_string_list_arg(args, "include_globs"),
        exclude_globs=_optional_string_list_arg(args, "exclude_globs"),
    )


def _tool_extract_latex_context(args: dict[str, Any]) -> dict[str, Any]:
    index = _index_for_args(args)
    return extract_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 2)),
        after=int(args.get("after", 2)),
        file=args.get("file") if isinstance(args.get("file"), str) else None,
        include_globs=_optional_string_list_arg(args, "include_globs"),
        exclude_globs=_optional_string_list_arg(args, "exclude_globs"),
    )


def _tool_extract_latex_neighborhood(args: dict[str, Any]) -> dict[str, Any]:
    index = _index_for_args(args)
    return extract_paragraph_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 1)),
        after=int(args.get("after", 1)),
        file=args.get("file") if isinstance(args.get("file"), str) else None,
        include_globs=_optional_string_list_arg(args, "include_globs"),
        exclude_globs=_optional_string_list_arg(args, "exclude_globs"),
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


def _tool_code_implements_equation(args: dict[str, Any]) -> dict[str, Any]:
    aliases = args.get("aliases")
    if aliases is not None and not isinstance(aliases, dict):
        raise ValueError("aliases must be an object mapping equation symbols to code names")
    return code_implements_equation(
        _required_string(args, "equation"),
        _required_string(args, "code"),
        aliases=aliases,
    )


def _tool_classify_math_claim(args: dict[str, Any]) -> dict[str, Any]:
    evidence = args.get("evidence", [])
    if evidence is None:
        evidence = []
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list of objects")
    return classify_math_claim(_required_string(args, "claim"), evidence=evidence)


def _tool_audit_report_claim_boundary(args: dict[str, Any]) -> dict[str, Any]:
    snippets = args.get("evidence_snippets", args.get("evidence_snippet"))
    if isinstance(snippets, str):
        snippets = [snippets]
    if snippets is not None and (not isinstance(snippets, list) or not all(isinstance(item, str) for item in snippets)):
        raise ValueError("evidence_snippets must be a string or list of strings")
    source = args.get("source")
    if source is not None and not isinstance(source, dict):
        raise ValueError("source must be an object")
    return high_level_audit_report_claim_boundary(
        _required_string(args, "claim"),
        evidence_snippets=snippets,
        source=source,
    )


def _tool_reconcile_notation(args: dict[str, Any]) -> dict[str, Any]:
    left_records = args.get("left_records")
    right_records = args.get("right_records")
    if not isinstance(left_records, list) or not isinstance(right_records, list):
        raise ValueError("left_records and right_records must be lists of notation objects")
    return reconcile_notation(
        left_records,
        right_records,
        left_context=str(args.get("left_context", "left")),
        right_context=str(args.get("right_context", "right")),
    )


def _optional_list_arg(args: dict[str, Any], name: str) -> list[Any] | None:
    value = args.get(name)
    if value is None:
        return None
    if isinstance(value, list):
        return value
    raise ValueError(f"{name} must be a list")


def _optional_string_list_arg(args: dict[str, Any], name: str, *aliases: str) -> list[str] | None:
    value = args.get(name)
    if value is None:
        for alias in aliases:
            value = args.get(alias)
            if value is not None:
                break
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    names = ", ".join((name, *aliases))
    raise ValueError(f"{names} must be a string or list of strings")


def _tool_generate_math_tests(args: dict[str, Any]) -> dict[str, Any]:
    numeric_fixtures = args.get("numeric_fixtures")
    if numeric_fixtures is not None and not isinstance(numeric_fixtures, dict):
        raise ValueError("numeric_fixtures must be an object")
    return generate_math_tests(
        _required_string(args, "target"),
        assumptions=_optional_list_arg(args, "assumptions"),
        notation=_optional_list_arg(args, "notation"),
        kinds=_optional_list_arg(args, "kinds"),
        numeric_fixtures=numeric_fixtures,
        expected_failure_mode=str(args.get("expected_failure_mode", "mismatch_or_unverified")),
    )


def _tool_math_review_packet(args: dict[str, Any]) -> dict[str, Any]:
    source = args.get("source")
    evidence = args.get("evidence", [])
    if source is not None and not isinstance(source, dict):
        raise ValueError("source must be an object")
    if evidence is None:
        evidence = []
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list of objects")
    packet_id = args.get("packet_id")
    return build_math_review_packet(
        _required_string(args, "question"),
        source=source,
        evidence=evidence,
        packet_id=packet_id if isinstance(packet_id, str) and packet_id else None,
    )


def _optional_dict_arg(args: dict[str, Any], name: str) -> dict[str, Any] | None:
    value = args.get(name)
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    raise ValueError(f"{name} must be an object")


def _tool_math_change_impact(args: dict[str, Any]) -> dict[str, Any]:
    return math_change_impact(
        _required_string(args, "changed_id"),
        changed_kind=str(args.get("changed_kind", "label")),
        graph=_optional_dict_arg(args, "graph"),
        packets=_optional_list_arg(args, "packets"),
        code_links=_optional_list_arg(args, "code_links"),
        generated_tests=_optional_list_arg(args, "generated_tests"),
        claims=_optional_list_arg(args, "claims"),
        assumptions=_optional_list_arg(args, "assumptions"),
    )


def _tool_literature_local_audit(args: dict[str, Any]) -> dict[str, Any]:
    theorem_assumptions = args.get("theorem_assumptions")
    local_assumptions = args.get("local_assumptions")
    if not isinstance(theorem_assumptions, list) or not isinstance(local_assumptions, list):
        raise ValueError("theorem_assumptions and local_assumptions must be lists of objects")
    notation_audit = args.get("notation_audit")
    if notation_audit is not None and not isinstance(notation_audit, dict):
        raise ValueError("notation_audit must be an object")
    return literature_local_audit(
        _required_string(args, "theorem_id"),
        theorem_assumptions,
        local_assumptions,
        local_context=str(args.get("local_context", "local")),
        notation_audit=notation_audit,
        human_waivers=_optional_list_arg(args, "human_waivers"),
    )


def _tool_high_level_derive_from(args: dict[str, Any]) -> dict[str, Any]:
    return high_level_derive_from(
        _required_string(args, "target"),
        givens=_optional_string_list_arg(args, "givens", "given"),
        assumptions=_optional_string_list_arg(args, "assumptions", "assumption"),
        lhs=args.get("lhs") if isinstance(args.get("lhs"), str) and args.get("lhs") else None,
        rhs=args.get("rhs") if isinstance(args.get("rhs"), str) and args.get("rhs") else None,
        backend=str(args.get("backend", "auto")),
    )


def _tool_high_level_prove_or_counterexample(args: dict[str, Any]) -> dict[str, Any]:
    return high_level_prove_or_counterexample(
        _required_string(args, "claim"),
        assumptions=_optional_string_list_arg(args, "assumptions", "assumption"),
        lhs=args.get("lhs") if isinstance(args.get("lhs"), str) and args.get("lhs") else None,
        rhs=args.get("rhs") if isinstance(args.get("rhs"), str) and args.get("rhs") else None,
        backend=str(args.get("backend", "auto")),
        lean_source=args.get("lean_source") if isinstance(args.get("lean_source"), str) and args.get("lean_source") else None,
    )


def _tool_high_level_assumptions_for(args: dict[str, Any]) -> dict[str, Any]:
    return high_level_assumptions_for(
        _required_string(args, "target"),
        provided_assumptions=_optional_string_list_arg(args, "provided_assumptions", "provided_assumption"),
    )


def _tool_high_level_audit_and_propose_assumptions(args: dict[str, Any]) -> dict[str, Any]:
    labels = args.get("labels")
    if labels is None:
        labels = args.get("label")
    if isinstance(labels, str):
        labels = [labels]
    if labels is not None and (not isinstance(labels, list) or not all(isinstance(item, str) for item in labels)):
        raise ValueError("labels must be a string or list of strings")
    output = args.get("output")
    if output is None:
        output = args.get("output_path")
    return high_level_audit_and_propose_assumptions(
        _required_string(args, "question"),
        target=args.get("target") if isinstance(args.get("target"), str) and args.get("target") else None,
        root=args.get("root") if isinstance(args.get("root"), str) and args.get("root") else None,
        labels=labels,
        provided_assumptions=_optional_string_list_arg(args, "provided_assumptions", "provided_assumption"),
        output_path=output if isinstance(output, str) and output else None,
    )


def _tool_high_level_audit_and_propose_derivations(args: dict[str, Any]) -> dict[str, Any]:
    labels = args.get("labels")
    if labels is None:
        labels = args.get("label")
    if isinstance(labels, str):
        labels = [labels]
    if labels is not None and (not isinstance(labels, list) or not all(isinstance(item, str) for item in labels)):
        raise ValueError("labels must be a string or list of strings")
    output = args.get("output")
    if output is None:
        output = args.get("output_path")
    return high_level_audit_and_propose_derivations(
        _required_string(args, "question"),
        target=args.get("target") if isinstance(args.get("target"), str) and args.get("target") else None,
        root=args.get("root") if isinstance(args.get("root"), str) and args.get("root") else None,
        labels=labels,
        givens=_optional_string_list_arg(args, "givens", "given"),
        assumptions=_optional_string_list_arg(args, "assumptions", "assumption"),
        backend=str(args.get("backend", "auto")),
        output_path=output if isinstance(output, str) and output else None,
    )


def _tool_high_level_debug_derivation(args: dict[str, Any]) -> dict[str, Any]:
    steps = _optional_string_list_arg(args, "steps", "step")
    if not steps:
        raise ValueError("steps must contain at least one string")
    return high_level_debug_derivation(
        steps,
        assumptions=_optional_string_list_arg(args, "assumptions", "assumption"),
        backend=str(args.get("backend", "auto")),
    )


def _tool_high_level_audit_math_to_code(args: dict[str, Any]) -> dict[str, Any]:
    aliases = args.get("aliases")
    if aliases is not None and not isinstance(aliases, dict):
        raise ValueError("aliases must be an object mapping math symbols to code names")
    return high_level_audit_math_to_code(
        _required_string(args, "math"),
        _required_string(args, "code"),
        aliases=aliases,
    )


def _tool_high_level_prepare_review_packet(args: dict[str, Any]) -> dict[str, Any]:
    source = args.get("source")
    evidence = args.get("evidence")
    if source is not None and not isinstance(source, dict):
        raise ValueError("source must be an object")
    if evidence is not None and not isinstance(evidence, list):
        raise ValueError("evidence must be a list of objects")
    result = high_level_prepare_review_packet(
        _required_string(args, "question"),
        evidence=evidence,
        source=source,
        packet_id=args.get("packet_id") if isinstance(args.get("packet_id"), str) and args.get("packet_id") else None,
    )
    if bool(args.get("handoff")):
        return review_packet_agent_handoff(result)
    return result


def _tool_high_level_propose_fix(args: dict[str, Any]) -> dict[str, Any]:
    evidence = args.get("evidence") or []
    if not isinstance(evidence, list) or not all(isinstance(item, dict) for item in evidence):
        raise ValueError("evidence must be a list of objects")
    source = args.get("source")
    if source is not None and not isinstance(source, dict):
        raise ValueError("source must be an object")
    result = high_level_propose_fix(
        _required_string(args, "question"),
        evidence=evidence,
        source=source,
        doc_root=args.get("root") or args.get("doc_root") or None,
        query=args.get("query") or None,
        code_path=args.get("code") or args.get("code_path") or None,
        label=args.get("label") or None,
        required_terms=_optional_terms(args),
        lhs=args.get("lhs") or None,
        rhs=args.get("rhs") or None,
        limit=int(args.get("limit", 3)),
        cache_path=args.get("cache") or None,
    )
    if bool(args.get("handoff")):
        return proposal_agent_handoff(result)
    return result


def _tool_high_level_audit_and_propose_fix(args: dict[str, Any]) -> dict[str, Any]:
    evidence = args.get("evidence")
    if evidence is not None and (not isinstance(evidence, list) or not all(isinstance(item, dict) for item in evidence)):
        raise ValueError("evidence must be a list of objects")
    labels = args.get("labels")
    if labels is None:
        labels = args.get("label")
    if isinstance(labels, str):
        labels = [labels]
    if labels is not None and (not isinstance(labels, list) or not all(isinstance(item, str) for item in labels)):
        raise ValueError("labels must be a string or list of strings")
    source = args.get("source")
    if source is not None and not isinstance(source, dict):
        raise ValueError("source must be an object")
    backend_order = args.get("backend_order", args.get("validation_backend_order"))
    if backend_order is None:
        backend_order = args.get("validation_backends")
    if isinstance(backend_order, str):
        backend_order = [backend_order]
    if backend_order is not None and (not isinstance(backend_order, list) or not all(isinstance(item, str) for item in backend_order)):
        raise ValueError("backend_order must be a string or list of strings")
    return high_level_audit_and_propose_fix(
        _required_string(args, "question"),
        root=args.get("root") or None,
        labels=labels,
        whole_document=bool(args.get("whole_document", args.get("document", False))),
        target_file=args.get("file") or args.get("target_file") or None,
        label_limit=int(args["label_limit"]) if args.get("label_limit") is not None else None,
        label_kinds=args.get("label_kinds") if isinstance(args.get("label_kinds"), list) else None,
        evidence=evidence,
        source=source,
        paragraph_context=bool(args.get("paragraph_context", True)),
        summary_only=bool(args.get("summary_only", True)),
        backend=str(args.get("backend", "sympy")),
        validate_proposed_fixes=bool(args.get("validate_proposed_fixes", False)),
        certifier_policy=str(args.get("certifier_policy", "require_attempt_when_encodable")),
        backend_order=backend_order,
        workers=int(args.get("workers", 1)),
        output_path=args.get("output") or args.get("output_path") or None,
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


def _tool_derive_or_refute(args: dict[str, Any]) -> dict[str, Any]:
    givens = args.get("givens") or args.get("given") or []
    assumptions = args.get("assumptions") or args.get("assumption") or []
    if isinstance(givens, str):
        givens = [givens]
    if isinstance(assumptions, str):
        assumptions = [assumptions]
    if not isinstance(givens, list) or not all(isinstance(item, str) for item in givens):
        raise ValueError("givens must be a string or list of strings")
    if not isinstance(assumptions, list) or not all(isinstance(item, str) for item in assumptions):
        raise ValueError("assumptions must be a string or list of strings")
    return derive_or_refute(
        _required_string(args, "target"),
        givens=givens,
        assumptions=assumptions,
        lhs=args.get("lhs") if isinstance(args.get("lhs"), str) and args.get("lhs") else None,
        rhs=args.get("rhs") if isinstance(args.get("rhs"), str) and args.get("rhs") else None,
        backend=str(args.get("backend", "auto")),
    )


def _tool_prove_or_refute(args: dict[str, Any]) -> dict[str, Any]:
    assumptions = args.get("assumptions") or args.get("assumption") or []
    if isinstance(assumptions, str):
        assumptions = [assumptions]
    if not isinstance(assumptions, list) or not all(isinstance(item, str) for item in assumptions):
        raise ValueError("assumptions must be a string or list of strings")
    return prove_or_refute(
        _required_string(args, "claim"),
        assumptions=assumptions,
        lhs=args.get("lhs") if isinstance(args.get("lhs"), str) and args.get("lhs") else None,
        rhs=args.get("rhs") if isinstance(args.get("rhs"), str) and args.get("rhs") else None,
        backend=str(args.get("backend", "auto")),
        lean_source=args.get("lean_source") if isinstance(args.get("lean_source"), str) and args.get("lean_source") else None,
    )


def _tool_localize_proof_gap(args: dict[str, Any]) -> dict[str, Any]:
    steps = args.get("steps") or args.get("step")
    assumptions = args.get("assumptions") or args.get("assumption") or []
    if isinstance(steps, str):
        steps = [steps]
    if isinstance(assumptions, str):
        assumptions = [assumptions]
    if not isinstance(steps, list) or not all(isinstance(item, str) for item in steps):
        raise ValueError("steps must be a list of strings")
    if not isinstance(assumptions, list) or not all(isinstance(item, str) for item in assumptions):
        raise ValueError("assumptions must be a string or list of strings")
    return localize_proof_gap(steps, assumptions=assumptions, backend=str(args.get("backend", "auto")))


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


def _tool_audit_temporal_contract(args: dict[str, Any]) -> dict[str, Any]:
    bindings = args.get("required_bindings")
    if not isinstance(bindings, dict):
        raise ValueError("required_bindings must be a mapping from temporal symbols to binding specs")
    return audit_temporal_contract(
        _required_string(args, "root"),
        _required_string(args, "label"),
        _required_string(args, "code"),
        bindings,
        before=int(args.get("before", 1)),
        after=int(args.get("after", 1)),
    )


def _tool_run_benchmarks(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return build_benchmark_report(root)



def _tool_benchmark_gate(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return benchmark_gate_report(root)


def _tool_workbench_benchmark_quality(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return build_workbench_benchmark_quality_report(root)


def _tool_high_level_workflow_quality(args: dict[str, Any]) -> dict[str, Any]:
    root = Path(_required_string(args, "root"))
    return build_high_level_workflow_quality_report(root)


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


def _tool_plan_math_document_rigor_audit(args: dict[str, Any]) -> dict[str, Any]:
    focus_labels = args.get("focus_labels", args.get("focus_label"))
    if isinstance(focus_labels, str):
        focus_labels = [focus_labels]
    if focus_labels is not None and (not isinstance(focus_labels, list) or not all(isinstance(item, str) for item in focus_labels)):
        raise ValueError("focus_labels must be a string or list of strings")
    max_labels = args.get("max_labels", 30)
    max_label_value = int(max_labels) if max_labels is not None else None
    if max_label_value is not None and max_label_value <= 0:
        max_label_value = None
    return high_level_plan_math_document_rigor_audit(
        _required_string(args, "tex_path"),
        focus_labels=focus_labels,
        max_labels=max_label_value,
    )


def _tool_audit_math_document_rigor(args: dict[str, Any]) -> dict[str, Any]:
    focus_labels = args.get("focus_labels", args.get("focus_label"))
    if isinstance(focus_labels, str):
        focus_labels = [focus_labels]
    if focus_labels is not None and (not isinstance(focus_labels, list) or not all(isinstance(item, str) for item in focus_labels)):
        raise ValueError("focus_labels must be a string or list of strings")
    validation_backends = args.get("validation_backends", args.get("validation_backend"))
    if isinstance(validation_backends, str):
        validation_backends = [validation_backends]
    if validation_backends is not None and (not isinstance(validation_backends, list) or not all(isinstance(item, str) for item in validation_backends)):
        raise ValueError("validation_backends must be a string or list of strings")
    max_labels = args.get("max_labels", 30)
    max_label_value = int(max_labels) if max_labels is not None else None
    if max_label_value is not None and max_label_value <= 0:
        max_label_value = None
    return high_level_audit_math_document_rigor(
        _required_string(args, "tex_path"),
        output_md=args.get("output_md") or None,
        output_json=args.get("output_json") or None,
        focus_labels=focus_labels,
        max_labels=max_label_value,
        backend_env=str(args.get("backend_env", "mathdevmcp-backends")),
        validation_backends=validation_backends,
    )


def _tool_audit_document_derivation_tree(args: dict[str, Any]) -> dict[str, Any]:
    focus_labels = args.get("focus_labels", args.get("focus_label"))
    if isinstance(focus_labels, str):
        focus_labels = [focus_labels]
    if focus_labels is not None and (not isinstance(focus_labels, list) or not all(isinstance(item, str) for item in focus_labels)):
        raise ValueError("focus_labels must be a string or list of strings")
    max_labels = args.get("max_labels", 30)
    max_label_value = int(max_labels) if max_labels is not None else None
    if max_label_value is not None and max_label_value <= 0:
        max_label_value = None
    return high_level_audit_document_derivation_tree(
        _required_string(args, "tex_path"),
        output_md=args.get("output_md") or None,
        output_json=args.get("output_json") or None,
        focus_labels=focus_labels,
        max_labels=max_label_value,
        budget_profile=str(args.get("budget_profile", "standard")),
        max_attempts=int(args.get("max_attempts", 3)),
        backend_env=str(args.get("backend_env", "mathdevmcp-backends")),
        search_mode=str(args.get("search_mode", "agent_guided")),
        grounding_policy=str(args.get("grounding_policy", "strict")),
        workers=int(args.get("workers", 1)),
    )


def _tool_status_taxonomy(args: dict[str, Any]) -> dict[str, Any]:
    _ = args
    return status_taxonomy()


def _tool_external_tool_first_plan(args: dict[str, Any]) -> dict[str, Any]:
    capabilities = args.get("capabilities")
    integrations = args.get("integrations")
    if capabilities is not None and not isinstance(capabilities, dict):
        raise ValueError("capabilities must be an object")
    if integrations is not None and not isinstance(integrations, dict):
        raise ValueError("integrations must be an object")
    gap_justification = args.get("gap_justification")
    return high_level_external_tool_first_plan(
        _required_string(args, "target"),
        goal_kind=str(args.get("goal_kind", "derivation")),
        capabilities=capabilities,
        integrations=integrations,
        allow_in_house_gap=bool(args.get("allow_in_house_gap", False)),
        gap_justification=gap_justification if isinstance(gap_justification, str) else None,
    )


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
    MCPToolSpec("compare_doc_code", _tool_compare_doc_code, "Compare a document file against a code file; doc and code must be filesystem paths, not raw text.", "doc_code_consistency_result", "workflow", stability="experimental"),
    MCPToolSpec(
        "code_implements_equation",
        _tool_code_implements_equation,
        "Compare equation terms against Python code structure without executing code.",
        "equation_code_match_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "classify_math_claim",
        _tool_classify_math_claim,
        "Classify a math claim by supplied evidence without promoting diagnostics to proof.",
        "math_claim_classification",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "audit_report_claim_boundary",
        _tool_audit_report_claim_boundary,
        "Classify report-status and nonclaim prose without treating it as a theorem claim.",
        "report_claim_boundary_audit",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "reconcile_notation",
        _tool_reconcile_notation,
        "Compare explicit notation convention records and report conflicts or unresolved aliases.",
        "notation_reconciliation_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "generate_math_tests",
        _tool_generate_math_tests,
        "Generate diagnostic pytest snippets or plan-only tests from a math obligation.",
        "math_test_generation_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "math_review_packet",
        _tool_math_review_packet,
        "Build a compact human-review packet from math debugging evidence.",
        "math_review_packet",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "math_change_impact",
        _tool_math_change_impact,
        "Trace likely downstream impact of a changed math artifact without claiming exhaustive coverage.",
        "math_change_impact_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "literature_local_audit",
        _tool_literature_local_audit,
        "Compare supplied theorem assumptions to local assumptions without fetching papers.",
        "literature_local_audit_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "derive_from",
        _tool_high_level_derive_from,
        "Answer a scoped high-level derivability question with explicit evidence boundaries.",
        "high_level_workflow_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "prove_or_counterexample",
        _tool_high_level_prove_or_counterexample,
        "Answer a scoped high-level proof/counterexample question with explicit evidence boundaries.",
        "high_level_workflow_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "assumptions_for",
        _tool_high_level_assumptions_for,
        "Find route-required assumptions for a scoped target without claiming global minimality.",
        "high_level_workflow_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "audit_and_propose_assumptions",
        _tool_high_level_audit_and_propose_assumptions,
        "Audit targets or labels and propose concrete assumption repairs without claiming proof closure.",
        "audit_assumption_report_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "audit_and_propose_derivations",
        _tool_high_level_audit_and_propose_derivations,
        "Audit targets or labels and propose concrete derivation repairs without applying edits or claiming proof closure.",
        "derivation_audit_report_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "debug_derivation",
        _tool_high_level_debug_derivation,
        "Localize a scoped derivation gap while preserving non-claim boundaries.",
        "high_level_workflow_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "audit_math_to_code",
        _tool_high_level_audit_math_to_code,
        "Run a structural math-to-code audit without treating structural evidence as proof.",
        "high_level_workflow_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "prepare_review_packet",
        _tool_high_level_prepare_review_packet,
        "Prepare a high-level human-review packet; diagnostic only, not a certificate.",
        "high_level_workflow_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "propose_fix",
        _tool_high_level_propose_fix,
        "Propose diagnostic repair steps from existing evidence; not an applied edit, proof, or certificate.",
        "high_level_workflow_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec(
        "audit_and_propose_fix",
        _tool_high_level_audit_and_propose_fix,
        "Audit explicit or discovered document labels, propose conservative repair steps, and optionally write a Markdown report with coverage.",
        "high_level_workflow_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec("audit_implementation_label", _tool_audit_implementation_label, "Audit a labeled document block against a code file path.", "implementation_audit_result", "workflow"),
    MCPToolSpec(
        "compare_label_code",
        _tool_compare_label_code,
        "Deprecated alias for audit_implementation_label; code must be a file path.",
        "label_consistency_result",
        "workflow",
        stability="deprecated",
        deprecated=True,
        replacement="audit_implementation_label",
    ),
    MCPToolSpec("derive_label_step", _tool_derive_label_step, "Check a derivation step against labeled document context.", "label_derivation_result", "workflow", certifying_capable=True),
    MCPToolSpec(
        "derive_or_refute",
        _tool_derive_or_refute,
        "Try a bounded derivation or refutation for a target equality.",
        "derive_or_refute_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "prove_or_refute",
        _tool_prove_or_refute,
        "Try a bounded proof or refutation for a target equality.",
        "prove_or_refute_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "localize_proof_gap",
        _tool_localize_proof_gap,
        "Find the first unsupported step in a bounded derivation chain.",
        "proof_gap_result",
        "workflow",
        certifying_capable=True,
        stability="experimental",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec("implementation_brief", _tool_implementation_brief, "Build a document-grounded implementation brief for a code file path.", "implementation_brief", "workflow"),
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
    MCPToolSpec("audit_kalman_recursion", _tool_audit_kalman_recursion, "Audit AST-level Kalman recursion structure in Python code text or a code file path.", "kalman_recursion_audit", "workflow"),
    MCPToolSpec("typed_obligation_label", _tool_typed_obligation_label, "Build typed/dimensional diagnostics for a labeled math obligation.", "typed_obligation_label_diagnostic", "workflow"),
    MCPToolSpec("audit_temporal_contract", _tool_audit_temporal_contract, "Audit explicit current/next temporal bindings between a labeled DSGE-style document context and a code file path.", "temporal_contract_audit", "workflow", stability="experimental"),
    MCPToolSpec("run_benchmarks", _tool_run_benchmarks, "Run seeded consistency benchmarks.", "benchmark_results", "operational"),
    MCPToolSpec("benchmark_gate", _tool_benchmark_gate, "Return CI-friendly benchmark gate results.", "benchmark_gate", "operational"),
    MCPToolSpec("workbench_benchmark_quality", _tool_workbench_benchmark_quality, "Return seeded workbench benchmark quality thresholds.", "workbench_benchmark_quality_report", "operational", stability="experimental"),
    MCPToolSpec("high_level_workflow_quality", _tool_high_level_workflow_quality, "Return seeded high-level workflow benchmark quality thresholds.", "high_level_workflow_quality_report", "operational", stability="experimental"),
    MCPToolSpec("tool_matrix", _tool_tool_matrix, "Return the current MathDevMCP tool matrix.", "tool_matrix", "informational", server_name="get_tool_matrix"),
    MCPToolSpec(
        "external_tool_first_plan",
        _tool_external_tool_first_plan,
        "Plan the external tools that must be considered before in-house mathematical search.",
        "external_tool_first_plan_result",
        "workflow",
        stability="experimental",
    ),
    MCPToolSpec("status_taxonomy", _tool_status_taxonomy, "Return the current MathDevMCP status and substatus taxonomy.", "status_taxonomy", "informational"),
    MCPToolSpec("doctor", _tool_doctor, "Report external backend capabilities and environment diagnostics.", "doctor_report", "operational"),
    MCPToolSpec("release_corpus_manifest", _tool_release_corpus_manifest, "Return the release corpus manifest.", "release_corpus_manifest", "operational"),
    MCPToolSpec("validate_release_corpus", _tool_validate_release_corpus, "Validate release corpus privacy and gate metadata.", "release_corpus_validation_report", "operational"),
    MCPToolSpec("governance_policy", _tool_governance_policy, "Return security and governance policy.", "governance_policy", "informational"),
    MCPToolSpec("release_readiness", _tool_release_readiness, "Return an auditable release-readiness report.", "release_readiness_report", "operational"),
    MCPToolSpec("release_profile_analysis", _tool_release_profile_analysis, "Analyze every release profile and remaining profile gaps.", "release_profile_analysis", "operational"),
    MCPToolSpec("lean_readiness", _tool_lean_readiness, "Report direct Lean, Lake, and LeanDojo readiness separately.", "lean_readiness", "operational"),
    MCPToolSpec("plan_math_document_rigor_audit", _tool_plan_math_document_rigor_audit, "Plan a focused mathematical rigor audit for one LaTeX file.", "math_document_rigor_audit_plan", "workflow", stability="experimental"),
    MCPToolSpec("audit_math_document_rigor", _tool_audit_math_document_rigor, "Audit one LaTeX file and write a rigor gap/proposal report.", "math_document_rigor_audit", "workflow", stability="experimental", optional_capability="symbolic_backend"),
    MCPToolSpec("audit_document_derivation_tree", _tool_audit_document_derivation_tree, "Audit LaTeX document targets with semantic work packets and derivation trees.", "document_derivation_tree_audit", "workflow", stability="experimental", optional_capability="symbolic_backend"),
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
    except Exception as exc:
        # MCP clients need a stable public envelope. Raw tracebacks and local
        # paths belong in logs/debug sessions, not in default tool responses.
        return error_result(
            "tool_execution_error",
            f"MathDevMCP tool failed during execution: {name}",
            diagnostics=_tool_failure_diagnostics(exc, arguments),
        )
