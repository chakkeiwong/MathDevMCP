# Credit Card NPV Proposal Citation-Discipline Hardening Plan

Date: 2026-07-01

## Objective

Execute a focused precision-hardening pass on
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
in response to the citation audit in
`docs/plans/credit-card-npv-component-proposal-citation-audit-2026-07-01.md`.

This is not a broad rewrite. The current proposal architecture should be
preserved. The goal is to align the main-body wording with the conservative
evidence standard already present in the source-support appendix.

## Skeptical Plan Audit

Wrong baseline risk: A broad rewrite could repeat the earlier failure mode of
compressing a long technical proposal into a short memo. Mitigation: make only
targeted edits to audited passages and add a compact decision-request section.

Evidence risk: Wording changes could weaken useful claims too much or obscure
why the literature matters. Mitigation: distinguish three classes explicitly:
literature-supported mechanism, project derivation/design convention, and
issuer-specific empirical quantity.

Artifact risk: The pass could fix prose but leave the audit ledger stale.
Mitigation: update the claim/source-support material with allowed and forbidden
claims for sensitive sources.

Build risk: The pass edits LaTeX and must be rebuilt. Mitigation: run
`latexmk -pdf -interaction=nonstopmode -halt-on-error`.

Decision: plan passes. Proceed with a precision pass, not a structural rewrite.

## Tasks

1. Add a front-end `Requested Panel Decisions` section:
   - approve phase-1 batch acquisition/prescreen slice;
   - approve shadow scoring and reconciliation;
   - approve holdout/experiment evidence program;
   - approve default valuation semantics only for that slice;
   - explicitly not approve broader underwriting, line, account-management,
     CECL, stress, or official finance use.
2. Tighten macro/liquidity wording:
   - public spending/liquidity papers motivate controls and hypotheses;
   - issuer-specific payment, routing, loss, and attrition effects require bank
     evidence.
3. Tighten rewards wording:
   - Agarwal et al. rewards evidence is a booked-account analogue;
   - new-card acquisition and activation require issuer-specific experiments.
4. Tighten CARD Act/product-terms wording:
   - CARD Act supports fee, disclosure, repayment, and revenue/payment
     channels;
   - broader transition-kernel mapping is project design logic.
5. Label outside-wallet and movable-wallet at first introduction as latent,
   issuer-specific project objects.
6. Remove drafting residue referring to the user.
7. Add allowed/forbidden claim guidance for sensitive sources in the
   source-support appendix.
8. Rebuild PDF and record audit result.

## Acceptance Criteria

- The proposal remains full-depth and is not shortened for readability theater.
- The main body no longer overclaims the cited literature for macro/liquidity,
  rewards, CARD Act, or wallet constructs.
- The decision request is explicit but does not convert the proposal into a
  short board memo.
- The source-support appendix tells reviewers what the sensitive sources can
  and cannot support.
- LaTeX builds successfully.
