# Phase 1 Subplan: Source Target Extraction

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Add deterministic extraction of smaller derivation targets from LaTeX label
blocks: displayed equations, individual align rows, equation labels, lhs/rhs,
source text, parent label, file, and line provenance.

## Entry Conditions Inherited From Previous Phase

- Phase 0 plan/review gate passed.
- Existing LaTeX index can locate risky-debt labels.
- Current report workflow remains green.

## Required Artifacts

- New module:
  `src/mathdevmcp/derivation_target_extraction.py`
- New tests:
  `tests/test_derivation_target_extraction.py`
- Phase 1 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-01-target-extraction-result-2026-07-06.md`
- Refreshed Phase 2 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derivation_target_extraction.py -q`
- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derive_from.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_target_extraction.py`
- `git diff --check -- src/mathdevmcp/derivation_target_extraction.py tests/test_derivation_target_extraction.py docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-01-target-extraction-result-2026-07-06.md`
- Claude read-only review if extraction changes source/provenance semantics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can label blocks be converted into smaller source-localized derivation targets? |
| Baseline/comparator | Current full-block label target behavior. |
| Primary criterion | Risky-debt `prop:risky-pricing` yields one pricing equation target; `prop:interior-foc` yields two FOC targets with labels/lines/lhs/rhs. |
| Veto diagnostics | Malformed lhs/rhs; lost file/line; hidden fallback; duplicate unstable ids; target text not traceable to source. |
| Explanatory diagnostics | Number of extracted targets, fallback count, row labels. |
| Not concluded | No backend proof; no report integration yet. |
| Artifact | Extractor module/tests/result. |

## Forbidden Claims/Actions

- Do not claim extracted equations are mathematically proven.
- Do not parse arbitrary TeX beyond bounded displayed environments.
- Do not remove full-block fallback.
- Do not edit source documents.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- extracted targets have stable ids and provenance;
- fallback behavior is explicit;
- tests cover equation and align cases;
- Phase 2 subplan names route planner schema.

## Stop Conditions

Stop if:

- extraction cannot preserve line provenance;
- align row splitting is too unreliable for risky-debt labels;
- supporting changes to `latex_index` would exceed this phase.
