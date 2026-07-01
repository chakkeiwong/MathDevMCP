# Credit card NPV component proposal review log

Date: 2026-06-30

This log records bounded Claude review rounds for the proposal writing plan and
the later final-document rewrite process.

## Plan review rounds

### Round 1

Reviewer: Claude Code

Decision: REVISE

Material findings:

1. The decision-context section was too flat and risked scope creep by mixing
   decision-time calls, offline analytics, and portfolio reporting.
2. The valuation contract was under-specified: horizon, discounting, capital,
   tax, relationship value, cannibalization, terminal value, and assumption
   bundle ownership needed explicit treatment.
3. The integration contract lacked operational API semantics such as request
   IDs, timestamps, schema versions, option grids, no-score behavior, lineage,
   fallback, shadow mode, and rollback.
4. Validation and governance needed separation into predictive validation,
   causal validation, finance reconciliation, integration monitoring, and
   use-case approval.
5. Migration needed reconciliation artifacts beyond shadow scoring.

Revisions made:

- Added a component charter to keep the ownership boundary explicit.
- Replaced the flat decision-context list with grouped acquisition/cross-sell,
  existing-account treatment, and offline portfolio/finance/risk consumers.
- Added a standalone valuation policy and assumption contract section.
- Expanded input/output contracts with request IDs, use-case IDs, timestamps,
  schema/model/scenario/assumption versions, option grids, no-score statuses,
  and decomposition identifiers.
- Added online, batch, and multi-option grid operating modes with SLA, feature
  freshness, idempotency, audit, fallback, and rollback requirements.
- Expanded integration failure modes.
- Rewrote validation/governance requirements around five governance lenses and
  use-case-specific approval.
- Expanded migration to include ranking comparisons, segment tie-outs,
  decomposition tie-outs, assumption comparison, downstream contract tests,
  legacy-output retirement, rollback triggers, and rollback ownership.

### Round 2

Reviewer: Claude Code

Decision: ACCEPT

Material findings:

- None.

Non-blocking suggestions incorporated:

- Added canonical valuation-semantics identifier requirements.
- Required compact request/response examples for online and batch or
  multi-option scoring.
- Added hard contract-test acceptance criteria for schema validation,
  decomposition summation, deterministic replay, no-score/degraded-score
  behavior, and downstream contract tests.

## Final-document review and rewrite rounds

### Rewrite-plan round 1

Reviewer: Claude Code

Decision: REVISE

Material findings:

1. The rewrite plan did not fully carry through operational requirements for
   idempotency and rollback.
2. It did not force the decision-context rewrite to state that caller systems
   own final action choice and execution.
3. Status, fallback, and replay semantics were too loose.
4. Schema instructions did not require fields to be marked required, optional,
   or conditionally required.

Revisions made:

- Added action-owner and caller-owned execution requirements to the
  decision-context rewrite.
- Added idempotency, permitted fallback, rollback expectation, and rollback
  interface columns to operating-mode requirements.
- Added status-trigger, downstream-handling, logging, and replay requirements.
- Added required/optional/conditional schema-field requirements.

### Rewrite-plan round 2

Reviewer: Claude Code

Decision: REVISE

Material findings:

1. Schema requirements were still too descriptive and did not require
   field-level type, unit, cardinality, enum/domain, or compatibility semantics.
2. Score-status semantics did not force request-level, row/account-level, and
   option-level scope, nor mixed-status batch or option-grid behavior.
3. Migration and reconciliation artifacts lacked explicit cutover thresholds
   and pass/fail gates.

Revisions made:

- Required every schema field to specify name, business definition, data type,
  unit/currency, cardinality, allowed values or enum domain, requiredness by
  context/mode, and versioning/backward-compatibility rule.
- Required status semantics for request, row/account, and option scope,
  mixed-status responses, and the distinction between governed business
  outcomes and retryable technical failures.
- Required migration cutover gates for tie-outs, ranking and decision impact,
  disagreement rates, contract tests, no-score/degraded-score rates, and named
  rollback triggers.

### Rewrite-plan round 3

Reviewer: Claude Code

Decision: ACCEPT

Material findings:

- No material blocker remained. Claude confirmed that the revised plan now
  required field-level schema semantics, request/row/option status scope,
  mixed-status behavior, idempotency, fallback, rollback, migration cutover
  thresholds, and component-only scope containment.

### Final-document review round 1

Reviewer: Claude Code

Decision: ACCEPT

Material findings:

- No rewrite was required. Claude found the organization, scope containment,
  cohesion, and implementation specificity acceptable for shipment.

Minor edits made after acceptance:

- Added an explicit first production slice: one controlled marketing or
  prescreen acquisition consumer, batch mode, one offer family, and one
  incremental pre-tax valuation semantics bundle.
- Normalized the compact JSON example to use the canonical
  `baseline_action_id` field.
- Lightly trimmed repeated scope language in the charter and conclusion.

## Evidence-integrated rewrite rounds

### Evidence rewrite plan

Decision: EXECUTED

Plan artifact:

- `docs/plans/credit-card-npv-component-evidence-integrated-rewrite-plan-2026-06-30.md`

Skeptical audit before execution:

- The correct baseline was the existing component proposal plus the existing
  LaTeX literature review, not a blank report.
- The objective remained incremental risk-adjusted NPV, not response,
  approval, activation, first spend, or schema completeness.
- Scope was kept to the replacement NPV component, not the surrounding
  campaign, underwriting, finance, stress, account-management, or reporting
  platforms.
- Public literature was used to justify mechanisms and model structure; bank
  parameters were labeled as requiring internal data or experiments.
- Dense implementation material was moved or kept in appendices.

### Evidence final-document review round 1

Reviewer: Claude Code

Decision: REVISE

Material findings:

1. The revised document materially integrated the literature review, but still
   read too much like "survey recap, then proposal" in the evidence section.
2. The front door was still too technical for executive readers.
3. The four evidence classes were introduced, but not carried consistently
   through later design sections.
4. Some implementation-contract and status material risked pulling the report
   toward a broader platform proposal.
5. A few design choices could be mistaken for conclusions compelled by the
   literature.

Revisions made:

- Added a seven-commitment executive front-door summary.
- Rewrote the evidence section around six design requirements:
  incremental value, state-dependent spend/payment/balance/loss, separate
  issuance/activation/use transitions, lifetime and attrition states,
  bank-native auditable decomposition, and downstream-policy tagging.
- Labeled bank-native decomposition as a governance-aligned design
  extrapolation rather than a direct literature result.
- Labeled principal/non-principal subledgers, valuation semantics, request
  lineage, and status handling as governance or engineering conventions.
- Clarified that all-bank incremental value for existing-client cross-sell
  requires approved internal identification evidence.
- Shortened the online-scoring wording that had caused the earlier overfull
  LaTeX line.

### Evidence final-document review round 2

Reviewer: Claude Code

Decision: ACCEPT

Material findings:

- No material rewrite remained. Claude found that the document now had the
  requested design-decision spine, clear front-door summary, explicit evidence
  classes, and clearer labeling of literature-supported mechanisms versus
  bank-specific estimation needs versus design conventions.

Minor edits made after acceptance:

- Added an explicit pointer from the executive summary to the appendices for
  implementation contracts, status semantics, migration artifacts, and
  claim-support detail.
- Made the three main-table captions more action-oriented.
- Added a line in the governance section that the proposal does not by itself
  approve any production use case beyond a shadow-tested first slice.
- Trimmed one repeated scope sentence from the conclusion.

Build verification:

- Built `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
  with `latexmk -pdf -interaction=nonstopmode -halt-on-error`.
- Output PDF:
  `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.pdf`
  (18 pages).
- Focused log scan found no undefined citations, no undefined references, no
  fatal LaTeX errors, and no overfull boxes. Remaining underfull bibliography
  warnings are due to long URLs.

## Full-depth remediation after compression regression

### Regression finding

Reviewer: User

Decision: REVISE

Material finding:

- The evidence-integrated rewrite compressed a 26-page literature survey plus
  a substantial component proposal into an 18-page PDF. That was a serious
  regression. Integration should preserve evidentiary substance and operating
  detail while organizing them for human readers; it should not collapse the
  work into an executive digest.

### Remediation plan

Decision: EXECUTED

Plan artifact:

- `docs/plans/credit-card-npv-component-full-depth-remediation-plan-2026-06-30.md`

Skeptical audit before execution:

- The baseline was reset to the full literature survey plus the accepted
  component-proposal plans and review log, not the 18-page compressed memo.
- Page count was treated only as an anti-compression guardrail; the substantive
  objective remained a defensible incremental NPV replacement-component
  proposal.
- The replacement scope stayed component-only: not a campaign platform,
  underwriting engine, finance ledger, stress platform, account-management
  platform, or reporting platform.
- Literature supports mechanisms and model structure; bank-specific activation,
  cannibalization, spend response, loss elasticity, and value parameters remain
  internal-data or experiment requirements.

### Remediation work

- Restored the proposal source from the full LaTeX survey as the evidence base.
- Added a new executive summary and component charter.
- Added a replacement-boundary section explaining how the evidence body and
  operating specification fit together.
- Preserved the survey's substantive sections on market/employment effects,
  payment adoption/use, rewards, cannibalization, lifetime expenditure, model
  architecture, component decomposition, decision pitfalls, empirical
  validation, open gaps, and source-support audit.
- Added component-specific operating sections for decision-context contracts,
  valuation semantics, request contract, response contract, score-status
  semantics, operating modes, governance, migration artifacts, cutover gates,
  and explicit non-approval of broader production uses.
- Added a reader guide and a system-context figure to clarify that the proposal
  replaces the valuation component, not the surrounding caller systems.

### Remediation review round 1

Reviewer: Claude Code

Decision: ACCEPT

Material findings:

- Claude found that the regression was fixed: the current proposal preserves
  the survey's substantive analytical spine and adds a real
  replacement-component proposal on top of it.
- Claude found the literature genuinely integrated into component design, with
  operating-spec detail sufficient for valuation semantics, decision contexts,
  request/response/status contracts, operating modes, migration, and
  governance.
- Claude found table density to be a non-blocking readability issue rather
  than a substantive blocker.

Non-blocking polish incorporated:

- Added a reader guide distinguishing preserved survey evidence from the new
  operating specification.
- Added a system-context figure showing caller systems, the NPV component,
  assumption bundles, governance, and finance/risk reconciliation.

Build verification:

- Built `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
  with `latexmk -pdf -interaction=nonstopmode -halt-on-error`.
- Output PDF:
  `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.pdf`
  (39 pages).
- Source length: 2,562 LaTeX lines.
- Focused log scan found no undefined citations, no undefined references, no
  fatal LaTeX errors, and no overfull boxes. Remaining underfull warnings are
  from longtable cells and bibliography URLs.
