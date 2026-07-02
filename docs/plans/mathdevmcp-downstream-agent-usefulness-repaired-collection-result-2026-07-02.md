# Repaired Collection Result

Date: 2026-07-02

Status: `REPAIRED_COLLECTION_COMPLETE_NO_PROMOTION`

## Objective

Collect and score one downstream-agent response for each repaired prompt fixture
after the user waived the additional approval gate, while preserving the
original Phase 4 artifacts and keeping Claude out of the response-worker role.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Do repaired prompt fixtures, with A-condition leakage removed, produce a valid local A/B/C downstream-agent usefulness diagnostic? |
| Baseline/comparator | Repaired `A_task_only`, `B_evidence_only`, and `C_human_framed` prompt conditions. |
| Primary criterion | Passed for collection/scoring: 27/27 repaired responses recorded, no hidden retries, no malformed replacements, hard-veto-first scoring against the frozen Phase 1 rubric. |
| Veto diagnostics | Passed: no Claude response worker, no repaired prompt mutation during collection, no scoring-rubric mutation, no A leakage in repaired prompts, no aggregate-only promotion, no unsupported C-over-B claim. |
| Explanatory diagnostics | Repaired response manifest, repaired score table, hard-veto counts, condition summaries, prompt validation, limitations. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped certified obligations, or general model reliability. |

## Artifacts

- `.mathdevmcp/downstream_agent_usefulness/responses_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/response_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`

## Result

The repaired A/B/C comparison is valid as a local diagnostic because the
original A-condition evaluator/status leakage was removed and prompt validation
reports zero repaired prompt-contract errors.

Condition summary:

| Condition | Rows | Hard vetoes | Malformed | Prompt leaks | Required passes | Required total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 9 | 0 | 0 | 0 | 8 | 106/108 |
| `B_evidence_only` | 9 | 0 | 0 | 0 | 9 | 108/108 |
| `C_human_framed` | 9 | 0 | 0 | 0 | 9 | 108/108 |

Interpretation:

- Repaired A is now a valid baseline.
- C improves over A on the Joseph backend-certificate case because A lacked
  decisive certificate evidence for a proof-level pass.
- C ties B under the frozen required dimensions.
- The minimum candidate rule does not pass because
  `c_better_than_b_on_predeclared_usefulness_axis` is false.

## Skeptical Audit

- Wrong baseline: fixed relative to Phase 4. The repaired A baseline validates
  with zero prompt-contract errors.
- Proxy metrics: avoided. Prompt completeness and packet polish are not treated
  as task success; rows are scored against downstream task outcome, evidence,
  reasoning, gaps, boundaries, and actionability.
- Missing stop conditions: avoided. The result stops at local diagnostic
  evidence and does not promote C over B.
- Unfair comparison: improved but still limited. A/B/C are valid prompt
  conditions, but A remains strong because it includes bounded summaries and
  guardrails; B/C ceiling effects limit discrimination.
- Hidden assumptions: preserved as limitations. One response per prompt and
  non-randomized collection are not general model evidence.
- Artifact mismatch: avoided. The repaired score artifacts answer the repaired
  collection question; they do not revise or overwrite original Phase 4 raw
  responses.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close repaired collection without C-over-B promotion | Passed for local diagnostic collection and scoring | No hard vetoes; no repaired A leakage; no unsupported promotion | Ceiling effect and one-response-per-prompt variance limit discriminability | Design a harder replicated benchmark only if the project wants a stronger C-vs-B test | No release/public/scientific/product/general-reliability claim; no C-over-B superiority |

## Close Record

The repaired collection is complete. The benchmark-design blocker from Phase 4
is repaired for this diagnostic run, but the repaired result still does not
support a C-over-B usefulness promotion.
