# Phase 3 Subplan: Prompt Harness And Collection Gate

Date: 2026-07-01

Status: `READY_FOR_PHASE_3_EXECUTION`

## Phase Objective

Build or validate frozen A/B/C prompt fixtures and response-collection harness
metadata, then stop for explicit response-collection approval if needed.

## Entry Conditions Inherited From Previous Phase

- Phase 2 case manifest is frozen.
- Phase 1 rubric is frozen.
- No response collection has started.

## Required Artifacts

- Phase 3 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-result-2026-07-01.md`.
- Prompt manifest, preferably:
  `.mathdevmcp/downstream_agent_usefulness/prompt_manifest.json`.
- Frozen prompt fixtures under:
  `.mathdevmcp/downstream_agent_usefulness/prompts/`.
- Response-subject policy manifest.
- Approval request note if response collection is not already approved.
- Updated ledger and stop handoff if execution stops.

## Required Checks, Tests, Reviews

- Prompt count and A/B/C balance check.
- Determinism check for fixture generation if a generator is introduced.
- No-hidden-retry and malformed-output preservation check in the response
  policy.
- Claude read-only review of the compact collection-gate brief.
- Local skeptical audit for prompt leakage, unfair comparators, and approval
  boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are prompt fixtures and collection rules frozen enough to collect downstream-agent responses without hidden bias or approval drift? |
| Baseline/comparator | Phase 2 cases and Phase 1 A/B/C comparator contract. |
| Primary criterion | Prompt fixtures, manifest, response-subject policy, retry policy, and artifact paths are frozen before any response collection. |
| Veto diagnostics | Response collection starts before approval; prompts expose condition labels unfairly; A/B/C conditions differ in task substance; hidden retries allowed; malformed outputs replaceable; Claude assigned as worker. |
| Explanatory diagnostics | Prompt manifest, fixture hashes, condition counts, response-subject policy. |
| Not concluded | No usefulness result, no model reliability, no scoring result, no promotion decision. |

## Forbidden Claims Or Actions

- Do not collect responses unless explicit approval already covers the exact
  prompt count, response subject, no-hidden-retry policy, and artifact paths.
- Do not use Claude as a response subject.
- Do not revise Phase 1 scoring after seeing prompt artifacts unless the phase
  writes a blocker and returns to Phase 1.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- prompts and manifests are frozen and validated;
- response-subject policy is explicit;
- human approval exists for response collection, or Phase 3 writes a blocker
  requesting approval and stops;
- the Phase 4 subplan is reviewed for no-hidden-retry and artifact safety.

## Stop Conditions

Stop if:

- response collection approval is missing;
- response subject is ambiguous;
- prompt fixture generation cannot preserve fair A/B/C comparators;
- Claude review finds a material boundary issue that does not converge within
  five rounds.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 3 result or blocker record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
