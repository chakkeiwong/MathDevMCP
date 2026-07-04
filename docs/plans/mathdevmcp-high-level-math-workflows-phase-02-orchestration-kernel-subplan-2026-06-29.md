# Phase 2 Subplan: Orchestration Kernel

## Phase Objective

Implement shared high-level orchestration helpers that route user questions to
existing low-level tools and package evidence under the Phase 1 contract.

## Entry Conditions Inherited From Previous Phase

- High-level result contract exists and passes tests.
- Low-level workbench tools are available.

## Required Artifacts

- `high_level_workflows` or equivalent orchestration module.
- Route selection helpers.
- Evidence packaging helpers.
- Low-level-to-high-level evidence mapping table for derive/prove,
  assumption, proof-gap, code/equation, and review-packet outputs.
- Kernel tests for route selection and no-overclaim behavior.
- Phase 2 result record.
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Kernel unit tests.
- Contract tests.
- Focused low-level tool tests touched by imports.
- `python3 -m py_compile` for new/touched modules.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a shared kernel call existing tools and preserve their evidence semantics? |
| Baseline/comparator | Direct low-level tool outputs. |
| Primary pass criterion | Kernel routes planned workflow types and packages evidence without changing certifying/diagnostic meaning. |
| Veto diagnostics | Kernel summarizes diagnostic evidence as proof; catches exceptions as proof/refutation; hides backend availability. |
| Explanatory diagnostics | Route decisions and nested evidence records. |
| Not concluded | User-facing workflow completeness. |
| Artifact | Kernel code/tests/result. |

## Required Evidence Mapping

Phase 2 must map existing low-level outputs into the Phase 1 envelope without
changing their mathematical meaning:

| Low-level output | High-level status | Evidence class | Certification source | Boundary rule |
| --- | --- | --- | --- | --- |
| `derive_or_refute` or `prove_or_refute` status `proved` with certifying backend attempt | `proved` | `backend_certificate` | `backend` | Only scoped backend certification is represented. |
| `derive_or_refute` or `prove_or_refute` status `refuted` with counterexample | `refuted` | `backend_counterexample` | `backend` | Requires counterexample object. |
| Low-level status `missing_assumptions` | `missing_assumptions` | `missing_assumption` | `none` | Preserve route-required, not globally minimal, assumption boundary. |
| Low-level status `backend_unavailable` | `backend_unavailable` | `backend_unavailable` | `none` | Must not refute. |
| Low-level status `not_encodable` | `not_encodable` | `not_encodable` | `none` | Must not imply falsehood. |
| `localize_proof_gap` non-proved non-refuted first gap | `gap_found` | `proof_gap` | `none` | Localizes first gap only; no global theorem-failure claim. |
| `code_implements_equation` status `consistent` | `structural_match` | `structural_match` | `none` | Structural evidence is diagnostic, not proof. |
| `code_implements_equation` status `mismatch` | `structural_mismatch` | `structural_mismatch` | `none` | Structural mismatch is not a semantic refutation. |
| `math_review_packet` any status | `diagnostic_only` unless blocked by nested high-level refutation later | `review_packet` | `none` | Review packet is never a certificate. |
| Unknown or unsupported low-level status | `inconclusive` | none or `human_review_required` | `none` | Require action/veto explaining missing evidence. |

The kernel may include raw low-level evidence as nested extension metadata
inside a Phase 1 evidence entry. It must not weaken Phase 1 validation to fit
low-level outputs.

## Forbidden Claims And Actions

- Do not add LLM-only proof routes.
- Do not change low-level tool semantics to fit the wrapper.
- Do not expose CLI/MCP commands in this phase.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 if the kernel can build compliant envelopes and route
derivation/proof/assumption/debug/code/review workflow types.

## Stop Conditions

Stop if orchestration cannot preserve low-level evidence boundaries or if
planned workflows require unavailable external services.
