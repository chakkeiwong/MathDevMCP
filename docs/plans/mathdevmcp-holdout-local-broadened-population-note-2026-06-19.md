# MathDevMCP Holdout-Local Broadened Population Note

## Date

2026-06-19

## Scope

This note records a bounded broadening of the **local-only holdout population**.

It remains a local population checkpoint, not holdout evaluation evidence.

## What changed locally

The local holdout manifest and local candidate-answer fixture set were broadened
from a single example family to two local-only example families:

1. a `latex-papers` larger chapter-neighborhood retrieval/provenance family;
2. a `dsge_hmc` blocker-preservation result-note family.

The local artifacts remain under:

- `.local/mathdevmcp/holdout_local_cases.json`
- `.local/mathdevmcp/holdout_local_candidate_answers.json`

and remain ignored by repo policy.

## Why broadening was justified

The first local-only holdout entry exercised one retrieval/provenance-style
family. Broadening to a second family improves local holdout diversity without
promoting anything into the public benchmark surface.

The second family was chosen because it differs by:

- source-family,
- blocker/evidence-boundary pattern,
- and author-exposure context.

That keeps the holdout-local disjointness logic active in practice rather than
just in policy.

## Current local family mix

Local-only holdout example families now include:

- `retrieval_and_provenance`
- `evidence_boundary_discipline`

This is still only a tiny local seed, but it is better than a single-family
local example.

## What this does **not** mean

This checkpoint does **not** mean:

- holdout-local evaluation has now been completed,
- holdout-backed generalization evidence exists,
- local holdout scoring is ready for policy or release use,
- the benchmark is complete.

This is still local population and local fixture/scoring preparation only.

## Why this matters

This broadening is useful because it shifts the holdout-local tier from:

- one example family,

to:

- at least a small multi-family local seed.

That makes future holdout-informed calibration more realistic without exposing
those cases to the public benchmark surface.
