# Phase 2 Subplan: Case Manifest Candidate

Date: 2026-07-02

Status: `READY_FOR_PHASE_2_EXECUTION_AFTER_PHASE_1_CLOSE`

## Phase Objective

Create the v2 case manifest candidate and scoring applicability map under the
separate v2 artifact root, using the Phase 1 difficulty requirements and
without creating prompt fixtures or collecting responses.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline hash manifest exists and records the repaired baseline.
- Phase 1 ceiling-effect analysis exists and parses.
- Phase 1 difficulty requirements exist and parse.
- No v2 prompt fixtures or response artifacts have been created.
- Repaired baseline artifacts remain unmodified.

## Required Artifacts

- Phase 2 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-result-2026-07-02.md`.
- V2 case manifest candidate:
  `.mathdevmcp/downstream_agent_usefulness_v2/case_manifest_candidate.json`.
- V2 scoring applicability map:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json`.
- Draft Phase 3 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-subplan-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- JSON parse Phase 2 artifacts.
- Coverage check that all six workflow families are represented.
- Check that at least three cases are predeclared high C-sensitivity.
- Check each case has: case id, workflow family, source boundary, task prompt
  summary, evidence class, expected answer family for evaluator-only manifest
  use, required artifact type, B compact-evidence design, C framing design,
  non-claim boundaries, and scoring applicability.
- Check Phase 2 creates no prompt fixture files and no response artifacts.
- Check repaired baseline hashes still match Phase 0 manifest for primary
  artifacts.
- Run `git diff --check` on v2 plans/artifacts.
- Local skeptical audit for answer leakage, case overfitting, private-source
  boundary, and scoring drift.
- Attempt compact Claude read-only review for the Phase 3 subplan if
  available; otherwise record reviewer unavailability and local review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the v2 candidate case set cover the target workflow families with harder, source-bounded cases that plausibly separate B and C without leaking expected answers? |
| Baseline/comparator | Phase 1 difficulty requirements and the frozen repaired benchmark baseline. |
| Primary criterion | Phase 2 passes if the case manifest and scoring map parse, cover all six workflow families, include at least three high C-sensitivity cases, preserve source boundaries, and stop before prompt generation. |
| Veto diagnostics | Prompt fixtures created early; response collection; repaired baseline mutation; evaluator-only answers copied into prompt fields; substantial private excerpts; cases tuned to implementation changes; unsupported C-over-B or benchmark-validity claims. |
| Explanatory diagnostics | Workflow/evidence/artifact coverage, C-sensitivity count, source-boundary summary, baseline hash recheck, local review. |
| Not concluded | No prompt validity, no scored response evidence, no C-over-B superiority, no model reliability, no release/public/scientific/product claim. |

## Forbidden Claims Or Actions

- Do not create prompt fixture files in Phase 2.
- Do not collect responses.
- Do not edit `.mathdevmcp/downstream_agent_usefulness/`.
- Do not use hidden evaluator labels in future prompt-visible fields.
- Do not claim v2 validity beyond candidate case design.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- case manifest candidate and scoring applicability map exist and parse;
- all six workflow families are covered;
- at least three cases are high C-sensitivity;
- no prompt fixtures or response artifacts exist under the v2 root;
- Phase 3 subplan exists and includes objective, entry conditions, artifacts,
  checks, evidence contract, forbidden claims/actions, handoff conditions, and
  stop conditions.

## Stop Conditions

Stop if:

- the case set cannot avoid answer leakage without becoming too vague;
- source materials require privacy/copyright decisions beyond bounded summaries
  or synthetic fixtures;
- B/C discrimination requires changing the frozen scoring rubric after seeing
  responses;
- repaired baseline hashes no longer match the Phase 0 manifest;
- Claude/Codex review finds a material boundary flaw that cannot be repaired
  after five focused review rounds.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 2 result/close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. attempt compact Claude read-only review if available, or record current
   reviewer unavailability.
