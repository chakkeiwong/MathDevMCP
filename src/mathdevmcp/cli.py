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
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index, write_index
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
    )
    print(json.dumps(result, indent=2))
    return 0



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

    p_brief = sub.add_parser("implementation-brief", help="Build a document-grounded implementation brief")
    p_brief.add_argument("query", help="Document search query")
    p_brief.add_argument("code", help="Code file path")
    p_brief.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_brief.add_argument("--label", default="", help="Specific LaTeX label to use")
    p_brief.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_brief.add_argument("--lhs", default="", help="Optional derivation left-hand side")
    p_brief.add_argument("--rhs", default="", help="Optional derivation right-hand side")
    p_brief.add_argument("--limit", type=int, default=3, help="Maximum search results")
    p_brief.set_defaults(func=_cmd_implementation_brief)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
