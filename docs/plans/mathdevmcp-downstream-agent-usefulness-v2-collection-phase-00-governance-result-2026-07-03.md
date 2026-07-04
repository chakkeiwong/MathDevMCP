# Phase 0 Result: Governance And Candidate Freeze

Date: 2026-07-03

Status: `SONNET_REVIEW_R1_REVISE_REPAIR_IN_PROGRESS`

## Phase Objective

Freeze the v2 candidate state, approval boundaries, role contract, and Claude
review-gate process before writing approval/scoring artifacts or considering
response collection.

## Result Summary

Phase 0 local checks passed and the candidate freeze artifacts were written.
The material Claude Opus review gate did not converge. After one
permission-layer timeout, two launched gate attempts returned
`REVIEW_STATUS=probe_timeout`. After explicit informed human approval to send
the bounded Phase 0 bundle to Claude/Anthropic, a third launched gate reached
the gateway but returned `REVIEW_STATUS=transport_down` because the configured
`opus` alias resolved to unavailable `claude-opus-4-7`.

Separate no-bundle probes showed that Claude transport/auth is alive for
`sonnet`, but tested Opus aliases are unavailable or unsupported. No human
waiver of Claude review was given. The Phase 0 material bundle remains
unreviewed by Claude.

## Artifacts Produced

- Candidate freeze manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`.
- Draft Phase 1 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md`.
- Claude review bundle:
  `docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md`.
- Updated execution ledger:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-execution-ledger-2026-07-03.md`.

## Local Checks

| Check | Status | Evidence |
| --- | --- | --- |
| v2 JSON parse | pass | prompt manifest, prompt validation, and case manifest parsed with `python3 -m json.tool`; freeze manifest parsed after creation |
| Prompt count | pass | 18 prompts, 6 cases, A/B/C counts 6/6/6 |
| Prompt validation | pass | `validation_errors: []` |
| V2 response artifacts | pass | count 0 |
| Repaired baseline hashes | pass | 11/11 primary artifacts matched |
| Focused pytest | pass | `python3 -m pytest tests/test_downstream_usefulness_prompts.py`: 3 passed |
| Diff whitespace | pass | `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-*.md docs/reviews`: clean |

## Claude Review Gate Attempts

Required command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name mathdevmcp-v2-collection-phase-00 \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md \
  --model opus \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Attempt 1:

- requested elevated/trusted execution for the narrow review-gate command;
- permission approval review timed out before a decision;
- Claude was not invoked.

Attempt 2:

- retried the same narrow review-gate command;
- command launched;
- gate result:
  `REVIEW_STATUS=probe_timeout`, `VERDICT=NONE`;
- `RUN_DIR`:
  `.claude_reviews/20260703-210129-mathdevmcp-v2-collection-phase-00`;
- `SUMMARY_JSON`:
  `.claude_reviews/20260703-210129-mathdevmcp-v2-collection-phase-00/status.json`.

Attempt 3:

- reran the same bundle with a longer probe timeout:
  `--probe-timeout 240 --timeout-seconds 180`;
- command launched;
- gate result:
  `REVIEW_STATUS=probe_timeout`, `VERDICT=NONE`;
- `RUN_DIR`:
  `.claude_reviews/20260703-211758-mathdevmcp-v2-collection-phase-00-r2`;
- `SUMMARY_JSON`:
  `.claude_reviews/20260703-211758-mathdevmcp-v2-collection-phase-00-r2/status.json`.

No further retry was run because the probe itself timed out twice, including
with a 240 second timeout. Since the probe prompt is just `Reply exactly: OK`,
redesigning the material review bundle would not address this failure mode.

Attempt 4:

- ran after explicit informed human approval for sending the bounded Phase 0
  bundle to Claude/Anthropic;
- gate result:
  `REVIEW_STATUS=transport_down`, `VERDICT=NONE`;
- `RUN_DIR`:
  `.claude_reviews/20260703-215201-mathdevmcp-v2-collection-phase-00-r3`;
- `SUMMARY_JSON`:
  `.claude_reviews/20260703-215201-mathdevmcp-v2-collection-phase-00-r3/status.json`;
- probe stdout reported:
  `API Error: 500 model is not available. model: claude-opus-4-7`.

Follow-up no-bundle probes:

- `sonnet` returned `OK`, so Claude transport/auth is available.
- `claude-opus-4-6` returned model unavailable.
- `claude-opus-4-5` returned unsupported.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Locally answered for candidate freeze; not fully review-closed because Claude Opus is unavailable |
| Baseline/comparator | v2 candidate artifacts and repaired baseline hash manifest |
| Primary criterion | not met for Claude-reviewed closure; local checks passed but the required Opus material review did not run |
| Veto diagnostics | no response artifacts, no validation errors, no baseline mismatch, no collection authorization, no Claude-as-worker use |
| Explanatory diagnostics | hashes, prompt count, validation status, pytest result, Opus model-unavailable blocker, Sonnet transport probe success |
| Not concluded | no response quality, no scored v2 result, no C-over-B superiority, no release/public/scientific/product/general-reliability claim |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop for reviewer-model direction before treating Phase 0 as Claude-reviewed | blocked by Opus model unavailability | no local veto failed | whether to retry Opus later or allow Sonnet max as substitute reviewer for this planning gate | ask human for reviewer-model direction; preserve no-collection boundary | no usefulness result, no C-over-B claim, no collection authorization |

## Human Direction Needed

Human explicitly approved sending the bounded Phase 0 bundle to
Claude/Anthropic despite the non-public workspace artifact exfiltration risk.
That approval did not waive Claude review.

Safe next options:

- retry Opus later;
- explicitly approve Sonnet max effort as the read-only reviewer substitute
  for this planning-only gate;
- explicitly waive Claude review for this planning-only boundary.

Do not collect responses without explicit collection approval.

## Latest Reviewer Retry

The human selected `1`, interpreted as retry Opus. A no-bundle Opus probe was
run before sending any review bundle and failed with:

```text
API Error: 500 model is not available. model: claude-opus-4-7
```

The bounded Phase 0 review bundle was not sent on this retry. Opus remains
unavailable through the current gateway.

## Substitute Reviewer Gate

The human approved Sonnet max as substitute read-only reviewer. Sonnet review
round 1 ran on the bounded Phase 0 review bundle and returned:

- `REVIEW_STATUS=revise`;
- `VERDICT=REVISE`;
- `RUN_DIR=.claude_reviews/20260703-230309-mathdevmcp-v2-collection-phase-00-sonnet-r1`;
- blocker: Phase 1 next-phase handoff incorrectly treated pending
  reviewer-model direction as sufficient to advance.

Repair action:

- Tighten Phase 1 handoff wording so pending reviewer-model direction remains
  a stop state. Phase 2 may proceed only after a converged bounded reviewer
  verdict or explicit human waiver/direction for local-only planning.
