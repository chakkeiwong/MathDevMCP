# MathDevMCP Benchmark Calibration Milestone Note

Role: current-synthesis
Current-state status: living
Grounded in:
- docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md
- docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md
## Date

2026-06-19

## Scope

This note consolidates the current benchmark calibration state across:

- the public benchmark corpus,
- the public scored fixture layer,
- the local-only holdout scored tier,
- the normalization prototype,
- and the current strategic checkpoints.

It is a **calibration milestone** note, not a benchmark completion note and not
an operational readiness note.

## Evidence contract

### Question

What does the current benchmark now honestly support as an evaluation system,
and what is still the most limiting remaining uncertainty?

### Exact baseline / comparator

This note synthesizes the current artifact state rather than comparing against a
single earlier run:

- current public report summary,
- current public scored summary,
- current local holdout scored summary,
- current calibration and strategic checkpoint notes.

### Primary criterion

The primary criterion is whether the benchmark has moved beyond infrastructure
assembly into a state where the main remaining uncertainty is genuinely about
coverage and interpretive maturity, not about missing basic mechanics.

### Veto diagnostics

This note would be unsound if any of the following were true:

- current structural scores or summaries were promoted into generalization or
  release claims;
- holdout-local local-only evidence were treated as public benchmark evidence;
- the benchmark were described as complete or policy-ready;
- current veto failures were washed out by aggregate summaries.

### Explanatory-only diagnostics

The following are descriptive only:

- case totals,
- family counts,
- scored-case totals,
- false-confidence-veto counts,
- missing scored-case IDs.

### What will not be concluded

This note does **not** conclude that:

- the benchmark is complete;
- the benchmark has holdout-backed generalization evidence;
- workflow, gate, or release-policy coupling is justified;
- semantic evaluation maturity has been reached.

## Current benchmark milestone state

### Public corpus state

Current public benchmark state:

- public case total: `12`
- expected statuses represented:
  - `consistent`: `6`
  - `unverified`: `2`
  - `mismatch`: `3`
  - `inconclusive`: `1`
- false-confidence-veto cases: `12`

Interpretation:

- the public benchmark corpus is now a real, diverse, machine-checkable public
  calibration surface.

### Public scored state

Current public scored state:

- scored candidate total: `12`
- remaining unscored public case IDs: none
- false-confidence-veto failures: `1`

Interpretation:

- the public scored layer is now fully covered by committed candidate fixtures;
- the public side is no longer primarily limited by scored-fixture sparsity.

### Local holdout scored state

Current local holdout scored state:

- holdout case total: `7`
- scored candidate total: `7`
- missing candidate case IDs: none
- false-confidence-veto failures: `1`

Family coverage currently exercised locally:

- `evidence_boundary_discipline`: `4`
- `retrieval_and_provenance`: `1`
- `numerical_oracle_parity`: `1`
- `derivation_boundary_and_abstention`: `1`

Interpretation:

- the local holdout tier is now fully scored relative to its current seed;
- it is broader than before in both family coverage and judgment-shape
  coverage;
- it remains local-only and still too small for strong representativeness
  claims.

### Normalization prototype state

Current normalization prototype coverage:

- `MF-03-hmc-helper-nonclaim-boundary`
- `MF-04-short-hmc-acceptance-veto-diagnosis`
- `DH-06-densesoap-source-contract-mismatch`

Interpretation:

- the normalization layer is useful and safe as a bounded prototype;
- it is not yet a general semantic benchmark evaluator.

## What the benchmark now supports

At this point, the benchmark now supports these stronger but still bounded
claims:

1. MathDevMCP has a real public benchmark surface with meaningful status
   diversity.
2. The public scored layer is broad enough that its remaining gap is no longer
   the dominant maturity problem.
3. The local holdout tier is no longer only a scaffold; it is a real local-only
   scored tier with multiple families and multiple judgment shapes.
4. The benchmark’s main remaining uncertainty is now about **representativeness
   and cross-tier interpretation**, not about missing basic benchmark mechanics.

## What still limits the benchmark

### 1. Holdout representativeness
The local holdout tier is broader than before, but still small enough that its
failure and abstention signals may not be representative.

### 2. Cross-tier asymmetry
The public tier and local holdout tier are now both scoreable and both show at
least some mismatch/veto behavior, but they still do not have equal breadth or
family shape.

### 3. Structural-score ceiling
Both tiers are still interpreted mainly through deterministic structural scoring,
not rich semantic evaluation.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as having reached a real calibration milestone, but not completion | Met | Public and local tiers both show active veto-aware scored behavior without policy drift | Whether the current local holdout tier is representative enough for stronger calibration claims | Prefer representativeness-focused next work over more infrastructure layers; choose next move based on evaluation value, not mere buildability | No generalization proof, no benchmark completion claim, no workflow/gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The benchmark may now look mature mainly because most infrastructural gaps are
closed, while the harder remaining problems — representativeness and semantic
interpretation — are slower to expose.

### What would overturn confidence

Confidence in this milestone interpretation would weaken if:

- modest new holdout additions changed the local failure/abstention picture
  substantially;
- broader semantic layers changed the current public/local structural picture
  materially;
- a stronger cross-tier calibration pass showed current local differences were
  still mostly seed artifacts.

### Weakest part of the evidence

The weakest part of the current evidence is not public or local execution
stability. It is uncertainty about how broadly the current local holdout tier
reflects the true task distribution we care about.

## Next justified action

The next justified action is **not** another small infrastructure layer by
default.

The next justified action should be chosen by what most improves the benchmark’s
representativeness and interpretability, such as:

- one more carefully chosen local holdout family, if it clearly adds a new
  judgment or failure shape; or
- a deeper interpretive calibration pass that tests how much current
  public-vs-local conclusions depend on the present local seed.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark has reached the point where the central remaining problem
is no longer “can we build the benchmark?” but “how representative and how
interpretable is the benchmark we have built?”
