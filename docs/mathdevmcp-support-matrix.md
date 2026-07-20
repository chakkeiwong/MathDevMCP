# MathDevMCP Support Matrix

This matrix defines the supported install and release evidence profiles for
the internal release candidate and the public industrial release gate.

Use `PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root
"$PWD"` for cross-profile release review. Use `release-readiness --profile X`
when investigating one specific profile.

| Profile or mode | Purpose | Install or setup | Validation command | Release status |
| --- | --- | --- | --- | --- |
| `base` | Local document search, parser policy, benchmark gate, governance, and release-corpus checks. | `python -m pip install -e ".[dev]"` | `PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base` | Supported for internal release candidate use. |
| MCP stable | Default agent-facing stdio server exposing the 23 stable tools. | `python -m pip install -e ".[dev,mcp]"` | `PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py tests/test_mcp_stdio_smoke.py` | Supported department surface after registry/docs/server checks pass. |
| MCP all | Explicit opt-in surface exposing stable, experimental, and deprecated tools. | Set `MATHDEVMCP_MCP_PROFILE=all` before launching `mathdevmcp-mcp`. | Run the same surface and stdio tests with the profile set. | Supervised use only; experimental/deprecated tools are not stable support commitments. |
| symbolic | SymPy-backed bounded proof-obligation diagnostics. | `python -m pip install -e ".[dev,symbolic]"` | `PYTHONPATH=src pytest -q tests/test_symbolic_backend.py tests/test_proof_obligations.py` | Optional supported backend. |
| `backend` | Isolated LeanDojo backend evidence. | `scripts/setup_backend_env.sh` with `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`, or select an existing validated env with `MATHDEVMCP_BACKEND_CONDA_ENV`. | `scripts/backend_env_doctor.sh "$PWD"` and `scripts/validate_backend_install.sh "$PWD"`. | Supported strict internal profile when Pandoc, Lean, Sage, and isolated LeanDojo validate. LaTeXML and SymPy are optional backend-validator caveats. |
| `lean-search` | Optional Lean declaration and premise retrieval integrations. | `python -m pip install -e ".[dev,lean-search]"` for LeanExplore, or rerun `scripts/setup_backend_env.sh` to install the supported backend pin. LeanSearch-v2 client/runtime belongs in the isolated backend or a separate service/GPU environment. | `PYTHONPATH=src python -m mathdevmcp.cli doctor` and inspect `integrations.lean_explore`, `integrations.leansearchv2`, and `integrations.jixia`. | Version-controlled integration lane; not required by base/public profiles until a workflow explicitly selects it. |
| `tree-derivation` | Internal external-tool-first derivation search lane with tree evidence, bounded controller, and branch-derived reports. | Base package; optional `[symbolic]`, backend, Lean-search, and proof-state profiles only when selected by a workflow. | `PYTHONPATH=src pytest -q tests/test_tree_derivation_lane_integration.py tests/test_derivation_branch_controller.py tests/test_derivation_tree_report.py tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py`. | Internal agent-workflow lane. It is not public release evidence, not complete MCTS, and not a whole-document proof. |
| `document-derivation-tree` | Agent-facing document audit lane with semantic packets, agent-guided hypothesis branches, tree/backend evidence, and strict proposal compilation. | Base package; optional `[symbolic]` and backend profiles improve evidence when selected. | `PYTHONPATH=src pytest -q tests/test_document_derivation_tree.py` and inspect `tool_grounded_proposal_compiler_result`. | Experimental workflow lane. Use `search_mode=agent_guided` and `grounding_policy=strict`; blocked paths are gap reports, not repairs. |
| `pantograph` | Optional Lean proof-state interaction adapter. | Install `pantograph==0.3.15` in a Python 3.11 backend env with matching Lean/lake. | `PYTHONPATH=src python -m mathdevmcp.cli doctor` and inspect `integrations.pantograph`; smoke with `from pantograph import Server`. Direct Lean remains the certification boundary. | Experimental integration lane, not a core dependency. |
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

## Integration Version Control

Optional external tools are treated as part of the MathDevMCP package contract
only through explicit, versioned integration profiles. The authoritative
manifest lives in `src/mathdevmcp/integration_versions.py`; `doctor` reports
the supported version, installed active-Python version, installed backend-env
version when a backend is selected, and a resolved availability status.

Current supported pins:

- `sympy==1.14.0`
- `mcp==1.27.0`
- `lean-dojo==4.20.0` with `leanprover/lean4:v4.20.0`
- `lean-explore==1.2.1`
- `pantograph==0.3.15`
- LeanSearch-v2 source/service commit `94f4888cbaf9`
- jixia source commit `755fde27a9cf` with `leanprover/lean4:v4.29.0`

Do not silently depend on whatever version happens to be installed. A workflow
that uses one of these tools should either require a matching `doctor`
integration status or record the mismatch/unavailable state as diagnostic
evidence.

LeanExplore is currently installed in the isolated `mathdevmcp-backends`
environment by `scripts/setup_backend_env.sh`. It may bring a newer transitive
`mcp` package into that backend env than the core `[mcp]` profile uses. This is
acceptable only because backend-env MCP is not the MathDevMCP public MCP server
runtime; `doctor.integrations.mcp` records both active-Python and backend-env
versions so the distinction stays visible.

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
