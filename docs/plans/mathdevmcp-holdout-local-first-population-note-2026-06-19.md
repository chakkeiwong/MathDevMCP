# MathDevMCP Holdout-Local First Population Note

## Date

2026-06-19

## Scope

This note records the first **local-only holdout population checkpoint**.

It does **not** record holdout evaluation, holdout scoring, or generalization
results.

The purpose of the checkpoint is only to show that the holdout-local workflow
has moved from:

- policy,
- scaffold,
- recipe,
- example note,
- and helper/initializer support

into one actual local populated artifact outside the committed benchmark
surface.

## What was populated locally

A local-only holdout manifest was initialized and populated at:

- `.local/mathdevmcp/holdout_local_cases.json`

This path is now ignored by repo policy and remains outside the committed public
benchmark surface.

## Chosen example family

The first local populated example follows the already-documented family from:

- `docs/plans/mathdevmcp-holdout-local-population-example-2026-06-19.md`

That family uses:

- a larger `latex-papers` chapter-neighborhood case,
- intentionally disjoint from public `LP-01` / `LP-02`,
- category: `retrieval_and_provenance`.

## Why this case remains holdout-local

Disjointness rationale used for the local entry:

- `different_label_neighborhood`
- `different_task_template`

This is enough to keep the case in the holdout-local tier under the current
policy.

## What this checkpoint does **not** mean

This checkpoint does **not** mean:

- holdout-local evaluation has been run,
- the case has been scored,
- the benchmark now has holdout evidence,
- the benchmark now supports generalization claims,
- overfitting risk has been reduced in practice.

This is a local population checkpoint only.

## Why this checkpoint is useful

This is the first point at which the holdout-local workflow becomes materially
real rather than purely documentary:

- the path is ignored by git,
- the helper/initializer path works,
- a local entry now exists in the intended local location,
- and the public benchmark surface remains unchanged.

## Verification

The checkpoint is successful if all of the following are true:

- `.gitignore` excludes `.local/mathdevmcp/`;
- `.local/mathdevmcp/holdout_local_cases.json` exists locally;
- committed tests do not depend on this file;
- no public report, manifest, or gate path consumes this local artifact.
