# MathDevMCP Mission Gap Closure Visible Gated Execution Runbook

Date: 2026-07-04

## Status

`COMPLETE_LOCAL_CHECKS_AND_FINAL_READ_ONLY_REVIEW_AGREED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is an overnight-style gated plan in the sense that it is phase-gated,
quiet, restartable, and ledgered. It is executed visibly in the current
conversation.

## Quiet Visible Execution Pattern

For commands that may produce large output, full stdout/stderr should be a log
artifact and chat should receive a bounded summary.

Required pattern:

1. Predeclare log and structured artifact paths in the phase subplan or ledger.
2. Redirect full stdout/stderr to a log file when output is expected to be
   large.
3. Prefer commands that write JSON/Markdown/result artifacts directly.
4. After the command, report exit status, artifact paths, pass/fail fields, and
   at most the last 20-40 log lines on failure.
5. Poll bounded status commands for long-running work.
6. Treat excessive output as an execution-flow defect and repair the runbook or
   write a stop handoff if needed.

## Program

Master program:

- `docs/plans/mathdevmcp-mission-gap-closure-master-program-2026-07-04.md`

Reviewed plan artifacts:

- `docs/reviews/mathdevmcp-mission-gap-closure-program-review-bundle-2026-07-04.md`

Execution ledger:

- `docs/plans/mathdevmcp-mission-gap-closure-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/mathdevmcp-mission-gap-closure-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governed Launch | `docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-result-2026-07-04.md` |
| 1 | CLI/MCP Handoff Presentation | `docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-result-2026-07-04.md` |
| 2 | End-To-End Workflow | `docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-result-2026-07-04.md` |
| 3 | Realistic Case Coverage | `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-result-2026-07-04.md` |
| 4 | V2 Regression Guard | `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-result-2026-07-04.md` |
| 5 | Compatibility Policy | `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-result-2026-07-04.md` |
| 6 | Release Readiness Boundary | `docs/plans/mathdevmcp-mission-gap-closure-phase-06-release-readiness-boundary-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-06-release-readiness-boundary-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current conversation close the known MathDevMCP mission gaps through gated, visible product work? |
| Baseline/comparator | Current post-`agent_handoff` state and recorded local check/review result. |
| Primary pass criterion | Each phase meets its subplan evidence contract, writes a result, and advances only on explicit handoff conditions. |
| Veto diagnostics | Boundary weakening, benchmark-as-product drift, unapproved external/model/runtime crossing, destructive edits, hidden pass/fail changes, or missing result artifacts. |
| Explanatory diagnostics | Test output, CLI/MCP output shape, review notes, compatibility notes, v2 replay summaries. |
| Not concluded | No proof, semantic code correctness, release readiness, public benchmark validity, scientific validation, funding readiness, or model reliability. |
| Artifacts | Master program, phase subplans/results, ledger, stop handoff, review bundles/logs, tests and bounded outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use visible execution | Template under `~/python/claudecodex/docs/templates`. | Avoids detached authority and preserves recoverability. | Long phases may stall chat. | Bounded logs and stop handoff. | Reviewed default pending review |
| Codex executes; Claude reviews | User instruction and policy. | Keeps implementation authority with Codex. | Claude review mistaken for approval. | Result notes must record Claude as advisory only. | Reviewed default pending review |
| Start with CLI/MCP presentation | Current result's implementation next step. | Directly improves agent consumption. | Formatting-only change misses product value. | Phase 1 requires CLI/MCP tests and preserved boundaries. | Reviewed default pending review |
| Use v2 after product work | Mission charter and ledger. | Prevents optimizing benchmark first. | Regression checked late. | Phase 4 explicitly replays/adapts as guard. | Reviewed default pending review |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

Check:

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
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase plans/results/diffs to Claude as bounded read-only
     review bundles.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the same subplan/result visibly.
   - Rerun focused checks.
   - Rerun Claude review only for material issues.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

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

Use Claude only as a reviewer. The prompt must say:

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

Codex must preserve review artifacts and inspect whether Claude stayed within
the read-only role.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- new model/API response collection beyond approved read-only review gates;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
