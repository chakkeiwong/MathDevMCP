# MathDevMCP Derivation Target Extraction Visible Gated Execution Runbook

Date: 2026-07-06

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This visible runbook does not launch detached or nested agents.

## Program

Master program:

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-master-program-2026-07-06.md`

Review bundle:

- `docs/reviews/mathdevmcp-derivation-target-extraction-routing-plan-review-bundle.md`

Execution ledger:

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Plan/Review Gate | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-00-plan-review-subplan-2026-07-06.md` | Phase 0 result |
| 1 | Target Extraction | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-01-target-extraction-subplan-2026-07-06.md` | Phase 1 result |
| 2 | Backend Route Planner | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-02-backend-route-planner-subplan-2026-07-06.md` | Phase 2 result |
| 3 | Report Integration | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-03-report-integration-subplan-2026-07-06.md` | Phase 3 result |
| 4 | Risky-Debt V2 Experiment | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-04-risky-debt-v2-experiment-subplan-2026-07-06.md` | Phase 4 result |
| 5 | Public Surface Regression | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-05-public-surface-regression-subplan-2026-07-06.md` | Phase 5 result |
| 6 | Final Review/Handoff | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-06-final-review-handoff-subplan-2026-07-06.md` | Phase 6 result |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can extracted target obligations and route plans make derivation reports more actionable without unsupported proof claims? |
| Baseline/comparator | Current full-block `audit_and_propose_derivations` report. |
| Primary pass criterion | V2 risky-debt report uses extracted obligations and route plans while preserving validation/non-claim boundaries. |
| Veto diagnostics | Malformed extraction, lost provenance, diagnostic promoted to proof, generic fixes, failed public-surface tests. |
| Explanatory diagnostics | Target counts, route plan status counts, validation counts. |
| Not concluded | Source correctness, source edits, release readiness, general theorem proving. |
| Artifacts | Plans, results, tests, v2 report, review records. |

## Skeptical Plan Audit Requirement

Before every phase, Codex records an audit for:

- wrong baselines;
- proxy metrics as pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, record evidence contract.
2. `EXECUTE_MINIMAL`: implement or run only the smallest needed action.
3. `ASSESS_GATE`: compare outputs to primary criterion/veto diagnostics.
4. `PASS_REVIEW`: use Claude read-only review for material subplans/results
   when available/approved; otherwise record Codex fallback.
5. `REPAIR_LOOP`: patch fixable issues, rerun focused checks, max five Claude
   rounds for same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate passes.

## Quiet Execution

Large command output should be redirected to a log artifact. Chat summaries
should include status, artifact paths, and bounded failure tails only.

## Human-Required Stop Conditions

Stop if continuing would require:

- external installs, network fetches, credentials, or funding;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- editing unrelated dirty user work;
- detached launch without explicit approval;
- Claude/Codex review non-convergence after five rounds.
