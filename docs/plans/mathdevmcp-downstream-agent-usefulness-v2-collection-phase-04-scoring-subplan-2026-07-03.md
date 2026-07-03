# Phase 4 Subplan: Hard-Veto-First Scoring

Date: 2026-07-03

Status: `READY_FOR_PHASE_4_EXECUTION`

## Phase Objective

Score the 18 collected v2 response artifacts under the frozen collection
scoring contract, applying hard vetoes before required-pass counts and
producing bounded local diagnostic artifacts.

## Entry Conditions Inherited From Previous Phase

- Phase 3 response collection completed with 18 response artifacts.
- Response manifest exists and parses:
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`.
- Every approved prompt id is represented exactly once.
- No hidden retries or malformed-output replacements were used.
- Claude was not used as a response worker.
- Scored-response files do not yet exist.
- Frozen scoring contract exists:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.
- Candidate-only stressors remain explanatory only.

## Required Artifacts

- Scored JSON:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`.
- Scored Markdown:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.
- Phase 4 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-result-2026-07-03.md`.
- Draft Phase 5 review/decision subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-subplan-2026-07-03.md`.
- Updated execution ledger and stop handoff if Phase 5 review cannot proceed.

## Required Checks, Tests, Reviews

- Parse response manifest, scoring contract, scoring applicability map, and
  baseline rubric.
- Verify prompt manifest hash still matches the frozen scoring contract.
- Verify response manifest records 18 responses and each response path/hash
  matches.
- Apply scoring in the frozen order:
  hard vetoes, primary required dimensions, explanatory dimensions,
  candidate-only stressor notes, per-case B/C deltas, then condition summary.
- Verify scored JSON parses.
- Verify scored JSON has 18 rows and each row follows the frozen row schema.
- Verify hard-veto counts are reported before pass counts in Markdown.
- Verify C-over-B interpretation obeys the per-case comparison rule and does
  not rely on aggregate-only promotion.
- Run focused pytest:
  `python3 -m pytest tests/test_downstream_usefulness_prompts.py`.
- Run `git diff --check` over v2 artifacts and collection plans.
- Local skeptical audit for proxy metrics, prompt-polish scoring, hidden
  criterion changes, aggregate-only promotion, and unsupported claims.
- Claude review is not a scoring authority. If Phase 5 uses Claude, it is
  read-only reviewer only and cannot authorize claims or boundary crossings.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Under the frozen scoring contract, do v2 C_human_framed responses improve downstream-agent task performance over B_evidence_only responses without hard-veto or malformed-output regressions? |
| Baseline/comparator | Per-case B_evidence_only rows are the primary comparator; A_task_only rows are diagnostic context. |
| Primary criterion | Phase 4 passes if scored JSON/Markdown exist, parse/check cleanly, hard vetoes are reported before pass counts, and the C-vs-B decision follows the frozen per-case rule. |
| Veto diagnostics | Scoring criteria changed after responses; Claude response-worker use; hidden retry or replacement; malformed-output regression hidden; hard-veto regression hidden; candidate-only stressors promoted to primary; prompt polish scored as task success; aggregate-only C-over-B claim; unsupported public/scientific/product/release/general-reliability claim. |
| Explanatory diagnostics | Per-row scores, condition totals, per-case B/C deltas, candidate-stressor notes, malformed-output count, limitations. |
| Not concluded | No proof certificate, no release gate, no public benchmark result, no scientific validation, no product capability evidence, no broad theorem-proving proof, and no general model reliability claim. |

## Forbidden Claims Or Actions

- Do not change scoring criteria after seeing responses.
- Do not use Claude as scoring authority or response worker.
- Do not replace or repair responses.
- Do not score prompt polish as task success.
- Do not promote candidate-only stressors to primary dimensions.
- Do not declare C better than B if C has any hard-veto, malformed-output, or
  primary-dimension regression relative to B on any case.
- Do not declare C better than B from aggregate counts alone.
- Do not claim public benchmark validity, release readiness, scientific
  validation, product capability, broad theorem proving, proof correctness
  beyond scoped obligations, or general model reliability.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- scored JSON and Markdown exist and parse/check cleanly;
- scored JSON contains exactly 18 rows;
- hard vetoes are summarized before required-pass counts;
- condition and per-case B/C summaries are present;
- C-over-B interpretation obeys the frozen rule;
- Phase 4 result exists and records checks;
- Phase 5 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  next-phase handoff, and stop conditions.

## Stop Conditions

Stop if:

- response manifest or scoring contract fails to parse;
- response files or hashes do not match the manifest;
- scoring would require changing the frozen criteria;
- a response row cannot be scored without inventing missing evidence;
- aggregate counts conflict with per-case hard-veto or regression evidence;
- any release/public/scientific/product/general-reliability claim would be
  required to proceed;
- Phase 5 review requires an unavailable or unapproved external-review model
  and no human waiver/substitute direction exists.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 4 result/close record;
3. draft or refresh the Phase 5 review/decision subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. stop before Phase 5 if reviewer-model or human-boundary conditions are not
   satisfied.
