# Downstream-Agent Usefulness Benchmark V2 Candidate Result Note

Date: 2026-07-02

Status: `CANDIDATE_READY_FOR_HUMAN_COLLECTION_APPROVAL_NO_RESPONSES_COLLECTED`

## Objective

Create a harder v2 benchmark candidate that can later test whether
human-framed handoff prompts help downstream agents more than compact
machine-evidence prompts, while preserving repaired-baseline artifacts and
stopping before response collection.

## Result

The v2 candidate artifact set is complete for local maintenance review:

- cases: 6;
- prompt conditions: A/B/C;
- prompt fixtures: 18;
- prompt-contract validation errors: 0;
- high C-sensitivity cases: 4;
- v2 response artifacts: 0;
- repaired primary baseline hash recheck: 11/11 matched.

## Artifacts

- `.mathdevmcp/downstream_agent_usefulness_v2/baseline_hash_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/ceiling_effect_analysis.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/difficulty_requirements.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/case_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompts_candidate/`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/adversarial_ceiling_analysis.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close v2 candidate as ready for human collection approval | Passed: candidate artifacts and local checks complete | Passed: no responses collected, no Claude worker role, no prompt validation errors, no repaired baseline mutation | Whether B remains at ceiling under future responses | Ask for explicit human approval before any collection | No scored v2 result, no C-over-B superiority, no model reliability, no release/public/scientific/product claim |

## Required Future Approval

Future response collection requires explicit human approval for:

- prompt manifest and prompt count: 18 prompts;
- response-worker surface; Claude is forbidden as a response worker;
- retry policy;
- malformed-output policy;
- scoring contract;
- artifact paths for responses, response manifest, and scored responses.

## Non-Claims

This candidate does not establish:

- downstream-agent usefulness;
- C-over-B superiority;
- tool improvement;
- model reliability;
- release readiness;
- public benchmark validity;
- scientific validation;
- product capability.
