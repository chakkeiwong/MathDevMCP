# Credit Card NPV Proposal Content Preservation Ledger

Date: 2026-07-01

Baseline artifact:

- Proposal: `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
- PDF baseline before this hardening pass: 80 pages, 589,397 bytes.

## Preservation Rule

The panel-submission hardening pass is not a compression rewrite. Substantive
material should be preserved, expanded, or relocated with a pointer. A passage
may be removed only if it is duplicate, incorrect, or superseded by a stronger
version.

## Current Section Map

| Current section | Main content | Hardening action |
|---|---|---|
| Executive Summary and Component Charter | Scope, component boundary, first production slice | Keep; add clearer navigation and notation pointers. |
| Replacement Boundary and Evidence Use | Evidence classes and evidence-to-design spine | Keep; align with source-support ledger. |
| How to Read This Technical Proposal | Reader map | Keep; expand to mention new data, notation, worked contracts, implementation sections. |
| Valuation Object, State Space, and Wallet Accounting | Core NPV notation, wallet decomposition | Keep; add notation glossary to reduce symbol ambiguity. |
| Literature sections | Macro, usage, CLV, architecture | Preserve; do not compress into a short summary. Add stronger claim-support anchors over time. |
| Component Decomposition | Losses, balances, PPNR, overlays, schematic | Preserve; connect to implementation section. |
| Decision and Measurement Pitfalls | Consultant issues and funnel/objective problems | Preserve; later re-architecture may merge with reviewer risks if duplication is controlled. |
| Empirical Design and Validation | Early data and validation design | Preserve; later align with formal validation gates. |
| Identification, Endogeneity, and Data Strategy | Causal/data strategy, external/internal data | Preserve; expand with concrete internal/external data inventories. |
| Practical Experimental Design Program | Formal experimental-design framework | Preserve; add worked contracts. |
| Module-Level Identification Plan | Module evidence grades | Preserve; connect to implementation and evidence-grade propagation. |
| Uncertainty and Formal Validation | Uncertainty, calibration, veto gates | Preserve; connect to implementation. |
| Remaining Reviewer Risks | Risk/mitigation/residual gap sections | Preserve; table-heavy material should remain secondary. |
| Default Valuation Semantics | Valuation bundle principles | Expand into concrete first-slice base case plus sensitivities. |
| Allowed-Use Taxonomy | Output labels and prohibited uses | Preserve. |
| Decision Processes / Migration / Operating Spec | Contracts, modes, governance | Preserve; table readability pass needed. |
| Source-Support Audit | Claim and source ledgers | Expand as a hardening ledger; keep dense tables in appendix. |

## Additions Required by the Hardening Plan

1. Notation glossary and conventions.
2. Internal bank data feasibility section.
3. Public/official/LSEG data operational inventory.
4. Concrete first-slice valuation semantics and sensitivity cases.
5. Worked acquisition/prescreen experiment contract.
6. Worked existing-client cannibalization contract.
7. Model implementation blueprint.
8. Table readability notes and appendix strategy.
9. Expanded source-support and claim-support ledgers.

## Removal Ledger

No substantive proposal material is scheduled for removal in this pass.
