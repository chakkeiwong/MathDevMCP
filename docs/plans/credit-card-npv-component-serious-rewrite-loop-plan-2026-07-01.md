# Credit card NPV component serious rewrite loop plan

Date: 2026-07-01

Target document:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

## Objective

Perform a real restructuring of the credit-card NPV component proposal, not a
cosmetic bridge pass. The current proposal preserves the literature survey and
contains many useful operating details, but the main body still reads like a
survey followed by a specification. The improved report should read as a
human-facing proposal for replacing one bank component: the NPV valuation
component. Literature, equations, component design, data requirements,
validation, integration, migration, and governance should be woven together.

## Skeptical plan audit

- **Wrong baseline risk:** The baseline is the current 42-page proposal plus
  the preserved literature survey and prior component plans. Do not start from
  a blank short memo.
- **Compression risk:** Do not delete the evidence base merely to improve
  readability. Dense operating material may move to an appendix, but the
  substantive mechanisms and equations must remain.
- **Scope risk:** Do not expand into building the campaign platform,
  underwriting engine, finance ledger, stress platform, account-management
  platform, rewards system, collections workflow, or reporting platform. The
  component owns valuation, decomposition, assumptions, outputs, lineage,
  validation evidence, and migration artifacts.
- **Proxy-metric risk:** Do not let response, approval, activation, first use,
  first-90-day spend, schema completeness, or table coverage become the
  objective. The objective remains incremental risk-adjusted NPV under a
  declared counterfactual and valuation-semantics bundle.
- **Evidence risk:** Public literature supports mechanisms and model structure.
  Bank-specific activation rates, cannibalization, spend elasticity, payment
  response, loss elasticity, funding/capital allocation, and terminal-value
  parameters require internal data, experiments, or approved assumptions.
- **Readability risk:** The user explicitly objected to dense tables. Main-body
  tables must be short and explanatory. Schema-like longtables belong in a
  reference appendix.
- **Audit risk:** Do not declare success because the PDF builds. The audit must
  check structure, integration, table readability, claim support, scope, and
  decision-use clarity.

## Rewrite architecture

The rewritten proposal should have this main-body spine:

1. Executive summary and component charter.
2. What the replacement component must estimate.
3. Why card NPV is difficult and decision-specific.
4. Evidence-grounded component architecture.
5. Module chapters, each using the same pattern:
   - literature/supervisory support;
   - mathematical model slot;
   - internal bank data required;
   - NPV output implication;
   - validation and veto diagnostics.
6. Decision contexts and valuation semantics.
7. Integration with existing bank systems.
8. Migration, governance, first production slice, and open empirical questions.
9. Source-support and claim-support audit.
10. Appendices for dense operating contracts.

## Module chapters to create or strengthen

1. Spend, macro, and employment state dependence.
2. New-card adoption, activation, use, rewards, and cannibalization.
3. Lifetime state, attrition, dormancy, and terminal value.
4. Balances, payments, credit line, promo balances, and cash advances.
5. Losses: PD, LGD, EAD, principal/non-principal subledgers, vintage and
   months-on-book.
6. PPNR, rewards, funding, capital, tax, cost, fraud, servicing, and
   relationship spillovers.
7. Sequential policy dependence and downstream assumptions.

## Dense material policy

Move or reframe the following as appendices or compact reference sections:

- decision-context longtables;
- valuation-semantics table;
- request contract table;
- response contract table;
- score-status table;
- operating-mode table;
- governance and migration artifact tables.

The main body may retain short prose summaries and small summary lists. The
appendices can retain implementation detail.

## Loop process

For each iteration, up to five:

1. Write the iteration goal and planned edits in this file.
2. Execute the edit in the TeX source.
3. Build the PDF with `latexmk`.
4. Audit against the criteria below.
5. If material gaps remain, write the next iteration goal and repeat.

## Audit criteria

The audit fails if any of the following remain materially true:

- The first half and second half still read like separate documents.
- The main body is dominated by unreadable dense tables.
- A module lacks one of: evidence, model slot, bank data, output implication,
  or validation/veto.
- The document implies public literature supplies issuer-specific parameters.
- The component boundary drifts into owning caller-system actions.
- Decision contexts and counterfactuals are unclear or treated as one NPV.
- Migration and governance are only checklist-like and not tied to replacement
  risk.
- The source-support section lacks a claim-support discipline.
- The PDF fails to build, has undefined citations/references, or has fatal
  LaTeX errors.

## Iteration log

### Iteration 1 plan

Restructure the main body without deleting the evidence base:

- add a new section, `Integrated Design of the Replacement NPV Component`,
  before the detailed literature sections;
- make this section the main human-readable proposal spine;
- add module subsections for the seven module chapters above;
- explicitly connect each module to evidence, bank data, output fields, and
  validation;
- reframe the later operating specification as a reference contract appendix;
- add `\appendix` before the dense operating-contract material, preserving the
  detail while removing it from the main-body narrative;
- add a source/claim-support section that is explicitly an audit artifact, not
  a casual bibliography table.

### Iteration 1 audit

Decision: PASS WITH NON-BLOCKING POLISH.

Build result:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`
  succeeded.
- Output PDF: 47 pages.
- Final log scan found no fatal errors, undefined references, undefined
  citations, or overfull boxes. Remaining warnings are underfull boxes from
  tables and bibliography entries.

Audit against criteria:

- **First half / second half disjointness:** Passed materially. The new
  `Integrated Design of the Replacement NPV Component` section gives the
  proposal a component-design spine before the detailed evidence sections. The
  later `Using the Component in Existing Bank Decision Processes` section now
  explains how the design enters caller systems in prose before the reference
  appendix.
- **Dense main-body tables:** Passed materially. The large implementation
  contract longtables now begin only after `\appendix`. Four short main-body
  summary tables remain because they summarize evidence-to-model, component
  outputs, and decision counterfactuals; they are not the dominant reader path.
- **Module completeness:** Passed. The seven integrated module subsections each
  state mechanism/evidence, component requirement, internal bank data or
  approval need, output implication, and validation or veto implication.
- **Public-literature overclaiming:** Passed. The new design section and
  claim-support ledger repeatedly state that issuer-specific activation,
  cannibalization, spend elasticity, payment response, loss elasticity, and
  terminal-value parameters require bank data or experiments.
- **Component boundary:** Passed. The main-body decision-use section and
  appendix continue to state that caller systems own action selection and
  execution.
- **Decision contexts and counterfactuals:** Passed. The proposal now explains
  targeting, cross-sell, underwriting, line assignment, retention, product
  conversion, and promotional treatment as distinct contrasts.
- **Migration and governance narrative:** Passed. The new main-body migration
  section now explains inventory, valuation-definition comparison, shadow
  scoring, disagreement registers, cutover by consumer/context, governance
  questions, and rollback.
- **Claim-support discipline:** Passed materially. A claim-support ledger was
  added before the source-by-source ledger.

Non-blocking polish:

- The detailed evidence sections still retain a few compact tables. They are
  acceptable as summary aids, but a later editorial pass could convert one or
  two of them to prose if the target audience strongly dislikes tables.
- The source-support audit still truthfully says that full technical-section
  checking, retraction checks, citation metadata, and backward/forward
  snowballing remain open. That is a research-audit limitation, not a defect in
  this restructuring loop.

Loop decision:

- No material gap remains under the loop acceptance criteria. Stop after
  iteration 1 rather than performing needless churn.
