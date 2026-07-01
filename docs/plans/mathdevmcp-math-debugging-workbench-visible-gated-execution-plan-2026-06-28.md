# MathDevMCP Mathematical Debugging Workbench Visible Gated Execution Plan

Date: `2026-06-28`

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-sized plan, but execution is visible and recoverable inside
the current conversation.

## Program

Master program:

- `docs/plans/mathdevmcp-math-debugging-workbench-master-program-2026-06-28.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-math-debugging-workbench-claude-review-trail-2026-06-28.md`

Execution ledger:

- `docs/plans/mathdevmcp-math-debugging-workbench-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/mathdevmcp-math-debugging-workbench-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and Baseline Audit | `docs/plans/mathdevmcp-math-debugging-workbench-phase-00-governance-baseline-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-00-governance-baseline-result-2026-06-28.md` |
| 1 | Common Workbench Kernel | `docs/plans/mathdevmcp-math-debugging-workbench-phase-01-common-kernel-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-01-common-kernel-result-2026-06-28.md` |
| 2 | Backend Router | `docs/plans/mathdevmcp-math-debugging-workbench-phase-02-backend-router-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-02-backend-router-result-2026-06-28.md` |
| 3 | Counterexample Search | `docs/plans/mathdevmcp-math-debugging-workbench-phase-03-counterexample-search-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-03-counterexample-search-result-2026-06-28.md` |
| 4 | Assumption Discovery | `docs/plans/mathdevmcp-math-debugging-workbench-phase-04-assumption-discovery-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-04-assumption-discovery-result-2026-06-28.md` |
| 5 | Derive Or Refute | `docs/plans/mathdevmcp-math-debugging-workbench-phase-05-derive-or-refute-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-05-derive-or-refute-result-2026-06-28.md` |
| 6 | Prove Or Refute | `docs/plans/mathdevmcp-math-debugging-workbench-phase-06-prove-or-refute-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-06-prove-or-refute-result-2026-06-28.md` |
| 7 | Proof Gap Localization | `docs/plans/mathdevmcp-math-debugging-workbench-phase-07-proof-gap-localization-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-07-proof-gap-localization-result-2026-06-28.md` |
| 8 | Code Implements Equation | `docs/plans/mathdevmcp-math-debugging-workbench-phase-08-code-implements-equation-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-08-code-implements-equation-result-2026-06-28.md` |
| 9 | Claim Classification | `docs/plans/mathdevmcp-math-debugging-workbench-phase-09-claim-classification-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-09-claim-classification-result-2026-06-28.md` |
| 10 | Notation Reconciliation | `docs/plans/mathdevmcp-math-debugging-workbench-phase-10-notation-reconciliation-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-10-notation-reconciliation-result-2026-06-28.md` |
| 11 | Generate Tests From Math | `docs/plans/mathdevmcp-math-debugging-workbench-phase-11-generate-tests-from-math-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-11-generate-tests-from-math-result-2026-06-28.md` |
| 12 | Human Review Packet | `docs/plans/mathdevmcp-math-debugging-workbench-phase-12-human-review-packet-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-12-human-review-packet-result-2026-06-28.md` |
| 13 | Mathematical Change Impact | `docs/plans/mathdevmcp-math-debugging-workbench-phase-13-change-impact-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-13-change-impact-result-2026-06-28.md` |
| 14 | Literature To Local Audit | `docs/plans/mathdevmcp-math-debugging-workbench-phase-14-literature-local-audit-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-14-literature-local-audit-result-2026-06-28.md` |
| 15 | Operator UX And Regression Closure | `docs/plans/mathdevmcp-math-debugging-workbench-phase-15-operator-ux-regression-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-math-debugging-workbench-phase-15-operator-ux-regression-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo grow a visible, tested, conservative mathematical debugging workbench without crossing proof, release, or scientific claim boundaries? |
| Baseline/comparator | Current low-level proof, derivation, typed-obligation, proof-packet, code-document, symbolic, numeric, and Lean surfaces. |
| Primary pass criterion | Each phase produces its required artifacts and checks, and no workflow promotes unsupported evidence into proof. |
| Veto diagnostics | Prose-only proof, numeric-as-proof, hidden assumption promotion, unavailable-backend-as-refutation, release/gate/readiness overclaim, unrelated dirty-worktree overwrite. |
| Explanatory diagnostics | Focused pytest, CLI smoke checks, MCP sync checks, plan review, and result ledgers. |
| Not concluded | Full proof automation, scientific validity, release readiness, benchmark generalization, or theorem applicability outside checked assumptions. |
| Artifacts | Master program, phase subplans/results, ledger, Claude review trail, stop handoff, code/tests/docs diffs. |

## Skeptical Plan Audit

Before executing any phase, Codex must check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the relevant subplan or write a
blocker result before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run visible local commands in the current conversation.
   - Prefer the smallest implementation or diagnostic needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase plans/results/diffs to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or patch and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch visibly, rerun focused checks, and update
     result artifacts.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the phase gate passes.
   - Stop and write handoff if a human-required blocker appears.

## Claude Read-Only Review Template

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review this compact brief, not whole files:
- phase:
- objective:
- artifacts:
- checks:
- evidence contract:
- forbidden claims/actions:
- handoff:
- stop conditions:

Check wrong baseline, proxy metrics, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim, and
artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed program;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default release or benchmark policy;
- modifying unrelated dirty user work;
- interpreting special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.
