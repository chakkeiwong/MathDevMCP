# Credit Card NPV Proposal: Wallet-Ideas Absorption Plan

Date: 2026-07-01

## Objective

Revise the credit-card NPV component proposal so that it absorbs the useful
wallet-modeling ideas from adjacent bank modeling work without mentioning or
referencing that adjacent note. The ideas should become native credit-card NPV
requirements: partial observability, spend-source decomposition, movable
outside wallet, evidence grades, validation anchors, estimation ledgers, and
transportability diagnostics.

## Planned Changes

1. Add an early "latent card wallet" framing that states the bank observes only
   part of the customer payment and borrowing life.
2. Strengthen the spend-source decomposition so observed new-card spend is
   separated into incremental consumption, competitor shift, existing-bank-card
   cannibalization, debit/deposit substitution, promotion pull-forward, and
   measurement error.
3. Add an offer- and horizon-specific movable-wallet object for outside card
   spend and outside revolving balances.
4. Add evidence grades to component outputs and governance language:
   directly observed, internally anchored, externally benchmarked,
   experimentally identified, quasi-experimental, model-imputed, and
   scenario-only.
5. Add an estimation-ledger subsection in the identification/data section:
   selection/funnel, offer/terms, outside-wallet/cannibalization,
   dynamic-behavior, causal-evidence, and downstream-policy ledgers.
6. Strengthen validation anchors for outside-wallet, cannibalization, and
   durable wallet-share estimates.
7. Add target-population and transportability diagnostics.
8. Update open risks and claim-support ledger.
9. Build the LaTeX document and review the final document against this plan.

## Skeptical Plan Audit

Wrong baseline risk: the revision could mistake estimated outside wallet for
incremental NPV. Mitigation: explicitly separate outside wallet size, movable
wallet, causal response, and NPV.

Proxy-metric risk: new-card spend, first 90-day spend, card-on-file setup, or
activation might be treated as proof of incremental value. Mitigation: state
these are diagnostics unless tied to a validated spend-source decomposition and
causal design.

Hidden assumption risk: competitor-card spend and outside revolving balances
are mostly unobserved. Mitigation: require evidence grades and uncertainty,
and distinguish directly observed, anchored, benchmarked, imputed, and
scenario-only estimates.

Stale context risk: the current proposal already contains cannibalization and
identification sections. Mitigation: integrate with those sections rather than
creating a disconnected new chapter.

Artifact adequacy: the user asked to execute the plan and review carefully.
Mitigation: patch the proposal, rebuild the PDF, and record a post-execution
audit in this plan file.

Decision: the plan passes after these mitigations. Proceed with scoped edits.

## Execution Summary

Implemented in:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.pdf`

The revision deliberately does not mention or cite the adjacent SME/deposit
wallet note. The absorbed ideas are expressed as native credit-card NPV design
requirements.

## Post-Execution Review Against The Plan

1. Latent card wallet framing: satisfied. The executive section now states that
   card wallet is a partially observed state and separates outside wallet size,
   movable wallet, causal response, and NPV.

2. Spend-source decomposition: satisfied. The cannibalization section now
   decomposes observed new-card spend into incremental consumption,
   competitor-card shift, old-bank-card cannibalization, debit/deposit
   substitution, promotion timing, and measurement error.

3. Movable wallet object: satisfied. The proposal now defines outside card
   wallet and offer-specific movable wallet and warns that large outside wallet
   does not imply captured wallet or positive NPV.

4. Evidence grades: satisfied. Module 2, the cannibalization section, data
   requirements, production metadata, and estimation ledgers now use evidence
   grades such as directly observed, internally anchored, externally
   benchmarked, experimentally identified, quasi-experimental, model-imputed,
   and scenario-only.

5. Estimation-ledger subsection: satisfied. The identification/data section now
   includes ledgers for selection/funnel populations, offer and terms
   assignment, outside-wallet/cannibalization evidence, dynamic behavior,
   causal evidence, and downstream policy.

6. Validation anchors: satisfied. The validation section now requires anchors
   such as balance-transfer or payoff records, old-card spend decay,
   debit/deposit substitution, card-on-file migration, bureau aggregates where
   available, account-aggregation samples, and post-promotion decay.

7. Transportability diagnostics: satisfied. The validation and estimation-ledger
   sections now require target-population diagnostics across prospects,
   contacted customers, responders, applicants, approvals, booked accounts,
   activated accounts, and active incumbents.

8. Open risks: satisfied. The risk list now warns against treating new-card
   spend as captured outside wallet, outside wallet as movable wallet, wallet
   size as NPV, model-imputed wallet as observed/experimental evidence, and
   temporary promotion lift as durable wallet share.

9. Claim-support ledger: satisfied. The ledger now includes claims for
   spend-source decomposition and for separating outside wallet, movable wallet,
   causal response, and NPV, with project-derivation support and internal
   validation requirements.

## Build And Review Result

`latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex`
completed successfully. The output PDF has 59 pages. The final log scan found
no unresolved citations, undefined references, fatal errors, or overfull boxes.

Review decision: the current document satisfies the plan at proposal level.
The remaining future-model-package work is to instantiate the ledgers and
evidence grades for each production submodel with concrete thresholds,
approved populations, and owner sign-offs.
