# Holdout-local benchmark scaffold

This directory documents the **holdout-local** tier of the real-task benchmark
program.

## What `holdout_local` means

Holdout-local cases are locally available benchmark cases that are intentionally
kept outside the committed public benchmark corpus.

Their purpose is to help evaluate whether improvements seen on the public set
generalize beyond that public development/calibration surface.

## What qualifies a case as holdout-local

A holdout-local case should differ from the public benchmark set by at least one
meaningful axis, such as:

- different source repo area or document family;
- different label neighborhood or chapter neighborhood;
- different task template;
- different benchmark-author exposure status.

A case is **not** meaningfully holdout-local if it differs only by filename or
minor path placement while preserving the same effective benchmark template.

## Why it is not in the public manifest

The committed public manifest is a stable development/calibration artifact.

The holdout-local tier exists to reduce overfitting pressure on that public set.
If holdout cases were committed and optimized against in the same way, they
would stop serving their evaluation-separation role.

## What a developer may use it for

Holdout-local cases may be used for:

- milestone evaluation;
- pre-release benchmark sanity checks;
- public-calibration cross-checks;
- bounded local quality review.

They should **not** be repeatedly tuned against as though they were ordinary
public development fixtures.

## What must not be concluded from public-only results

Improvement on the public benchmark set alone is **development/calibration
evidence**, not holdout evidence.

Until holdout-local evaluation is actually run, public-only benchmark
improvement must not be described as:

- generalization evidence,
- reduced overfitting risk,
- benchmark maturity beyond public calibration,
- release-readiness evidence.

## Relationship to the private/external tier

Holdout-local is **not** the same as `private_external`.

- `holdout_local` is an evaluation-separation tier for locally available cases.
- `private_external` is the later tier for external/private repos and corpora
  with additional privacy and redaction requirements.

## Scaffolding in this slice

This slice provides only:

- this README;
- `../manifests/holdout_local_cases.template.json`;
- the holdout-local population guidance in:
  - `docs/plans/mathdevmcp-holdout-local-population-recipe-2026-06-18.md`
  - `docs/plans/mathdevmcp-holdout-local-candidate-inventory-2026-06-18.md`

The template is a schema-aligned scaffold, not committed evaluated data.
