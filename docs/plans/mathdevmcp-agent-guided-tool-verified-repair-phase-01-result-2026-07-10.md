# Phase 01 Result: Strict Contracts And Regression Gates

Date: 2026-07-10

Status: `PASSED`

## Phase Objective

Define strict machine-readable contracts and regression gates that prevent
diagnostic-only or raw-agent branches from rendering as repair proposals.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can contracts prevent raw agent hypotheses and diagnostic-only branches from becoming repair proposals? |
| Baseline/comparator | Existing `context_aware_executable_repair_proposal` generation from top-ranked branch. |
| Primary criterion | Met. Blocked branches now render as `document_gap_report`; backend-closed paths still render as `context_aware_executable_repair_proposal`. |
| Veto diagnostics | No veto fired. Focused tests reject blocked FOC/NPV repair proposal leakage and preserve the positive simple-algebra backend-closed proposal path. |
| Explanatory diagnostics | Reports become more conservative: blocked stochastic cases now produce gap reports with exact blockers instead of proposed LaTeX repairs. |
| Not concluded | No recursive search, agent hypothesis generation, backend formalization expansion, or real-document quality claim yet. |

## Implementation Summary

- Added `DOCUMENT_GAP_REPORT_CONTRACT = "document_gap_report"`.
- Added strict closure classification:
  `closed_by_backend`, `partially_closed_by_backend`,
  `blocked_at_exact_node`, `refuted_by_backend`, and
  `source_assumption_gap_only`.
- Changed blocked top-ranked branches to emit `document_gap_reports` instead
  of `document_ready_repair_proposals`.
- Preserved `context_aware_executable_repair_proposal` for backend-closed or
  partially backend-closed paths.
- Added `strict_proposal_gate` to the tool-use ledger.
- Updated Markdown rendering with a separate `Document gap reports` section.
- Updated focused tests so blocked NPV/FOC cases cannot regress into repair
  proposals.

## Files Changed

- `src/mathdevmcp/document_derivation_tree.py`
- `tests/test_document_derivation_tree.py`

## Checks

| Check | Status |
| --- | --- |
| `python3 -m pytest tests/test_document_derivation_tree.py -q` | Passed: `13 passed in 109.90s` |
| `python3 -m pytest tests/test_derivation_tree_report.py tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_tree_derivation_lane_integration.py -q` | Passed: `29 passed in 0.20s` |
| `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py` | Passed |
| `git diff --check` on touched Phase 01 files | Passed |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 02 | `passed` | No blocked diagnostic branch rendered as repair in focused tests | Future agent-hypothesis interface must preserve the new gate | Implement structured agent hypothesis expansion records | No recursive search or real-document improvement claim |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Dirty worktree; exact commit not asserted in Phase 01 |
| Commands/checks | Listed above |
| Environment | Local workspace `/home/chakwong/python/MathDevMCP` |
| CPU/GPU | N/A |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Focused document-tree test took `109.90s`; related tests took `0.20s` |
| Output artifacts | This result file |
| Plan file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-contracts-subplan-2026-07-10.md` |
| Result file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-result-2026-07-10.md` |

## Review Trail

No external Claude review was used for Phase 01 because the Phase 00 Claude
gate was rejected as external data transfer.  Codex performed a local skeptical
review against the Phase 01 evidence contract before and after the checks.

## Next Action

Begin Phase 02: Agent Hypothesis Expansion Interface.
