# MathDevMCP Holdout-Local Candidate Fixture Boundary Note

## Date

2026-06-19

## Scope

This note documents the boundary for the first **local holdout candidate-answer
fixture scaffold**.

It is not a public benchmark fixture and not a release or gate artifact.

## What exists now

The holdout-local workflow now has a committed local-only template for candidate
answers and a local-only fixture runner that can score explicitly provided local
candidate answers against local holdout cases.

## Why this matters

This improves local holdout execution ergonomics:

- users can scaffold local candidate answers in a stable shape,
- local holdout scoring can be repeated without hand-writing every candidate in
  a Python call,
- but nothing about this turns holdout artifacts into public benchmark inputs.

## Boundary

The boundary for local holdout candidate fixtures is:

- local-only,
- deterministic/structural,
- explicitly separate from public candidate fixtures,
- not public benchmark evidence,
- not benchmark-gate evidence,
- not release-readiness evidence.

## What this does **not** mean

This does **not** mean:

- holdout candidate fixtures are now part of the committed public benchmark
  surface,
- local fixture scoring can be reported as public benchmark results,
- the benchmark is ready for policy coupling.
