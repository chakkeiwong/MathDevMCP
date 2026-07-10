# MathDevMCP External-Tool-First Tree Derivation Phase 00 Result

Date: 2026-07-08

## Objective

Make external-tool-first a repository policy and executable contract before
building the budgeted tree derivation search engine.

## Artifacts

- `AGENTS.md`
- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-plan-2026-07-08.md`
- `src/mathdevmcp/external_tool_policy.py`
- `src/mathdevmcp/backend_route_planner.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `src/mathdevmcp/cli.py`
- `tests/test_external_tool_policy.py`
- focused updates to route planner, MCP, server, CLI, README, and MCP README

## What Changed

Added a repo-local policy requiring derivation, proof, premise-search,
missing-assumption, document-rigor, and repair workflows to consider existing
external tools before proposing in-house search.

Added `external_tool_first_plan`, an agent-facing policy contract that records:

- considered tools;
- selected external routes;
- unavailable tools;
- formalization-required routes;
- per-tool certification boundaries;
- version/environment evidence from `doctor`/integration manifests;
- the in-house search gate and required gap justification.

Embedded the policy plan inside `plan_backend_routes` so existing derivation
route plans carry the external-tool-first ledger.

Exposed the plan through CLI/MCP:

- CLI: `external-tool-first-plan`
- MCP facade/server: `external_tool_first_plan`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed for Phase 0: external tool consideration is now policy, code contract, route-plan field, MCP/CLI surface, and test fixture. |
| Veto diagnostics | No test permits in-house search without explicit gap justification; route plans retain non-certifying boundaries; backend absence remains diagnostic. |
| Explanatory diagnostics | Full tree search is not yet implemented; `requires_formalization` is selectable as a next route, not a proof. |
| Not concluded | No broad theorem proving, no public release readiness, no complete tree search, no proof/certification from route planning. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m py_compile src/mathdevmcp/external_tool_policy.py src/mathdevmcp/backend_route_planner.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py src/mathdevmcp/cli.py` | Passed. |
| `git diff --check -- ...touched files...` | Passed. |
| `python3 -m pytest tests/test_external_tool_policy.py tests/test_backend_route_planner.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py -q` | Passed: 67 passed. |
| `python3 -m pytest tests/test_release_smoke.py::test_cli_external_tool_first_plan_returns_contract -q` | Passed: 1 passed. |
| `PYTHONPATH=src python3 -m mathdevmcp.cli external-tool-first-plan 'a + b = b + a'` | Passed and returned `external_tool_first_plan_result`. |
| `python3 -m pytest tests/test_release_smoke.py::test_release_hypotheses_script_public_mode_passes -q` | Failed for pre-existing release-boundary reason: the public release hypothesis gate requires a clean/public-ready tree and the current worktree is dirty. |

## Review

Local skeptical review found no blocker for Phase 0. The main boundary to carry
forward is that `requires_formalization` means "external route to attempt after
formalization," not proof or certification.

Claude review was requested with a bounded bundle:

- `docs/reviews/mathdevmcp-external-tool-first-tree-derivation-review-bundle-2026-07-08.md`

The first Opus attempt failed with a server-side model-unavailable error. A
default-model retry also failed with a server-side model-unavailable error.
Claude review was therefore unavailable for this phase. The phase proceeds on
the local skeptical review plus focused test evidence above; this is weaker
than an independent Claude review and should not be represented as a Claude
approval.

## Next Handoff

Proceed to Phase 1/2 by defining the branch/tree JSON data model on top of
`external_tool_first_plan`. Do not implement search expansion until every node
can record source span, assumptions, tool consideration, backend attempt,
blocker, and non-claim boundary.
