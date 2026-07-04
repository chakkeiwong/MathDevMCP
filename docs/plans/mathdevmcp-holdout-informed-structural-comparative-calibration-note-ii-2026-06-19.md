# MathDevMCP Holdout-Informed Structural Comparative Calibration Note III

## Date

2026-06-19

## Scope

This note deepens the comparative structural calibration again after the local
holdout tier began exposing its own mismatch/veto-shaped signal.

It is grounded in the current scored summaries of:

- the committed public scored tier, and
- the local-only holdout scored tier.

It remains a structural calibration note, not a semantic evaluation result and
not a generalization proof.

## Evidence contract

### Question

Now that both the public and local holdout scored tiers contain at least one
mismatch/veto-shaped signal, what do the remaining public-vs-local differences
actually imply about benchmark maturity and the next best calibration step?

### Exact baseline / comparator

Comparator A:
- current committed public scored tier

Comparator B:
- current local-only holdout scored tier

This comparison is over structural scored surfaces only.

### Primary criterion

The primary criterion is whether the benchmark can now move beyond
“holdout exists and is scoreable” into a more substantive comparative
interpretation of:

- relative breadth,
- relative failure-shape exposure,
- and relative maturity limits.

### Veto diagnostics

This note would be unsound if any of the following were true:

- local mismatch/veto signals were promoted into generalization evidence;
- the current scored comparison were treated as workflow, gate, or release
  evidence;
- the public and local tiers were treated as equally representative merely
  because both now show some failure behavior.

### Explanatory-only diagnostics

The following are descriptive only:

- total scored cases,
- by-status counts,
- by-family scored coverage,
- false-confidence-veto counts,
- remaining scored-case coverage gaps.

### What will not be concluded

This note does **not** conclude that:

- the benchmark has holdout-backed generalization evidence;
- the local holdout seed is representative enough for stable conclusions;
- the benchmark is complete;
- the benchmark is ready for workflow/gate/release integration.

## Current comparative state

### Public scored tier

Current public scored summary:

- public case total: `12`
- scored candidate total: `11`
- missing scored case IDs:
  - `DH-04-bayesfilter-engineering-qualification-boundary`
- by status:
  - `consistent`: `10`
  - `mismatch`: `1`
- by family currently exercised in scored execution:
  - `evidence_boundary_discipline`: `4`
  - `code_document_consistency`: `3`
  - `derivation_boundary_and_abstention`: `1`
  - `numerical_oracle_parity`: `2`
  - `retrieval_and_provenance`: `1`
- false-confidence-veto failures: `1`

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

## Comparative interpretation

### What is now similar between the tiers

Both the public and local holdout scored tiers now show:

- at least one mismatch/veto-shaped signal,
- explicit false-confidence-veto behavior,
- non-gating structural score outputs.

This reduces the earlier asymmetry where the local holdout tier appeared cleaner
only because it had not yet surfaced any local failure shape.

### What remains materially different

The public tier still differs from the local holdout tier in two important ways:

1. **Breadth**
   - the public tier covers more total cases and more benchmark families overall.

2. **Failure-shape diversity**
   - both tiers now show mismatch/veto behavior, but the public tier still
     exposes a broader set of scored public case types than the local holdout
     tier.

So the benchmark is no longer facing a simple “one tier has failures, the other
has none” asymmetry. It is now facing a more mature question:

> is the local holdout tier broad enough to make its failure signals meaningfully
> comparable to the public tier’s failure signals?

### What this suggests about benchmark maturity

This is a stronger calibration state than before because:

- the public scored tier is close to full coverage,
- the local holdout tier is fully covered relative to its current seed,
- both tiers now exhibit at least some mismatch/veto behavior,
- and the local tier now spans one more judgment shape (`unverified`) than the
  previous local comparison state.

But it is still not a strong comparative state because:

- the local tier remains much smaller,
- the family distributions remain asymmetrical,
- the local failure variety is still limited.

## Main remaining uncertainties

1. **Representativeness of local failures**
   - the local tier now has mismatch/veto behavior, but it is not yet clear
     whether that behavior is representative or just a narrow probe case.

2. **Cross-tier family asymmetry**
   - both tiers overlap in some families, but not yet in enough breadth to make
     their scored behavior strongly comparable.

3. **Structural-score ceiling**
   - both tiers are still being interpreted through deterministic structural
     scoring rather than richer semantic evaluation.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as ready for a more meaningful public-vs-local structural comparison, but still not for strong comparative claims | Met | Both tiers now show at least one mismatch/veto-shaped signal | Whether the local mismatch/veto behavior is representative enough rather than merely present | Choose between one more holdout broadening step or a deeper comparative calibration pass that explicitly studies the meaning of the current local failure-shape coverage | No generalization proof, no benchmark completion claim, no workflow/gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The local holdout tier may now look more comparable simply because it contains a
single carefully chosen violation-oriented case, not because it has achieved
broad enough failure diversity for strong comparative use.

### What would overturn confidence

Confidence in the current interpretation would weaken if:

- one or two more local holdout additions materially changed the local mismatch
  pattern;
- the current local mismatch proved too template-shaped to be a good local
  generalization probe;
- richer semantic layers altered the apparent public-vs-local comparison.

### Weakest part of the evidence

The weakest part of the current evidence is no longer the existence of local
failure signals. It is uncertainty about how *representative* those local
failure signals are.

## Next justified action

The next justified action is now genuinely strategic:

- either broaden the local holdout tier one more step to improve failure-shape
  representativeness,
- or run the next deeper comparative interpretation pass now and explicitly
  study how much the current comparison still depends on the local seed’s small
  size.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark has now reached the point where the most important
remaining question is no longer whether the local tier can reveal failures, but
how trustworthy those local failure signals are as calibration evidence.
