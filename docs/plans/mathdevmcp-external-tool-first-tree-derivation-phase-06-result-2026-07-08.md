# MathDevMCP External-Tool-First Tree Derivation Phase 06 Result

Date: 2026-07-08

## Objective

Make the external-tool-first tree derivation lane durable for future agents
through mission-control guidance, support-matrix documentation, and integrated
controller-to-report regression coverage.

## Artifacts

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-06-subplan-2026-07-08.md`
- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md`
- `docs/mathdevmcp-support-matrix.md`
- `tests/test_tree_derivation_lane_integration.py`

## What Changed

Added lane-specific mission control that records:

- completed phases;
- callable contracts;
- core invariants;
- required regression checks;
- future work;
- non-claims.

Updated the support matrix with the internal `tree-derivation` lane and its
validation command. The row explicitly states that this lane is not public
release evidence, not complete MCTS, and not a whole-document proof.

Added integrated regression tests that run controller output through the report
renderer for:

- a proved branch with explicit tool and promotion-guard evidence;
- a budget-exhausted branch preserving blockers and no fabricated patch;
- an unrelated Lean source that must not prove the controller target.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed: future agents now have mission-control guidance and integrated tests tying controller-to-report behavior together. |
| Veto diagnostics | Passed: tests do not require optional packages; support docs avoid release-readiness claims; integrated reports preserve blockers, promotion guard status, exact tool ids, and non-claims. |
| Explanatory diagnostics | CLI/MCP exposure, full document experiments, benchmark fixtures, and MCTS/best-first expansion remain future work. |
| Not concluded | No public release readiness, no complete MCTS, no whole-document proof, no full document repair integration. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_tree_derivation_lane_integration.py tests/test_derivation_branch_controller.py tests/test_derivation_tree_report.py -q` | Passed: 18 passed. |
| `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_tree_report.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py` | Passed. |
| `git diff --check -- docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md docs/mathdevmcp-support-matrix.md tests/test_tree_derivation_lane_integration.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-06-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-06-result-2026-07-08.md` | Passed before this result note was added; rerun after note creation required for closeout. |

## Review

Local skeptical review found no blocker. This phase adds mission-control and
regression durability rather than new certification logic. Claude review was
not attempted because prior review-gate artifact export was rejected by policy.

## Master Program Status

The master-program slice described by
`docs/plans/mathdevmcp-external-tool-first-tree-derivation-plan-2026-07-08.md`
is complete for Phases 0-6:

- external-tool-first policy;
- search-tree evidence model;
- adapter evidence wrappers;
- budgeted branch controller;
- branch-derived report renderer;
- mission-control and integrated regression durability.

Remaining deferred work is outside this completed slice:

- CLI/MCP exposure for the new controller/report APIs;
- full risky-debt and credit-card document experiments;
- larger benchmark fixtures;
- MCTS/best-first expansion;
- optional real-backend smoke tests under explicit backend profiles.
