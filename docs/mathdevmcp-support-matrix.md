# MathDevMCP Support Matrix

This matrix defines the supported install and release evidence profiles for
the internal release candidate and the public industrial release gate.

Use `PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root
"$PWD"` for cross-profile release review. Use `release-readiness --profile X`
when investigating one specific profile.

| Profile or mode | Purpose | Install or setup | Validation command | Release status |
| --- | --- | --- | --- | --- |
| `base` | Local document search, parser policy, benchmark gate, governance, and release-corpus checks. | `python -m pip install -e ".[dev]"` | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base` | Supported for internal release candidate use. |
| MCP | Agent-facing stdio server and in-process facade. | `python -m pip install -e ".[dev,mcp]"` | `PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py` | Supported public surface after registry/docs/server checks pass. |
| symbolic | SymPy-backed bounded proof-obligation diagnostics. | `python -m pip install -e ".[dev,symbolic]"` | `PYTHONPATH=src pytest -q tests/test_symbolic_backend.py tests/test_proof_obligations.py` | Optional supported backend. |
| `backend` | Isolated LeanDojo backend evidence. | `scripts/setup_backend_env.sh` with `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`, or select an existing validated env with `MATHDEVMCP_BACKEND_CONDA_ENV`. | `scripts/backend_env_doctor.sh "$PWD"` and `scripts/validate_backend_install.sh "$PWD"`. | Supported strict internal profile when Pandoc, Lean, Sage, and isolated LeanDojo validate. LaTeXML and SymPy are optional backend-validator caveats. |
| `latexml` | Strict LaTeXML parser validation. | Install the OS package `latexml` or set `MATHDEVMCP_LATEXML_PATH`. | `MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"`. | Supported strict internal profile when the executable validates. |
| `private-corpus` | External private or sanitized department corpus validation. | Set `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` to an external manifest outside git. | `scripts/validate_private_corpus.sh "$PWD"`. | Supported strict internal profile; private material must never be committed. |
| `full` | All internal optional evidence: backend, LaTeXML, and private corpus. | Combine `backend`, `latexml`, and `private-corpus` setup in the same shell. | `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_REQUIRE_LATEXML=1 MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full`. | Internal full-profile release evidence, not a public release claim by itself. |
| `public` | Public industrial release product-surface gate. | Base package plus CI, MCP docs, support matrix, packaging metadata, quality gate, and generated-evidence redaction. | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public`. | Required before public industrial release claims. |

## Backend Isolation Policy

LeanDojo remains outside the base Python environment. Use the
`mathdevmcp-backends` conda environment so Ray, Pydantic, and LeanDojo
dependencies do not destabilize document, PDF, ML, or MCP workflows.
Release operators may select a different already-provisioned environment with
`MATHDEVMCP_BACKEND_CONDA_ENV`; the validator requires the release-critical
backend evidence and reports symbolic extras such as SymPy as optional caveats.

The base and public profiles must stay usable when the optional backend stack is
absent. Missing private corpora, LeanDojo, active-environment Lean caches, or
backend dependency compatibility is recorded in raw doctor and corpus evidence,
but it should not downgrade a public/base recommendation unless the selected
profile requires that capability. The base profile may still report optional
parser-worker caveats such as missing LaTeXML; the public profile relies on the
public surface gate instead. MCP-facing installs use the optional `[mcp]` extra;
base library imports remain lightweight.

Direct Lean source rejection is a mismatch. Lean executable absence, toolchain download failures, timeouts, and placeholder proofs are diagnostic or inconclusive evidence, not mathematical refutations.

## Public Release Boundary

The `base`, `backend`, `latexml`, `private-corpus`, and `full` profiles are
internal/deployment evidence profiles. The `public` profile adds public
industrial release checks for packaging, CI, MCP surface consistency, support
matrix coverage, documentation alignment, quality gates, and private path
redaction. A public release should not be claimed unless the `public` profile
is executable and has no blockers.

## Profile-Scoped Caveats

Release-readiness reports keep the complete `doctor_summary`, so unavailable
tools and dependency conflicts remain visible to reviewers. The selected
profile controls whether that evidence affects the release recommendation.
Optional strict-profile evidence does not downgrade a public/base recommendation:

- `base` and `public` do not require private corpus material, LeanDojo, or a
  working Lean toolchain cache.
- `backend` and `full` require isolated backend evidence and report
  backend-relevant Lean/dependency caveats.
- `latexml` and `full` require strict LaTeXML validation.
- `private-corpus` and `full` require an external private or sanitized manifest.
