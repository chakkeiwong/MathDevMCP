# Phase 3 Subplan: Derive From Workflow

## Phase Objective

Implement `derive_from(target, givens)` for "Can I derive X from Y?" questions.

## Entry Conditions Inherited From Previous Phase

- Shared contract and orchestration kernel exist.
- Low-level `derive_or_refute` and assumption diagnostics are available.

## Required Artifacts

- `derive_from` function.
- Explicit givens/assumptions boundary: free-form `givens` are recorded as
  context and are not claimed to be used as formal proof assumptions unless the
  caller supplies `assumptions` that the low-level route can consume.
- Tests for proof, refutation, missing assumptions, not-encodable, backend
  boundary cases, and phase-local false-confidence traps.
- Phase 3 result record.
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- `derive_from` tests.
- Kernel/contract tests.
- Low-level `derive_or_refute` tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow answer derivability questions with proof/refutation/abstention evidence? |
| Baseline/comparator | Direct `derive_or_refute` outputs and assumption diagnostics. |
| Primary pass criterion | True identities prove, false identities refute, missing assumptions are explicit, unsupported syntax abstains, and local mutation/negative controls catch proof-boundary promotion. |
| Veto diagnostics | Givens silently claimed as formal proof assumptions; missing assumptions silently inserted; unsupported syntax becomes proof/refutation. |
| Explanatory diagnostics | Nested low-level evidence and assumptions. |
| Not concluded | General derivability beyond scoped target/givens. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not invent derivation steps without backend/tool support.
- Do not treat nearby notation or givens text as proof.
- Do not claim that `givens` were formally used unless they are also present in
  explicit route assumptions or backend evidence.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 if `derive_from` returns compliant envelopes and passes
negative-control tests.

## Stop Conditions

Stop if target/givens parsing cannot be scoped enough to avoid overclaims.
