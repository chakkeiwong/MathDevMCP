# MathDevMCP Reboot Reset Memo

Date: 2026-07-10

Status: `READY_FOR_REBOOT`

## Read This First

This memo records the clean reboot state after the agent-guided,
tool-verified repair lane was completed, committed, and pushed.

The governing mission remains:

- build a conservative agent-facing math-development tool;
- make outputs directly useful to agents and colleagues;
- prefer deterministic or specialist external tools whenever possible;
- keep agent hypotheses as candidate branches, not evidence;
- never promote diagnostics, route plans, retrieval, or generated prose into
  proof without backend verification under explicit assumptions.

Read these first after reboot:

- `AGENTS.md`
- `docs/plans/mathdevmcp-mission-reset-memo.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-runbook-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md`
- `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-phase09-real-doc-comparison-2026-07-10.md`

## Repository State Before This Memo

The implementation and evidence lane was committed and pushed before this
reset memo was written.

- Branch: `main`
- Implementation commit: `a495ff3`
- Commit subject: `Implement agent-guided tool-verified repair lane`
- Remote state at closeout: `HEAD`, `origin/main`, and `origin/HEAD` pointed
  to `a495ff3`
- Working tree before this memo: clean

If this memo is committed separately, that later docs-only commit should be
treated as the reboot entry point, with `a495ff3` as the implementation base.

## What Is Now Implemented

The agent-guided, tool-verified repair lane is complete through Phase 09.

Core behavior:

- agent hypotheses can propose branches;
- derivation-tree and backend routes must verify or close a branch before it
  can become a published repair proposal;
- strict mode publishes concrete repairs only from tool/tree/backend-grounded
  evidence;
- unresolved paths produce structured gap reports instead of hand-wavy fixes;
- parallel row-level search is deterministic in result ordering and metadata;
- CLI/MCP surfaces expose the strict repair workflow.

Key implementation modules include:

- `src/mathdevmcp/document_derivation_tree.py`
- `src/mathdevmcp/agent_hypothesis_expansion.py`
- `src/mathdevmcp/derivation_tree_expansion.py`
- `src/mathdevmcp/backend_formalization_target.py`
- `src/mathdevmcp/derivation_branch_controller.py`
- `src/mathdevmcp/derivation_search_tree.py`
- `src/mathdevmcp/derivation_tree_report.py`
- `src/mathdevmcp/external_tool_adapters.py`
- `src/mathdevmcp/external_tool_policy.py`
- `src/mathdevmcp/math_document_rigor.py`
- `src/mathdevmcp/actionable_abstentions.py`
- `src/mathdevmcp/report_claim_boundary.py`

Public surfaces touched include:

- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `mcp/README.md`
- `docs/mathdevmcp-support-matrix.md`

## Evidence To Preserve

Phase/runbook evidence:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-master-program-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-runbook-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-ledger-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-stop-handoff-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-result-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md`

Real-document regression evidence:

- `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-phase09-real-doc-comparison-2026-07-10.md`

Policy and literature context:

- `AGENTS.md`
- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md`
- `docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.tex`
- `docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.pdf`
- `docs/plans/mathdevmcp-integration-version-control-note-2026-07-07.md`

## Verification Already Run

Before commit `a495ff3`, the following checks passed:

- `python3 -m compileall -q src/mathdevmcp tests`
- `git diff --check --cached`
- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`
  - result: `60 passed`
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`
  - result: `44 passed`
- `python3 -m pytest tests/test_actionable_abstentions.py tests/test_audit_math_to_code.py tests/test_backend_route_planner.py tests/test_derivation_target_extraction.py tests/test_doctor.py tests/test_external_tool_adapters.py tests/test_external_tool_policy.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_latex_index.py tests/test_lean_readiness.py tests/test_math_document_rigor.py tests/test_math_document_rigor_interfaces.py tests/test_math_ir.py tests/test_report_claim_boundary.py -q`
  - result: `116 passed, 1 skipped`

`tests/test_release_smoke.py` was not rerun as a final promotion gate for this
memo. Do not infer public release readiness from the focused checks above.

## Git Hygiene

The reboot hygiene policy from the prior closeout was:

- claim-supporting source, tests, plans, and review reports are tracked;
- local generated/downloaded material is ignored;
- all files are either tracked or gitignored.

Important ignore decision:

- `.localresources/` is ignored because it contains about 1.2G of downloaded
  papers, cloned third-party code, and local survey caches. It is useful local
  context, not a repository evidence artifact.

Generated Python and LaTeX cache patterns are also ignored through existing
`.gitignore` rules.

After reboot, run:

```bash
git status --short
git log --oneline --decorate -3
git ls-files --others --exclude-standard
```

Expected state after this memo is committed:

- `git status --short` is empty;
- `git ls-files --others --exclude-standard` is empty;
- latest commit is either the docs-only reset-memo commit or `a495ff3` if this
  memo has not been committed yet.

## Non-Claims

Do not claim:

- public release readiness;
- full-document proof for the credit-card NPV document;
- full-document proof for the risky-debt document;
- backend certification of the Phase 09 real-document reports;
- that agent hypotheses are mathematically valid unless a backend/tool route
  closed the branch;
- that Claude authorized implementation or crossing project boundaries.

The Phase 09 real-document outputs are strict regression evidence. They show
that unresolved cases become structured gap reports rather than unsupported
repair prose. In the recorded Phase 09 run, the real-document reports contained
strict gaps and no certified repairs.

## Known Risks

- Report quality is improved in contract discipline, but many hard mathematical
  targets still need stronger formalization before Lean/Sage-style tools can
  prove or refute them.
- Tool availability does not by itself certify results. Availability is
  routing evidence only.
- External review bundles are evidence artifacts, not execution authority.
- Large JSON review outputs are tracked because they support regression and
  claim boundaries, but future lanes should consider compact evidence indexes
  if report size becomes a maintenance problem.
- The implementation has focused test coverage, not a full release gate.

## Next Safe Work Packages

Good next lanes after reboot:

1. Improve formalization coverage for common document obligations so more
   branches can be closed by deterministic tools.
2. Add compact evidence indexes for large JSON reports while preserving enough
   detail to reproduce claims.
3. Strengthen backend-route contracts for Lean, Sage, SymPy, LeanSearch,
   LeanDojo/Pantograph, and fallback abstentions.
4. Expand real-document regression cases only under the strict policy:
   unresolved means gap report, not invented repair.
5. Add a release-grade smoke gate only after the focused lane remains stable.

For any next lane, begin with a skeptical plan audit and an evidence contract.
Do not start with a broad refactor.
