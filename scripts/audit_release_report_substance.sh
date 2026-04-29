#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REPORT="$ROOT/docs/mathdevmcp-release-report.tex"
PDF="$ROOT/docs/mathdevmcp-release-report.pdf"
EVIDENCE_DIR="$ROOT/docs/generated/release_report"

python - "$REPORT" "$PDF" "$EVIDENCE_DIR" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path


report = Path(sys.argv[1])
pdf = Path(sys.argv[2])
evidence_dir = Path(sys.argv[3])

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


if not report.exists():
    fail(f"missing report source: {report}")
    text = ""
else:
    text = report.read_text(encoding="utf-8")

if not pdf.exists():
    fail(f"missing built PDF: {pdf}")

if not evidence_dir.exists():
    fail(f"missing generated evidence directory: {evidence_dir}")

banned = [
    "TODO",
    "FIXME",
    "placeholder chapter",
    "to be written",
    "lorem ipsum",
]
for marker in banned:
    if marker in text:
        fail(f"banned filler marker appears in report source: {marker}")

chapter_pattern = re.compile(r"^\\chapter\{([^}]*)\}", re.MULTILINE)
part_appendix_pattern = re.compile(r"^\\part\*\{Appendices\}", re.MULTILINE)
appendix_match = part_appendix_pattern.search(text)
appendix_start = appendix_match.start() if appendix_match else len(text) + 1
matches = list(chapter_pattern.finditer(text))
chapters: dict[str, tuple[str, int, bool]] = {}
for index, match in enumerate(matches):
    start = match.end()
    end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
    title = match.group(1)
    body = text[start:end]
    line_count = len(body.splitlines())
    is_appendix = match.start() > appendix_start
    chapters[title] = (body, line_count, is_appendix)


def require_chapter(title: str) -> tuple[str, int, bool]:
    if title not in chapters:
        fail(f"missing chapter: {title}")
        return "", 0, False
    return chapters[title]


workflow_titles = [
    "Workflow 1: Find Mathematical Context",
    "Workflow 2: Read a Labeled Neighborhood",
    "Workflow 3: Compare Document and Code",
    "Workflow 4: Audit a Derivation",
    "Workflow 5: Build an Implementation Brief",
]
workflow_markers = [
    r"\section*{When to use it}",
    r"\section*{Command}",
    r"\section*{How to read the output}",
    r"\section*{Failure mode}",
    r"\section*{Agent handoff}",
]
for title in workflow_titles:
    body, lines, _ = require_chapter(title)
    if lines < 35:
        fail(f"workflow chapter too thin ({lines} lines): {title}")
    for marker in workflow_markers:
        if marker not in body:
            fail(f"workflow chapter missing marker {marker}: {title}")
    if "\\lstinputlisting" not in body and "\\begin{lstlisting}" not in body:
        fail(f"workflow chapter lacks generated output or command block: {title}")

case_titles = [
    "Kalman State-Space Likelihood",
    "HMC Leapfrog and Hamiltonian Flow",
    "Macro Filter Multi-File Corpus",
    "DSGE Euler Equation",
    "Stochastic Volatility Likelihood",
    "SDE and PDE Numerics",
    "ML and LLM Objective Functions",
    "Bayesian ELBO and Variational Inference",
    "Computational Physics MCMC",
]
case_markers = [
    r"\section*{Colleague scenario}",
    r"\section*{Fixture and command}",
    r"\section*{Output to inspect}",
    r"\section*{Interpretation}",
    r"\section*{Next action}",
    r"\section*{Boundary}",
]
for title in case_titles:
    body, lines, _ = require_chapter(title)
    if lines < 45:
        fail(f"case-study chapter too thin ({lines} lines): {title}")
    for marker in case_markers:
        if marker not in body:
            fail(f"case-study chapter missing marker {marker}: {title}")
    if "\\lstinputlisting" not in body:
        fail(f"case-study chapter lacks generated evidence: {title}")

private_body, private_lines, _ = require_chapter("Private Corpus Validation")
if private_lines < 50:
    fail(f"private corpus chapter too thin ({private_lines} lines)")
for marker in case_markers:
    if marker not in private_body:
        fail(f"private corpus chapter missing marker {marker}")
if "\\lstinputlisting" not in private_body:
    fail("private corpus chapter lacks generated evidence")

minimum_lines = {
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
for title, minimum in minimum_lines.items():
    _, lines, _ = require_chapter(title)
    if lines < minimum:
        fail(f"chapter below substance threshold ({lines} < {minimum}): {title}")

for title, (_body, lines, is_appendix) in chapters.items():
    if not is_appendix and lines < 18:
        fail(f"thin non-appendix chapter ({lines} lines): {title}")

evidence_files = sorted(evidence_dir.glob("*.txt")) if evidence_dir.exists() else []
if not evidence_files:
    fail("no generated evidence snippets found")

required_evidence = [
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
]
for name in required_evidence:
    path = evidence_dir / name
    if not path.exists():
        fail(f"missing required evidence snippet: {name}")
        continue
    snippet = path.read_text(encoding="utf-8")
    if "Command:" not in snippet:
        fail(f"evidence snippet does not name its command: {name}")

leak_patterns = [
    "/tmp/mathdevmcp",
    "/home/chakwong/python/MathDevMCP",
    "manifest.json",
]
for path in evidence_files:
    snippet = path.read_text(encoding="utf-8")
    for pattern in leak_patterns:
        if pattern in snippet:
            fail(f"generated evidence leaks banned path marker {pattern}: {path.name}")

if errors:
    print("Release report substance audit failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Release report substance audit passed.")
print(f"Chapters audited: {len(chapters)}")
print(f"Evidence snippets audited: {len(evidence_files)}")
PY
