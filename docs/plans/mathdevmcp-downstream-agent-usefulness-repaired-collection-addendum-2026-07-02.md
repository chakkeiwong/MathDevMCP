# Repaired Collection Addendum

Date: 2026-07-02

Status: `REPAIRED_RESPONSE_COLLECTION_AUTHORIZED_BY_USER`

## Scope

The user waived the extra approval gate for repaired-prompt response
collection. This addendum authorizes one diagnostic repaired collection over:

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do repaired prompt fixtures, with A-condition leakage removed, produce a valid local A/B/C downstream-agent usefulness diagnostic? |
| Baseline/comparator | Repaired `A_task_only`, `B_evidence_only`, and `C_human_framed` prompt conditions. |
| Primary criterion | One recorded Codex-subagent response or malformed-output record per repaired prompt; no hidden retries; hard-veto-first scoring against the frozen Phase 1 rubric. |
| Veto diagnostics | Hidden retry, Claude as response worker, malformed output replaced, repaired prompt modified after collection starts, scoring rubric changed, A leakage persists, aggregate-only promotion, unsupported C superiority. |
| Explanatory diagnostics | Repaired response manifest, repaired score table, hard-veto counts, condition summaries, limitations. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped certified obligations, or general model reliability. |

## Collection Rules

- Use Codex subagents as response subjects.
- Do not use Claude as a response worker.
- Read one repaired prompt fixture per response subject.
- Do not browse.
- Do not inspect other files from response subjects.
- Do not retry malformed or incomplete outputs.
- Preserve raw response artifacts separately from the Phase 4 raw responses.

## Artifact Paths

- Raw repaired responses:
  `.mathdevmcp/downstream_agent_usefulness/responses_repaired_candidate/`
- Repaired response manifest:
  `.mathdevmcp/downstream_agent_usefulness/response_manifest_repaired_candidate.json`
- Repaired scoring artifacts:
  `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
  and
  `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`
- Repaired collection result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-repaired-collection-result-2026-07-02.md`

## Stop Conditions

Stop and record a blocker if:

- repaired prompt validation fails before collection;
- a response worker would require Claude;
- a model/agent surface produces no output and the failure cannot be recorded
  as a single outcome;
- scoring cannot be applied without changing the frozen rubric;
- a hard veto blocks any usefulness interpretation beyond diagnostic limits.
