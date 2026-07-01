# Credit card NPV component proposal rewrite plan

Date: 2026-06-30

Document under review:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

## Review cycle 1: self-review findings

Decision: REWRITE REQUIRED

The first draft has the right scope boundary and covers the major sections from
the accepted writing plan. It builds successfully and avoids the earlier
over-scope problem. However, it still needs a rewrite before it is strong enough
as a bank implementation proposal.

## Material issues

1. **Decision-context contracts are too thin.**
   The current decision-context tables name context, scored unit, candidate
   action, baseline, and mode, but the accepted plan required richer contract
   fields: caller or consumer system, candidate-action owner, explicit
   counterfactual, feature stage, required output, and reminder that the caller
   chooses the action. The current tables are concise but not yet sufficiently
   operational.

2. **Valuation policy needs ownership and approval detail.**
   The valuation policy section defines semantics, but it should more clearly
   state who must approve discounting, funds-transfer-pricing, capital, tax,
   cost allocation, terminal value, relationship value, and scenario bundles.
   It should distinguish business-default, finance-approved, model-risk-approved,
   and use-case-specific conventions.

3. **Input/output contract should be more schema-like.**
   The current prose lists fields, but the final proposal should include compact
   contract tables for request envelope fields, valuation fields, feature-domain
   groups, output fields, and status/warning semantics. This will make the
   document easier for engineering, model governance, and consuming-system teams
   to use.

4. **No-score, degraded-score, fallback, and replay semantics are underdeveloped.**
   The document says these statuses exist, but it should define when each status
   is used, what downstream systems may do with it, and what must be logged.
   It should also state that replay reproducibility depends on retained feature
   snapshots, model versions, schema versions, assumption bundles, and code
   artifacts.

5. **Operating modes need sharper practical requirements.**
   The online, batch, and option-grid descriptions are useful but still generic.
   Add a table with latency/freshness, request shape, failure handling, fallback,
   idempotency, audit logging, and rollback expectations for each mode.

6. **Governance needs explicit owners, vetoes, and reapproval triggers.**
   The five governance lenses are present, but the document should add a table
   that names likely owners and gives concrete veto diagnostics and reapproval
   triggers. The text should emphasize that approval is by use case and by
   valuation semantics.

7. **Migration section needs stronger reconciliation artifacts.**
   The migration steps are good, but the document should add a table of required
   artifacts: consumer inventory, legacy schema map, valuation-definition
   comparison, ranking comparison, segment tie-out, decomposition tie-out,
   disagreement analysis, contract tests, legacy retirement map, rollback plan.

8. **Readability and cohesion can improve.**
   Some sections repeat the boundary language, while other sections need a
   clearer handoff. Add short opening paragraphs that orient the reader to why
   each section exists. Keep the literature support short, but explicitly refer
   to the literature survey as the evidence appendix rather than rearguing the
   literature.

## Rewrite instructions

### A. Strengthen the executive framing

Add a short paragraph after the executive recommendation explaining the three
questions every component call must answer:

1. What decision context is being valued?
2. What valuation semantics and assumption bundle are being used?
3. What can the caller safely do with the output?

Keep the component-only boundary.

### B. Rewrite decision-context section

Replace or augment the two current decision tables with richer tables. Required
columns:

- context;
- caller system;
- scored unit;
- action owner;
- candidate-action form or action-set shape;
- baseline/counterfactual;
- feature stage;
- mode;
- output needed.

Keep acquisition/cross-sell and existing-account treatment grouped separately.
Add a concise offline-consumer table for portfolio, finance, and risk use.
Each row must state that the caller system owns final action choice and
execution; the component only values options. Offline portfolio, finance, and
risk rows must be framed as consumers of component outputs only, not as new
reporting, ledger, or stress-platform scope.

### C. Expand valuation policy section

Add a table of valuation choices:

- horizon and terminal value;
- discount curve;
- funding/FTP;
- capital;
- tax;
- marginal versus allocated costs;
- rewards and acquisition cost;
- relationship/deposit value;
- cannibalization;
- scenario and downstream policy bundle.

For each choice specify owner/approver, output tag, and risk if unspecified.

### D. Add schema-style request and response tables

Add tables for:

- request envelope fields;
- required feature-domain groups;
- response envelope and valuation fields;
- status and warning semantics.

The schema tables must mark required, optional, and conditionally required
fields by decision context and operating mode. For each contract field, specify
at least:

- field name;
- business definition;
- data type;
- unit or currency where applicable;
- cardinality;
- allowed values or enum domain;
- requiredness by context and operating mode;
- versioning and backward-compatibility rule.

The status table must define:

- conditions that trigger `scored`, `no-score`, `degraded-score`,
  `out-of-domain`, and `manual-review` statuses;
- status scope: request-level, batch-row/account-level, and candidate-option
  level;
- how mixed-status batch and multi-option responses are encoded;
- the distinction between governed business outcomes such as `no-score` or
  `manual-review` and retryable technical or integration failures;
- what downstream systems are allowed to do for each status;
- mandatory warning, log, and audit fields for each status;
- replay prerequisites and known replay limitations.

Keep the JSON examples, but make the tables the primary contract.

### E. Add operating-mode table

Add a table covering:

- single-request online;
- batch portfolio;
- multi-option grid.

Columns:

- typical consumers;
- latency/freshness;
- request shape;
- idempotency expectation;
- failure/fallback;
- permitted fallback behavior, such as legacy output, conservative no-score, or
  manual review;
- audit/replay requirement.
- rollback expectation and rollback interface.

### F. Add governance table

Add a table for the five governance lenses:

- predictive validation;
- causal/treatment validation;
- finance reconciliation;
- data-quality/integration monitoring;
- use-case approval/change control.

Columns:

- primary owner;
- veto diagnostics;
- monitoring cadence;
- reapproval triggers.

Include compliance language that NPV explanations are not automatically
adverse-action reasons.

### G. Add migration artifact table

Add a table listing required migration artifacts, purpose, and owner:

- current-consumer inventory;
- legacy schema/output map;
- legacy-vs-new valuation policy comparison;
- shadow-score run manifest;
- ranking and decision-impact comparison;
- segment aggregate tie-out;
- decomposition tie-out;
- disagreement-analysis register;
- downstream contract-test results;
- legacy retirement map;
- rollback plan.

Add cutover-gate language for the migration artifacts. The rewritten proposal
must specify that every controlled consumer has documented pass/fail criteria
before production reliance, including:

- acceptable segment-level aggregate tie-out tolerances;
- acceptable decomposition tie-out tolerances;
- ranking-comparison and decision-impact thresholds;
- disagreement-rate thresholds and required disagreement-register disposition;
- contract-test pass requirements;
- no-score and degraded-score thresholds;
- named rollback triggers, rollback owner, and rollback interface.

### H. Preserve what works

Keep:

- the title and abstract structure;
- the component charter;
- the core NPV equations;
- the component-only boundary;
- the internal modeling module table;
- the pitfalls and controls table;
- the roadmap and acceptance criteria;
- the short literature support section.

## Acceptance criteria for rewrite cycle 1

- The rewritten proposal still states that this is only an NPV component.
- Decision-context tables include caller, owner, counterfactual, feature stage,
  mode, and output needed.
- Valuation policy table includes owners/approvers and output tags.
- Request/response schema and status semantics are explicit.
- Operating modes include failure/fallback and replay requirements.
- Governance includes owners, vetoes, cadence, and reapproval triggers.
- Migration includes reconciliation artifacts.
- Decision-context and operating-mode material state that caller systems own
  final action choice and execution.
- Operating modes specify idempotency and rollback expectations.
- Score statuses define downstream handling and logging obligations.
- Schema tables mark required, optional, and conditionally required fields.
- Schema tables include field-level type, unit, cardinality, allowed values, and
  compatibility semantics.
- Score statuses define request, row/account, and option-level scope and mixed
  batch/option-grid behavior.
- Migration includes explicit cutover gates and rollback trigger thresholds.
- PDF builds with no fatal errors, undefined citations/references, or overfull
  boxes.

## Claude review status

Round 1: REVISE. Claude found that the rewrite instructions did not fully carry
through operational requirements for idempotency, rollback, caller-owned action
choice, status handling, replay semantics, and required-vs-conditional schema
fields. This plan has been revised to make those requirements explicit.

Round 2: REVISE. Claude found that schema instructions still lacked
field-level type/unit/cardinality/enum/versioning semantics, status semantics
did not force request-vs-row-vs-option scope or mixed-status behavior, and
migration artifacts did not force cutover thresholds. This plan has been
revised to require those details.
