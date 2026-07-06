# Phase 2 Result: Rich `derive_from` Output

Date: 2026-07-06

Status: `PASSED`

## Objective

Attach Phase 1 derivation gaps, proposals, validation summaries, tool-use
records, and agent handoff fields to the existing high-level `derive_from`
workflow.

## Skeptical Plan Audit

Audit result: `PASSED_WITH_BOUNDARY`.

Boundary preserved:

- Existing `derive_from` proof/refutation promotion rules were not weakened.
- Free-form `givens` remain context only and are not promoted to backend
  assumptions.
- Missing-assumption repairs remain non-certifying.
- Not-encodable and unknown routes return formalization proposals, not false or
  proof claims.

## Artifacts Changed

- `src/mathdevmcp/derive_from.py`
- `tests/test_derive_from.py`

## Behavior Added

`derive_from` now attaches:

- `source`
- `coverage`
- `tool_uses`
- `gaps`
- `proposals`
- `validation`
- `agent_handoff`

The attached proposal ledger covers:

- `accept_backend_certificate` for scoped backend proofs;
- `accept_counterexample` for concrete counterexample refutations;
- `manual_review_with_named_gap` when low-level refutation lacks a concrete
  counterexample artifact and the high-level envelope remains inconclusive;
- `add_assumptions` for missing route-required assumptions, including linked
  assumption repairs;
- `formalize_target` for unknown and not-encodable routes.

## Required Checks

Passed:

- `python3 -m pytest tests/test_derive_from.py -q`
  - `7 passed`
- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
  - `24 passed`
- `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`
  - passed

Pending until this result file is included:

- `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-result-2026-07-06.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can `derive_from` return agent-consumable gaps/proposals while preserving existing proof/refutation boundaries? |
| Primary criterion | Passed for proved, refuted-with-counterexample, refuted-without-counterexample, missing-assumption, unknown, and not-encodable cases. |
| Veto diagnostics | No high-level validation failures; no refutation promotion without counterexample; no generic review action without a named gap/proposal. |
| Not concluded | No document-wide Markdown audit report yet; no new MCP/CLI command; no proof closure from assumption proposals alone. |

## Next Handoff

Phase 3 should build the public report workflow:

- source/label selection over LaTeX;
- call `derive_from` or `derive_or_refute` per target;
- emit Markdown with exact tool uses, locations, problems, mathematical reasons,
  proposed derivation fixes, backend plans, validation, and non-claims.
