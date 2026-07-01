# Agent-Handoff Packet Standardization Visible Gated Execution Plan

Date: 2026-07-01

## Status

`LAUNCHED_WITH_HUMAN_CLAUDE_REVIEW_WAIVER`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Claude review was attempted before Phase 0, but the review and tiny probes
timed out. The user explicitly directed: "no claude review for this time".
For this visible execution window, Claude review gates are waived and replaced
by Codex-only skeptical review plus required local checks. This is not Claude
approval and does not relax any non-Claude boundary.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Execution is visible and recoverable inside the current conversation. If
detached overnight execution is desired, stop and write a separate detached
supervisor plan.

## Program

Master program:

- `docs/plans/mathdevmcp-agent-handoff-packet-standardization-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-agent-handoff-packet-standardization-claude-review-trail-2026-07-01.md`

Execution ledger:

- `docs/plans/mathdevmcp-agent-handoff-packet-standardization-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/mathdevmcp-agent-handoff-packet-standardization-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Inventory | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-00-governance-baseline-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-00-governance-baseline-result-2026-07-01.md` |
| 1 | Contract And Schema Standard | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-01-contract-schema-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-01-contract-schema-result-2026-07-01.md` |
| 2 | Reusable Builder And Validator | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-02-reusable-builder-validator-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-02-reusable-builder-validator-result-2026-07-01.md` |
| 3 | Workflow And Benchmark Integration | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-03-workflow-benchmark-integration-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-03-workflow-benchmark-integration-result-2026-07-01.md` |
| 4 | CLI, MCP, And Operator Docs | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-04-cli-mcp-docs-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-04-cli-mcp-docs-result-2026-07-01.md` |
| 5 | Regression And Agent-Usefulness Benchmark Hook | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-05-regression-agent-usefulness-benchmark-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-05-regression-agent-usefulness-benchmark-result-2026-07-01.md` |
| 6 | Final Decision And Handoff | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-06-final-decision-handoff-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-06-final-decision-handoff-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the provisional C-style packet be made into a reusable, tested, boundary-safe local standard for MathDevMCP high-level workflow handoffs? |
| Baseline/comparator | Existing `prepare_review_packet`, `math_review_packet`, durable benchmark packet report, and prior calibration decision. |
| Primary pass criterion | The run produces a reviewed contract and either implements/tests the local standard or writes a precise blocker; existing packet regressions are checked; final decision is bounded to actual artifacts. |
| Veto diagnostics | C-over-B overclaim; diagnostic packet treated as proof; schema change without gate; evidence lost into prose; source anchors/non-claims missing; formatting proxy treated as correctness; Claude used as worker/authority; unapproved downstream response collection. |
| Explanatory diagnostics | Field coverage checks, regression tests, packet completeness summaries, docs/interface checks, Claude read-only findings. |
| Not concluded | Mathematical truth of cases, release readiness, public benchmark validity, scientific validation, product capability, general model reliability, or universal packet optimality. |
| Artifacts | Master program, subplans/results, runbook, ledger, review trail, contract spec, implementation/tests if produced, regression outputs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| C-style packet as starting standard | Prior calibration final decision | Provisional local candidate with self-contained context | Misread as scored C-over-B win | Phase 0 records tie and non-claims | Provisional |
| Reusable module first | Existing packet construction lives in benchmark/report paths | Reduces duplication and clarifies contract | Too broad abstraction | Phase 1 contract and Phase 2 focused tests | Hypothesis |
| Preserve high-level envelope initially | Existing validators enforce fixed fields | Avoids broad behavior change | Parallel standard not integrated | Phase 3 gate | Reviewed default |
| Existing benchmark cases as regression | Local tests already cover durable packet fields | Feasible local evidence | Overfitting | Phase 5 non-gating scope | Baseline |
| Claude read-only review | User instruction and policy | Boundary critique | Treated as authority | Review trail and Codex assessment | Constraint |
| Visible execution only | Template | Recoverable, auditable execution | Not detached overnight | Ledger entries | Required |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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
   - Under the human Claude-review waiver, run Codex-only review of material
     phase plans, diffs, results, or final decisions.
   - If Claude review is re-enabled later, continue only after
     `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Codex-only review when material under the human Claude-review waiver.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use compact briefs rather than whole files.

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review this compact brief:
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
- collecting downstream model responses without explicit approval;
- using Claude as worker rather than read-only reviewer;
- continuing after five Codex review/repair rounds for the same blocker under
  the human Claude-review waiver, or after Claude/Codex do not converge after
  five review rounds if Claude review is re-enabled.

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
