# MathDevMCP Benchmark-Driven Improvement Program

## Date

2026-06-19

## Purpose

This document turns the benchmark-driven improvement plan into a concrete phased
execution program.

The program is intended to answer a narrow question:

> Given the current benchmark state, what exact changes should we make next to
> improve MathDevMCP in ways that are justified by benchmark evidence rather
> than by speculation?

This is not a release plan and not a benchmark-gate plan.

## Governing artifacts

This program is grounded in:

- `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-driven-improvement-plan-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-iv-2026-06-19.md`

## Safety invariant

No phase in this program may silently promote the benchmark into:

- workflow-ready evidence,
- benchmark-gate evidence,
- release-policy evidence,
- holdout-backed generalization evidence,
- or a complete semantic evaluator.

All changes must continue to preserve hard false-confidence and
forbidden-claim boundaries.

## Skeptical audit

This program is justified only if each phase reduces a current benchmark
uncertainty rather than merely adding more mechanics.

- **Wrong baseline checked:** the current benchmark already has strong
  infrastructure; the next phases should be driven by representativeness and
  interpretability gaps.
- **Proxy-metric checked:** better scores are not enough; each phase must improve
  what the benchmark can responsibly mean.
- **Stop-condition checked:** every phase below includes a stop condition so work
  halts if it starts adding mechanics without reducing uncertainty.
- **Hidden assumptions checked:** no phase assumes policy/gate readiness,
  private/external availability, or broad semantic maturity.
- **Artifact-usefulness checked:** every phase must produce an artifact that
  changes the interpretation of the benchmark, not just its size.

## Phase 1 — Finish public scored coverage

### Goal

Reduce the remaining public scored coverage gap so the public tier is no longer
meaningfully limited by fixture sparsity.

### Exact files likely to change

Committed:
- `benchmarks/real_tasks/fixtures/public_candidate_answers.json`
- `tests/test_real_tasks_candidate_fixtures.py`
- `tests/test_real_tasks_scored_report.py`
- `docs/plans/mathdevmcp-public-candidate-fixture-coverage-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-result-note-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`

### Concrete task

- decide whether the remaining unscored public case should receive a committed
  normalized candidate fixture;
- if yes, add the fixture and refresh fixture-driven expectations;
- if no, add explicit documentation explaining why that case remains intentionally
  unscored.

### Acceptance checks

- public scored coverage improves or the remaining gap is explicitly justified;
- fixture/scored-report tests pass;
- no new public fixture weakens hard-veto behavior.

### Stop condition

If the last public case requires brittle or unnatural fixture logic, stop and
record it as an intentionally unscored edge rather than forcing a low-quality
fixture.

## Phase 2 — Improve holdout representativeness only if it adds a new judgment or failure shape

### Goal

Improve local holdout representativeness only when a new local family clearly
adds a missing judgment shape or failure shape.

### Exact files likely to change

Local-only:
- `.local/mathdevmcp/holdout_local_cases.json`
- `.local/mathdevmcp/holdout_local_candidate_answers.json`

Committed notes:
- `docs/plans/mathdevmcp-holdout-local-*.md` (new checkpoint notes as needed)
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-ii-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`

### Concrete task

- add at most one local family at a time;
- only add it if it introduces a new family/judgment/failure shape that the
  local tier does not currently express.

### Acceptance checks

- local family/judgment-shape table changes materially;
- local candidate coverage remains complete for the local seed;
- local/public boundaries remain explicit.

### Stop condition

If a candidate family does not add a new judgment or failure shape, do not add
it.

## Phase 3 — Re-run and reinterpret holdout-informed structural calibration

### Goal

Use the updated public and local scored tiers to reduce uncertainty about what
kind of comparison the benchmark now supports.

### Exact files likely to change

- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-result-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-ii-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`

### Concrete task

- regenerate current public and local scored summaries;
- update the interpretation of the most important remaining asymmetry;
- decide whether the dominant weakness is still holdout breadth or now semantic
  interpretability.

### Acceptance checks

- the updated note identifies one dominant remaining uncertainty clearly;
- public-vs-local comparison is less ambiguous than before;
- non-claim boundaries remain intact.

### Stop condition

If the comparison remains dominated by obvious coverage imbalance, do not make a
stronger interpretive claim; record the imbalance and return to Phase 2.

## Phase 4 — Define the structural-score ceiling explicitly

### Goal

Convert the repeated idea “structural scoring is useful but limited” into a
concrete boundary artifact for future semantic work.

### Exact files likely to change

- new note under `docs/plans/`, e.g.
  - `mathdevmcp-structural-score-ceiling-note-2026-06-19.md`
- possibly:
  - `docs/plans/mathdevmcp-benchmark-acceptance-policy-proposal-2026-06-19.md`
  - `docs/plans/mathdevmcp-benchmark-driven-improvement-plan-2026-06-19.md`

### Concrete task

Define explicitly:

- what current structural scoring can safely support,
- what requires richer semantic interpretation,
- what kinds of future semantic work are justified.

### Acceptance checks

- clear examples of structural-safe vs semantic-needed cases;
- benchmark notes stop overloading “structural” into “semantic.”

### Stop condition

If the ceiling cannot be stated concretely, do not broaden semantic work yet.

## Phase 5 — Bounded semantic / normalization expansion

### Goal

If justified by Phase 4, add only narrowly bounded semantic or answer-
normalization improvements.

### Exact files likely to change

- `src/mathdevmcp/real_tasks_answer_normalization.py`
- `tests/test_real_tasks_answer_normalization.py`
- calibration notes if behavior changes materially

### Concrete task

- add at most 1–2 clearly structured new normalization paths;
- preserve fail-closed behavior;
- preserve downstream veto behavior.

### Acceptance checks

- new normalization path composes with the existing scorer;
- unsupported cases still return `inconclusive`;
- no broad semantic evaluator claims are introduced.

### Stop condition

If the work starts requiring broad per-case heuristics or blurs into a general
semantic evaluator, stop and reassess.

## Phase 6 — Reassess benchmark acceptance tier

### Goal

Update the role-based acceptance assessment after the above phases, using the
proposed policy rather than intuition.

### Exact files likely to change

- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- possibly the policy proposal note if thresholds or caveat wording need
  clarification

### Concrete task

Re-evaluate whether the benchmark remains:

- `calibration_only` accepted,
- `internal_accepted_with_caveats`,
- `internal_accepted`,
- `policy_ready_candidate`.

### Acceptance checks

- tier shifts are explicitly justified by changed evidence;
- caveats remain visible;
- no tier is promoted without real supporting evidence.

### Stop condition

If representativeness remains the dominant unresolved uncertainty, do not
promote the benchmark above `accepted_with_caveats`.

## Decision table

| Phase | Why it matters | Acceptance signal | Stop condition |
|---|---|---|---|
| 1. Finish public scored coverage | Remove the last obvious public scored gap | Public tier is fully scored or the last gap is explicitly justified | Last remaining case would require brittle fixtures |
| 2. Improve holdout representativeness | Reduce the biggest remaining benchmark weakness | New local family adds a new judgment/failure shape | Added family is just “more of the same” |
| 3. Re-run holdout-informed calibration | Sharpen what the benchmark can currently mean | One dominant remaining asymmetry is clearly identified | Comparison still dominated by obvious imbalance |
| 4. Define structural-score ceiling | Clarify where semantics are actually needed | Structural-safe vs semantic-needed cases are explicit | Boundary stays vague |
| 5. Bounded semantic expansion | Improve only the next justified evaluator layer | New semantic/normalization path stays bounded and fail-closed | Work turns into a general evaluator prototype |
| 6. Reassess acceptance tier | Turn benchmark maturity into explicit role-based judgment | Tier status justified by evidence | Evidence still dominated by the same caveat |

## Non-claim boundary

This program does **not** mean the benchmark should keep growing indefinitely.

It means the next buildout steps should be earned by benchmark evidence and
uncertainty reduction, not by implementation convenience.
