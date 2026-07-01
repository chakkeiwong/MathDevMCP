# Reset Memo: MathDevMCP Benchmark Program

## Scope and lane

This reset memo is for the **MathDevMCP real-task benchmark program**.

Governing benchmark structure/policy artifacts:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-note-taxonomy-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-policy-proposal-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-driven-improvement-program-2026-06-19.md`

Current canonical synthesis layer (read these first in a new session):

- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-read-me-first-2026-06-19.md`

Historical evidence / strategic checkpoint layer (do not treat as the canonical
current truth unless specifically referenced by the synthesis layer):

- `docs/plans/mathdevmcp-bounded-overnight-benchmark-run-result-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-result-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-ii-2026-06-19.md`
- the holdout-local broadening / population / failure-shape notes
- the strategic review checkpoint series

## Why this reset memo exists

The benchmark note stack has become large enough that a clean restart should not
require rediscovering:

- which documents govern the benchmark,
- which notes are current-state canonical,
- what the current objective benchmark state is,
- what acceptance tier the benchmark currently satisfies,
- what remains unfinished,
- and what the safest next step is.

This memo is intended to be shareable with Claude Code or Codex.

## Current benchmark state (authoritative summary)

### Public tier

Current public benchmark summary:

- public case total: `12`
- public expected-status coverage:
  - `consistent`: `6`
  - `unverified`: `2`
  - `mismatch`: `3`
  - `inconclusive`: `1`
- public false-confidence-veto cases: `12`

Current public scored summary:

- public scored candidate total: `12`
- remaining unscored public case IDs: none
- public scored status mix:
  - `consistent`: `11`
  - `mismatch`: `1`
- public false-confidence-veto failures: `1`

Interpretation:

- the public benchmark is a real, structurally healthy calibration surface;
- the public scored layer is effectively complete for the current committed
  fixture set;
- public scored sparsity is no longer the dominant benchmark weakness.

### Local holdout tier

Current local holdout scored summary:

- local holdout case total: `7`
- local scored candidate total: `7`
- missing local candidate case IDs: none
- local scored status mix:
  - `consistent`: `6`
  - `mismatch`: `1`
- local false-confidence-veto failures: `1`

Current local family/judgment-shape coverage includes:

- `evidence_boundary_discipline`
- `retrieval_and_provenance`
- `numerical_oracle_parity`
- `derivation_boundary_and_abstention`

Local artifacts (ignored, non-public):

- `.local/mathdevmcp/holdout_local_cases.json`
- `.local/mathdevmcp/holdout_local_candidate_answers.json`

Interpretation:

- the local holdout tier is real, populated, fully fixture-covered relative to
  its current seed, and executable in a bounded local-only way;
- it now shows more than one judgment shape and at least one mismatch/veto-style
  signal;
- it is still small enough that **representativeness** remains the dominant
  unresolved uncertainty.

### Structural scoring / normalization

Committed public execution surfaces exist for:

- public manifest loader/validator
- public non-gating report
- public structural scorer
- public scored report
- public candidate-answer fixtures

Bounded normalization prototype currently supports:

- `MF-03-hmc-helper-nonclaim-boundary`
- `MF-04-short-hmc-acceptance-veto-diagnosis`
- `DH-06-densesoap-source-contract-mismatch`

Interpretation:

- the benchmark has a working structural scoring layer and a tiny bounded
  answer-normalization prototype;
- it does **not** yet have a general semantic evaluator.

## Acceptance status (authoritative summary)

Per `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`:

- `calibration_only` → `accepted`
- `internal_accepted_with_caveats` → `accepted_with_caveats`
- `internal_accepted` → `not_accepted`
- `policy_ready_candidate` → `not_accepted`

Interpretation:

- the benchmark is good enough for calibration and bounded internal use with
  caveats;
- it is not yet good enough for policy-bearing, gate, or release use.

## Main unresolved uncertainty

The benchmark is no longer primarily blocked by missing infrastructure.

The dominant unresolved uncertainty is now:

- **holdout representativeness / cross-tier interpretability**

In plain language:

- the benchmark can now compare public and local structural behavior,
- but it is still uncertain how representative the current local holdout seed is
  as a model of the broader task distribution.

## Current best interpretation

The benchmark is:

- not complete,
- not holdout-backed generalization evidence,
- not workflow/gate/release-ready,
- but strong enough to act as a bounded internal calibration and decision-support
  instrument.

## What changed in this workstream

The work accomplished in this benchmark cycle includes:

### Governance / planning
- benchmark spec
- benchmark master program
- category scoring subplan
- benchmark note taxonomy
- benchmark read-me-first guide
- acceptance policy proposal
- acceptance assessment
- benchmark-driven improvement plan/program
- multiple calibration and strategic checkpoint notes
- pause/review checkpoint

### Public benchmark system
- real-task public case manifest
- public manifest loader/validator
- public non-gating report
- deterministic structural scorer
- public scored report
- committed public candidate-answer fixtures
- bounded answer-normalization prototype

### Holdout-local system
- holdout-local scaffold/template
- holdout recipe and candidate inventory
- holdout example workflow note
- local discovery/initializer helpers
- local-only holdout scoring helper
- local candidate-fixture scaffold and runner support
- populated local holdout seed
- broadened local holdout families and judgment shapes

## What remains unfinished in the master benchmark program

Still materially unfinished:

- broader holdout-local representativeness
- private/external corpus design/execution
- workflow integration
- gate-candidate selection
- release-policy integration

In terms of the current benchmark-driven improvement program, the next highest
value work is likely to be guided by:

- representativeness gaps,
- structural-to-semantic boundary clarity,
- and benchmark-driven product improvement choices,

not by adding more benchmark scaffolding indiscriminately.

## Safe next-step guidance for a new session

### Read first
1. `docs/plans/mathdevmcp-benchmark-read-me-first-2026-06-19.md`
2. `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
3. `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`
4. `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
5. `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`
6. `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`
7. `docs/plans/mathdevmcp-benchmark-driven-improvement-program-2026-06-19.md`

### Best next move
The strongest next move is **not** another small benchmark helper by default.

The best next move should be chosen by whichever of these most improves
representativeness or interpretability:

- a carefully justified local holdout addition, or
- a benchmark-driven MathDevMCP product improvement item from the improvement
  program.

### Do not overclaim
Do not claim that the benchmark is:

- complete,
- holdout-backed generalization evidence,
- workflow/gate-ready,
- or policy-ready.

## Non-claim boundary

This reset memo does **not** mean the benchmark work is complete.

It means the benchmark is now mature enough that a new session should not need
 to rediscover its current structure, current state, and current limits before
continuing.
