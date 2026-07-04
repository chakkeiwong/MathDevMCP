# Phase 5 Subplan: Review And Decision

Date: 2026-07-03

Status: `EXECUTED_FINAL_REVIEW_AGREED`

## Phase Objective

Review the Phase 4 scored v2 artifacts and write a final bounded decision for
the collection/scoring program, preserving the distinction between local
diagnostic evidence and any public, release, scientific, product, proof, or
general reliability claim.

## Entry Conditions Inherited From Previous Phase

- Phase 4 scored JSON exists and parses:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`.
- Phase 4 scored Markdown exists:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.
- Phase 4 result exists:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-result-2026-07-03.md`.
- Local scoring checks passed.
- C-over-B interpretation is bounded to a single-response local diagnostic.
- Claude Opus review gates were previously unavailable; Claude cannot be used
  as response worker or scoring authority.

## Required Artifacts

- Phase 5 result/final decision:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-result-2026-07-03.md`.
- Updated visible execution ledger.
- Updated final stop handoff.
- Optional compact Claude review bundle and review-trail entry if an approved
  read-only reviewer model is available.

## Required Checks, Tests, Reviews

- Parse scored JSON.
- Verify scored JSON row count remains 18.
- Verify hard-veto counts precede pass-count interpretation.
- Verify final decision repeats the non-claims and one-response limitation.
- Verify no public/release/scientific/product/general-reliability claim is
  introduced.
- Run focused pytest:
  `python3 -m pytest tests/test_downstream_usefulness_prompts.py`.
- Run `git diff --check` over v2 artifacts and collection plans.
- If Claude review is used, send only a compact bounded review bundle and
  record `REVIEW_STATUS`, `VERDICT`, `RUN_DIR`, and `SUMMARY_JSON`.
- If Claude Opus remains unavailable and no reviewer substitution/waiver is
  available, stop with local result plus review-boundary limitation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the whole v2 collection/scoring program complete as a bounded local diagnostic, and what decision is justified by the scored evidence? |
| Baseline/comparator | Phase 4 scored artifacts, response manifest, frozen scoring contract, and prior repaired benchmark as historical context only. |
| Primary criterion | Phase 5 passes if final decision states the local C-over-B diagnostic result, all limitations and non-claims, review status, checks, and next justified action without crossing unsupported boundaries. |
| Veto diagnostics | Missing scored artifacts; hard-veto/pass-count order hidden; aggregate-only claim; unsupported public/release/scientific/product/proof/general-reliability claim; Claude as authority; reviewer unavailability presented as agreement. |
| Explanatory diagnostics | Claude/local review status, row counts, per-case summary, limitations, artifact list, checks. |
| Not concluded | No proof certificate, release gate, public benchmark result, scientific validation, product capability evidence, broad theorem-proving proof, or general model reliability. |

## Forbidden Claims Or Actions

- Do not change scored results unless a visible scoring error is found and
  patched under the frozen contract.
- Do not use Claude as response worker, scoring authority, or boundary
  approver.
- Do not treat absent Claude review as agreement.
- Do not hide the one-response-per-prompt limitation.
- Do not promote local diagnostic evidence into public benchmark, release,
  scientific, product, proof-correctness, broad theorem-proving, or general
  reliability claims.

## Exact Next-Phase Handoff Conditions

This is the final phase. Mark the runbook complete only if:

- Phase 5 result exists;
- final decision is bounded and cites the scored artifacts;
- checks pass;
- review status is accurately recorded;
- unresolved limitations and non-claims are explicit.

## Stop Conditions

Stop if:

- scored artifacts fail validation;
- a scoring inconsistency is found that requires Phase 4 repair;
- reviewer model access is required but unavailable and no waiver/substitute
  direction exists;
- the final decision would require any unsupported public/release/scientific/
  product/proof/general-reliability claim.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 5 result/final decision;
3. update the visible ledger and stop handoff;
4. if complete, mark the program complete with bounded non-claims.
