# Phase 1 Result: Derivation Gap/Proposal Builder

Date: 2026-07-06

Status: `PASSED`

## Objective

Add an internal deterministic builder that converts low-level derivation
evidence into agent-consumable derivation gaps and concrete proposals without
claiming proof beyond certifying backend evidence.

## Skeptical Plan Audit

The Phase 1 plan was checked before implementation for wrong baselines, proxy
criteria, missing stop conditions, hidden assumptions, environment mismatch,
and commands whose artifacts would not answer the question.

Audit result: `PASSED_WITH_BOUNDARY`.

Boundary preserved:

- The builder translates existing `derive_or_refute` evidence only.
- It does not expose a new public CLI or MCP command.
- It does not change derivation truth values.
- It treats diagnostic routes, assumption proposals, not-encodable results, and
  backend-unavailable results as non-certifying.
- It accepts proof only from certifying backend attempts and refutation only
  from concrete counterexample artifacts.

## Artifacts Created

- `src/mathdevmcp/derivation_gap_proposals.py`
- `tests/test_derivation_gap_proposals.py`

## Behavior Added

The new builder provides:

- `build_derivation_gaps`
- `build_derivation_proposals`
- `summarize_derivation_validation`
- `build_derivation_tool_uses`
- `build_derivation_gap_proposal_packet`

Supported baseline statuses:

| Status | Proposal behavior | Validation boundary |
| --- | --- | --- |
| `proved` | `accept_backend_certificate` | certifying only with backend status `proved` and severity `certifying` |
| `refuted` | `accept_counterexample` | certifying only with a concrete counterexample artifact |
| `missing_assumptions` | `add_assumptions` | links to assumption gap/proposal builder; non-certifying |
| `unknown` | `formalize_target` | abstains and asks for typed obligation/backend retry |
| `not_encodable` | `formalize_target` | blocked by encoding gap; not false |
| `backend_unavailable` | `try_backend_proof` | blocked by backend availability; not refutation |

## Required Checks

Passed:

- `python3 -m pytest tests/test_derivation_gap_proposals.py -q`
  - `8 passed`
- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
  - `23 passed`
- `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`
  - passed

Pending until this result file is committed to the diff:

- `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py tests/test_derivation_gap_proposals.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can low-level derivation evidence be converted into structured gaps and proposals without inventing proof steps? |
| Primary criterion | Passed for proved, refuted, missing-assumption, unknown, not-encodable, and backend-unavailable cases. |
| Veto diagnostics | No generic `collect_more_evidence`; every proposal links to a gap; every proposal has validation; proof/refutation boundary is preserved. |
| Not concluded | No public workflow exposure yet; no document-wide source-label report; no general theorem proving. |

## Review Boundary

Claude read-only review was not rerun for Phase 1 because the previous review
gate was rejected by the approval reviewer due external data export risk. This
phase did not change public proof/refutation status mapping, so local tests and
Codex-supervised review were used as the implementation gate.

## Next Handoff

Proceed to Phase 2 only after `git diff --check` passes for the Phase 1 files.

Phase 2 should attach the internal builder output to `derive_from` so direct
agent calls return:

- `gaps`
- `proposals`
- `validation`
- `tool_uses`
- `agent_handoff`

without weakening the existing high-level result validation contract.
