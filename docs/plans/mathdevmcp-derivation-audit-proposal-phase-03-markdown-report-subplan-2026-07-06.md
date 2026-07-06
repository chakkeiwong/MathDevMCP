# Phase 3 Subplan: Derivation Audit/Proposal Markdown Report

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Build a public high-level report workflow that audits direct targets or LaTeX
labels, runs the derivation gap/proposal machinery, and writes a Markdown report
that an agent can directly consume.

The report must explain:

- the location of each problem;
- what the problem is;
- why it is a mathematical derivation problem;
- what concrete proposed fix or next derivation artifact is required;
- exactly which deterministic tools were used and on what inputs.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result is `PASSED`.
- `derive_from` returns `gaps`, `proposals`, `validation`, `tool_uses`, and
  `agent_handoff`.
- Phase 2 required tests, compile checks, and diff checks pass.

## Required Artifacts

- New or updated public workflow module, likely one of:
  - `src/mathdevmcp/derivation_audit_report.py`, or
  - an extension in `src/mathdevmcp/derive_from.py` if local style favors it.
- CLI/MCP exposure only if the repository's high-level workflow pattern expects
  report workflows to be public in the same phase.
- Focused tests, likely:
  - `tests/test_derivation_audit_report.py`
  - updates to `tests/test_mcp_facade.py` and `tests/test_mcp_server.py` only if
    public MCP exposure is included.
- Phase 3 result record:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-03-markdown-report-result-2026-07-06.md`.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- If a new report test is added:
  `python3 -m pytest tests/test_derivation_audit_report.py -q`
- If CLI/MCP is exposed:
  `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py <new-or-updated-report-module>`
- `git diff --check -- <changed-source-and-test-files> docs/plans/mathdevmcp-derivation-audit-proposal-phase-03-markdown-report-result-2026-07-06.md`
- Claude read-only review only if external review approval is explicitly
  granted or public proof/refutation status semantics are changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the derivation lane produce a useful Markdown audit/proposal report for agents from direct targets or LaTeX labels? |
| Baseline/comparator | Assumption report workflow and rich `derive_from` packet. |
| Primary criterion | Markdown contains tool-use table, location, problem, mathematical why, proposed fix, derivation route/backend plan, validation boundary, evidence refs, and non-claims for each proposal. |
| Veto diagnostics | Report contains generic `collect_more_evidence`; location missing for source labels; proposed fix lacks route/backend artifact; proof/refutation claims exceed validation; source labels cannot be traced to file/line. |
| Explanatory diagnostics | Target count, gap count, proposal count, coverage gaps, validation status counts. |
| Not concluded | No automatic source edits; no proof of full document correctness; no global theorem proving; no claim that adding proposed assumptions is sufficient unless backend rerun certifies it. |
| Artifact | Report workflow, tests, Phase 3 result, generated sample report if requested. |

## Report Requirements

For every proposal, Markdown must include:

- `Location`
- `Problem`
- `Why`
- `Proposed fix`
- `Derivation route`
- `Backend plan`
- `Validation`
- `Evidence refs`

For missing assumptions, Markdown must also include linked assumption repairs:

- proposed assumption;
- mathematical missing-assumption reasoning;
- possible sufficient assumption sets;
- how the derivation works under those assumptions.

## Forbidden Claims And Actions

- Do not edit the audited document.
- Do not claim source-wide correctness from label-level checks.
- Do not claim assumption proposals prove the derivation.
- Do not hide failed or unavailable backend attempts.
- Do not emit handwavy proposals when the structured packet has named gaps.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if:

- Phase 3 report workflow passes focused tests;
- generated Markdown is readable and includes all required fields;
- the workflow records exact tool uses;
- Phase 4 subplan states whether to apply the report to
  `docs/risky-debt-maliar-deep-learning-lecture-note.tex` and what labels or
  extraction strategy will be used.

## Stop Conditions

Stop if:

- LaTeX source indexing cannot reliably map labels to file/line locations;
- report workflow requires broad public contract changes not covered by Phase
  3;
- no deterministic target extraction path exists for the selected source
  without human label selection.
