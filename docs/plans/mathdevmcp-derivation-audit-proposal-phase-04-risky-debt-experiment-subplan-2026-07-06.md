# Phase 4 Subplan: Risky-Debt Derivation Report Experiment

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Apply the new derivation audit/proposal report workflow to
`docs/risky-debt-maliar-deep-learning-lecture-note.tex` and inspect whether the
generated Markdown is concrete enough for another agent to use.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result is `PASSED`.
- `audit_and_propose_derivations` exists and passes focused tests.
- Phase 3 regression, compile, and diff checks pass.
- Known risky-debt labels exist under `docs/`:
  - `prop:risky-pricing`
  - `prop:interior-foc`

## Required Artifacts

- Generated report:
  `docs/reviews/risky-debt-derivation-gap-proposals.md`
- Phase 4 result record:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-result-2026-07-06.md`
- Optional focused bug-fix commits/tests only if the generated report fails a
  Phase 4 veto diagnostic.

## Required Checks, Tests, Reviews

- Generate the report with a local Python call to `audit_and_propose_derivations`.
- Inspect the generated Markdown for required fields:
  - Location
  - Problem
  - Why
  - Proposed fix
  - Derivation route
  - Backend plan
  - Validation
  - Evidence refs
  - linked assumption repairs when assumptions are missing
- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derive_from.py src/mathdevmcp/derivation_gap_proposals.py`
- `git diff --check -- docs/reviews/risky-debt-derivation-gap-proposals.md docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-result-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the new report workflow produce a useful derivation gap/proposal report for the risky-debt lecture note labels? |
| Baseline/comparator | Earlier handwavy audit/fix report and improved assumption report. |
| Primary criterion | Report contains concrete localized proposal entries for the target labels, including mathematical why, proposed fix, derivation/backend route, validation boundary, and linked assumption repairs. |
| Veto diagnostics | Location missing; proposed fix is generic or says only collect evidence; no tool-use arguments; no validation boundary; no linked assumption reasoning for missing assumptions; report claims proof closure without backend certificate. |
| Explanatory diagnostics | Target count, gap count, proposal count, validation status counts, coverage gaps. |
| Not concluded | No claim that the risky-debt note is correct; no source edits; no proof that proposed assumptions are sufficient until backend-rerun evidence exists. |
| Artifact | Generated Markdown report and Phase 4 result. |

## Forbidden Claims And Actions

- Do not edit the risky-debt LaTeX file.
- Do not claim the labels are mathematically fixed.
- Do not hide that the current label text may be too broad for full backend
  proof.
- Do not treat the assumptions route as a proof certificate.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if:

- generated report passes the required-field inspection;
- all focused tests pass after report generation;
- Phase 5 subplan states whether CLI/MCP exposure is needed and exact tests for
  public-surface parity.

## Stop Conditions

Stop if:

- the labels cannot be found under `docs/`;
- the report regresses to generic prose;
- source extraction returns text too broad for any useful deterministic gap and
  a smaller source-extraction patch is needed first.
