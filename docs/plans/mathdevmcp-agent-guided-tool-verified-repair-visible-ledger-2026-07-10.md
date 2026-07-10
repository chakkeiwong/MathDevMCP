# MathDevMCP Agent-Guided Tool-Verified Repair Visible Ledger

Date: 2026-07-10

Status: `COMPLETE`

## Ledger Entries

### 2026-07-10 - Phase 00 - PRECHECK

Evidence contract:

- Question: Does the lane target the real problem: agent creativity must enter
  as candidate branches, while reports publish only tree/tool-grounded
  evidence?
- Baseline/comparator: current Phase 06 context-aware repair reports.
- Primary criterion: required plan/runbook/subplan/review artifacts exist and
  encode the agent-hypothesis/tree-verification/report-compiler boundary.
- Veto diagnostics: detached execution despite visible template, Claude
  authority drift, no baseline failure lock, no stop conditions, no
  external-tool-first discipline.
- Non-claims: no implementation correctness, no improved report quality, no
  backend certification, no release readiness.

Skeptical audit:

- Wrong baseline checked: the baseline is current report leakage from blocked
  ranked branches, not a complete theorem prover.
- Proxy metric checked: branch counts, hypothesis counts, and backend attempt
  counts are not promotion criteria.
- Stop conditions checked: Phase 00 requires no installs, network fetches,
  backend mutations, detached launches, or destructive actions.
- Hidden assumptions checked: agent hypotheses must record assumptions
  explicitly and cannot be published without tree/tool validation.
- Artifact mismatch checked: Phase 00 produces governance artifacts only;
  implementation starts in Phase 01 after review.

Actions:

- Draft master program, phase subplans, visible runbook, ledger, stop handoff,
  and compact review bundle.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-master-program-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-runbook-2026-07-10.md`
- `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-plan-review-bundle-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 01 strict contracts and regression gates.

### 2026-07-10 - Phase 00 - ASSESS_GATE

Actions:

- Ran local artifact section scan over phase subplans.
- Ran boundary scan for Claude authority, detached execution, diagnostic proof
  promotion, raw agent text, and blocked-branch repair rendering.
- Ran `git diff --check` on the new plan and review artifacts.
- Attempted Claude read-only review gate.  The escalation reviewer rejected the
  call because exporting local plan artifacts to the external Claude service
  was considered a data-transfer risk.
- Used the planned safer fallback: fresh local Codex read-only review of the
  bounded plan artifacts.

Review trail:

- Claude review gate: `blocked_by_policy`; no Claude verdict claimed.
- Fresh Codex fallback reviewer: `VERDICT: AGREE`; no material findings.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Start Phase 01.

### 2026-07-10 - Phase 01 - ASSESS_GATE

Evidence contract:

- Question: Can contracts prevent raw agent hypotheses and diagnostic-only
  branches from becoming repair proposals?
- Baseline/comparator: current top-ranked-branch proposal generation.
- Primary criterion: blocked branches render as gap reports, while
  backend-closed paths can still render as repair proposals.
- Veto diagnostics: raw agent text emitted as fix; diagnostic evidence
  promoted; blocked path rendered as repair.
- Non-claims: no recursive search or real-document quality claim.

Actions:

- Added strict proposal/gap classification to
  `src/mathdevmcp/document_derivation_tree.py`.
- Added `document_gap_report` output for blocked branches.
- Preserved `context_aware_executable_repair_proposal` only for closed or
  partially backend-closed paths.
- Updated focused tests for blocked NPV/FOC and simple algebra.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 109.90s`.
- `python3 -m pytest tests/test_derivation_tree_report.py tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `29 passed in 0.20s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py`:
  passed.
- `git diff --check` on touched Phase 01 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 02 agent hypothesis expansion interface.

### 2026-07-10 - Phase 02 - ASSESS_GATE

Evidence contract:

- Question: Can agent-generated mathematical ideas be admitted only as
  structured, non-certifying candidate branches?
- Baseline/comparator: deterministic branch templates with no explicit
  agent-hypothesis schema.
- Primary criterion: candidate expansions preserve blocker id, assumptions,
  route, backend expectation, success criterion, failure criterion, and
  non-proof boundary.
- Veto diagnostics: vague hypothesis, missing blocker id, implicit assumptions,
  absent backend route, raw agent text entering report.
- Non-claims: hypotheses are not repairs, proofs, or backend certificates.

Actions:

- Added `agent_hypothesis_expansion` and `agent_hypothesis_expansion_set`
  contracts.
- Added deterministic seed expansion routes for conditional-law,
  integrability, macro-translation, and generic formalization blockers.
- Attached expansion sets to blocked document-tree branches.
- Added branch expansion records with kind `agent_hypothesis_candidate`.

Checks:

- `python3 -m pytest tests/test_agent_hypothesis_expansion.py -q`: passed,
  `4 passed in 0.02s`.
- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 114.12s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `29 passed in 0.24s`.
- `python3 -m py_compile src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py`:
  passed.
- `git diff --check` on touched Phase 02 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 03 recursive derivation tree search.

### 2026-07-10 - Phase 03 - ASSESS_GATE

Evidence contract:

- Question: Can exact blockers be recursively expanded into child search nodes
  without proof overclaims?
- Baseline/comparator: one-shot branch controller and static branch ranking.
- Primary criterion: validated hypotheses create child nodes with parent
  blocker provenance and explicit budget status.
- Veto diagnostics: duplicate/infinite expansion, lost provenance, hidden
  budget exhaustion, diagnostic promotion.
- Non-claims: no MCTS optimality, completeness, backend proof, or repair
  proposal.

Actions:

- Added `derivation_tree_expansion_result` and
  `expand_tree_with_hypotheses`.
- Added bounded child-node expansion from validated hypothesis candidates.
- Integrated recursive expansion summary into document derivation tree output.

Checks:

- `python3 -m pytest tests/test_derivation_tree_expansion.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `32 passed in 0.20s`.
- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 120.12s`.
- `python3 -m py_compile src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/document_derivation_tree.py`:
  passed.
- `git diff --check` on touched Phase 03 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 04 backend formalization targets.

### 2026-07-10 - Phase 04 - ASSESS_GATE

Evidence contract:

- Question: Can each candidate path become a runnable backend target or an
  exact formalization blocker?
- Baseline/comparator: branch-level backend attempts and formalization stubs.
- Primary criterion: expanded child nodes carry backend formalization targets.
- Veto diagnostics: search traces as proof, Lean `sorry` certifying, backend
  unavailable as refutation, assumptions omitted from targets.
- Non-claims: no full-document proof or backend completeness claim.

Actions:

- Added `backend_formalization_target` contract and builder.
- Classified SymPy/Sage/Lean/search/manual routes as backend-ready, skeleton
  only, diagnostic-only, or blocked-not-encodable.
- Attached backend formalization targets to expanded child nodes.

Checks:

- `python3 -m pytest tests/test_backend_formalization_target.py tests/test_derivation_tree_expansion.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py -q`:
  passed, `28 passed in 0.21s`.
- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 120.57s`.
- `python3 -m py_compile src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/document_derivation_tree.py`:
  passed.
- `git diff --check` on touched Phase 04 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 05 expansion rule library.

### 2026-07-10 - Phase 05 - ASSESS_GATE

Evidence contract:

- Question: Can common blockers generate concrete candidate paths rather than
  generic "collect more evidence" text?
- Baseline/comparator: current typed translation blockers and static
  sufficient assumption branches.
- Primary criterion: supported blockers yield candidate assumptions,
  derivation route, backend target or exact blocker, and evidence refs.
- Veto diagnostics: generic handwavy expansion; assumptions not explicit; no
  backend route; no source-local symbols; claim of minimal assumptions.
- Non-claims: no claim that generated branches are necessary or globally
  minimal.

Actions:

- Extended the agent-hypothesis expansion rule library for conditioning scope,
  derivative-under-expectation interchange, transition-law independence,
  domain/shape declarations, multiline grouping, full-display recovery, and
  finite-horizon accounting/valuation conditions.
- Added focused rule-library tests and preserved the non-proof candidate
  boundary.

Checks:

- `python3 -m pytest tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `15 passed in 0.04s`.
- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 111.20s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `29 passed in 0.22s`.
- `python3 -m py_compile src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py`:
  passed.
- `git diff --check` on touched Phase 05 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 06 tool-grounded proposal compiler.

### 2026-07-10 - Phase 06 - ASSESS_GATE

Evidence contract:

- Question: Can reports publish only evidence-grounded repairs and exact
  blockers?
- Baseline/comparator: current document-ready proposal section generated from
  ranked branch evidence.
- Primary criterion: closed/partial paths render as proposals with evidence;
  blocked paths render as gap reports; no raw agent hypothesis text becomes a
  fix.
- Veto diagnostics: blocked path rendered as repair; missing
  location/problem/why/fix/evidence; diagnostic status presented as proof; no
  remaining blockers for partial path.
- Non-claims: no claim that all document issues are found.

Actions:

- Added `tool_grounded_proposal_compiler_result` to the document derivation
  tree workflow.
- Added strict validation for repair proposals and gap reports.
- Made the compiler the machine-readable strict grounding ledger while
  preserving existing proposal/gap arrays.
- Rendered compiler decisions, evidence refs, and remaining blockers in
  Markdown.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `13 passed in 110.60s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `29 passed in 0.22s`.
- `python3 -m pytest tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `15 passed in 0.04s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/backend_formalization_target.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_tree_report.py`:
  passed.
- `git diff --check` on touched Phase 06 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 07 CLI and MCP integration.

### 2026-07-10 - Phase 07 - ASSESS_GATE

Evidence contract:

- Question: Can agents call the strict workflow directly and receive
  machine-readable evidence reports?
- Baseline/comparator: current `audit_document_derivation_tree` CLI/MCP
  exposure.
- Primary criterion: CLI and MCP produce equivalent strict-grounding
  JSON/Markdown artifacts with explicit tool-use ledger.
- Veto diagnostics: MCP omits strict fields; CLI and MCP disagree; defaults
  silently weaken evidence policy; no tool-use ledger.
- Non-claims: no public release or full backward compatibility claim beyond
  tests.

Actions:

- Added `search_mode="agent_guided"` and `grounding_policy="strict"` to the
  library function, CLI, MCP facade, and FastMCP server.
- Rejected unsupported policy values in the shared library path.
- Updated support matrix and MCP README for the strict document derivation-tree
  workflow.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  passed, `59 passed in 236.36s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`:
  passed.
- `git diff --check` on touched Phase 07 files: passed.

Broad-suite caveat:

- `python3 -m pytest tests/test_mcp_surface_sync.py tests/test_release_smoke.py -q`
  failed because the public release hypothesis check reports dirty-worktree and
  public-release blockers.  This is outside the Phase 07 scoped workflow
  contract.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-result-2026-07-10.md`

Gate status:

- `PASSED_WITH_RECORDED_BROAD_SUITE_CAVEAT`

Next action:

- Begin Phase 08 parallel search discipline.

### 2026-07-10 - Phase 08 - ASSESS_GATE

Evidence contract:

- Question: Can independent branches be tested faster without changing logical
  results or hiding failures?
- Baseline/comparator: serial strict workflow from Phase 07.
- Primary criterion: serial and parallel runs agree on logical statuses;
  timeouts/errors become exact blockers; output order remains deterministic.
- Veto diagnostics: nondeterministic report order; lost backend errors;
  timeout treated as refutation; parallel run changes closure status.
- Non-claims: no speedup guarantee or benchmark claim.

Actions:

- Added optional `workers` execution to the document derivation-tree workflow,
  CLI, MCP facade, and FastMCP server.
- Kept serial execution as the default.
- Sorted parallel target results back to source order.
- Converted worker exceptions into target-level blockers and strict compiler
  validation errors.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed,
  `14 passed in 129.77s`.
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  passed, `46 passed in 126.17s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_backend_formalization_target.py -q`:
  passed, `44 passed in 0.22s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`:
  passed.
- `git diff --check` on touched Phase 08 files: passed.

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-result-2026-07-10.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 09 real-document regression and mission-control closeout.

### 2026-07-10 - Phase 09 - ASSESS_GATE

Evidence contract:

- Question: Does the strict workflow improve honesty and usefulness on the real
  card-NPV and risky-debt documents?
- Baseline/comparator: Phase 06 frozen reports and the known weakness where
  blocked branches could look like repairs.
- Primary criterion: Reports separate closed repairs, partial repairs,
  refutations, and blocked gap reports; no diagnostic-only branch is rendered
  as a fix.
- Veto diagnostics: same handwavy proposal regression; missing exact blocker;
  no tool-use ledger; unsupported improvement claim; final policy omits
  agent/tree/backend role split.
- Non-claims: no document is claimed publication-ready or fully verified.

Actions:

- Generated frozen strict card-NPV and risky-debt reports under `docs/reviews`.
- Wrote a real-document comparison note.
- Updated external-tool-first tree derivation mission control with the
  agent-hypothesis, strict compiler, and optional parallelism invariants.

Checks:

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

Artifacts:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md`
- `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-phase09-real-doc-comparison-2026-07-10.md`
- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-mission-control-2026-07-08.md`

Gate status:

- `PASSED`

Next action:

- Runbook complete.
