# Phase 04 Result: Backend Formalization Targets

Date: 2026-07-10

Status: `PASSED`

## Phase Objective

Translate validated search paths into backend-native formalization targets, or
return exact non-encodability blockers.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can each candidate path become a runnable backend target or an exact formalization blocker? |
| Baseline/comparator | Current branch-level backend attempts and formalization stubs. |
| Primary criterion | Met for Phase 04 scope. Expanded child nodes now carry `backend_formalization_target` records that classify backend-ready, skeleton-only, diagnostic-only, and blocked-not-encodable routes. |
| Veto diagnostics | No veto fired. LeanDojo/Pantograph/search routes remain diagnostic-only; Lean skeletons with `sorry` carry placeholder blockers; backend-not-encodable is not a refutation. |
| Explanatory diagnostics | Formalization targets prepare execution but do not run certifying backends in this phase. |
| Not concluded | No full-document proof, backend completeness claim, or certification from formalization targets alone. |

## Implementation Summary

- Added `src/mathdevmcp/backend_formalization_target.py`.
- Added `backend_formalization_target` contract.
- Added `build_backend_formalization_target`.
- Formalization target statuses include:
  - `backend_ready`;
  - `blocked_not_encodable`;
  - `diagnostic_only_route`;
  - `lean_skeleton_only`.
- Integrated formalization targets into expanded derivation-tree child nodes.
- Child nodes append exact formalization blockers from targets.

## Files Changed

- `src/mathdevmcp/backend_formalization_target.py`
- `src/mathdevmcp/derivation_tree_expansion.py`
- `tests/test_backend_formalization_target.py`
- `tests/test_derivation_tree_expansion.py`

## Checks

| Check | Status |
| --- | --- |
| `python3 -m pytest tests/test_backend_formalization_target.py tests/test_derivation_tree_expansion.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py -q` | Passed: `28 passed in 0.21s` |
| `python3 -m pytest tests/test_document_derivation_tree.py -q` | Passed: `13 passed in 120.57s` |
| `python3 -m py_compile src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/document_derivation_tree.py` | Passed |
| `git diff --check` on touched Phase 04 files | Passed |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 05 | `passed` | No diagnostic route was promoted to proof | Expansion-rule coverage is still sparse | Add generic expansion rules for common blockers | No backend certification from target records |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Dirty worktree; exact commit not asserted in Phase 04 |
| Commands/checks | Listed above |
| Environment | Local workspace `/home/chakwong/python/MathDevMCP` |
| CPU/GPU | N/A |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Document-tree test took `120.57s`; related tests took `0.21s` |
| Output artifacts | This result file |
| Plan file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-backend-formalization-subplan-2026-07-10.md` |
| Result file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-result-2026-07-10.md` |

## Review Trail

Codex performed a local skeptical review against the Phase 04 evidence
contract.  No Claude review was used because Phase 00 established that the
external Claude gate was blocked by data-transfer policy.

## Next Action

Begin Phase 05: Expansion Rule Library.
