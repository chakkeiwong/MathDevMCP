# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `mathdevmcp-external-tool-first-tree-derivation`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority. Claude is an advisory
read-only reviewer.

## Objective

Review the new external-tool-first policy and first implementation slice for
the MathDevMCP tree derivation search lane.

## Artifacts To Inspect

Inspect these bounded local artifacts only as needed:

- `AGENTS.md`
- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-plan-2026-07-08.md`
- `src/mathdevmcp/external_tool_policy.py`
- `src/mathdevmcp/backend_route_planner.py`
- `tests/test_external_tool_policy.py`
- `tests/test_backend_route_planner.py`
- `mcp/README.md`
- `README.md`

Do not review unrelated dirty worktree changes. The repository has many
pre-existing modified/untracked files from earlier lanes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does this slice correctly enforce an external-tool-first discipline before future in-house tree search? |
| Baseline/comparator | Existing MathDevMCP route plans and high-level workflows, which could produce weak one-shot reports. |
| Primary criterion | Policy, plan, code, and tests must force explicit external tool consideration and preserve non-certifying boundaries. |
| Veto diagnostics | In-house search allowed without a gap justification; route/retrieval/proof-state evidence treated as proof; backend absence treated as refutation; tests fail to guard the policy. |
| Explanatory diagnostics | Missing polish, naming improvements, or future-phase suggestions that do not break the boundary. |
| Not concluded | No broad theorem-proving claim, no public release readiness, no proof of full tree search, and no claim that a route plan certifies math. |

## Local Checks Already Run

- `python3 -m py_compile src/mathdevmcp/external_tool_policy.py src/mathdevmcp/backend_route_planner.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py src/mathdevmcp/cli.py` passed.
- `git diff --check -- ...` on touched files passed.
- `python3 -m pytest tests/test_external_tool_policy.py tests/test_backend_route_planner.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py -q` passed: 67 passed.
- `python3 -m pytest tests/test_release_smoke.py::test_cli_external_tool_first_plan_returns_contract -q` passed: 1 passed.
- `tests/test_release_smoke.py::test_release_hypotheses_script_public_mode_passes` fails because the existing release hypothesis gate requires a clean/public-ready tree and this worktree is dirty. Treat that as a release-boundary blocker, not evidence against this slice.

## Review Questions

1. Is there a material correctness or boundary issue in the policy/plan/code
   contract?
2. Does the implementation avoid building a new prover and instead force
   direct external-tool consideration?
3. Are the tests sufficient for Phase 0, especially the in-house search gate
   and non-certifying boundary?
4. Are there unsupported claims or hidden authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
