# MathDevMCP Holdout-Local Further Broadened Seed Note

## Date

2026-06-19

## Scope

This note records a further bounded broadening of the **local-only holdout
seed**.

It remains a local population and local fixture checkpoint, not holdout-backed
evaluation evidence.

## What changed locally

The local holdout seed now spans three local-only example families:

1. a `latex-papers` chapter-neighborhood retrieval/provenance family;
2. a `dsge_hmc` blocker-preservation result-note family;
3. a `MacroFinance` blocked-diagnostic/result-note family.

The local candidate-answer fixture set has also been extended to cover the new
MacroFinance family.

## Why this broadening was justified

This broadening improves the local holdout seed along an important axis:

- it is no longer only a `latex-papers` + `dsge_hmc` local mixture;
- it now includes a `MacroFinance` local-only family as well.

That improves local holdout diversity without promoting anything into the public
benchmark surface.

## Current local family mix

The local-only holdout seed now includes:

- `retrieval_and_provenance`
- `evidence_boundary_discipline` from `dsge_hmc`
- `evidence_boundary_discipline` from `MacroFinance`

The local candidate-answer fixtures now cover:

- one `dsge_hmc` local holdout case,
- one `MacroFinance` local holdout case.

## What this still does **not** mean

This checkpoint still does **not** mean:

- holdout-local scoring is broad enough to support generalization claims,
- the benchmark is complete,
- the holdout tier is ready for policy or release coupling,
- the local seed is balanced enough to stand in for mature holdout evaluation.

## Why this matters

The local holdout tier is becoming more representative by family, which is the
right direction under the master program.

But it is still only a tiny local seed. Its value is that it now gives a more
realistic foundation for later holdout-informed calibration, not that it already
proves anything strong.
