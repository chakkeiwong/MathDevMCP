# MathDevMCP Structural-Score Ceiling Note

## Date

2026-06-19

## Scope

This note defines the current **structural-score ceiling** for the benchmark.

It answers a benchmark-driven product question:

> What can the current deterministic structural scorer and tiny normalization
> prototype support safely, and where would broader semantic interpretation be
> required before further expansion is justified?

This note is a boundary artifact, not a semantic-evaluator plan and not a
release/gate artifact.

## Why this note exists

The benchmark now has enough scoring and normalization machinery that the main
remaining uncertainty is no longer “can we score anything?” It is:

- where structural scoring is already safe,
- where bounded normalization is enough,
- and where further expansion would require richer semantic judgment.

Without making that boundary explicit, future work risks drifting into semantic
expansion merely because another case is implementable.

## Current capability buckets

### 1. Structural-safe now

These are cases where the current benchmark can safely rely on the existing
structural scorer and committed candidate-answer fixture shape without needing a
normalization adapter.

Typical characteristics:

- explicit expected status/substatus,
- explicit required terms,
- explicit forbidden claims,
- explicit required next actions,
- no nuanced label extraction or paraphrase-heavy interpretation needed.

Representative public cases:

- `DH-05-sgu-exact-manifold-blocker`
- `DH-07-neutra-real-nk-migration-not-complete`
- `DH-04-bayesfilter-engineering-qualification-boundary`
- `RA-01-parser-benchmark-inventory`
- `MF-02-large-scale-lgssm-missing-data-policy`

Representative local holdout families:

- blocker-preservation local cases,
- local policy-contract cases,
- local inventory-structure cases,
- local violation-probe cases.

Why these are structural-safe:

- the benchmark’s current contract already encodes what must be present or absent;
- candidate answers can be written in the normalized object shape directly;
- false-confidence-veto behavior remains explicit and testable.

### 2. Structural-safe with bounded normalization

These are cases where a tiny case-whitelisted normalization step is acceptable
before scoring.

Typical characteristics:

- strong lexical anchors exist,
- no label-heavy extraction is required,
- candidate-answer fields can be reconstructed deterministically from the text,
- failure to find anchors can safely return `inconclusive`.

Current supported examples:

- `MF-03-hmc-helper-nonclaim-boundary`
- `MF-04-short-hmc-acceptance-veto-diagnosis`
- `DH-06-densesoap-source-contract-mismatch`

Why these fit the bounded-normalization bucket:

- they are governed by explicit phrases such as:
  - `R-hat`,
  - `diagnostic only`,
  - `not authorized`,
  - explicit forbidden-claim phrases,
- they do not require broad semantic paraphrase handling,
- the normalizer is still fail-closed and case-whitelisted.

### 3. Semantic-needed / not yet justified

These are cases where current structural scoring or tiny normalization is not a
safe basis for further expansion without a new justification.

Typical characteristics:

- label-heavy or chapter-neighborhood-dependent interpretation,
- derivation/reconciliation tasks with multiple acceptable phrasings,
- cases where the answer quality depends on reasoning over broader context,
- cases where extending the whitelist would likely become ad hoc and fragile.

Representative current examples:

- broader retrieval/provenance neighborhood cases,
- some derivation/reconciliation cases beyond the current explicit phrase set,
- future local or public cases whose acceptable answers are too semantically rich
  for deterministic phrase anchoring.

A concrete public example that illustrates the edge of this boundary is:

- `LP-02-basis-reconciliation-audit`

The current structural contract can score a normalized candidate object, but
blindly broadening the free-form normalizer for similar cases would risk
sliding from bounded lexical normalization into a pseudo-semantic evaluator.

## Practical rule for future expansions

A proposed benchmark expansion should be accepted only if it fits one of these:

1. **structural-safe now**
   - use the current scorer directly;
2. **bounded-normalization-safe**
   - add a narrow whitelist rule only if anchors are strong and fail-closed
     behavior remains obvious.

If a case does **not** fit either, it belongs in the semantic-needed bucket and
should not be expanded casually.

## Stop conditions

Stop and reassess rather than extend the benchmark if:

- a new normalization path needs many case-specific heuristics;
- acceptable answers are too paraphrase-dependent to score structurally;
- the extension would weaken forbidden-claim or false-confidence-veto behavior;
- the case’s meaning depends more on broader semantic interpretation than on the
  current normalized object contract.

## Implications for the improvement program

This note clarifies that future semantic/normalization work should be justified
only after asking:

- is this case still structural-safe?
- or does it now require a richer semantic evaluator?

That means the next improvement phases should be read as:

- use structural scoring where it is already trustworthy;
- use bounded normalization only where anchors remain explicit;
- resist semantic drift unless there is a strong benchmark-driven reason.

## Non-claim boundary

This note does **not** mean the benchmark is semantically mature.

It means the benchmark now has a clearer boundary between:

- what it can already do safely,
- what it can do with a tiny bounded adapter,
- and what should remain out of scope until a richer semantic layer is
  deliberately justified.
