# Downstream-Agent Usefulness Visible Gated Execution Plan

Date: 2026-07-01

## Status

`LAUNCHED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

Initial Claude plan review and tiny probe did not return usable output. This is
recorded as reviewer unavailable, not as approval. Phase 0 may launch under
Codex-only skeptical review plus required local checks. Later material phases
must retry Claude review or record reviewer unavailability before advancing.

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

- `docs/plans/mathdevmcp-downstream-agent-usefulness-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-claude-review-trail-2026-07-01.md`

Execution ledger:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-result-2026-07-01.md` |
| 1 | Usefulness Contract And Rubric | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-result-2026-07-01.md` |
| 2 | Case Corpus And Fixture Design | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-result-2026-07-01.md` |
| 3 | Prompt Harness And Collection Gate | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-result-2026-07-01.md` |
| 4 | Response Collection And Scoring | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-result-2026-07-01.md` |
| 5 | Failure Taxonomy And Capability Repairs | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-result-2026-07-01.md` |
| 6 | Regression And Promotion Decision | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-subplan-2026-07-01.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do MathDevMCP high-level workflow packets measurably improve downstream-agent task performance on governed local math tasks? |
| Baseline/comparator | Frozen A/B/C prompt conditions, existing high-level workflow benchmark, and prior packet-standard candidate artifacts. |
| Primary pass criterion | The visible execution either implements a governed usefulness benchmark with scored results and bounded decision, or stops with a precise blocker before crossing approval or evidence boundaries. |
| Veto diagnostics | Hidden retries; unapproved response collection; Claude as response worker; rubric changed after responses; malformed outputs replaced; aggregate-only promotion; packet proxy promoted to correctness; unsupported scientific/product/public claims. |
| Explanatory diagnostics | Prompt manifests, response manifests, score tables, failure taxonomy, backend evidence-class coverage, local tests, Claude read-only reviews. |
| Not concluded | Release readiness, public benchmark validity, scientific validation, product capability, broad theorem proving, general model reliability, or proof correctness beyond certified obligations. |
| Artifacts | Plan files, ledgers, review trail, contracts, fixtures, prompts, responses if approved, scoring reports, repair records, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| A/B/C comparison | Prior calibration | Directly targets usefulness delta | Too narrow to prove broad reliability | Phase 1 rubric and non-claims | Baseline |
| Local cases first | Existing benchmark policy | Auditable and feasible | Overfitting | Phase 2 diversity matrix | Baseline |
| One response per prompt by default | Prior calibration discipline | No hidden retries and bounded cost | Variance | Phase 4 diagnostic-only label unless replicated | Constraint |
| Claude read-only review | User instruction | Boundary critique | Treated as authority | Review trail | Constraint |
| Visible execution | Template | Recoverable and auditable | Not actually overnight detached | Ledger entries | Required |

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
   - Send material phase plans, results, repairs, diffs, or final decisions to
     Claude as compact read-only briefs.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
   - If Claude remains unavailable after a compact review and tiny probe,
     record reviewer unavailability and use Codex-only skeptical review only
     for phases that do not cross human approval, response collection,
     scoring, repair, final promotion, runtime, model-file, funding, product,
     or scientific-claim boundaries.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the active subplan or write a blocker plan.
   - Get Claude review when material.
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

- project-direction decision not already in the reviewed plan;
- collecting new downstream-agent/model responses without explicit approval;
- package installation, network fetch, credentials, or model-file changes;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing release/default benchmark policy;
- modifying unrelated dirty user work;
- copying substantial content from neighboring repositories rather than
  bounded summaries and provenance;
- using Claude as worker rather than read-only reviewer;
- claiming scientific, product, release, public benchmark, or general model
  reliability beyond local evidence;
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
