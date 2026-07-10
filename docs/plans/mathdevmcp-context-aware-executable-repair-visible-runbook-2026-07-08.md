# MathDevMCP Context-Aware Executable Repair Visible Runbook

Date: 2026-07-08

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook is based on the visible gated execution template.  It must not
launch a detached or nested agent.  It must not use `codex exec`,
`overnight_gated_launch.sh`, detached `tmux`, `nohup`, `setsid`, backgrounded
phase runners, or copied-workspace execution.  This is therefore a visible
gated execution plan for an overnight-scale lane, not a detached overnight
supervisor.

## Program

Master program:

- `docs/plans/mathdevmcp-context-aware-executable-repair-master-program-2026-07-08.md`

Review bundle:

- `docs/reviews/mathdevmcp-context-aware-executable-repair-plan-review-bundle-2026-07-08.md`

Execution ledger:

- `docs/plans/mathdevmcp-context-aware-executable-repair-visible-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/mathdevmcp-context-aware-executable-repair-visible-stop-handoff-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Review Gate | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-governance-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-result-2026-07-08.md` |
| 1 | Proposition And Context Packet Extraction | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-proposition-context-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-result-2026-07-08.md` |
| 2 | Local Mathematical Context Graph | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-context-graph-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-result-2026-07-08.md` |
| 3 | Typed Repair Obligation IR | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-typed-ir-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-result-2026-07-08.md` |
| 4 | Executable Backend Translators | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-executable-backends-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-result-2026-07-08.md` |
| 5 | Budgeted Repair Branch Search | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-branch-search-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-result-2026-07-08.md` |
| 6 | Document-Ready Repair Report Regression | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-report-regression-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP move from structured diagnostics to context-aware executable repair proposals? |
| Baseline/comparator | Current Phase 04 display-equation reports. |
| Primary pass criterion | Frozen targets produce proposition/context packets, typed obligations, executable attempts or precise blockers, ranked branches, and document-ready repair text. |
| Veto diagnostics | Template-only text, missing proposition targets, proof overclaim, no external-tool ledger, no typed obligation. |
| Explanatory diagnostics | Backend absence, unsupported stochastic operators, ambiguous context, budget exhaustion. |
| Not concluded | Whole-document proof, release readiness, global minimality. |
| Artifacts | Phase results, logs, tests, review trail, frozen reports. |

## Anticipated Approval Needs

- Claude read-only review gate may require trusted execution:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh ...`.
- No package installation, network fetch, destructive filesystem action, or
  detached execution is anticipated for Phase 00 or Phase 01.
- If Claude review is blocked as external-service data transfer, Codex will
  record the blocker and use fresh Codex read-only fallback review.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, restate evidence contract, append ledger entry.
2. `EXECUTE_MINIMAL`: implement or diagnose the smallest bounded slice.
3. `ASSESS_GATE`: compare outputs to pass/veto criteria and write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer when allowed; otherwise use
   fresh Codex fallback review.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, stop
   after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase passes.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, credentials, or environment setup;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- modifying unrelated dirty user work;
- proof-boundary weakening;
- continuing after five nonconvergent review rounds.
