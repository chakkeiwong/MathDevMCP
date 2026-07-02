# Phase 1 Subplan: Ceiling-Effect And Difficulty Requirements

Date: 2026-07-02

Status: `READY_FOR_PHASE_1_EXECUTION_AFTER_PHASE_0_CLOSE`

## Phase Objective

Inventory why the repaired benchmark produced a B/C ceiling effect and convert
that diagnosis into v2 difficulty requirements that can guide case design
without inspecting new response-worker outputs or tuning to implementation
changes.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline hash manifest exists and parses.
- V2 artifact root exists separately from the repaired baseline root.
- Phase 0 result records no repaired-baseline mutation.
- No v2 case manifest, prompt fixtures, or responses have been created.
- Claude review remains read-only only; current availability is recorded in
  the review trail.

## Required Artifacts

- Phase 1 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-result-2026-07-02.md`.
- Ceiling-effect analysis:
  `.mathdevmcp/downstream_agent_usefulness_v2/ceiling_effect_analysis.json`.
- Difficulty requirements:
  `.mathdevmcp/downstream_agent_usefulness_v2/difficulty_requirements.json`.
- Draft Phase 2 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-subplan-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- JSON parse the repaired scored responses and Phase 1 v2 JSON artifacts.
- Check that Phase 1 artifacts are analysis/requirements only and contain no
  prompt fixtures or response artifacts.
- Coverage check that requirements address all six target workflow families:
  `derive_from`, `prove_or_counterexample`, `assumptions_for`,
  `audit_math_to_code`, `debug_derivation`, and `prepare_review_packet`.
- Check that no repaired baseline file content is modified.
- Run `git diff --check` on v2 plans/artifacts.
- Local skeptical audit for proxy metrics, answer leakage, hidden assumptions,
  stale context, and commands whose artifacts would not answer the phase
  question.
- Attempt compact Claude read-only review of the Phase 2 subplan if available;
  if unavailable, record the current probe status and run local review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Why did B and C tie in the repaired benchmark, and what predeclared difficulty requirements should v2 cases satisfy to plausibly separate them without answer leakage? |
| Baseline/comparator | Repaired scored responses and repaired prompt-contract validation under `.mathdevmcp/downstream_agent_usefulness/`. |
| Primary criterion | Phase 1 passes if it records the B/C ceiling-effect causes, maps them to v2 requirements across the six workflow families, and preserves all non-claim and no-collection boundaries. |
| Veto diagnostics | New response collection; cases selected after new outputs; changing frozen scores; treating prompt polish as success; claiming C-over-B superiority; adding requirements that leak expected answers into prompts. |
| Explanatory diagnostics | Per-case repaired B/C tie reasons, requirement-to-workflow matrix, artifact-kind check, baseline hash check. |
| Not concluded | No v2 case validity, no prompt validity, no downstream-agent usefulness, no model reliability, no C-over-B superiority, no public/scientific/product/release claim. |

## Forbidden Claims Or Actions

- Do not collect or score new responses.
- Do not edit `.mathdevmcp/downstream_agent_usefulness/`.
- Do not treat repaired B/C tied passing rows as evidence that C is useless or
  that B is sufficient in general.
- Do not create v2 prompts in Phase 1.
- Do not introduce evaluator-only expected answers into future prompt text.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- ceiling-effect analysis exists and parses as JSON;
- difficulty requirements exist and parse as JSON;
- every target workflow family has at least one v2 difficulty requirement;
- Phase 1 result records checks and non-claims;
- Phase 2 subplan exists and includes objective, entry conditions, artifacts,
  checks, evidence contract, forbidden claims/actions, handoff conditions, and
  stop conditions.

## Stop Conditions

Stop if:

- repaired artifacts are missing or cannot be parsed;
- B/C ceiling effect cannot be diagnosed without new response collection;
- requirements would need response collection, implementation details, private
  source excerpts, or post-hoc scoring changes;
- Claude/Codex review finds a material boundary flaw that cannot be repaired
  after five focused review rounds.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 1 result/close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. attempt compact Claude read-only review if available, or record current
   reviewer unavailability.
