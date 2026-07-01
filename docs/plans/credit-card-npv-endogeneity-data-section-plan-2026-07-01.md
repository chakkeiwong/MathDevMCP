# Credit Card NPV Proposal: Endogeneity and Data Strategy Section Plan

Date: 2026-07-01

## Objective

Add an integrated proposal section explaining how the replacement credit-card
NPV component should handle endogeneity, confounding, selection bias, public
and licensed external data, and internal bank data. The section should be
grounded in the causal-inference, sample-selection, treatment-effect, panel,
and program-evaluation literature, and it should translate that literature into
concrete component requirements.

## Scope

This is not a plan for building a new platform. The output remains the NPV
component proposal. The new material should explain what the component must
request, preserve, estimate, validate, tag, and refuse to claim when the
evidence is weak.

## Execution Plan

1. Verify the current proposal structure, citation set, and source-support
   ledger so the new material can be integrated in the main body.
2. Check official source descriptions for the public and licensed data sources
   named in the new section, including Federal Reserve EFA, G.19, Z.1, NY Fed
   Household Debt and Credit, BLS LAUS, BEA regional accounts, Census ACS,
   CFPB credit-card data, FRED/ALFRED, and LSEG/Refinitiv sources.
3. Add bibliography entries for additional causal-identification references
   and data sources.
4. Insert a prose-led section, "Identification, Endogeneity, and Data
   Strategy," after empirical validation and before open gaps. It should cover:
   treatment assignment, funnel selection, endogenous product terms, dynamic
   policy feedback, macro confounding, public/licensed data use, internal data
   construction, and component gates.
5. Update the executive roadmap, open gaps, claim-support ledger, and
   source-support ledger.
6. Build the LaTeX document and inspect the log for undefined citations,
   undefined references, fatal errors, and serious overfull boxes.
7. Audit the revised document against the user's requirements A, B, and C.

## Skeptical Plan Audit

Potential wrong baseline: the section could accidentally treat predictive
accuracy as causal validity. Mitigation: explicitly separate prediction,
causal lift, and policy value; require holdouts or credible quasi-experiments
for incremental NPV claims.

Proxy-metric risk: activation, first spend, AUC, and portfolio correlations may
be tempting promotion criteria. Mitigation: identify them as diagnostics only
unless the decision objective is explicitly a proxy objective.

Hidden assumption risk: public macro and credit series could be presented as if
they identify customer-level treatment effects. Mitigation: state that external
data are scenario, benchmarking, and control inputs, not substitutes for
internal treatment variation.

Selection risk: booked or active-account data may be used for prospect,
applicant, or suppressed-population decisions. Mitigation: require preservation
of suppressed, declined, referred, approved, booked, and active populations
with decision-time snapshots.

Environment mismatch: the document is LaTeX and must compile. Mitigation:
patch TeX and BibTeX directly, then run `latexmk`.

Artifact adequacy: a standalone chat answer would not answer the user's need
for proposal material. Mitigation: edit the proposal and leave this plan as
the execution artifact.

Decision: the plan passes after these mitigations. Proceed with a main-body
section and ledger updates.

## Execution Note

Implemented in:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_refs.bib`

The proposal now includes a main-body section titled "Identification,
Endogeneity, and Data Strategy." It covers:

- why observed-outcome prediction is not causal incremental NPV;
- campaign selection, funnel selection, endogenous product terms, simultaneity,
  attrition, macro/geography confounding, and relationship-value confounding;
- randomized holdouts, encouragement designs, propensity and doubly robust
  methods, double/debiased ML, causal forests, regression discontinuity,
  difference-in-differences/event studies, sample-selection correction, and
  dynamic treatment-policy concerns;
- public data sources including Federal Reserve EFA/DFA, G.19, Z.1, NY Fed
  Household Debt and Credit, BLS LAUS, BEA regional accounts, Census ACS, CFPB
  credit-card data, and FRED/ALFRED;
- licensed LSEG/Refinitiv data categories, with entitlement and permitted-use
  cautions;
- internal data requirements and selection-safe construction;
- production metadata, evidence levels, and veto diagnostics for the NPV
  component.

## Post-Execution Audit

Requirement A: addressed. The new section identifies the major endogeneity,
confounding, leakage, survivorship, policy-feedback, and selection mechanisms
that affect the proposed submodels, and connects each to handling strategies
from the literature.

Requirement B: addressed. The proposal names useful public and licensed
external data sources and restricts their role to scenario construction,
controls, benchmarking, product/competitive context, priors, and monitoring
unless a separate causal design supports stronger use.

Requirement C: addressed. The proposal explains how internal bank data should
be used through a funnel-preserving analytic base, decision-time feature cuts,
randomization/holdout logs, historical policy logs, subledger detail, and
module-specific outcome construction.

Remaining caveat: this is still a proposal-level section. A future model
package should add a module-by-module identification appendix with the exact
estimand, eligible population, data table, treatment definition, diagnostic
thresholds, and approved use for each production submodel.
