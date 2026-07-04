# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `mathdevmcp-v2-collection-final-state`
Supervisor/executor: Codex
Reviewer: Claude Sonnet max read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, collect
responses, score responses as authority, approve boundary crossings, or act as
execution authority. Claude is advisory only; Codex remains supervisor and
executor.

## Objective

Review the current final-state v2 collection/scoring artifacts for
consistency, correctness, feasibility of the recorded evidence, artifact
coverage, stale-state repair, and boundary safety.

This is not response collection authorization. It is not a request to inspect
the whole repository.

## Context Summary

Earlier Phase 0/1 review bundles described a pre-collection state with zero
response artifacts. The current workspace is later: local collection and
scoring artifacts now exist. Codex identified the stale-state mismatch and
patched the runbook status to `LOCAL_DIAGNOSTIC_COMPLETE_PENDING_FINAL_EXTERNAL_REVIEW`.

Current local validation summary:

- prompt count: 18;
- prompt manifest sha256:
  `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe`;
- prompt validation errors: 0;
- collection authorization record status:
  `collection_authorized_by_current_human_approval_for_exact_scope`;
- response count: 18;
- scored rows: 18;
- missing response/scored ids: none;
- response hash mismatches: none;
- Claude response-worker markers: none;
- retry issues: none;
- hard vetoes A/B/C: 0/0/0;
- required passes A/B/C: 6/5/6;
- candidate rule pass: true;
- improved case: `V2-PRP-01-gaussian-score-review-packet`;
- focused pytest:
  `python3 -m pytest tests/test_downstream_usefulness_prompts.py`: 3 passed;
- diff whitespace check over v2 artifacts/plans/reviews: clean.

## Artifacts To Inspect

Inspect only these bounded local artifacts as needed:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-final-state-consistency-audit-2026-07-04.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-stop-handoff-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-result-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-result-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-result-2026-07-03.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/collection_authorization_record.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`

Do not inspect generated response bodies unless a listed manifest/path
inconsistency makes that necessary. Do not inspect the whole repository.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the current final-state runbook and artifact set internally consistent and safely bounded as a local diagnostic pending/under final external review? |
| Baseline/comparator | Current authorization record, response manifest, frozen scoring contract, scored JSON/Markdown, Phase 3-5 results, final handoff, and final-state consistency audit. |
| Primary criterion | Agree only if the artifacts support a bounded local diagnostic, stale pre-collection claims have been repaired or clearly marked historical, Claude is not treated as response worker/scoring authority/boundary approver, and non-claims remain explicit. |
| Veto diagnostics | Reusing stale zero-response bundles as current evidence; unsupported collection approval claim; Claude response-worker use; hidden retry/replacement; scoring criteria changed after responses; hard-veto or malformed regression hidden; aggregate-only C-over-B claim; absent external review treated as agreement; unsupported public/release/scientific/product/proof/general-reliability claim. |
| Explanatory diagnostics | Counts, hashes, no-retry and no-Claude markers, per-case C-vs-B summary, focused pytest, diff whitespace, one-response limitation, manual scoring limitation. |
| Not concluded | No proof certificate, no release gate, no public benchmark result, no scientific validation, no product capability evidence, no broad theorem-proving proof, no funding claim, and no general model reliability. |

## Review Questions

1. Is there any material stale-state, consistency, correctness, feasibility,
   artifact coverage, or boundary-safety issue that should block final
   external-review closure?
2. Does the final handoff accurately distinguish the historical Phase 2 stop
   from the later completed local collection/scoring state?
3. Does the Phase 5 result preserve the local-diagnostic limitation and avoid
   treating absent Claude review as agreement?
4. Does the scored-result interpretation avoid aggregate-only promotion and
   unsupported C-over-B, release, public, scientific, product, proof, funding,
   or general-reliability claims?
5. Is there a fixable issue Codex should patch before marking final external
   review converged?

## Required Output

Return concise findings first. If there is a blocker, say exactly what
artifact or wording should be patched. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
