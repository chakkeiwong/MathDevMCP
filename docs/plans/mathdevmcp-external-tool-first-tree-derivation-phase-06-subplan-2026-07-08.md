# MathDevMCP External-Tool-First Tree Derivation Phase 06 Subplan

Date: 2026-07-08

## Phase Objective

Make the external-tool-first tree derivation lane durable for future agents by
adding mission-control guidance, support-matrix documentation, and integrated
regression coverage tying controller output to report rendering.

## Entry Conditions

- Phase 0 external-tool-first policy exists.
- Phase 1/2 tree contract exists.
- Phase 3 adapter evidence wrappers exist.
- Phase 4 budgeted controller exists.
- Phase 5 branch-derived renderer exists.
- The current worktree is dirty from prior lanes and must be preserved.

## Required Artifacts

- mission-control/checklist update under `docs/plans`
- support-matrix or README update if scoped
- integrated regression test
- phase result note under `docs/plans`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can future agents discover and preserve the external-tool-first tree derivation lane without regressing to yes/no or hand-wavy report behavior? |
| Baseline/comparator | Phases 0-5 create code contracts, but no final mission-control durable handoff or integrated regression test exists. |
| Primary criterion | A mission-control checklist names the lane, exact contracts, phase artifacts, boundaries, and regression checks; integrated tests exercise controller-to-report behavior for proof/refutation/blocked or budget-exhausted cases. |
| Veto diagnostics | Mission control claims release readiness; tests require optional external packages; integrated report hides blockers or promotion guard errors; documentation implies retrieval/proof-state evidence is proof. |
| Explanatory diagnostics | Remaining deferred work: CLI/MCP exposure, full document experiments, benchmark fixtures. |
| Not concluded | No public release readiness, no complete MCTS, no full document repair integration. |

## Required Checks

- `python3 -m pytest tests/test_tree_derivation_lane_integration.py tests/test_derivation_branch_controller.py tests/test_derivation_tree_report.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_tree_report.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py`
- `git diff --check -- docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md docs/mathdevmcp-support-matrix.md tests/test_tree_derivation_lane_integration.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-06-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-06-result-2026-07-08.md`

## Required Reviews

- Local skeptical review after implementation.
- Fresh Codex read-only fallback review only if new boundary issues are
  suspected; do not use Claude without explicit artifact-export approval.

## Scope

Implement:

- mission-control checklist for the lane;
- concise support-matrix row for tree derivation lane status;
- integrated regression test that runs controller output through renderer and
  checks exact tools, blockers, promotion guard, and non-claims.

Defer:

- CLI/MCP exposure;
- full risky-debt/credit-card document experiments;
- large benchmark corpus integration;
- MCTS or parallel hypothesis search.

## Forbidden Claims And Actions

- Do not claim the master program proves documents.
- Do not claim public release readiness.
- Do not run long backend or document experiments.
- Do not require optional external packages in tests.
- Do not revert unrelated dirty worktree changes.

## Exact Closeout Conditions

The runbook can be considered completed for this master-program slice when:

- all Phase 6 checks pass;
- the mission-control doc lists completed phases and remaining deferred work;
- integrated tests prevent yes/no or hand-wavy report regressions for the lane;
- result notes explicitly preserve non-claims.

## Stop Conditions

Stop and write a blocker if:

- integrated tests cannot be made deterministic without optional packages;
- support documentation would need broader release-readiness decisions;
- dirty worktree changes make scoped docs/tests unsafe to edit.

## Skeptical Plan Audit

Wrong baseline: Phase 6 is not product launch. It is durable handoff and
regression discipline for the lane.

Proxy metric: documentation length is not success. The pass criterion is a
future-agent checklist plus executable integrated regression.

Hidden assumption: support-matrix text must describe current lane status, not
overstate readiness or document-repair completeness.

Environment mismatch: tests must use injected runners and local fixtures only.

Audit result: proceed with mission-control doc, narrow support-matrix update,
and integrated regression test.
