# MathDevMCP Derivation Audit/Proposal Master Program

Date: 2026-07-06

Status: `DRAFT_UNDER_REVIEW`

## Objective

Build an agent-consumable high-level derivation lane for questions of the form:

```text
Can we derive TARGET from givens, assumptions, or source?
```

The lane must return structured evidence rather than a binary answer. The
target output is a deterministic-first gap/proposal packet with backend
attempts, missing assumptions, proposed derivation routes, formalization
targets, validation boundaries, CLI/MCP parity, optional Markdown reports, and
clear non-claims.

## Mission Fit

This program continues the agent-consumable gap/proposal lane governed by:

- `docs/plans/mathdevmcp-agent-consumable-gap-proposal-mission-control-2026-07-06.md`
- `docs/plans/mathdevmcp-assumptions-agent-consumable-improvement-plan-2026-07-06.md`

The assumptions lane is the template. The derivation lane should make
`derive_from`, `derive_or_refute`, `debug_derivation`, and source-aware
derivation audits produce outputs that another agent can directly consume
without inventing missing math.

## Current Baseline

Available derivation-facing tools:

- `derive_or_refute`: bounded low-level derivation/refutation.
- `derive_from`: high-level "can I derive X?" wrapper with a diagnostic route
  plan, but no rich gap/proposal packet yet.
- `prove_or_counterexample`: proof/counterexample framing.
- `debug_derivation`: localizes gaps in a supplied derivation chain.
- `audit_derivation_v2_label`: audits derivation obligations extracted from
  LaTeX labels.
- `audit_and_propose_assumptions`: now emits rich assumption gap/proposal
  reports that can be reused when derivation fails due to missing assumptions.

Baseline risk:

- Existing derivation tools can report `proved`, `refuted`,
  `missing_assumptions`, `unknown`, or `not_encodable`, but the handoff is not
  yet a concrete derivation repair packet.

## Skeptical Plan Audit

This master program passes the pre-execution skeptical audit with the following
controls.

| Risk | Audit Result | Control |
| --- | --- | --- |
| Wrong baseline | Baseline is current callable behavior, not desired prose. | Phase 0 freezes current library/CLI/MCP behavior with focused tests and examples. |
| Proxy metric | Proposal count is not a pass criterion. | Pass criteria require linked gaps, backend attempts, validation or abstention, and non-claims. |
| Missing stop conditions | Long program could drift into open-ended theorem proving. | Each phase has explicit stop conditions and forbidden claims. |
| Unfair comparison | New lane may look better only because it writes longer reports. | Markdown must mirror structured fields; tests inspect structured payloads. |
| Hidden assumptions | Givens, assumptions, source text, and backend evidence can be conflated. | Schema separates givens, explicit assumptions, source provenance, backend attempts, and candidate routes. |
| Stale context | Worktree already has assumptions/audit lane changes. | Preserve unrelated dirty work and build on current code instead of reverting. |
| Environment mismatch | Lean/Sage/Claude may be unavailable. | Backends and reviewers produce `backend_unavailable`, `not_encodable`, or review-substitution records, not proof/refutation. |
| Artifact mismatch | A plan-only lane would not change agent behavior. | Every implementation phase must change callable library behavior and tests, then optionally render Markdown. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP answer derivability questions with structured evidence, gaps, and concrete next derivation proposals? |
| Baseline/comparator | Current `derive_from`, `derive_or_refute`, `debug_derivation`, `audit_derivation_v2_label`, and the new assumptions report pattern. |
| Primary pass criterion | Public library/CLI/MCP derivation workflow returns agent-consumable gap/proposal packets with deterministic tool-use records, backend attempts, validation/abstention, and Markdown reports for source-aware audits. |
| Veto diagnostics | Any diagnostic route reported as proof; backend absence treated as refutation; givens silently promoted to assumptions; generated Markdown contains claims not present in structured payloads; no exact location for source-label gaps when localization exists. |
| Explanatory diagnostics | Number of proposals, backend route selected, parser coverage, review comments, and report length. |
| Not concluded | No general theorem proving, no scientific validation of the risky-debt note, no proof beyond accepted backend evidence, no release readiness. |
| Preserved artifacts | Master program, phase subplans, phase results, review bundles, review logs, generated Markdown reports, and test outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure Mode | Early Diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use assumptions lane as output template | Current successful assumptions report work | Same agent-consumable pattern fits derivation gaps | Overfitting derivation to assumption-only outputs | Phase 1 schema must include backend attempts, target lhs/rhs, and derivation route fields | Reviewed default |
| Start with direct `derive_from` before source-aware reports | Existing tests and callable surface | Smallest behavior slice before document extraction complexity | Source-label report may be delayed | Phase 2 tests direct targets before Phase 3 labels | Reviewed default |
| Use rule/backend validation boundaries from current contracts | Existing high-level contracts | Preserves non-claim discipline | Certifying language leaks into diagnostic packets | Contract and tests inspect `certification_source`, backend attempts, validation statuses | Reviewed default |
| Claude read-only review for material plans | User request and review gate guide | Useful independent review without execution authority | Claude timeout or prompt too broad | Bounded review bundle and fallback/Codex substitution record | Reviewed default |
| Do not launch detached overnight execution without explicit approval and concrete supervisor command | Template and sandbox policy | Prevents fake unattended execution | User expected immediate detached execution | Gated overnight plan lists approval and launch prerequisites | Reviewed default |

## Phase Index

| Phase | Name | Objective | Subplan | Result Artifact |
| --- | --- | --- | --- | --- |
| 0 | Baseline, Schema, Review Gate | Freeze current behavior, define schema, review master/Phase 1 direction. | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-subplan-2026-07-06.md` | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-result-2026-07-06.md` |
| 1 | Gap/Proposal Builder | Add deterministic derivation gap/proposal builders. | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-subplan-2026-07-06.md` | `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md` |
| 2 | Rich Direct `derive_from` | Attach gaps/proposals/validation/tool-use records to direct derivability questions. | To be refreshed before Phase 2 execution | Phase 2 result |
| 3 | Source-Aware `audit_and_propose_derivation` | Add direct-target and LaTeX-label report-producing workflow. | To be drafted after Phase 2 | Phase 3 result |
| 4 | Backend Discipline And Assumption Integration | Reuse assumptions proposals, formalization targets, backend attempts, and abstention statuses. | To be drafted after Phase 3 | Phase 4 result |
| 5 | CLI/MCP Parity | Expose public CLI/MCP surfaces and contract sync. | To be drafted after Phase 4 | Phase 5 result |
| 6 | Real-Document Experiment | Generate derivation report for risky-debt labels and record residual gaps. | To be drafted after Phase 5 | Phase 6 result |
| 7 | Final Review And Handoff | Run focused regression, review final claims, and write reset memo update. | To be drafted after Phase 6 | Phase 7 result |

## Required Per-Phase Subplan Template

Every phase subplan must state:

- phase objective;
- entry conditions inherited from previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase:

1. run required local checks;
2. write a phase result / close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.

## Claude Review Protocol

Claude is a read-only reviewer only. Codex remains supervisor and executor.

Use:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name <review-name> \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/<bundle>.md \
  --model opus \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

If Claude does not respond:

1. send one tiny probe through the review gate;
2. if the probe responds, revise the material review prompt and retry;
3. if Claude remains unavailable, replace the review with a fresh Codex
   read-only review and record the substitution.

Review loops stop after five rounds for the same blocker.

## Program Stop Conditions

Stop and write a blocker result if:

- the same material plan/review blocker fails to converge after five review
  rounds;
- continuing needs a human direction change;
- continuing needs package installation, network fetch, credentials, or
  detached supervisor approval not already granted;
- implementation would require reverting unrelated dirty user work;
- a backend diagnostic would have to be presented as proof to proceed;
- source extraction cannot localize labels enough for the phase question and no
  smaller direct-target slice remains.

## Launch Boundary

The visible runbook for this program is:

- `docs/plans/mathdevmcp-derivation-audit-proposal-visible-gated-execution-runbook-2026-07-06.md`

The detached/overnight launch plan is:

- `docs/plans/mathdevmcp-derivation-audit-proposal-gated-overnight-execution-plan-2026-07-06.md`

Detached launch requires a concrete supervisor command and explicit approval.
Until that approval is granted, execution proceeds visibly in the current Codex
conversation.
