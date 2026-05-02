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
    cleaned = cleaned.replace(str(Path.home()), "<home>")
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


def _command_text(command: list[str]) -> str:
    return " ".join(command).replace(str(root), "<repo>")


def _short_text(value: object, *, max_chars: int = 280) -> str:
    text = str(value).replace("\n", " ").strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def _case_search(filename: str, *, query: str) -> None:
    command = [
        "python",
        "-m",
        "mathdevmcp.cli",
        "search-latex",
        query,
        "--root",
        str(fixtures),
        "--limit",
        "3",
    ]
    payload = _run_json(command, env={**os.environ, "PYTHONPATH": str(root / "src")})
    rows = payload if isinstance(payload, list) else []
    lines = ["Command: " + _command_text(command), f"Query: {query}", f"Results returned: {len(rows)}"]
    for index, item in enumerate(rows[:3], start=1):
        lines.extend(
            [
                f"Result {index}: label={item.get('label')} file={item.get('file')} lines={item.get('line_start')}-{item.get('line_end')} score={item.get('score')}",
                "  " + _short_text(item.get("text", "")),
            ]
        )
    _write(filename, "\n".join(lines))


def _case_compare(filename: str, *, label: str, code_file: str, required_terms: str) -> None:
    code_path = fixtures / code_file
    command = [
        "python",
        "-m",
        "mathdevmcp.cli",
        "compare-label-code",
        label,
        str(code_path),
        "--root",
        str(fixtures),
        "--required-terms",
        required_terms,
        "--paragraph-context",
    ]
    payload = _run_json(command, env={**os.environ, "PYTHONPATH": str(root / "src")})
    findings = payload.get("findings", []) if isinstance(payload, dict) else []
    matched = [item.get("term") for item in findings if item.get("kind") == "matched_term"]
    missing = payload.get("missing_in_code", []) if isinstance(payload, dict) else []
    context = payload.get("doc_context", {}) if isinstance(payload, dict) else {}
    paragraphs = context.get("paragraphs", []) if isinstance(context, dict) else []
    lines = [
        "Command: " + _command_text(command),
        f"Label: {label}",
        f"Code file: {code_file}",
        f"Status: {payload.get('status') if isinstance(payload, dict) else 'unknown'}",
        f"Reason: {payload.get('reason') if isinstance(payload, dict) else 'unknown'}",
        f"Required terms: {required_terms}",
        f"Matched terms: {matched}",
        f"Missing terms: {missing}",
        f"Provenance: {context.get('file')}:{context.get('line_start')}-{context.get('line_end')}",
    ]
    if paragraphs:
        lines.append("Document excerpt: " + _short_text(paragraphs[0].get("text", ""), max_chars=420))
    _write(filename, "\n".join(lines))


def _case_brief(filename: str, *, query: str, code_file: str, required_terms: str) -> None:
    code_path = fixtures / code_file
    command = [
        "python",
        "-m",
        "mathdevmcp.cli",
        "implementation-brief",
        query,
        str(code_path),
        "--root",
        str(fixtures),
        "--required-terms",
        required_terms,
        "--limit",
        "2",
    ]
    payload = _run_json(command, env={**os.environ, "PYTHONPATH": str(root / "src")})
    consistency = payload.get("checks", {}).get("consistency", {}) if isinstance(payload, dict) else {}
    context = payload.get("doc_context", {}) if isinstance(payload, dict) else {}
    paragraphs = context.get("paragraphs", []) if isinstance(context, dict) else []
    lines = [
        "Command: " + _command_text(command),
        f"Query: {query}",
        f"Selected label: {payload.get('selected_label') if isinstance(payload, dict) else 'unknown'}",
        f"Brief status: {payload.get('status') if isinstance(payload, dict) else 'unknown'}",
        f"Brief reason: {payload.get('reason') if isinstance(payload, dict) else 'unknown'}",
        f"Consistency status: {consistency.get('status')}",
        f"Consistency reason: {consistency.get('reason')}",
        f"Missing terms: {consistency.get('missing_in_code', [])}",
        f"Provenance: {context.get('file')}:{context.get('line_start')}-{context.get('line_end')}",
    ]
    if paragraphs:
        lines.append("Context excerpt: " + _short_text(paragraphs[0].get("text", ""), max_chars=420))
    _write(filename, "\n".join(lines))


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
_write_json_excerpt("benchmark-gate-json-excerpt.txt", gate, max_lines=120)

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
_write_json_excerpt("parser-policy-json-excerpt.txt", parser, max_lines=100)

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
_write_json_excerpt("release-corpus-json-excerpt.txt", release_corpus, max_lines=100)

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
_write_json_excerpt("release-readiness-full-json-excerpt.txt", full, max_lines=120)

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
    _write_json_excerpt("private-corpus-json-excerpt.txt", private, max_lines=100)
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

case_specs = [
    {
        "prefix": "case-kalman",
        "query": "state space likelihood",
        "label": "eq:dept-state-space-likelihood",
        "code": "doc_department_state_space_missing_solve.py",
        "terms": "logdet,solve",
    },
    {
        "prefix": "case-hmc",
        "query": "Hamiltonian leapfrog",
        "label": "eq:dept-hmc-leapfrog",
        "code": "doc_department_hmc_jax.py",
        "terms": "grad,hamiltonian",
    },
    {
        "prefix": "case-macro-filter",
        "query": "macro filter likelihood",
        "label": "eq:macro-filter-likelihood",
        "code": "doc_macro_filter_missing_gain.py",
        "terms": "logdet,solve,K_t",
    },
    {
        "prefix": "case-dsge",
        "query": "Euler equation stochastic discount factor",
        "label": "eq:dept-euler-equation",
        "code": "doc_sanitized_dsge_macro_finance.py",
        "terms": "expectation,euler_residual",
    },
    {
        "prefix": "case-stochastic-volatility",
        "query": "stochastic volatility likelihood",
        "label": "eq:dept-sv-likelihood",
        "code": "doc_sanitized_stochastic_volatility.py",
        "terms": "innovation,posterior_or_likelihood",
    },
    {
        "prefix": "case-sde-pde",
        "query": "Euler Maruyama stability",
        "label": "eq:dept-euler-maruyama",
        "code": "doc_sanitized_sde_pde_numerics.py",
        "terms": "drift,diffusion,stability_condition",
    },
    {
        "prefix": "case-ml-objective",
        "query": "ML objective gradient",
        "label": "eq:dept-ml-gradient",
        "code": "doc_sanitized_ml_llm_objective.py",
        "terms": "gradient,loss",
    },
    {
        "prefix": "case-elbo",
        "query": "ELBO reparameterization gradient",
        "label": "eq:dept-elbo",
        "code": "doc_sanitized_bayesian_elbo_vi.py",
        "terms": "expectation,elbo",
    },
    {
        "prefix": "case-physics-mcmc",
        "query": "acceptance ratio Hamiltonian",
        "label": "eq:dept-acceptance-ratio",
        "code": "doc_sanitized_computational_physics_mcmc.py",
        "terms": "hamiltonian,gradient",
    },
]

for spec in case_specs:
    _case_search(f"{spec['prefix']}-search.txt", query=spec["query"])
    _case_compare(
        f"{spec['prefix']}-compare.txt",
        label=spec["label"],
        code_file=spec["code"],
        required_terms=spec["terms"],
    )
    _case_brief(
        f"{spec['prefix']}-brief.txt",
        query=spec["query"],
        code_file=spec["code"],
        required_terms=spec["terms"],
    )

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
            "case-kalman-search.txt",
            "case-kalman-compare.txt",
            "case-kalman-brief.txt",
            "case-hmc-search.txt",
            "case-hmc-compare.txt",
            "case-hmc-brief.txt",
            "case-macro-filter-search.txt",
            "case-macro-filter-compare.txt",
            "case-macro-filter-brief.txt",
            "case-dsge-search.txt",
            "case-dsge-compare.txt",
            "case-dsge-brief.txt",
            "case-stochastic-volatility-search.txt",
            "case-stochastic-volatility-compare.txt",
            "case-stochastic-volatility-brief.txt",
            "case-sde-pde-search.txt",
            "case-sde-pde-compare.txt",
            "case-sde-pde-brief.txt",
            "case-ml-objective-search.txt",
            "case-ml-objective-compare.txt",
            "case-ml-objective-brief.txt",
            "case-elbo-search.txt",
            "case-elbo-compare.txt",
            "case-elbo-brief.txt",
            "case-physics-mcmc-search.txt",
            "case-physics-mcmc-compare.txt",
            "case-physics-mcmc-brief.txt",
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
