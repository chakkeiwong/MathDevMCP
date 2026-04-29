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
from .consistency import compare_files, compare_label_to_code
from .derivation import derive_step_for_label, derive_step_from_files
from .doctor import doctor_report
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index, write_index
from .performance import index_performance_smoke
from .parser_benchmark import compare_parser_backends
from .proof_obligations import check_proof_obligation
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .governance import governance_policy, validate_governance
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_policy import RELEASE_PROFILES, release_readiness_report
from .typed_workflows import typed_obligation_for_label
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief


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


def _cmd_audit_kalman_recursion(args: argparse.Namespace) -> int:
    required_operations = [item.strip() for item in args.required_operation if item.strip()]
    result = audit_kalman_recursion(args.code, required_operations=required_operations or None)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_typed_obligation_label(args: argparse.Namespace) -> int:
    result = typed_obligation_for_label(args.root, args.label, backend=args.backend, context_text=args.context_text or "")
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

    p_compare = sub.add_parser("compare-doc-code", help="Compare document text against code text")
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
