# Downstream-Agent Usefulness Visible Stop Handoff

Date: 2026-07-01

Status: `FINAL_REPAIRED_COLLECTION_COMPLETE_NO_PROMOTION`

## Current Phase

Runbook complete, with repaired-collection addendum complete.

## Current Status

Phases 0 through 3 passed or reached the intended response-collection gate under
local checks with Claude reviewer unavailable. Initial Claude compact review,
tiny probe, and Phase 1 compact review produced no usable output, so reviewer
unavailability is recorded as non-approval.

Phase 3 froze 27 prompt fixtures and stopped before response collection because
explicit approval was required for this exact new scope. The user approved that
scope on 2026-07-02. Phase 4 collected one Codex subagent response per frozen
prompt with no hidden retries and no Claude response worker.

Phase 4 scoring found a material benchmark-design flaw: all nine
`A_task_only` prompts leaked evaluator/status fields, so the A baseline is
contaminated and the A/B/C comparison cannot support a usefulness promotion.
B and C rows passed locally but tied numerically; C superiority is not
established.

Phase 5 created a repaired candidate prompt set and a prompt-condition
validator. The repaired candidate manifest validates with zero prompt-contract
errors.

Phase 6 closed the runbook without usefulness promotion. The final decision is
that the original Phase 4 result cannot support promotion because of the
A-condition leakage.

After that closeout, the user waived the additional repaired-collection
approval gate. The repaired addendum collected 27 Codex-subagent responses, one
per repaired prompt, with no hidden retries and no Claude response worker. The
original Phase 4 artifacts remain preserved.

The repaired result fixes the A-baseline validity problem for the local
diagnostic run. Repaired scoring found no hard vetoes, no malformed outputs, and
no repaired A prompt leakage. Required-pass counts are A = 8/9, B = 9/9, and
C = 9/9. C improves over A on the Joseph backend-certificate case, but C ties B
under the frozen required dimensions. Therefore no C-over-B usefulness
promotion is supported.

## Result Artifacts

- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-result-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-result-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-result-2026-07-01.md`
- `.mathdevmcp/downstream_agent_usefulness/benchmark_contract.json`
- `.mathdevmcp/downstream_agent_usefulness/scoring_rubric.json`
- `.mathdevmcp/downstream_agent_usefulness/case_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/evidence_class_matrix.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-result-2026-07-01.md`
- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/response_subject_policy.json`
- `.mathdevmcp/downstream_agent_usefulness/response_collection_approval_request.md`
- `.mathdevmcp/downstream_agent_usefulness/response_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-result-2026-07-01.md`
- `.mathdevmcp/downstream_agent_usefulness/failure_taxonomy.json`
- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/repaired_prompt_contract_validation.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-result-2026-07-01.md`
- `.mathdevmcp/downstream_agent_usefulness/final_summary.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-result-2026-07-01.md`
- `.mathdevmcp/downstream_agent_usefulness/responses_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/response_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-repaired-collection-result-2026-07-02.md`

## Known Boundaries

- Claude is read-only reviewer only.
- Claude is not a response worker or execution authority.
- Original Phase 4 A rows are not valid clean-baseline evidence because of
  condition-artifact leakage.
- Repaired A rows are valid for the repaired local diagnostic, but the repaired
  result still does not support C-over-B promotion.
- No release, public benchmark, product, scientific, or general model
  reliability claim is authorized.
- Claude final review was attempted but unavailable because the requested Opus
  model returned a server-side unavailable error.

## Next Safe Action

Stop. If continuing, design a harder replicated benchmark or revised prompt
contrast that can discriminate B from C without changing the frozen scoring
rubric post hoc. Do not claim C-over-B superiority from the repaired collection.
