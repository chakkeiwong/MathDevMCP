# Phase 3 Subplan: Prompt Fixtures And Contract Validation

Date: 2026-07-02

Status: `READY_FOR_PHASE_3_EXECUTION_AFTER_PHASE_2_CLOSE`

## Phase Objective

Generate v2 A/B/C prompt fixtures, a prompt manifest with hashes, and a
prompt-contract validation report from the Phase 2 case manifest candidate,
while preserving the repaired baseline and stopping before any response
collection.

## Entry Conditions Inherited From Previous Phase

- Phase 2 case manifest candidate exists and parses.
- Phase 2 scoring applicability map exists and parses.
- All six workflow families are covered.
- At least three cases are predeclared high C-sensitivity.
- No v2 response artifacts exist.
- Repaired baseline artifacts remain unmodified.

## Required Artifacts

- Phase 3 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-result-2026-07-02.md`.
- Prompt fixture directory:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompts_candidate/`.
- Prompt manifest with hashes:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`.
- Prompt-contract validation report:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json`.
- Draft Phase 4 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-subplan-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- JSON parse case manifest, prompt manifest, and validation report.
- Confirm expected prompt count: 6 cases x 3 conditions = 18 prompts.
- Confirm every case has A/B/C prompt coverage.
- Run prompt-contract validation with the existing
  `validate_downstream_prompt_contract` helper.
- Run additional v2 leakage checks:
  - A prompt text must not include decisive witness/certificate/evidence
    fields, evaluator-only labels, or artifact answer labels.
  - B prompt text must not include human-framed packet fields,
    recommended-next-action prose, or narrative answer fields.
  - C prompt text may include framing but must not include
    `expected_output_family`, `evidence_class`, or evaluator-only labels as
    authority.
- Verify prompt manifest hashes match prompt file contents.
- Check no response artifacts were created.
- Check repaired baseline hashes still match Phase 0 manifest for primary
  artifacts.
- Run focused pytest for downstream prompt validator if code is touched; if no
  code is touched, run a local validation script only.
- Run `git diff --check` on v2 plans/artifacts.
- Local skeptical audit for prompt leakage, answer leakage, hidden scoring
  labels, stale source boundaries, and accidental collection.
- Attempt compact Claude read-only review for the Phase 4 subplan if
  available; otherwise record reviewer unavailability and local review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can v2 A/B/C prompt fixtures be generated from the candidate cases while preserving condition boundaries and avoiding answer leakage? |
| Baseline/comparator | Phase 2 case manifest candidate, frozen repaired prompt-contract helper, and Phase 0 baseline hashes. |
| Primary criterion | Phase 3 passes if 18 prompt fixtures exist, manifest hashes match, prompt-contract validation has zero errors, v2 leakage checks pass, no responses are collected, and Phase 4 subplan is ready. |
| Veto diagnostics | A leaks decisive evidence or evaluator labels; B leaks human framing or narrative answer; C leaks hidden scoring labels as authority; response artifacts created; repaired baseline mutation; prompt manifest/hash mismatch; unsupported C-over-B claim. |
| Explanatory diagnostics | Condition counts, hash check, leakage check report, validator output, local review. |
| Not concluded | No response quality, no downstream-agent usefulness, no C-over-B superiority, no model reliability, no release/public/scientific/product claim. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not edit `.mathdevmcp/downstream_agent_usefulness/`.
- Do not change the existing prompt validator unless a focused, reviewed code
  repair is required.
- Do not put evaluator-only expected answer fields into prompt text.
- Do not treat prompt validation as task success.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- 18 prompt fixtures exist and are referenced by a parsing prompt manifest;
- manifest hashes match file contents;
- prompt-contract validation report records zero errors;
- v2 leakage checks pass;
- no response artifacts exist under v2 root;
- Phase 4 subplan exists and includes objective, entry conditions, artifacts,
  checks, evidence contract, forbidden claims/actions, handoff conditions, and
  stop conditions.

## Stop Conditions

Stop if:

- A/B/C boundaries cannot be enforced without making prompts too vague;
- v2 leakage checks fail after five focused repair rounds;
- prompt generation would require substantial private source excerpts;
- repaired baseline hashes no longer match the Phase 0 manifest;
- continuing would require response collection or scoring.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 3 result/close record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. attempt compact Claude read-only review if available, or record current
   reviewer unavailability.
