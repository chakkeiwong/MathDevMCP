# Phase 4 Subplan: Scoring And Analysis

Date: 2026-07-01

Status: `LOCAL_REVIEWED_READY_AFTER_PHASE_3`

## Phase Objective

Score collected responses against the frozen rubric, compare prompt conditions,
and identify whether human-framed packets improve downstream agent work on the
local selected cases.

## Entry Conditions Inherited From Previous Phase

- Response manifest exists and matches the approved collection protocol.
- Rubric is frozen before scoring.
- No hard-veto or dimension criteria changed after response collection.

Phase 3 refresh note: the response manifest now exists at
`.mathdevmcp/agent_handoff_packet_calibration/response_manifest.json` with 15
responses for 15 frozen prompts. The response collection preserved one response
per prompt, no hidden retries, no malformed replacement, and no Claude response
worker.

## Local Skeptical Audit Before Execution

Audit result: passed.

- Wrong baseline risk: controlled by scoring A/B/C conditions from the same
  frozen case set and manifest.
- Proxy metric risk: controlled by hard-veto-first reporting and by treating
  artifact usefulness, context reuse, and efficiency as explanatory unless all
  required dimensions pass.
- Missing stop condition risk: scoring stops if response manifest is incomplete,
  if hard-veto handling becomes ambiguous, or if prompt leakage is found.
- Unfair comparison risk: Phase 2 froze identical skeleton/output/length/retry
  controls and B/C machine-evidence parity.
- Hidden assumption risk: scoring must record local/non-gating scope and cannot
  infer statistical or general model claims from five cases.
- Artifact-answerability risk: scored tables must preserve per-row notes and
  hard-veto counts before any condition summary.

## Required Artifacts

- Phase 4 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-04-scoring-analysis-result-2026-07-01.md`.
- Scored response table:
  `.mathdevmcp/agent_handoff_packet_calibration/scored_responses.json`.
- Human-readable comparison table:
  `.mathdevmcp/agent_handoff_packet_calibration/scored_responses.md`.
- Failure taxonomy note.
- Refreshed Phase 5 subplan.
- Ledger entry.

## Required Checks, Tests, And Reviews

- Validate scored JSON.
- Verify every response has per-dimension scores and hard-veto status.
- Verify aggregate summaries do not hide hard vetoes.
- Verify hard-veto rows are displayed before numeric or qualitative summaries.
- Verify artifact usefulness and context reuse are explanatory unless required
  correctness/boundary dimensions pass.
- Claude read-only review of scoring consistency and claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did the human-framed condition improve downstream agent work relative to baselines on the selected local cases? |
| Baseline/comparator | A/B conditions from same frozen case set and response protocol. |
| Primary criterion | Condition C improves or preserves required dimensions: correct next action, evidence use, boundary discipline, assumption discipline, and overclaim avoidance without introducing hard vetoes. Artifact usefulness/context reuse are explanatory unless required dimensions pass. |
| Veto diagnostics | Rubric applied inconsistently; aggregate score hides hard veto; soft proxy dimensions override correctness/boundary failures; scorer knows condition and biases interpretation without notes; result claims general model reliability. |
| Explanatory diagnostics | Per-case deltas, qualitative failure patterns, hard-veto counts, response excerpts within copyright/scope limits. |
| Not concluded | Universal packet superiority, model benchmark validity, release readiness, scientific validation, or proof correctness. |

## Forbidden Claims And Actions

- Do not retroactively change scoring criteria.
- Do not claim statistical significance from a five-case local calibration.
- Do not treat human-framed packets as proven optimal.
- Do not use Claude as scoring authority.
- Do not score if Phase 3 ended as a model-use blocker.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if:

- scored table exists and validates;
- hard vetoes are reported separately from aggregate scores;
- no hard-veto regression is hidden behind soft dimensions;
- Phase 4 result states local/non-gating interpretation and unresolved risks.

## Stop Conditions

Stop if:

- response manifest is incomplete;
- scoring cannot be applied consistently;
- hard-veto handling is ambiguous;
- results reveal prompt leakage requiring Phase 2 repair.

## End-Of-Phase Protocol

Run checks, write result, refresh/review Phase 5, append ledger, then advance or
stop.
