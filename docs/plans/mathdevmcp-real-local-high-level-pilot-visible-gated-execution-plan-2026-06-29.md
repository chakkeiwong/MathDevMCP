# MathDevMCP Real-Local High-Level Pilot Visible Gated Execution Plan

Date: 2026-06-29

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

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

- `docs/plans/mathdevmcp-real-local-high-level-pilot-master-program-2026-06-29.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-real-local-high-level-pilot-claude-review-trail-2026-06-29.md`

Execution ledger:

- `docs/plans/mathdevmcp-real-local-high-level-pilot-visible-execution-ledger-2026-06-29.md`

Stop handoff:

- `docs/plans/mathdevmcp-real-local-high-level-pilot-visible-stop-handoff-2026-06-29.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Source Boundary | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-00-governance-source-boundary-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-00-governance-source-boundary-result-2026-06-29.md` |
| 1 | Manifest And Case Contract | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-result-2026-06-29.md` |
| 2 | Loader, Runner, And Scoring | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-02-loader-runner-scoring-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-02-loader-runner-scoring-result-2026-06-29.md` |
| 3 | Pilot Calibration And Reports | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-03-calibration-report-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-03-calibration-report-result-2026-06-29.md` |
| 4 | CLI, Docs, And Non-Gating Integration | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-04-cli-docs-integration-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-04-cli-docs-integration-result-2026-06-29.md` |
| 5 | Final Regression And Handoff | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-result-2026-06-29.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP construct and execute a five-case local real-source high-level workflow pilot without overclaiming? |
| Baseline/comparator | Current high-level workflow tests/benchmark quality plus the real-local pilot inventory. |
| Primary pass criterion | All phases pass their local gates; five cases are represented, executable probes run deterministically, scoring preserves evidence boundaries, and final handoff records non-claims. |
| Veto diagnostics | Source exfiltration, probe pass treated as full proof, local pilot treated as benchmark-gate evidence, Claude treated as authority, release/scientific claims. |
| Explanatory diagnostics | Manifest validation, unit tests, pilot report, seeded high-level quality report, benchmark gate where safe, Claude review trail. |
| Not concluded | Release readiness, external benchmark validity, public redistributability, scientific validity, broad theorem proving. |
| Artifacts | Master program, subplans/results, manifest, code/tests/docs, pilot report, ledger, review trail, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | Template and user recovery needs | Keeps state observable after reboots/interruptions | Longer than detached automation | Ledger and phase results | Reviewed default |
| Five selected cases | Pilot inventory recommendation | Focused first slice | Overgeneralization | Non-claims and future-work handoff | Reviewed baseline |
| Separate source obligation and executable probe | Current workflow capability boundary | Avoids fake full derivation proof | Probe pass overclaimed | Manifest schema and scoring non-claims | Reviewed default |
| Local/holdout tier | Sibling repo provenance | Avoids public fixture decision | CI/public confusion | Path validation and docs wording | Reviewed default |
| Claude read-only compact review | User instruction | Independent critique | Prompt block/hang | Probe and smaller prompt loop | Reviewed default |
| Dual-channel report schema | Claude review R1 | Source obligations and executable probes are different evidence channels | Blended accuracy number misleads operators | Separate source/probe/adapter ledgers | Reviewed default |
| Known-bad scorer tests | Claude review R1 | Boundary checks need adversarial tests | Happy-path tests miss false-confidence promotion | Must-fail fixtures in Phase 2 | Reviewed default |

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

Global stop gates:

- local vs public source-tier ambiguity;
- executable probes cannot be separated from full-source claims;
- any phase tries to add pilot results to benchmark-gate totals;
- any phase emits a single aggregate pilot accuracy metric that blends source
  obligations and executable probes;
- any output implies release readiness, external benchmark validity, broad
  theorem proving, proof-by-prose, or scientific validation.

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
   - Advance only after the current phase gate passes.
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

If Claude does not respond, run a small probe. If the probe responds, redesign
the prompt and retry smaller. Claude silence is never approval; the probe is
only a liveness/debugging action. After five failed repair/review rounds for
the same blocker, write a blocked-phase result and failure packet, then stop.
Claude is never an execution authority.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed program;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default release or benchmark policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
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
