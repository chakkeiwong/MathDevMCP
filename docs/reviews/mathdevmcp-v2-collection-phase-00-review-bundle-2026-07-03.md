# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `mathdevmcp-v2-collection-phase-00`
Supervisor/executor: Codex
Reviewer: Claude Opus max effort read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, collect responses, score responses, or act as execution
authority. Claude is advisory only; Codex remains supervisor and executor.

## Objective

Review Phase 0 governance/candidate freeze and the draft Phase 1 subplan for
consistency, correctness, feasibility, artifact coverage, and boundary safety.
This is a planning and governance review only. It is not response collection
authorization.

## Artifacts To Inspect

Inspect only these bounded local artifacts as needed:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-scoring-master-program-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-gated-execution-plan-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-subplan-2026-07-03.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json`

Do not inspect the whole repository. Do not inspect or mutate generated
response directories. There should be no v2 response artifacts.

## Context Summary

The v2 benchmark candidate was previously constructed and reviewed as a
candidate-only artifact. The new collection/scoring program is a gated program
whose next concrete work is approval-packet and scoring-contract preparation.

Phase 0 local checks:

- v2 prompt count: 18;
- cases: 6;
- condition counts: A/B/C = 6/6/6;
- prompt validation errors: 0;
- v2 response artifact count: 0;
- repaired baseline primary hash check: 11/11 matched;
- focused pytest: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`
  passed, 3 tests;
- `git diff --check` over v2 artifacts/plans/reviews passed.

Candidate freeze manifest hashes include:

- prompt manifest:
  `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe`;
- prompt validation:
  `17ef6e802137856acbdd155779c32a3148d75546d108444046a0e660a92fce70`;
- case manifest:
  `769a5911e4c5ebce1b46403ba4f2b6785421275e9c534f1ddfeed97d08471be5`;
- scoring applicability map:
  `4dc0e144c4d31d4f6f631b847c904b0dc834337dbe1a2389022f5ea7b7e1417b`;
- prompt directory aggregate:
  `8a4b488bbcbd730276e7bbb5834a7a426ebe6f97819281cb42ba0b637a7084d1`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Phase 0 safely closed as a candidate-freeze/governance phase, and is Phase 1 safe to execute as approval-packet/scoring-contract preparation only? |
| Baseline/comparator | V2 candidate artifacts, Phase 0 freeze manifest, repaired baseline hash manifest, and the collection/scoring master program. |
| Primary criterion | Review should agree only if the freeze state is coherent, response collection remains unauthorized, Phase 1 contains all required subplan fields, and the next phase cannot accidentally collect responses or change scoring after responses. |
| Veto diagnostics | Response collection; v2 response artifacts present; Claude as response worker; implied approval; assumed response-worker surface; scoring criteria dependent on future responses; candidate-only stressors silently promoted; unsupported C-over-B, release, public benchmark, scientific, product, funding, or general model-reliability claim. |
| Explanatory diagnostics | Hash list, prompt count, validation status, pytest result, Phase 1 required artifacts, stop conditions, non-claims. |
| Not concluded | No response quality, no scored v2 result, no downstream-agent usefulness claim, no C-over-B superiority, no release readiness, no public benchmark validity, no scientific validation, no product capability, no general model reliability. |

## Review Questions

1. Is there any material consistency, correctness, feasibility, artifact
   coverage, or boundary-safety issue that should block closing Phase 0?
2. Does the Phase 1 subplan include the required fields: objective, inherited
   entry conditions, artifacts, checks/reviews, evidence contract, forbidden
   claims/actions, next-phase handoff, and stop conditions?
3. Does the Phase 1 subplan preserve the approval boundary for prompt count,
   response-worker surface, retry policy, malformed-output policy, scoring
   contract, and artifact paths?
4. Does any artifact imply collection approval, Claude response-worker use,
   scoring drift after responses, or usefulness claims from candidate-only
   evidence?
5. Is there a fixable issue Codex should patch before advancing to Phase 1?

## Required Output

Return concise findings first. If there is a blocker, say exactly what artifact
or wording should be patched. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
