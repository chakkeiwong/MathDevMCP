# MathDevMCP Maintainer Guide

This guide is for developers who need to maintain MathDevMCP without knowing
the whole codebase.

## Repository Map

- `src/mathdevmcp/latex_index.py`: LaTeX parsing, labels, context, and search.
- `src/mathdevmcp/consistency.py`: document/code term comparison.
- `src/mathdevmcp/derivation.py`: scoped derivation-step checks.
- `src/mathdevmcp/proof_audit.py`: first-generation proof-audit workflow.
- `src/mathdevmcp/proof_audit_v2.py`: release-facing typed proof-audit
  workflow.
- `src/mathdevmcp/math_ir.py`: typed/dimensional obligation diagnostics.
- `src/mathdevmcp/ast_operation_graph.py`: Python AST operation extraction.
- `src/mathdevmcp/parser_benchmark.py`: parser backend measurement.
- `src/mathdevmcp/parser_policy.py`: parser routing decision for proof audit.
- `src/mathdevmcp/release_corpus.py`: public/private corpus manifest and
  privacy validation.
- `src/mathdevmcp/release_policy.py`: release profiles, blockers, caveats, and
  evidence command list.
- `src/mathdevmcp/public_release.py`: public industrial release product-surface
  checks for CI, packaging, MCP docs, support matrix, and redaction evidence.
- `src/mathdevmcp/doctor.py`: runtime capability diagnostics.
- `src/mathdevmcp/backend_env.py`: isolated backend environment selection.
- `src/mathdevmcp/mcp_facade.py`: in-process MCP tool facade.
- `src/mathdevmcp/mcp_server.py`: FastMCP server wrapper.
- `src/mathdevmcp/cli.py`: command-line entry point.
- `scripts/`: repeatable release, backend, and evidence workflows.
- `docs/generated/release_report/`: committed, redacted release-report
  snippets generated from commands.

## Maintenance Rules

- Preserve JSON `metadata.contract` names unless a compatibility path is added.
- Keep CLI and MCP wrappers thin; put behavior in library functions.
- Keep optional tools optional unless a strict release profile requires them.
- Keep LeanDojo in the backend environment.
- Keep base/public release checks separate from strict backend checks. Missing
  backend evidence remains visible in doctor output, but it should only affect
  the release recommendation for profiles that require backend evidence.
- Treat Lean toolchain download and availability failures as diagnostic
  `inconclusive` evidence. Only direct Lean rejection of supplied source is a
  `mismatch`.
- Never commit private documents or populated private manifests.
- Run focused tests after each behavior change, then the full suite.
- Treat `full` as strict internal/deployment evidence and `public` as the
  public industrial release product-surface gate.

## Adding a Benchmark Case

1. Add or update public/sanitized fixtures under `benchmarks/fixtures`.
2. Add a benchmark case in the appropriate case builder.
3. Add or update tests that assert the new expected total or category summary.
4. Run `PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"`.
5. Update the release report evidence if the new case affects release claims.

## Adding a Private Corpus Entry

1. Keep the source documents outside git.
2. Add the entry to an external manifest, not to the repository.
3. Include expected labels, operations, parser backends, and either expected
   abstentions or false-confidence seeds.
4. Run `scripts/validate_private_corpus.sh "$PWD"`.
5. Confirm output contains `<redacted-private-path>`.

## Adding a Backend

1. Add a capability check in `doctor.py`.
2. Add backend environment handling in `backend_env.py` if isolation is needed.
3. Wrap subprocess calls with explicit timeouts.
4. Return structured unavailable, timeout, diagnostic, mismatch, and certifying
   states.
5. Add tests for missing backend behavior.
6. Only then add release-profile requirements.

## Updating the Release Report

Regenerate evidence:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json \
scripts/generate_release_report_evidence.sh docs/generated/release_report
```

## Public Industrial Release Checks

Before any public industrial release claim, run the cross-profile analysis
first, then the public gate:

```bash
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
scripts/quality_gate.sh
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

The profile analysis answers which release claims are currently justified and
which strict profile hypotheses remain. The public gate checks that CI,
packaging metadata, MCP surface documentation, support matrix coverage,
documentation boundary language, quality checks, and generated-evidence
redaction all agree. It does not certify arbitrary mathematics; it certifies
that the public product surface is coherent enough for release review.

For strict internal/full release evidence, configure all optional evidence in
one shell. An existing validated backend env may be selected with
`MATHDEVMCP_BACKEND_CONDA_ENV`; `scripts/setup_backend_env.sh` remains the
bootstrap path when no such env exists. `scripts/validate_backend_install.sh`
requires Pandoc, Lean, Sage, and isolated LeanDojo evidence, and reports SymPy
as an optional symbolic-backend caveat.

```bash
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_REQUIRE_LATEXML=1
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
scripts/validate_private_corpus.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

Scan for path leaks:

```bash
rg -n "/secure|/tmp/mathdevmcp|manifest.json|/home/" docs/generated/release_report
```

Build the report:

```bash
cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
```

## Common Failure Modes

- `private_corpus_manifest_required`: set
  `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` to an external manifest.
- `backend_lean_dojo_unavailable`: run `scripts/setup_backend_env.sh` and set
  `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`, or select another
  validated backend env. Missing SymPy is an optional symbolic-backend caveat,
  not the LeanDojo backend blocker.
- `latexml_required_backend_unavailable`: install LaTeXML or set
  `MATHDEVMCP_LATEXML_PATH`.
- Dirty worktree caveat: commit or intentionally record the dirty evidence.
- Parser policy blocked: check expected labels and provenance in
  `parser-benchmark`.
