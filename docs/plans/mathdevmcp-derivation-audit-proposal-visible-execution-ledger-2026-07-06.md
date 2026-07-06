# MathDevMCP Derivation Audit/Proposal Visible Execution Ledger

Date: 2026-07-06

Status: `IN_PROGRESS`

## Program

- `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`

## Ledger

### 2026-07-06 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is the derivation audit/proposal lane planned with correct
  baselines, schema direction, gates, artifacts, and review boundaries?
- Baseline/comparator: current `derive_from`, `derive_or_refute`,
  `assumptions_for`, and assumptions report pattern.
- Primary criterion: plan artifacts exist, baseline tests pass, and review gate
  agrees or documented fallback review finds no material blocker.
- Veto diagnostics: missing stop conditions, Claude as execution authority,
  hidden detached launch, proof claims without backend evidence, missing result
  artifact path.
- Non-claims: no implementation behavior change yet; no detached launch.

Actions:

- Read Claude review guide.
- Found visible runbook template at `.md` suffixed path.
- Inspected current derivation-facing code and tests.
- Created master program, Phase 0 subplan, Phase 1 draft subplan, visible
  runbook, detached launch plan, ledger, and review bundle.

Artifacts:

- `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-subplan-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-subplan-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-gated-overnight-execution-plan-2026-07-06.md`
- `docs/reviews/mathdevmcp-derivation-audit-proposal-plan-review-bundle.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run baseline checks, diff check, and read-only review gate.

### 2026-07-06 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Is the derivation audit/proposal lane planned with correct
  baselines, schema direction, gates, artifacts, and review boundaries?
- Baseline/comparator: current `derive_from`, `derive_or_refute`,
  `assumptions_for`, and assumptions report pattern.
- Primary criterion: plan artifacts exist, baseline tests pass, and review gate
  agrees or documented fallback review finds no material blocker.
- Veto diagnostics: missing stop conditions, Claude as execution authority,
  hidden detached launch, proof claims without backend evidence, missing result
  artifact path.
- Non-claims: no implementation behavior change yet; no detached launch.

Actions:

- Ran `python3 -m pytest tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 15 passed.
- Ran `python3 -m pytest tests/test_assumptions_for.py -q`: 13 passed.
- Ran `git diff --check` over Phase 0 plan/review artifacts: passed.
- Attempted Claude review gate; approval reviewer rejected external Claude
  review-bundle export.
- Wrote local Codex fallback review with `VERDICT: AGREE`.
- Wrote Phase 0 result.

Artifacts:

- `docs/reviews/mathdevmcp-derivation-audit-proposal-plan-codex-fallback-review.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-result-2026-07-06.md`

Gate status:

- `PASSED_WITH_CODEX_FALLBACK_REVIEW`

Next action:

- Execute visible Phase 1 internal derivation gap/proposal builder.

### 2026-07-06 - Phase 1 - PRECHECK

Evidence contract:

- Question: Can low-level derivation evidence be converted into structured
  derivation gaps and proposals without inventing proof steps?
- Baseline/comparator: current `derive_from`, `derive_or_refute`, and the
  richer assumption gap/proposal builder.
- Primary criterion: stable gaps/proposals for proved, refuted,
  missing-assumption, unknown, not-encodable, and backend-unavailable cases.
- Veto diagnostics: diagnostic route becomes proof; refutation lacks concrete
  counterexample; generic `collect_more_evidence`; proposal lacks gap link or
  validation.
- Non-claims: no public workflow exposure, no source-label Markdown report, no
  general theorem proving.

Skeptical audit:

- Baseline was current low-level derivation output, not a desired future API.
- Proxy diagnostics were kept non-certifying.
- Existing high-level refutation boundary in `derive_from` was preserved.
- Commands selected directly answer the implementation and regression question.

Gate status:

- `PASSED`

### 2026-07-06 - Phase 1 - EXECUTE

Actions:

- Added `src/mathdevmcp/derivation_gap_proposals.py`.
- Added `tests/test_derivation_gap_proposals.py`.
- Reused `assumption_gap_proposals` for missing-assumption derivation repairs.
- Kept Phase 1 internal only; no CLI/MCP/public workflow exposure.

Artifacts:

- `src/mathdevmcp/derivation_gap_proposals.py`
- `tests/test_derivation_gap_proposals.py`

Gate status:

- `IMPLEMENTED`

### 2026-07-06 - Phase 1 - ASSESS_GATE

Checks:

- Ran `python3 -m pytest tests/test_derivation_gap_proposals.py -q`: 8 passed.
- Ran `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 23 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`: passed.

Artifacts:

- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-subplan-2026-07-06.md`

Gate status:

- `PASSED_PENDING_DIFF_CHECK`

Next action:

- Run Phase 1 `git diff --check`, then execute Phase 2 if clean.

### 2026-07-06 - Phase 1 - FINAL_CHECK

Checks:

- Ran `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py tests/test_derivation_gap_proposals.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-result-2026-07-06.md`: passed.

Gate status:

- `PASSED`

Next action:

- Execute Phase 2 rich `derive_from` integration.

### 2026-07-06 - Phase 2 - PRECHECK

Evidence contract:

- Question: Can `derive_from` return agent-consumable gaps/proposals while
  preserving existing proof/refutation boundaries?
- Baseline/comparator: current high-level `derive_from` envelope plus Phase 1
  internal builder packet.
- Primary criterion: attach `gaps`, `proposals`, `validation`, `tool_uses`, and
  `agent_handoff` for baseline statuses.
- Veto diagnostics: high-level validator fails; proof/refutation promotion
  boundary weakens; generic review action has no named gap/proposal.
- Non-claims: no document-wide report, no new CLI/MCP command, no proof from
  assumption proposals alone.

Skeptical audit:

- Existing `derive_from` proof/refutation promotion rules were treated as the
  baseline.
- The not-encodable branch was required to use the same rich schema.
- Free-form givens remained separate from explicit assumptions.

Gate status:

- `PASSED`

### 2026-07-06 - Phase 2 - EXECUTE

Actions:

- Updated `src/mathdevmcp/derive_from.py` to attach derivation gap/proposal
  fields.
- Updated `tests/test_derive_from.py` to assert rich output and preserved
  boundaries.

Artifacts:

- `src/mathdevmcp/derive_from.py`
- `tests/test_derive_from.py`

Gate status:

- `IMPLEMENTED`

### 2026-07-06 - Phase 2 - ASSESS_GATE

Checks:

- Ran `python3 -m pytest tests/test_derive_from.py -q`: 7 passed.
- Ran `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 24 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`: passed.

Artifacts:

- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-result-2026-07-06.md`

Gate status:

- `PASSED_PENDING_DIFF_CHECK`

Next action:

- Run Phase 2 `git diff --check`, then draft Phase 3 report-workflow subplan.

### 2026-07-06 - Phase 2 - FINAL_CHECK

Checks:

- Ran `git diff --check -- src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-02-derive-from-rich-output-result-2026-07-06.md`: passed.

Gate status:

- `PASSED`

Next action:

- Execute Phase 3 Markdown report workflow.

### 2026-07-06 - Phase 3 - PRECHECK

Evidence contract:

- Question: Can the derivation lane produce a useful Markdown audit/proposal
  report for agents from direct targets or LaTeX labels?
- Baseline/comparator: assumption report workflow and rich `derive_from`
  packet.
- Primary criterion: Markdown includes tool uses, location, problem, why,
  proposed fix, derivation route, backend plan, validation, evidence refs, and
  non-claims.
- Veto diagnostics: generic evidence collection, missing location, hidden
  backend boundary, or proof/refutation claims beyond validation.

Skeptical audit:

- Phase 3 was scoped to report workflow and tests only.
- CLI/MCP exposure was deferred to avoid broad public-surface changes.
- Label source extraction was limited to indexed label block text and
  provenance.

Gate status:

- `PASSED`

### 2026-07-06 - Phase 3 - EXECUTE

Actions:

- Added `src/mathdevmcp/derivation_audit_report.py`.
- Added `tests/test_derivation_audit_report.py`.
- Added optional `source` provenance support to `derive_from`.

Artifacts:

- `src/mathdevmcp/derivation_audit_report.py`
- `tests/test_derivation_audit_report.py`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-03-markdown-report-result-2026-07-06.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-subplan-2026-07-06.md`

Gate status:

- `IMPLEMENTED`

### 2026-07-06 - Phase 3 - ASSESS_GATE

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py -q`: 4 passed.
- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 28 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py src/mathdevmcp/derive_or_refute.py`: passed.
- Ran `git diff --check -- src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_gap_proposals.py src/mathdevmcp/derive_from.py tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-03-markdown-report-result-2026-07-06.md`: passed.

Gate status:

- `PASSED`

Next action:

- Execute Phase 4 risky-debt report experiment.

### 2026-07-06 - Phase 4 - PRECHECK

Evidence contract:

- Question: Does the new report workflow produce a useful derivation
  gap/proposal report for the risky-debt lecture note labels?
- Baseline/comparator: earlier handwavy audit/fix report and improved
  assumption report.
- Primary criterion: generated Markdown contains localized concrete proposal
  entries with mathematical why, proposed fix, derivation/backend route,
  validation boundary, and linked assumption repairs.
- Veto diagnostics: missing location, generic proposed fix, hidden tool-use
  arguments, missing validation boundary, or proof closure without certificate.

Skeptical audit:

- The experiment audits labels only and does not edit the LaTeX source.
- Full-block LaTeX targets are acceptable for this experiment if the limitation
  is recorded and no backend proof is claimed.

Gate status:

- `PASSED`

### 2026-07-06 - Phase 4 - EXECUTE

Actions:

- Generated `docs/reviews/risky-debt-derivation-gap-proposals.md` for labels
  `prop:risky-pricing` and `prop:interior-foc`.

Observed summary:

- status: `proposal_ready`
- targets: 2
- gaps: 2
- proposals: 2
- validation: `blocked_by_missing_assumptions` for both proposals
- coverage gaps: none

Artifacts:

- `docs/reviews/risky-debt-derivation-gap-proposals.md`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-result-2026-07-06.md`

Gate status:

- `IMPLEMENTED`

### 2026-07-06 - Phase 4 - ASSESS_GATE

Checks:

- Inspected generated Markdown for location, problem, why, proposed fix,
  derivation route, backend plan, validation, evidence refs, linked assumption
  repairs, possible sufficient assumption sets, and non-claims.
- Confirmed no `collect more evidence` wording.
- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 28 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derive_from.py src/mathdevmcp/derivation_gap_proposals.py`: passed.
- Ran `git diff --check -- docs/reviews/risky-debt-derivation-gap-proposals.md docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-result-2026-07-06.md`: passed.

Recorded limitation:

- Label targets are currently full LaTeX proposition blocks. The report is
  useful for deterministic missing-assumption discovery, but later backend
  proof attempts need smaller equation/proof-obligation extraction.

Gate status:

- `PASSED_WITH_RECORDED_LIMITATION`

Next action:

- Draft and execute Phase 5 CLI/MCP parity, unless deferred by user direction.

### 2026-07-06 - Phase 5 - PRECHECK

Evidence contract:

- Question: Can agents call the derivation report workflow through public
  CLI/MCP surfaces with the same structured contract as the library path?
- Baseline/comparator: existing `audit_and_propose_assumptions` CLI/MCP
  pattern.
- Primary criterion: CLI and MCP expose `audit_and_propose_derivations`, return
  `derivation_audit_report_result`, and preserve direct target/root-label
  behavior.
- Veto diagnostics: wrapper drops labels, validation boundaries, source
  locations, or tool-use arguments; wrapper changes proof/refutation semantics.

Skeptical audit:

- Public wrappers were required to delegate to the same library function.
- No public command edits source files.
- No broader CLI/MCP refactor was needed.

Gate status:

- `PASSED`

### 2026-07-06 - Phase 5 - EXECUTE

Actions:

- Added CLI command `audit-and-propose-derivations`.
- Added MCP facade tool `audit_and_propose_derivations`.
- Added FastMCP server wrapper `audit_and_propose_derivations`.
- Added public-surface tests.

Artifacts:

- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_derivation_audit_report.py`
- `tests/test_mcp_facade.py`
- `tests/test_mcp_server.py`
- `docs/plans/mathdevmcp-derivation-audit-proposal-phase-05-cli-mcp-parity-result-2026-07-06.md`

Gate status:

- `IMPLEMENTED`

### 2026-07-06 - Phase 5 - ASSESS_GATE

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`: 47 passed.
- Ran `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 24 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`: passed.
- Ran `git diff --check -- src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-05-cli-mcp-parity-result-2026-07-06.md`: passed.

Gate status:

- `PASSED`

Next action:

- Phase 6 should improve smaller equation/proof-obligation extraction for
  backend proof attempts.
