# Phase 3 Subplan: Realistic Case Coverage

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

## Phase Objective

Cover realistic hard review cases with tests and handoff expectations so the
product does not only work on the representative happy path.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result names the active report/handoff surface:
  `prepare_review_packet(..., handoff=True)` and CLI
  `prepare-review-packet --handoff`.
- Phase 2 result covers one representative workflow: backend derivation
  evidence plus structural code audit packaged into compact handoff.
- Phase 2 result lists uncovered cases below.
- Existing proof boundaries and full JSON packet access remain intact.

## Required Artifacts

- Test cases or fixtures for these uncovered realistic cases:
  - missing assumptions;
  - route gap or diagnostic-only route;
  - backend unavailable or not encodable;
  - math/code mismatch;
  - notation conflict;
  - deterministic refutation;
  - deterministic verification under explicit assumptions when local backend
    evidence is available.
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-result-2026-07-04.md`
- Refreshed Phase 4 subplan defining the v2 regression guard inputs.

## Required Checks, Tests, And Reviews

- Focused pytest for the new/updated case coverage.
- `python3 -m pytest tests/test_math_review_packet.py tests/test_prepare_review_packet.py`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py`
- `python3 -m py_compile src/mathdevmcp/math_review_packet.py src/mathdevmcp/prepare_review_packet.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
- `git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md`
- Bounded Claude read-only review for material case interpretation or boundary
  changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do realistic hard cases preserve correct statuses, risks, non-claims, and next actions through the handoff surface? |
| Baseline/comparator | Phase 2 representative workflow and current packet tests. |
| Primary criterion | Each selected case emits status, evidence/gap/risk, non-claim boundary, and next action appropriate to its evidence. |
| Veto diagnostics | False verification, missing non-claim boundary, missing next action, benchmark tuning instead of product behavior, or changed pass/fail semantics after seeing outputs. |
| Explanatory diagnostics | Per-case status table, skipped cases with reason, backend availability notes. |
| Not concluded | No comprehensive theorem-proving ability, downstream-agent reliability, public benchmark validity, or release readiness. |

## Forbidden Claims And Actions

- Do not make case tests assert unsupported mathematical truth.
- Do not promote structural matches to semantic code correctness.
- Do not hide backend unavailability.
- Do not add model-generated cases without approval.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- Phase 3 result contains a per-case decision table.
- Required checks pass.
- Any material review converges.
- Phase 4 subplan names whether it will replay existing v2 artifacts only or
  request approval for new model/API collection.

## Stop Conditions

Stop if:

- Required cases need external data/model calls not already approved.
- Test outcomes suggest a real boundary bug requiring redesign before more
  coverage.
- The phase starts optimizing for benchmark prompts instead of product cases.
