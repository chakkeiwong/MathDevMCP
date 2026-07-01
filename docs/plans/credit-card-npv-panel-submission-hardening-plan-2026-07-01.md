# Credit Card NPV Component Proposal: Panel Submission Hardening Plan

Date: 2026-07-01

## Objective

Turn `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
from a strong but still accumulated technical draft into a panel-grade proposal
for a technically sophisticated review committee.

The goal is **not** to shorten the proposal. The goal is to make the proposal
more defensible, better architected, easier to navigate, and richer in the
places where a panel will press for substance: source support, notation,
bank-data feasibility, external-data usage, valuation semantics, experiment
contracts, and implementation detail.

## Explicit Non-Goal: Do Not Shrink the Proposal

Shorter is not a success criterion. The rewrite must preserve substantive
content unless a passage is duplicated, incorrect, or superseded by a stronger
version. Deletion must be justified in a relocation/removal ledger.

The target writing style is:

- rigorous enough for former academics, senior managers, model-risk reviewers,
  finance/risk owners, and implementation engineers;
- readable through prose, equations, examples, and schematics;
- not table-driven as the main exposition;
- expansive where detail is needed;
- well organized enough that the reader can find the relevant detail without
  reverse-engineering the drafting history.

## Accepted Remaining Gaps

This plan addresses the accepted gaps from the current proposal audit, excluding
the prior item about the panel ask, which is out of scope for this pass.

1. Source-support audit is incomplete.
2. The document feels accumulated rather than architected.
3. Notation needs a consistency audit.
4. Bank-specific data feasibility is underdeveloped.
5. External/public/Refinitiv data are listed but not operationalized.
6. Valuation semantics are principled but too abstract.
7. Experimental design lacks worked contracts.
8. Model implementation detail remains thin.
9. Some dense tables remain reader-hostile.

## Skeptical Plan Audit

Wrong baseline risk: A rewrite could repeat the earlier failure mode of
compressing a large survey and proposal into a short memo. Mitigation: maintain
a content preservation ledger and treat page-count shrinkage as a warning, not
a win.

Proxy-readability risk: The document could become "easier" by omitting hard
material. Mitigation: every simplification must either preserve the technical
argument in prose/equations or move detailed material to an appendix with a
clear pointer.

Evidence risk: The proposal could cite literature generically without checked
technical anchors. Mitigation: add a source-support workstream that records
paper sections/equations/tables/appendices and separates primary support,
project derivation, survey context, source gap, and bank-data requirement.

Implementation-handwaving risk: The proposal could state that the bank "must
estimate" many quantities without showing data feasibility or modeling workflow.
Mitigation: add bank data, external data, model implementation, and worked
experiment contract sections.

Organization risk: Adding more material can make the document more chaotic.
Mitigation: first define a target architecture, then move or expand content
according to that architecture. Do not add disconnected sections.

Decision: the plan passes. Execution should proceed as a structured hardening
rewrite, not a summary rewrite.

## Proposed Target Architecture

The revised proposal should read as one monograph with a clear spine:

1. **Executive Charter and Reader Map**
   - Component boundary.
   - What problem the NPV component solves.
   - What it does not own.
   - How to read the document.

2. **Valuation Object and Accounting Spine**
   - Incremental NPV object.
   - State space.
   - Wallet accounting.
   - Cash-flow decomposition.
   - Decision-context and counterfactual semantics.

3. **Evidence-Integrated Literature Foundation**
   - Macro, employment, liquidity, and spend.
   - Payment adoption, activation, usage, rewards, and cannibalization.
   - CLV, duration, attrition, and lifetime state modeling.
   - Credit risk, PD/LGD/EAD, PPNR, funding, capital, and accounting.
   - Each subsection should end with "how this enters the component."

4. **NPV Component Design**
   - Module architecture.
   - Module inputs and outputs.
   - Module dependencies.
   - Interaction between spend, balances, losses, rewards, attrition, funding,
     capital, and relationship value.

5. **Identification and Experimental Evidence**
   - Endogeneity and selection risks.
   - Practical experimental-design framework.
   - Worked acquisition/prescreen contract.
   - Worked existing-client cannibalization contract.
   - Evidence grades and allowed-use propagation.

6. **Data Strategy**
   - Internal bank data inventory.
   - External public data inventory.
   - LSEG/Refinitiv licensed data inventory.
   - Data lineage, vintages, entitlements, joins, timing, and feature cuts.

7. **Valuation Semantics and Assumption Bundles**
   - First-slice default valuation bundle.
   - Sensitivity bundles.
   - Funding, discounting, capital, tax, terminal value, rewards, costs,
     relationship value, and downstream policy.

8. **Model Implementation and Validation**
   - Baseline and challenger model classes.
   - Training base construction.
   - Monthly simulation or path construction.
   - Calibration and reconciliation.
   - Uncertainty propagation.
   - Formal validation gates.
   - Monitoring and refresh triggers.

9. **Operating Contract and Migration**
   - Request and response schema obligations.
   - Status semantics.
   - Operating modes.
   - Shadow testing.
   - Cutover gates.
   - Rollback.

10. **Appendices and Ledgers**
   - Source-support ledger.
   - Claim-support ledger.
   - Notation glossary.
   - Data inventory tables.
   - Experimental evidence contracts.
   - Dense tables moved here where they are useful as audit artifacts.

## Workstream 1: Content Preservation and Re-Architecture

### Tasks

1. Create a content preservation ledger before rewriting:
   - current section;
   - main ideas/equations/tables;
   - target section in new architecture;
   - keep, expand, merge, move to appendix, or remove;
   - reason for removal if any.
2. Reorder sections to match the target architecture.
3. Remove duplicated passages only when the stronger version is preserved.
4. Add transition paragraphs so the reader understands why one section follows
   the previous one.
5. Add a section-opening "reader promise" to major technical sections: what the
   section answers and what it does not answer.

### Acceptance Criteria

- No substantive topic from the current proposal disappears silently.
- The document is longer or roughly similar in length unless deletions are
  explicitly justified as duplicate/superseded.
- A reviewer can navigate from literature to model requirement to data need to
  validation gate.

## Workstream 2: Source-Support and Literature Hardening

### Tasks

1. Build a source-support ledger for all cited academic and regulatory sources:
   - citation key;
   - source class;
   - local/full-text status;
   - publication status;
   - inspected technical sections;
   - inspected equations/tables/appendices;
   - allowed claims;
   - forbidden claims;
   - retraction/erratum/version status;
   - remaining source gap.
2. Build a claim-support ledger organized by proposal claim:
   - claim;
   - support type: primary technical support, project derivation, bank-data
     requirement, design convention, survey context only, or source gap;
   - citation or derivation anchor;
   - what a reviewer could still challenge.
3. Add backward/forward snowballing notes for the most important seed papers:
   - direct marketing optimization;
   - CLV/customer equity;
   - liquidity/unemployment/spend;
   - payment choice and rewards;
   - credit-card regulation and credit risk;
   - causal inference/uplift;
   - RD/DiD/IV/selection/dynamic treatment regimes.
4. Add an omitted-paper risk register for famous or direct competitor methods.
5. Integrate only the most important source-support conclusions into the main
   prose; keep detailed ledgers in appendix.

### Acceptance Criteria

- Every important modeling claim has a source, derivation, or explicit
  bank-data requirement.
- No source is used to support more than it actually supports.
- The proposal clearly separates what the literature proves, what the project
  derives, and what the bank must estimate.

## Workstream 3: Notation Consistency Audit

### Tasks

1. Create a notation glossary near the beginning or as an appendix.
2. Audit overloaded symbols:
   - `Z` currently appears as lifecycle state and assignment;
   - `D` can mean default/delinquency and treatment received;
   - `S` can mean state, spend, or source component;
   - `P` can mean payment behavior or probability;
   - `H` appears as observed horizon and valuation horizon.
3. Rename symbols where needed:
   - lifecycle state could be `LState` or `\mathcal{Z}`;
   - randomized assignment could be `A^{assign}` or `R`;
   - treatment received could be `T`;
   - spend could use `Spend`;
   - scenario and valuation bundles should have stable notation.
4. Ensure all equations use consistent indices, horizons, and conditioning
   information.
5. Add a "notation conventions" paragraph before the first major equation.

### Acceptance Criteria

- No core symbol has two incompatible meanings in nearby sections.
- Experimental-design notation is compatible with valuation notation.
- A mathematically trained reviewer can trace the NPV functional from state
  transition to cash-flow decomposition to experiment estimand.

## Workstream 4: Internal Bank Data Feasibility

### Tasks

Add a substantive internal data section with prose plus a compact inventory.
It should cover:

1. Campaign and offer data:
   - eligibility;
   - exposure;
   - channel;
   - creative;
   - offer cell;
   - assignment probability;
   - suppress/holdout flags;
   - contact timestamp.
2. Application and underwriting data:
   - application attributes;
   - approval/decline/refer;
   - score bands;
   - policy rule;
   - line/APR/term assignment;
   - overrides.
3. Account and transaction data:
   - activation;
   - first use;
   - merchant category;
   - ticket size;
   - card-present/card-not-present;
   - digital wallet/card-on-file;
   - cash advance;
   - balance transfer.
4. Balance and payment subledgers:
   - principal purchase balance;
   - promotional balance;
   - balance-transfer balance;
   - cash-advance balance;
   - fees;
   - accrued interest;
   - payments;
   - credits;
   - charge-offs.
5. Risk and loss data:
   - delinquency state;
   - PD/LGD/EAD snapshots;
   - collections treatment;
   - hardship;
   - bankruptcy;
   - recovery;
   - charge-off sale.
6. Rewards, cost, fraud, and servicing:
   - earn/burn;
   - signup bonus;
   - statement credits;
   - servicing contacts;
   - disputes;
   - fraud losses;
   - marginal and allocated costs.
7. Relationship data:
   - deposits;
   - debit;
   - ACH/payroll signals where permitted;
   - other products;
   - digital engagement;
   - household/relationship graph.
8. Data risks:
   - survivorship;
   - post-treatment leakage;
   - missing holdout lineage;
   - stale or revised features;
   - inconsistent customer/account identifiers;
   - legal/permitted-use constraints;
   - data retention limits.

### Acceptance Criteria

- For every major NPV module, the proposal names plausible bank data sources,
  grain, timing, and key risks.
- The data section says what is observable, partially observable, latent, and
  model-imputed.
- Feature-cut and leakage rules are explicit.

## Workstream 5: Public, Official, and LSEG/Refinitiv Data Operationalization

### Tasks

Replace generic external-data discussion with an operational inventory. For
each source, state:

- source;
- example variables;
- frequency;
- geography;
- vintage/revision handling;
- module use;
- join key or aggregation path;
- whether it is scenario, control, benchmark, prior, or causal evidence;
- limitations and entitlements.

Sources to cover:

1. Federal Reserve Enhanced Financial Accounts.
2. Federal Reserve G.19 consumer credit.
3. Federal Reserve Z.1 Financial Accounts.
4. NY Fed Household Debt and Credit.
5. BLS LAUS and unemployment series.
6. BEA regional income and consumption proxies.
7. Census ACS demographics.
8. CFPB credit-card agreement/product data.
9. FRED/ALFRED real-time vintages.
10. LSEG/Refinitiv macro, rate, curve, issuer, competitor, market, and sector
    data available under license, subject to entitlement review.

### Acceptance Criteria

- External data are not presented as issuer causal evidence.
- Each source has a concrete use in a model module or validation process.
- Vintage handling is explicit for backtesting and scenario construction.
- LSEG/Refinitiv usage is conditioned on license, lineage, and permitted-use
  review.

## Workstream 6: Concrete Valuation Semantics

### Tasks

Expand the valuation semantics section into a concrete first-slice base case
plus sensitivities. Include:

1. Horizon:
   - monthly horizon;
   - observed window;
   - valuation horizon;
   - terminal-value convention.
2. Discounting:
   - discount curve source;
   - compounding;
   - currency;
   - valuation date.
3. Funding / FTP:
   - balance-sensitive funding charge;
   - revolver/transactor distinction;
   - scenario sensitivity.
4. Capital:
   - economic/regulatory/stress capital convention;
   - capital price;
   - exposure base;
   - constraint versus charge.
5. Tax:
   - pre-tax versus post-tax output;
   - first-slice default.
6. Rewards:
   - earn;
   - redemption;
   - breakage;
   - signup bonus;
   - teaser incentives.
7. Costs:
   - acquisition;
   - servicing;
   - fraud;
   - disputes;
   - collections;
   - marginal versus allocated cost.
8. Losses:
   - expected loss path;
   - principal/non-principal treatment;
   - charge-off and recovery timing.
9. Relationship value:
   - default excluded from core card NPV;
   - included only under separate causal evidence grade.
10. Downstream policy:
    - current-policy bundle;
    - target-policy bundle;
    - reapproval trigger when policy changes.

### Acceptance Criteria

- The section gives a concrete base case reviewers can debate.
- Sensitivity cases are explicit.
- The proposal does not pretend these are final bank policies; it presents them
  as governed conventions for the first production slice.

## Workstream 7: Worked Experimental Evidence Contracts

### Tasks

Add two worked examples after the experimental-design framework or in an
appendix, with prose first and compact contract tables second.

### Worked Contract A: Acquisition / Prescreen Contact-Suppress

Must include:

- decision context;
- population and eligibility;
- baseline and treatment;
- randomization unit;
- assignment probability;
- primary NPV estimand;
- module estimands;
- observed horizon and valuation horizon;
- MDE/power fields;
- constructed value outcome;
- required data fields;
- veto diagnostics;
- explanatory diagnostics;
- finance/risk reconciliation;
- allowed-use consequence;
- what is not concluded.

### Worked Contract B: Existing-Client New-Card Cannibalization

Must include:

- no-offer versus offer cells;
- all-bank spend lift;
- new-card spend lift;
- old-card cannibalization;
- debit/deposit substitution where observable;
- balance-transfer and payoff records;
- promotion decay;
- reward cost;
- loss and balance effects;
- relationship spillover excluded unless separately identified;
- NPV bridge;
- what is not concluded.

### Acceptance Criteria

- The examples show exactly how experimental evidence enters the NPV component.
- They make clear that response, activation, and new-card spend are not enough.
- They can be used as templates for future experiment ledgers.

## Workstream 8: Model Implementation Detail

### Tasks

Add a model-implementation section that is concrete but not prematurely
technology-specific. It should cover:

1. Analytic base construction by decision context:
   - prospect;
   - applicant;
   - approved/booked;
   - active account;
   - dormant/retention.
2. Baseline models:
   - transparent GLM/hazard/state-transition baselines;
   - scorecard/logit/survival models where appropriate;
   - finance reconciliation baselines.
3. Challenger models:
   - gradient boosting or other ML for prediction;
   - causal forests/uplift/DML for treatment effects where design supports it;
   - dynamic state models for lifetime paths.
4. Monthly path engine:
   - state transitions;
   - balance stock-flow identity;
   - spend/payment/loss/attrition dependencies;
   - downstream policy bundle.
5. Calibration:
   - horizon-level calibration;
   - vintage/months-on-book calibration;
   - segment calibration;
   - macro-regime calibration.
6. Reconciliation:
   - finance tie-out;
   - risk tie-out;
   - decomposition residual;
   - old-versus-new component comparison.
7. Evidence-grade propagation:
   - module evidence grade;
   - aggregate output label;
   - downgrade rules;
   - no-score and degraded-score rules.
8. Monitoring:
   - data drift;
   - treatment-policy drift;
   - macro drift;
   - calibration drift;
   - overlap/support drift;
   - finance/risk reconciliation drift.

### Acceptance Criteria

- A senior implementation engineer can see how the component would be built.
- A model-risk reviewer can see the baseline/challenger and validation path.
- The proposal remains component-scoped and does not become a platform build.

## Workstream 9: Table Readability and Appendix Strategy

### Tasks

1. Audit all tables:
   - main exposition table;
   - contract summary table;
   - appendix ledger;
   - dense audit artifact.
2. For every dense table:
   - add prose explanation before the table;
   - reduce columns if possible;
   - split into multiple tables if needed;
   - move audit-only ledgers to appendix.
3. Ensure no table is the first explanation of an important idea.
4. Add section summaries where tables are unavoidable.

### Acceptance Criteria

- A reader can understand each section by reading prose and equations before
  tables.
- Tables support completeness and auditability rather than carrying the main
  argument.
- Dense ledgers are clearly labeled as appendices.

## Execution Sequence

### Phase 0: Freeze and Inventory

1. Build current PDF and record page count.
2. Create content preservation ledger.
3. Create notation issue list.
4. Create table inventory.

Deliverables:

- `docs/plans/credit-card-npv-content-preservation-ledger-2026-07-01.md`
- `docs/plans/credit-card-npv-notation-audit-2026-07-01.md`
- `docs/plans/credit-card-npv-table-readability-audit-2026-07-01.md`

### Phase 1: Re-Architecture Skeleton

1. Reorder the document to target architecture.
2. Add transition prose.
3. Add "reader promise" paragraphs.
4. Preserve all material through moves, not deletion.

Deliverable:

- Rebuilt proposal with clean section order and no unexplained content loss.

### Phase 2: Evidence and Literature Hardening

1. Build source-support ledger.
2. Build claim-support ledger.
3. Add omitted-paper and snowballing risk register.
4. Integrate strongest support statements into main body.

Deliverables:

- Proposal source-support appendix expanded.
- Separate plan/audit file with literature ledger if the appendix becomes too
  large.

### Phase 3: Data and Semantics Expansion

1. Add internal bank data feasibility section.
2. Add public and LSEG/Refinitiv data operational inventory.
3. Expand valuation semantics into concrete first-slice base case and
   sensitivities.

Deliverable:

- Proposal section that a data owner, finance owner, and model-risk owner can
  review directly.

### Phase 4: Experiment Contracts and Implementation Detail

1. Add acquisition/prescreen worked contract.
2. Add existing-client cannibalization worked contract.
3. Add model implementation section.
4. Tie implementation details back to evidence grades and validation gates.

Deliverable:

- Proposal section that a modeler and implementation engineer can use as a
  build specification for the NPV component.

### Phase 5: Table and Readability Pass

1. Convert table-heavy exposition into prose-first explanation.
2. Move dense ledgers to appendices.
3. Add summaries before and after dense artifacts.
4. Verify no substantive material was lost.

Deliverable:

- More readable proposal with at least the same substantive coverage.

### Phase 6: Build and Review

1. Build LaTeX PDF.
2. Check unresolved references/citations.
3. Check page count and compare against baseline.
4. Run hostile panel-readiness audit:
   - source defensibility;
   - notation consistency;
   - data feasibility;
   - valuation semantics specificity;
   - experimental contract usefulness;
   - implementation specificity;
   - table readability;
   - content preservation.
5. Patch gaps found by the audit.

Deliverables:

- Updated PDF.
- Post-execution audit note under `docs/plans`.

## Review Loop

After each major phase:

1. Run a local self-audit against the acceptance criteria.
2. If Claude review is available, ask for a bounded read-only review focused on
   one phase at a time.
3. Patch only the gaps that improve rigor, organization, or defensibility.
4. Do not accept suggestions that merely shorten the document without preserving
   technical content.

Stop condition:

- No material gaps remain in the eight accepted gap areas, or
- the remaining gaps require bank-specific data, approvals, source access, or
  policy decisions unavailable to the proposal author.

## Final Acceptance Criteria

The hardening pass is successful only if all of the following are true:

1. The proposal is at least as substantive as the current version.
2. The section order is coherent and defensible.
3. Every major claim has source support, project derivation, or explicit
   bank-data requirement.
4. Notation is consistent enough for a technical reviewer.
5. Internal and external data use is operationally concrete.
6. Valuation semantics include a concrete first-slice base case and sensitivity
   cases.
7. At least two worked experiment contracts are included.
8. Model implementation is detailed enough to guide component design.
9. Tables support the argument instead of replacing it.
10. The LaTeX build is clean with no unresolved citations or references.

## Execution Note: 2026-07-01 Pass

This pass executed the remaining high-priority hardening tasks without
shrinking the proposal.

Added to
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`:

- `External data operational inventory`, converting the public/LSEG source list
  into operational model-use classes, vintage requirements, join paths,
  limitations, and entitlement cautions.
- `Concrete first-slice base case` and `Sensitivity and challenger bundles`
  under the valuation-semantics section, including a named first-slice bundle,
  monthly horizon logic, terminal-value formula, discount/funding separation,
  loss, capital, rewards, costs, relationship value, and downstream-policy
  conventions.
- `Model Implementation Blueprint for the Replacement Component`, covering
  decision-context analytic bases, baseline and challenger model classes,
  monthly path engine, cash-flow compiler, calibration, finance/risk
  reconciliation, evidence-grade propagation, monitoring, refresh triggers,
  and implementation artifacts.
- `Worked contract: acquisition or prescreen contact-suppress`, with
  estimand, constructed observed-horizon value, required records, analysis
  specification, veto diagnostics, allowed-use consequence, and non-claims.
- `Worked contract: existing-client new-card cannibalization`, with all-bank
  spend, old-card cannibalization, debit substitution, new-card spend, NPV
  bridge, required records, veto diagnostics, and non-claims.
- `Notation Glossary and Symbol Discipline`, documenting stable component
  notation and warning about inherited local overloads.
- Updated the reader map so valuation, data, experiment, model-risk, and
  engineering readers are directed to the new sections.

Current self-assessment before build:

- The document grew in substance rather than being compressed.
- The new sections are prose-first. Tables remain primarily contract or audit
  artifacts.
- Remaining risks are expected to be source-ledger completeness, unresolved
  LaTeX references if any, and the fact that bank-specific data access,
  finance policy, capital price, and experiment outcomes cannot be supplied by
  the proposal author.
