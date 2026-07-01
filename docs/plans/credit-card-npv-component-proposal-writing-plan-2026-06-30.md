# Credit card NPV component proposal writing plan

Date: 2026-06-30

## Purpose

Write a standalone proposal for building a replacement **credit card customer
NPV estimation component** for a large U.S. retail bank. The component is not an
enterprise decisioning platform. It is the valuation module that plugs into
existing bank systems and returns decision-grade, component-level,
counterfactual NPV estimates for new-card and new-card-to-existing-client
decisions.

The literature survey in `docs/credit-card-npv-survey/` is an input and
supporting appendix. The new proposal must be practical: it should specify
scope, interfaces, data contracts, output contracts, model design, validation,
governance, migration, and implementation risks.

## Skeptical plan audit

The most likely failure mode is scope creep: accidentally proposing that we
build the surrounding marketing, underwriting, account-management, finance, or
reporting platforms. The proposal must instead state that those systems remain
owners of execution and policy, while the NPV component owns valuation,
decomposition, methodology, validation evidence, and integration contracts.

The second failure mode is writing a generic strategy memo. The proposal must be
specific enough to guide implementation: it should name input data classes,
output fields, decision contexts, component submodels, validation tests,
fallback behavior, and migration steps from the current component.

The third failure mode is treating one NPV estimate as universal. The component
must be decision-context aware: the caller must declare the population, action
set, counterfactual, data timestamp, scenario, and downstream policy assumption.

The fourth failure mode is treating the literature survey as the main product.
The survey should support why the component needs causal lift, adoption/use
separation, PD/LGD/EAD, CLV/duration, and dynamic policy assumptions, but the
proposal should focus on the component that the bank will build.

## Target deliverables

1. A standalone LaTeX proposal under
   `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`.
2. A compiled PDF under the same directory.
3. A bibliography file or reuse of the existing survey bibliography.
4. A review log under
   `docs/plans/credit-card-npv-component-proposal-review-log-2026-06-30.md`.
5. A rewrite plan under
   `docs/plans/credit-card-npv-component-proposal-rewrite-plan-2026-06-30.md`
   if the final-document review identifies material issues.

## Proposed title

`Credit Card Customer NPV Estimation Component: Proposal for a Replacement
Valuation Module Integrated with Bank Decision Systems`

## Proposal thesis

The bank should replace the current NPV/value component with a governed,
component-based NPV estimator that can be called by existing decision systems.
For a declared decision context, the component should return incremental
risk-adjusted NPV and its drivers:

```text
NPVOutput = f(CustomerState,
              DecisionContext,
              CandidateAction,
              ProductTerms,
              ScenarioAssumptions,
              DownstreamPolicyAssumptions,
              ModelVersion)
```

The component is a valuation service/library. It does not own campaign
execution, underwriting policy, account-management workflow, finance systems, or
enterprise reporting.

## Audience

- Card product and marketing leadership.
- Credit-risk and underwriting teams.
- Account-management and line-management teams.
- Finance/PPNR and capital stakeholders.
- Data engineering and platform teams responsible for integration.
- Model-risk management and compliance reviewers.

## Required sections

### 1. Executive Summary

State the recommendation, replacement scope, business value, and non-ownership
boundary. Explain why the component is needed even if the surrounding systems
already exist.

Key points:

- The current problem is not lack of a decisioning platform; it is lack of a
  reliable, reusable NPV component.
- The component must be callable by many decision systems but must not conflate
  their counterfactuals.
- The output must be decomposed and auditable, not only one score.
- Include a short "How to read this proposal" summary table that distinguishes
  the component boundary, consumer systems, valuation contracts, integration
  contracts, controls, and migration path.

### 2. Current-State Problem and Replacement Boundary

Describe what the current component likely does and why it is insufficient.
Avoid inventing internal facts; phrase unknowns as discovery items.

Cover:

- current consumers to inventory;
- current input/output schema to map;
- weak spots to test: raw response/value proxies, missing counterfactuals,
  weak cannibalization treatment, limited component explanations, stale
  assumptions, inconsistent finance/risk definitions;
- compatibility requirements and backward-compatible output fields during
  migration.

### 3. Component Scope and Non-Scope

Begin with a short component charter:

> The NPV component owns valuation. Caller systems own action selection,
> policy thresholds, campaign orchestration, underwriting rules, line-management
> workflow, finance reporting, and customer execution.

Then explicitly list owned and non-owned responsibilities.

Owned by the NPV component:

- NPV definition and cash-flow decomposition;
- counterfactual valuation logic;
- component forecasts for spend, balance, payment, loss, cost, funding,
  capital, attrition, and terminal value;
- decision-context input contract;
- output contract and explanations;
- scenario/sensitivity support;
- validation and monitoring package;
- model versioning and audit metadata.

Not owned:

- campaign orchestration;
- underwriting rule engine;
- bureau ingestion platform;
- card processor system of record;
- rewards fulfillment platform;
- servicing/collections workflow;
- finance ledger, CECL, or stress-testing production platforms;
- enterprise reporting platform.

### 4. Decision Contexts the Component Must Support

Do not use one flat table that implies all consumers have the same decision
semantics. Use grouped subsections or grouped tables.

Group 1: decision-time acquisition and cross-sell consumers:

- new-to-bank acquisition targeting;
- existing-client new-card cross-sell;
- prescreen/preapproval;
- application underwriting;
- initial line assignment;
- offer design and pricing;
- activation/early-usage treatment.

Group 2: existing-account treatment consumers:

- existing-cardholder line increase/decrease;
- retention and inactivity treatment;
- product conversion;
- promotional balance or rewards treatment;
- collections/servicing-sensitive forward value where permitted.

Group 3: offline portfolio, finance, and risk consumers:

- campaign budget allocation analytics;
- portfolio profitability reporting;
- vintage profitability and business review;
- scenario, stress, and planning analyses.

For every row require:

- caller/consumer system;
- scored unit, such as person, household, account, application, or account-action
  pair;
- candidate-action owner;
- action set;
- explicit baseline action;
- counterfactual definition;
- population and available feature stage;
- required latency or batch mode;
- required output;
- key pitfalls;
- statement that the caller, not the component, chooses or executes the action.

### 5. Valuation Policy and Assumption Contract

Add a standalone section before the input contract. This is the definition of
"NPV" that prevents different consumers from using incompatible value numbers.

Require the proposal to define:

- horizon or horizons, such as 12-month, 36-month, lifetime, and terminal-value
  conventions;
- discount-rate, funds-transfer-pricing, and liquidity/funding conventions;
- capital cost convention and whether capital is economic, regulatory, or
  stress capital;
- tax treatment and pre-tax versus post-tax output requirements;
- marginal versus allocated operating-cost rules;
- reward, acquisition, servicing, fraud, dispute, and collections cost rules;
- when deposit and broader relationship value is allowed, forbidden, or reported
  separately;
- cannibalization treatment for old bank cards, debit, deposits, and outside
  cards;
- shared-household and multi-product attribution rules;
- terminal-value approach and sensitivity requirements;
- scenario bundle ownership, approval, and versioning;
- downstream policy-assumption bundle ownership, approval, and versioning;
- canonical valuation-semantics identifiers that tag incremental versus total
  basis, horizon basis, tax basis, discount/funding bundle, scenario bundle,
  and downstream-policy bundle;
- required fields that identify which valuation convention produced the output.

### 6. Input Contract

Define required and optional inputs. Organize by domain:

- `request_id` and `trace_id`;
- `consumer_use_case_id`;
- schema version, model version, assumption-bundle version, and scenario version;
- as-of timestamp, feature-cut timestamp, and request timestamp;
- identity and relationship state;
- decision context;
- candidate action, candidate-action ID, and option-grid structure where
  applicable;
- product terms;
- current card/account state;
- historical transactions and payments;
- bureau/risk variables;
- deposits and relationship variables;
- rewards and fees;
- servicing, fraud, disputes, collections;
- macro/scenario variables;
- downstream policy assumptions;
- data timestamp and feature availability stage.

State that the component should reject, warn, or degrade gracefully when a
caller submits inputs inconsistent with the declared decision context. Require
explicit training-serving feature-cut controls so prospect, applicant, booked,
and active-account calls cannot silently use unavailable or post-decision data.

### 7. Output Contract

Specify the full output schema:

- `request_id`, `trace_id`, `consumer_use_case_id`, schema version, model
  version, scenario version, and assumption-bundle version;
- expected incremental NPV;
- NPV by horizon;
- pre-tax and post-tax outputs where required;
- confidence/sensitivity range;
- component cash-flow breakdown;
- decomposition identifiers for downstream audit and reconciliation;
- activation/use/spend/balance/loss paths;
- PD/LGD/EAD and expected loss;
- rewards, servicing, fraud, funding, capital, tax/accounting;
- cannibalization estimate;
- relationship/deposit value only where justified;
- key drivers and explanation fields;
- warnings/low-confidence flags;
- no-score, degraded-score, out-of-domain, and manual-review statuses;
- model, scenario, and policy-assumption metadata.

Make clear that consuming systems may use different decision rules, but should
consume the same governed NPV object.

### 8. Internal Modeling Architecture

Translate the literature survey into build components:

- lifecycle state model;
- activation and usage module;
- spend/category module;
- balance/payment/revolve module;
- line utilization/EAD module;
- PD/LGD/EAD loss module;
- rewards/fees/interchange module;
- servicing/fraud/disputes/collections module;
- funding/capital/tax module;
- attrition/dormancy/terminal-value module;
- causal lift/cannibalization layer;
- scenario and sensitivity engine.

For each module state inputs, outputs, modeling method candidates, and
validation diagnostics.

### 9. Integration Architecture

Describe how the component plugs into existing systems without owning them.

Require three concrete operating modes:

1. single-request online scoring;
2. batch portfolio scoring;
3. multi-option grid scoring for line, offer, product, or treatment alternatives.

For each operating mode specify:

- caller systems and typical use cases;
- SLA and latency expectations;
- feature freshness rules;
- failure handling and fallback behavior;
- idempotency requirements;
- audit logging and lineage;
- rollback path;
- whether fallback can use the current component, a conservative no-score, or
  manual review.

Include at least one compact request/response example for online scoring and
one compact request/response example for batch or multi-option scoring.

Also include:

- batch scoring for marketing;
- real-time or near-real-time scoring for decisioning where required;
- option-grid scoring for line assignment and offer design;
- portfolio aggregation interface for finance/reporting;
- feature store/data lake dependencies;
- model registry and version pinning;
- monitoring feeds.

Discuss failure modes:

- unavailable features;
- stale bureau data;
- missing transaction history;
- scenario mismatch;
- policy-assumption mismatch;
- caller uses wrong decision context.
- inconsistent feature availability across funnel stages;
- training-serving skew from different as-of joins;
- duplicate household/customer identities across systems;
- offline/online feature parity breaks;
- incompatible legacy enumerations or field definitions;
- inability to reconstruct inputs later for audit, model review, or dispute
  review.

### 10. Practical Pitfalls and Controls

This should be one of the longest sections. Cover:

- NPV is latent and assumption-sensitive;
- populations differ across the funnel;
- the counterfactual changes by decision;
- one model cannot ignore feature availability timing;
- new-card spend can cannibalize old bank-card spend;
- rewards/promotions can create high spend and negative value;
- line changes affect usage and EAD simultaneously;
- terminal value can dominate rankings;
- downstream policy changes invalidate upstream NPV;
- finance, risk, marketing, and model-risk teams may define profit differently;
- fairness/compliance constraints may limit how outputs can be used;
- uncertainty should be reported, not hidden.

For each pitfall, specify a component-level control.

### 11. Validation, Monitoring, and Governance

Separate five governance lenses:

1. predictive model validation;
2. causal/treatment validation where actions change outcomes;
3. finance-definition and decomposition reconciliation;
4. data-quality and integration monitoring;
5. use-case approval and change control.

For each lens require:

- explicit veto diagnostics;
- escalation thresholds;
- reapproval triggers;
- monitoring cadence;
- named owners.

Define validation by use case:

- marketing: randomized holdout incremental NPV;
- underwriting: booked-account outcomes, approval selection, loss calibration;
- line assignment: utilization, spend lift, EAD/loss response;
- offer design: reward cost, promo decay, cannibalization;
- account management: retention, attrition, forward value.

General validation:

- vintage backtests;
- component calibration;
- stress/scenario testing;
- sensitivity testing;
- challenger models;
- segment stability;
- fairness/compliance review;
- model-risk documentation;
- decision-impact analysis.

Add explicit governance rules:

- approval is use-case specific; marketing validation does not automatically
  approve underwriting, line assignment, or account-management use;
- the proposal must state how outputs may and may not be used in credit
  decisions;
- explanation support from the NPV component is not the same as adverse-action
  reasoning unless specifically validated and approved;
- caller systems remain responsible for separate adverse-action, fair-lending,
  and compliance processes where required.

### 12. Migration from the Current Component

Define phases:

1. inventory current consumers and schema;
2. reconstruct current NPV definition;
3. build compatibility wrapper;
4. run shadow scoring;
5. perform ranking comparisons;
6. perform segment-level aggregate NPV tie-outs;
7. perform decomposition-level tie-outs by major cash-flow component;
8. compare assumption bundles and valuation conventions;
9. analyze disagreements by use case and segment;
10. calibrate component outputs;
11. define legacy-output retirement rules;
12. run downstream contract tests;
13. controlled cutover by use case;
14. post-cutover monitoring and fallback.

Require explicit rollback triggers and a named rollback owner. State historical
replay limitations when old features, old assumptions, or old policy states
cannot be reconstructed.

### 13. Implementation Roadmap

Propose phases:

- Phase 0: discovery and current-state inventory.
- Phase 1: valuation policy, data contract, and output schema.
- Phase 2: first acquisition/marketing component MVP with holdout validation.
- Phase 3: balance/loss/PPNR component expansion.
- Phase 4: line/offer option-grid support.
- Phase 5: account-management and conversion support.
- Phase 6: production hardening, model-risk approval, migration.

Each phase should include deliverables, acceptance criteria, risks, and approval
gates. Required gates:

- contract signoff;
- finance-definition signoff;
- model-risk signoff;
- compliance/fair-lending signoff where applicable;
- integration signoff;
- controlled-consumer cutover signoff.

### 14. Deliverables and Acceptance Criteria

List concrete deliverables:

- technical specification;
- data contract;
- API/schema contract;
- model methodology document;
- validation report;
- integration map;
- monitoring design;
- migration plan;
- model-risk package;
- literature appendix.

Acceptance criteria should be testable.

Include hard contract tests, at minimum:

- schema validation passes for every declared operating mode;
- component decomposition sums back to reported NPV within tolerance;
- identical replay inputs reproduce the same governed output object for a fixed
  model and assumption bundle;
- no-score/degraded-score states are returned rather than silent malformed
  values when required inputs are missing;
- downstream contract tests pass for each controlled consumer before cutover.

### 15. Literature Support Appendix

Summarize how the existing literature survey supports the design:

- direct marketing and CLV support discounted contribution;
- causal/uplift literature supports counterfactual lift;
- payment-choice literature supports adoption vs usage;
- household-finance evidence supports macro/employment state dependence;
- credit risk literature supports PD/LGD/EAD;
- dynamic policy literature supports downstream policy assumptions.

Do not let this appendix dominate the proposal.

## Review process for this writing plan

Use Claude Code as a bounded critic. For each round:

1. Ask Claude to identify material gaps, over-scope, missing sections,
   organization problems, and implementation-risk blind spots.
2. Require Claude to return:
   - `DECISION: ACCEPT` or `DECISION: REVISE`;
   - ranked material findings;
   - precise edits required;
   - what not to change.
3. If `REVISE`, update this plan and append a review-log entry.
4. Stop when Claude returns `ACCEPT` or after 10 rounds.

## Proposal drafting process

After the plan is accepted:

1. Create a standalone LaTeX proposal directory.
2. Reuse bibliography entries from the literature survey where appropriate.
3. Write for a senior bank audience: practical, structured, and specific.
4. Keep the boundary clear in every major section.
5. Include tables for decision contexts, input/output contract, modules,
   pitfalls/controls, validation, and roadmap.
6. Compile the proposal PDF and scan for LaTeX errors, undefined citations, and
   overfull boxes.

## Final-document review and rewrite loop

After drafting:

1. Review the full document for organization, readability, consistency, and
   cohesiveness.
2. Create a rewrite plan under `docs/plans` if any material issue is found.
3. Review the rewrite plan with Claude using the same bounded review process
   and stop at `ACCEPT` or 10 rounds.
4. Execute the rewrite plan.
5. Rebuild and rescan the document.
6. Repeat the review/rewrite loop until no material rewrite suggestions remain
   or after 10 full-document rewrite cycles.

## Completion criteria

- Writing plan accepted by Claude or 10 plan-review rounds completed.
- Proposal drafted as a standalone buildable LaTeX document.
- Final proposal reviewed internally and by Claude-assisted rewrite-plan loop.
- Final PDF builds without fatal errors, undefined references/citations, or
  overfull boxes.
- Final answer reports review rounds, files created, and verification results.
