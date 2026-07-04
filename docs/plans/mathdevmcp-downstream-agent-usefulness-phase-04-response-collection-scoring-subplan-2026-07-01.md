# Phase 4 Subplan: Response Collection And Scoring

Date: 2026-07-01

Status: `APPROVED_FOR_PHASE_4_EXECUTION`

## Phase Objective

Collect approved downstream-agent responses under frozen prompts and score them
under the frozen rubric, preserving malformed or incomplete outputs.

## Entry Conditions Inherited From Previous Phase

- Phase 3 prompt fixtures and manifests are frozen.
- Human approval exists for exact response collection scope.
- Claude is excluded as response worker.
- No hidden retries are permitted.

## Required Artifacts

- Phase 4 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-result-2026-07-01.md`.
- Response manifest:
  `.mathdevmcp/downstream_agent_usefulness/response_manifest.json`.
- Raw response artifacts under:
  `.mathdevmcp/downstream_agent_usefulness/responses/`.
- Scored responses:
  `.mathdevmcp/downstream_agent_usefulness/scored_responses.json` and/or
  `.mathdevmcp/downstream_agent_usefulness/scored_responses.md`.
- Updated ledger and stop handoff if execution stops.

## Required Checks, Tests, Reviews

- Manifest validation: one and only one recorded outcome per approved prompt.
- No-hidden-retry audit using timestamps/manifest entries.
- Scoring rubric validation against Phase 1 contract.
- Hard-veto-first analysis.
- Claude read-only review of scored-result summary, not raw whole file unless
  specifically needed and approved by artifact size.
- Local skeptical audit for proxy promotion and aggregate-only conclusions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What do approved downstream responses show under the frozen usefulness rubric? |
| Baseline/comparator | A/B/C prompt conditions from Phase 3. |
| Primary criterion | Every approved prompt has one recorded response or malformed-output record; scores use the frozen rubric; hard vetoes and per-case results are reported before aggregates. |
| Veto diagnostics | Hidden retry; missing malformed output; Claude response worker; changed rubric; unrecorded prompt; aggregate promotion despite hard veto; unsupported C superiority claim. |
| Explanatory diagnostics | Score tables, condition summaries, hard-veto counts, malformed-output records, qualitative failure notes. |
| Not concluded | No release readiness, public benchmark validity, scientific validation, product capability, or general model reliability. |

## Forbidden Claims Or Actions

- Do not rerun bad responses.
- Do not discard malformed outputs.
- Do not use Claude as worker.
- Do not change scoring criteria after viewing responses.
- Do not conclude more than the response sample supports.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- response and score manifests validate;
- hard-veto-first summaries exist;
- limitations from sample size and response-subject choice are explicit;
- the Phase 5 repair subplan is reviewed for avoiding overfitting and
  criterion drift.

## Stop Conditions

Stop if:

- response collection approval is absent or narrower than needed;
- response worker fails in a way that would require hidden retries;
- scoring cannot be applied without changing the rubric;
- hard-veto evidence reveals an unfixable boundary flaw.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 4 result or blocker record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
