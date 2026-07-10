# Phase 09 Result: Real-Document Regression And Mission Control

Date: 2026-07-10

Status: `PASSED`

## Evidence Contract Result

Question: Does the strict workflow improve honesty and usefulness on the real
card-NPV and risky-debt documents?

Result: yes for the scoped frozen regression set.  The reports are more honest
than the previous weak reports because every selected target is compiled as an
exact gap report rather than a repair proposal.  No diagnostic-only or blocked
branch is rendered as a document-ready fix.

## Real-Document Artifacts

- Card NPV Markdown:
  `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- Card NPV JSON:
  `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- Risky debt Markdown:
  `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- Risky debt JSON:
  `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- Comparison note:
  `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-phase09-real-doc-comparison-2026-07-10.md`
- Mission control update:
  `docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md`

## Result Summary

| Document | Targets | Ready repairs | Gap reports | Compiler errors | Worker failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Card NPV | 4 | 0 | 4 | 0 | 0 |
| Risky debt | 2 | 0 | 2 | 0 | 0 |

All compiled items have `publishable_as_repair=false`,
`publishable_as_gap_report=true`, non-empty evidence refs, and non-empty
remaining blocker ids.

## Skeptical Audit

- Wrong baseline checked: the baseline is weak blocked-branch report behavior,
  not whole-document proof.
- Proxy metric checked: the number of findings is not success; the gate checks
  strict classification, evidence refs, and exact blockers.
- Hidden assumption checked: no candidate hypothesis is published as a fix.
- Environment mismatch checked: backend availability is recorded through
  `doctor_report`; it is not proof.
- Artifact mismatch checked: real Markdown/JSON reports and mission-control
  policy were produced, not only tests.

Audit result: passed.

## Checks Run

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  passed, `60 passed in 247.94s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `44 passed in 0.26s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_tree_report.py`:
  passed.
- Real-report JSON assertions for strict compiler status, zero repairs,
  nonzero gap reports, evidence refs, remaining blockers, and zero compiler
  validation errors: passed.
- `git diff --check` on touched Phase 09 files: passed.

## Non-Claims

- No whole-document proof.
- No claim that the target papers are publication-ready.
- No claim that the listed assumptions are globally minimal.
- No public release-readiness claim.
- No speedup guarantee.

## Closeout

The runbook is complete through Phase 09.
