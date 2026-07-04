# Phase 5 Subplan: Candidate Close And Handoff

Date: 2026-07-02

Status: `READY_FOR_PHASE_5_EXECUTION_AFTER_PHASE_4_CLOSE`

## Phase Objective

Run final local checks, write the v2 candidate result note and visible stop
handoff, and stop before any unauthorized response collection.

## Entry Conditions Inherited From Previous Phase

- Phase 4 adversarial/ceiling analysis exists and parses.
- Phase 4 future collection runbook exists and states collection is not
  authorized.
- Phase 3 prompt validation reports zero errors.
- No v2 response artifacts exist.
- Repaired baseline hashes still match Phase 0 manifest.

## Required Artifacts

- Phase 5 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-result-2026-07-02.md`.
- Candidate result note:
  `.mathdevmcp/downstream_agent_usefulness_v2/result_note_candidate.md`.
- Updated visible stop handoff:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-stop-handoff-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- JSON parse all v2 JSON artifacts.
- Run prompt-contract validation or inspect the Phase 3 validation report for
  zero errors.
- Confirm prompt count is 18 and response artifact count is 0.
- Recheck primary repaired baseline hashes against Phase 0 manifest.
- Run focused pytest for downstream prompt validator.
- Run `git diff --check` on v2 plans/artifacts.
- Local skeptical audit for unsupported claims, missing handoff conditions,
  artifact mismatch, and accidental collection.
- Attempt compact Claude read-only review for the final handoff if available;
  if unavailable, record current status and do not treat it as approval.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the v2 benchmark candidate complete as a local maintenance artifact, with exact future collection approval boundaries and no unauthorized response collection? |
| Baseline/comparator | Frozen repaired benchmark baseline and all v2 candidate artifacts. |
| Primary criterion | Phase 5 passes if all local checks pass, result/handoff artifacts are written, no response artifacts exist, and final status stops at candidate readiness. |
| Veto diagnostics | Response collection; Claude as worker; baseline mutation; prompt validation errors; unsupported C-over-B, release, public, scientific, product, or general-reliability claim; missing future approval boundary. |
| Explanatory diagnostics | Artifact inventory, validation report, local tests, hash recheck, review status, stop handoff. |
| Not concluded | No scored v2 result, no C-over-B superiority, no model reliability, no release/public/scientific/product claim. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not create response manifests or scored-response files.
- Do not mutate repaired baseline artifacts.
- Do not claim v2 public validity or C-over-B superiority.
- Do not claim Claude review approval if Claude remains unavailable.

## Exact Next-Phase Handoff Conditions

There is no next execution phase in this program. Completion requires:

- result note and Phase 5 result written;
- visible stop handoff updated;
- checks recorded;
- explicit statement that future collection requires human approval for prompt
  count, response-worker surface, retry policy, scoring contract, and artifact
  paths.

## Stop Conditions

Stop with blocker if:

- any final check fails and cannot be repaired within five focused repair
  rounds;
- response artifacts are present unexpectedly;
- baseline hashes mismatch;
- final handoff would require collection, scoring, implementation repair,
  source-permission decisions, or unsupported claims.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 5 result/close record;
3. update the visible stop handoff;
4. record Claude review status;
5. stop before response collection.
