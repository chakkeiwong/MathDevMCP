# MathDevMCP Real-Task Master Visible Gated Execution Plan

Date: `2026-06-28`

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus/max is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

This is a visible gated execution plan for potentially long-running work inside
the current conversation. It is not a detached overnight supervisor.

Claude cannot authorize crossing human, runtime, model-file, funding,
product-capability, policy, or scientific-claim boundaries.

## Program

Master program:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-audit-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-master-claude-review-trail-2026-06-28.md`

Execution ledger:

- `docs/plans/mathdevmcp-real-tasks-master-visible-execution-ledger-2026-06-28.md`

Stop handoff:

- `docs/plans/mathdevmcp-real-tasks-master-visible-stop-handoff-2026-06-28.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Program framing and governance | `docs/plans/mathdevmcp-real-tasks-master-phase-00-governance-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-00-governance-result-2026-06-28.md` |
| 1 | Category contracts and scoring rules | `docs/plans/mathdevmcp-real-tasks-master-phase-01-category-scoring-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-01-category-scoring-result-2026-06-28.md` |
| 2 | Public corpus buildout | `docs/plans/mathdevmcp-real-tasks-master-phase-02-public-corpus-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-02-public-corpus-result-2026-06-28.md` |
| 3 | Holdout-local corpus design | `docs/plans/mathdevmcp-real-tasks-master-phase-03-holdout-local-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-03-holdout-local-result-2026-06-28.md` |
| 4 | Private/external corpus design | `docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-result-2026-06-28.md` |
| 5 | Schema, loader, and validator hardening | `docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-result-2026-06-28.md` |
| 6 | Non-gating reporting | `docs/plans/mathdevmcp-real-tasks-master-phase-06-non-gating-reporting-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-06-non-gating-reporting-result-2026-06-28.md` |
| 7 | Pilot execution and calibration | `docs/plans/mathdevmcp-real-tasks-master-phase-07-pilot-calibration-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-07-pilot-calibration-result-2026-06-28.md` |
| 8 | Workflow integration | `docs/plans/mathdevmcp-real-tasks-master-phase-08-workflow-integration-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-08-workflow-integration-result-2026-06-28.md` |
| 9 | Gate-candidate selection | `docs/plans/mathdevmcp-real-tasks-master-phase-09-gate-candidate-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-09-gate-candidate-result-2026-06-28.md` |
| 10 | Release-policy integration | `docs/plans/mathdevmcp-real-tasks-master-phase-10-release-policy-subplan-2026-06-28.md` | `docs/plans/mathdevmcp-real-tasks-master-phase-10-release-policy-result-2026-06-28.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the MathDevMCP real-task benchmark master program be executed phase by phase with visible gates, repair loops, and boundary-safe handoffs? |
| Baseline/comparator | Master program, prior audit, current synthesis docs, live local report/scoring checks. |
| Primary pass criterion | Each phase either passes its subplan gate and writes a result, or stops with a blocker result before crossing a human/policy/scientific boundary. |
| Veto diagnostics | Proxy metrics promoted to readiness, local holdout treated as public evidence, fixture scoring treated as workflow performance, hidden private/external access assumption, gate/release movement without human approval. |
| Explanatory diagnostics | Case counts, scored coverage, family mix, test pass/fail summaries, Claude review findings. |
| Not concluded | Benchmark completion, holdout-backed generalization, semantic maturity, workflow/gate/release readiness, mathematical/scientific validation. |
| Artifacts | Phase subplans/results, ledger, Claude review trail, stop handoff, local check outputs summarized in result notes. |

Local tests, mechanical section checks, `git diff --check`, and live summaries
are non-promoting diagnostics. They can support phase-local infrastructure or
document consistency only; they do not establish benchmark validity,
generalization, workflow readiness, release suitability, or scientific claims.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution in current conversation | Runbook template | Preserves recoverability and user visibility | Detached work could cross boundaries silently | Confirm no detached supervisor commands are used | Reviewed default |
| Claude as read-only reviewer | User instruction and global policy | Adds skeptical review without delegating execution | Claude treated as authority or edits/runs commands | Prompt requires read-only and exact verdict; preserve trail | Reviewed default |
| Opus/max for material reviews | User instruction | Higher-effort review for material subplans | Long prompts trigger approval blocks or stale context | Send bounded excerpts/artifact lists, not whole long files | Reviewed default |
| Existing local holdout artifacts may exist | Reset memo and live scoring | Needed for local-only calibration summaries | Local evidence could be mistaken as public | Policy boundary in each result note | Baseline |
| No automatic policy movement | Master program phases 8-10 | Prevents premature gate/release coupling | Late phases could be executed as if already approved | Human-required stop conditions in phases 9-10 | Reviewed default |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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
   - Re-verify current branch/worktree status, artifact existence, test target
     names, and whether upstream phase outputs changed since the subplan was
     written.
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
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker and write a
     blocker handoff with unresolved questions, blocked artifact IDs, owning
     human decision, and the earliest prior phase that must be reopened.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Prompt Rules

Use Claude only as a reviewer. Do not send whole long files. Send:

- the phase objective;
- relevant excerpt line ranges or compact summaries;
- artifact paths;
- checks run;
- specific concerns.

If Claude does not respond:

1. run a tiny read-only probe;
2. if the probe responds, redesign the prompt to be shorter and more bounded;
3. if the probe fails, record a blocker and request approval or human direction.

Claude review prompt must end with:

```text
End with exactly:
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
- interpreting GPU/special hardware results without trusted-context evidence;
- adding or activating workflow/gate/release policy authority;
- continuing after Claude and Codex do not converge after five review rounds.

If stopping after five Claude review rounds, the stop handoff must include:

- unresolved question list;
- blocked artifact IDs;
- owning human decision;
- earliest prior phase that must be reopened;
- focused checks already rerun;
- what remains forbidden to conclude.

## Launch Criteria

The plan may launch Phase 0 only after:

- all subplans exist;
- the ledger, review trail, and stop handoff exist;
- local setup checks pass;
- Claude read-only review of the plan/subplan index returns `VERDICT: AGREE`
  or all fixable findings have been repaired with focused checks rerun.

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
