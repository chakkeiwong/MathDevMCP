"""Command-line entry point for MathDevMCP release and workflow tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmarks import (
    benchmark_gate_report,
    build_benchmark_report,
    run_label_consistency_benchmark,
    run_seeded_mismatch_benchmark,
    write_benchmark_report,
    write_seeded_mismatch_benchmark,
)
from .code_search import search_files
from .claim_support import build_claim_support_packet
from .consistency import compare_files, compare_label_to_code
from .derivation import derive_step_for_label, derive_step_from_files
from .doctor import doctor_report
from .domain_templates import generate_obligations_from_template, list_domain_templates, suggest_domain_templates
from ._install_rules import install_rules
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index, write_index
from .lean_readiness import lean_readiness
from .mcp_alias_audit import audit_deprecated_alias_usage
from .performance import index_performance_smoke
from .parser_benchmark import compare_parser_backends
from .proof_obligations import check_proof_obligation
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .proof_packet import build_proof_packet_label
from .negative_evidence import build_negative_evidence_packet
from .public_release import public_release_check
from .governance import governance_policy, validate_governance
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_hypotheses import release_hypothesis_check
from .release_profile_analysis import release_profile_analysis
from .release_policy import RELEASE_PROFILES, release_readiness_report
from .status_taxonomy import status_taxonomy
from .temporal_contracts import audit_temporal_contract
from .typed_workflows import typed_obligation_for_label
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief


def _load_json_argument_or_file(value: str):
    try:
        path = Path(value)
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    return json.loads(value)


def _cmd_index(args: argparse.Namespace) -> int:
    index = write_index(Path(args.root), Path(args.output))
    print(json.dumps({"output": args.output, "n_blocks": index["n_blocks"], "n_labels": index["n_labels"]}, indent=2))
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    results = search_index(index, args.query, limit=args.limit)
    print(json.dumps(results, indent=2))
    return 0



def _cmd_extract_context(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    result = extract_context_for_label(index, args.label, before=args.before, after=args.after)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_extract_paragraph_context(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    result = extract_paragraph_context_for_label(index, args.label, before=args.before, after=args.after)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_search_code_docs(args: argparse.Namespace) -> int:
    results = search_files(Path(args.root), args.query, limit=args.limit)
    print(json.dumps(results, indent=2))
    return 0



def _cmd_compare(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = compare_files(args.doc, args.code, required_terms=required_terms or None)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_compare_label(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = compare_label_to_code(
        args.root,
        args.label,
        args.code,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        required_terms=required_terms or None,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_tool_matrix(args: argparse.Namespace) -> int:
    print(json.dumps(tool_matrix(), indent=2))
    return 0


def _cmd_status_taxonomy(args: argparse.Namespace) -> int:
    _ = args
    print(json.dumps(status_taxonomy(), indent=2))
    return 0


def _cmd_domain_templates(args: argparse.Namespace) -> int:
    print(json.dumps(list_domain_templates(), indent=2))
    return 0


def _cmd_suggest_domain_templates(args: argparse.Namespace) -> int:
    result = suggest_domain_templates(
        label=args.label or "",
        section_path=[item.strip() for item in args.section_path if item.strip()],
        equation_text=args.equation_text or "",
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_generate_template_obligations(args: argparse.Namespace) -> int:
    result = generate_obligations_from_template(args.template_id, label=args.label)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_claim_support(args: argparse.Namespace) -> int:
    citations = [{"id": item} for item in args.citation]
    result = build_claim_support_packet(
        args.claim,
        claim_id=args.claim_id or None,
        citations=citations,
        linked_labels=[item for item in args.label if item],
        linked_packets=[item for item in args.packet if item],
        empirical=args.empirical,
        assumption=args.assumption,
        proposed=args.proposed,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_doctor(args: argparse.Namespace) -> int:
    print(json.dumps(doctor_report(), indent=2))
    return 0



def _cmd_parser_benchmark(args: argparse.Namespace) -> int:
    result = compare_parser_backends(Path(args.root), backends=args.backend or None)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_derive_step(args: argparse.Namespace) -> int:
    result = derive_step_from_files(args.doc, args.lhs, args.rhs)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_derive_label(args: argparse.Namespace) -> int:
    result = derive_step_for_label(
        args.root,
        args.label,
        args.lhs,
        args.rhs,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_benchmark_plan(args: argparse.Namespace) -> int:
    plan = write_seeded_mismatch_benchmark(Path(args.root))
    print(json.dumps(plan, indent=2))
    return 0



def _cmd_run_benchmark(args: argparse.Namespace) -> int:
    results = run_seeded_mismatch_benchmark(Path(args.root))
    passed = sum(1 for result in results if result["passed"])
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    return 0 if passed == len(results) else 1



def _cmd_run_label_benchmark(args: argparse.Namespace) -> int:
    results = run_label_consistency_benchmark(Path(args.root))
    passed = sum(1 for result in results if result["passed"])
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    return 0 if passed == len(results) else 1



def _cmd_run_benchmarks(args: argparse.Namespace) -> int:
    report = build_benchmark_report(Path(args.root))
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1



def _cmd_write_benchmark_report(args: argparse.Namespace) -> int:
    result = write_benchmark_report(Path(args.root), Path(args.output))
    print(json.dumps(result, indent=2))
    report = result["report"]
    return 0 if report["passed"] == report["total"] else 1



def _cmd_benchmark_gate(args: argparse.Namespace) -> int:
    result = benchmark_gate_report(Path(args.root))
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1



def _cmd_index_performance(args: argparse.Namespace) -> int:
    queries = [query.strip() for query in args.query if query.strip()]
    cache_path = Path(args.cache) if args.cache else None
    result = index_performance_smoke(Path(args.root), queries=queries or None, repeat=args.repeat, limit=args.limit, cache_path=cache_path)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_implementation_brief(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = build_implementation_brief(
        args.root,
        args.query,
        args.code,
        label=args.label or None,
        required_terms=required_terms or None,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        limit=args.limit,
        cache_path=Path(args.cache) if args.cache else None,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_check_proof_obligation(args: argparse.Namespace) -> int:
    result = check_proof_obligation(args.lhs, args.rhs, assumptions=args.assumption or None, backend=args.backend)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_audit_derivation_label(args: argparse.Namespace) -> int:
    result = audit_derivation_for_label(
        args.root,
        args.label,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        backend=args.backend,
        cache_path=Path(args.cache) if args.cache else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_derivation_v2_label(args: argparse.Namespace) -> int:
    result = audit_derivation_v2_for_label(
        args.root,
        args.label,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        backend=args.backend,
        cache_path=Path(args.cache) if args.cache else None,
        summary_only=args.summary_only,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_proof_packet_label(args: argparse.Namespace) -> int:
    result = build_proof_packet_label(args.root, args.label, summary_only=args.summary_only)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_negative_evidence_label(args: argparse.Namespace) -> int:
    audit = audit_derivation_v2_for_label(args.root, args.label, summary_only=True)
    result = build_negative_evidence_packet(args.label, audit)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_kalman_recursion(args: argparse.Namespace) -> int:
    required_operations = [item.strip() for item in args.required_operation if item.strip()]
    result = audit_kalman_recursion(args.code, required_operations=required_operations or None)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_typed_obligation_label(args: argparse.Namespace) -> int:
    result = typed_obligation_for_label(args.root, args.label, backend=args.backend, context_text=args.context_text or "")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_temporal_contract(args: argparse.Namespace) -> int:
    bindings = _load_json_argument_or_file(args.required_bindings)
    result = audit_temporal_contract(args.root, args.label, args.code, bindings, before=args.before, after=args.after)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_release_corpus_manifest(args: argparse.Namespace) -> int:
    print(json.dumps(release_corpus_manifest(args.root, private_manifest=args.private_manifest or None), indent=2))
    return 0


def _cmd_validate_release_corpus(args: argparse.Namespace) -> int:
    result = validate_release_corpus_manifest(args.root, private_manifest=args.private_manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1


def _cmd_governance_policy(args: argparse.Namespace) -> int:
    _ = args
    print(json.dumps(governance_policy(), indent=2))
    return 0


def _cmd_validate_governance(args: argparse.Namespace) -> int:
    result = validate_governance(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1


def _cmd_release_readiness(args: argparse.Namespace) -> int:
    result = release_readiness_report(args.root, profile=args.profile)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready", "ready_with_caveats"} else 1


def _cmd_release_profile_analysis(args: argparse.Namespace) -> int:
    result = release_profile_analysis(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready", "ready_with_caveats"} else 1


def _cmd_lean_readiness(args: argparse.Namespace) -> int:
    print(json.dumps(lean_readiness(args.root or None), indent=2))
    return 0


def _cmd_public_release_check(args: argparse.Namespace) -> int:
    result = public_release_check(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_release_hypothesis_check(args: argparse.Namespace) -> int:
    result = release_hypothesis_check(
        args.root,
        public=args.public,
        strict_full=args.strict_full,
        require_canonical_backend=args.require_canonical_backend,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_install_rules(args: argparse.Namespace) -> int:
    result = install_rules(args.root, args.client, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_mcp_aliases(args: argparse.Namespace) -> int:
    result = audit_deprecated_alias_usage(args.root, include_history=args.include_history)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1



def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MathDevMCP development utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index-latex", help="Build a JSON index of LaTeX structure")
    p_index.add_argument("root", help="Root directory containing LaTeX files")
    p_index.add_argument("--output", default=".mathdevmcp/latex_index.json", help="Output JSON path")
    p_index.set_defaults(func=_cmd_index)

    p_search = sub.add_parser("search-latex", help="Search a LaTeX index or root")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_search.add_argument("--index", default="", help="Existing index JSON path")
    p_search.add_argument("--limit", type=int, default=10, help="Maximum results")
    p_search.set_defaults(func=_cmd_search)

    p_context = sub.add_parser("extract-latex-context", help="Extract context around a LaTeX label")
    p_context.add_argument("label", help="LaTeX label to inspect")
    p_context.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_context.add_argument("--index", default="", help="Existing index JSON path")
    p_context.add_argument("--before", type=int, default=2, help="Lines of context before")
    p_context.add_argument("--after", type=int, default=2, help="Lines of context after")
    p_context.set_defaults(func=_cmd_extract_context)

    p_paragraph = sub.add_parser("extract-latex-neighborhood", help="Extract paragraph neighborhood around a LaTeX label")
    p_paragraph.add_argument("label", help="LaTeX label to inspect")
    p_paragraph.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_paragraph.add_argument("--index", default="", help="Existing index JSON path")
    p_paragraph.add_argument("--before", type=int, default=1, help="Paragraphs before")
    p_paragraph.add_argument("--after", type=int, default=1, help="Paragraphs after")
    p_paragraph.set_defaults(func=_cmd_extract_paragraph_context)

    p_code = sub.add_parser("search-code-docs", help="Search code and document files together")
    p_code.add_argument("query", help="Search query")
    p_code.add_argument("--root", default=".", help="Project root")
    p_code.add_argument("--limit", type=int, default=20, help="Maximum results")
    p_code.set_defaults(func=_cmd_search_code_docs)

    p_compare = sub.add_parser("compare-doc-code", help="Compare a document file against a code file")
    p_compare.add_argument("doc", help="Document file path")
    p_compare.add_argument("code", help="Code file path")
    p_compare.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_compare.set_defaults(func=_cmd_compare)

    p_compare_label = sub.add_parser("compare-label-code", help="Compare a labeled document block against code")
    p_compare_label.add_argument("label", help="LaTeX label to inspect")
    p_compare_label.add_argument("code", help="Code file path")
    p_compare_label.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_compare_label.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_compare_label.add_argument("--before", type=int, default=0, help="Context units before")
    p_compare_label.add_argument("--after", type=int, default=0, help="Context units after")
    p_compare_label.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_compare_label.set_defaults(func=_cmd_compare_label)

    p_matrix = sub.add_parser("tool-matrix", help="Print the current tool matrix")
    p_matrix.set_defaults(func=_cmd_tool_matrix)

    p_status_taxonomy = sub.add_parser("status-taxonomy", help="Print the current status and substatus taxonomy")
    p_status_taxonomy.set_defaults(func=_cmd_status_taxonomy)

    p_domain_templates = sub.add_parser("domain-templates", help="Print governed domain template catalog")
    p_domain_templates.set_defaults(func=_cmd_domain_templates)

    p_suggest_templates = sub.add_parser("suggest-domain-templates", help="Suggest domain templates for label or equation context")
    p_suggest_templates.add_argument("--label", default="", help="Optional source label")
    p_suggest_templates.add_argument("--section-path", action="append", default=[], help="Section path element; can be repeated")
    p_suggest_templates.add_argument("--equation-text", default="", help="Localized equation text")
    p_suggest_templates.set_defaults(func=_cmd_suggest_domain_templates)

    p_template_obligations = sub.add_parser("generate-template-obligations", help="Generate diagnostic obligations from a domain template")
    p_template_obligations.add_argument("template_id", help="Template id")
    p_template_obligations.add_argument("--label", required=True, help="Source label")
    p_template_obligations.set_defaults(func=_cmd_generate_template_obligations)

    p_claim_support = sub.add_parser("claim-support", help="Build a local claim-support packet")
    p_claim_support.add_argument("claim", help="Claim text")
    p_claim_support.add_argument("--claim-id", default="", help="Stable claim id")
    p_claim_support.add_argument("--citation", action="append", default=[], help="Citation or local paper id; can be repeated")
    p_claim_support.add_argument("--label", action="append", default=[], help="Linked label; can be repeated")
    p_claim_support.add_argument("--packet", action="append", default=[], help="Linked packet id; can be repeated")
    p_claim_support.add_argument("--empirical", action="store_true", help="Classify as empirical regularity")
    p_claim_support.add_argument("--assumption", action="store_true", help="Classify as model assumption")
    p_claim_support.add_argument("--proposed", action="store_true", help="Classify as proposed extension")
    p_claim_support.set_defaults(func=_cmd_claim_support)

    p_doctor = sub.add_parser("doctor", help="Report external backend capabilities and environment diagnostics")
    p_doctor.set_defaults(func=_cmd_doctor)

    p_parser_benchmark = sub.add_parser("parser-benchmark", help="Compare LaTeX parser backends on a corpus")
    p_parser_benchmark.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_parser_benchmark.add_argument("--backend", action="append", choices=["current", "latexml", "pandoc"], help="Parser backend to run; can be repeated")
    p_parser_benchmark.set_defaults(func=_cmd_parser_benchmark)

    p_derive = sub.add_parser("derive-step", help="Evaluate whether a derivation step is justified")
    p_derive.add_argument("doc", help="Document path used for provenance")
    p_derive.add_argument("lhs", help="Left-hand side expression")
    p_derive.add_argument("rhs", help="Right-hand side expression")
    p_derive.set_defaults(func=_cmd_derive_step)

    p_derive_label = sub.add_parser("derive-label-step", help="Evaluate a derivation step against a labeled document block")
    p_derive_label.add_argument("label", help="LaTeX label to inspect")
    p_derive_label.add_argument("lhs", help="Left-hand side expression")
    p_derive_label.add_argument("rhs", help="Right-hand side expression")
    p_derive_label.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_derive_label.add_argument("--before", type=int, default=0, help="Context units before")
    p_derive_label.add_argument("--after", type=int, default=0, help="Context units after")
    p_derive_label.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_derive_label.set_defaults(func=_cmd_derive_label)

    p_bench = sub.add_parser("benchmark-plan", help="Print the seeded mismatch benchmark plan")
    p_bench.add_argument("--root", default=".", help="Project root")
    p_bench.set_defaults(func=_cmd_benchmark_plan)

    p_run_bench = sub.add_parser("run-benchmark", help="Run the seeded mismatch benchmark")
    p_run_bench.add_argument("--root", default=".", help="Project root")
    p_run_bench.set_defaults(func=_cmd_run_benchmark)

    p_run_label_bench = sub.add_parser("run-label-benchmark", help="Run the label-based consistency benchmark")
    p_run_label_bench.add_argument("--root", default=".", help="Project root")
    p_run_label_bench.set_defaults(func=_cmd_run_label_benchmark)

    p_run_benchmarks = sub.add_parser("run-benchmarks", help="Run the full structured benchmark suite")
    p_run_benchmarks.add_argument("--root", default=".", help="Project root")
    p_run_benchmarks.set_defaults(func=_cmd_run_benchmarks)

    p_write_benchmarks = sub.add_parser("write-benchmark-report", help="Write the structured benchmark report to JSON")
    p_write_benchmarks.add_argument("--root", default=".", help="Project root")
    p_write_benchmarks.add_argument("--output", default=".mathdevmcp/benchmark_report.json", help="Output JSON path")
    p_write_benchmarks.set_defaults(func=_cmd_write_benchmark_report)

    p_benchmark_gate = sub.add_parser("benchmark-gate", help="Run benchmark gate evaluation for CI")
    p_benchmark_gate.add_argument("--root", default=".", help="Project root")
    p_benchmark_gate.set_defaults(func=_cmd_benchmark_gate)

    p_index_perf = sub.add_parser("index-performance-smoke", help="Measure cold indexing and repeated LaTeX search timings")
    p_index_perf.add_argument("--root", default=".", help="Project root or LaTeX root")
    p_index_perf.add_argument("--query", action="append", default=[], help="Search query to time; can be repeated")
    p_index_perf.add_argument("--repeat", type=int, default=3, help="Repeated searches per query")
    p_index_perf.add_argument("--limit", type=int, default=5, help="Maximum search results per query")
    p_index_perf.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_index_perf.set_defaults(func=_cmd_index_performance)

    p_brief = sub.add_parser("implementation-brief", help="Build a document-grounded implementation brief")
    p_brief.add_argument("query", help="Document search query")
    p_brief.add_argument("code", help="Code file path")
    p_brief.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_brief.add_argument("--label", default="", help="Specific LaTeX label to use")
    p_brief.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_brief.add_argument("--lhs", default="", help="Optional derivation left-hand side")
    p_brief.add_argument("--rhs", default="", help="Optional derivation right-hand side")
    p_brief.add_argument("--limit", type=int, default=3, help="Maximum search results")
    p_brief.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_brief.set_defaults(func=_cmd_implementation_brief)

    p_obligation = sub.add_parser("check-proof-obligation", help="Check a bounded derivation/proof obligation")
    p_obligation.add_argument("lhs", help="Left-hand side expression")
    p_obligation.add_argument("rhs", help="Right-hand side expression")
    p_obligation.add_argument("--assumption", action="append", default=[], help="Assumption attached to the obligation; can be repeated")
    p_obligation.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_obligation.set_defaults(func=_cmd_check_proof_obligation)

    p_audit = sub.add_parser("audit-derivation-label", help="Audit derivation obligations extracted from a labeled document block")
    p_audit.add_argument("label", help="LaTeX label to audit")
    p_audit.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_audit.add_argument("--before", type=int, default=0, help="Context units before")
    p_audit.add_argument("--after", type=int, default=0, help="Context units after")
    p_audit.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_audit.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_audit.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_audit.set_defaults(func=_cmd_audit_derivation_label)

    p_audit_v2 = sub.add_parser("audit-derivation-v2-label", help="Audit a labeled derivation with typed routing and release evidence")
    p_audit_v2.add_argument("label", help="LaTeX label to audit")
    p_audit_v2.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_audit_v2.add_argument("--before", type=int, default=0, help="Context units before")
    p_audit_v2.add_argument("--after", type=int, default=0, help="Context units after")
    p_audit_v2.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_audit_v2.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="sympy", help="Backend preference")
    p_audit_v2.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_audit_v2.add_argument("--summary-only", action="store_true", help="Return compact per-obligation summaries")
    p_audit_v2.set_defaults(func=_cmd_audit_derivation_v2_label)

    p_proof_packet = sub.add_parser("proof-packet-label", help="Build a durable proof packet for a labeled document block")
    p_proof_packet.add_argument("label", help="LaTeX label to audit")
    p_proof_packet.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_proof_packet.add_argument("--summary-only", action="store_true", help="Store compact nested audit evidence")
    p_proof_packet.add_argument("--output", default="", help="Optional JSON output path")
    p_proof_packet.set_defaults(func=_cmd_proof_packet_label)

    p_negative_packet = sub.add_parser("negative-evidence-label", help="Build a negative-evidence packet for a labeled document block")
    p_negative_packet.add_argument("label", help="LaTeX label to audit")
    p_negative_packet.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_negative_packet.add_argument("--output", default="", help="Optional JSON output path")
    p_negative_packet.set_defaults(func=_cmd_negative_evidence_label)

    p_kalman_recursion = sub.add_parser("audit-kalman-recursion", help="Audit AST-level Kalman recursion structure in Python code")
    p_kalman_recursion.add_argument("code", help="Python code file path")
    p_kalman_recursion.add_argument("--required-operation", action="append", default=[], help="Required AST operation; can be repeated")
    p_kalman_recursion.set_defaults(func=_cmd_audit_kalman_recursion)

    p_typed_obligation = sub.add_parser("typed-obligation-label", help="Build typed/dimensional diagnostics for a labeled math obligation")
    p_typed_obligation.add_argument("label", help="LaTeX label to inspect")
    p_typed_obligation.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_typed_obligation.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="sympy", help="Backend preference for source proof audit")
    p_typed_obligation.add_argument("--context-text", default="", help="Optional explicit context/assumption text")
    p_typed_obligation.set_defaults(func=_cmd_typed_obligation_label)

    p_temporal = sub.add_parser("audit-temporal-contract", help="Audit explicit current/next temporal bindings between a label and code")
    p_temporal.add_argument("label", help="LaTeX label to inspect")
    p_temporal.add_argument("code", help="Code file path")
    p_temporal.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_temporal.add_argument("--required-bindings", required=True, help="JSON string or JSON file path with temporal binding specs")
    p_temporal.add_argument("--before", type=int, default=1)
    p_temporal.add_argument("--after", type=int, default=1)
    p_temporal.set_defaults(func=_cmd_audit_temporal_contract)

    p_release_corpus = sub.add_parser("release-corpus-manifest", help="Print the release corpus manifest")
    p_release_corpus.add_argument("--root", default="benchmarks/fixtures", help="Root directory for public fixture entries")
    p_release_corpus.add_argument("--private-manifest", default="", help="Optional private corpus manifest path")
    p_release_corpus.set_defaults(func=_cmd_release_corpus_manifest)

    p_validate_release_corpus = sub.add_parser("validate-release-corpus", help="Validate the release corpus manifest")
    p_validate_release_corpus.add_argument("--root", default="benchmarks/fixtures", help="Root directory for public fixture entries")
    p_validate_release_corpus.add_argument("--private-manifest", default="", help="Optional private corpus manifest path")
    p_validate_release_corpus.set_defaults(func=_cmd_validate_release_corpus)

    p_governance = sub.add_parser("governance-policy", help="Print security and governance policy")
    p_governance.set_defaults(func=_cmd_governance_policy)

    p_validate_governance = sub.add_parser("validate-governance", help="Validate security and governance release checks")
    p_validate_governance.add_argument("--root", default=".", help="Project root")
    p_validate_governance.set_defaults(func=_cmd_validate_governance)

    p_release = sub.add_parser("release-readiness", help="Build a release-readiness report")
    p_release.add_argument("--root", default=".", help="Project root")
    p_release.add_argument("--profile", choices=sorted(RELEASE_PROFILES), default="base", help="Release profile to evaluate")
    p_release.set_defaults(func=_cmd_release_readiness)

    p_profile_analysis = sub.add_parser("release-profile-analysis", help="Analyze all release profiles and remaining profile gaps")
    p_profile_analysis.add_argument("--root", default=".", help="Project root")
    p_profile_analysis.set_defaults(func=_cmd_release_profile_analysis)

    p_lean_readiness = sub.add_parser("lean-readiness", help="Report direct Lean, Lake, and LeanDojo readiness separately")
    p_lean_readiness.add_argument("--root", default=".", help="Project root or Lean project root")
    p_lean_readiness.set_defaults(func=_cmd_lean_readiness)

    p_public = sub.add_parser("public-release-check", help="Validate public release product-surface gates")
    p_public.add_argument("--root", default=".", help="Project root")
    p_public.set_defaults(func=_cmd_public_release_check)

    p_hypotheses = sub.add_parser("release-hypothesis-check", help="Validate executable release-closeout hypotheses")
    p_hypotheses.add_argument("--root", default=".", help="Project root")
    p_hypotheses.add_argument("--public", action="store_true", help="Run public/base-safe release hypothesis checks")
    p_hypotheses.add_argument("--strict-full", action="store_true", help="Require configured strict full-profile evidence")
    p_hypotheses.add_argument("--require-canonical-backend", action="store_true", help="Require MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends")
    p_hypotheses.set_defaults(func=_cmd_release_hypothesis_check)

    p_install_rules = sub.add_parser("install-rules", help="Install portable MathDevMCP workflow rules for an MCP client")
    p_install_rules.add_argument("client", choices=["cursor", "copilot", "all"], help="Client instruction target to update")
    p_install_rules.add_argument("--root", default=".", help="Project root where client instruction files live")
    p_install_rules.add_argument("--dry-run", action="store_true", help="Preview the updated instruction file content without writing")
    p_install_rules.set_defaults(func=_cmd_install_rules)

    p_aliases = sub.add_parser("audit-mcp-aliases", help="Audit active docs/scripts for deprecated MCP tool aliases")
    p_aliases.add_argument("--root", default=".", help="Project root to scan")
    p_aliases.add_argument("--include-history", action="store_true", help="Include historical plans and generated evidence directories")
    p_aliases.set_defaults(func=_cmd_audit_mcp_aliases)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
