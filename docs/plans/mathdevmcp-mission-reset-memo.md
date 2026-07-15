# MathDevMCP Mission Reset Memo

Date: 2026-07-04
Mission wording amended: 2026-07-10

Status: `READ_THIS_FIRST_REAL_DOCUMENT_AUDIT_OPEN_GAPS_2026_07_16`

## Read This First

The benchmark is an instrument, not the mission.

The mission is to build an exploratory, high-standard, rigorous, agent-facing
mathematical development system, exposed through CLI/MCP, that helps agents
and colleagues audit and develop mathematical code and documents, locate proof
gaps, missing assumptions, implementation mismatches, and backend limitations,
and investigate candidate repairs while never mistaking diagnostics or
hypotheses for proof.

The system is exploratory in search and rigorous at the claim boundary:
candidate branches may be speculative, but published repairs and verified
claims require explicit assumptions and reproducible supporting evidence.

Before starting any substantial lane, read:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`
- `docs/plans/mathdevmcp-agent-consumable-gap-proposal-mission-control-2026-07-06.md`

Sonnet max read-only review agreed with the 2026-07-04 wording of this mission
spine:
`REVIEW_STATUS=agreed`, `VERDICT=AGREE`,
`RUN_DIR=.claude_reviews/20260704-021100-mathdevmcp-mission-spine-sonnet-r1`.
The 2026-07-10 wording amendment has not inherited that review verdict; it
preserves the reviewed evidence and claim-boundary rules.

## Current Direction

The 2026-07-16 full public-surface mission audit against the credit-card NPV
proposal has final status `MISSION_NOT_YET_ACCOMPLISHED`; see
`docs/plans/mathdevmcp-credit-card-full-mission-audit-result-2026-07-16.md`.
All 57 public MCP tools were accounted for, 48 were invoked with valid bounded
inputs, and 9 were explicitly inapplicable because the document does not bind
their required code, literature, or temporal inputs. The strongest repaired
lane is substantively useful, but the audit found claim-boundary and workflow
vetoes: a source definition is falsely refuted as a theorem, high-level tools
do not share one complete extraction contract, duplicate labels are not safely
bound everywhere, and branches stop before source-faithful specialist
execution. The full suite also remains non-clean at 1531 passed, 33 failed, and
4 skipped.

The next program should be a focused semantic target-unification and execution
repair, not another benchmark or governance cycle:

1. carry typed claim roles and exact file/content identity through extraction,
   packets, proof routing, and reports;
2. make every high-level document workflow consume the repaired label-scoped
   complete-row obligation;
3. prohibit definition/identity targets from entering free-variable theorem
   refutation routes;
4. add expression-aware assumption discharge;
5. execute one reviewed discounted-cash-flow/valuation obligation end to end
   through an installed specialist backend;
6. repair the independent full-suite checker, isolation, FOC, and pilot
   failures, then rerun this credit-card audit as the regression test.

The real-document remediation program completed Phases 00-09 on 2026-07-15
with final bounded status `SAFE_AND_SUBSTANTIVELY_USEFUL`; see
`docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-result-2026-07-15.md`.
The result establishes one exact `backend_checked` real-document subclaim and
an actionable two-document compact workflow. It does not establish proof,
broad corpus validity, publication, release, defaults, or full-suite health.
Do not reopen that program absent a newly identified defect; start the next
scientific/product lane with a fresh evidence contract.

The v2 downstream-agent usefulness collection is closed as a bounded local
diagnostic with final Sonnet review agreement.

Do not default to building another benchmark. The current evidence points to
implementation work:

- use the agent-consumable gap/proposal mission-control template for high-level
  tool modifications;
- improve review-packet/handoff-packet generation;
- make generated packets compact, actionable, provenance-aware, and explicit
  about assumptions, route gaps, veto risks, non-claims, and next artifacts;
- expose the improved workflow through stable CLI/MCP or library surfaces;
- use the v2 benchmark as a regression/evaluation harness after the product
  workflow changes.

## Product Spine To Preserve

```text
source label or code path
-> parser/provenance evidence
-> typed MathObligation diagnostics
-> route decision
-> shape/dimension diagnostics
-> backend evidence or explicit abstention
-> compact colleague/agent-facing report
-> benchmark or release artifact
```

## What To Ask At Lane Start

1. Which part of the product spine is being improved or protected?
2. Which user workflow becomes easier, safer, or more reproducible?
3. What evidence instrument will measure the change?
4. How will the result feed implementation, release readiness, or a regression
   guard?
5. What claim remains forbidden?

## What To Avoid

- Do not optimize benchmark totals for their own sake.
- Do not treat review/handoff packets as proof certificates.
- Do not add governance artifacts when a concrete CLI/MCP workflow repair is
  the justified next step.
- Do not weaken abstention, backend-evidence, provenance, or non-claim
  boundaries to make outputs look more successful.
- Do not design benchmark cases around unmerged implementation details.

## Current Best Next Plan

Draft and execute a mission-aligned implementation plan:

```text
Source-Bound Semantic Target Unification And Valuation Execution
```

Likely scope:

- define and preserve typed claim roles, especially definition versus theorem;
- require exact file/content identity for ambiguous labels;
- route every high-level document workflow through the complete label-scoped
  obligation contract;
- normalize expression-specific assumptions against backend preconditions;
- add one reviewed discounted-cash-flow or valuation formalization and execute
  it through an installed specialist backend;
- repair the full-suite root failures relevant to checkers, isolation, the FOC
  regression, and the real-local pilot;
- rerun the credit-card mission audit as the end-to-end regression.

Stop if the plan turns back into benchmark or governance expansion without a
concrete source-bound semantic or execution repair.

## 2026-07-06 Derivation Target Extraction/Routing Handoff

The derivation audit lane now has a completed target-extraction/routing slice:

- master program:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-master-program-2026-07-06.md`;
- final ledger:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-execution-ledger-2026-07-06.md`;
- v2 risky-debt report:
  `docs/reviews/risky-debt-derivation-gap-proposals-v2.md`;
- final fallback review:
  `docs/reviews/mathdevmcp-derivation-target-extraction-routing-final-codex-fallback-review.md`.

New behavior:

- label reports extract source-local equation/align-row targets with lhs/rhs,
  parent label, equation label, file/line provenance, source text, stable ids,
  and explicit full-block fallback;
- route plans name deterministic candidate tools, expected evidence contracts,
  backend/formalization status, and non-certifying boundaries;
- `audit_and_propose_derivations` now reports extracted targets, route plans,
  target-level gaps/proposals, and linked assumption repairs;
- public CLI/MCP contract remains `derivation_audit_report_result` with
  additive fields.

Final focused checks passed:

- 38 derivation/extraction tests;
- 43 MCP public-surface tests;
- `git diff --check`.

Important limitation:

- This slice improves agent-consumable diagnostics. It does not prove the
  risky-debt note or apply edits. LaTeX-heavy obligations still require
  formalization before Lean/Sage/counterexample tools can certify them.
