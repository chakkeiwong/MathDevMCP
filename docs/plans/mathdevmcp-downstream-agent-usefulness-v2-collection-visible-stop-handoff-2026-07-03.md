# V2 Collection And Scoring Visible Stop Handoff

Date: 2026-07-03

Status: `COMPLETE_LOCAL_DECISION_CLAUDE_REVIEW_WAIVED_FOR_THIS_RUN`

## Current Status

The v2 collection/scoring program launched in visible gated planning mode.
Phase 0 local checks passed and the candidate freeze artifacts were written.
The required Claude Opus read-only review gate did not reach material review:
two attempts returned `probe_timeout`, and a later attempt after explicit
informed approval to send the bounded bundle to Claude/Anthropic returned
`transport_down` because the `opus` alias resolved to unavailable
`claude-opus-4-7`. No-bundle probes showed `sonnet` transport works, while
tested Opus aliases were unavailable or unsupported. No Claude-review waiver
has been recorded.

Phase 1 created the approval packet and frozen scoring contract. Phase 2
preflight passed local checks and previously stopped because collection
approval was incomplete. A later current resumed approval authorized the exact
Phase 3 collection scope: 18 frozen prompts, Codex subagents via
`multi_agent_v1.spawn_agent`, one visible attempt per prompt, malformed-output
preservation, frozen scoring contract, and the named response/scoring artifact
paths.

Phase 3 collection is now complete: 18/18 response artifacts were collected,
with no hidden retries, no malformed-output replacements, and no Claude
response worker. Phase 4 hard-veto-first scoring is complete locally: hard
vetoes A/B/C = 0/0/0, required passes A/B/C = 6/5/6, and C ties B on five
cases while improving on the Gaussian-score review-packet case. Phase 5 final
decision is complete with Claude review waived for this run.

## Stop Policy

Stop and update this handoff if:

- collection approval is incomplete;
- Claude is proposed as response worker;
- prompt validation fails and cannot be repaired;
- scoring criteria would need to change after seeing responses;
- response collection requires unapproved network/API/funding/model-file
  boundaries;
- any public/scientific/product/release/general-reliability claim would be
  required.

## Final Handoff Fields

Final phase reached:

- Phase 2: Preflight And Collection Gate.

Final status:

- `BLOCKED_PENDING_COLLECTION_APPROVAL`.

Artifacts produced:

- `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/collection_approval_packet.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/collection_preflight_report.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md`
- `docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-result-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-result-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-result-2026-07-03.md`

Local checks run:

- v2 JSON parse: passed.
- prompt count: 18.
- prompt validation errors: 0.
- v2 response artifact count: 0.
- repaired baseline primary hashes: 11/11 matched.
- focused pytest: 3 passed.
- diff whitespace check: clean.
- Phase 1/2 local checks: JSON parse, prompt hash check, approval completeness
  check, response artifact absence check, focused pytest, and diff whitespace
  check passed.

Claude review status:

- Not converged. One permission-layer attempt timed out before execution.
- Two launched `claude_review_gate.sh` attempts returned
  `REVIEW_STATUS=probe_timeout`, `VERDICT=NONE`.
- The second launched attempt used `--probe-timeout 240`.
- A third launched Phase 0 gate after explicit informed external-review
  approval returned `REVIEW_STATUS=transport_down`, `VERDICT=NONE`, because
  `claude-opus-4-7` was unavailable.
- No-bundle `sonnet` probe returned `OK`.
- No-bundle Opus 4.6 and 4.5 probes were unavailable or unsupported.

Unresolved blocker:

- Response collection remains unauthorized until explicit collection approval
  names prompt count, response-worker surface, retry policy, malformed-output
  policy, scoring contract, and artifact paths.

Human direction received:

- explicit informed approval to send the bounded Phase 0 review bundle to
  Claude/Anthropic despite the non-public workspace artifact exfiltration
  risk.
- no waiver of Claude review has been recorded.

Reviewer-model direction still needed:

- retry Opus later;
- approve Sonnet max effort as substitute read-only reviewer for this
  planning-only gate;
- explicitly waive Claude review for this planning-only boundary.

Latest reviewer-model attempt:

- Human selected `1`, interpreted as retry Opus.
- A no-bundle Opus probe failed with:
  `API Error: 500 model is not available. model: claude-opus-4-7`.
- No review bundle was sent on that retry.

Exact approval needed for Phase 3:

- prompt manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`;
- prompt count: 18;
- response-worker surface: explicitly named non-Claude model/agent surface;
- retry policy: one visible attempt per prompt, no hidden retries, unless a
  different replicated design is approved before launch;
- malformed-output policy: preserve malformed, empty, partial, or off-schema
  outputs and score them as malformed; do not replace them;
- scoring contract:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`;
- response artifact directory:
  `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/`;
- response manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`;
- scored outputs:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
  and
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.

What was not concluded:

- No response quality result.
- No scored v2 result.
- No C-over-B superiority.
- No response collection authorization.
- No release, public benchmark, scientific, product, funding, or general
  model-reliability claim.

Template fields retained for future stop/completion updates:

- final phase reached;
- final status;
- artifacts produced;
- local checks run;
- Claude review status;
- unresolved blockers;
- exact approval needed for future collection if stopped before collection;
- what was not concluded.
