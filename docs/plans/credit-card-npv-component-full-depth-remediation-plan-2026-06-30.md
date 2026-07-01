# Credit card NPV component full-depth remediation plan

Date: 2026-06-30

Target document:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

## Problem

The evidence-integrated rewrite compressed a 26-page literature survey plus a
substantial component proposal into an 18-page PDF. That is a regression. The
user's point is correct: integration should preserve evidence and operating
substance while organizing it for humans. It should not collapse the work into
an executive memo.

## Corrective objective

Rebuild the proposal as a full-depth integrated report:

- use the existing LaTeX survey as the evidence core;
- preserve the survey's detailed equations, source-specific discussion, and
  source-support ledger;
- integrate component-specific sections on replacement boundary, valuation
  semantics, decision contexts, request/response contracts, operating modes,
  validation, governance, migration, and first production slice;
- avoid giant unreadable main-body tables, but keep necessary implementation
  detail in clear sections and appendices;
- clearly label literature-supported mechanisms, bank-specific empirical
  requirements, regulatory/supervisory support, and design conventions.

## Skeptical audit before execution

- **Wrong baseline risk:** The baseline is not the 18-page memo. It is the
  26-page survey plus the earlier accepted component-proposal plan and review
  log.
- **Compression risk:** Readability must not mean deleting technical substance.
  The document may summarize duplicate sentences, but must retain mechanisms,
  equations, claim support, and operating contracts.
- **Proxy metric risk:** Page count is only a guardrail against compression.
  The object remains a defensible proposal for an incremental NPV component.
- **Scope risk:** The document must keep the boundary: build the replacement
  NPV component, not the surrounding campaign, underwriting, finance, stress,
  account-management, or reporting platforms.
- **Evidence risk:** Public literature supports mechanisms and model structure.
  Bank-specific activation, cannibalization, spend response, loss elasticity,
  and value parameters require internal data or experiments.
- **Table risk:** Tables should be readable and introduced by prose. Dense
  schema/status artifacts belong in appendices or compact implementation
  sections.

## Target structure

1. Executive summary and component charter.
2. Replacement boundary and how this proposal uses the literature.
3. Full literature-driven modeling body, preserving the existing survey:
   market/employment/spend, adoption/use, rewards, cannibalization, CLV,
   architecture, component decomposition, decision pitfalls, validation.
4. Component operating specification:
   decision contexts, valuation semantics, request contract, response contract,
   statuses, operating modes, integration with bank systems.
5. Migration, first production slice, governance, and open empirical questions.
6. Source-support and claim-support ledgers.

## Acceptance criteria

- The proposal PDF is materially longer than the 26-page survey and no longer
  looks like a compressed executive digest.
- The survey's detailed equations and paper-specific discussions are preserved
  in the proposal body.
- Component-specific operating detail is present: valuation semantics, data
  contracts, status semantics, operating modes, migration artifacts, and
  governance/reapproval triggers.
- Scope remains component-only.
- PDF builds with no fatal LaTeX errors or undefined citations/references.
- Claude review specifically checks for compression/regression risk before
  final acceptance.
