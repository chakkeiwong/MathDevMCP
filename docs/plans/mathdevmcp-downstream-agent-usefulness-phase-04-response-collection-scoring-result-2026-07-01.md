# Phase 4 Result: Response Collection And Scoring

Date: 2026-07-02

Status: `COMPLETED_WITH_A_CONDITION_LEAKAGE_VETO`

## Phase Objective

Collect approved downstream-agent responses under frozen prompts and score them
under the frozen rubric, preserving malformed or incomplete outputs.

## Skeptical Audit Result

Phase 4 response collection itself satisfied the approved collection contract:

- 27 frozen prompts existed before response collection.
- 27 raw Codex-subagent response artifacts were recorded.
- No Claude response worker was used.
- No hidden retries were used.
- No malformed or incomplete response was replaced.

The scoring audit found a material benchmark-design flaw after collection:

- all nine `A_task_only` prompt fixtures included
  `evidence_class_for_evaluator` and `expected_output_family_for_evaluator`;
- those fields are outside the Phase 1 A-condition allowed payload;
- therefore the A baseline is contaminated by evaluator/status leakage.

This is a hard-veto design finding, not a response-worker failure. The raw
responses remain useful diagnostic artifacts, but the A/B/C comparison cannot
be used as a clean downstream-agent usefulness benchmark result.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Partially answered as a diagnostic: response collection and B/C scoring completed, but the A baseline cannot answer clean A/B/C usefulness. |
| Baseline/comparator | A/B/C comparator is not valid because A leaked evaluator/status fields. B/C remain interpretable as a local tie. |
| Primary criterion | Collection manifest passed; scoring applied frozen rubric; hard-veto-first summary exists; comparison promotion failed. |
| Veto diagnostics | `condition_artifact_leakage` fired for all nine A rows. No hidden retry, Claude-worker, rubric-change, malformed-output, or unsupported-promotion veto fired. |
| Explanatory diagnostics | Score table, response manifest, hard-veto counts, and limitations are recorded. |
| Not concluded | No release readiness, public benchmark validity, scientific validation, product capability, broad theorem proving, general model reliability, or C-over-B superiority. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness/response_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.md`
- 27 raw response files under
  `.mathdevmcp/downstream_agent_usefulness/responses/`

## Hard-Veto-First Result

| Condition | Rows | Hard vetoes | Fixture contract violations | Malformed | Required passes after veto |
| --- | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 9 | 9 | 9 | 0 | 0 |
| `B_evidence_only` | 9 | 0 | 0 | 0 | 9 |
| `C_human_framed` | 9 | 0 | 0 | 0 | 9 |

Interpretation:

- A rows are preserved as raw responses but are not valid clean-baseline
  evidence.
- B and C rows pass the frozen rubric in this single-response diagnostic.
- B and C tie numerically on the required dimensions.
- C superiority is not established.
- The benchmark must be repaired before any new A/B/C response collection or
  promotion decision.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4 as completed with design veto | Response collection and scoring artifacts exist; A/B/C comparison invalid | A-condition leakage veto fired; no collection-policy veto fired | Whether repaired prompts will produce discriminating A/B/C results | Phase 5 benchmark repair taxonomy and fixture-regeneration plan | No C-over-B superiority, no product/scientific/release/public/general reliability claim |

## Required Checks Run

Checks run before this close record:

- JSON parse for frozen manifests, response manifest, and scored responses.
- Response count check: 27 raw response files.
- Prompt hash check during collection: no frozen prompt hash mismatch found.
- Required response-section check: all raw response files contained the frozen
  requested output sections.
- Scoring audit against Phase 1 condition contract found the A-condition
  leakage veto.

## Phase 5 Subplan Refresh

Phase 5 should not proceed as generic capability repair. The material failure is
benchmark-design leakage:

- classify the fixture-contract violation and any secondary measurement risks;
- repair prompt-generation rules so A excludes evaluator evidence/status;
- add validation tests that fail if forbidden condition fields leak;
- decide whether a new response-collection phase needs explicit human
  approval;
- do not rerun responses or claim repaired benchmark results without a new
  approved collection.

## Boundary Review

Local review of the Phase 5 direction:

- Consistency: Phase 5 now follows the observed Phase 4 failure rather than
  inventing workflow failures.
- Correctness: benchmark repair precedes any new comparison or promotion.
- Feasibility: prompt-harness validation and manifest checks are local and
  bounded.
- Artifact coverage: Phase 5 needs a failure taxonomy, repaired prompt design
  artifacts or plan, validation checks, and an explicit recollection approval
  boundary.
- Boundary safety: no new response collection, no scoring-rubric change, and no
  promotion claim is authorized by Phase 4.

## Handoff

Proceed to Phase 5 only as benchmark repair and measurement-design work. Any
new downstream-agent response collection after repaired prompts requires
explicit human approval for the new prompt count, subject surface, retry policy,
and artifact paths.
