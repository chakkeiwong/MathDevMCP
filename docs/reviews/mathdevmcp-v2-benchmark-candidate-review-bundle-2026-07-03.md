# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `mathdevmcp-v2-benchmark-candidate-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, collect responses, score responses, or act as execution
authority.

## Objective

Review whether the completed downstream-agent usefulness benchmark v2
candidate is internally consistent, boundary-safe, and ready to stop at
candidate handoff before any response collection.

This is a review of benchmark-maintenance artifacts only. It is not a request
to collect responses or decide C-over-B superiority.

## Artifacts To Inspect

Inspect only these bounded local artifacts as needed:

- `.mathdevmcp/downstream_agent_usefulness_v2/result_note_candidate.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/case_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/adversarial_ceiling_analysis.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-result-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-stop-handoff-2026-07-02.md`

Do not inspect the whole repository. Do not inspect or mutate generated
response directories. There should be no v2 response artifacts.

## Context Summary

The repaired baseline remains frozen under
`.mathdevmcp/downstream_agent_usefulness/`. The v2 candidate lives separately
under `.mathdevmcp/downstream_agent_usefulness_v2/`.

Completed v2 candidate summary:

- 6 candidate cases;
- 18 prompt fixtures: 6 cases x A/B/C;
- prompt validation errors: 0;
- v2 response artifacts: 0;
- repaired primary baseline hash recheck: 11/11 matched;
- focused pytest passed: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`;
- `git diff --check` passed over v2 plans/artifacts.

Claude was previously probed through the wrong direct worker path and timed
out. This bundle is intended to close that review gap using the proper
`claude_review_gate.sh` flow.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the v2 benchmark candidate complete as a local maintenance artifact, with exact future collection approval boundaries and no unauthorized response collection? |
| Baseline/comparator | Frozen repaired benchmark baseline and v2 candidate artifacts under `.mathdevmcp/downstream_agent_usefulness_v2/`. |
| Primary criterion | Review should agree only if artifacts are internally consistent, prompt/collection boundaries are explicit, no response collection is implied, and final status stops at candidate readiness. |
| Veto diagnostics | Response collection; Claude as response worker; repaired baseline mutation; prompt validation errors ignored; hidden retries; scoring criteria drift after responses; prompt polish treated as task success; unsupported C-over-B, release, public benchmark, scientific, product, or general model-reliability claim. |
| Explanatory diagnostics | Artifact coverage, risk table, runbook approval checklist, prompt validation summary, residual B-ceiling risk. |
| Not concluded | No scored v2 result, no downstream-agent usefulness claim, no C-over-B superiority, no tool improvement, no model reliability, no release readiness, no public benchmark validity, no scientific validation, no product capability. |

## Review Questions

1. Is there any material consistency, correctness, feasibility, artifact
   coverage, or boundary-safety issue that should block the v2 candidate
   handoff?
2. Does the future collection runbook preserve the required approval boundary:
   prompt count, response-worker surface, retry policy, malformed-output
   policy, scoring contract, and artifact paths?
3. Do the artifacts avoid treating prompt validity, synthetic case design, or
   C framing as scored usefulness evidence?
4. Do the non-claims and Claude role boundaries remain explicit enough?
5. Is there any fixable issue Codex should patch before considering the review
   gap closed?

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
