"""CLI registration for parser benchmarking and PDF extraction commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parser_benchmark import compare_parser_backends
from .pdf_cli import register_pdf_command
from .applied_math_audit import (
    APPLIED_MATH_PAGE_COLLECTIONS,
    audit_applied_math_document,
    page_applied_math_audit_records,
)


def _run_parser_benchmark(args: argparse.Namespace) -> int:
    result = compare_parser_backends(Path(args.root), backends=args.backend or None)
    print(json.dumps(result, indent=2))
    return 0


def _run_applied_math_audit(args: argparse.Namespace) -> int:
    result = audit_applied_math_document(
        args.source,
        code_paths=args.code or None,
        data_paths=args.data or None,
        mode=args.mode,
        specialist_policy=args.specialist_policy,
        response_mode=args.response_mode,
        artifact_root=args.artifact_root,
    )
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


def _run_page_applied_math_audit(args: argparse.Namespace) -> int:
    result = page_applied_math_audit_records(
        args.artifact_path,
        args.sha256,
        args.collection,
        offset=args.offset,
        limit=args.limit,
    )
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


def register_parser_commands(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("parser-benchmark", help="Compare LaTeX parser backends on a corpus")
    parser.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    parser.add_argument(
        "--backend",
        action="append",
        choices=["current", "latexml", "pandoc"],
        help="Parser backend to run; can be repeated",
    )
    parser.set_defaults(func=_run_parser_benchmark)
    register_pdf_command(subparsers)
    applied = subparsers.add_parser(
        "audit-applied-math-document",
        help="Run the general applied-mathematics document audit orchestrator",
    )
    applied.add_argument("source", nargs="+", help="Source document paths (PDF, TeX, or related source files)")
    applied.add_argument("--code", action="append", default=[], help="Optional code/model path; can be repeated")
    applied.add_argument("--data", action="append", default=[], help="Optional data/artifact path; can be repeated")
    applied.add_argument("--mode", choices=["screen", "deep", "reproduce"], default="screen")
    applied.add_argument("--specialist-policy", choices=["auto", "none", "explicit"], default="auto")
    applied.add_argument("--response-mode", choices=["compact", "detailed"], default="compact")
    applied.add_argument("--artifact-root", default=".mathdevmcp/applied_math_audits")
    applied.set_defaults(func=_run_applied_math_audit)
    page = subparsers.add_parser(
        "page-applied-math-audit-records",
        help="Page an allowlisted collection from an exact applied-math audit artifact",
    )
    page.add_argument("artifact_path")
    page.add_argument("sha256")
    page.add_argument("collection", choices=sorted(APPLIED_MATH_PAGE_COLLECTIONS))
    page.add_argument("--offset", type=int, default=0)
    page.add_argument("--limit", type=int, default=50)
    page.set_defaults(func=_run_page_applied_math_audit)
