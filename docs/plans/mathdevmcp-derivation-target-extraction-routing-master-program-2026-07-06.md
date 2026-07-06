# MathDevMCP Derivation Target Extraction And Backend Routing Master Program

Date: 2026-07-06

Status: `DRAFT_UNDER_REVIEW`

## Objective

Improve the derivation audit lane from full LaTeX block diagnostics to
small, source-localized derivation obligations that can be routed through
deterministic tools whenever possible.

The target workflow is:

```text
LaTeX label/direct target
  -> extracted equation/align-row obligations
  -> backend route plan
  -> derive_from / assumptions / counterexample / formalization evidence
  -> gap-linked proposals
  -> Markdown + agent handoff
```

## Mission Fit

This program is the next slice after:

- `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`
- `docs/reviews/risky-debt-derivation-gap-proposals.md`

The prior lane made reports useful and non-handwavy, but still routed whole
LaTeX proposition blocks. This program addresses that recorded limitation by
extracting smaller obligations such as `eq:risky-pricing`, `eq:foc-k`, and
`eq:foc-b`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP extract small derivation obligations from source labels and route them through deterministic tools without hallucinated proof claims? |
| Baseline/comparator | Current `audit_and_propose_derivations`, which routes full label blocks and records missing assumptions. |
| Primary pass criterion | Risky-debt v2 report groups extracted obligations under parent labels, preserves file/line provenance, records backend route plans, and never promotes diagnostics to proof. |
| Veto diagnostics | Malformed lhs/rhs extraction; missing source location; backend diagnostic reported as proof; route planner hides backend unavailability; report loses linked assumption repairs; generic `collect more evidence` proposals. |
| Explanatory diagnostics | Extracted target count, equation labels, backend route candidates, route statuses, validation status counts. |
| Not concluded | No proof of risky-debt note correctness; no automatic edits; no global theorem proving; no claim that assumptions are minimal or sufficient without backend closure. |
| Artifacts | Master program, phase subplans/results, review bundle/logs, target extractor, route planner, tests, v2 report. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Extract displayed equations and align rows first | Current LaTeX index has block text and equation rows | Smallest unit likely useful for backend routing | Row splitting may break multiline equations | Unit tests on risky-debt labels and synthetic fixtures | Reviewed default |
| Keep full block as fallback | Existing report behavior | Avoid losing coverage when extraction fails | Fallback may mask extractor weakness | Coverage field must count fallback targets separately | Reviewed default |
| Route planning is advisory | Existing backend boundary policy | Prevents route availability from becoming proof | Agents may read route candidate as proof attempt | Validation must say non-certifying unless backend certificate/counterexample exists | Reviewed default |
| Reuse `derive_from` for each extracted obligation | Existing rich packet behavior | Keeps proof/refutation boundaries centralized | Extracted target may still be not encodable | Tests require formalization proposal, not proof claim | Reviewed default |
| Use Claude only for read-only plan/result review | User request and review guide | Independent check without execution authority | External review unavailable or blocked | Record review gate status and Codex fallback when needed | Reviewed default |

## Skeptical Plan Audit

This plan has been audited before execution for:

- wrong baselines: baseline is current report behavior, not hoped-for proof;
- proxy metrics: target count is explanatory only, not success;
- missing stop conditions: every phase has stop conditions;
- unfair comparisons: v2 report must preserve or improve current report fields;
- hidden assumptions: extraction and routing boundaries are explicit;
- stale context: existing dirty worktree is preserved;
- environment mismatch: Lean/Sage may be unavailable and must be recorded;
- artifact mismatch: every implementation phase has tests and result artifacts.

Audit result: `PASSED_WITH_BOUNDARY`.

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| --- | --- | --- | --- | --- |
| 0 | Plan/Review Gate | Create reviewed plan artifacts and baseline checks. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-00-plan-review-subplan-2026-07-06.md` | Phase 0 result |
| 1 | Target Extraction | Extract equation/align-row obligations with provenance. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-01-target-extraction-subplan-2026-07-06.md` | Phase 1 result |
| 2 | Backend Route Planner | Build deterministic route planner and validation boundary. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-02-backend-route-planner-subplan-2026-07-06.md` | Phase 2 result |
| 3 | Report Integration | Route extracted targets through report workflow. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-03-report-integration-subplan-2026-07-06.md` | Phase 3 result |
| 4 | Risky-Debt V2 Experiment | Generate and inspect risky-debt v2 report. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-04-risky-debt-v2-experiment-subplan-2026-07-06.md` | Phase 4 result |
| 5 | Public Surface Regression | Preserve CLI/MCP parity and regression guards. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-05-public-surface-regression-subplan-2026-07-06.md` | Phase 5 result |
| 6 | Final Review/Handoff | Final review, reset memo, stop/next handoff. | `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-06-final-review-handoff-subplan-2026-07-06.md` | Phase 6 result |

## Claude Review Protocol

Claude is read-only reviewer only. Codex remains supervisor and executor.

Use a compact review bundle; do not send whole source files or the whole
repository. Review loops stop after five rounds for the same blocker.

If Claude is blocked or unavailable:

1. send a tiny probe through the review gate;
2. if the probe is alive, revise the prompt/bundle and retry;
3. if unavailable or external export is rejected, write a Codex fallback review
   and record that it is weaker than Claude review.

## Repair Loop

For every phase:

1. run local checks;
2. write phase result;
3. draft or refresh next subplan;
4. review next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. if a fixable issue is found, patch visibly and rerun focused checks;
6. stop only for a recorded stop condition.

## Approval Needs

Expected commands:

- local reads/writes under this repository;
- `python3 -m pytest ...`;
- `python3 -m compileall ...`;
- `git diff --check ...`;
- Claude review gate command requiring escalated/trusted permissions because it
  may use network/auth/model API access;
- optional detached overnight launch, requiring explicit user approval before
  running.

No dependency installation, network fetch, destructive git command, or source
document edit is planned.

## Program Stop Conditions

Stop and write a blocker result if:

- source extraction cannot preserve file/line provenance;
- extracted lhs/rhs is malformed enough to make reports misleading;
- route planner would have to present diagnostics as proof;
- Claude and Codex review do not converge after five rounds for the same
  blocker;
- continuing requires external installation, credentials, funding, or
  destructive state changes;
- user direction changes the scientific or product boundary.
