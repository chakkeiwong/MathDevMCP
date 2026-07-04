# MathDevMCP Holdout-Informed Structural Calibration Note

## Date

2026-06-19

## Scope

This note records the first **holdout-informed structural calibration** view of
the benchmark program.

It is grounded in:

- the current public non-gating report surface,
- the current local-only holdout scoring surface,
- the current local-only holdout population and candidate-fixture state,
- and the benchmark master program / status dashboard.

It does **not** claim that holdout evaluation is complete or that the benchmark
now supports generalization claims.

## Evidence contract

### Question

What does the current combination of:

- public benchmark structure and reporting,
- and local-only holdout scoring,

already tell us about benchmark maturity, and what does it still not justify us
to claim?

### Exact baseline / comparator

Comparator A:
- current committed public corpus + public non-gating report

Comparator B:
- current local-only holdout corpus + local holdout candidate-fixture scoring

This is a structural calibration comparison, not a semantic model-output
comparison.

### Primary criterion

The primary criterion is whether the benchmark now has enough local holdout
execution structure to begin **holdout-informed calibration discussion** without
overstating what the current tiny local seed proves.

### Veto diagnostics

This note would be considered unsound if any of the following were true:

- the local holdout layer were described as public benchmark evidence;
- the local holdout layer were treated as benchmark-gate or release evidence;
- the public and holdout tiers were merged conceptually despite their different
  maturity levels;
- the current tiny local holdout seed were described as generalization proof.

### Explanatory-only diagnostics

The following are useful descriptive signals, but not promotion criteria by
 themselves:

- public case counts by category/status;
- holdout case counts and local candidate coverage;
- local holdout family mix;
- local mismatch/consistent counts from the current tiny local candidate set.

### What will not be concluded

This note does **not** conclude that:

- the benchmark now has holdout-backed generalization evidence;
- the public and local holdout tiers are balanced enough for strong comparative
  metrics;
- the current local holdout seed is representative;
- the benchmark is complete or policy-ready.

## Current public vs local holdout structural state

### Public benchmark state

Current public benchmark summary:

- public case total: `12`
- expected statuses represented:
  - `consistent`: `6`
  - `unverified`: `2`
  - `mismatch`: `3`
  - `inconclusive`: `1`
- family distribution:
  - `evidence_boundary_discipline`: `5`
  - `numerical_oracle_parity`: `2`
  - `code_document_consistency`: `3`
  - `retrieval_and_provenance`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto cases: `12`

Interpretation:

- the public tier is structurally diverse enough to support meaningful early
  calibration;
- but it remains a development/calibration surface, not a generalization
  surface.

### Local holdout benchmark state

Current local holdout summary:

- local holdout case total: `4`
- currently scored candidate total: `4`
- local candidate coverage gap remains for:
  - none in the current local seed
- scored local family coverage currently exercised in scoring:
  - `retrieval_and_provenance`
  - `evidence_boundary_discipline`
- false-confidence-veto failures in the current scored local set: `0`

Interpretation:

- the local holdout tier is now real and executable in a bounded sense;
- the current local seed is now fully covered by local candidate fixtures;
- the local seed is broader than before, but still small enough that this should
  be interpreted as improved local breadth rather than strong holdout maturity.

## Holdout-informed interpretation

### What this now justifies

At this stage, the benchmark now justifies the following narrower claim:

- the program has crossed from public-only calibration into the first stage of
  holdout-informed calibration, because a local holdout tier now exists,
  contains multiple local families, and can be scored with local-only fixtures.

That is a real maturity step.

### What it still does **not** justify

At this stage, the benchmark still does **not** justify:

- saying that public-tier improvements generalize;
- interpreting the current local seed as representative holdout evidence;
- comparing public vs holdout metrics as though they were stable;
- any gate, workflow, or release-policy coupling.

## Main calibration uncertainties

1. **Tiny local seed size**
   - the holdout-local tier is broader than before, but still contains only a
     small number of local cases;
   - even with full candidate coverage over the current local seed, it is not
     yet broad or balanced enough for strong generalization claims.

2. **Family imbalance between public and local tiers**
   - the public tier is richer and broader;
   - the local holdout tier is still concentrated in a very small number of
     families.

3. **Coverage gap within the local holdout tier**
   - `HOLDOUT-LATEX-NEIGHBORHOOD-001` currently lacks a local candidate fixture,
     which means the local execution tier is not yet evenly runnable.

4. **Structural scoring still dominates both tiers**
   - both public and local calibration are still mostly structural and bounded;
   - this is appropriate now, but means the benchmark is still not semantically
     mature.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as having reached the first holdout-informed calibration stage | Met | No tier-boundary veto was crossed | Tiny local seed and partial local candidate coverage | Broaden local holdout entries and local candidate coverage before interpreting holdout behavior strongly | No generalization proof, no stable holdout-vs-public metric comparison, no benchmark completion claim |

## Post-run red-team note

### Strongest alternative explanation

The current public/holdout comparison may look more mature than it is simply
because the holdout tier is now executable at all. That is progress, but it does
not mean the holdout tier is yet broad or stable enough to support strong
comparative conclusions.

### What result would overturn confidence

Confidence in the current interpretation would weaken if:

- local holdout expansion revealed that current local cases are unusually easy;
- local candidate fixtures had to be shaped too closely to public templates;
- future local scoring revealed many veto or mismatch failures that the tiny seed
  currently does not expose.

### Weakest part of the evidence

The weakest part of the current evidence is the **small and partially covered
local holdout seed**, not the existence of the local holdout machinery itself.

## Next justified action

The next justified action is to broaden the local holdout tier a little more —
particularly candidate coverage for the currently unscored local family — before
using the holdout tier for anything stronger than bounded internal calibration.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark has now reached the point where holdout-informed
calibration can begin to be discussed, while still remaining far below
holdout-backed generalization or policy maturity.
