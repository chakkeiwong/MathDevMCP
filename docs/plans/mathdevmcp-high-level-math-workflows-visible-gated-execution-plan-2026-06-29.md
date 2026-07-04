# MathDevMCP High-Level Math Workflows Visible Gated Execution Plan

Date: `2026-06-29`

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

- `docs/plans/mathdevmcp-high-level-math-workflows-master-program-2026-06-29.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-high-level-math-workflows-claude-review-trail-2026-06-29.md`

Execution ledger:

- `docs/plans/mathdevmcp-high-level-math-workflows-visible-execution-ledger-2026-06-29.md`

Stop handoff:

- `docs/plans/mathdevmcp-high-level-math-workflows-visible-stop-handoff-2026-06-29.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline | `docs/plans/mathdevmcp-high-level-math-workflows-phase-00-governance-baseline-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-00-governance-baseline-result-2026-06-29.md` |
| 1 | Contract And Evidence Schema | `docs/plans/mathdevmcp-high-level-math-workflows-phase-01-contract-evidence-schema-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-01-contract-evidence-schema-result-2026-06-29.md` |
| 2 | Orchestration Kernel | `docs/plans/mathdevmcp-high-level-math-workflows-phase-02-orchestration-kernel-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-02-orchestration-kernel-result-2026-06-29.md` |
| 3 | Derive From Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-03-derive-from-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-03-derive-from-result-2026-06-29.md` |
| 4 | Prove Or Counterexample Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-04-prove-or-counterexample-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-04-prove-or-counterexample-result-2026-06-29.md` |
| 5 | Assumptions For Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-05-assumptions-for-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-05-assumptions-for-result-2026-06-29.md` |
| 6 | Debug Derivation Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-06-debug-derivation-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-06-debug-derivation-result-2026-06-29.md` |
| 7 | Audit Math To Code Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-07-audit-math-to-code-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-07-audit-math-to-code-result-2026-06-29.md` |
| 8 | Prepare Review Packet Workflow | `docs/plans/mathdevmcp-high-level-math-workflows-phase-08-prepare-review-packet-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-08-prepare-review-packet-result-2026-06-29.md` |
| 9 | Question-Level Benchmark | `docs/plans/mathdevmcp-high-level-math-workflows-phase-09-question-level-benchmark-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-09-question-level-benchmark-result-2026-06-29.md` |
| 10 | CLI And MCP Exposure | `docs/plans/mathdevmcp-high-level-math-workflows-phase-10-cli-mcp-exposure-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-10-cli-mcp-exposure-result-2026-06-29.md` |
| 11 | Docs And Operator UX | `docs/plans/mathdevmcp-high-level-math-workflows-phase-11-docs-operator-ux-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-11-docs-operator-ux-result-2026-06-29.md` |
| 12 | Final Regression And Handoff | `docs/plans/mathdevmcp-high-level-math-workflows-phase-12-final-regression-handoff-subplan-2026-06-29.md` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-12-final-regression-handoff-result-2026-06-29.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP add benchmarked high-level mathematical workflows for common derivation/proof/assumption/debug/code-review questions without overclaiming? |
| Baseline/comparator | Existing low-level workbench tools, formal benchmark gate, and workbench benchmark quality report. |
| Primary pass criterion | High-level workflows share a stable contract, pass focused tests, pass question-level benchmark quality thresholds, and are exposed through CLI/MCP only after benchmark pass. |
| Veto diagnostics | LLM/prose treated as proof; backend unavailable treated as refutation; numeric/structural/generated-test evidence promoted to proof; benchmark pass rate used as sole quality signal; public surfaces exposed before benchmark pass. |
| Explanatory diagnostics | Unit tests, benchmark totals, quality report, mutation probes, CLI/MCP tests, docs grep, and ledger entries. |
| Not concluded | General theorem proving, release readiness, external benchmark performance, scientific validity, or correctness beyond scoped evidence. |
| Artifacts | Master program, subplans/results, ledger, review trail, code/tests/docs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| High-level workflows are wrappers/orchestrators | Existing workbench primitives | Reuse tested backend/diagnostic semantics | Wrapper summary may overclaim | Contract tests and false-confidence traps | Reviewed baseline |
| Question-level benchmark before CLI/MCP | Prior workbench benchmark quality pattern | Prevents unbenchmarked public surface | Delays UX exposure | Phase 10 blocked on Phase 9 pass | Reviewed default |
| Seeded local benchmark first | Current repo has deterministic local fixtures | Avoids external source uncertainty | Synthetic overfit | Negative-control and mutation probes | Reviewed baseline |
| No external data fetch | Approval/network/provenance policy | Keeps execution local and visible | External benchmark adaptation remains future work | Docs and non-claims | Convenience choice |
| Claude read-only review | User instruction | Independent critique without delegating execution | Claude hang or prompt issue | Tiny probe, smaller prompt, max 5 rounds | Reviewed default |

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

- unresolved evidence-schema ambiguity after Phase 1;
- benchmark harness cannot distinguish diagnostic from certified evidence;
- benchmark cases lack adjudicable gold/rubric quality;
- backend-unavailable cases dominate the benchmark so promotion would be
  meaningless;
- any output implies release readiness, broad theorem proving, proof-by-prose,
  or proof by structural/numeric/generated-test/review-packet evidence.

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
