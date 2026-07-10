# MathDevMCP External-Tool-First Tree Derivation Phase 05 Result

Date: 2026-07-08

## Objective

Render derivation-search tree evidence into agent-consumable repair reports
without fabricating fixes or converting diagnostic evidence into proof.

## Artifacts

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-05-subplan-2026-07-08.md`
- `src/mathdevmcp/derivation_tree_report.py`
- `tests/test_derivation_tree_report.py`

## What Changed

Added `render_derivation_tree_report`, which returns a
`derivation_tree_report_result` payload with structured branch sections and
Markdown.

Each section renders evidence from the tree:

- location from `source_span` or patch candidate location;
- problem and mathematical why;
- assumption sets and derivation steps;
- exact tool/backend attempt ids, statuses, evidence kinds, and certification
  statuses;
- proposed patch candidates from the tree;
- remaining blockers and required next evidence;
- warnings when no patch candidate exists;
- promotion-guard result and non-claims.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed for Phase 5: renderer emits required location/problem/why/tools/patch/blocker/non-claim fields from tree evidence. |
| Veto diagnostics | Passed in focused tests: missing patch candidates produce warnings rather than fabricated fixes; blockers are preserved; certifying status is reported only from the tree promotion guard. |
| Explanatory diagnostics | This renderer does not yet write `.md` files from CLI/MCP or run document experiments. |
| Not concluded | No automatic document patching, no full audit integration, no proof of document correctness, no public release readiness. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_tree_report.py tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py -q` | Passed after review repair: 24 passed. |
| `python3 -m py_compile src/mathdevmcp/derivation_tree_report.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py` | Passed. |
| `git diff --check -- src/mathdevmcp/derivation_tree_report.py tests/test_derivation_tree_report.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-05-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-05-result-2026-07-08.md` | Passed before this result note was added; rerun after note creation required for closeout. |

## Review

Local skeptical review found no blocker. Claude review was not attempted
because prior review-gate artifact export was rejected by policy.

A fresh Codex read-only fallback review returned `VERDICT: REVISE` with three
findings:

1. The renderer described `proved`/`refuted` nodes as evidence-supported based
   on node status alone instead of the promotion guard.
2. Markdown did not render promotion guard errors or evidence refs, so a human
   report could hide malformed proof/refutation claims.
3. Tests covered the happy certifying `proved` case but not a malformed
   `proved` node with diagnostic-only evidence.

All findings were repaired. Proof/refutation wording now depends on
`branch_promotion_report`, Markdown renders promotion guard status, evidence
refs, and errors, and a malformed proved-node regression test enforces the
boundary. Required checks passed after repair.

## Next Handoff

Proceed to Phase 6 if closeout checks and fallback review pass. Phase 6 should
make this lane durable through mission-control and benchmark integration:

- mission-control checklist entry;
- regression cases for blocked, partial, proved, refuted, and budget-exhausted
  tree reports;
- support-matrix/README surface updates;
- MCP/CLI parity only if scoped and low-risk.
