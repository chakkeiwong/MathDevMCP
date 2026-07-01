# Credit Card NPV Proposal: Panel Remediation Execution Plan

Date: 2026-07-01

## Objective

Execute a panel-readiness remediation pass on
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`.
The goal is not to shorten the proposal. The goal is to make the technical
argument easier to follow, more explicit, and more defensible for a panel of
former academics, senior managers, and senior implementation engineers.

## Scope

This pass will keep the current proposal as the working document and add
missing technical substance where the current report is weakest:

1. Add a reader-navigation section that explains the argument architecture.
2. Add a more explicit valuation-object and decomposition section that
   distinguishes states, causal contrasts, forecasts, policy value, cash-flow
   identities, and wallet concepts.
3. Add module-level identification plans for response/activation, usage and
   spend source, cannibalization, balances/payments/line response, losses,
   rewards/promotions, attrition/conversion, and relationship spillovers.
4. Add an uncertainty-propagation section covering submodel uncertainty,
   scenario uncertainty, terminal value, funding/capital assumptions,
   cross-module dependence, and optimizer exploitation of model error.
5. Add more precise validation-gate formulas and threshold-setting logic.
6. Add a default valuation-semantics bundle that finance/risk/product owners
   can debate and amend.
7. Add an allowed-use taxonomy that connects output evidence grades to permitted
   and prohibited uses.
8. Strengthen the source-support appendix by explaining what is and is not yet
   panel-grade evidence.
9. Build the PDF and record a post-execution audit.

## Non-Goals

- Do not remove detail for brevity.
- Do not invent bank-specific data availability, baseline defects, thresholds,
  or approvals.
- Do not claim a full literature audit has been completed.
- Do not fetch live citation counts or citation-network metadata in this pass.
- Do not convert this into a full platform proposal; keep the scope as the NPV
  replacement component.

## Skeptical Plan Audit

Wrong-baseline risk: adding technical detail could blur the fact that the
component replaces only the NPV valuation component. Mitigation: every new
section will state the component boundary and caller-system boundary where
relevant.

Proxy-metric risk: validation formulas could accidentally promote AUC,
short-horizon spend, or calibration as proof of lifetime incremental NPV.
Mitigation: validation gates will distinguish causal lift, predictive
calibration, finance reconciliation, and diagnostic metrics.

Hidden-assumption risk: default valuation semantics could look like approved
bank policy. Mitigation: present the bundle as a proposed starting convention
requiring owner approval, not as final policy.

Evidence risk: adding literature language could overstate support from papers
whose technical sections have not been audited. Mitigation: use existing
citations only for mechanisms and methods already cited; label project
derivations and issuer-specific quantities clearly.

Organization risk: adding many sections could make the paper longer but still
disorganized. Mitigation: add a reader-navigation section and integrate new
sections at the exact points where the current argument needs them.

Artifact risk: a plan without execution would not satisfy the user request.
Mitigation: patch the LaTeX proposal, rebuild the PDF, and record the build and
audit result here.

Decision: the plan passes. Execute the scoped remediation.

## Post-Execution Audit

Execution date: 2026-07-01.

The remediation pass was executed against
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`.
The proposal now includes the following panel-readiness additions:

1. A reader-navigation section explaining how the literature, valuation object,
   identification strategy, component design, and governance material fit
   together.
2. A valuation-object and wallet-accounting section defining the state space,
   the decision-conditional NPV functional, the cash-flow primitive, and the
   distinction between outside wallet, movable wallet, captured wallet, and
   profitable captured wallet.
3. A module-level identification plan covering response, application,
   approval, booking, activation, first use, usage, cannibalization, balances,
   payments, lines, APR, promotions, losses, rewards, attrition, product
   conversion, retention, and relationship spillovers.
4. An uncertainty-propagation and model-risk-control section covering
   cross-module parameter uncertainty, scenario uncertainty, terminal-value
   uncertainty, dependence across modules, and optimizer exploitation of model
   error.
5. A formal validation-gates section with calibration, balance, overlap,
   decomposition, and promotion-gate formulas.
6. A default valuation-semantics bundle that can be reviewed and amended by
   finance, risk, product, and governance owners.
7. An allowed-use taxonomy separating causal incremental NPV,
   policy-conditional expected NPV, diagnostic/scenario NPV, degraded NPV,
   no-score status, and prohibited uses.
8. A strengthened source-support audit appendix explaining that the current
   tables are audit ledgers, not main exposition, and that a full
   primary-source/snowball/claim-support audit remains a required governance
   artifact.

Build verification:

- Command run from `docs/credit-card-npv-component-proposal`:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`.
- Result: successful PDF build.
- Output: `credit_card_npv_component_proposal.pdf`, 69 pages, 525,885 bytes.
- Log check found no LaTeX errors, fatal stops, undefined citations,
  undefined references, multiply defined labels, or rerun-required warnings.
- Residual typography warning: one very small overfull `\hbox` warning
  (`0.52028pt`) around line 1003. This is a formatting issue rather than a
  substantive or build blocker.

Residual caveats:

- This execution improves organization, technical specificity, and component
  semantics, but it does not complete a full primary-source literature audit.
  The proposal now says explicitly that a source-support ledger,
  claim-support ledger, backward/forward snowball ledgers, and omitted-paper
  register are still required before model-governance submission.
- The new sections intentionally avoid inventing bank-specific thresholds,
  approval statuses, data availability, or empirical results. Those must be
  supplied by bank owners or validated from actual bank data.
- The proposal remains a component proposal, not a platform proposal. The
  caller systems, decision engines, finance ledger, campaign platform, and
  account-management systems are treated as integration boundaries.

Post-execution decision: the scoped remediation plan has been carried out. The
remaining gaps are now governance and evidence-production work rather than
failures to execute this pass.

## Follow-Up Risk-Section Remediation

Execution date: 2026-07-01.

After review, the original "Open Gaps and Reviewer Risks" section was judged
too compressed for panel use. It listed serious endogeneity, selection,
wallet, and evidence-risk issues but did not explain the identification
failure, mitigation, and residual gap for each issue. The proposal was
therefore revised again.

Changes made:

1. Replaced the short risk list with
   `Endogeneity, Confounding, and Remaining Reviewer Risks`.
2. Added dedicated subsections on:
   - funnel selection and transportability;
   - policy variables, counterfactuals, and causal lift;
   - cannibalization, wallet decomposition, and promotion decay;
   - CLV, credit risk, and balance-sheet cost;
   - state dependence, macro conditions, and dynamic feedback;
   - external data, relationship spillovers, and residual evidence gaps.
3. Reframed each issue as risk, mitigation, and residual gap.
4. Anchored the discussion in existing proposal citations for sample
   selection, propensity scores, IV, RD, DiD, event studies, dynamic panels,
   CLV, payment choice, rewards, liquidity, unemployment, macro shocks, public
   macro data, and licensed data.
5. Preserved the scope boundary: the component estimates NPV and evidence
   labels; it does not claim that the literature supplies issuer-specific
   activation, cannibalization, movable-wallet, reward-elasticity, capital, or
   relationship-spillover parameters.

Build verification:

- Command run from `docs/credit-card-npv-component-proposal`:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`.
- Result: successful PDF build.
- Output: `credit_card_npv_component_proposal.pdf`, 72 pages, 538,313 bytes.
- Log check found no LaTeX errors, fatal stops, undefined citations,
  undefined references, multiply defined labels, or rerun-required warnings.
- Residual typography warning remains the same very small overfull `\hbox`
  warning (`0.52028pt`) around line 1003.

Follow-up decision: the reviewer-risk section is no longer merely a list of
objections. It now gives the panel a defensible map from each critical issue
to the proposed econometric or governance treatment and the remaining
issuer-specific evidence requirement.
