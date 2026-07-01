# MathDevMCP Workbench Benchmark Visible Gated Execution Plan

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

- `docs/plans/mathdevmcp-workbench-benchmark-master-program-2026-06-28.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-workbench-benchmark-claude-review-trail-2026-06-28.md`

Execution ledger:

- `docs/plans/mathdevmcp-workbench-benchmark-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/mathdevmcp-workbench-benchmark-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Source Inventory | `docs/plans/mathdevmcp-workbench-benchmark-phase-00-governance-source-inventory-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-00-governance-source-inventory-result-2026-06-28.md` |
| 1 | Schema And Quality Rubric | `docs/plans/mathdevmcp-workbench-benchmark-phase-01-schema-quality-rubric-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-01-schema-quality-rubric-result-2026-06-28.md` |
| 2 | Seeded Workbench Benchmark | `docs/plans/mathdevmcp-workbench-benchmark-phase-02-seeded-workbench-benchmark-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-02-seeded-workbench-benchmark-result-2026-06-28.md` |
| 3 | Benchmark Quality Metrics | `docs/plans/mathdevmcp-workbench-benchmark-phase-03-benchmark-quality-metrics-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-03-benchmark-quality-metrics-result-2026-06-28.md` |
| 4 | External Source Provenance Protocol | `docs/plans/mathdevmcp-workbench-benchmark-phase-04-external-source-provenance-protocol-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-04-external-source-provenance-protocol-result-2026-06-28.md` |
| 5 | External Adapted Pack Ingestion | `docs/plans/mathdevmcp-workbench-benchmark-phase-05-external-adapted-pack-ingestion-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-05-external-adapted-pack-ingestion-result-2026-06-28.md` |
| 6 | Gate And Report Integration | `docs/plans/mathdevmcp-workbench-benchmark-phase-06-gate-report-integration-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-06-gate-report-integration-result-2026-06-28.md` |
| 7 | Docs And Operator UX | `docs/plans/mathdevmcp-workbench-benchmark-phase-07-docs-operator-ux-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-07-docs-operator-ux-result-2026-06-28.md` |
| 8 | Final Regression And Handoff | `docs/plans/mathdevmcp-workbench-benchmark-phase-08-final-regression-handoff-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-workbench-benchmark-phase-08-final-regression-handoff-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP add a formal benchmark program for the new workbench tools that measures status/boundary behavior, benchmark quality, and licensed external adapted-pack readiness without overclaiming? |
| Baseline/comparator | Existing formal benchmark gate `41/41`, focused workbench regression `84 passed`, and MCP sync `26 passed`. |
| Primary pass criterion | Seeded workbench benchmark enters formal reporting with quality metrics; external adapted packs have provenance protocol and remain diagnostic unless promoted by explicit gates. |
| Veto diagnostics | Proxy metrics promoted to proof/release/scientific claims; unapproved network/download; external diagnostic cases made release-gating; missing source provenance; hidden dirty-worktree dependency. |
| Explanatory diagnostics | Local tests, benchmark reports, quality scorecards, manifest validation, Claude read-only review, and ledger entries. |
| Not concluded | Release readiness, external leaderboard performance, broad theorem-proving capability, or scientific validity. |
| Artifacts | Master program, phase subplans/results, ledger, review trail, benchmark code/tests/docs, final handoff. |

## Seeded-Gate Promotion Thresholds

Phase 6 may integrate the seeded workbench category into formal gated totals
only after Phase 3 records:

- complete new-tool coverage;
- required oracle-class coverage;
- at least 40% negative-control or false-confidence cases;
- hidden-assumption and notation-conflict traps for relevant workflow groups;
- deterministic rerun with stable case ids/results;
- fixed mutation family detection for unavailable-backend, structural-only,
  numeric-support, and missing-assumption proof-promotion errors;
- complete run manifest and scoring-rubric version.

If any threshold fails, the seeded category remains non-gating until repaired.

## External Reporting Rule

External adapted packs are reported by source family and oracle class only. They
must not be combined with seeded formal totals or used for cross-source ranking,
leaderboard, release, or product-capability claims.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Seeded local benchmark first | Current deterministic repo tests | Enables CI-safe progress before external source handling | Synthetic overfit | Negative-control and mutation-sensitivity metrics | Reviewed baseline |
| External packs diagnostic first | User license statement plus evidence policy | Avoids premature release-gate or leaderboard claims | Diagnostic status lingers | Promotion criteria in Phase 6 | Reviewed default |
| No downloads at launch | Sandbox/network policy | Allows visible execution to start | Phase 5 may block | Source availability precheck | Convenience choice |
| Claude read-only review | User instruction | Independent plan critique | Hangs or oversteps | Compact prompt/probe/max 5 loops | Reviewed default |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

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
