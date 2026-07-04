# Phase 5 Subplan: Failure Taxonomy And Benchmark Repairs

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE_4_A_CONDITION_LEAKAGE_VETO`

## Phase Objective

Convert Phase 4 findings into a targeted failure taxonomy and repair plan.
Because Phase 4 found an A-condition fixture-contract violation, the primary
repair target is benchmark/harness design rather than high-level math workflow
capability.

The phase may implement local prompt-harness validation repairs and update
benchmark documentation. It must not rerun downstream-agent responses, change
the frozen Phase 1 scoring rubric, or promote any usefulness claim.

## Entry Conditions Inherited From Previous Phase

- Phase 4 scored responses exist and identify `condition_artifact_leakage` for
  all nine `A_task_only` rows.
- Phase 1 rubric remains frozen for interpreting Phase 4 evidence.
- Any proposed repair is tied to a concrete observed failure or measurement
  limitation.
- New response collection remains outside this phase unless separately
  approved by the user.

## Required Artifacts

- Phase 5 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-result-2026-07-01.md`.
- Failure taxonomy artifact:
  `.mathdevmcp/downstream_agent_usefulness/failure_taxonomy.json` or markdown
  equivalent.
- Benchmark repair plan or patch list.
- Focused tests or validation scripts for any prompt-harness or manifest
  repair.
- Updated docs if boundary language, condition contracts, or operator behavior
  changes.
- A recollection approval request if repaired prompts would require new
  downstream-agent responses.
- Updated ledger and stop handoff if execution stops.

## Required Checks, Tests, Reviews

- Failure taxonomy coverage check: every material Phase 4 failure or limitation
  is classified or explicitly deferred.
- Prompt-condition contract validation: A must exclude evaluator/status,
  evidence, proof/counterexample, gap, machine-evidence, and human-framing
  payloads; B and C must satisfy B/C machine-evidence parity.
- Focused pytest or local validation for touched prompt-generation or benchmark
  code.
- Existing high-level workflow and packet tests only if those surfaces are
  touched.
- Claude read-only review for material repairs and claim boundaries.
- Local skeptical audit for overfitting, default-policy drift, and unsupported
  promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which Phase 4 failures can be safely repaired, and what remains a measurement limitation requiring new approval or a new collection phase? |
| Baseline/comparator | Phase 4 scored responses, prompt manifest, Phase 1 condition contract, and current prompt-generation behavior. |
| Primary criterion | Repairs are traceable to observed fixture leakage or measurement limitations, pass focused checks, and do not change scoring/promotion criteria post hoc. |
| Veto diagnostics | Repair overfits to response wording; rubric changed; A leakage remains; B/C parity broken; hidden response rerun; diagnostic evidence relabeled as proof; unrelated refactor. |
| Explanatory diagnostics | Failure taxonomy, prompt-contract validation, repair diffs, focused test results, recollection boundary note. |
| Not concluded | No final usefulness promotion, no repaired-benchmark result, and no C-over-B claim until a separately approved repaired collection is run and scored. |

## Forbidden Claims Or Actions

- Do not change Phase 1 scoring criteria.
- Do not rerun Phase 4 responses to improve scores unless a new approved
  collection phase is planned separately.
- Do not make broad refactors unrelated to observed failures.
- Do not convert diagnostic routes into certified claims.
- Do not treat repaired prompt fixtures as response evidence before new
  approved collection.
- Do not use the contaminated A rows as clean-baseline evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- every material Phase 4 failure and measurement limitation is classified as
  repaired, deferred, evidence limit, recollection-needed, or blocker;
- any prompt-harness repair has focused validation;
- the recollection approval boundary is explicit if new responses are needed;
- final regression subplan is reviewed for fair comparison and non-claims.

## Stop Conditions

Stop if:

- failures imply the benchmark design is invalid;
- repairs require changing the frozen scoring rubric;
- repairs need package/network/model-file changes without approval;
- new response collection is required before further progress and the user has
  not approved the exact scope;
- a material Claude/Codex review issue fails to converge within five rounds.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 5 result or blocker record;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.

## Phase 5 Start Review After Phase 4

Local skeptical review:

- Wrong baseline risk: high. The original A baseline is contaminated and must
  not be reused as clean baseline evidence.
- Proxy metric risk: contained if Phase 5 repairs prompts and validations only;
  repaired prompts are not themselves usefulness evidence.
- Stop-condition risk: any new response collection requires explicit approval.
- Fairness risk: B/C parity must be validated alongside A de-leakage.
- Artifact-answerability risk: Phase 5 must produce a failure taxonomy and
  validation artifact; otherwise Phase 6 cannot make a bounded decision.

Phase 5 is feasible as a benchmark repair phase. It is not authorized as a
promotion or response-recollection phase.
