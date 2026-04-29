#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/generate_release_report_evidence.sh OUTPUT_DIR

Generate short, redacted evidence snippets for the MathDevMCP release report.
Set MATHDEVMCP_PRIVATE_CORPUS_MANIFEST to include private-corpus evidence.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

OUT="${1:-}"
if [[ -z "$OUT" ]]; then
  usage >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT="$(python -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$OUT")"

mkdir -p "$OUT"
export PYTHONPATH="$ROOT/src"
export MATHDEVMCP_RELEASE_REPORT_ROOT="$ROOT"
export MATHDEVMCP_RELEASE_REPORT_OUT="$OUT"

python - <<'PY'
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from mathdevmcp.benchmarks import benchmark_gate_report
from mathdevmcp.doctor import doctor_report
from mathdevmcp.parser_policy import decide_parser_policy
from mathdevmcp.release_corpus import validate_release_corpus_manifest
from mathdevmcp.release_policy import release_readiness_report

root = Path(os.environ["MATHDEVMCP_RELEASE_REPORT_ROOT"]).resolve()
out = Path(os.environ["MATHDEVMCP_RELEASE_REPORT_OUT"]).resolve()
fixtures = root / "benchmarks" / "fixtures"
private_manifest = os.environ.get("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", "").strip()


def _write(name: str, text: str) -> None:
    cleaned = text.replace(str(root), "<repo>")
    if private_manifest:
        cleaned = cleaned.replace(private_manifest, "<redacted-private-manifest>")
    out.joinpath(name).write_text(cleaned.rstrip() + "\n", encoding="utf-8")


def _write_json_excerpt(name: str, payload: dict, *, max_lines: int = 240) -> None:
    text = json.dumps(payload, indent=2)
    lines = text.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["... truncated for release report appendix ..."]
    _write(name, "\n".join(lines))


def _run_json(args: list[str], *, env: dict[str, str] | None = None) -> dict:
    completed = subprocess.run(args, cwd=root, check=False, capture_output=True, text=True, timeout=60, env=env)
    if completed.returncode not in {0, 1}:
        return {"status": "command_failed", "returncode": completed.returncode, "stderr": completed.stderr.strip()}
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status": "non_json", "returncode": completed.returncode, "stdout": completed.stdout.strip()}


doctor = doctor_report()
capabilities = doctor["capabilities"]
_write(
    "doctor-summary.txt",
    "\n".join(
        [
            "Command: PYTHONPATH=src python -m mathdevmcp.cli doctor",
            f"Overall ok: {doctor['ok']}",
            f"Python: {doctor['python']['version']} at {doctor['python']['executable']}",
            f"LaTeXML: {capabilities['latexml']['status']} ({capabilities['latexml'].get('version')})",
            f"Pandoc: {capabilities['pandoc']['status']} ({capabilities['pandoc'].get('version')})",
            f"Lean: {capabilities['lean']['status']} ({capabilities['lean'].get('version')})",
            f"Sage: {capabilities['sage']['status']} ({capabilities['sage'].get('version')})",
            f"LeanDojo in active env: {capabilities['lean_dojo']['status']} ({capabilities['lean_dojo']['detail']})",
            f"SymPy: {capabilities['sympy']['status']} ({capabilities['sympy'].get('version')})",
            f"Conflicts: {len(doctor.get('conflicts', []))}",
        ]
    ),
)

gate = benchmark_gate_report(root)
summary = gate["summary"]
_write(
    "benchmark-gate-summary.txt",
    "\n".join(
        [
            "Command: PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root \"$PWD\"",
            f"Passed: {gate['passed']}",
            f"Cases: {gate['passed_count']}/{gate['total']}",
            f"Expected abstentions: {summary['expected_abstentions']}",
            "Categories:",
            *[
                f"  {name}: {item['passed']}/{item['total']} passed, expected abstentions {item['expected_abstentions']}"
                for name, item in summary["by_category"].items()
            ],
        ]
    ),
)
_write_json_excerpt("benchmark-gate-json-excerpt.txt", gate, max_lines=260)

parser = decide_parser_policy(str(fixtures), backends=["current"])
parser_report = parser["benchmark_report"]["results"][0]
_write(
    "parser-policy-summary.txt",
    "\n".join(
        [
            "Command: PYTHONPATH=src python -m mathdevmcp.cli parser-benchmark --root \"$PWD/benchmarks/fixtures\" --backend current",
            f"Policy status: {parser['status']}",
            f"Selected backend: {parser['selected_backend']}",
            f"Labels found: {parser_report['labels_found']}",
            f"Environments found: {parser_report['environments_found']}",
            f"Align-like blocks found: {parser_report['align_like_found']}",
            f"Provenance quality: {parser_report['provenance_quality']}",
            f"Blocking findings: {len(parser.get('blocking_findings', []))}",
        ]
    ),
)
_write_json_excerpt("parser-policy-json-excerpt.txt", parser, max_lines=220)

release_corpus = validate_release_corpus_manifest(fixtures)
manifest = release_corpus["manifest"]
_write(
    "release-corpus-summary.txt",
    "\n".join(
        [
            "Command: PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root \"$PWD/benchmarks/fixtures\"",
            f"Status: {release_corpus['status']}",
            f"Findings: {len(release_corpus['findings'])}",
            f"Entries: {len(manifest['entries'])}",
            f"Private manifest status: {manifest['private_manifest']['status']}",
            f"Private paths redacted: {manifest['private_paths_redacted']}",
        ]
    ),
)
_write_json_excerpt("release-corpus-json-excerpt.txt", release_corpus, max_lines=220)

full = release_readiness_report(root, profile="full")
_write(
    "release-readiness-full-summary.txt",
    "\n".join(
        [
            "Command: PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root \"$PWD\" --profile full",
            f"Status: {full['status']}",
            f"Reason: {full['reason']}",
            f"Blockers: {[item['kind'] for item in full['blockers']]}",
            f"Caveats: {[item['kind'] for item in full['caveats']]}",
            f"Git commit: {full['git_commit']}",
            f"Dirty worktree: {full['dirty_worktree']}",
        ]
    ),
)
_write_json_excerpt("release-readiness-full-json-excerpt.txt", full, max_lines=280)

if private_manifest:
    env = os.environ.copy()
    env["MATHDEVMCP_PRIVATE_CORPUS_MANIFEST"] = private_manifest
    private = _run_json([str(root / "scripts" / "validate_private_corpus.sh"), str(root)], env=env)
    _write(
        "private-corpus-summary.txt",
        "\n".join(
            [
                "Command: MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=<redacted-private-manifest> scripts/validate_private_corpus.sh \"$PWD\"",
                f"Status: {private.get('status')}",
                f"Reason: {private.get('reason')}",
                f"Private paths redacted: {private.get('private_paths_redacted')}",
                f"Findings: {len(private.get('findings', []))}",
                f"Parser reports: {[(item.get('entry_id'), item.get('status')) for item in private.get('parser_reports', [])]}",
            ]
        ),
    )
    _write_json_excerpt("private-corpus-json-excerpt.txt", private, max_lines=260)
else:
    _write(
        "private-corpus-summary.txt",
        "\n".join(
            [
                "Command: MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=<redacted-private-manifest> scripts/validate_private_corpus.sh \"$PWD\"",
                "Status: skipped",
                "Reason: MATHDEVMCP_PRIVATE_CORPUS_MANIFEST was not set during evidence generation.",
                "Private paths redacted: true",
            ]
        ),
    )
    _write("private-corpus-json-excerpt.txt", '{"status": "skipped", "private_paths_redacted": true}')

workflow_commands = {
    "workflow-search.txt": [
        "python",
        "-m",
        "mathdevmcp.cli",
        "search-latex",
        "Kalman likelihood",
        "--root",
        str(fixtures),
        "--limit",
        "3",
    ],
    "workflow-context.txt": [
        "python",
        "-m",
        "mathdevmcp.cli",
        "extract-latex-neighborhood",
        "eq:dept-state-space-likelihood",
        "--root",
        str(fixtures),
    ],
    "workflow-compare.txt": [
        "python",
        "-m",
        "mathdevmcp.cli",
        "compare-label-code",
        "eq:dept-state-space-likelihood",
        str(fixtures / "doc_department_state_space_missing_solve.py"),
        "--root",
        str(fixtures),
        "--required-terms",
        "logdet,solve",
        "--paragraph-context",
    ],
    "workflow-audit.txt": [
        "python",
        "-m",
        "mathdevmcp.cli",
        "audit-derivation-v2-label",
        "eq:dept-state-space-likelihood",
        "--root",
        str(fixtures),
        "--summary-only",
    ],
    "workflow-brief.txt": [
        "python",
        "-m",
        "mathdevmcp.cli",
        "implementation-brief",
        "state space likelihood",
        str(fixtures / "doc_department_state_space_missing_solve.py"),
        "--root",
        str(fixtures),
        "--required-terms",
        "logdet,solve",
        "--limit",
        "2",
    ],
}

for filename, command in workflow_commands.items():
    payload = _run_json(command, env={**os.environ, "PYTHONPATH": str(root / "src")})
    text = json.dumps(payload, indent=2)
    if len(text.splitlines()) > 80:
        text = "\n".join(text.splitlines()[:80] + ["... truncated for report ..."])
    _write(filename, "Command: " + " ".join(command).replace(str(root), "<repo>") + "\n" + text)

_write(
    "evidence-index.txt",
    "\n".join(
        [
            "Generated release report evidence snippets:",
            "doctor-summary.txt",
            "benchmark-gate-summary.txt",
            "parser-policy-summary.txt",
            "release-corpus-summary.txt",
            "release-readiness-full-summary.txt",
            "private-corpus-summary.txt",
            "workflow-search.txt",
            "workflow-context.txt",
            "workflow-compare.txt",
            "workflow-audit.txt",
            "workflow-brief.txt",
            "benchmark-gate-json-excerpt.txt",
            "parser-policy-json-excerpt.txt",
            "release-corpus-json-excerpt.txt",
            "release-readiness-full-json-excerpt.txt",
            "private-corpus-json-excerpt.txt",
        ]
    ),
)
PY

echo "Release report evidence written to $OUT"
