# MathDevMCP Benchmark-Driven Improvement Plan

## Date

2026-06-19

## Scope

This plan is derived from:

- `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`

Its purpose is to turn the current benchmark findings into a bounded product
improvement program for MathDevMCP.

This is not a release plan and not a benchmark gate plan.

## Evidence contract

### Question

Given the current benchmark state, what are the most justified improvement
priorities for MathDevMCP itself?

### Exact baseline / comparator

Baseline:

- current public benchmark corpus and scored coverage,
- current local holdout scored tier,
- current structural scoring and bounded normalization layers,
- current benchmark acceptance assessment.

### Primary criterion

The primary criterion is whether each proposed improvement directly addresses a
benchmark-identified weakness rather than merely adding more machinery.

### Veto diagnostics

This plan would be unsound if:

- it proposed workflow/gate/release integration before representativeness and
  calibration maturity improve;
- it proposed broad semantic expansion without a bounded rationale;
- it prioritized new infrastructure that does not reduce a current benchmark
  weakness.

### What will not be concluded

This plan does **not** conclude that:

- the benchmark is complete;
- all remaining work should be benchmark work;
- every benchmark weakness requires immediate implementation.

## Current benchmark-driven priorities

### Priority 1 — Improve holdout representativeness

**Why this is first:**

The current assessment says the dominant remaining weakness is still the local
holdout tier’s representativeness.

**Bounded improvement directions:**

- add at most a few additional local holdout families only when they add a truly
  new judgment shape or failure shape;
- prefer cases that reduce obvious cross-tier asymmetry rather than merely
  increasing local count.

**What this would improve:**

- stronger holdout-informed calibration,
- better public-vs-local comparison,
- lower risk that local holdout remains template-shaped.

---

### Priority 2 — Improve public scored completeness only where it still matters

**Why this is second:**

The public scored tier is already close to full coverage, so this is no longer
its dominant weakness. But the one remaining unscored public case should either:

- be scored, or
- be explicitly justified as intentionally left unscored.

**Bounded improvement directions:**

- decide whether `DH-04-bayesfilter-engineering-qualification-boundary` needs a
  committed candidate fixture;
- if yes, add it in a narrowly bounded way.

**What this would improve:**

- close the last obvious public scored gap,
- simplify public-vs-local coverage comparisons.

---

### Priority 3 — Clarify the structural-to-semantic boundary

**Why this matters now:**

The benchmark now has enough structural machinery that the next key product
question is where structural scoring stops being enough and richer semantic
judgment should begin.

**Bounded improvement directions:**

- keep the current answer-normalization prototype narrow and explicit;
- document where structural matching is likely too brittle;
- only broaden semantic layers when a case clearly cannot be handled by current
  structural methods.

**What this would improve:**

- better control of scope creep,
- clearer evaluator roadmap,
- less risk of pretending the current normalizer/scorer is already semantic.

---

### Priority 4 — Improve calibration interpretation discipline

**Why this matters now:**

The benchmark now produces multiple calibration and strategic notes. The risk is
not too little interpretation, but interpretive drift.

**Bounded improvement directions:**

- keep using decision tables and non-claim sections;
- ensure milestone/checkpoint notes stay synchronized with actual public and
  local scored summaries;
- keep “accepted with caveats” distinct from “accepted” in internal messaging.

**What this would improve:**

- better program governance,
- less overclaiming risk,
- cleaner benchmark-to-product decision support.

## Lower-priority / deferred work

These are real future directions, but they are not the highest-value immediate
improvements based on the current benchmark state.

### Deferred 1 — Workflow integration

Why deferred:
- the benchmark is not yet policy-ready or workflow-ready.

### Deferred 2 — Gate candidate selection

Why deferred:
- benchmark acceptance above calibration is still caveat-heavy.

### Deferred 3 — Release-policy integration

Why deferred:
- explicitly unsupported by current benchmark maturity.

### Deferred 4 — Private/external execution

Why deferred from immediate product improvement:
- important, but still partially dependent on external/private availability and
  separate policy work.

## Decision table

| Improvement priority | Why it is justified now | Why it is not yet overreach |
|---|---|---|
| Holdout representativeness | Largest remaining benchmark weakness | Adds evaluation value, not policy claims |
| Public scored completeness | Removes the last obvious public scored gap | Narrowly bounded, not broad corpus growth |
| Structural-to-semantic boundary clarity | Current evaluation is still mostly structural | Clarifies scope rather than widening it |
| Calibration interpretation discipline | Many benchmark artifacts now exist | Keeps the benchmark useful without inflating authority |

## Recommended next bounded move

If choosing one immediate next product-improvement slice, the strongest option
is:

1. resolve the most valuable remaining representativeness or scored-coverage gap,
   then
2. revisit whether the next gain comes from another benchmark artifact or from a
   deeper semantic/evaluator boundary refinement.

## Non-claim boundary

This plan does **not** mean the benchmark work should continue indefinitely.

It means the benchmark is now good enough to guide a bounded, evidence-based
MathDevMCP improvement plan rather than speculative feature work.
