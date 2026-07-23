"""CLI wiring for the optional ResearchAssistant PDF provider bridge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .artifact_storage import write_bytes_safe
from .research_assistant_pdf import extract_pdf_with_research_assistant


def run_extract_pdf(args: argparse.Namespace) -> int:
    result = extract_pdf_with_research_assistant(
        args.pdf,
        research_assistant_root=args.research_assistant_root,
        response_mode=args.response_mode,
        timeout_seconds=args.timeout_seconds,
        max_provider_output_bytes=args.max_provider_output_bytes,
    )
    payload = (json.dumps(result, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    if args.output_json:
        write_bytes_safe(Path(args.output_json), payload)
    else:
        sys.stdout.buffer.write(payload)
    return 0


def register_pdf_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "extract-pdf-with-research-assistant",
        help="Extract a local PDF through a source-bound ResearchAssistant provider bridge",
    )
    parser.add_argument("pdf")
    parser.add_argument(
        "--research-assistant-root",
        default=str(Path.home() / "python" / "ResearchAssistant"),
    )
    parser.add_argument("--response-mode", choices=("compact", "detailed"), default="compact")
    parser.add_argument("--timeout-seconds", type=float, default=1_000)
    parser.add_argument("--max-provider-output-bytes", type=int, default=64 * 1024 * 1024)
    parser.add_argument("--output-json")
    parser.set_defaults(func=run_extract_pdf)
