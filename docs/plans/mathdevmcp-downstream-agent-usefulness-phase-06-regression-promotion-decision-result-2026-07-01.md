# Phase 6 Result: Regression And Promotion Decision

Date: 2026-07-02

Status: `FINAL_NO_PROMOTION_REPAIRED_CANDIDATE_READY`

## Phase Objective

Run final regression checks and make a bounded downstream-agent usefulness
decision.

## Final Decision

Do not promote downstream-agent usefulness from this runbook.

The bounded decision is:

- Phase 4 response collection succeeded as an approved, one-response-per-prompt
  diagnostic collection.
- Phase 4 A/B/C comparison is invalid for promotion because the A baseline
  leaked evaluator/status fields.
- B and C rows passed locally but tied numerically; C superiority is not
  established.
- Phase 5 repaired candidate prompt fixtures and validation are ready.
- New repaired-prompt response collection requires explicit human approval.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | What bounded downstream-agent usefulness decision is justified by the produced artifacts? |
| Baseline/comparator | Phase 4 scored results plus Phase 5 repaired candidate prompts. |
| Primary criterion | Passed for bounded closeout: final decision preserves the A-leakage hard veto, non-claims, and recollection approval boundary. |
| Veto diagnostics | No aggregate score overrides hard veto; no repaired candidate prompt is treated as response evidence; no release/public/scientific/product/general reliability claim is made. |
| Explanatory diagnostics | Final summary, scored responses, failure taxonomy, repaired prompt validation, focused tests, and review-unavailability record. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, general model reliability, C-over-B superiority, or proof correctness beyond scoped certified obligations. |

## Final Summary Artifact

- `.mathdevmcp/downstream_agent_usefulness/final_summary.json`

## Checks Run

- `python3 -m pytest tests/test_downstream_usefulness_prompts.py tests/test_agent_handoff_packet.py`
  - `13 passed`
- Phase 6 JSON/prompt-contract validation script:
  - `phase6_validation_ok json=11 responses=27 current_leak_errors=18 repaired_errors=0`
- Forbidden-claim grep over downstream-usefulness docs/artifacts:
  - only explicit non-claims were found.
- `git diff --check -- src/mathdevmcp/downstream_usefulness_prompts.py tests/test_downstream_usefulness_prompts.py .mathdevmcp/downstream_agent_usefulness docs/plans/mathdevmcp-downstream-agent-usefulness-*.md`
  - clean

## Claude Review

Claude read-only final review was attempted with a compact final-decision brief.
It did not return a review. A tiny probe was also attempted. On interruption,
the review call reported:

`API Error: 500 model is not available. model: claude-opus-4-7`

This is recorded as reviewer unavailable, not approval. The final decision rests
on local checks and the explicit hard-veto evidence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close runbook without usefulness promotion | Passed for bounded closeout | A-leakage hard veto preserved; no promotion claim | Whether repaired prompts will produce a discriminating result | Ask for explicit approval before any repaired-prompt response collection | No C-over-B superiority, no release/public/scientific/product/general reliability claim |

## Next Human Decision

If the project wants an actual repaired usefulness result, the next step is a
new approved collection over:

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`

The approval should specify:

- prompt count;
- response-subject surface;
- retry policy;
- randomization or counterbalancing plan;
- artifact paths;
- whether to keep one response per prompt or collect replicated subjects.

Until that approval exists, the safe stopping point is this final closeout.
