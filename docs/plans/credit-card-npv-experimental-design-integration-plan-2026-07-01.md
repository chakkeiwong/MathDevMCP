# Credit Card NPV Proposal: Experimental Design Integration Plan

Date: 2026-07-01

## Objective

Integrate the experimental-design read in
`docs/plans/credit-card-npv-experimental-design-read-2026-07-01.md` into
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`.
The goal is to turn the proposal's identification doctrine into an operational
experiment program for the NPV component.

## Scope

1. Add a main-body section titled `Practical Experimental Design Program`
   after `Identification, Endogeneity, and Data Strategy` and before
   `Module-Level Identification Plan`.
2. Explain why experiments are required for bank-specific NPV parameters even
   when the literature supports the economic mechanisms.
3. Add an experiment portfolio covering acquisition/prescreen holdouts,
   existing-client cannibalization holdouts, reward/promotion randomization,
   line/APR/term variation, activation/onboarding nudges, retention/reactivation
   experiments, relationship-spillover holdouts, and macro/geography/policy
   quasi-experiments.
4. Add concrete experiment-design cautions: power and minimum detectable
   effects, randomization unit, household/relationship-level contamination,
   holdout integrity, compliance/take-up, multiple testing, decision-stage
   feature cuts, legal/fair-lending constraints, and horizon discipline.
5. Add an evidence-contract template and a worked existing-client
   cannibalization contract in the proposal appendix.
6. Rebuild the PDF and record a post-execution audit.

## Non-Goals

- Do not claim that experiments alone establish five-year NPV.
- Do not claim that activation, first-use, response AUC, or short-horizon spend
  is sufficient for production promotion.
- Do not invent bank-specific sample sizes, MDE thresholds, power results,
  compliance approvals, legal approvals, or experiment outcomes.
- Do not add new literature claims beyond the current source-support status.
- Do not turn the proposal into a campaign-platform build; keep the scope as
  the NPV component's evidence requirements and consumption contract.

## Skeptical Plan Audit

Wrong-baseline risk: an experiment section could imply that the component owns
campaign execution. Mitigation: state that the component consumes experiment
metadata and evidence grades; caller systems run campaigns and actions.

Proxy-metric risk: experiment menus could promote response, activation, or
short-horizon spend instead of NPV. Mitigation: every experiment will name the
NPV estimand and identify proxy metrics as explanatory or veto diagnostics.

Hidden-assumption risk: experiment examples could read as approved bank
designs. Mitigation: describe them as design templates requiring product,
risk, legal/compliance, model-risk, and technology approval where relevant.

Evidence risk: literature citations support mechanisms and methods, not this
bank's parameters. Mitigation: explicitly separate mechanism support from
issuer-specific experimental evidence.

Operational-risk gap: experiments can fail through contamination, weak power,
holdout loss, noncompliance, or bad feature timing. Mitigation: include these
as required design checks and veto diagnostics.

Artifact risk: adding only prose would not make the component contract
actionable. Mitigation: add appendix evidence-contract and ledger fields that
the component must ingest and return.

Decision: the plan passes. Execute the scoped integration.

## Post-Execution Audit

Execution date: 2026-07-01.

The proposal was updated to include a dedicated experimental-design section
and an appendix evidence contract.

Main-body changes:

1. Added `Practical Experimental Design Program` after
   `Identification, Endogeneity, and Data Strategy`.
2. Defined an experiment-level NPV estimand that ties each experiment back to
   the component's valuation object.
3. Added an experiment portfolio covering:
   - acquisition or prescreen holdouts;
   - existing-client new-card cannibalization holdouts;
   - reward and promotion-cell randomization;
   - line, APR, and promotional-term variation;
   - activation and onboarding-friction experiments;
   - retention, dormancy, and reactivation experiments;
   - relationship-value spillover holdouts;
   - macro, geography, and policy-change quasi-experiments.
4. Added explicit design cautions for power, contamination, holdout integrity,
   compliance and take-up, leakage, multiplicity, legal/fair-lending
   constraints, and horizon discipline.
5. Added evidence-contract and promotion-logic language so experiments feed the
   NPV component as governed evidence rather than as loose proxy metrics.

Appendix changes:

1. Added `Experimental evidence contract` under the operating specification.
2. Added a minimum ledger for experiment name, decision context, treatment and
   baseline, population, identification design, randomization unit, feature
   cut, primary estimand, horizon, veto diagnostics, explanatory diagnostics,
   allowed-use label, confounders addressed, confounders not addressed, and
   artifact location.
3. Identified the acquisition/prescreen holdout and the existing-client
   cannibalization holdout as the first contracts to write.

Build verification:

- Command run from `docs/credit-card-npv-component-proposal`:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`.
- Result: successful PDF build.
- Output: `credit_card_npv_component_proposal.pdf`, 76 pages, 553,719 bytes.
- Log check found no LaTeX errors, fatal stops, undefined citations, undefined
  references, multiply defined labels, or rerun-required warnings after the
  final build pass.
- Residual typography warning remains the same very small overfull `\hbox`
  warning (`0.52028pt`) around line 1004.

Follow-up decision: the proposal now has a concrete experimental-design layer
that a panel can inspect, and the component contract now records experiment
evidence explicitly. This closes the gap between identification theory and
issuer-specific parameter learning for the NPV component.
