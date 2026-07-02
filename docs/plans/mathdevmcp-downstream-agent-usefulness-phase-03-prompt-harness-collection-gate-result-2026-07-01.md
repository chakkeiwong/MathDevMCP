# Phase 3 Result: Prompt Harness And Collection Gate

Date: 2026-07-01

Status: `BLOCKED_PENDING_EXPLICIT_RESPONSE_COLLECTION_APPROVAL`

## Phase Objective

Build or validate frozen A/B/C prompt fixtures and response-collection harness
metadata, then stop for explicit response-collection approval if needed.

## Skeptical Audit

Checked before closing Phase 3:

- Wrong baseline: avoided. Prompts were generated from frozen Phase 1 contract
  and Phase 2 case manifest.
- Proxy metrics: avoided. Prompt completeness is not scored as downstream
  usefulness.
- Missing stop conditions: avoided. Phase 4 is blocked until exact human
  response-collection approval exists.
- Unfair comparison: controlled. Every case has exactly three prompt variants:
  A_task_only, B_evidence_only, and C_human_framed.
- Hidden assumptions: recorded. One response per prompt/no hidden retries is
  policy, but no response has been collected yet.
- Environment mismatch: no response worker, network model call, package
  install, or external data fetch was used.
- Artifact mismatch: artifacts freeze prompts and collection policy only.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are prompt fixtures and collection rules frozen enough to collect downstream-agent responses without hidden bias or approval drift? |
| Baseline/comparator | Phase 2 cases and Phase 1 A/B/C comparator contract. |
| Primary criterion | Passed for fixture readiness: prompt fixtures, manifest, response-subject policy, retry policy, and artifact paths are frozen before response collection. |
| Veto diagnostics | Passed: no response collection started, no Claude worker role, no hidden retries, no malformed-output replacement policy, no A/B/C count imbalance. |
| Explanatory diagnostics | Prompt manifest validation, prompt hashes, condition counts, response-subject policy, approval request note. |
| Not concluded | No usefulness result, model reliability, scoring result, response quality, or promotion decision. |

## Artifacts

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts/`
- `.mathdevmcp/downstream_agent_usefulness/response_subject_policy.json`
- `.mathdevmcp/downstream_agent_usefulness/response_collection_approval_request.md`

## Prompt Summary

| Field | Value |
| --- | --- |
| Case count | 9 |
| Conditions | `A_task_only`, `B_evidence_only`, `C_human_framed` |
| Prompt count | 27 |
| Condition balance | 9 prompts per condition |
| Response collection | Not started |
| Claude role | Read-only reviewer only, not response worker |

## Required Local Checks

| Check | Result |
| --- | --- |
| Prompt manifest validation | Passed: `prompt_manifest_valid`, condition counts `9/9/9`, case count `9`. |
| Fixture hash validation | Passed: every prompt file matches its manifest SHA-256. |
| Response policy check | Passed: `approval_required_before_collection=true`; Claude role is read-only reviewer only. |
| Response directory check | Passed: `no_responses_collected`. |
| `git diff --check` on downstream-usefulness artifacts | Passed. |

## Approval Needed For Phase 4

Phase 4 is blocked until the user explicitly approves this exact response
collection scope:

- response subject: Codex subagent or another explicitly approved non-Claude
  model/agent surface;
- prompt count: 27 prompts under
  `.mathdevmcp/downstream_agent_usefulness/prompts/`;
- retry policy: one response per prompt, no hidden retries;
- malformed output policy: record malformed or incomplete outputs, do not
  replace them;
- Claude role: read-only reviewer only, never response worker;
- artifact paths:
  `.mathdevmcp/downstream_agent_usefulness/response_manifest.json`,
  `.mathdevmcp/downstream_agent_usefulness/responses/`,
  `.mathdevmcp/downstream_agent_usefulness/scored_responses.json`, and
  `.mathdevmcp/downstream_agent_usefulness/scored_responses.md`.

## Claude Review Status

Claude remained unavailable from prior attempts. Phase 3 did not collect
responses, use Claude as worker, change scoring criteria, or cross a promotion
or scientific/product boundary.

## Next Subplan Review

Phase 4 subplan was reviewed locally for:

- sequencing: it requires frozen prompts and explicit approval;
- correctness: it enforces one recorded outcome per prompt and frozen rubric
  scoring;
- feasibility: it can proceed only after response-worker approval;
- artifact coverage: it requires response manifest, raw responses, scored
  outputs, hard-veto analysis, result, ledger, and stop handoff;
- boundary safety: it forbids hidden retries, malformed-output replacement,
  Claude as worker, changed rubric, and unsupported C superiority.

## Blocker Handoff

Do not start Phase 4 until explicit human approval is given for the exact scope
listed above. This is an intended runbook gate, not an error.
