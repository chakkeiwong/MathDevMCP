# Phase 3 Result: Derivation Audit/Proposal Markdown Report

Date: 2026-07-06

Status: `PASSED`

## Objective

Build a public high-level report workflow that audits direct derivation targets
or LaTeX labels and writes an agent-consumable Markdown report.

## Skeptical Plan Audit

Audit result: `PASSED_WITH_BOUNDARY`.

Boundary preserved:

- The report mirrors structured `derive_from` gaps/proposals.
- No automatic source edits are applied.
- Source-label findings use indexed file/line provenance.
- Missing-assumption repairs remain non-certifying unless a backend rerun later
  certifies the scoped target.
- CLI/MCP exposure was deferred to avoid broad public-surface changes in this
  phase.

## Artifacts Created Or Changed

- `src/mathdevmcp/derivation_audit_report.py`
- `tests/test_derivation_audit_report.py`
- `src/mathdevmcp/derive_from.py`
  - added optional `source` provenance support.

## Behavior Added

New function:

- `audit_and_propose_derivations`

Supported inputs:

- direct `target`;
- LaTeX `root` plus `labels`;
- repeated `givens` and explicit `assumptions`;
- backend preference;
- optional Markdown `output_path`.

Markdown now includes:

- tool-use table with arguments;
- location;
- problem;
- mathematical why;
- proposed fix;
- derivation route;
- backend plan;
- validation;
- evidence refs;
- linked assumption repairs with missing-assumption reasoning, possible
  sufficient assumption sets, and derivation route under assumptions;
- non-claims.

## Required Checks

Passed:

- `python3 -m pytest tests/test_derivation_audit_report.py -q`
  - `4 passed`
- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
  - `28 passed`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`
  - passed

Pending until this result file is included:

- `git diff --check -- src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-03-markdown-report-result-2026-07-06.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the derivation lane produce a useful Markdown audit/proposal report for agents from direct targets or LaTeX labels? |
| Primary criterion | Passed for direct missing-assumption target, label location target, missing label coverage gap, and certifying backend target. |
| Veto diagnostics | No generic `collect_more_evidence`; source-label location appears in Markdown; proposed fixes include derivation/backend artifacts; validation boundaries are rendered. |
| Not concluded | No automatic source edits; no source-wide correctness claim; no CLI/MCP exposure; no risky-debt experiment yet. |

## Next Handoff

Phase 4 should apply the report workflow to
`docs/risky-debt-maliar-deep-learning-lecture-note.tex` using known labels
`prop:risky-pricing` and `prop:interior-foc`, write the generated Markdown under
`docs/reviews`, and inspect whether the output is sufficiently concrete for
agent use.
