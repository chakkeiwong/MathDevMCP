# MathDevMCP Derivation Audit/Proposal Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This visible runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

A separate detached/overnight launch plan exists for approval-gated detached
execution:

- `docs/plans/mathdevmcp-derivation-audit-proposal-gated-overnight-execution-plan-2026-07-06.md`

## Quiet Visible Execution Pattern

Full command output is an artifact, not chat content. For large commands,
predeclare a log path under `docs/plans/logs`, redirect stdout/stderr there,
and summarize only exit status, artifacts, and bounded failure tails.

For short focused tests, direct output in the current conversation is allowed.

## Program

Master program:

- `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`

Reviewed plan artifacts:

- `docs/reviews/mathdevmcp-derivation-audit-proposal-plan-review-bundle.md`

Execution ledger:

- `docs/plans/mathdevmcp-derivation-audit-proposal-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/mathdevmcp-derivation-audit-proposal-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline, Schema, Review Gate | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-subplan-2026-07-06.md` | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-result-2026-07-06.md` |
| 1 | Derivation Gap/Proposal Builder | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-subplan-2026-07-06.md` | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md` |
| 2 | Rich Direct `derive_from` | To be refreshed before Phase 2 | Phase 2 result |
| 3 | Source-Aware Derivation Report | To be refreshed before Phase 3 | Phase 3 result |
| 4 | Backend Discipline And Assumption Integration | To be refreshed before Phase 4 | Phase 4 result |
| 5 | CLI/MCP Parity | To be refreshed before Phase 5 | Phase 5 result |
| 6 | Real-Document Experiment | To be refreshed before Phase 6 | Phase 6 result |
| 7 | Final Review And Handoff | To be refreshed before Phase 7 | Phase 7 result |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the derivation audit/proposal lane be built in visible gated phases without overclaiming derivation proof or reviewer authority? |
| Baseline/comparator | Current high-level derivation tools and assumptions report reference behavior. |
| Primary pass criterion | Each phase passes its subplan criteria, writes a result artifact, and preserves proof/refutation boundaries. |
| Veto diagnostics | Diagnostic evidence promoted to proof, hidden detached launch, no stop condition, unsupported Markdown claims, backend absence treated as failure of math. |
| Explanatory diagnostics | Review status, test counts, generated report length, proposal counts. |
| Not concluded | No release readiness, no general theorem proving, no scientific validation. |
| Artifacts | Phase subplans/results, ledger, review bundles/logs, tests, generated reports. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution first | Review template | Keeps Codex supervisor in current conversation | User expected detached overnight execution | Separate detached plan with approval gate | Reviewed |
| Claude Opus max-effort as reviewer | User request | Independent bounded review | Timeout or no verdict | Review gate probe and Codex fallback record | Reviewed |
| Phase-by-phase subplans | User request and project policy | Prevents broad unreviewed implementation | Planning overhead slows progress | Phase 0 only writes enough for Phase 1 execution | Reviewed |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
the ledger. Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
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
   - Restate the evidence contract.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write the required phase result artifact.
4. `PASS_REVIEW`
   - Send material plans/results/diffs to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch visibly, rerun focused checks, and retry
     review as needed.
   - Stop after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write a handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Claude Read-Only Review Template

Use Claude only as reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <phase result / blocker plan / implementation diff / final decision>

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting hardware-specific results without trusted-context evidence;
- launching detached overnight execution without explicit approval;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
