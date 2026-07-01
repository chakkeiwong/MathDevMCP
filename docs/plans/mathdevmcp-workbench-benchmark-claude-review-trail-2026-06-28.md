# Workbench Benchmark Claude Review Trail

Date: `2026-06-28`

## Role Contract

Claude is a read-only reviewer only. Claude cannot authorize human, runtime,
model-file, funding, product, release, or scientific-claim boundary crossings.

## Round 1

Prompt:

- Compact master-program review for the workbench benchmark program.

Verdict:

- `VERDICT: REVISE`

Key findings:

- Gate integration needed hard Phase 3 thresholds.
- Oracle classes were not explicit enough.
- Backend unavailable needed a dedicated non-claim class.
- Seeded track needed mandatory negative-control/hidden-assumption fixtures.
- Run manifest/scoring rubric were underspecified.
- External-source reporting needed stricter separation and no aggregate
  cross-source scores.
- Phase 5 needed a seeded-only continuation path if external samples are absent.

Repair:

- Added oracle classes to the master program.
- Added seeded-gate promotion thresholds.
- Added run manifest and scoring-rubric requirements.
- Added external reporting rules forbidding combined external totals/rankings.
- Patched Phase 1-7 subplans and visible runbook to enforce these requirements.

## Round 2

Prompt:

- Repair-delta review focused on whether Round 1 blockers were resolved.

Outcome:

- First repaired prompt hung without output and was interrupted.
- Tiny probe prompt returned `OK`.
- Smaller verdict-only repaired prompt also hung without output and was
  interrupted.

Status:

- `CLAUDE_REVIEW_UNAVAILABLE_AFTER_SUCCESSFUL_PROBE`

Codex assessment:

- The material Round 1 findings were patched visibly.
- Local plan checks passed after repair.
- Continue to Phase 0 because Claude silence is not an execution authority and
  no remaining human-required boundary was identified.

## Phase 3 Subplan Review

### Round 1

Verdict: `REVISE`

Findings:

- Exact thresholds, formulas, denominators, and aggregation rules were missing.
- Baseline/comparator for false-confidence resistance was incomplete.
- Mutation panel needed explicit fairness/non-completeness language.
- Backend availability and scorer/rubric versions needed to be recorded in the
  threshold report.
- Handoff had to block on any failed threshold, not only known mutation-family
  failures.

Resolution:

- Patched Phase 3 subplan with exact thresholds and denominators.
- Added mutation diagnostic-only boundary.
- Added manifest/backend/scoring-version requirement.
- Added broad failed-threshold blocker/repair condition.

### Round 2

- Re-review prompt hung.
- Tiny probe returned `OK`.
- Smaller re-review prompt also hung.
- Recorded as `CLAUDE_REVIEW_UNAVAILABLE_AFTER_SUCCESSFUL_PROBE`.
- Proceeded after local skeptical audit because the Round 1 material findings
  were visibly patched and Phase 3 checks passed.
