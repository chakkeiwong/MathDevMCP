# Phase 4 Result: Hard-Veto-First Scoring

Date: 2026-07-03

Status: `COMPLETE_LOCAL_DIAGNOSTIC_READY_FOR_PHASE_5_REVIEW_DECISION`

## Phase Objective

Score the 18 collected v2 response artifacts under the frozen collection
scoring contract, applying hard vetoes before required-pass counts and
producing bounded local diagnostic artifacts.

## Result Summary

Phase 4 passed locally. Scored JSON and Markdown artifacts were written and
validated.

Hard vetoes: A = 0, B = 0, C = 0. Required-pass counts: A = 6/6, B = 5/6,
C = 6/6. Under the frozen per-case comparison rule, C ties B on five cases and
improves on the Gaussian-score review-packet case, where the B response is a
sparse diagnostic status while the C response gives a self-contained review
question, gaps, veto risks, and next artifact.

This supports only a bounded local C-over-B diagnostic for this single-response
run. It is not a public benchmark result, release gate, scientific validation,
product capability claim, broad theorem-proving claim, proof-correctness claim
beyond scoped obligations, or general model-reliability claim.

## Artifacts Produced

- Scored JSON:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`.
- Scored Markdown:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.
- Phase 4 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-result-2026-07-03.md`.
- Draft Phase 5 review/decision subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-subplan-2026-07-03.md`.
- Updated execution ledger and stop handoff.

## Checks

| Check | Result |
| --- | --- |
| Response manifest JSON parse | Passed |
| Scoring contract JSON parse | Passed |
| Scored JSON parse | Passed |
| Scored row count | Passed: 18 |
| Required dimensions present on every row | Passed |
| Explanatory dimensions present on every row | Passed |
| Required-pass flags match score floors/hard veto/malformed state | Passed |
| Response artifact paths exist | Passed |
| Per-case C-vs-B rule violations | Passed: 0 |
| Hard-veto-first Markdown summary | Passed |
| Focused pytest | Passed: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`, 3 tests |
| Diff whitespace | Passed |

## Hard-Veto-First Summary

| Condition | Rows | Hard vetoes | Malformed | Required passes | Required total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 6 | 0 | 0 | 6 | 72/72 |
| `B_evidence_only` | 6 | 0 | 0 | 5 | 69/72 |
| `C_human_framed` | 6 | 0 | 0 | 6 | 72/72 |

## Per-Case C-vs-B Decision

| Case | C vs B | Primary reason |
| --- | --- | --- |
| `V2-DF-01-affine-matrix-domain-obligation` | tied | B and C both preserve scalar-vs-matrix obligations and abstain from overclaiming derivation. |
| `V2-PC-01-domain-restricted-counterexample` | tied | B and C both distinguish unrestricted witness evidence from restricted-domain proof/refutation. |
| `V2-AF-01-masked-likelihood-score-assumptions` | tied | B and C both identify same-scalar, mask, covariance-domain, and differentiability obligations. |
| `V2-AMC-01-logdet-quadratic-code-trace` | tied | B and C both flag the unresolved quadratic solve term without code-global overclaim. |
| `V2-DD-01-first-gap-product-rule` | tied | B and C both identify Step 2 as the first product-rule failure. |
| `V2-PRP-01-gaussian-score-review-packet` | better | C gives a self-contained review packet with question, gaps, risks, and next artifact; B is too sparse for a full required pass. |

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Answered locally: under the frozen scoring contract, C improves over B on one case and has no hard-veto, malformed-output, or primary-dimension regression. |
| Baseline/comparator | Per-case B_evidence_only rows were the primary comparator; A_task_only rows were diagnostic context. |
| Primary criterion | Passed: scored JSON/Markdown exist and parse/check cleanly; hard vetoes are reported before pass counts; C-vs-B decision follows the frozen per-case rule. |
| Veto diagnostics | Passed: no scoring criteria change, no Claude response-worker use, no hidden retry/replacement, no hidden malformed-output or hard-veto regression, no candidate-only stressor promotion, no prompt-polish scoring, no aggregate-only promotion, and no unsupported public/scientific/product/release/general-reliability claim. |
| Explanatory diagnostics | Per-row scores, condition totals, per-case B/C deltas, candidate-stressor notes, malformed-output count, limitations. |
| Not concluded | No proof certificate, no release gate, no public benchmark result, no scientific validation, no product capability evidence, no broad theorem-proving proof, and no general model reliability claim. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4 as bounded local C-over-B diagnostic | Passed | No veto triggered | One response per prompt and manual local scoring limit generality | Run Phase 5 review/decision if reviewer boundary is available or explicitly waived | No public/release/scientific/product/general-reliability claim and no broad proof capability claim |

## Phase 5 Handoff

Phase 5 should review the scored artifacts and write the final bounded
decision. Claude may be used only as read-only reviewer if an approved and
available reviewer model exists. If reviewer access remains unavailable and no
waiver is given, Phase 5 should stop with a review-boundary handoff rather than
overclaiming the scored result.
