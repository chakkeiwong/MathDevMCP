# Phase 4 Subplan: Derive-From Route Plans

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Make `derive_from` return route plans with givens, assumptions, backend steps,
proof obligations, and route gaps instead of only packaging low-level results.

## Entry Conditions

- Phase 3 proof/counterexample evidence surface is available.
- Phase 2 assumption taxonomy is available.
- Existing derive tests pass.
- Proof and refutation evidence entries expose backend attempt, scoped
  obligation, and counterexample details when available.

## Required Artifacts

- Updated `src/mathdevmcp/derive_from.py`,
  `src/mathdevmcp/derive_or_refute.py`, and/or
  `src/mathdevmcp/proof_obligations.py`.
- Focused tests in `tests/test_derive_from.py`.
- Phase 4 result record.
- Refreshed Phase 5 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py`
- `python3 -m pytest tests/test_high_level_contracts.py tests/test_high_level_workflows.py`
- `git diff --check` over touched files.
- Claude read-only review if derivation status or proof-boundary logic changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can `derive_from` expose a useful derivation route without inventing unsupported steps? |
| Baseline/comparator | Existing `derive_from` behavior and benchmark cases RLHLB-04/RLHLB-09. |
| Primary criterion | Results distinguish context givens, explicit assumptions, backend-certified steps, concrete counterexamples or scoped contradictions, unresolved obligations, and route gaps. |
| Veto diagnostics | Proxy derivation promoted to matrix/domain result; hidden assumptions; unchecked multi-step proof; route gap reported as proof. |
| Explanatory diagnostics | Route table, obligation list, assumption ledger. |
| Not concluded | No general derivation capability, no scientific validation, no proof beyond scoped evidence. |

## Forbidden Claims/Actions

- Do not synthesize unchecked derivation chains.
- Do not promote givens to assumptions silently.
- Do not weaken not-encodable or missing-assumption boundaries.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if derivation route artifacts are structured enough to
be included in review packets and exposed through MCP.

## Stop Conditions

Stop if route planning requires domain-specific theorem design outside local
fixtures, or if tests cannot distinguish route gaps from derivation success.
