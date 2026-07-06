# Phase 2 Subplan: Attach Rich Derivation Gaps To `derive_from`

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Expose the Phase 1 internal derivation gap/proposal builder through the
existing high-level `derive_from` workflow so an agent can ask "can I derive
this?" and receive a gap/proposal packet rather than a bare yes/no or generic
review action.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result is `PASSED`.
- `src/mathdevmcp/derivation_gap_proposals.py` exists.
- `tests/test_derivation_gap_proposals.py` passes.
- Existing `derive_from` and `derive_or_refute` tests pass.
- `git diff --check` over Phase 1 files passes.

## Required Artifacts

- Updated `src/mathdevmcp/derive_from.py`.
- Updated `tests/test_derive_from.py`.
- Optional targeted additions to `tests/test_derivation_gap_proposals.py` only
  if the integration exposes a missing schema boundary.
- Phase 2 result record:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-result-2026-07-06.md`.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`
- `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-result-2026-07-06.md`
- Local schema validation through existing `validate_high_level_result` tests.
- Claude read-only review only if external review approval is explicitly
  granted or if the phase changes public proof/refutation status semantics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can `derive_from` return agent-consumable gaps/proposals while preserving existing proof/refutation boundaries? |
| Baseline/comparator | Current `derive_from` high-level envelope plus Phase 1 internal builder packet. |
| Primary criterion | `derive_from` returns `gaps`, `proposals`, `validation`, `tool_uses`, and `agent_handoff` for proved, refuted, missing-assumption, unknown, not-encodable, and backend-unavailable statuses. |
| Veto diagnostics | High-level validator fails; proof is promoted without certifying backend artifact; refutation is promoted without counterexample in high-level workflow; generic review action appears without named gap/proposal; existing tests regress. |
| Explanatory diagnostics | Proposal type counts, validation status counts, backend attempt count, counterexample count. |
| Not concluded | No document-wide audit report yet; no CLI/MCP exposure change unless already inherited from `derive_from`; no claim that proposed assumptions prove the derivation. |
| Artifact | Updated `derive_from`, tests, Phase 2 result. |

## Exact Output Fields To Attach

For successful low-level `derive_or_refute` calls, attach:

- `gaps`: from `build_derivation_gaps(low_level, source=source)` if `source`
  support is added, otherwise direct target location.
- `proposals`: from `build_derivation_proposals(gaps)`.
- `validation`: from `summarize_derivation_validation(proposals)`.
- `tool_uses`: from `build_derivation_tool_uses(target, givens, assumptions,
  backend)`, possibly appended to existing route-plan evidence.
- `agent_handoff`: includes scoped question, status, reason, source context,
  derivation gap ledger, proposals, validation, non-claims, next actions, and
  certification boundary.

For `ValueError`/not-encodable targets, either:

- route through a small synthetic low-level not-encodable packet and the same
  builder, or
- attach a single formalization gap/proposal with the same validation policy.

The first option is preferred if it keeps the output schema uniform.

## Forbidden Claims And Actions

- Do not change `derive_or_refute` status semantics in this phase.
- Do not weaken `derive_from` high-level validation.
- Do not claim assumption repairs prove the derivation.
- Do not promote free-form `givens` into explicit backend assumptions.
- Do not expose a new MCP/CLI command in this phase.
- Do not edit the risky-debt document.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if:

- `derive_from` has rich gap/proposal output for all baseline statuses;
- all existing derivation tests pass;
- every proposal has a validation object and gap link;
- Phase 3 subplan states whether to expose a public report/Markdown workflow,
  and which source indexing or label-selection tools it will call.

## Stop Conditions

Stop if:

- attaching fields breaks `validate_high_level_result` in a way that requires a
  broader public contract decision;
- the not-encodable branch cannot be made schema-consistent without changing
  low-level contracts;
- tests reveal inconsistent status mapping between `derive_or_refute` and
  `derive_from` that requires a human decision.
