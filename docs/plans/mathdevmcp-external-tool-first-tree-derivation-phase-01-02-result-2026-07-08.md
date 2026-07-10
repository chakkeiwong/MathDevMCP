# MathDevMCP External-Tool-First Tree Derivation Phase 01/02 Result

Date: 2026-07-08

## Objective

Define the backend-evidence and derivation-search-tree data model needed by the
later budgeted branch controller. This phase is representation-only: it does
not execute backends, search branches, or certify mathematical claims.

## Artifacts

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-subplan-2026-07-08.md`
- `docs/reviews/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-review-bundle.md`
- `src/mathdevmcp/derivation_search_tree.py`
- `tests/test_derivation_search_tree.py`

## What Changed

Added `derivation_search_tree_result`, an agent-consumable contract for a
derivation-search ledger. The contract records:

- source spans;
- external-tool-first plans;
- assumption sets;
- backend attempts;
- derivation steps;
- blocker nodes;
- patch candidates;
- child branches;
- non-claims and promotion boundaries.

Added promotion guards that distinguish certifying/refuting evidence from
diagnostic evidence. A branch can only promote to `proved` through scoped
certifying backend evidence with an output artifact. A branch can only promote
to `refuted` through a concrete counterexample or scoped contradiction artifact.
Route plans, retrieval hits, static extraction, proof-state traces,
formalization-required states, backend timeouts, and backend unavailability
remain diagnostic.

Added an initial tree builder that embeds the Phase 0
`external_tool_first_plan`. If no external route is selectable and no in-house
gap justification exists, the root is blocked with
`external_tool_or_gap_justification_required` rather than allowing speculative
search.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed for Phase 1/2: the tree serializes source, assumptions, external-tool-first evidence, backend attempts, blockers, patch candidates, non-claims, and promotion guards. |
| Veto diagnostics | Passed in focused tests: route/retrieval/formalization evidence cannot prove a branch; backend unavailability cannot refute a branch; missing external routes create a blocker; patch candidates require location and rationale. |
| Explanatory diagnostics | The model is intentionally not wired into MCP/CLI yet. Direct adapters and the branch controller are Phase 3/4 work. |
| Not concluded | No backend execution, no search expansion, no proof of any document target, no global minimality, no public release readiness. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_search_tree.py tests/test_external_tool_policy.py tests/test_backend_route_planner.py -q` | Passed after repair: 19 passed. |
| `python3 -m py_compile src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/external_tool_policy.py src/mathdevmcp/backend_route_planner.py` | Passed. |
| `git diff --check -- src/mathdevmcp/derivation_search_tree.py tests/test_derivation_search_tree.py docs/reviews/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-review-bundle.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-result-2026-07-08.md` | Passed after repair. |

## Review

Local skeptical review found no phase blocker. The main boundary is preserved:
the tree is a ledger and promotion guard, not a proof engine.

Claude review gate was requested with the bounded review bundle. The sandbox
reviewer rejected the escalated Claude call because it would export local
plan/code/test artifacts to an external review service. No workaround was
attempted. This phase therefore cannot claim Claude approval.

A fresh Codex read-only review was requested as the safer fallback specified by
the runbook. The fallback review returned `VERDICT: REVISE` with two findings:

1. `branch_promotion_report` could return `can_promote=True` while also
   carrying guard errors for a branch whose declared status conflicted with the
   available proof/refutation evidence.
2. The negative promotion test covered route/retrieval/formalization evidence
   but did not explicitly cover static-extraction or proof-state evidence,
   although the veto contract named both.

Both findings were repaired. Promotion guard errors now force
`can_promote=False`, and tests now cover static extraction, proof state, and a
conflicting-status/counterexample case. The focused pytest, py-compile, and diff
checks passed after repair.

## Next Handoff

Proceed to Phase 3 only after closeout diff checks pass and the fallback review
does not identify a material blocker. Phase 3 should implement direct external
tool adapters as bounded evidence producers:

- SymPy/Sage checks for encodable algebra;
- Lean direct check for final certification;
- LeanSearch-v2/LeanExplore retrieval as evidence-only;
- jixia/Pantograph/LeanDojo only when a Lean project/formalization context
  exists.

Phase 3 must keep the same promotion boundary: adapter evidence is diagnostic
unless the scoped backend result is certifying or refuting under this tree
contract.
