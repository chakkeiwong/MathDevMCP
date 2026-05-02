# MathDevMCP Deployment Guide

MathDevMCP is deployed as a small base package with optional external workers.
The base package must import without LaTeXML, Pandoc, Lean, Sage, or LeanDojo.
The public industrial release gate is separate from internal deployment
profiles and is checked with `public-release-check`.
The MCP server runtime is also optional; install `mathdevmcp[mcp]` or
`.[dev,mcp]` before running `mathdevmcp-mcp`.

## Local Smoke

Run:

```bash
scripts/release_smoke.sh /path/to/MathDevMCP
```

The smoke path runs:

- `doctor`,
- current-parser benchmark,
- benchmark gate,
- release corpus validation,
- governance policy,
- release-readiness report.

## Optional Workers

Use separate environments or workers for:

- parser tools: LaTeXML and Pandoc,
- symbolic/numeric tools: SymPy and Sage,
- Lean direct checking,
- LeanDojo proof search.

LeanDojo should remain isolated from document/PDF/ML environments when dependency conflicts appear.

## Isolated Backend Environment

Recommended local layout:

```bash
scripts/setup_backend_env.sh
```

This creates or updates a `mathdevmcp-backends` conda environment for Python backend packages such as `lean-dojo`, while installing Lean through user-local `elan`. Keep this separate from GPU/document/PDF environments because LeanDojo currently brings a large dependency stack including Ray and Pydantic.
The script installs the requested Lean toolchain but does not change the user's global `elan default`; MathDevMCP subprocesses use the `MATHDEVMCP_LEAN_TOOLCHAIN` pin below.

To use the backend environment from the normal project shell:

```bash
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean"
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli doctor
```

`doctor` will check Python modules such as `lean_dojo` inside the backend env and executable tools through explicit paths or PATH. Set `MATHDEVMCP_LEAN_TOOLCHAIN` to pin the `elan` proxy for MathDevMCP subprocesses without changing the user's global Lean default. If Lean toolchain download fails, `doctor` reports Lean as unavailable even when the wrapper exists; treat that as a toolchain caveat, not as a proof backend.

LaTeXML is still a system package on this machine rather than a Python package. If conda cannot resolve it, install it through the OS package manager or provide an executable path with:

```bash
export MATHDEVMCP_LATEXML_PATH=/path/to/latexml
```

Validate the optional LaTeXML backend with:

```bash
scripts/validate_latexml_backend.sh /path/to/MathDevMCP
```

This command exits successfully with an `unavailable` caveat by default. Set `MATHDEVMCP_REQUIRE_LATEXML=1` only for deployments that intentionally require LaTeXML.
Use `scripts/setup_latexml_backend.sh` for OS-package installation guidance.

Run backend commands through the isolated conda environment with:

```bash
scripts/run_backend_command.sh python -m mathdevmcp.cli doctor
```

For a clean checkout smoke after committing release changes:

```bash
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean
```

This copies `HEAD` with `git archive`, installs the base package in a disposable conda env, and runs doctor, focused parser tests, and the benchmark gate. Set `MATHDEVMCP_INSTALL_BACKENDS=1` only when backend installation should be tested explicitly.

Use release evidence collection for review artifacts:

```bash
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence --profile base
```

Generated evidence should be stored outside git by default. The committed scripts and schemas are the reproducible release mechanism; routine evidence directories should be treated as review artifacts.

For release-report snippets that are safe to commit, use:

```bash
scripts/generate_release_report_evidence.sh docs/generated/release_report
```

Set `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` first when the report should include
private-corpus evidence. The generated report snippets redact private paths.

## Release Caveats

External commands must have timeouts and structured `inconclusive` failures. Private corpora should not be committed; only manifest stubs and expected labels belong in git.

Private corpus evaluation can be supplied through `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST`. Default reports redact private paths and governance validation rejects private roots inside the checkout.
Validate private corpora with:

```bash
scripts/validate_private_corpus.sh /path/to/MathDevMCP
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli release-readiness \
  --root /path/to/MathDevMCP --profile private-corpus
```

For a local profile matrix:

```bash
scripts/release_matrix.sh /path/to/MathDevMCP
```

For public industrial release surface validation:

```bash
scripts/quality_gate.sh
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli public-release-check \
  --root /path/to/MathDevMCP
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli release-readiness \
  --root /path/to/MathDevMCP --profile public
```

This public gate validates CI, packaging metadata, MCP surface consistency,
support matrix coverage, documentation boundary language, quality checks, and
generated-evidence redaction. It does not require private corpus material.

For no-intervention sanitized validation outside git:

```bash
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json
scripts/validate_private_corpus.sh /path/to/MathDevMCP
```
