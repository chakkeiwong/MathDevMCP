# MathDevMCP Context-Aware Executable Repair Visible Ledger

Date: 2026-07-08

Status: `IN_PROGRESS`

## Ledger Entries

### 2026-07-08 - Phase 00 - PRECHECK

Evidence contract:

- Question: Does the program target context-aware executable repair proposals?
- Baseline/comparator: current Phase 04 display-equation reports.
- Primary criterion: plan requires proposition/context packets, context graph,
  typed IR, executable/blocker backend attempts, branch search, and
  document-ready regression reports.
- Veto diagnostics: no frozen targets, no external-tool-first discipline,
  detached execution despite visible template, Claude authority drift.
- Non-claims: no implementation correctness or report quality claim yet.

Skeptical audit:

- Wrong baseline checked: current improved report is the baseline, not an ideal
  theorem prover.
- Proxy metric checked: branch/stub counts are not pass criteria.
- Stop conditions checked: no installs, detached launches, or proof-boundary
  weakening.
- Hidden assumptions checked: surrounding context may already state some
  assumptions and must be represented explicitly.
- Artifact mismatch checked: each implementation phase must add code/tests or
  frozen reports.

Actions:

- Drafted master program, phase subplans, visible runbook, ledger, stop
  handoff, and review bundle.

Gate status:

- `PASSED`

Next action:

- Begin Phase 01 proposition/context packet extraction.

### 2026-07-09 - Phase 02 - PRECHECK

Evidence contract:

- Question: Can the workflow avoid proposing assumptions that are already
  stated nearby?
- Baseline/comparator: current document-tree reports that list route-required
  assumptions without a local source-evidence graph.
- Primary criterion: `prop:interior-foc` marks at least one proposition-stated
  assumption as `stated` and at least one route-required expectation/interchange
  condition as `missing` or `unresolved`.
- Veto diagnostics: all assumptions marked missing; all assumptions marked
  stated without source references; no source references; graph text treated as
  proof.
- Non-claims: context graph statuses are deterministic diagnostics only, not
  proof certificates, not sufficiency claims, and not global minimality claims.

Skeptical audit:

- Wrong baseline checked: compare against the missing/stated distinction absent
  from current reports, not against a full theorem prover.
- Proxy metric checked: graph node counts are not pass criteria; tests must
  assert specific statuses and evidence refs on the frozen FOC proposition.
- Stop conditions checked: no package installation, network fetch, detached
  execution, destructive action, or proof-boundary weakening is needed.
- Hidden assumptions checked: proposition hypotheses may state interiority and
  differentiability, but expectation law, integrability, and interchange still
  need explicit evidence and must not be silently inferred.
- Artifact mismatch checked: implementation must add structured graph fields,
  Markdown display, tests, and a Phase 02 close record.

Actions:

- Begin scoped implementation in `src/mathdevmcp/document_derivation_tree.py`
  and focused regression tests.

Gate status:

- `IN_PROGRESS`

### 2026-07-09 - Phase 06 - ASSESS_GATE

Evidence contract:

- Question: Does the final high-level report produce good repair proposals for
  frozen targets?
- Primary criterion: reports include proposition/context handling, local
  context, typed assumptions, executable attempts or precise blockers, ranked
  branches, and branch-derived document-ready repair text.
- Veto diagnostics: template-only proposal, proof overclaim, missing frozen
  target, absent backend attempt/blocker, absent non-claims.

Actions:

- Added `context_aware_executable_repair_proposal` records to compact document
  derivation trees.
- Rendered `Document-ready repair proposals` before the low-level branch dump.
- Included proposed LaTeX, missing/stated assumption status, branch route,
  backend evidence, remaining blockers, validation, and non-claims.
- Fixed `\middle|` conditioning-object parsing so it does not corrupt
  conditioning information in credit-card NPV reports.
- Generated frozen Phase 06 risky-debt and credit-card NPV reports.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`:
  passed, `21 passed in 116.57s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_document_derivation_tree.py -q`:
  passed, `34 passed in 133.34s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`:
  passed.
- Frozen report content assertions:
  passed. Both reports contain proposal contract, top-branch linkage, problem,
  why, proposed assumptions, proposed LaTeX, blockers, and non-claims.
- `git diff --check`:
  passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-result-2026-07-08.md`
- `docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.md`
- `docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.json`
- `docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.md`
- `docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.json`

Gate status:

- `PASSED`

Review trail:

- Claude review remained unavailable under the Phase 00 external-service
  rejection boundary.
- Codex performed a local read-only skeptical review against the Phase 06
  evidence contract; no veto issue remained.

Next action:

- Close the context-aware executable repair visible runbook.

### 2026-07-09 - Phase 04 - ASSESS_GATE

Evidence contract:

- Question: Can branches show actual executable attempts or exact typed
  translation blockers?
- Primary criterion: encodable algebraic branch exposes scoped executable
  evidence; hard stochastic branches expose exact typed blockers and do not
  promote diagnostic evidence.
- Veto diagnostics: stubs as proof, backend absence as refutation, hidden
  root-only branch evidence, unbounded backend command, missing artifacts.

Actions:

- Added branch-level `backend_attempts`, `translation_attempts`,
  `translation_blockers`, `backend_evidence`, and local blockers.
- Rendered branch backend attempts and blockers in Markdown.
- Generated risky-debt and simple algebra Phase 04 frozen smoke artifacts.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_external_tool_adapters.py tests/test_derive_or_refute.py -q`:
  passed, `31 passed in 107.62s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/external_tool_adapters.py`:
  passed.
- Frozen smoke JSON assertion:
  passed. Risky-debt branch is blocked with exact typed blockers; simple algebra
  branch has scoped SymPy proof evidence.
- `git diff --check`:
  passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-result-2026-07-08.md`
- `docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.md`
- `docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.json`
- `docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.md`
- `docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.json`

Gate status:

- `PASSED`

Review trail:

- Claude review remained unavailable under the Phase 00 external-service
  rejection boundary.
- Codex performed a local read-only skeptical review against the Phase 04
  evidence contract; no veto issue remained.

Next action:

- Begin Phase 05 budgeted repair branch search.

### 2026-07-09 - Phase 05 - ASSESS_GATE

Evidence contract:

- Question: Can the tool rank repair branches by evidence rather than listing
  templates?
- Primary criterion: report can say which branch is best supported, which branch
  is blocked, and what concrete evidence or blocker drives the ranking.
- Veto diagnostics: ranking based on raw branch count, unsupported branch
  promotion, hidden budget exhaustion, proof/minimality overclaim.

Actions:

- Added `rank_repair_branches` and `branch_expansion_records` in
  `src/mathdevmcp/derivation_branch_controller.py`.
- Attached branch expansion records and `repair_branch_ranking_result` to
  document derivation trees.
- Rendered branch ranking and expansion records in Markdown.
- Generated frozen Phase 05 risky-debt and simple-algebra smoke artifacts.

Checks:

- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_document_derivation_tree.py -q`:
  passed, `32 passed in 101.68s`.
- `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/document_derivation_tree.py`:
  passed.
- Frozen smoke JSON assertion:
  passed. Risky-debt has six ranked branches with blocked-specific-evidence
  outcomes; simple algebra has one top branch with `scoped_proved` outcome.
- `git diff --check`:
  passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-result-2026-07-08.md`
- `docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.md`
- `docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.json`
- `docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.md`
- `docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.json`

Gate status:

- `PASSED`

Review trail:

- Claude review remained unavailable under the Phase 00 external-service
  rejection boundary.
- Codex performed a local read-only skeptical review against the Phase 05
  evidence contract; no veto issue remained.

Next action:

- Begin Phase 06 document-ready repair report regression.

### 2026-07-09 - Phase 06 - PRECHECK

Evidence contract:

- Question: Does the final high-level report produce good repair proposals for
  frozen targets?
- Baseline/comparator: Phase 04/05 frozen display-equation reports.
- Primary criterion: proposition targets are handled; local context is used;
  assumptions are stated or missing with evidence; executable attempts or typed
  blockers are shown; repair text is document-ready and branch-derived.
- Veto diagnostics: template-only proposal, proof overclaim, missing frozen
  target, no backend attempt/blocker, no non-claims.
- Non-claims: no whole-document proof, release readiness, global optimality, or
  global minimality.

Skeptical audit:

- Wrong baseline checked: compare against prior frozen reports, not against an
  ideal theorem prover.
- Proxy metric checked: ranked branch count is not enough; the report must give
  location, problem, why, proposed assumptions/fix text, derivation route, and
  required backend/formalization evidence.
- Hidden assumption checked: branch ranking remains diagnostic and must not be
  treated as proof or minimality.
- Environment mismatch checked: no package install, network fetch, detached
  execution, destructive action, or proof-boundary weakening is needed.
- Material flaw found before execution: the current Markdown exposes branch
  evidence but buries the actionable repair in long patch prose. The older
  credit-card frozen report also shows a generic parser regression where
  `\middle|` can be partially interpreted as `\mid`, producing a malformed
  conditioning object.

Revised execution slice:

- Add a structured document-ready repair proposal contract derived from the
  top-ranked branch for each target.
- Render a concise repair-proposal section with location, problem, why,
  proposed edit text, branch route, blockers, backend evidence, validation, and
  non-claims.
- Fix conditional-bar parsing so `\middle|` is preferred over `\mid`.
- Run Phase 06 tests and frozen risky-debt/credit-card regressions.

Gate status:

- `IN_PROGRESS`

### 2026-07-09 - Phase 03 - ASSESS_GATE

Evidence contract:

- Question: Can each branch be generated from a typed obligation rather than
  raw LaTeX templates?
- Primary criterion: branches cite typed obligation ids with unresolved
  constructs and backend route hints.
- Veto diagnostics: branch without typed obligation, hidden stochastic or
  derivative blockers, proof overclaim, source provenance dropped.

Actions:

- Added `typed_repair_obligation_from_packet` in `src/mathdevmcp/math_ir.py`.
- Reused existing typed math obligation diagnostics.
- Attached typed repair obligations to proposition/context packets, semantic
  packets, compact trees, branches, coverage, tool-use ledger, and Markdown.
- Added focused tests for typed repair obligation construction and branch
  citation.
- Generated frozen Phase 03 risky-debt typed-IR smoke artifacts.

Checks:

- `python3 -m pytest tests/test_math_ir.py tests/test_document_derivation_tree.py -q`:
  passed, `18 passed in 79.06s`.
- `python3 -m py_compile src/mathdevmcp/math_ir.py src/mathdevmcp/document_derivation_tree.py`:
  passed.
- `git diff --check`: passed.
- Targeted trailing-whitespace/final-newline check on touched Phase 03 files:
  passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-result-2026-07-08.md`
- `docs/reviews/risky-debt-typed-ir-phase03-smoke-2026-07-09.md`
- `docs/reviews/risky-debt-typed-ir-phase03-smoke-2026-07-09.json`

Gate status:

- `PASSED`

Review trail:

- Claude review remained unavailable under the Phase 00 external-service
  rejection boundary.
- Codex performed a local read-only skeptical review against the Phase 03
  evidence contract; no veto issue remained.

Next action:

- Begin Phase 04 executable backend translators.

### 2026-07-09 - Phase 04 - PRECHECK

Evidence contract:

- Question: Can branches show actual executable attempts or exact typed
  translation blockers?
- Baseline/comparator: current branch records contain typed obligations and
  formalization stubs, while executable controller attempts live only at the
  tree root.
- Primary criterion: branch records expose bounded backend attempts or precise
  blockers; an encodable algebraic fixture has scoped executable evidence; hard
  stochastic targets name the exact conditional expectation/interchange/domain
  blockers.
- Veto diagnostics: stubs described as proof, backend absence treated as
  refutation, branch-level evidence hidden at the root, unbounded backend
  command, or missing input/output artifact.
- Non-claims: backend attempts certify only the scoped encoded subgoal; typed
  blockers and translation attempts are diagnostic and do not prove the
  document claim.

Skeptical audit:

- Wrong baseline checked: compare against root-only backend attempts and branch
  stubs, not against a complete theorem-prover pipeline.
- Proxy metric checked: attempt/blocker counts are insufficient; tests must
  assert branch-visible evidence and specific typed blockers.
- Stop conditions checked: no package installation, network fetch, detached
  execution, destructive action, or proof-boundary weakening is needed.
- Hidden assumptions checked: root attempts must not be silently promoted to
  branch proofs unless the existing promotion guard accepts scoped certifying
  evidence.
- Artifact mismatch checked: implementation must update branch records,
  Markdown, tests, smoke artifacts, and the Phase 04 close record.

Actions:

- Begin scoped implementation in `src/mathdevmcp/document_derivation_tree.py`
  and focused document-tree tests.

Gate status:

- `IN_PROGRESS`

### 2026-07-09 - Phase 02 - ASSESS_GATE

Evidence contract:

- Question: Can the workflow avoid proposing assumptions that are already
  stated nearby?
- Primary criterion: `prop:interior-foc` marks proposition-stated assumptions
  as `stated`; equation rows inherit nearby stated proposition context;
  expectation law/integrability/interchange remain missing or unresolved.
- Veto diagnostics: all assumptions missing, all assumptions stated without
  source evidence, absent source refs, or proof overclaim.

Actions:

- Added deterministic local context graph construction.
- Attached context graphs to proposition/context packets and semantic packets.
- Added paragraph-context inheritance for row-level targets.
- Added Markdown display and coverage counters for graph status counts.
- Added focused regression tests for `prop:interior-foc` and `eq:foc-k`.
- Generated frozen Phase 02 risky-debt smoke artifacts.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_assumption_discovery.py -q`:
  passed, `13 passed in 67.46s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/assumption_discovery.py`:
  passed.
- `git diff --check`: passed.
- Targeted trailing-whitespace/final-newline check on touched Phase 02 files:
  passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-result-2026-07-08.md`
- `docs/reviews/risky-debt-context-graph-phase02-smoke-2026-07-09.md`
- `docs/reviews/risky-debt-context-graph-phase02-smoke-2026-07-09.json`

Gate status:

- `PASSED`

Review trail:

- Claude review remained unavailable under the Phase 00 external-service
  rejection boundary.
- Fresh subagent review was attempted but could not start because the agent
  thread limit was reached.
- Codex performed a local read-only skeptical review against the evidence
  contract; no veto issue remained.

Next action:

- Begin Phase 03 typed repair obligation IR.

### 2026-07-09 - Phase 03 - PRECHECK

Evidence contract:

- Question: Can each branch be generated from a typed obligation rather than
  raw LaTeX templates?
- Baseline/comparator: current branch records derive from semantic packet
  templates and formalization stubs; context graph exists but is not yet a
  typed obligation contract.
- Primary criterion: branches cite typed obligation ids with unresolved
  constructs and backend route hints; frozen FOC targets preserve expectation
  and derivative/interchange blockers.
- Veto diagnostics: branch without typed obligation; typed record hides
  unsupported stochastic/derivative operators; typed IR treated as proof;
  source provenance dropped.
- Non-claims: typed obligations are diagnostic routing artifacts only, not
  proof certificates and not backend encodings.

Skeptical audit:

- Wrong baseline checked: compare against semantic-packet branches without
  typed obligation ids, not against complete formalization.
- Proxy metric checked: obligation count alone is insufficient; tests must
  assert unresolved constructs, assumption statuses, backend route hints, and
  branch citations.
- Stop conditions checked: no package install, network fetch, destructive
  action, detached execution, or proof-boundary weakening is needed.
- Hidden assumptions checked: \(\E[\cdot\mid z]\), derivative rows, and
  context-graph statuses must remain visible in typed IR; source-stated
  differentiability must not close interchange/integrability.
- Artifact mismatch checked: implementation must reuse `math_ir.py`, update
  document-tree output, tests, smoke report, and Phase 03 close record.

Actions:

- Begin scoped implementation in `src/mathdevmcp/math_ir.py` and
  `src/mathdevmcp/document_derivation_tree.py`.

Gate status:

- `IN_PROGRESS`

### 2026-07-08 - Phase 01 - PRECHECK

Evidence contract:

- Question: Can proposition labels produce context packets rather than
  missing-focus entries?
- Baseline/comparator: current risky-debt Phase 04 report with
  `prop:interior-foc` in `missing_focus_labels`.
- Primary criterion: `prop:interior-foc` yields proposition source, equation
  targets `eq:foc-k`/`eq:foc-b`, local statement/context, and non-proof
  boundary.
- Veto diagnostics: proposition label still only missing; equation rows
  detached from parent proposition; context omitted; parser uncertainty hidden.
- Non-claims: context extraction is not proof or repair.

Skeptical audit:

- Wrong baseline checked: compare against missing proposition label in the
  prior report, not against complete proof extraction.
- Proxy metric checked: packet count is insufficient; tests must assert parent
  label, equation targets, statement/context, and non-claim boundary.
- Stop conditions checked: no new parser package; reuse existing LaTeX index
  and derivation target extraction.
- Hidden assumption checked: proposition statement is captured as source
  context, not treated as sufficient proof.

Actions:

- Begin scoped implementation in `src/mathdevmcp/derivation_target_extraction.py`
  and `src/mathdevmcp/document_derivation_tree.py`.

Gate status:

- `IN_PROGRESS`

### 2026-07-08 - Phase 01 - ASSESS_GATE

Evidence contract:

- Question: Can proposition labels produce context packets rather than
  missing-focus entries?
- Primary criterion: `prop:interior-foc` yields proposition source, equation
  targets `eq:foc-k`/`eq:foc-b`, local statement/context, and non-proof
  boundary.
- Veto diagnostics: proposition label still only missing; equation rows
  detached from parent proposition; context omitted; parser uncertainty hidden.

Actions:

- Added proposition context packet builder.
- Integrated proposition/context packets into `audit_document_derivation_tree`.
- Added tests for `prop:interior-foc` context packets and document audit
  coverage.
- Generated bounded risky-debt smoke report.

Checks:

- `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py -q`: passed, `11 passed in 55.11s`.
- `python3 -m py_compile src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py`: passed.
- `git diff --check` on touched Phase 01 files and ledger: passed.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-result-2026-07-08.md`
- `docs/reviews/risky-debt-context-packet-phase01-smoke-2026-07-08.md`
- `docs/reviews/risky-debt-context-packet-phase01-smoke-2026-07-08.json`

Gate status:

- `PASSED`

Non-claims:

- Context packets are not proofs and not repairs.
- Proof block linkage is not yet robustly modeled.

Next action:

- Phase 02 local mathematical context graph.

Review trail:

- Local artifact checks passed.
- Claude review gate was attempted with the compact read-only bundle, but the
  environment rejected it as external-service data exfiltration risk.  No
  workaround was attempted.
- Fresh Codex fallback review returned `VERDICT: AGREE`.

### 2026-07-08 - Phase 00 - ASSESS_GATE

Evidence contract:

- Question: Does the program target context-aware executable repair proposals?
- Primary criterion: plan requires proposition/context packets, context graph,
  typed IR, executable/blocker backend attempts, branch search, and
  document-ready regression reports.
- Veto diagnostics: no frozen targets, no external-tool-first discipline,
  detached execution despite visible template, Claude authority drift.

Actions:

- Wrote Phase 00 close record.
- Recorded Claude unavailability and fallback review agreement.

Artifacts:

- `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-result-2026-07-08.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 01 proposition/context packet extraction.
