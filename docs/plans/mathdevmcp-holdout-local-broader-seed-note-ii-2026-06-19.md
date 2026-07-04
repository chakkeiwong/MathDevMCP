# MathDevMCP Holdout-Local Broader Seed Note II

## Date

2026-06-19

## Scope

This note records another bounded broadening of the **local-only holdout seed**.

It remains a local population and local fixture checkpoint, not holdout-backed
generalization evidence.

## What changed locally

The local holdout seed now spans five local-only example families.

The new addition is a `MacroFinance` policy-contract style family based on the
missing-data policy lane. This broadens the local tier beyond:

- retrieval/provenance,
- result-note blocker families,
- and inventory-structure families,

by adding an explicit local policy-contract family.

The local candidate-answer fixture set has also been extended to cover this new
local case.

## Current local family mix

The local-only holdout seed now includes:

- `retrieval_and_provenance`
- `evidence_boundary_discipline` from `dsge_hmc`
- `evidence_boundary_discipline` from `MacroFinance`
- `evidence_boundary_discipline` from `MacroFinance/ResearchAssistant`
- `numerical_oracle_parity` from `MacroFinance`

The local candidate-answer fixtures now cover all currently populated local
holdout entries.

## Why this broadening was justified

This broadening improves local representativeness because it adds a new task
style that is not only another blocker or narrative boundary case.

It introduces a local policy-contract family, which is useful for checking that
future holdout-informed calibration is not dominated only by evidence-boundary
notes.

## What this still does **not** mean

This still does **not** mean:

- the local holdout tier is broad enough for strong comparative claims,
- holdout-backed generalization is established,
- the benchmark is complete,
- workflow/gate/release coupling is justified.

## Why this matters

The holdout-local seed is now broader by both source family and task template.
That makes the local tier a stronger basis for the next calibration pass, even
though it remains small and local-only.
