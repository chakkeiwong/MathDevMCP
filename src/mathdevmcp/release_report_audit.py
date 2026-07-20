"""Substantive, repository-local release report validation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from .contracts import attach_contract


WORKFLOW_ROLES = (
    "Find Mathematical Context",
    "Read a Labeled Neighborhood",
    "Compare Document and Code",
    "Audit a Derivation",
    "Build an Implementation Brief",
)
CASE_ROLES = (
    "Kalman State-Space Likelihood",
    "HMC Leapfrog and Hamiltonian Flow",
    "Macro Filter Multi-File Corpus",
    "DSGE Euler Equation",
    "Stochastic Volatility Likelihood",
    "SDE and PDE Numerics",
    "ML and LLM Objective Functions",
    "Bayesian ELBO and Variational Inference",
    "Computational Physics MCMC",
)
WORKFLOW_MARKERS = (
    r"\section*{When to use it}",
    r"\section*{Command}",
    r"\section*{How to read the output}",
    r"\section*{Failure mode}",
    r"\section*{Agent handoff}",
)
CASE_MARKERS = (
    r"\section*{Colleague scenario}",
    r"\section*{Fixture and command}",
    r"\section*{Output to inspect}",
    r"\section*{Interpretation}",
    r"\section*{Next action}",
    r"\section*{Boundary}",
)
REQUIRED_EVIDENCE = (
    "workflow-search.txt",
    "workflow-context.txt",
    "workflow-compare.txt",
    "workflow-audit.txt",
    "workflow-brief.txt",
    "case-kalman-compare.txt",
    "case-hmc-compare.txt",
    "case-macro-filter-compare.txt",
    "case-dsge-compare.txt",
    "case-stochastic-volatility-compare.txt",
    "case-sde-pde-compare.txt",
    "case-ml-objective-compare.txt",
    "case-elbo-compare.txt",
    "case-physics-mcmc-compare.txt",
    "private-corpus-summary.txt",
)


def audit_release_report_substance(root: str | Path) -> dict[str, Any]:
    """Validate maintained report roles, evidence, and non-claim boundaries."""

    root_path = Path(root)
    report_path = root_path / "docs" / "mathdevmcp-release-report.tex"
    pdf_path = root_path / "docs" / "mathdevmcp-release-report.pdf"
    evidence_dir = root_path / "docs" / "generated" / "release_report"
    findings: list[dict[str, Any]] = []

    def fail(kind: str, detail: str, **extra: Any) -> None:
        findings.append({"severity": "high", "kind": kind, "detail": detail, **extra})

    if not report_path.is_file():
        fail("report_source_missing", str(report_path))
        text = ""
    else:
        text = report_path.read_text(encoding="utf-8")
    if not pdf_path.is_file():
        fail("report_pdf_missing", str(pdf_path))
    if not evidence_dir.is_dir():
        fail("report_evidence_directory_missing", str(evidence_dir))

    for marker in ("TODO", "FIXME", "placeholder chapter", "to be written", "lorem ipsum"):
        if marker in text:
            fail("report_filler_marker", marker)

    chapters = _chapters(text)
    for role in WORKFLOW_ROLES:
        title, body, lines = _chapter_for_role(chapters, role)
        if title is None:
            fail("missing_chapter_role", role)
            continue
        if lines < 35:
            fail("workflow_chapter_too_thin", title, line_count=lines)
        for marker in WORKFLOW_MARKERS:
            if marker not in body:
                fail("workflow_marker_missing", title, marker=marker)
        if "\\lstinputlisting" not in body and "\\begin{lstlisting}" not in body:
            fail("workflow_evidence_block_missing", title)

    for role in CASE_ROLES:
        title, body, lines = _chapter_for_role(chapters, role)
        if title is None:
            fail("missing_chapter_role", role)
            continue
        if lines < 45:
            fail("case_chapter_too_thin", title, line_count=lines)
        for marker in CASE_MARKERS:
            if marker not in body:
                fail("case_marker_missing", title, marker=marker)
        if "\\lstinputlisting" not in body:
            fail("case_evidence_block_missing", title)
        if r"\section*{MCP conversation}" not in body:
            fail("case_conversation_missing", title)

    private_title, private_body, private_lines = _chapter_for_role(chapters, "Private Corpus Validation")
    if private_title is None:
        fail("missing_chapter_role", "Private Corpus Validation")
    else:
        if private_lines < 50:
            fail("private_corpus_chapter_too_thin", private_title, line_count=private_lines)
        for marker in CASE_MARKERS:
            if marker not in private_body:
                fail("private_corpus_marker_missing", private_title, marker=marker)
        if "\\lstinputlisting" not in private_body:
            fail("private_corpus_evidence_block_missing", private_title)
        if r"\section*{MCP conversation}" not in private_body:
            fail("case_conversation_missing", private_title)

    minimum_lines = {
        "MCP Conversations That Sell The Tool": 85,
        "System Architecture": 45,
        "Core Data Contracts": 28,
        "Parser Policy": 25,
        "Benchmark Gate": 25,
        "Security and Privacy": 35,
        "Operations": 40,
        "Maintainer Guide": 35,
        "Limitations and Accepted Boundaries": 30,
        "Backend Environment Operating Model": 28,
        "Code Architecture for Maintainers": 28,
        "Release Evidence Maintenance": 20,
        "Risk Register": 30,
    }
    for role, minimum in minimum_lines.items():
        title, _body, lines = _chapter_for_role(chapters, role)
        if title is None:
            fail("missing_chapter_role", role)
        elif lines < minimum:
            fail("chapter_too_thin", title, line_count=lines, minimum=minimum)

    conversation_title, conversation_body, _ = _chapter_for_role(chapters, "MCP Conversations That Sell The Tool")
    if conversation_title is not None:
        for marker in (
            r"\section{The Conversation Pattern}",
            r"\section{A Realistic Review Transcript}",
            r"\section{Prompt Patterns That Trigger Tools}",
            r"\section{When MCP Tools Trigger Instead of LLM-Only Reasoning}",
            r"\subsection*{Cases That Look Like Tool Triggers But Usually Are Not}",
            r"\subsection*{How A Colleague Can Verify That The Tool Actually Ran}",
            r"\section{Example Prompts and Expected Tool Calls}",
            "LLM-only",
            "Tool: search_latex",
            "Tool: audit_implementation_label",
            "Tool: audit_derivation_v2_label",
            "validate_release_corpus",
            "benchmark_gate",
        ):
            if marker not in conversation_body:
                fail("conversation_marker_missing", conversation_title, marker=marker)

    for title, chapter in chapters.items():
        if not chapter[2] and chapter[1] < 18:
            fail("non_appendix_chapter_too_thin", title, line_count=chapter[1])

    evidence_files = sorted(evidence_dir.glob("*.txt")) if evidence_dir.is_dir() else []
    if not evidence_files:
        fail("release_evidence_missing", str(evidence_dir))
    for name in REQUIRED_EVIDENCE:
        path = evidence_dir / name
        if not path.is_file():
            fail("required_evidence_missing", name)
        elif "Command:" not in path.read_text(encoding="utf-8"):
            fail("evidence_command_missing", name)
    for path in evidence_files:
        snippet = path.read_text(encoding="utf-8")
        for marker in ("/tmp/mathdevmcp", "/home/chakwong/python/MathDevMCP", "manifest.json"):
            if marker in snippet:
                fail("generated_evidence_path_leak", path.name, marker=marker)

    status = "consistent" if not findings else "mismatch"
    return attach_contract(
        {
            "status": status,
            "reason": (
                "Release report substance audit passed."
                if status == "consistent"
                else "Release report substance audit failed."
            ),
            "chapter_count": len(chapters),
            "evidence_file_count": len(evidence_files),
            "findings": findings,
        },
        "release_report_substance_audit",
    )


def _chapters(text: str) -> dict[str, tuple[str, int, bool]]:
    pattern = re.compile(r"^\\chapter\{([^}]*)\}", re.MULTILINE)
    appendix_match = re.search(r"^\\part\*\{Appendices\}", text, re.MULTILINE)
    appendix_start = appendix_match.start() if appendix_match else len(text) + 1
    matches = list(pattern.finditer(text))
    chapters: dict[str, tuple[str, int, bool]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        chapters[match.group(1)] = (body, len(body.splitlines()), match.start() > appendix_start)
    return chapters


def _chapter_for_role(
    chapters: dict[str, tuple[str, int, bool]], role: str
) -> tuple[str | None, str, int]:
    for title, (body, lines, _is_appendix) in chapters.items():
        if title == role or re.fullmatch(rf"Workflow \d+: {re.escape(role)}", title):
            return title, body, lines
    return None, "", 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the substantive MathDevMCP release report")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)
    report = audit_release_report_substance(args.root)
    if report["status"] == "consistent":
        print(report["reason"])
        print(f"Chapters audited: {report['chapter_count']}")
        print(f"Evidence snippets audited: {report['evidence_file_count']}")
        return 0
    print(report["reason"])
    for finding in report["findings"]:
        marker = f" ({finding['marker']})" if finding.get("marker") else ""
        print(f"- {finding['kind']}: {finding['detail']}{marker}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
