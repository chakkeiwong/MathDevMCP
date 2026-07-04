# Phase 4 Subplan: Adversarial Analysis And Collection Runbook

Date: 2026-07-02

Status: `READY_FOR_PHASE_4_EXECUTION_AFTER_PHASE_3_CLOSE`

## Phase Objective

Write adversarial/ceiling-effect analysis for the v2 candidate prompts and a
future response-collection runbook that preserves no-hidden-retry discipline
and stops before explicit human collection approval.

## Entry Conditions Inherited From Previous Phase

- Phase 3 prompt manifest exists and parses.
- Phase 3 prompt-contract validation report records zero errors.
- 18 v2 prompt fixtures exist and hashes match.
- No v2 response artifacts exist.
- Repaired baseline hashes still match Phase 0 manifest.

## Required Artifacts

- Phase 4 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-result-2026-07-02.md`.
- Adversarial/ceiling-effect analysis:
  `.mathdevmcp/downstream_agent_usefulness_v2/adversarial_ceiling_analysis.json`.
- Future collection runbook:
  `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`.
- Draft Phase 5 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-subplan-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- JSON parse adversarial/ceiling analysis.
- Check runbook contains:
  - explicit approval boundary;
  - prompt count;
  - response subject surface to be approved;
  - retry policy;
  - malformed-output policy;
  - artifact paths for future responses/scoring;
  - Claude read-only-only boundary;
  - no collection in this program.
- Check no v2 response artifacts were created.
- Check repaired baseline hashes still match Phase 0 manifest.
- Run `git diff --check` on v2 plans/artifacts.
- Local skeptical audit for collection creep, unsupported validity claims,
  hidden retries, prompt-polish proxy scoring, and scoring drift.
- Attempt compact Claude read-only review for the Phase 5 subplan if
  available; otherwise record reviewer unavailability and local review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the v2 candidate have documented leakage/ceiling risks and a future collection runbook that preserves approval, retry, malformed-output, and Claude-role boundaries? |
| Baseline/comparator | Phase 3 validated v2 prompt fixtures and frozen repaired baseline. |
| Primary criterion | Phase 4 passes if adversarial analysis and future collection runbook exist, checks pass, no responses are collected, and Phase 5 handoff subplan is ready. |
| Veto diagnostics | Actual response collection; hidden retries; Claude as worker; scoring criteria changed after responses; prompt polish treated as success; unsupported C-over-B, release, public, scientific, product, or general-reliability claims; repaired baseline mutation. |
| Explanatory diagnostics | Risk table, ceiling-effect risks, collection approval checklist, artifact-path plan, baseline hash recheck. |
| Not concluded | No scored v2 result, no C-over-B superiority, no model reliability, no release/public/scientific/product claim. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not create response manifests or scored-response files as if collection
  occurred.
- Do not use Claude as a response worker.
- Do not change scoring criteria after seeing responses.
- Do not claim v2 validity beyond candidate readiness.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- adversarial/ceiling analysis exists and parses;
- future collection runbook exists and states the approval boundary;
- no response artifacts exist under v2 root;
- repaired baseline hashes match Phase 0 manifest;
- Phase 5 subplan exists and includes objective, entry conditions, artifacts,
  checks, evidence contract, forbidden claims/actions, handoff conditions, and
  stop conditions.

## Stop Conditions

Stop if:

- runbook cannot state a clean collection approval contract;
- adversarial analysis finds prompt leakage requiring Phase 3 repair;
- future scoring would require rubric drift after collection;
- response collection is requested without explicit approval for prompt count,
  response-worker surface, retry policy, and artifact paths;
- repaired baseline hashes no longer match the Phase 0 manifest.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 4 result/close record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. attempt compact Claude read-only review if available, or record current
   reviewer unavailability.
