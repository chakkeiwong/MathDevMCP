# Phase 2 Subplan: Assumption Route Taxonomy

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Upgrade assumption discovery from keyword-style output toward route-specific
assumption ledgers for likelihood, score, neural-solver, and affine-recursion
cases.

## Entry Conditions

- Phase 1 evidence ledger is available and validated.
- Existing `assumptions_for` tests pass.
- High-level workflow results expose an optional `evidence_ledger` that Phase 2
  can reuse for route-category provenance without claiming general semantic
  correctness.

## Required Artifacts

- Updated `src/mathdevmcp/assumption_discovery.py`,
  `src/mathdevmcp/assumptions_for.py`, and/or
  `src/mathdevmcp/domain_templates.py`.
- Focused tests in `tests/test_assumptions_for.py`.
- Explicit taxonomy oracle/provenance artifact for the scoped benchmark-like
  cases used in tests.
- Evidence-ledger integration for assumption route categories where present.
- Phase 2 result record.
- Refreshed Phase 3 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_assumptions_for.py tests/test_high_level_workflows.py`
- `git diff --check` over touched files
- Claude read-only review if new taxonomy semantics materially affect claims

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP report route-required assumptions in reusable typed categories? |
| Baseline/comparator | Existing `assumptions_for` behavior, Phase 1 evidence ledger, and repaired benchmark cases RLHLB-02, RLHLB-05, RLHLB-09. |
| Primary criterion | Assumption outputs match the predeclared scoped-fixture taxonomy oracle for route categories and preserve non-minimality boundaries. |
| Veto diagnostics | Claims global minimal assumptions; silently invents assumptions; omits covariance/domain/masking/route-link assumptions required by the scoped taxonomy oracle. |
| Explanatory diagnostics | Matched/missing assumption set tests, route-category coverage, and oracle/provenance review. |
| Not concluded | No proof of sufficiency unless separately established; no scientific validation. |

## Forbidden Claims/Actions

- Do not claim route-required assumptions are globally minimal or generally
  semantically correct beyond the scoped oracle.
- Do not promote assumptions to facts.
- Do not alter benchmark expected scores.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if proof/counterexample workflows can consume or
display assumption ledgers without ambiguity.

## Stop Conditions

Stop if templates become domain-inaccurate, if tests require unsupported
mathematical claims, or if assumption categories cannot be validated locally.
