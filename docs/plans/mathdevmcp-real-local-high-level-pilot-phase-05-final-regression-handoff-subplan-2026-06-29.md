# Phase 05 Subplan: Final Regression And Handoff

## Phase Objective

Run final focused regressions, write the final result/handoff, and identify the
next justified implementation program.

## Entry Conditions Inherited From Previous Phase

- Phase 04 integration/docs decision is complete.
- The local pilot remains non-gating.
- No open phase blocker remains unresolved.

## Required Artifacts

- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-result-2026-06-29.md`
- Stop/final handoff:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-visible-stop-handoff-2026-06-29.md`
- Updated execution ledger and review trail.

## Required Checks, Tests, And Reviews

- Local checks:
  - Focused pilot tests.
  - Focused high-level workflow tests.
  - Pilot report command if available.
  - `python3 -m pytest` subset appropriate to touched files.
  - Optional non-gating regression observation may run
    `python3 -m mathdevmcp.cli benchmark-gate --root "$PWD"` only as an
    existing-suite regression check. It must not add pilot cases to benchmark
    totals or be cited as pilot promotion evidence.
- Review:
  - Codex final self-review required.
  - Claude read-only review required for final interpretation if material
    code/docs changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the local real-source high-level pilot implemented, checked, and handed off with correct boundaries? |
| Baseline/comparator | Phase 00 baseline and existing seeded high-level benchmark/benchmark gate. |
| Primary pass criterion | Required focused tests pass, pilot report passes, result/handoff preserve non-claims, report channels remain separate, and no unintended gate/release policy changes occurred. |
| Veto diagnostics | Failed focused tests, missing final report, blended pilot accuracy metric, benchmark-gate regression from touched files, unsupported claim in docs/result, unresolved Claude/Codex review blocker. |
| Explanatory diagnostics | Test counts, report summary, dirty-worktree/touched-file note. |
| Not concluded | Release readiness, external benchmark validity, scientific proof of source cases, public fixture readiness. |
| Artifacts | Final phase result, stop handoff, ledger, review trail. |

## Forbidden Claims And Actions

- Do not claim the master program achieved public benchmark promotion.
- Do not cite optional benchmark-gate execution as pilot promotion evidence.
- Do not commit or revert unrelated dirty work.
- Do not hide failed checks.
- Do not mark the overall execution complete if a required phase artifact is
  missing.

## Exact Next-Phase Handoff Conditions

There is no next implementation phase in this master program. Completion
requires:

- all phase result artifacts present;
- final checks recorded;
- stop/final handoff written;
- unresolved adapter and formalization gaps listed as future work.

## Stop Conditions

- Stop if final focused checks fail and cannot be repaired locally.
- Stop if an optional existing-suite benchmark-gate regression check fails
  because of touched files; do not treat that check as pilot promotion
  evidence.
- Stop if final interpretation would cross a public/release/scientific claim
  boundary.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Write the final visible handoff.
4. Review the handoff for consistency, correctness, artifact coverage, and
   boundary safety.
