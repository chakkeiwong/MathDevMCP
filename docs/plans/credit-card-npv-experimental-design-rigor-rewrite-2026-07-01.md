# Credit Card NPV Experimental Design Rigor Rewrite Plan

Date: 2026-07-01

## Objective

Rewrite the `Practical Experimental Design Program` section in
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
so it is a defensible measurement framework for the NPV component rather than
a high-level program memo.

## Problem Diagnosed

The current section names useful experiment families, but it is still too
handwavy for a technical panel. It does not yet state enough:

- design-specific estimands;
- identification assumptions;
- distinction between ITT, take-up/complier, and conditional effects;
- power and minimum-detectable-effect discipline;
- contamination and interference controls;
- horizon and terminal-value discipline;
- rules for how experimental evidence updates the NPV component;
- limits on what can be concluded from each experiment.

## Rewrite Plan

1. Replace the opening of the section with a formal evidence-production
   framework using potential outcomes and the proposal's existing NPV notation.
2. Add an explicit separation between primary NPV estimands and module-level
   diagnostic estimands.
3. Add design families with equations:
   - contact/suppress acquisition holdouts;
   - existing-client new-card cannibalization holdouts;
   - reward, promotion, APR, and line experiments;
   - activation and onboarding experiments;
   - retention, dormancy, and reactivation experiments;
   - relationship-spillover holdouts;
   - quasi-experiments for policy, macro, and geographic shocks.
4. Add identification requirements and failure modes for each design family,
   anchored to causal-inference literature already cited in the proposal.
5. Add power, MDE, cluster, rare-loss, compliance, and horizon rules.
6. Add a promotion rule that says exactly when an experiment can upgrade a
   module from diagnostic or policy-conditional evidence to causal incremental
   NPV evidence.
7. Update the appendix evidence contract so it captures the new formal fields
   without turning the main section into a dense table.
8. Rebuild the LaTeX document and audit for unresolved references/citations,
   LaTeX errors, and obvious readability regressions.

## Skeptical Plan Audit

Wrong baseline risk: The section might imply the NPV component runs
experiments. Mitigation: state that caller systems run experiments; the NPV
component consumes their evidence and metadata.

Proxy-metric risk: Response, activation, or short-horizon spend might be
treated as NPV evidence. Mitigation: require a primary NPV estimand or a stated
module-to-NPV bridge; proxies are explanatory unless pre-specified as module
estimands with reconciliation.

Hidden assumption risk: Causal language could be used without stating
assignment, overlap, exclusion, pre-trends, or transport assumptions.
Mitigation: each design family gets explicit assumptions and veto diagnostics.

Power risk: Experiments can be powered for response but not for NPV, losses,
cannibalization, or relationship spillovers. Mitigation: require MDE and
cluster/horizon fields in the evidence contract.

Evidence risk: Literature can support method and mechanism, but not this
bank's issuer-specific parameters. Mitigation: state this boundary repeatedly
and require internal experimental or quasi-experimental anchors for production
promotion.

Artifact risk: Adding more prose without integration rules would still be weak.
Mitigation: include a mechanical update rule for evidence grade, allowed-use
label, model priors/posteriors, and scenario status.

Decision: the plan passes. Execute the rewrite and verify with a LaTeX build.

## Post-Execution Audit

Execution date: 2026-07-01.

Files changed:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.pdf`
- `docs/plans/credit-card-npv-experimental-design-rigor-rewrite-2026-07-01.md`

What changed in the proposal:

1. Rewrote `Practical Experimental Design Program` as a measurement framework
   rather than a program memo.
2. Added formal experiment-level NPV, ITT, LATE/complier, acquisition,
   cannibalization, offer-cell, onboarding, retention, relationship-spillover,
   and DiD/event-study estimands.
3. Added a new `Analysis specifications, not just experiment names` subsection
   with constructed experimental value outcomes, ANCOVA/stratified randomized
   analysis, IPW design contrasts, multi-arm offer regressions, encouragement
   first-stage/reduced-form discipline, RD local specification, event-study
   specification, and policy-value estimation for targeting rules.
4. Added identification assumptions and veto diagnostics for randomization,
   observational adjustment, RD, DiD/event studies, IV/encouragement, and
   selection correction.
5. Added power/MDE and cluster design-effect equations, plus rare-loss and
   horizon-bridge discipline.
6. Added an evidence tuple and mechanical promotion rule for how experimental
   evidence updates the NPV component and when the aggregate output must remain
   policy-conditional, diagnostic, or scenario NPV.
7. Expanded the appendix experimental evidence contract with assignment
   probability, treatment receipt/take-up, estimand class, power/MDE, tail
   bridge, contamination/interference, NPV decomposition, finance/risk
   reconciliation, transport boundary, and `what is not concluded`.

Audit against the original weakness:

- Not just prose: the section now includes explicit equations and estimators.
- Not just experiment names: each design family states the target estimand and
  the inference boundary.
- Not proxy-driven: response, activation, first use, and short-horizon spend are
  explicitly labeled diagnostics unless bridged into NPV.
- Not platform scope creep: the text states that caller systems run experiments
  and the NPV component consumes evidence and metadata.
- Not overclaiming: literature supports mechanisms and methods; issuer-specific
  parameters still require internal randomized, quasi-experimental, or
  explicitly downgraded observational evidence.

Build verification:

- Command run from `docs/credit-card-npv-component-proposal`:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`
- Result: successful PDF build.
- Output: `credit_card_npv_component_proposal.pdf`, 80 pages, 589,397 bytes.
- Log check found no LaTeX errors, fatal stops, undefined citations, undefined
  references, multiply defined labels, or rerun-required warnings after the
  final build pass.
- Residual typography warnings are pre-existing table/URL/line-break issues
  plus the small overfull `\hbox` warning around line 1004.

Decision: the handwavy experimental-design gap is materially reduced. The next
review should focus on whether the proposed estimands and diagnostics are the
right bank operating standard, not on whether the section lacks substance.
