# Credit card NPV component integration improvement plan

Date: 2026-07-01

Target document:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

## Objective

Improve the current full-depth proposal without compressing it. The current
version preserves the literature survey and includes a real operating
specification, but it still reads too sequentially: first a literature survey,
then a component specification. The next improvement should integrate the two
halves by restoring the strongest ideas from the previous discussion as an
explicit evidence-to-design spine.

The goal is not to add another platform architecture. The bank is replacing the
NPV component only. The improved document should make clear how the component
plugs into existing caller systems while preserving decision-specific
counterfactuals, valuation semantics, decomposed outputs, status handling,
validation, and migration controls.

## Skeptical audit before execution

- **Wrong baseline risk:** The baseline is the current 39-page full-depth
  proposal plus the prior plans and review log, not the earlier 18-page memo or
  a blank paper.
- **Compression risk:** Do not remove the preserved literature body. Integration
  means adding bridge text and restructuring local handoffs, not deleting
  evidence.
- **Scope risk:** Do not propose building a campaign platform, underwriting
  engine, finance ledger, stress platform, account-management platform, or
  reporting platform. The component owns valuation; callers own action
  selection and execution.
- **Proxy-metric risk:** Do not let response, approval, activation, first use,
  first-90-day spend, schema completeness, or table coverage become the target.
  The object remains incremental risk-adjusted NPV.
- **Evidence risk:** Public literature can support mechanisms and model
  structure. It cannot supply this bank's activation rate, cannibalization
  rate, spend elasticity, loss elasticity, cost allocation, or terminal-value
  parameter. Mark those as internal-data or experiment requirements.
- **Readability risk:** The user has objected to dense tables. Do not add new
  large tables. Use prose and, where helpful, short enumerated obligations.
- **Stop condition:** Stop after the proposal has explicit cross-links from
  evidence to component requirements, builds cleanly, and no fatal LaTeX or
  undefined citation/reference errors remain.

## Material from the previous discussion to restore or strengthen

1. **The five consultant issues as front-door motivation.** NPV is latent and
   assumption-sensitive; card value is heterogeneous; the scored population
   changes through the funnel; objectives and counterfactuals change by
   decision; decisions are interdependent over time.
2. **Decision-specific counterfactuals.** Targeting, cross-sell, underwriting,
   line assignment, activation, retention, product conversion, and account
   management need separate populations, feature stages, baselines, action
   sets, and approval boundaries.
3. **Component-only charter.** The NPV component owns valuation,
   decomposition, model methodology, assumptions, outputs, validation evidence,
   versioning, and lineage. Caller systems own campaign, credit, servicing,
   finance, stress, reporting, and execution responsibilities.
4. **Bank-native decomposition.** Losses, balances/activity, PPNR, and
   cost/control overlays should be presented as one auditable model
   architecture, not a list of loosely related bank terms.
5. **Adoption and usage funnel.** Offer response, application, approval,
   booking, activation, first use, repeated use, wallet share, cannibalization,
   dormancy, attrition, and charge-off should remain separate.
6. **Lifetime state model.** The lifetime section should lead naturally into the
   component's state-transition architecture.
7. **Evidence-to-design pattern.** Each main literature block should state:
   what the literature supports, what component requirement follows, what bank
   data are required, what output fields are affected, and what validation is
   needed.
8. **Valuation semantics.** Horizon, terminal value, discounting, funding,
   capital, tax, cost, rewards, relationship value, cannibalization, scenario,
   and downstream-policy assumptions must be versioned and visible in outputs.
9. **Request/response/status semantics.** The operational contracts should be
   framed as protections against misuse of the NPV number, not as a platform
   build.
10. **Migration and governance.** Shadow scoring, ranking comparisons, segment
    tie-outs, decomposition tie-outs, disagreement analysis, contract tests,
    use-case approvals, and rollback triggers are required because this
    replaces an existing component.

## Execution steps

1. Add a short executive "reader spine" after the first production slice that
   lists the five hard facts about card NPV and states that they drive the
   rest of the proposal.
2. Add a subsection in the replacement-boundary section called
   `Evidence-to-design spine`. This subsection will explain the recurring
   pattern: literature mechanism, component requirement, bank data, output
   implication, and validation implication.
3. Add short "Implication for the NPV component" paragraphs or subsections
   after the macro, usage/cannibalization, lifetime, architecture, and
   decomposition blocks. These should cross-reference the later operating
   specification.
4. Add a prose bridge before the operating specification explaining that the
   contracts are not generic API design; they are controls derived from the
   evidence body and the decision pitfalls.
5. Add a short "claim-support discipline" paragraph before the source-support
   audit explaining how each important design claim should be supported in
   future model-risk materials.
6. Build the PDF with `latexmk`.
7. Scan the log for fatal errors, undefined references/citations, and overfull
   boxes.

## Acceptance criteria

- The proposal still preserves the literature evidence and does not shrink into
  a short memo.
- The proposal explicitly integrates the first half and second half through
  evidence-to-design bridge text.
- No new dense main-body tables are added.
- The component-only boundary remains clear.
- The restored previous ideas are present in prose-led form.
- The PDF builds with no fatal LaTeX errors, undefined references, or undefined
  citations.
