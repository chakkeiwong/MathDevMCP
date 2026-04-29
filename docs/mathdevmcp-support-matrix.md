# MathDevMCP Support Matrix

This matrix defines the supported install and release evidence profiles for
the internal release candidate and the public industrial release gate.

| Profile or mode | Purpose | Install or setup | Validation command | Release status |
| --- | --- | --- | --- | --- |
| `base` | Local document search, parser policy, benchmark gate, governance, and release-corpus checks. | `python -m pip install -e ".[dev]"` | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base` | Supported for internal release candidate use. |
| MCP | Agent-facing stdio server and in-process facade. | `python -m pip install -e ".[dev,mcp]"` | `PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py` | Supported public surface after registry/docs/server checks pass. |
| symbolic | SymPy-backed bounded proof-obligation diagnostics. | `python -m pip install -e ".[dev,symbolic]"` | `PYTHONPATH=src pytest -q tests/test_symbolic_backend.py tests/test_proof_obligations.py` | Optional supported backend. |
| `backend` | Isolated LeanDojo backend evidence. | `scripts/setup_backend_env.sh` with `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`. | `scripts/backend_env_doctor.sh "$PWD"` and `scripts/validate_backend_install.sh "$PWD"`. | Supported strict internal profile when the backend env validates. |
| `latexml` | Strict LaTeXML parser validation. | Install the OS package `latexml` or set `MATHDEVMCP_LATEXML_PATH`. | `MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"`. | Supported strict internal profile when the executable validates. |
| `private-corpus` | External private or sanitized department corpus validation. | Set `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` to an external manifest outside git. | `scripts/validate_private_corpus.sh "$PWD"`. | Supported strict internal profile; private material must never be committed. |
| `full` | All internal optional evidence: backend, LaTeXML, and private corpus. | Combine `backend`, `latexml`, and `private-corpus` setup. | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full`. | Internal full-profile release evidence, not a public release claim by itself. |
| `public` | Public industrial release product-surface gate. | Base package plus CI, MCP docs, support matrix, packaging metadata, quality gate, and generated-evidence redaction. | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public`. | Required before public industrial release claims. |

## Backend Isolation Policy

LeanDojo remains outside the base Python environment. Use the
`mathdevmcp-backends` conda environment so Ray, Pydantic, and LeanDojo
dependencies do not destabilize document, PDF, ML, or MCP workflows.

## Public Release Boundary

The `base`, `backend`, `latexml`, `private-corpus`, and `full` profiles are
internal/deployment evidence profiles. The `public` profile adds public
industrial release checks for packaging, CI, MCP surface consistency, support
matrix coverage, documentation alignment, quality gates, and private path
redaction. A public release should not be claimed unless the `public` profile
is executable and has no blockers.

