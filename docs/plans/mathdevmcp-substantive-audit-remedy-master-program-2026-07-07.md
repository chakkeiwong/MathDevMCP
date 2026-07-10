# MathDevMCP Substantive Audit Remedy Master Program

Date: 2026-07-07

Status: `COMPLETED_WITH_BOUNDARIES`

## Objective

Repair the weak-report regression in `audit_math_document_rigor` and address
the D447 downstream feedback by making MathDevMCP high-level tools produce
agent-consumable mathematical gap/proposal reports with concrete derivation
payloads, actionable abstention, version-aware evidence selection, and explicit
nonclaim boundaries.

## Motivation

The current document-rigor report has useful provenance and field structure, but
it can still present weak entries such as "add a review boundary" or "then
prove" as proposed fixes. That is a contract failure: field presence is being
treated as mathematical usefulness.

The D447 feedback reports the same underlying failure mode in another setting:
MathDevMCP abstains safely, but often does not say what exact obligation,
assumption, scope boundary, or safe wording would make the abstention useful.

## Target Surfaces

- `search_latex`
- `latex_label_lookup`
- `audit_and_propose_fix`
- `audit_math_document_rigor`
- `audit_math_to_code`
- `classify_math_claim`
- new `audit_report_claim_boundary` workflow
- CLI, MCP facade, and FastMCP exposure for changed/new workflows

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Review Gate | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-00-governance-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-00-governance-result-2026-07-07.md` |
| 1 | Version-Aware Evidence Selection | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-01-version-aware-search-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-01-version-aware-search-result-2026-07-07.md` |
| 2 | Substantive Proposal Contract | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-02-substantive-contract-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-02-substantive-contract-result-2026-07-07.md` |
| 3 | Actionable Abstention And Domain Obligations | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-03-actionable-abstention-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-03-actionable-abstention-result-2026-07-07.md` |
| 4 | Scope-Aware Math-To-Code Audit | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-04-scope-aware-code-audit-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-04-scope-aware-code-audit-result-2026-07-07.md` |
| 5 | Report Claim Boundary Workflow | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-05-report-claim-boundary-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-05-report-claim-boundary-result-2026-07-07.md` |
| 6 | Integrated Experiments And Closeout | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-06-integrated-closeout-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-substantive-audit-remedy-phase-06-integrated-closeout-result-2026-07-07.md` |

## Execution Dependencies

Phase 1 must run before any document experiments so old/final sibling files do
not contaminate evidence. Phase 2 must run before rendering or rerunning reports
so weak proposals are demoted. Phase 3 then adds richer abstention payloads
that the Phase 2 contract/rendering path can preserve in Phase 6 reruns. Phase
4 and Phase 5 address D447 feedback not specific to document-rigor reports.
Phase 6 reruns experiments only after the tool behavior has been repaired.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP turn conservative abstention into concrete agent-consumable mathematical repair guidance without overclaiming proof? |
| Baseline/comparator | Current `credit-card-npv-component-proposal-rigor-audit` report and D447 feedback examples. |
| Primary pass criterion | Changed workflows either provide concrete replacement/derivation/safe-wording payloads, or explicitly classify entries as non-actionable diagnostics with missing obligations and next smallest audit. Bare proof targets or assumption lists are diagnostic unless paired with a specific edit, derivation route, safe wording, or next audit. |
| Veto diagnostics | Versioned-file contamination; field-presence-only "fixes"; generic "then prove" proposals in the concrete-fix ledger; backend not-encodable treated as false/proof; report-status/nonclaim text classified as ordinary theorem; structural code scope mismatch reported as formula contradiction. |
| Explanatory diagnostics | Backend attempts, not-encodable reasons, matched terms, missing variables, missing domain obligations, safe wording. |
| Not concluded | No full formal proof of the credit-card NPV document, no full D447 scientific validation, no product/release readiness claim, and no claim that LeanDojo search is a proof certificate. |
| Artifacts | Phase subplans/results, visible ledger, review trail, focused tests, regenerated reports. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Keep conservative proof policy | Existing MathDevMCP governance and D447 feedback | Safer than hallucinated proof | Abstention stays too vague | Tests require missing obligations and safe wording | Reviewed default |
| Exact-file filtering first | Credit-card and D447 duplicate-version failures | Prevents polluted evidence | Later reports mix old and final documents | Search/lookup tests with sibling D446/D447 fixtures | Reviewed default |
| Concrete-fix and diagnostic ledgers | Current weak report regression | Prevents slogans appearing as fixes | Agents apply non-actionable prose | Tests reject generic concrete fixes and bare proof-target-only entries | Reviewed default |
| Domain routers are obligation extractors, not solvers | D447 OBC/NPV/Bellman feedback | Useful without overclaiming structural validation | Router text becomes proof claim | Nonclaims and certification boundaries required | Reviewed default |
| Claude is read-only reviewer | User instruction and review-gate guide | Independent plan/phase audit | Reviewer appears to authorize execution | Ledger records advisory-only status | Reviewed default |

## Skeptical Plan Audit

This program must not pass merely because new fields exist. The material test is
whether an agent can consume the output and know:

- what mathematical object is missing;
- what assumption or derivation step would close the gap;
- what deterministic backend did or did not check;
- whether the output is a concrete proposed edit or a diagnostic abstention.

The plan would be flawed if Phase 6 reruns reports before Phases 1-3 repair
evidence selection, proposal substance, and actionable abstention. It would also
be flawed if D447 feedback were handled only as documentation. The phases are
therefore ordered so routing and contracts precede experiments.

## Forbidden Claims

- Do not claim proof of macro-finance equations unless a certifying backend
  checks explicit placeholder-free source.
- Do not treat LeanDojo availability as a proof certificate.
- Do not call a proposal concrete with only a proof target or only an
  assumption list. A concrete proposal must contain a specific replacement,
  derivation route, safe report wording, or smallest next audit that an agent
  can execute.
- Do not edit target user documents during audit experiments.
- Do not commit or push unless explicitly requested after closeout.
