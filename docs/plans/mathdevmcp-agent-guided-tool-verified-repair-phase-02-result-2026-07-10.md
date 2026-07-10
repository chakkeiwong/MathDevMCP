# Phase 02 Result: Agent Hypothesis Expansion Interface

Date: 2026-07-10

Status: `PASSED`

## Phase Objective

Represent agent brainstorming as validated candidate expansions attached to
exact blocker nodes, not as repair text.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can agent-generated mathematical ideas be admitted only as structured, non-certifying candidate branches? |
| Baseline/comparator | Current deterministic branch templates with no explicit agent-hypothesis schema. |
| Primary criterion | Met. Blockers can now produce validated `agent_hypothesis_expansion` candidates with blocker id, assumptions, route, backend role, success criterion, failure criterion, source refs, and non-proof boundary. |
| Veto diagnostics | No veto fired. Vague/unbounded hypotheses are rejected by validation; document reports still use gap reports for blocked branches. |
| Explanatory diagnostics | Initial implementation uses deterministic seed expansions. External LLM-generated hypotheses can later enter through the same validator. |
| Not concluded | Hypotheses are not repairs, proofs, validated assumptions, recursive search results, or backend certificates. |

## Implementation Summary

- Added `src/mathdevmcp/agent_hypothesis_expansion.py`.
- Added contracts:
  - `agent_hypothesis_expansion`
  - `agent_hypothesis_expansion_set`
- Added `propose_hypothesis_expansions` with deterministic seed routes for:
  - conditional-law blockers;
  - integrability blockers;
  - macro-translation blockers;
  - generic manual-formalization blockers.
- Added `validate_agent_hypothesis_expansion`.
- Attached hypothesis expansion sets to blocked document-tree branches.
- Rendered those hypotheses into branch expansion records as
  `agent_hypothesis_candidate`, preserving the non-proof boundary.

## Files Changed

- `src/mathdevmcp/agent_hypothesis_expansion.py`
- `src/mathdevmcp/document_derivation_tree.py`
- `src/mathdevmcp/derivation_branch_controller.py`
- `tests/test_agent_hypothesis_expansion.py`
- `tests/test_document_derivation_tree.py`

## Checks

| Check | Status |
| --- | --- |
| `python3 -m pytest tests/test_agent_hypothesis_expansion.py -q` | Passed: `4 passed in 0.02s` |
| `python3 -m pytest tests/test_document_derivation_tree.py -q` | Passed: `13 passed in 114.12s` |
| `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q` | Passed: `29 passed in 0.24s` |
| `python3 -m py_compile src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py` | Passed |
| `git diff --check` on touched Phase 02 files | Passed |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 03 | `passed` | Vague/unbounded hypotheses rejected; no raw hypothesis report leakage | Recursive tree search still needs to consume candidate hypotheses as child nodes | Implement bounded recursive derivation tree expansion | No proof or repair certification from hypotheses |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Dirty worktree; exact commit not asserted in Phase 02 |
| Commands/checks | Listed above |
| Environment | Local workspace `/home/chakwong/python/MathDevMCP` |
| CPU/GPU | N/A |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | Document-tree test took `114.12s`; related tests took `0.24s`; standalone tests took `0.02s` |
| Output artifacts | This result file |
| Plan file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-agent-hypotheses-subplan-2026-07-10.md` |
| Result file | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-result-2026-07-10.md` |

## Review Trail

Codex performed a local skeptical review against the Phase 02 evidence
contract.  No Claude review was used because Phase 00 established that the
external Claude gate was blocked by data-transfer policy.

## Next Action

Begin Phase 03: Recursive Derivation Tree Search.
