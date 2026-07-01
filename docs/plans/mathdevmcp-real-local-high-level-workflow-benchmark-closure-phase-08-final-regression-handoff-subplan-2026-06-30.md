# Phase 8 Subplan: Final Regression And Handoff

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_7`

## Phase Objective

Run final focused regressions, produce final benchmark/report artifacts, and
write the visible stop handoff with exact residual risks and non-claims.

## Entry Conditions Inherited From Previous Phase

- Phases 0-7 have passed or documented accepted residuals.
- Benchmark manifest/report, workflow repairs, packet standard, and docs/policy
  artifacts exist.
- No unresolved human-required boundary remains.

## Required Artifacts

- Final benchmark/report JSON under `.mathdevmcp/`.
- Final matrix artifact with per case: expected route, actual route, verdict,
  failure class, repair round, remaining limitation, and local-regression-only
  versus future governed benchmark-candidate status.
- Phase 8 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-08-final-regression-handoff-result-2026-06-30.md`.
- Final visible stop handoff update.
- Updated ledger entry.

## Required Checks, Tests, And Reviews

- Run focused high-level workflow, benchmark, CLI/MCP, and docs tests touched by
  the program.
- Run real-local benchmark report/quality command.
- Verify final matrix exists and matches final report cases.
- Run benchmark gate only as existing-suite regression unless Phase 7
  explicitly approved promotion.
- Run forbidden-claim grep.
- Final Codex skeptical audit; Claude final review if permitted and not blocked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did the program close the real-local high-level workflow benchmark gap under the stated evidence boundaries? |
| Baseline/comparator | Phase 0 current baseline and Phase 4 pre-repair benchmark run. |
| Primary criterion | Final reports show benchmark cases, final matrix, per-case statuses, improved or explicit residual behavior, stable packets/docs, and no boundary/regression failures. |
| Veto diagnostics | Failed focused tests; hidden wrong/boundary cases; aggregate-only reporting; missing final matrix; artifact does not answer the closure question; release/scientific/public/broad-proof claims; benchmark gate silently changed. |
| Explanatory diagnostics | Final test counts, benchmark summaries, residual table, docs grep, review trail. |
| Not concluded | Release readiness, public benchmark validity, scientific validation, production implementation correctness, external reproducibility, full LaTeX proof checking, or broad theorem proving. |

## Forbidden Claims And Actions

- Do not claim all future derivations/proofs are handled.
- Do not claim external/public benchmark validity.
- Do not claim release readiness or scientific validation.
- Do not hide residual cases or abstentions.
- Do not alter benchmark policy after seeing final results.

## Exact Next-Phase Handoff Conditions

No automatic next phase. Final handoff must state final phase reached, final
status, artifacts, tests run, Claude review trail, unresolved blockers,
non-claims, and safest next human decision.

## Stop Conditions

Stop with blocked/partial handoff if final tests fail, reports are not
reproducible, docs overclaim, or unresolved human-required boundaries remain.

## End-Of-Phase Protocol

At phase end: run checks; write Phase 8 result; update final handoff; review
final artifacts for consistency, correctness, feasibility, artifact coverage,
and boundary safety.
