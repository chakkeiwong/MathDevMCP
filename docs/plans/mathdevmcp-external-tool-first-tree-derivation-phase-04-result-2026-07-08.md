# MathDevMCP External-Tool-First Tree Derivation Phase 04 Result

Date: 2026-07-08

## Objective

Implement a first deterministic, budgeted branch controller over the Phase 1/2
search-tree contract and Phase 3 adapter evidence wrappers.

## Artifacts

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-04-subplan-2026-07-08.md`
- `src/mathdevmcp/derivation_branch_controller.py`
- `tests/test_derivation_branch_controller.py`

## What Changed

Added `can_derive_with_budget`, a controller that:

- initializes a derivation search tree from an external-tool-first plan;
- respects the external-tool-first blocked gate and does not run in-house
  actions when the gate is blocked;
- runs bounded evidence actions in deterministic order;
- records backend attempts and diagnostic blockers in the root branch;
- preserves budget exhaustion with explicit exhausted action names;
- promotes `proved`/`refuted` only through the Phase 1/2 promotion guard;
- returns the tree contract with controller diagnostics rather than a bare
  yes/no answer.

Implemented budget profiles:

- `smoke`: one evidence attempt;
- `standard`: three evidence attempts.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed for Phase 4: the controller initializes a tree, runs deterministic bounded evidence actions, records attempts/blockers, and sets status through the promotion guard. |
| Veto diagnostics | Passed in focused tests: blocked external-tool-first gate runs no attempts; proof/refutation require promotable evidence; adapter errors become diagnostic blockers; budget exhaustion preserves attempted and exhausted action state. |
| Explanatory diagnostics | This is a deterministic skeleton, not MCTS. Automatic assumption expansion, formalization search, and report rendering are deferred. |
| Not concluded | No complete theorem search, no global minimality, no document repair reports, no public release readiness. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py -q` | Passed after review repair: 30 passed. |
| `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py` | Passed. |
| `git diff --check -- src/mathdevmcp/derivation_branch_controller.py tests/test_derivation_branch_controller.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-04-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-04-result-2026-07-08.md` | Passed before this result note was added; rerun after note creation required for closeout. |

## Repair Loop

The first controller test run exposed status and ordering issues:

1. The final promotion pass could overwrite `budget_exhausted` back to
   `partial`.
2. Explicit Lean source was scheduled after counterexample search, causing the
   standard budget to spend an attempt on finite search before Lean
   verification.

Both were repaired. Budget exhaustion now remains visible unless proof or
refutation has already been promoted, and explicit Lean source is checked
before counterexample fallback.

## Review

Local skeptical review found no blocker after the repair above. Claude review
was not attempted because prior review-gate export was rejected by policy.

A fresh Codex read-only fallback review returned `VERDICT: REVISE` with three
findings:

1. Lean verification could promote an unrelated target because the controller
   accepted any verified `lean_source`.
2. The implementation order had drifted from the subplan's
   algebra/counterexample/Lean order.
3. Controller action calls were not guarded against adapter-side exceptions
   outside the adapter wrapper's own runner exception handling.

All three findings were repaired. Lean source is now conservatively required to
bind to the controller target before it can be scheduled as certifying evidence;
otherwise it creates a formalization blocker. The controller action order is
again algebra, counterexample, then Lean. Controller action calls are wrapped so
unexpected adapter exceptions become diagnostic attempts and blockers. Focused
regression tests cover all three repairs, and the required checks passed after
repair.

## Next Handoff

Proceed to Phase 5 if closeout checks and fallback review pass. Phase 5 should
render branch-derived reports with:

- location;
- problem;
- mathematical why;
- assumptions/routes;
- derivation evidence;
- exact tools used;
- proposed patch;
- remaining blockers.

The report must be generated from tree evidence, not generic fallback prose.
