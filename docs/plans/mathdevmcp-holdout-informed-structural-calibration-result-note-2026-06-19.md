# MathDevMCP Holdout-Informed Structural Calibration Result Note

## Date

2026-06-19

## Scope

This note records a stronger **holdout-informed structural calibration pass**
over the current scored tiers:

- the committed public scored-report surface, and
- the current local-only holdout scored-report surface.

It remains a structural calibration artifact, not a semantic benchmark result
or a generalization proof.

## Evidence contract

### Question

What does the current direct comparison between the **public scored tier** and
the **local holdout scored tier** suggest about current benchmark maturity, and
what remains too thin for stronger interpretation?

### Exact baseline / comparator

Comparator A:
- `score_real_task_public_candidates(...)` over the committed public candidate
  fixture set

Comparator B:
- `score_local_holdout_candidate_fixtures(...)` over the current local-only
  holdout manifest and local candidate-answer fixture set

This is a comparison of **structural scored tiers**, not of free-form semantic
model outputs.

### Primary criterion

The primary criterion is whether the benchmark now has enough scored structure in
both the public and local tiers to support a more direct calibration
interpretation than earlier notes.

### Veto diagnostics

This note would be unsound if any of the following were true:

- the public scored layer were interpreted as public benchmark performance in a
  broad semantic sense;
- the local holdout scored layer were interpreted as generalization evidence;
- false-confidence-veto failures were smoothed over by aggregate counts;
- the current comparison were promoted into workflow, gate, or release claims.

### Explanatory-only diagnostics

The following are descriptive only:

- scored-case totals,
- by-status totals,
- by-family scored coverage,
- missing scored-case IDs,
- current false-confidence-veto failure counts.

### What will not be concluded

This note does **not** conclude that:

- the benchmark now has holdout-backed generalization evidence;
- the public scored tier is complete;
- the local holdout tier is representative;
- public-vs-holdout score differences are stable enough for policy decisions;
- the benchmark is complete.

## Current scored-tier comparison

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

Interpretation:

- the public scored tier is now close to full-corpus scored coverage;
- it is no longer severely limited by fixture sparsity;
- the remaining public scored gap is now small enough that the public-vs-local
  comparison can be interpreted more directly than before.

### Local holdout scored tier

Current local holdout scored summary:

- holdout case total: `5`
- scored candidate total: `5`
- missing scored case IDs: none
- by status:
  - `consistent`: `5`
- by family currently exercised in scored execution:
  - `evidence_boundary_discipline`: `3`
  - `retrieval_and_provenance`: `1`
  - `numerical_oracle_parity`: `1`
- false-confidence-veto failures: `0`

Interpretation:

- the local holdout tier is fully scored relative to its current seed;
- it now spans a broader set of task families than before;
- it is still much smaller than the public tier, but the local holdout side is
  now less obviously narrow in kind as well as in count.

## Calibration interpretation

### What this stronger comparison now justifies

At this stage, the stronger comparison justifies the following bounded claim:

- both the public and local tiers now have executable scored surfaces rich enough
  to support a more direct structural calibration discussion.

More specifically:

- the public tier is broader and now much more fully scored than before;
- the local holdout tier is smaller but fully scored relative to its current
  seed;
- therefore the benchmark can now reason about **coverage maturity imbalance**
  under conditions where public scored sparsity is much less distorting than it
  was in earlier calibration passes.

### What it still does **not** justify

At this stage, the stronger comparison still does **not** justify:

- strong public-vs-holdout performance claims;
- generalization claims from the current local holdout seed;
- gate/readiness interpretation;
- semantic benchmark maturity.

## Main remaining calibration uncertainties

1. **Coverage maturity imbalance remains, but is narrowing further**
   - the public tier is now much more fully scored than in earlier passes;
   - the local tier is still fully scored relative to its current seed;
   - the remaining asymmetry is now less about basic local family absence and
     more about how representative the current five-family local seed is.

2. **Asymmetric family distribution still remains, but is improving**
   - the public scored tier and the local holdout scored tier do not yet cover
     the same family mix or breadth.

3. **Structural scoring limits remain active**
   - both tiers are still interpreted through structural, normalized candidate
     scoring rather than richer semantic evaluation.

4. **The meaning of the lone public mismatch and lone public veto failure**
   - those are useful signals, but still too sparse to support broad score
     interpretation on their own.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as ready for richer cross-tier structural calibration, but not for strong comparative claims | Met | The public tier still has a veto failure; the local tier currently does not | The remaining question is increasingly whether the current five-family local seed is representative enough for stronger cross-tier interpretation | Revisit whether one more round of local broadening or a deeper public-vs-local calibration pass is now the higher-leverage move | No generalization proof, no benchmark completion claim, no gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The current comparison may still flatter the local holdout tier because it is
fully covered relative to a small hand-curated seed, while the public tier is
broader and therefore naturally harder to cover completely with committed
candidate fixtures.

### What would overturn confidence

Confidence in the current interpretation would weaken if:

- expanding public candidate coverage changed the public structural picture
  materially;
- expanding local holdout breadth produced many new veto or mismatch findings;
- later semantic layers showed that the current structural score comparison was
  too brittle to support even internal calibration.

### Weakest part of the evidence

The weakest part of the current evidence is not execution stability. It is the
continued asymmetry between:

- public breadth with partial scored coverage, and
- local narrowness with full scored coverage.

## Next justified action

The next justified action is to improve the most important remaining source of
coverage and interpretation uncertainty.

At this moment, the benchmark is no longer obviously bottlenecked by either:

- extreme public scored sparsity, or
- trivial local holdout thinness.

The sharper remaining question is whether the current five-family local seed is
representative enough to support a deeper public-vs-local calibration pass, or
whether one more round of local broadening is still the higher-value move.

So the next best move is likely one of:

1. run a deeper cross-tier structural calibration pass now, or
2. broaden the local holdout tier one more step before that pass.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark now has enough scored structure on both tiers to make the
coverage maturity imbalance itself the central calibration question.
