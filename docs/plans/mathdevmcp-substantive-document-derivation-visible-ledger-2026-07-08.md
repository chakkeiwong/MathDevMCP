# MathDevMCP Substantive Document Derivation Visible Ledger

Date: 2026-07-08

Status: `IN_PROGRESS`

## Ledger Entries

### 2026-07-08 - Phase 00 - PRECHECK

Evidence contract:

- Question: Is the proposed program aimed at the real generic-tool regression?
- Baseline/comparator: current `audit_document_derivation_tree` output and
  existing external-tool-first lane.
- Primary criterion: plan requires semantic source reconstruction,
  branch-linked assumptions, formalization stubs, external-tool evidence,
  concrete patch text, and non-claims.
- Veto diagnostics: missing stop conditions, card-specific implementation,
  renderer-only workaround, no local tests, Claude treated as execution
  authority.
- Non-claims: no implementation correctness or report quality claim yet.

Skeptical audit:

- Wrong baseline checked: comparator is the current generic workflow, not an
  ideal theorem prover.
- Proxy metric checked: branch count and template count are not success
  criteria.
- Stop conditions checked: installs, detached launch, proof-boundary weakening,
  and nonconvergent review stop the run.
- Hidden assumptions checked: optional backend availability is diagnostic only.
- Artifact mismatch checked: later phases must add code/tests/reports, not just
  prose.

Actions:

- Drafted master program, phase subplans, visible runbook, and compact review
  bundle.

Artifacts:

- `docs/plans/mathdevmcp-substantive-document-derivation-master-program-2026-07-08.md`
- `docs/plans/mathdevmcp-substantive-document-derivation-visible-runbook-2026-07-08.md`
- `docs/reviews/mathdevmcp-substantive-document-derivation-plan-review-bundle-2026-07-08.md`

Gate status:

- `PASSED`

Next action:

- Patch review findings, rerun local artifact checks, then run fallback review.

Review trail:

- Claude review gate was attempted with a compact read-only bundle, but the
  environment rejected the command as an external-service data exfiltration
  risk.  This was treated as reviewer unavailability, not approval.
- Fresh Codex read-only fallback reviewer returned `VERDICT: REVISE`.
- Findings patched:
  - Phase 04 now freezes comparator artifacts, files, and labels.
  - Phase 02 now requires branch-level external-tool-first ledgers.
  - Phase results now require run manifests and decision tables.
- Second fresh Codex read-only fallback review returned `VERDICT: AGREE`.

### 2026-07-08 - Phase 00 - ASSESS_GATE

Evidence contract:

- Question: Is the proposed program aimed at the real generic-tool regression?
- Primary criterion: plan requires semantic source reconstruction,
  branch-linked assumptions, formalization stubs, external-tool evidence,
  concrete patch text, and non-claims.
- Veto diagnostics: card-specific implementation, renderer-only workaround,
  no local tests, missing stop conditions, Claude authority drift.

Actions:

- Wrote Phase 00 close record.
- Recorded Claude unavailability and Codex fallback review convergence.

Artifacts:

- `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-result-2026-07-08.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 01 semantic obligation reconstruction.

### 2026-07-08 - Phase 01 - PRECHECK

Evidence contract:

- Question: Can the document workflow stop auditing row fragments and preserve
  complete local proof targets?
- Baseline/comparator: current locator row packets with only a row target and a
  `label_row_count` blocker for multiline labels.
- Primary criterion: multiline label packets include full display text, display
  span, grouped source target, row target, operator inventory, and symbol
  inventory.
- Veto diagnostics: full display missing, line span wrong, row provenance
  dropped, source uncertainty hidden.
- Non-claims: reconstruction alone does not prove or repair any mathematical
  claim.

Skeptical audit:

- Wrong baseline checked: this phase compares against current row-local packet
  behavior, not a complete LaTeX parser.
- Proxy metric checked: field presence is insufficient unless tests check
  concrete multiline content.
- Stop conditions checked: no new parser package or broad locator rewrite.
- Environment mismatch checked: no backend calls are required for this phase.
- Artifact mismatch checked: phase must add code and tests, not only prose.

Actions:

- Begin scoped implementation in `src/mathdevmcp/document_derivation_tree.py`
  and `tests/test_document_derivation_tree.py`.

Gate status:

- `IN_PROGRESS`

### 2026-07-08 - Phase 04 - ASSESS_GATE

Evidence contract:

- Question: Does the high-level report materially improve without becoming
  document-specific or overclaiming?
- Primary criterion: frozen reports include semantic obligations,
  branch-linked assumptions, derivation routes, backend/formalization evidence,
  patch candidates or precise blockers, and non-claims.
- Veto diagnostics: card-specific logic, hand-wavy-only patch text, proof
  overclaim, missing non-claims.

Actions:

- Ran frozen risky-debt and credit-card report commands.
- Added visible `missing_focus_labels` to markdown summaries.
- Wrote Phase 04 result.

Checks:

- Frozen report JSON contract assertion: passed.
- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`: passed, `13 passed in 43.84s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`: passed.
- `git diff --check` on touched code/plans/reports: passed.

Artifacts:

- `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-result-2026-07-08.md`
- `docs/reviews/risky-debt-document-derivation-tree-phase04-frozen-2026-07-08.md`
- `docs/reviews/risky-debt-document-derivation-tree-phase04-frozen-2026-07-08.json`
- `docs/reviews/credit-card-npv-document-derivation-tree-phase04-frozen-2026-07-08.md`
- `docs/reviews/credit-card-npv-document-derivation-tree-phase04-frozen-2026-07-08.json`

Gate status:

- `PASSED_WITH_RECORDED_PROPOSITION_LABEL_LIMITATION`

Non-claims:

- No whole-document proof, global correctness, or release-readiness claim.
- Formalization stubs are non-certifying.

Next action:

- Close the visible runbook slice and report outcome.

### 2026-07-08 - Phase 03 - ASSESS_GATE

Evidence contract:

- Question: Can the tool show the next concrete backend check instead of only
  saying "formalize the claim"?
- Primary criterion: each supported branch has backend-specific stubs or
  explicit unsupported-formalization blockers.
- Veto diagnostics: stub represented as proof, backend absence as refutation,
  unbounded backend command, missing tool/version evidence.

Actions:

- Added SymPy/Sage/Lean formalization stubs to assumption branches.
- Added formalization blockers for unsupported constructs.
- Regenerated explanatory Phase 03 smoke report for
  `eq:panel-npv-functional`.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py tests/test_external_tool_adapters.py -q`: passed, `40 passed in 44.66s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/external_tool_adapters.py`: passed.
- `git diff --check -- src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`: passed.

Artifacts:

- `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-result-2026-07-08.md`
- `docs/reviews/credit-card-npv-formalization-stubs-phase03-smoke-2026-07-08.md`
- `docs/reviews/credit-card-npv-formalization-stubs-phase03-smoke-2026-07-08.json`

Gate status:

- `PASSED`

Non-claims:

- Formalization stubs are next-check artifacts, not certificates.

Next action:

- Begin Phase 04 frozen report regression gate.

### 2026-07-08 - Phase 04 - PRECHECK

Evidence contract:

- Question: Does the high-level report materially improve without becoming
  document-specific or overclaiming?
- Baseline/comparator: frozen baseline artifacts
  `docs/reviews/risky-debt-derivation-gap-proposals-v2.md` and
  `docs/reviews/credit-card-npv-generic-document-derivation-tree-smoke-2026-07-08.md`.
- Primary criterion: frozen-label reports include source-local semantic
  obligations, branch-linked assumptions, derivation routes, backend or
  formalization evidence, patch candidates or precise blockers, and non-claims.
- Veto diagnostics: card-specific logic, hand-wavy patch text, no proposed fix
  when branch supports one, proof overclaim, missing non-claims.
- Non-claims: no whole-document proof, release readiness, or global correctness
  claim.

Skeptical audit:

- Wrong baseline checked: use frozen old artifacts, not an easy-label report.
- Proxy metric checked: selected row counts cannot substitute for branch
  quality and patch text.
- Stop conditions checked: no long backend search or package install.
- Hidden assumption checked: proposition labels outside display math may be
  reported as missing focus labels, not silently ignored.

Actions:

- Run frozen risky-debt and credit-card report commands.

Gate status:

- `IN_PROGRESS`

### 2026-07-08 - Phase 02 - ASSESS_GATE

Evidence contract:

- Question: Can each proposed assumption set be consumed by an agent as a
  possible closure route rather than a generic suggestion?
- Primary criterion: branch closure links, source-local route, external-tool
  ledger, and proposed assumption text.
- Veto diagnostics: branch not tied to obligation, no route, no external-tool
  ledger, or global minimality claim.

Actions:

- Added `assumption_branches` and branch-derived patch candidates to document
  derivation trees.
- Added markdown sections for candidate assumption branches and proposed patch
  candidates.
- Regenerated explanatory Phase 02 smoke report for
  `eq:panel-npv-functional`.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_derivation_search_tree.py -q`: passed, `19 passed in 47.79s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py`: passed.
- `git diff --check -- src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`: passed.

Artifacts:

- `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-result-2026-07-08.md`
- `docs/reviews/credit-card-npv-assumption-branches-phase02-smoke-2026-07-08.md`
- `docs/reviews/credit-card-npv-assumption-branches-phase02-smoke-2026-07-08.json`

Gate status:

- `PASSED`

Non-claims:

- Patch candidates are diagnostic proposed text, not certified repairs.
- Branches are sufficient candidates, not globally minimal assumptions.

Next action:

- Begin Phase 03 formalization stub and backend blocker integration.

### 2026-07-08 - Phase 03 - PRECHECK

Evidence contract:

- Question: Can the tool show the next concrete backend check instead of only
  saying "formalize the claim"?
- Baseline/comparator: current branches include assumption routes and backend
  attempts but no backend-specific formalization stubs.
- Primary criterion: each supported branch has a backend-specific stub or an
  explicit unsupported-formalization blocker.
- Veto diagnostics: stub represented as proof, backend unavailability treated
  as refutation, unbounded backend command, missing tool/version evidence.
- Non-claims: stubs are not proofs unless a certifying backend verifies them.

Skeptical audit:

- Wrong baseline checked: this phase compares against no formalization stubs,
  not against complete Lean/Sage proof search.
- Proxy metric checked: generating many stubs is not success unless each has a
  backend, encoded assumptions, unsupported operators, and non-certifying
  boundary.
- Stop conditions checked: no package installs or long backend commands.
- Environment mismatch checked: backend availability comes from the recorded
  external-tool ledger/doctor, not assumptions about active Python.

Actions:

- Begin scoped implementation in `src/mathdevmcp/document_derivation_tree.py`
  and tests.

Gate status:

- `IN_PROGRESS`

### 2026-07-08 - Phase 01 - ASSESS_GATE

Evidence contract:

- Question: Can the document workflow stop auditing row fragments and preserve
  complete local proof targets?
- Primary criterion: full display text, display span, grouped source target,
  row target, operator inventory, and symbol inventory.
- Veto diagnostics: full display missing, row provenance dropped, source
  uncertainty hidden.

Actions:

- Added full-display reconstruction and semantic inventories to
  `src/mathdevmcp/document_derivation_tree.py`.
- Added focused tests in `tests/test_document_derivation_tree.py`.
- Generated explanatory smoke report for `eq:panel-npv-functional`.

Checks:

- `python3 -m pytest tests/test_document_derivation_tree.py -q`: passed, `5 passed in 45.30s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py`: passed.
- `git diff --check -- src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py`: passed.

Artifacts:

- `docs/reviews/credit-card-npv-semantic-obligation-phase01-smoke-2026-07-08.md`
- `docs/reviews/credit-card-npv-semantic-obligation-phase01-smoke-2026-07-08.json`

Gate status:

- `PASSED`

Non-claims:

- Phase 01 does not create concrete patch candidates or prove any branch.
- The smoke report is explanatory only; it is not the frozen Phase 04
  regression gate.

Next action:

- Begin Phase 02 assumption branch closure.

### 2026-07-08 - Phase 02 - PRECHECK

Evidence contract:

- Question: Can each proposed assumption set be consumed by an agent as a
  possible closure route rather than a generic suggestion?
- Baseline/comparator: current `possible_assumption_sets` lists with limited
  connection to exact document variables and no patch candidates.
- Primary criterion: each branch states obligations it closes, source-local
  route, branch-level external-tool-first evidence, and proposed assumption
  text.
- Veto diagnostics: branch not tied to obligation, no mathematical why, no
  derivation route, no external-tool ledger, or global minimality claim.
- Non-claims: branches are sufficient candidates, not necessary/minimal
  assumptions unless backend-certified.

Skeptical audit:

- Wrong baseline checked: this phase compares against the current assumptions
  list, not against complete proof search.
- Proxy metric checked: merely adding branch count is not enough; tests must
  check closure links and proposed text.
- Stop conditions checked: no domain-specific card-only implementation.
- External-tool policy checked: branch records must carry the tool ledger from
  the root plan.

Actions:

- Begin scoped implementation in `src/mathdevmcp/document_derivation_tree.py`
  and `tests/test_document_derivation_tree.py`.

Gate status:

- `IN_PROGRESS`
