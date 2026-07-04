# MathDevMCP Answer-Normalization Prototype Calibration Note

## Date

2026-06-19

## Scope

This note records the current capability boundary of the tiny answer-
normalization prototype.

It is grounded in:

- `src/mathdevmcp/real_tasks_answer_normalization.py`
- `src/mathdevmcp/real_tasks_scoring.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `tests/test_real_tasks_answer_normalization.py`
- `docs/plans/mathdevmcp-real-tasks-benchmark-structural-scoring-calibration-note-2026-06-18.md`

The note is about **normalization capability**, not semantic benchmark
execution in general.

## Evidence contract

### Question

What can the current case-whitelisted answer-normalization prototype already do,
and what does it still not justify us to claim?

### Exact baseline / comparator

The baseline is the prior benchmark state where normalized candidate-answer
objects were either hand-authored in tests or loaded from committed candidate
fixtures.

The current slice adds a narrow adapter from free-form answers into that
candidate shape for a tiny whitelist of public cases.

### Primary criterion

The primary criterion is whether the prototype can safely normalize a tiny set
of clearly anchored free-form answers into the existing candidate-answer object
shape **without** weakening the scorer’s false-confidence boundaries.

### Veto diagnostics

This note would be unsound if any of the following were true:

- the normalizer silently normalized unsupported case IDs;
- partial answers with missing anchors normalized anyway;
- forbidden stronger claims were dropped during normalization;
- the prototype was described as a general semantic evaluator.

### Explanatory-only diagnostics

Useful but non-promoting diagnostics include:

- number of whitelisted cases;
- whether positive tests pass;
- whether one mismatch case is supported;
- the fact that normalization composes with scoring.

### What will not be concluded

This note does **not** conclude that:

- MathDevMCP has a general free-form answer evaluator;
- arbitrary paraphrases are reliably normalized;
- label-heavy or nuance-heavy benchmark cases are now supported;
- holdout or private tiers can use the same prototype without further review.

## Current prototype coverage

The current normalizer supports only a tiny whitelist of public cases:

- `MF-03-hmc-helper-nonclaim-boundary`
- `MF-04-short-hmc-acceptance-veto-diagnosis`
- `DH-06-densesoap-source-contract-mismatch`

Interpretation:

- this is enough to demonstrate three distinct normalization patterns:
  - safe positive/`consistent`
  - blocked/inconclusive
  - explicit mismatch/diagnostic-only boundary
- it is deliberately far from general coverage.

## Structural findings

### 1. The normalizer remains case-whitelisted and fail-closed

Unsupported case IDs still return `inconclusive` rather than attempting broad
normalization.

Answers missing required lexical anchors also return `inconclusive`.

Interpretation:

- this is the correct safety posture for a prototype layer;
- the current normalizer is acting as a bounded adapter, not a guesser.

### 2. Forbidden stronger claims survive normalization

The prototype preserves forbidden stronger claims into the normalized
`claims` field. This means downstream structural scoring can still veto them.

Interpretation:

- the normalizer does not weaken benchmark safety by hiding overclaims;
- this is one of the most important properties of the current design.

### 3. The prototype now exercises three outcome styles

With the addition of `DH-06`, the normalizer now demonstrates:

- a safe positive/evidence-boundary case (`MF-03`),
- a blocked/inconclusive diagnostic case (`MF-04`),
- a mismatch/diagnostic-only source-contract case (`DH-06`).

Interpretation:

- the prototype boundary is stronger than the earlier two-case version;
- but the layer is still lexically anchored and not yet suitable for more
  nuanced, label-heavy, or paraphrase-heavy cases.

## Verification

The focused normalization tests now cover:

- successful normalization for `MF-03`
- successful normalization for `MF-04`
- successful normalization for `DH-06`
- fail-closed unsupported case ID behavior
- fail-closed missing-anchor behavior
- preservation of forbidden claims
- end-to-end normalization → scoring composition for:
  - safe `MF-03`
  - overclaiming `MF-03`
  - safe `MF-04`
  - safe `DH-06`

## Calibration interpretation

### What the prototype *does* justify

At this stage, the normalization prototype justifies the following claims:

1. a tiny free-form answer adapter can be built without changing the scoring
   contract;
2. the scorer’s false-confidence veto boundary can survive normalization;
3. one mismatch-case path can be normalized safely using explicit lexical
   anchors;
4. the benchmark now has a minimal path from free-form answer text to scored
   structural evaluation for a tiny public-case whitelist.

### What it still does **not** justify

At this stage, the prototype does **not** justify the following claims:

1. that general semantic normalization is solved;
2. that the benchmark can score arbitrary free-form answers reliably;
3. that this layer should yet be used for policy, release, or broad workflow
   integration;
4. that harder retrieval/provenance or derivation-heavy public cases are ready
   for the same normalization approach.

## Main uncertainties

1. **Lexical brittleness**
   - the current anchors are intentionally strict;
   - acceptable paraphrase variation is still mostly unsupported.

2. **Case scalability**
   - adding more cases may quickly force repeated custom logic;
   - the current note does not yet say where the bounded whitelist should stop.

3. **Label-heavy and nuance-heavy cases**
   - `LP-01` and `LP-02` remain deliberately out of scope;
   - that boundary is appropriate now, but means the prototype does not yet help
     with the hardest case families.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Keep the answer-normalization layer as a bounded whitelist prototype | Met | No normalization-boundary veto found | Lexical brittleness and unknown scaling beyond the first three cases | Add cases only when they are public, audited, and can still be fail-closed under explicit anchors | No general semantic evaluator and no broad free-form benchmark execution claim |

## Post-run red-team note

### Strongest alternative explanation

The prototype may appear stronger than it is because the current supported cases
have unusually explicit lexical anchors and strong benchmark metadata. That does
not mean the same approach will work cleanly for more nuanced or label-heavy
cases.

### What result would overturn confidence

Confidence would weaken if:

- adding one or two more cases immediately forced ad hoc, fragile, or
  contradictory normalization logic;
- normalization began dropping forbidden claims or softening veto conditions;
- later calibration showed the current answer texts had to be phrased too
  unnaturally to normalize safely.

### Weakest part of the evidence

The weakest part of the current evidence is not correctness of the supported
three-case paths; it is uncertainty about how fast the whitelist approach stops
being worth extending.

## Next justified action

The next justified action is either:

1. stop normalization expansion temporarily and prioritize holdout-local
   population and scored calibration over richer public candidate sets, or
2. add only another very clearly structured public case if it can still be
   normalized without weakening the fail-closed boundary.
