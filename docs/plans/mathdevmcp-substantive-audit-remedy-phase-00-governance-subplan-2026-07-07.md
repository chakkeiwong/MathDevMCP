# Phase 0 Subplan: Governance And Review Gate

Date: 2026-07-07

Status: `READY_FOR_REVIEW`

## Phase Objective

Validate the master program, phase decomposition, evidence contract, and visible
execution runbook before changing implementation code.

## Entry Conditions

- User requested a combined remedy plan and execution.
- D447 feedback document has been read.
- Current weak credit-card rigor report regression has been diagnosed.

## Required Artifacts

- Master program.
- Visible gated execution runbook.
- Phase subplans.
- Claude/Codex review trail.
- Phase 0 result record.

## Required Checks/Tests/Reviews

- Skeptical plan audit.
- `git diff --check` for plan artifacts.
- Claude read-only review gate if available.
- Fresh Codex fallback review if Claude is blocked/unavailable.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the remedy program logically ordered and safe to launch? |
| Baseline/comparator | Current weak report diagnosis and D447 feedback examples. |
| Primary criterion | Plan has explicit dependencies, stop conditions, evidence contracts, and forbids field-presence-only pass criteria. |
| Veto diagnostics | Missing stop conditions; Claude as executor; experiments before evidence filtering; report reruns before contract repair; proof/product/science overclaiming. |
| Explanatory diagnostics | Review verdict, local plan checks, dirty-worktree inventory. |
| Not concluded | Implementation correctness or improved report quality. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 0.
- Do not run document experiments in Phase 0.
- Do not let Claude authorize execution.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only after the plan/runbook pass review or fixable review
findings are repaired and rechecked.

## Stop Conditions

Stop if review finds a dependency-order flaw that cannot be repaired without a
human decision, or if both Claude and fallback review are unavailable.
