# MathDevMCP Real-Local Source Adapters Visible Gated Execution Plan

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

Execution is visible and recoverable inside the current conversation.

## Program

Master program:

- `docs/plans/mathdevmcp-real-local-source-adapters-master-program-2026-06-29.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-real-local-source-adapters-claude-review-trail-2026-06-29.md`

Execution ledger:

- `docs/plans/mathdevmcp-real-local-source-adapters-visible-execution-ledger-2026-06-29.md`

Stop handoff:

- `docs/plans/mathdevmcp-real-local-source-adapters-visible-stop-handoff-2026-06-29.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Source Freeze | `docs/plans/mathdevmcp-real-local-source-adapters-phase-00-governance-source-freeze-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-00-governance-source-freeze-result-2026-06-29.md` |
| 1 | Source Packet Extraction | `docs/plans/mathdevmcp-real-local-source-adapters-phase-01-source-packet-extraction-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-01-source-packet-extraction-result-2026-06-29.md` |
| 2 | Math IR And Notation Normalization | `docs/plans/mathdevmcp-real-local-source-adapters-phase-02-math-ir-notation-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-02-math-ir-notation-result-2026-06-29.md` |
| 3 | IFT Sign Adapter | `docs/plans/mathdevmcp-real-local-source-adapters-phase-03-ift-sign-adapter-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-03-ift-sign-adapter-result-2026-06-29.md` |
| 4 | Kalman Likelihood Adapter | `docs/plans/mathdevmcp-real-local-source-adapters-phase-04-kalman-likelihood-adapter-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-04-kalman-likelihood-adapter-result-2026-06-29.md` |
| 5 | Joseph Equivalence Adapter | `docs/plans/mathdevmcp-real-local-source-adapters-phase-05-joseph-equivalence-adapter-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-05-joseph-equivalence-adapter-result-2026-06-29.md` |
| 6 | Affine Recursion Adapter | `docs/plans/mathdevmcp-real-local-source-adapters-phase-06-affine-recursion-adapter-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-06-affine-recursion-adapter-result-2026-06-29.md` |
| 7 | Kalman Score Adapter | `docs/plans/mathdevmcp-real-local-source-adapters-phase-07-kalman-score-adapter-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-07-kalman-score-adapter-result-2026-06-29.md` |
| 8 | Source Obligation Scorer | `docs/plans/mathdevmcp-real-local-source-adapters-phase-08-source-obligation-scorer-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-08-source-obligation-scorer-result-2026-06-29.md` |
| 9 | CLI Docs And Non-Gating Integration | `docs/plans/mathdevmcp-real-local-source-adapters-phase-09-cli-docs-integration-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-09-cli-docs-integration-result-2026-06-29.md` |
| 10 | Final Regression And Handoff | `docs/plans/mathdevmcp-real-local-source-adapters-phase-10-final-regression-handoff-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-real-local-source-adapters-phase-10-final-regression-handoff-result-2026-06-29.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP complete bounded source-linked adapters for the five local high-level pilot obligations while preserving evidence boundaries? |
| Baseline/comparator | Completed real-local pilot with five passing executable probes and five adapter-required source obligations. |
| Primary pass criterion | All phases pass; final source-adapter report has five source results, zero residual adapter-required gaps under this local source-obligation schema, separate source/probe ledgers, no aggregate accuracy, and per-case clearance evidence containing source anchors, required-term coverage, adapter route, deterministic checks, and non-claims. |
| Veto diagnostics | Source exfiltration, hard-coded unsupported conclusions, probe promoted to source proof, adapter-required cleared by probe/test/benchmark success, frozen provenance drift, report added to benchmark gate, release/scientific/broad proof claims. |
| Explanatory diagnostics | Packet/IR validation, per-adapter tests, CLI reports, high-level workflow quality, benchmark-gate observation, Claude review trail. These are engineering/regression diagnostics only except for explicitly scoped adapter pass criteria. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, external reproducibility, full LaTeX proof checking, broad theorem proving. |
| Artifacts | Program docs, subplans/results, source adapter code/tests, reports, ledger, review trail, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | Template and reboot recovery needs | Keeps state observable | Longer than detached automation | Ledger and phase results | Reviewed default |
| Five selected cases | Completed pilot handoff | Directly closes known gap | Overgeneralization | Final non-claims | Reviewed baseline |
| Local sibling paths | User-provided source inventory | Real examples without public copy decision | Portability confusion | Local-only docs and path validation | Reviewed default |
| Rule/domain adapters | Current bounded-tool architecture | Deterministic, testable first step | Pattern matching overclaimed | Mutation tests and non-claims | Hypothesis with diagnostics |
| Separate ledgers | Pilot policy | Avoids false blended accuracy | Misread by operators | Tests and docs grep | Reviewed default |
| Claude read-only compact review | User and policy | Independent critique | Prompt block or silence | Probe and smaller retry | Reviewed default |
| Packet caps | Review R1 | Prevent source overcapture | Needed context exceeds cap | Stop/escalate instead of widening silently | Reviewed default |
| Drift guard | Review R2 | Prevent mixed-state source evidence | Worktree changes mid-run | Hash/provenance checks and blocked result | Reviewed default |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in the execution
ledger. The audit must check wrong baseline, proxy metrics promoted to pass
criteria, missing stop conditions, unfair comparisons, hidden assumptions, stale
context, environment mismatch, and commands whose artifacts would not answer
the phase question.

The drift guard and adapter-clearance rule are mandatory launch gates, but they
do not replace the full phase evidence contract. Each phase precheck must name:

- baseline/comparator;
- primary pass criterion;
- veto diagnostics;
- stop conditions;
- artifact provenance;
- non-claims.

## Pre-Launch Blocking Checklist

Before Phase 00 execution starts, Codex must verify and record:

- the completed pilot baseline is still five selected cases, five passing
  executable probes, five source obligations marked `adapter_required`, and
  `aggregate_accuracy: None`;
- no reviewed planning blocker remains open in the Claude review trail, except
  for an explicitly written blocker result accepted by the user;
- the manifest path, selected case ids, source line anchors, and local-only
  source policy are ready to be frozen in Phase 00;
- Phase 01 packet caps and Phase 02 source/probe/residual channel separation
  are required gates before any domain adapter can clear a case;
- `adapter_required` clearance is defined only by source-anchored local-schema
  checks over bounded packets, never by probes, tests, benchmark gate,
  confidence, or absence of blockers;
- no command requires package installation, network fetch, credentials,
  model-file changes, neighboring-repo edits, destructive git/filesystem
  actions, release-gate changes, or public benchmark promotion.

If any item fails, do not launch. Write a blocked/partial result and stop for
human direction.

Global stop gates:

- source/probe/adapter channels cannot be kept separate;
- local source text would need to be copied wholesale;
- a bounded adapter cannot close a case without broader semantic judgment or
  more context than the packet cap allows;
- manifest hash, selected case ids, source line anchors, packet content hashes,
  or repo commit/dirty provenance drift after capture;
- a phase attempts to change release/benchmark-gate policy;
- adapter result lacks source anchors or deterministic checks;
- `adapter_required` would be cleared by executable-probe success, absence of
  blockers, adapter confidence, `pytest`, high-level quality, or benchmark-gate
  outcomes rather than a source-anchored local-schema check;
- output implies release readiness, external benchmark validity, full LaTeX
  proof checking, scientific validation, or broad theorem proving.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the evidence contract.
   - Append a ledger entry with skeptical audit.
2. `EXECUTE_MINIMAL`
   - Run visible local commands in the current conversation.
   - Implement only the smallest change needed for the phase.
   - Use local-only source files and local deterministic checks; do not use
     network/model output for adapter execution or certification.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs with the primary criterion and veto diagnostics.
   - Write the phase result artifact.
4. `PASS_REVIEW`
   - Use Claude read-only review for material subplans/results.
   - Continue only after `VERDICT: AGREE`, or repair and retry.
5. `REPAIR_LOOP`
   - Patch fixable problems visibly.
   - Rerun focused checks.
   - Update result/review artifacts.
   - Stop after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write handoff if a human-required boundary appears.

## Claude Read-Only Review Template

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review this compact brief, not whole files:
- phase/program:
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
artifact mismatch, and source/probe boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run a tiny probe. If the probe responds, redesign
the prompt and retry smaller. Claude silence is never approval.

## Human-Required Stop Conditions

Stop if continuing would require:

- project-direction change not already in the reviewed program;
- package installation, network fetch, credentials, or model-file changes;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- changing default release or benchmark policy;
- modifying unrelated dirty user work;
- editing neighboring repositories;
- continuing after Claude/Codex do not converge after five rounds.

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
