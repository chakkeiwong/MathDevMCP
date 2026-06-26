# MathDevMCP Holdout-Local Failure-Shape Broadening Note

## Date

2026-06-19

## Scope

This note records a bounded local holdout broadening step specifically aimed at
exposing a **different local failure shape**.

It remains a local population / local fixture checkpoint, not holdout-backed
generalization evidence.

## What changed locally

A new local-only holdout case was added that is explicitly designed to test a
failure shape rather than only a safe local summary.

Added local case:

- `HOLDOUT-DSGE-BLOCKER-VIOLATION-001`

Added local fixture:

- `fixture-holdout-dsge-violation-001`

## Why this broadening matters

Previously, the local holdout tier was fully covered, but all currently scored
local fixtures produced `consistent` outcomes. That made the comparative
calibration notes correctly question whether the local seed was exposing enough
failure variety.

This new local case is deliberately shaped to test:

- blocker erasure,
- overpromotion of a preserved engineering blocker,
- and local mismatch/veto behavior.

That makes the holdout-local tier more informative as a calibration instrument.

## What this still does **not** mean

This step does **not** mean:

- the local holdout tier is now representative,
- holdout-backed generalization is established,
- the benchmark is complete,
- workflow/gate/release integration is justified.

It only means the local holdout seed now includes at least one explicit
violation-oriented case rather than only safe summary cases.
