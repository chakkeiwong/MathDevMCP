# MathDevMCP Holdout-Local First Scoring Boundary Note

## Date

2026-06-19

## Scope

This note documents the first **local-only holdout scoring surface**.

It is not a public benchmark artifact and not a release or gate artifact.

## What exists now

The benchmark now has a local-only holdout scoring helper that:

- loads an explicitly provided or default local holdout manifest path,
- scores normalized candidate answers against those local cases using the
  existing structural scorer,
- returns a local-only score report contract,
- and preserves explicit non-public, non-gating policy boundaries.

## Why this matters

This is the first point where the holdout-local tier can be treated as more than
policy and local file scaffolding.

The holdout-local tier still does **not** have a public report, public gate, or
committed evaluated cases, but it now has a minimal executable scoring surface
for explicitly local use.

## What this does **not** mean

This does **not** mean:

- holdout-local evidence is now public benchmark evidence;
- holdout-local scoring is part of `benchmark_gate`;
- release-readiness or policy signals should consume local holdout scores;
- the holdout-local tier is mature enough to support generalization claims by
  itself.

## Boundary

The boundary for this helper is:

- local-only,
- deterministic/structural,
- explicitly provided candidate answers,
- explicitly local manifest path,
- no public artifact coupling.
