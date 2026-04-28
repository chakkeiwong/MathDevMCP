# MathDevMCP Deployment Guide

MathDevMCP should be deployed as a small base package with optional external workers. The base package must import without LaTeXML, Pandoc, Lean, Sage, or LeanDojo.

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

For a clean checkout smoke after committing release changes:

```bash
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean
```

This copies `HEAD` with `git archive`, installs the base package in a disposable conda env, and runs doctor, focused parser tests, and the benchmark gate. Set `MATHDEVMCP_INSTALL_BACKENDS=1` only when backend installation should be tested explicitly.

## Release Caveats

External commands must have timeouts and structured `inconclusive` failures. Private corpora should not be committed; only manifest stubs and expected labels belong in git.
