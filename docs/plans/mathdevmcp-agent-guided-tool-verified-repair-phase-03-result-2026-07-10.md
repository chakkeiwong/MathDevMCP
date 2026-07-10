# Phase 03 Result: Recursive Derivation Tree Search

Date: 2026-07-10

Status: `PASSED`

## Phase Objective

Upgrade the derivation tree from ranked static ledger to bounded recursive
search over blocker nodes, candidate hypotheses, backend attempts, and exact
new blockers.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can exact blockers be recursively expanded into child search nodes without proof overclaims? |
| Baseline/comparator | Current one-shot branch controller and static branch ranking. |
| Primary criterion | Met for Phase 03 scope. Validated agent hypotheses become child nodes with parent node id, parent blocker id, candidate assumptions, derivation step, backend-evidence-required blocker, and explicit budget status. |
| Veto diagnostics | No veto fired. Expansion does not create backend evidence, does not promote branches, and records max-node budget exhaustion explicitly. |
| Explanatory diagnostics | This phase creates the recursive search spine only; backend formalization and execution remain Phase 04+. |
| Not concluded | No MCTS optimality, completeness, backend proof, repair proposal, or global derivation search claim. |

## Implementation Summary

- Added `src/mathdevmcp/derivation_tree_expansion.py`.
- Added `derivation_tree_expansion_result` contract.
- Added `expand_tree_with_hypotheses`.
- Added child-node statuses `expanded_by_agent` and `backend_ready` to the
  search-tree status set.
- Child nodes preserve:
  - parent node id;
  - parent blocker id;
  - source span;
  - external-tool-first plan;
  - explicit assumptions from the hypothesis;
  - candidate derivation step;
  - backend-evidence-required blocker.
- Integrated a bounded expansion summary into `audit_document_derivation_tree`
  compact tree output.

## Files Changed

- `src/mathdevmcp/derivation_tree_expansion.py`
- `src/mathdevmcp/derivation_search_tree.py`
- `src/mathdevmcp/document_derivation_tree.py`
- `tests/test_derivation_tree_expansion.py`
- `tests/test_document_derivation_tree.py`

## Checks

| Check | Status |
| --- | --- |
| `python3 -m pytest tests/test_derivation_tree_expansion.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q` | Passed: `32 passed in 0.20s` |
| `python3 -m pytest tests/test_document_derivation_tree.py -q` | Passed: `13 passed in 120.12s` |
| `python3 -m py_compile src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/document_derivation_tree.py` | Passed |
| `git diff --check` on touched Phase 03 files | Passed |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 04 | `passed` | No promotion or hidden budget veto | Child nodes still require backend-native formalization targets before evidence can close them | Implement backend formalization target records | No backend execution or repair certification from expansion alone |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Dirty worktree; exact commit not asserted in Phase 03 |
| Commands/checks | Listed above |
| Environment | Local workspace `/home/chakwong/python/MathDevMCP` |
| CPU/GPU | N/A |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Document-tree test took `120.12s`; related tests took `0.20s` |
| Output artifacts | This result file |
| Plan file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-recursive-tree-subplan-2026-07-10.md` |
| Result file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-result-2026-07-10.md` |

## Review Trail

Codex performed a local skeptical review against the Phase 03 evidence
contract.  No Claude review was used because Phase 00 established that the
external Claude gate was blocked by data-transfer policy.

## Next Action

Begin Phase 04: Backend Formalization Targets.
