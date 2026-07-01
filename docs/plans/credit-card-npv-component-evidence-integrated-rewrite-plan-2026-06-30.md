# Credit card NPV component evidence-integrated rewrite plan

Date: 2026-06-30

Target document:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

Evidence source to integrate:
`docs/credit-card-npv-survey/credit_card_customer_npv_survey.tex`

## Objective

Rewrite the component proposal as a human-readable, evidence-grounded report.
The prior proposal has useful implementation material, but the main body is too
table-heavy and the literature survey is not integrated into the argument. The
rewrite should use the existing literature survey as the evidence spine and
move dense contract artifacts into appendices.

## Skeptical audit before execution

- **Wrong baseline risk:** Do not compare the rewrite against a blank page. The
  baseline is the existing proposal plus the existing literature survey.
- **Proxy-metric risk:** Do not let response, approval, activation, first spend,
  or schema completeness become the promotion criterion. The business object
  remains incremental risk-adjusted NPV.
- **Scope risk:** Do not expand into building campaign platforms,
  underwriting engines, finance ledgers, stress systems, or reporting
  platforms. The work is the replacement NPV component.
- **Evidence risk:** Do not make claims that the public literature does not
  support. Each important claim must be grounded in literature, regulatory
  source, project derivation, or explicitly marked as requiring internal bank
  data.
- **Readability risk:** Tables in the main body must summarize arguments, not
  carry them. Dense schemas and implementation checklists belong in appendices.
- **Stop condition:** Stop when the PDF builds and the main report reads as a
  prose-led argument with evidence integrated into each design section.

## Evidence integration map

1. Survey introduction and equations become the proposal's problem definition:
   incremental risk-adjusted NPV, not response, approval, activation, or raw
   spend.
2. Survey market-condition section supports spend, payment, balance, and macro
   scenario requirements.
3. Survey new-card-use section supports separate activation, first use,
   repeated use, wallet-share, rewards, and cannibalization modules.
4. Survey CLV section supports lifetime horizon, active/dormant state,
   attrition, and terminal-value treatment.
5. Survey component decomposition section supports losses, balances, PPNR,
   principal/non-principal subledgers, rewards, fraud, servicing, funding,
   capital, taxes, and relationship spillovers.
6. Survey decision-pitfalls section supports decision-context counterfactuals,
   funnel population changes, latent NPV uncertainty, and downstream policy
   dependence.
7. Survey validation section supports internal data requirements, randomized
   holdouts, quasi-experimental lift, vintage validation, and stress/scenario
   validation.
8. Survey source-support audit becomes the basis for a proposal evidence
   appendix and claim-support language.

## New report structure

1. Executive Summary
2. What The Component Must Estimate
3. Evidence Base And Literature Integration
4. Evidence-To-Design Consequences
5. NPV Definition And Valuation Policy
6. Component Architecture
7. Decision Contexts And Counterfactuals
8. Data, Experiments, And Validation
9. Integration With Existing Bank Systems
10. Migration And First Production Slice
11. Limits, Open Empirical Questions, And Governance
12. Appendices for implementation details and evidence ledger

## Table policy

Main-body tables must be short, explanatory, and introduced by prose. Use at
most four columns in the main body. Move the prior large tables for request
schema, response schema, score-status contract, operating modes, governance
lenses, and migration artifacts into appendices.

## Claim support policy

Use the following labels in prose where helpful:

- Literature evidence.
- Regulatory or supervisory source.
- Internal bank data required.
- Proposed design convention.

Do not claim that any public paper supplies this bank's activation rate,
cannibalization rate, spend elasticity, loss elasticity, or NPV parameter.

## Rewrite steps

1. Replace the abstract and executive summary with a prose-led framing.
2. Add a substantive literature/evidence section that integrates the existing
   survey rather than merely citing it.
3. Rewrite design sections using the pattern:
   claim, evidence, design implication, internal data requirement.
4. Preserve the useful equations from the survey and proposal:
   incremental NPV, cash-flow identity, state transition, PD/LGD/EAD, stock-flow
   balance identity, and dynamic policy value.
5. Preserve the component-only boundary.
6. Move dense implementation contracts into appendices.
7. Build the PDF with `latexmk`.
8. Review for evidence defensibility and readability.

## Acceptance criteria

- Main body contains a real integrated literature/evidence section.
- Main body has no large schema-style tables.
- Each major module states why it is needed, what evidence supports it, what
  the bank must estimate internally, and how it feeds NPV.
- Proposal still says the NPV component is not the caller system.
- Dense implementation material remains available in appendices.
- PDF builds with no fatal LaTeX errors or undefined citations/references.
