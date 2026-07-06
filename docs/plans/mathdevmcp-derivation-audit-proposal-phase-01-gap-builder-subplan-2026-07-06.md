# Phase 1 Subplan: Derivation Gap/Proposal Builder

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Add a deterministic derivation gap/proposal builder that converts
`derive_or_refute`, `derive_from`, `debug_derivation`, and proof-audit evidence
into agent-consumable derivation gaps and concrete next derivation proposals.

This phase should not expose a new public CLI/MCP command yet. It creates the
internal schema and builder used by later phases.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result passed.
- Baseline `derive_from` and `derive_or_refute` tests passed or pre-existing
  blockers were recorded.
- Master program and visible runbook passed review.
- Assumption proposal builder exists and can be reused for
  `missing_assumptions` gaps.

## Required Artifacts

- New module, likely:
  `src/mathdevmcp/derivation_gap_proposals.py`
- Focused tests, likely:
  `tests/test_derivation_gap_proposals.py`
- Phase 1 result record:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md`
- Refreshed Phase 2 subplan for rich direct `derive_from` output.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`
- `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py tests/test_derivation_gap_proposals.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md`
- Claude read-only review if the builder changes proof/refutation boundary
  language or status mapping.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can low-level derivation evidence be converted into structured derivation gaps and proposals without inventing proof steps? |
| Baseline/comparator | Current route-plan evidence in `derive_from` and assumption gap/proposal builder pattern. |
| Primary criterion | Builder emits stable gaps/proposals for proved, refuted, missing-assumption, unknown, not-encodable, and backend-unavailable cases, each with validation or abstention. |
| Veto diagnostics | Diagnostic route becomes proof; counterexample missing but refutation claimed; generic "collect more evidence" without named artifact; no source evidence refs; proposal not linked to gap. |
| Explanatory diagnostics | Number of gap kinds supported, route kinds, backend attempt summaries. |
| Not concluded | No new public workflow, no source-label report, no general theorem proving. |
| Artifact | Builder module, tests, Phase 1 result. |

## Target Schema

`derivation_gap` fields:

- `id`
- `location`
- `target`
- `lhs`
- `rhs`
- `status`
- `problem`
- `why`
- `failed_route`
- `missing_assumptions`
- `backend_attempts`
- `counterexamples`
- `evidence_refs`
- `severity`

`derivation_proposal` fields:

- `id`
- `gap_ids`
- `type`
- `location`
- `proposal_text`
- `derivation_route`
- `formalization_target`
- `backend_plan`
- `validation`
- `evidence_refs`
- `application_status`

Allowed proposal types:

- `accept_backend_certificate`
- `accept_counterexample`
- `add_assumptions`
- `formalize_target`
- `split_derivation`
- `try_backend_proof`
- `supply_source_mapping`
- `manual_review_with_named_gap`

## Forbidden Claims And Actions

- Do not claim a derivation route is certified unless backend evidence is
  certifying under an explicit contract.
- Do not apply document or proof edits.
- Do not expose CLI/MCP yet.
- Do not generate Markdown until structured fields exist and tests pass.
- Do not silently promote free-form givens to formal assumptions.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- the builder handles all baseline statuses with tests;
- every proposal links to at least one gap;
- every proposal has validation or explicit abstention;
- Phase 2 subplan names exact `derive_from` fields to attach and tests to
  update.

## Stop Conditions

Stop if:

- current low-level evidence lacks enough fields to construct safe gaps and a
  smaller low-level evidence patch is needed first;
- tests reveal current status mapping is inconsistent across library/CLI/MCP;
- a proposed schema would require changing public contracts before internal
  builder behavior is proven.
