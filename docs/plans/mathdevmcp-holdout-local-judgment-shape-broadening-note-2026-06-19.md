# MathDevMCP Holdout-Local Judgment-Shape Broadening Note

## Date

2026-06-19

## Scope

This note records a bounded local holdout broadening step aimed specifically at
improving **judgment-shape representativeness**.

It remains a local population and local fixture checkpoint, not holdout-backed
generalization evidence.

## What changed locally

A new local-only holdout family was added to introduce a currently missing local
judgment shape:

- `HOLDOUT-LATEX-ABSTENTION-001`

This is a `derivation_boundary_and_abstention` family whose gold status is
`unverified`.

A matching local candidate-answer fixture was also added.

## Why this broadening matters

Before this step, the local holdout tier already had:

- `consistent`
- `mismatch`

but it did not yet have a local example whose correct outcome is explicitly
`unverified`.

That meant the local tier was still missing one important judgment shape that is
central to MathDevMCP’s benchmark philosophy: knowing when the right answer is
not to certify.

This new local case improves that gap.

## Current local judgment-shape mix

The local-only holdout seed now contains examples whose gold statuses include:

- `consistent`
- `mismatch`
- `unverified`

That is a healthier local judgment-shape distribution than before.

## What this still does **not** mean

This does **not** mean:

- the local holdout tier is now broad enough for strong generalization claims,
- the benchmark is complete,
- the local abstention family is by itself representative of all derivation
  boundary cases,
- workflow/gate/release coupling is justified.

## Why this matters now

This is a strong strategic broadening step because it adds a **new kind of
judgment** rather than merely another case of an already-represented pattern.

That makes the next holdout-informed calibration pass more informative than a
raw case-count increase would have.
