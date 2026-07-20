#!/usr/bin/env python3
"""Inventory deterministic LaTeX/PDF surface issues without judging scholarship."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


EQUATION_ENVIRONMENTS = (
    "equation",
    "equation*",
    "align",
    "align*",
    "aligned",
    "gather",
    "gather*",
    "multline",
    "multline*",
)
HEADING_PATTERN = re.compile(
    r"\\(?P<level>part|chapter|section|subsection|subsubsection)\*?\{(?P<title>[^{}]*)\}"
)
LABEL_PATTERN = re.compile(r"\\label\{([^{}]+)\}")
REF_PATTERN = re.compile(r"\\(?:eqref|ref|autoref|cref|Cref)\{([^{}]+)\}")
WORD_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report deterministic scholarly LaTeX/PDF surface diagnostics."
    )
    parser.add_argument("tex_path", type=Path, help="Canonical LaTeX source")
    parser.add_argument("--pdf", type=Path, help="Rendered PDF; defaults to TeX stem")
    parser.add_argument("--output-json", type=Path, help="Optional JSON report")
    parser.add_argument("--output-md", type=Path, help="Optional Markdown report")
    parser.add_argument(
        "--long-sentence-words",
        type=int,
        default=45,
        help="Flag prose-like sentences at or above this word count",
    )
    parser.add_argument(
        "--max-examples", type=int, default=20, help="Maximum examples per issue class"
    )
    return parser.parse_args()


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def equation_inventory(text: str) -> list[dict[str, Any]]:
    envs = "|".join(re.escape(env) for env in EQUATION_ENVIRONMENTS)
    pattern = re.compile(
        rf"\\begin\{{(?P<env>{envs})\}}(?P<body>.*?)\\end\{{(?P=env)\}}",
        re.DOTALL,
    )
    rows: list[dict[str, Any]] = []
    for match in pattern.finditer(text):
        labels = LABEL_PATTERN.findall(match.group("body"))
        rows.append(
            {
                "environment": match.group("env"),
                "start_line": line_number(text, match.start()),
                "end_line": line_number(text, match.end()),
                "labels": labels,
                "labeled": bool(labels),
            }
        )
    return rows


def latex_to_plain(text: str) -> str:
    text = re.sub(r"\\begin\{(?:equation\*?|align\*?|aligned|gather\*?|multline\*?)\}.*?"
                  r"\\end\{(?:equation\*?|align\*?|aligned|gather\*?|multline\*?)\}",
                  " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\\[[\s\S]*?\\\]", " ", text)
    text = re.sub(r"\\(?:cite\w*|ref|eqref|label|url|href)\*?(?:\[[^]]*\])?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ").replace("~", " ")
    return re.sub(r"\s+", " ", text)


def prose_candidate_text(text: str) -> str:
    """Mask non-prose blocks while preserving newlines for source locations."""

    def mask(value: re.Match[str] | str) -> str:
        source = value.group(0) if isinstance(value, re.Match) else value
        return re.sub(r"[^\n]", " ", source)

    document_start = text.find(r"\begin{document}")
    if document_start >= 0:
        text = mask(re.match(r"[\s\S]*?\\begin\{document\}", text).group(0)) + text[
            document_start + len(r"\begin{document}") :
        ]
    non_prose_environments = (
        *EQUATION_ENVIRONMENTS,
        "table",
        "table*",
        "tabular",
        "tabular*",
        "tabularx",
        "longtable",
        "figure",
        "figure*",
        "thebibliography",
    )
    for environment in non_prose_environments:
        pattern = re.compile(
            rf"\\begin\{{{re.escape(environment)}\}}.*?"
            rf"\\end\{{{re.escape(environment)}\}}",
            re.DOTALL,
        )
        text = pattern.sub(mask, text)
    text = re.sub(r"\\item(?:\[[^]]*\])?", ". ", text)
    text = re.sub(
        r"\\(?:part|chapter|section|subsection|subsubsection|paragraph)\*?\{",
        ". ",
        text,
    )
    return text


def long_sentences(text: str, threshold: int, limit: int) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    prose = prose_candidate_text(text)
    for match in re.finditer(r"[^.!?\n][^.!?]*[.!?]", prose):
        plain = latex_to_plain(match.group(0)).strip()
        count = len(WORD_PATTERN.findall(plain))
        if count >= threshold:
            examples.append(
                {
                    "line": line_number(prose, match.start()),
                    "words": count,
                    "excerpt": plain[:280],
                }
            )
    return sorted(examples, key=lambda row: row["words"], reverse=True)[:limit]


def typo_candidates(text: str, limit: int) -> dict[str, list[dict[str, Any]]]:
    plain = latex_to_plain(text)
    repeated = []
    for match in re.finditer(r"\b([A-Za-z]{2,})\s+\1\b", plain, re.IGNORECASE):
        repeated.append({"token": match.group(0), "context": plain[max(0, match.start()-60):match.end()+60]})

    patterns = {
        "space_before_punctuation": re.compile(r"\w\s+[,:;.!?]"),
        "placeholder_markers": re.compile(r"\b(?:TODO|TBD|FIXME|XXX)\b", re.IGNORECASE),
    }
    result: dict[str, list[dict[str, Any]]] = {"repeated_words": repeated[:limit]}
    for name, pattern in patterns.items():
        rows = []
        for match in pattern.finditer(text):
            rows.append(
                {
                    "line": line_number(text, match.start()),
                    "match": match.group(0),
                }
            )
        result[name] = rows[:limit]
    return result


def command_output(command: list[str]) -> str | None:
    if shutil.which(command[0]) is None:
        return None
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    return completed.stdout if completed.returncode == 0 else None


def pdf_inventory(pdf_path: Path | None) -> dict[str, Any]:
    if pdf_path is None or not pdf_path.exists():
        return {"available": False, "path": str(pdf_path) if pdf_path else None}
    result: dict[str, Any] = {"available": True, "path": str(pdf_path.resolve())}
    info = command_output(["pdfinfo", str(pdf_path)])
    if info:
        fields = {}
        for line in info.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip().lower().replace(" ", "_")] = value.strip()
        result["pdfinfo"] = fields
    text = command_output(["pdftotext", str(pdf_path), "-"])
    if text is not None:
        result["extracted_words"] = len(WORD_PATTERN.findall(text))
        result["form_feed_pages"] = text.count("\f") + (1 if text else 0)
    return result


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    tex_path = args.tex_path.resolve()
    raw = tex_path.read_text(encoding="utf-8")
    text = strip_comments(raw)
    labels = LABEL_PATTERN.findall(text)
    refs = REF_PATTERN.findall(text)
    label_counts = Counter(labels)
    headings = [
        {
            "level": match.group("level"),
            "title": latex_to_plain(match.group("title")).strip(),
            "line": line_number(text, match.start()),
        }
        for match in HEADING_PATTERN.finditer(text)
    ]
    equations = equation_inventory(text)
    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
    abstract_words = (
        len(WORD_PATTERN.findall(latex_to_plain(abstract_match.group(1))))
        if abstract_match
        else None
    )
    pdf_path = args.pdf.resolve() if args.pdf else tex_path.with_suffix(".pdf")
    return {
        "schema_version": "scholarly_surface_audit.v1",
        "disclaimer": (
            "Deterministic diagnostics only. This report does not certify readability, "
            "mathematical correctness, source fidelity, or scientific validity."
        ),
        "tex_path": str(tex_path),
        "counts": {
            "tex_lines": len(raw.splitlines()),
            "rough_tex_words": len(WORD_PATTERN.findall(latex_to_plain(text))),
            "headings": len(headings),
            "sections": sum(row["level"] == "section" for row in headings),
            "subsections": sum(row["level"] == "subsection" for row in headings),
            "equation_environments": len(equations),
            "labeled_equation_environments": sum(row["labeled"] for row in equations),
            "labels": len(labels),
            "unique_labels": len(label_counts),
            "references": len(refs),
            "figures": len(re.findall(r"\\begin\{figure\*?\}", text)),
            "includegraphics": len(re.findall(r"\\includegraphics", text)),
            "abstract_words": abstract_words,
        },
        "headings": headings,
        "equations": equations,
        "unlabeled_equations": [row for row in equations if not row["labeled"]],
        "duplicate_labels": sorted(label for label, count in label_counts.items() if count > 1),
        "missing_reference_targets": sorted(set(refs) - set(labels)),
        "unreferenced_labels": sorted(set(labels) - set(refs)),
        "long_sentence_examples": long_sentences(
            text, args.long_sentence_words, args.max_examples
        ),
        "typo_candidates": typo_candidates(text, args.max_examples),
        "pdf": pdf_inventory(pdf_path),
    }


def markdown_report(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "# Scholarly Surface Audit",
        "",
        f"Target: `{report['tex_path']}`",
        "",
        f"> {report['disclaimer']}",
        "",
        "## Counts",
        "",
        "| Diagnostic | Value |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {key.replace('_', ' ')} | {value} |" for key, value in counts.items())
    lines.extend(["", "## Structural Candidates", ""])
    lines.append(f"- Unlabeled equation environments: {len(report['unlabeled_equations'])}")
    lines.append(f"- Duplicate labels: {len(report['duplicate_labels'])}")
    lines.append(f"- Missing reference targets: {len(report['missing_reference_targets'])}")
    lines.append(f"- Labels not referenced through ref-like commands: {len(report['unreferenced_labels'])}")
    if report["unlabeled_equations"]:
        lines.extend(["", "### Unlabeled Equations", ""])
        lines.extend(
            f"- Lines {row['start_line']}--{row['end_line']}: `{row['environment']}`"
            for row in report["unlabeled_equations"]
        )
    if report["missing_reference_targets"]:
        lines.extend(["", "### Missing Reference Targets", ""])
        lines.extend(f"- `{label}`" for label in report["missing_reference_targets"])
    lines.extend(["", "## Long-Sentence Candidates", ""])
    if report["long_sentence_examples"]:
        lines.extend(
            f"- Line {row['line']} ({row['words']} words): {row['excerpt']}"
            for row in report["long_sentence_examples"]
        )
    else:
        lines.append("- None at the configured threshold.")
    lines.extend(["", "## Typo Candidates", ""])
    for category, rows in report["typo_candidates"].items():
        lines.append(f"- {category.replace('_', ' ')}: {len(rows)}")
    lines.extend(["", "## Required Human Review", ""])
    lines.extend(
        [
            "- Inspect the rendered PDF for motivation, hierarchy, pacing, clipping, and cognitive load.",
            "- Check important equations against their sources, assumptions, notation, and claimed role.",
            "- Distinguish source results, local inference, and unresolved questions.",
            "- Use task-specific cold-reader questions before declaring the repair successful.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if not args.tex_path.is_file():
        raise SystemExit(f"TeX file not found: {args.tex_path}")
    if args.long_sentence_words < 1 or args.max_examples < 1:
        raise SystemExit("Thresholds must be positive integers")
    report = build_report(args)
    json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    md_text = markdown_report(report)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json_text, encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(md_text, encoding="utf-8")
    if not args.output_json and not args.output_md:
        print(json_text, end="")
    else:
        print(md_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
