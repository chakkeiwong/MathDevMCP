# Phase 08 Result: Parallel Search Discipline

Date: 2026-07-10

Status: `PASSED`

## Evidence Contract Result

Question: Can independent branches be tested faster without changing logical
results or hiding failures?

Result: yes for independent document target rows.  The document
derivation-tree workflow now accepts `workers`, defaults to serial execution,
and uses bounded thread workers only when `workers > 1` and multiple target
rows are selected.  Outputs are sorted back to source-row order.  Worker
failures become target-level blockers and compiler validation errors, not
refutations or repair proposals.

## Skeptical Audit

- Wrong baseline checked: Phase 08 compares against serial strict output, not
  speed.
- Proxy metric checked: no speedup claim is made or used as a pass criterion.
- Hidden assumption checked: parallel execution is optional and does not change
  strict grounding policy.
- Environment mismatch checked: backend availability remains recorded through
  `doctor_report`; worker failure is a blocker.
- Artifact mismatch checked: tests compare logical serial/parallel outputs and
  source ordering, not only the existence of a `workers` flag.

Audit result: passed.

## Implementation Summary

- Added `workers` to `audit_document_derivation_tree`, CLI, MCP facade, and
  FastMCP server.
- Factored per-row target building into a shared helper used by both serial
  and parallel paths.
- Added `document_derivation_tree_parallel_execution` metadata to reports.
- Added deterministic ordering and target-level failure blockers for worker
  exceptions.
- Added serial/parallel logical-equivalence tests.

## Checks Run

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `14 passed in 129.77s`.
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  passed, `46 passed in 126.17s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `44 passed in 0.22s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`:
  passed.
- `git diff --check` on touched Phase 08 files: passed.

## Non-Claims

- No speedup guarantee.
- No claim that parallel execution is safe for every future backend adapter.
- No release-readiness claim.
- No whole-document proof claim.

## Handoff

Advance to Phase 09: Real-Document Regression And Mission Control.
