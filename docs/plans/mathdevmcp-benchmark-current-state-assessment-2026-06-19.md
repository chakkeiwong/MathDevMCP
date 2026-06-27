# MathDevMCP Benchmark Current-State Assessment

Role: current-synthesis
Current-state status: living
Grounded in:
- docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md
- docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md
- docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md
## Date

2026-06-19

## Scope

This note assesses the **current benchmark state** using the existing public and
local holdout benchmark surfaces.

It is grounded in:

- `src/mathdevmcp/real_tasks_report.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `src/mathdevmcp/real_tasks_holdout_local_scoring.py`
- `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`

This is a **benchmark assessment** note, not a gate or release artifact.

## Evidence contract

### Question

What does the benchmark currently say about MathDevMCP’s evaluation state, and
what are the most important remaining weaknesses that should drive the next
improvement plan?

### Exact baseline / comparator

This note synthesizes the current benchmark state from:

- the public benchmark report,
- the public scored candidate-fixture report,
- the local-only holdout scored report.

### Primary criterion

The primary criterion is whether the current benchmark state can be interpreted
as:

- structurally healthy and usable for calibration,
- but still limited by specific coverage or interpretation gaps that justify
  further benchmark-driven product work.

### Veto diagnostics

This assessment would be unsound if any of the following were true:

- public or local scored outputs were promoted into generalization claims;
- local holdout evidence were treated as public benchmark evidence;
- current veto failures were ignored or washed out by aggregate summaries;
- the benchmark were described as complete or policy-ready.

### Explanatory-only diagnostics

The following are descriptive only:

- case totals,
- family counts,
- scored-case counts,
- missing scored-case IDs,
- false-confidence-veto counts.

### What will not be concluded

This note does **not** conclude that:

- the benchmark is complete;
- the benchmark has holdout-backed generalization evidence;
- the benchmark is ready for workflow/gate/release use;
- the benchmark is semantically mature enough for broad free-form evaluation.

## Current public benchmark state

Current public benchmark summary:

- public case total: `12`
- by expected status:
  - `consistent`: `6`
  - `unverified`: `2`
  - `mismatch`: `3`
  - `inconclusive`: `1`
- by family:
  - `evidence_boundary_discipline`: `5`
  - `numerical_oracle_parity`: `2`
  - `code_document_consistency`: `3`
  - `retrieval_and_provenance`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto cases: `12`

Interpretation:

- the public corpus is now broad enough to serve as a real public calibration
  surface;
- all major expected-status types are represented;
- the public side is no longer the weakest structural part of the program.

## Current public scored state

Current public scored summary:

- public case total: `12`
- scored candidate total: `12`
- missing scored case IDs: none
- by scored status:
  - `consistent`: `11`
  - `mismatch`: `1`
- false-confidence-veto failures: `1`

Interpretation:

- the public scored layer is now fully covered by committed candidate fixtures;
- the public tier is no longer limited by scored-fixture sparsity.

## Current local holdout state

Current local holdout scored summary:

- holdout case total: `7`
- scored candidate total: `7`
- missing candidate case IDs: none
- by scored status:
  - `consistent`: `6`
  - `mismatch`: `1`
- by family:
  - `evidence_boundary_discipline`: `4`
  - `retrieval_and_provenance`: `1`
  - `numerical_oracle_parity`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto failures: `1`

Interpretation:

- the local holdout tier is fully candidate-covered for its current local seed;
- it now spans multiple families and multiple judgment shapes;
- but it is still a small local seed and therefore still the most important
  remaining representativeness uncertainty.

## Assessment summary

### What looks healthy

1. **Benchmark scaffolding is strong**
   - public and local tiers are both real and executable.

2. **Public calibration state is strong**
   - public scored coverage is high and status diversity is meaningful.

3. **Holdout tier is no longer only symbolic**
   - it is populated, scoreable, and fully fixture-covered relative to its
     current seed.

4. **False-confidence logic is visible in both tiers**
   - both the public and local scored surfaces now show at least one
     mismatch/veto-shaped signal.

### Main remaining weaknesses

1. **Holdout representativeness remains the dominant weakness**
   - the local tier is still small enough that its failure and abstention signals may not be
     representative.

2. **Cross-tier family breadth remains asymmetric**
   - the public tier is broader and still the better approximation of the task
     space.

3. **Structural scoring remains the main evaluation layer**
   - semantic maturity is still limited.

4. **Public-vs-local interpretation is now limited more by representativeness than by public scored coverage**
   - the public scored layer is fully covered;
   - the benchmark’s main comparative uncertainty has shifted toward the breadth and representativeness of the local holdout tier.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the current benchmark as structurally healthy and calibration-usable, but still representativeness-limited | Met | Public and local tiers both preserve veto-aware scoring behavior | Whether the local holdout tier is representative enough to support stronger calibration claims | Build a benchmark-driven MathDevMCP improvement plan that targets representativeness, scoring maturity, and semantic-layer boundaries | No benchmark completion claim, no holdout-backed generalization, no workflow/gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The benchmark may now look mature mainly because the public and local
infrastructure is solid, while the harder problem — whether the local holdout
seed is representative — is harder to see in summary tables.

### What would overturn confidence

Confidence in this assessment would weaken if:

- modest local holdout expansion materially changed the local scored profile;
- richer semantic evaluation changed the public/local comparison substantially;
- broader comparative calibration showed the current local differences were still
  mostly seed artifacts.

### Weakest part of the evidence

The weakest part of the current benchmark evidence is not execution stability. It
is the unresolved representativeness of the local holdout tier.

## Next justified action

The next justified action is to build the next MathDevMCP improvement plan from
this assessment.

That improvement plan should focus on:

- representativeness gaps,
- scoring maturity gaps,
- semantic-layer boundary gaps,
- and what additional benchmark work is still worth doing versus what has become
  diminishing-return infrastructure.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark is now strong enough to drive a benchmark-informed
improvement plan for MathDevMCP.
