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

## Real-Local High-Level Pilot

`high_level_pilot_cases.json` is a committed local pilot inventory for five
real-source high-level workflow cases. It is local/non-gating evidence only.

Run the pilot:

```bash
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-pilot --root "$PWD"
```

The command's `passed` status means only that the executable probes passed
their declared boundary checks. All five full source obligations remain
`adapter_required`.

This pilot is not benchmark-gate evidence, not public redistributability
evidence, not release-readiness evidence, not scientific validation, and not a
claim of full LaTeX derivation competence or broad theorem-proving ability.

## Real-Local Source Adapters

The source-adapter report evaluates the same five local source obligations with
bounded, line-linked source packets and deterministic local-schema checks.

Run the report:

```bash
PYTHONPATH=src python -m mathdevmcp.cli real-local-source-adapters --root "$PWD"
```

For the frozen local manifest, the current report is expected to be `partial`:

- `RLHL-01` has a local sign inconsistency candidate;
- `RLHL-06`, `RLHL-07`, and `RLHL-10` have bounded source support;
- `RLHL-04` remains `human_review_required` with an uncleared
  `adapter_required` residual because the frozen likelihood packet omits the
  source-anchored positive-definite innovation-covariance assumption.

The command exits successfully for `partial` because a visible residual gap is
an honest governed report state, not a command failure.

The source-adapter report keeps source-adapter, executable-probe, and
residual-gap ledgers separate and emits no aggregate accuracy metric. It is
local/non-gating only and must not be used as benchmark-gate evidence, public
redistributability evidence, release-readiness evidence, scientific validation,
or a claim of broad theorem-proving ability.

## Real-Local High-Level Workflow Benchmark Closure

`real_local_high_level_workflow_benchmark_cases.json` is the frozen local
nine-case benchmark manifest for high-level workflow closure. It extends the
pilot/source-adapter work with local cases for:

- derivation debugging;
- assumption discovery;
- scoped proof/counterexample behavior;
- math-to-code structural audit;
- review-packet packaging;
- source-boundary and opaque semantic-placeholder negative controls.

Run the closure reports:

```bash
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-benchmark-schema --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-routes --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-baseline --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-packets --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-final-matrix --root "$PWD"
```

The schema report validates the local manifest. The route report records
source/backend/review-packet availability before workflow execution. The
baseline report runs current high-level workflows against the frozen manifest.
The packet report creates durable review packets from the baseline outputs.
The final matrix summarizes the final per-case route, verdict, repair round,
residual limitation, and local-regression-only status.

Interpret these reports case by case:

- `aggregate_accuracy` is intentionally `null`.
- A route gap, backend-unavailable state, not-encodable state, or review packet
  is not a proof or refutation.
- Opaque semantic-placeholder equalities need explicit source-backed or formal
  evidence before proof or refutation.
- Durable packets are human-review aids and preserve residual gaps,
  counterexamples, assumptions, actions, and non-claims.

This benchmark closure surface remains local/non-gating. It is not part of the
formal release benchmark gate, not public redistributability evidence, not
release-readiness evidence, not scientific validation, not external
reproducibility evidence, and not a claim of full LaTeX derivation competence
or broad theorem-proving ability.
