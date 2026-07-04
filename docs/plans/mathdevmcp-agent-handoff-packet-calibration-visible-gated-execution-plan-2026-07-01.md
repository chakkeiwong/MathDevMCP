# Agent-Handoff Packet Calibration Visible Gated Execution Plan

Date: 2026-07-01

## Status

`REVISED_AFTER_CLAUDE_R1`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Execution is visible and recoverable inside the current conversation. If
detached overnight execution is desired, stop and write a separate
detached-supervisor plan.

## Program

Master program:

- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-claude-review-trail-2026-07-01.md`

Execution ledger:

- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-00-governance-baseline-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-00-governance-baseline-result-2026-07-01.md` |
| 1 | Calibration Contract And Rubric | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-01-contract-rubric-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-01-contract-rubric-result-2026-07-01.md` |
| 2 | Prompt Fixture Generation | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-02-prompt-fixtures-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-02-prompt-fixtures-result-2026-07-01.md` |
| 3 | Response Collection Protocol | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-03-response-collection-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-03-response-collection-result-2026-07-01.md` |
| 4 | Scoring And Analysis | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-04-scoring-analysis-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-04-scoring-analysis-result-2026-07-01.md` |
| 5 | Contract Decision And Handoff | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-05-contract-decision-handoff-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-05-contract-decision-handoff-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do human-framed packets improve downstream agent next-step work compared with task-only and evidence-only prompts? |
| Baseline/comparator | `A_task_only` and `B_evidence_only` conditions on the same frozen five-case set. |
| Primary pass criterion | The program produces fair prompt fixtures, a frozen rubric, collected responses or a precise model-use blocker, and a local/non-gating comparison decision. |
| Veto diagnostics | Prompt leakage; unequal task/output/length/retry policy; C gets extra non-framing evidence beyond B; proxy metrics treated as promotion criteria; hidden retries; Claude used as worker; model responses collected without required approval; partial scoring after approval blocker; hard vetoes hidden by aggregates; release/public/scientific/model-reliability claims. |
| Explanatory diagnostics | Per-case scores, hard-veto counts, failure taxonomy, response provenance, Claude read-only review findings. |
| Not concluded | General model reliability, release readiness, public benchmark validity, scientific validation, product capability, proof correctness, or universal packet optimality. |
| Artifacts | Master program, phase subplans/results, ledger, review trail, contract/rubric, prompt fixtures, response manifest, scored table, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | Template | Preserves recoverability | Not truly detached overnight | Ledger and phase results | Reviewed default |
| Five cases | Prior packet calibration | Covers hard local modes | Too small to generalize | Non-claims in every result | Local sample |
| A/B/C prompts | User question and calibration design | Separates framing effect | Prompt leakage | Phase 2 leakage checks | Hypothesis |
| Claude read-only review | User instruction | Independent critique | Mistaken as authority | Review trail and Codex gate | Constraint |
| Stop before unapproved model runs | Cross-agent/model boundary | Avoids hidden cost/authority issues | Incomplete calibration until approval | Phase 3 approval gate | Required |

## Freeze And Fairness Requirements

Phase 0 records commit/dirty status, artifact hashes, generator command
provenance, and selected-case rationale.

Phase 1/2 enforce identical task skeleton, requested output sections, response
length band, retry/malformed-output policy, and B/C evidence parity, with C
adding human framing as the isolated intervention.

Phase 3 stops with a blocker if model-use approval is missing. No partial
scoring, surrogate interpretation, or fixture tweaking is allowed after an
approval blocker.

Phase 4 surfaces hard vetoes before any summary score. Soft dimensions cannot
override correctness, boundary, assumption, or overclaim failures.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the ledger.

Check:

- wrong baseline;
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
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review this compact brief, not whole files:
- program/phase:
- objective:
- baseline:
- artifacts:
- checks:
- evidence contract:
- forbidden claims/actions:
- handoff:
- stop conditions:

Check wrong baseline, proxy metrics, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim,
artifact mismatch, and boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run a tiny probe. If the probe responds, redesign
the prompt smaller. Claude silence is never approval.

## Human-Required Stop Conditions

Stop if continuing would require:

- project-direction change not already in the reviewed program;
- package installation, network fetch, credentials, or model-file changes;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- changing default release or benchmark policy;
- modifying unrelated dirty user work;
- editing neighboring repositories;
- claiming scientific, product, release, public benchmark, or general model
  reliability beyond local evidence;
- collecting downstream model responses without required approval;
- partial scoring, surrogate interpretation, or prompt tweaking after a
  model-use approval blocker;
- using Claude as worker rather than read-only reviewer;
- continuing after Claude/Codex do not converge after five review rounds when
  Claude review is required.

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
