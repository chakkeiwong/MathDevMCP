# Real-Local High-Level Workflow Benchmark Closure Visible Gated Execution Plan

Date: 2026-06-30

## Status

`REVISED_AFTER_CLAUDE_R1`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only where tenant policy permits
repo-artifact review.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Execution is visible and recoverable inside the current conversation.

## Program

Master program:

- `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-master-program-2026-06-30.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-claude-review-trail-2026-06-30.md`

Execution ledger:

- `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-visible-execution-ledger-2026-06-30.md`

Stop handoff:

- `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-visible-stop-handoff-2026-06-30.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Current Baseline | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-00-governance-current-baseline-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-00-governance-current-baseline-result-2026-06-30.md` |
| 1 | Real Local Case Inventory | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-01-real-local-case-inventory-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-01-real-local-case-inventory-result-2026-06-30.md` |
| 2 | Benchmark Schema And Rubric | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-02-benchmark-schema-rubric-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-02-benchmark-schema-rubric-result-2026-06-30.md` |
| 3 | Backend Grounding Evidence Layer | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-03-backend-grounding-evidence-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-03-backend-grounding-evidence-result-2026-06-30.md` |
| 4 | Current Workflow Baseline Run | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-04-current-workflow-baseline-run-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-04-current-workflow-baseline-run-result-2026-06-30.md` |
| 5 | Targeted Capability Repairs | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-05-targeted-capability-repairs-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-05-targeted-capability-repairs-result-2026-06-30.md` |
| 6 | Derivation And Proof Packet Standard | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-06-derivation-proof-packet-standard-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-06-derivation-proof-packet-standard-result-2026-06-30.md` |
| 7 | Promotion Policy And Operator Docs | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-07-promotion-policy-operator-docs-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-07-promotion-policy-operator-docs-result-2026-06-30.md` |
| 8 | Final Regression And Handoff | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-08-final-regression-handoff-subplan-2026-06-30.md` | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-08-final-regression-handoff-result-2026-06-30.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP close the gap between seeded high-level workflow tests and realistic local derivation/proof tasks? |
| Baseline/comparator | Completed seeded high-level workflow program plus source-adapter Phase 11 addendum; no real-local high-level benchmark closure yet. |
| Primary pass criterion | A real-local benchmark exists, current baseline is measured, targeted repairs are driven by observed failures, final reports preserve boundaries, and non-claims are explicit. |
| Veto diagnostics | LLM prose treated as proof; backend absence treated as refutation; source/probe/backend/residual ledgers collapsed; source text overcopied; benchmark success promoted to release/scientific/public validity; aggregate score hides wrong/boundary-violating cases; phase artifact does not answer the phase question; local closure promoted to default policy. |
| Explanatory diagnostics | Case inventory, benchmark quality metrics, focused tests, CLI reports, per-case workflow reports, negative controls, mutation probes, docs grep, review trail. |
| Not concluded | Release readiness, public benchmark validity, scientific validation, production implementation correctness, external reproducibility, full LaTeX proof checking, or broad theorem proving. |
| Artifacts | Master program, subplans/results, ledger, review trail, benchmark manifest/report, code/tests/docs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution only | Template and prior reboot recovery | Keeps state observable | Slower than detached automation | Ledger and phase results | Reviewed default |
| 5-10 real-local cases | User request | Enough for concrete capability signal without unbounded crawl | Cherry-picking | Coverage table and negative controls | Baseline target |
| Benchmark before repairs | Scientific coding policy | Prevents speculative repairs | Baseline may look rough | Phase 4 diagnostic report | Reviewed default |
| Local/non-gating by default | Source-adapter policy | Avoids public/release overclaim | Useful cases remain non-public | Phase 7 promotion policy | Reviewed default |
| Claude compact review | User request | Independent critique | Tenant policy block | Sanitized prompts and recorded blocker | Conditional |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the ledger. The audit must check:

- wrong baseline;
- proxy metrics being promoted to pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Pre-Launch Blocking Checklist

Before Phase 00 execution starts, verify:

- the predecessor high-level workflow handoff exists and is read as seeded
  benchmark completion, not real-local closure;
- the source-adapter Phase 11 addendum exists and remains local/non-gating;
- no plan claims release readiness, public benchmark validity, scientific
  validity, production implementation correctness, or broad theorem proving;
- phase subplans exist for Phases 00-08 with required artifacts, checks,
  evidence contracts, forbidden actions, handoffs, and stop conditions;
- mandatory cross-phase artifacts are required: baseline freeze manifest,
  coverage matrix, minimal packet schema, route-availability ledger,
  workflow-family evidence contracts, anti-overfitting rerun set, and final
  per-case matrix;
- no command requires package installation, network fetch, credentials,
  model-file changes, neighboring-repo edits, destructive git/filesystem
  actions, release-gate changes, or public benchmark promotion.

If any item fails, do not launch. Write a blocked result and stop.

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
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs with primary criterion and veto diagnostics.
   - Write the phase result artifact.
4. `PASS_REVIEW`
   - Use Claude read-only review for material subplans/results where permitted.
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
- claiming scientific, product, release, or public benchmark capability beyond
  local evidence;
- claiming abstention quality is calibrated outside the benchmarked local
  cases;
- promoting local closure to default policy without a separate governed
  decision artifact;
- accepting an artifact that does not answer the phase question;
- continuing after Claude/Codex do not converge after five review rounds when
  Claude review is required.

## Claude Review Trail

- R1 verdict: `REVISE`.
- R1 repairs applied in the master/runbook/subplans before launch.

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
