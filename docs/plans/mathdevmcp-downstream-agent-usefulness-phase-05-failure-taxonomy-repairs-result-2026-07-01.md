# Phase 5 Result: Failure Taxonomy And Benchmark Repairs

Date: 2026-07-02

Status: `PASSED_REPAIRED_CANDIDATE_READY_RECOLLECTION_APPROVAL_NEEDED`

## Phase Objective

Convert Phase 4 findings into a targeted failure taxonomy and repair plan. The
material Phase 4 failure was benchmark-design leakage, so Phase 5 repaired the
prompt-condition validation path and produced repaired candidate prompt
fixtures. It did not rerun downstream-agent responses.

## Skeptical Audit Result

The Phase 5 plan survived local skeptical audit under the following constraints:

- Wrong baseline risk: addressed by treating the original A rows as
  contaminated rather than clean baseline evidence.
- Proxy metric risk: addressed by labeling repaired prompt fixtures as
  candidate artifacts, not usefulness evidence.
- Stop-condition risk: addressed by preserving the explicit approval boundary
  before any new response collection.
- Fairness risk: addressed by adding a prompt-condition validator for A leakage
  and B human-framing leakage.
- Artifact-answerability risk: addressed with a failure taxonomy, repaired
  candidate manifest, candidate prompts, validation summary, and focused tests.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Which Phase 4 failures can be safely repaired, and what remains a measurement limitation? |
| Baseline/comparator | Phase 4 scored responses, prompt manifest, Phase 1 condition contract, and current prompt fixtures. |
| Primary criterion | Passed for local benchmark repair: observed leakage is classified, repaired candidate prompts validate, and scoring criteria were not changed. |
| Veto diagnostics | No hidden response rerun, no rubric change, no promotion claim, and repaired candidate A prompts pass the leakage validator. |
| Explanatory diagnostics | Failure taxonomy, repaired candidate prompts/manifest, validation summary, and focused pytest results. |
| Not concluded | No repaired benchmark result, no final usefulness promotion, no C-over-B claim, and no release/public/scientific/product/general reliability claim. |

## Artifacts Produced

- `src/mathdevmcp/downstream_usefulness_prompts.py`
- `tests/test_downstream_usefulness_prompts.py`
- `.mathdevmcp/downstream_agent_usefulness/failure_taxonomy.json`
- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/repaired_prompt_contract_validation.json`

## Repair Summary

Implemented a local prompt-condition validator:

- `A_task_only` must not include evaluator/status, evidence, proof,
  counterexample, gap, machine-evidence, human-framing, or recommended-action
  payload terms.
- `B_evidence_only` must not include human-framing payload terms.
- Each case must have A/B/C prompt coverage.

Generated a repaired candidate prompt set:

- 9 cases x 3 conditions = 27 candidate prompts.
- Evaluator-only labels remain in the candidate manifest for scoring, but are
  not present in `A_task_only` prompt text.
- The repaired candidate set is not a response artifact and does not authorize
  any usefulness claim.

## Failure Taxonomy Summary

| Failure | Classification | Current status |
| --- | --- | --- |
| A-condition evaluator/status leakage | Hard veto | Repaired candidate created and validated |
| Single-response high variance | Measurement limit | Deferred to recollection design |
| Manifest-order collection | Measurement limit | Deferred to recollection design |
| B/C ceiling effect | Measurement limit | Deferred to benchmark design |
| Missing early subagent identifiers | Audit limit | Recorded limitation |

## Required Checks Run

- `python3 -m pytest tests/test_downstream_usefulness_prompts.py tests/test_agent_handoff_packet.py`
  - `13 passed`
- JSON parse over `.mathdevmcp/downstream_agent_usefulness/*.json`
  - `json ok 11`
- Prompt-contract validation:
  - current frozen manifest: `current_errors 18`
  - repaired candidate manifest: `repaired_errors 0`
- `git diff --check -- src/mathdevmcp/downstream_usefulness_prompts.py tests/test_downstream_usefulness_prompts.py .mathdevmcp/downstream_agent_usefulness docs/plans/mathdevmcp-downstream-agent-usefulness-*.md`
  - clean

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 6 with no promotion | Phase 5 repair artifacts and checks passed | Original A leakage repaired in candidate fixtures; no response rerun | Whether repaired prompts produce a discriminating A/B/C result | Final decision should record recollection approval needed | No usefulness promotion, no C-over-B superiority, no public/scientific/product/release/general reliability claim |

## Phase 6 Subplan Refresh

Phase 6 should close the current runbook with a bounded decision:

- mark the original Phase 4 comparison as invalid for promotion;
- mark Phase 5 repaired candidate fixtures as ready for a new approved
  collection;
- record that new downstream-agent response collection is a human approval
  boundary;
- recommend recollection design improvements if the user wants a stronger
  result: randomized/counterbalanced order, immediate subagent identity logging,
  and optionally replicated subjects per prompt.

## Boundary Review

Local review of the Phase 6 direction:

- Consistency: follows Phase 4 and Phase 5 artifacts.
- Correctness: no promotion can occur while the only collected A baseline is
  contaminated.
- Feasibility: final decision can be written with local checks only.
- Artifact coverage: final summary should cite Phase 4 scoring, Phase 5
  taxonomy, repaired prompt manifest, validation, and checks.
- Boundary safety: any repaired-prompt response collection requires explicit
  human approval.

## Handoff

Proceed to Phase 6 final regression and bounded decision. Do not collect new
downstream-agent responses unless the user explicitly approves the repaired
candidate collection scope.
