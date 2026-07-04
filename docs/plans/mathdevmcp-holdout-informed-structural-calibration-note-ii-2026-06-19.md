# MathDevMCP Holdout-Informed Structural Calibration Note II

## Date

2026-06-19

## Scope

This note deepens the earlier holdout-informed calibration interpretation by
comparing the **current public structural state** and the **current local-only
holdout structural state** more directly.

It is grounded in:

- `src/mathdevmcp/real_tasks_report.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `src/mathdevmcp/real_tasks_holdout_local_scoring.py`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-note-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-iii-2026-06-19.md`

This is still a **structural calibration** note. It is not a semantic benchmark
comparison and not a generalization result note.

## Evidence contract

### Question

What does a direct comparison between the current public structural benchmark
surfaces and the current local holdout structural surfaces now tell us about the
benchmark’s maturity and the remaining gaps before stronger interpretation is
justified?

### Exact baseline / comparator

Comparator A:
- current public benchmark structure and current scored public candidate-fixture
  coverage

Comparator B:
- current local-only holdout structure and current local candidate-fixture
  coverage

This note compares **structural coverage and scoreable shape**, not semantic
model performance.

### Primary criterion

The primary criterion is whether the local holdout tier is now mature enough to
support a stronger calibration interpretation than “holdout exists,” while still
remaining too immature for generalization claims.

### Veto diagnostics

This note would be unsound if any of the following were true:

- the local holdout tier were treated as public benchmark evidence;
- the current local/public comparison were treated as stable enough for policy or
  release relevance;
- missing public candidate coverage or local/public family imbalance were
  ignored;
- structural score counts were treated as semantic outcome quality.

### Explanatory-only diagnostics

The following are descriptive only:

- public case totals and by-family counts;
- public scored-candidate totals;
- local holdout case totals and by-family counts;
- local scored-candidate totals;
- current false-confidence-veto failure counts.

### What will not be concluded

This note does **not** conclude that:

- the benchmark now has holdout-backed generalization evidence;
- the public and local tiers are balanced enough for stable comparative metrics;
- the current local tier is representative;
- workflow integration, gate selection, or release-policy coupling is justified.

## Public vs local structural comparison

### Public structural state

Current public structural state:

- public case total: `12`
- public family distribution:
  - `evidence_boundary_discipline`: `5`
  - `numerical_oracle_parity`: `2`
  - `code_document_consistency`: `3`
  - `retrieval_and_provenance`: `1`
  - `derivation_boundary_and_abstention`: `1`
- scored public candidate total: `7`
- public scored family coverage currently exercised:
  - `evidence_boundary_discipline`: `4`
  - `code_document_consistency`: `2`
  - `derivation_boundary_and_abstention`: `1`
- public scored false-confidence-veto failures: `1`
- public scored candidate coverage gap remains for `5` public cases

Interpretation:

- the public benchmark is broader overall and now less sparse on the scored side
  than before;
- but it still remains only partially exercised through committed candidate
  fixtures.

### Local holdout structural state

Current local holdout structural state:

- holdout case total: `4`
- local family coverage currently present:
  - `retrieval_and_provenance`: `1`
  - `evidence_boundary_discipline`: `3`
- scored local candidate total: `4`
- local scored family coverage currently exercised:
  - `retrieval_and_provenance`: `1`
  - `evidence_boundary_discipline`: `3`
- local scored false-confidence-veto failures: `0`
- local scored candidate coverage gap remains for: none

Interpretation:

- the local holdout tier is now fully covered **for its current tiny seed**;
- it is still much smaller than the public tier, but it is more execution-ready
  relative to its own size.

## Calibration interpretation

### What the comparison now justifies

At this stage, the comparison justifies the following claim:

- the benchmark has progressed beyond “public calibration plus symbolic holdout
  policy” into a state where the public tier is more broadly fixture-covered and
  the local holdout tier is structurally scoreable enough to support a stronger
  internal calibration discussion.

In other words:

- the local holdout tier is no longer merely present;
- the public scored layer is no longer as sparse as it was in the earlier
  calibration pass;
- and both tiers can now be discussed as executable structural surfaces, even
  though neither is mature enough for strong comparative claims.

### What the comparison still does **not** justify

At this stage, the comparison still does **not** justify:

- any generalization claim from public to holdout;
- a claim that public and local tiers are comparably mature;
- a claim that the local holdout tier is broad enough for stable comparative
  metrics;
- any workflow/gate/release-policy implication.

## Main remaining calibration uncertainties

1. **Public scored coverage is better, but still incomplete**
   - the public scored layer now exercises more of the public corpus than
     before;
   - but a meaningful unscored remainder still exists.

2. **Local holdout breadth is broader and fully candidate-covered, but still
   small**
   - the local tier is now fully covered for its current seed;
   - that still does not make the local seed broad enough for strong
     generalization claims.

3. **Cross-tier family balance is still uneven**
   - both tiers include retrieval/provenance and evidence-boundary patterns, but
     the public tier still contains more varied family representation overall.

4. **Structural scoring still dominates both tiers**
   - both sides are still largely structural and bounded, not semantically rich.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the benchmark as ready for stronger holdout-informed structural calibration, but not for strong comparative claims | Met | No tier-boundary veto was crossed | Public scored coverage is still sparse and local holdout breadth is still small | Improve whichever side is the more binding coverage bottleneck for the next calibration pass, likely public scored coverage or further holdout breadth | No generalization proof, no stable public-vs-holdout metric interpretation, no benchmark completion claim |

## Post-run red-team note

### Strongest alternative explanation

The local holdout tier may now look cleaner than the public scored tier only
because it was hand-broadened together with its local candidate fixtures, while
the public tier still has a larger unscored remainder.

### What would overturn confidence

Confidence in the current interpretation would weaken if:

- broader local holdout expansion immediately exposed many veto failures or poor
  structural fit;
- public scored coverage expansion revealed that the public candidate set had
  been unusually favorable;
- later semantic layers destabilized the current structural comparison.

### Weakest part of the evidence

The weakest part of the current evidence is not the existence of both tiers. It
is the mismatch in **coverage maturity** between them: the local holdout seed is
fully covered relative to itself, while the public tier remains only partially
fixture-covered.

## Next justified action

The next justified action is to deepen calibration in a way that addresses the
most binding coverage gap.

At this moment, the sharper open question is whether to:

1. broaden public candidate-fixture coverage so public scored calibration is less
   sparse, or
2. broaden local holdout breadth further so the local tier becomes more
   representative.

Either direction is more justified than workflow or policy integration.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark has now reached a point where the limiting factor is not
whether a local holdout scoring tier exists, but how to improve the relative
coverage maturity of the public and local tiers.
