# MathDevMCP Holdout-Informed Structural Calibration Result Note II

## Date

2026-06-19

## Scope

This note performs a deeper **comparative holdout-informed structural
calibration pass** over the current scored tiers:

- the committed public scored tier, and
- the current local-only holdout scored tier.

It is intended to go one step beyond existence and simple maturity checks by
asking what the current differences between the tiers now *mean*.

It is still a structural calibration artifact and still not a semantic
benchmark result or a generalization proof.

## Evidence contract

### Question

Given the current public scored tier and the current local holdout scored tier,
what is the most meaningful remaining interpretation gap, and what is the most
justified next benchmark move?

### Exact baseline / comparator

Comparator A:
- `score_real_task_public_candidates(...)` over the committed public candidate
  fixture set

Comparator B:
- `score_local_holdout_candidate_fixtures(...)` over the current local-only
  holdout cases and local candidate fixtures

This is a comparison of **structural scored tier maturity**, not free-form model
quality.

### Primary criterion

The primary criterion is whether the current cross-tier comparison is now strong
enough to shift the main question from “can we score both tiers?” to “what do
current differences between the tiers imply about next benchmark investment?”

### Veto diagnostics

This note would be unsound if any of the following were true:

- the local holdout tier were interpreted as holdout-backed generalization
  evidence;
- the public tier’s lone veto failure were ignored because totals look strong;
- the comparison were promoted into workflow, gate, or release claims;
- the current cross-tier differences were treated as semantic evaluation quality
  rather than structural scored-tier differences.

### Explanatory-only diagnostics

The following are descriptive only:

- public and local scored totals,
- by-family scored coverage,
- veto counts,
- missing scored-case IDs,
- relative completeness of each tier.

### What will not be concluded

This note does **not** conclude that:

- the benchmark now has holdout-backed generalization evidence;
- the current local holdout tier is representative;
- public-vs-local score differences are stable enough for policy decisions;
- the benchmark is complete.

## Current cross-tier scored state

### Public scored tier

Current public scored summary:

- public case total: `12`
- scored candidate total: `12`
- missing scored case IDs: none
- by status:
  - `consistent`: `11`
  - `mismatch`: `1`
- by family currently exercised in scored execution:
  - `evidence_boundary_discipline`: `5`
  - `code_document_consistency`: `3`
  - `derivation_boundary_and_abstention`: `1`
  - `numerical_oracle_parity`: `2`
  - `retrieval_and_provenance`: `1`
- false-confidence-veto failures: `1`

Interpretation:

- the public scored tier is now fully covered by committed candidate fixtures;
- it already exposes at least one structural mismatch/veto failure;
- its main remaining weaknesses are no longer about fixture sparsity.

### Local holdout scored tier

Current local holdout scored summary:

- holdout case total: `7`
- scored candidate total: `7`
- missing scored case IDs: none
- by status:
  - `consistent`: `6`
  - `mismatch`: `1`
- by family currently exercised in scored execution:
  - `evidence_boundary_discipline`: `4`
  - `retrieval_and_provenance`: `1`
  - `numerical_oracle_parity`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto failures: `1`

Interpretation:

- the local holdout tier is fully scored relative to its current seed;
- it now spans multiple families and multiple judgment shapes;
- it is still much smaller than the public tier, but it no longer looks like a
  purely safe-only comparison partner.

## Comparative interpretation

### What the current difference most likely means

The strongest current difference is no longer just “public is broader, holdout is
smaller.” It is now:

- the **public scored tier** is broader and already contains at least one active
  mismatch/veto signal;
- the **local holdout scored tier** is smaller, but it now also contains at
  least one mismatch/veto-shaped signal.

This means the local holdout tier is becoming more useful as a **failure-shape
comparison partner**, even though it is still too small to support strong
comparative conclusions.

### Why that matters

The earlier local/public contrast risk was:

1. the local holdout tier is still too easy / too narrow;
2. the local holdout tier is simply too small for its failure surface to be
   visible yet.

The current local mismatch/veto signal weakens the first explanation somewhat:

- the local tier is no longer purely all-consistent;
- but it is still too small for strong comparative claims.

So the next useful move is not workflow/gate integration. It is to decide
whether one more round of local broadening would materially improve failure-shape
representativeness, or whether a deeper comparative interpretation pass is now
worth more.

## Main remaining calibration uncertainties

1. **Failure-shape asymmetry is reduced, but not resolved**
   - the public scored tier includes mismatch/veto behavior;
   - the local holdout tier now also includes mismatch/veto behavior;
   - but the local tier still exposes much less failure variety overall.

2. **Representativeness of the local seed**
   - the local seed is broader than before, but still small enough that full
     coverage does not imply strong representativeness.

3. **Cross-tier family mismatch**
   - the two tiers overlap in some families, but are not yet close to matched in
     breadth or shape.

4. **Structural scoring limits remain active**
   - all interpretation is still through deterministic normalized candidate
     scoring rather than richer semantic evaluation.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as ready for a more meaningful holdout-informed comparison, but still not for strong comparative claims | Met | Both tiers now expose at least one mismatch/veto-shaped signal | Whether the local holdout tier still lacks enough breadth to make that signal representative | Decide whether one more round of local broadening or a deeper comparative interpretation pass is now higher-value | No generalization proof, no benchmark completion claim, no gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The current comparison may overstate local holdout cleanliness simply because the
local tier still lacks enough failure-shape diversity, not because it is truly a
harder or cleaner benchmark slice.

### What would overturn confidence

Confidence in the current interpretation would weaken if:

- modest local broadening quickly introduced mismatch/veto failures;
- later local cases showed strong template leakage from the public tier;
- richer semantic layers changed the current structural public-vs-local picture
  materially.

### Weakest part of the evidence

The weakest part of the current evidence is not the existence of both scored
tiers. It is the local tier’s still-limited ability to expose failure variety.

## Next justified action

The next justified action is to improve the **representativeness and
comparability** of the cross-tier signal.

At this stage, both tiers now show at least some failure-shape variety, so the
next choice is no longer forced by an obvious missing signal. The remaining
question is whether another round of local broadening or a deeper comparative
interpretation pass would yield more information.

So the next best move is likely one of:

1. add one more carefully chosen local holdout family if we want stronger local
   breadth before comparison, or
2. run the next deeper comparative calibration pass now, using the fact that the
   local tier is no longer all-consistent.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark has now reached the point where the most informative next
question is not “can we score holdout?” but “does the holdout tier expose enough
failure diversity to make the comparison truly informative?”
