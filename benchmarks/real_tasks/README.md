# Real-task benchmark program

This directory holds the first source-of-truth artifacts for a benchmark suite that is grounded in **real mathematical/code-document tasks** rather than only synthetic fixtures.

## How this differs from `benchmarks/README.md`

The top-level benchmark fixture suite in [../README.md](../README.md) is primarily for:

- synthetic or sanitized benchmark fixtures;
- parser stability;
- seeded mismatch detection;
- narrow benchmark-gate coverage.

This `real_tasks/` program is different:

- cases are selected from actual repo artifacts in `MacroFinance`, `dsge_hmc`, `latex-papers`, and BayesFilter-related materials;
- the emphasis is on provenance, correct abstention, evidence-boundary discipline, and code-document drift;
- the first slice is documentation + manifest only, not release-gated execution.

## Corpus tiers

### `public`
Committed, CI-safe benchmark cases derived from public or sanitized artifacts.

### `holdout_local`
Locally available cases that are intentionally not day-to-day optimization targets.
See [holdout_local/README.md](holdout_local/README.md) for the current holdout-local policy and scaffolding.

### `private_external`
External/private repo or document cases that should not be committed into the public corpus.

## Why holdout and private tiers matter

A public benchmark alone is too easy to overfit, especially for retrieval and evidence-boundary tasks. The suite therefore needs:

- committed public cases for stable iteration;
- holdout-local cases to test generalization;
- private/external cases to stay aligned with the real work that motivated the benchmark.

## Path policy

The public manifest stores file and directory references as **repo-root-relative** paths from the MathDevMCP checkout root. Sibling repositories may be referenced via `../` segments when a benchmark source lives outside this checkout.

## First-slice contents

This directory currently defines only the source-of-truth artifacts needed for the first implementation slice:

- `manifests/public_cases.json` — initial public benchmark inventory;
- the companion benchmark spec in `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`.

Executable loading, validation, CLI/MCP exposure, and report integration are intentionally deferred to a later slice so the current benchmark gate remains stable.
