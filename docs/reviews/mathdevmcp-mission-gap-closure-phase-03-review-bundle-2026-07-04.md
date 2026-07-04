# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `mathdevmcp-mission-gap-closure-phase-03-r2`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Claude must not edit files, run experiments, launch agents, approve boundary
crossings, or act as execution authority. Codex remains supervisor and
executor.

## Objective

Review Phase 3 result and handoff to Phase 4 for correctness, feasibility,
artifact coverage, and boundary safety.

Phase 3 objective: cover realistic hard cases with compact handoff expectations
so agents see status, gaps/risks, non-claims, and next actions.

## Bounded Artifacts

Inspect only these local paths if needed:

- `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md`
- `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-result-2026-07-04.md`
- `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md`
- `src/mathdevmcp/math_review_packet.py`
- `tests/test_prepare_review_packet.py`

Do not inspect the whole repository. Treat unresolved questions as findings or
uncertainties rather than expanding scope.

## Implementation/Test Summary

Production repair:

- Compact handoff action normalization now accepts high-level action `code` as
  well as low-level action `kind`, emitting stable `next_actions[].kind`.

Case matrix coverage:

- missing assumptions;
- route gap;
- backend unavailable;
- not encodable;
- math/code mismatch;
- notation conflict;
- deterministic refutation;
- deterministic verification.

Repair since r1:

- First review returned `REVISE` because backend-unavailable coverage was
  promised but missing.
- Added a deterministic validated `backend_unavailable` high-level evidence
  fixture to the case matrix.
- This fixture does not depend on external backend availability.

## Local Evidence

Commands:

```text
python3 -m pytest tests/test_prepare_review_packet.py::test_prepare_review_packet_handoff_covers_realistic_case_matrix tests/test_math_review_packet.py tests/test_prepare_review_packet.py
13 passed in 0.27s

python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py
42 passed in 83.11s

python3 -m py_compile src/mathdevmcp/math_review_packet.py src/mathdevmcp/prepare_review_packet.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
passed

git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md
passed
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do realistic hard cases preserve correct statuses, risks, non-claims, and next actions through the handoff surface? |
| Baseline/comparator | Phase 2 representative workflow and current packet tests. |
| Primary criterion | Each selected case emits status, evidence/gap/risk, non-claim boundary, and next action appropriate to its evidence. |
| Veto diagnostics | False verification, missing non-claim boundary, missing next action, benchmark tuning, or pass/fail changes after seeing outputs. |
| Explanatory diagnostics | Per-case status table, action normalization repair, skipped cases with reason. |
| Not concluded | No comprehensive theorem-proving ability, downstream-agent reliability, public benchmark validity, or release readiness. |

## Review Questions

1. Does the action-normalization repair preserve boundaries and improve the
   product surface?
2. Is the case matrix sufficient for Phase 3's focused coverage objective?
3. Are the expectations conservative, especially for deterministic nested
   evidence that remains inside a diagnostic packet?
4. Does the refreshed Phase 4 subplan correctly prevent unapproved new
   model/API collection?
5. Did the backend-unavailable repair close the r1 coverage mismatch?
6. Is there any material reason to stop before Phase 4?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
