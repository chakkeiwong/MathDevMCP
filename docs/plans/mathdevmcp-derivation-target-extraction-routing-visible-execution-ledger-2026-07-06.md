# MathDevMCP Derivation Target Extraction Visible Execution Ledger

Date: 2026-07-06

Status: `IN_PROGRESS`

## Program

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-master-program-2026-07-06.md`

## Ledger

### 2026-07-06 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is the target extraction/routing program planned with correct
  gates, evidence contracts, artifacts, and boundaries?
- Baseline/comparator: prior derivation audit/proposal program and current
  risky-debt report limitation.
- Primary criterion: plan artifacts exist, baseline checks pass, and review
  gate agrees or fallback review records no material blocker.
- Veto diagnostics: missing stop conditions, Claude as executor, no repair
  loop, detached launch without approval, or checks that do not answer the
  phase question.
- Non-claims: no implementation behavior change in Phase 0.

Skeptical audit:

- Baseline is current full-block report behavior, not future extraction.
- Target count is explanatory, not a promotion criterion.
- Stop conditions are phase-local and program-wide.
- Claude is reviewer only.

Gate status:

- `IN_PROGRESS`

Next action:

- Run baseline checks, create review bundle, and request Claude review gate.

### 2026-07-06 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Is the target extraction/routing program planned with correct
  gates, evidence contracts, artifacts, and boundaries?
- Baseline/comparator: prior derivation audit/proposal program and current
  risky-debt report limitation.
- Primary criterion: plan artifacts exist, baseline checks pass, and review
  gate agrees or fallback review records no material blocker.
- Veto diagnostics: missing stop conditions, Claude as executor, no repair
  loop, detached launch without approval, or checks that do not answer the
  phase question.
- Non-claims: no implementation behavior change in Phase 0.

Actions:

- Created master program, phase subplans 0-6, visible runbook, overnight plan,
  ledger, and review bundle.
- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`: 29 passed.
- Ran `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`: 42 passed.
- Ran `git diff --check` over Phase 0 plan/review artifacts: passed.
- Attempted Claude review gate. Approval reviewer rejected external Claude data
  export. No workaround attempted.
- Wrote Codex fallback review with `VERDICT: AGREE`.
- Wrote Phase 0 result.

Artifacts:

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-00-plan-review-result-2026-07-06.md`
- `docs/reviews/mathdevmcp-derivation-target-extraction-routing-plan-codex-fallback-review.md`

Gate status:

- `PASSED_WITH_CODEX_FALLBACK_REVIEW`

Next action:

- Execute Phase 1 target extraction.

### 2026-07-06 - Phase 1 - PRECHECK

Evidence contract:

- Question: Can label blocks be converted into smaller source-localized
  derivation targets?
- Baseline/comparator: current full-block label target behavior.
- Primary criterion: risky-debt `prop:risky-pricing` yields one pricing
  equation target; `prop:interior-foc` yields two FOC targets with
  labels/lines/lhs/rhs.
- Veto diagnostics: malformed lhs/rhs, lost file/line provenance, hidden
  fallback, duplicate unstable ids, or target text not traceable to source.
- Non-claims: no backend proof and no report integration in Phase 1.

Skeptical audit:

- Baseline is full-block label auditing, not proof of extracted math.
- Target count is explanatory; source provenance and explicit fallback are the
  real gate.
- Existing `equation_locator` already provides row localization, so Phase 1 can
  remain a deterministic adapter instead of a new parser.
- The risky-debt source document is read-only for this phase.

Gate status:

- `PASSED`

Next action:

- Implement the target extraction adapter and focused tests.

### 2026-07-06 - Phase 1 - ASSESS_GATE

Actions:

- Added `src/mathdevmcp/derivation_target_extraction.py`.
- Added `tests/test_derivation_target_extraction.py`.
- Reused `locate_equations_in_text` for row localization.
- Added explicit `fallback_full_block` behavior.
- Preserved `source_text`, `target`, `lhs`, `rhs`, equation label, parent
  label, parent block id, file, line span, environment, row index, localization
  status, uncertainty, and section path.

Checks:

- Ran `python3 -m pytest tests/test_derivation_target_extraction.py -q`: 4
  passed.
- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derive_from.py -q`:
  12 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_target_extraction.py`:
  passed.

Artifacts:

- `src/mathdevmcp/derivation_target_extraction.py`
- `tests/test_derivation_target_extraction.py`
- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-01-target-extraction-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 1 diff hygiene, then proceed to Phase 2 backend route planner.

### 2026-07-06 - Phase 2 - PRECHECK

Evidence contract:

- Question: Can route planning prefer deterministic backends while preserving
  non-certifying boundaries?
- Baseline/comparator: current implicit router inside `derive_or_refute`.
- Primary criterion: planner emits route candidates for symbolic,
  counterexample, matrix/domain, Lean/formalization, and unavailable-backend
  cases without proof promotion.
- Veto diagnostics: route candidate marked proof without backend certificate,
  backend absence treated as refutation, missing formalization path, or no
  tool-use record.
- Non-claims: no route execution and no general theorem proving.

Skeptical audit:

- Route availability is diagnostic only and cannot become proof.
- Lean/Sage absence must be recorded as unavailable, not as mathematical
  evidence.
- Tests must inject capabilities so results are not environment-dependent.
- Existing `derive_or_refute` remains the actual proof/refutation boundary.

Gate status:

- `PASSED`

Next action:

- Implement non-certifying backend route planner and tests.

### 2026-07-06 - Phase 2 - ASSESS_GATE

Actions:

- Added `src/mathdevmcp/backend_route_planner.py`.
- Added `tests/test_backend_route_planner.py`.
- Added route candidates for SymPy, bounded counterexample search, Sage, and
  Lean.
- Attached each candidate to a tool, evidence contract, expected artifact, and
  non-certifying boundary.
- Repaired matrix/domain detection after the first focused test showed that
  `A*B = B*A` would otherwise be selected for scalar SymPy.

Checks:

- Ran `python3 -m pytest tests/test_backend_route_planner.py -q`: first run
  found the scalar route bug; after repair, 4 passed.
- Ran `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_derive_or_refute.py -q`:
  13 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/backend_route_planner.py src/mathdevmcp/derive_or_refute.py`:
  passed.

Artifacts:

- `src/mathdevmcp/backend_route_planner.py`
- `tests/test_backend_route_planner.py`
- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-02-backend-route-planner-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 2 diff hygiene, then proceed to Phase 3 report integration.

### 2026-07-06 - Phase 3 - PRECHECK

Evidence contract:

- Question: Can reports use extracted obligations instead of full blocks while
  preserving existing report usefulness?
- Baseline/comparator: current risky-debt report with two full-block targets.
- Primary criterion: label report records extracted target count and
  target-level proposals with parent label, equation label, line, lhs/rhs,
  route plan, validation, and assumption repairs.
- Veto diagnostics: missing old report fields, confusing target grouping,
  hidden route plan, less concrete report, or generic proposal text.
- Non-claims: no proof of risky-debt note and no source edits.

Skeptical audit:

- Route plans must be visible but non-certifying.
- Direct target path must keep working.
- Text-only label fallback must remain explicit, not disappear.
- Existing validation and assumption repair fields must remain in markdown.

Gate status:

- `PASSED`

Next action:

- Integrate extraction and route plans into the report workflow.

### 2026-07-06 - Phase 3 - ASSESS_GATE

Actions:

- Updated `src/mathdevmcp/derivation_audit_report.py` to extract label targets,
  plan backend routes, and run `derive_from` per extracted obligation.
- Updated markdown to include extracted targets and backend route plans.
- Updated `src/mathdevmcp/derivation_gap_proposals.py` location rendering so
  extracted equation gaps can show parent proposition label and equation label.
- Updated `tests/test_derivation_audit_report.py`.

Repair:

- First report test run found that extracted equation locations omitted the
  parent label. Patched the shared location helper to render
  `parent_label > equation_label > line` only when those labels differ.

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py -q`: first run
  found the location issue; after repair, 6 passed.
- Ran `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`:
  8 passed.
- Ran `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`:
  24 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/backend_route_planner.py src/mathdevmcp/derivation_gap_proposals.py`:
  passed.

Artifacts:

- `src/mathdevmcp/derivation_audit_report.py`
- `src/mathdevmcp/derivation_gap_proposals.py`
- `tests/test_derivation_audit_report.py`
- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-03-report-integration-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 3 diff hygiene, then proceed to Phase 4 risky-debt v2 experiment.

### 2026-07-06 - Phase 4 - PRECHECK

Evidence contract:

- Question: Does extracted-obligation reporting improve risky-debt derivation
  audit usefulness?
- Baseline/comparator:
  `docs/reviews/risky-debt-derivation-gap-proposals.md` full-block report.
- Primary criterion: v2 report separates pricing and FOC obligations with
  target-level provenance and no loss of assumption repair details.
- Veto diagnostics: missing locations, lost assumption repairs, hidden backend
  plan, or generic wording.
- Non-claims: no proof of the note, no applied edits, no scientific validation.

Skeptical audit:

- Report length is not a success criterion.
- The artifact must show `eq:risky-pricing`, `eq:foc-k`, and `eq:foc-b`.
- Route plans must remain diagnostic and cannot imply proof.
- Risky-debt LaTeX source remains read-only.

Gate status:

- `PASSED`

Next action:

- Generate and inspect the v2 risky-debt report.

### 2026-07-06 - Phase 4 - ASSESS_GATE

Actions:

- Generated `docs/reviews/risky-debt-derivation-gap-proposals-v2.md` through
  the CLI.
- Inspected the Markdown artifact for extracted targets, target-level
  locations, route plans, assumption repairs, and non-certifying boundaries.
- Tightened route planning after inspection showed LaTeX-heavy risky-debt
  counterexample/Sage candidates were too optimistic; regenerated the report.

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`:
  14 passed.
- Ran marker inspection with `rg`; required v2 markers were found.

Artifacts:

- `docs/reviews/risky-debt-derivation-gap-proposals-v2.md`
- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-04-risky-debt-v2-experiment-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 4 diff hygiene, then proceed to Phase 5 public-surface regression.

### 2026-07-06 - Phase 5 - PRECHECK

Evidence contract:

- Question: Do public surfaces preserve improved extracted-obligation
  reporting?
- Baseline/comparator: prior `audit_and_propose_derivations` public surface.
- Primary criterion: CLI/MCP tests pass and assert output contract plus
  extracted target coverage.
- Veto diagnostics: public output drops extracted targets, validation,
  locations, or tool uses.
- Non-claims: no release readiness or scientific correctness.

Skeptical audit:

- Public wrappers should not be broadened unless tests show a gap.
- Existing contract name should remain stable.
- Additive report fields should be asserted through MCP facade if available.

Gate status:

- `PASSED`

Next action:

- Run public-surface regression and patch tests/wrappers only if needed.

### 2026-07-06 - Phase 5 - ASSESS_GATE

Actions:

- Confirmed CLI/MCP wrappers already forward root/labels/output and did not
  require implementation changes.
- Updated `tests/test_mcp_facade.py` so direct reports expect
  `plan_backend_routes` in tool uses.
- Added an MCP facade label-path regression for extracted target coverage and
  route-plan boundary.

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  49 passed.
- Ran `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`:
  8 passed.
- Ran `python3 -m compileall -q src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`:
  passed.

Artifacts:

- `tests/test_mcp_facade.py`
- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-05-public-surface-regression-result-2026-07-06.md`

Gate status:

- `PASSED`

Next action:

- Run Phase 5 diff hygiene, then proceed to Phase 6 final review/handoff.

### 2026-07-06 - Phase 6 - PRECHECK

Evidence contract:

- Question: Is the extraction/routing lane ready for handoff with accurate
  claims and artifacts?
- Baseline/comparator: master program objectives and all phase result
  artifacts.
- Primary criterion: tests/diff pass, final claims match evidence, and residual
  limitations are explicit.
- Veto diagnostics: unsupported scientific claim, missing result artifact,
  failed public-surface test, or unrecorded review blocker.
- Non-claims: no source edits, no proof of risky-debt note, no release
  readiness.

Skeptical audit:

- Final result must not imply proof or source repair.
- Claude final review cannot be claimed because the Phase 0 review export was
  rejected.
- Worktree has prior-lane dirty/untracked files and must not be cleaned or
  reverted.

Gate status:

- `PASSED`

Next action:

- Run final focused checks and write final handoff artifacts.

### 2026-07-06 - Phase 6 - ASSESS_GATE

Actions:

- Ran final focused derivation/extraction regressions.
- Ran final public MCP regressions.
- Ran full `git diff --check`.
- Wrote Codex fallback final review.
- Updated `docs/plans/mathdevmcp-mission-reset-memo.md`.
- Wrote Phase 6 result.

Checks:

- Ran `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`:
  38 passed.
- Ran `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  43 passed.
- Ran `git diff --check`: passed.

Artifacts:

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-06-final-review-handoff-result-2026-07-06.md`
- `docs/reviews/mathdevmcp-derivation-target-extraction-routing-final-codex-fallback-review.md`
- `docs/plans/mathdevmcp-mission-reset-memo.md`

Gate status:

- `PASSED_WITH_CODEX_FALLBACK_REVIEW`

Program status:

- `COMPLETE`
