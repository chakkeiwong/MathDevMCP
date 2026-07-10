# Phase 06 Result: Tool-Grounded Proposal Compiler

Date: 2026-07-10

Status: `PASSED`

## Evidence Contract Result

Question: Can reports publish only evidence-grounded repairs and exact
blockers?

Result: yes for the scoped document derivation-tree workflow.  Each target now
records a `tool_grounded_proposal_compiler_result` that classifies compiled
items as publishable repair proposals or gap reports under the strict
grounding policy.  Backend-closed branches can publish repair proposals with
evidence refs.  Blocked branches publish gap reports with exact blockers and
blocked candidate edit text, not proposed edits.

## Skeptical Audit

- Wrong baseline checked: the baseline is blocked ranked-branch leakage into
  repair-like output, not complete theorem proving.
- Proxy metric checked: more compiled items is not success; the gate is
  closure status plus evidence refs plus exact blockers.
- Hidden assumption checked: agent hypotheses remain candidate evidence and do
  not enter repair proposals without tree/backend closure.
- Environment mismatch checked: backend availability remains provenance; it is
  not a proof or refutation.
- Artifact mismatch checked: the phase changed compiler output and tests, not
  only Markdown wording.

Audit result: passed.

## Implementation Summary

- Added `tool_grounded_proposal_compiler_result` to
  `src/mathdevmcp/document_derivation_tree.py`.
- Added strict validation for document-ready repair proposals and document gap
  reports.
- Preserved existing `document_ready_repair_proposals` and
  `document_gap_reports` fields for compatibility, but made the compiler
  result the machine-readable strict grounding ledger.
- Rendered compiler status, grounding policy, compiled items, evidence refs,
  and remaining blocker ids in Markdown.
- Added focused tests for backend-closed algebra and blocked risky-debt FOC
  report behavior.

## Checks Run

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 110.60s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `29 passed in 0.22s`.
- `python3 -m pytest tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `15 passed in 0.04s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_tree_report.py`:
  passed.
- `git diff --check` on touched Phase 06 files: passed.

## Non-Claims

- No claim that all document issues are found.
- No claim that gap reports are repairs.
- No claim that optional Lean/Sage/Pantograph/LeanDojo routes certify anything
  unless direct certifying evidence is present.
- No release-readiness claim.

## Handoff

Advance to Phase 07: CLI And MCP Integration.
