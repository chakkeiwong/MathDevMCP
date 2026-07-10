# MathDevMCP Agent-Guided Tool-Verified Repair Master Program

Date: 2026-07-10

Status: `DRAFT_UNDER_REVIEW`

## Objective

Build the next repair lane for MathDevMCP: agent-guided, tool-verified
derivation repair.  The agent may brainstorm mathematical routes, missing
assumptions, formalization strategies, and unblocker hypotheses, but those
hypotheses must enter the derivation tree as candidate branches.  Reports may
publish only what the tree records as backend-closed, partially backend-closed,
refuted, invalid, or blocked at exact nodes.

## Core Invariant

An agent may propose any mathematically plausible route, but MathDevMCP may
only publish what the derivation tree has verified, partially verified,
refuted, rejected, or blocked with exact evidence.

## Role Split

| Role | Responsibility | Boundary |
| --- | --- | --- |
| Agent | Generate candidate hypotheses and routes from exact blockers. | Agent prose is never direct repair evidence. |
| Derivation tree | Store search state, parent/child provenance, blockers, hypotheses, assumptions, backend attempts, and closure status. | Tree status is an evidence ledger, not a proof unless backed by certifying evidence. |
| Backends | Certify, refute, or diagnose scoped formalization targets. | Backend evidence is scoped to the encoded target and assumptions. |
| Report compiler | Publish only tree-grounded proposals, partial repairs, refutations, or gap reports. | Diagnostic-only paths cannot become repair proposals. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP combine agent brainstorming with derivation-tree and backend verification so that repair reports are useful without hallucinated mathematical fixes? |
| Baseline/comparator | Current Phase 06 context-aware executable repair reports: useful source localization, typed blockers, branch ranking, and backend attempts, but still able to render blocked ranked branches as repair-like prose. |
| Primary pass criterion | The final high-level workflow records agent hypotheses as candidate tree branches, recursively expands exact blockers, runs or blocks backend formalization targets, and emits repair proposals only from tool-grounded closed or partially closed paths. Blocked paths render as gap reports with exact next executable actions. |
| Veto diagnostics | Raw agent proposal emitted as a fix; diagnostic evidence promoted to certification; LeanDojo/Pantograph/retrieval trace treated as proof; blocked branch rendered as document-ready repair; missing source location/problem/why/proposed-fix evidence; no exact blocker after failed formalization; no stop condition or budget ledger. |
| Explanatory diagnostics | Optional backend unavailable, stochastic construct not encodable, ambiguous source symbol, budget exhausted, all candidate hypotheses blocked, Claude unavailable. |
| Not concluded | No whole-document proof, global theorem-proving completeness, minimality of assumptions, publication readiness, release readiness, or claim that optional external tools are installed unless directly checked. |
| Artifacts | Master program, phase subplans/results, visible runbook/ledger, stop handoff, Claude or Codex review bundle, focused tests, generated JSON/Markdown reports for frozen documents. |

## Frozen Regression Set

| Case | File | Labels | Required behavior |
| --- | --- | --- | --- |
| Card NPV valuation identity | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | Conditional-expectation blockers must become candidate hypothesis branches. Algebraic finite-horizon subclaims should be backend-attempted when encodable. Blocked stochastic branches must render as gap reports, not final repairs. |
| Risky debt FOC proposition | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | Proposition context, FOC assumptions, interchange/integrability blockers, and any backend attempts must remain linked to exact source spans. |
| Simple algebra fixture | Test fixture in `tests/test_document_derivation_tree.py` | `eq:simple` | Encodable algebraic branches must still promote only through scoped backend evidence. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Extend existing derivation tree modules | Current `document_derivation_tree.py`, `derivation_search_tree.py`, `derivation_branch_controller.py` | Preserves current source localization, typed blockers, and backend adapter contracts. | New loop bypasses existing proof-claim guards. | Phase 01 tests assert old promotion guards still apply. | Reviewed default |
| Agent is represented by structured hypothesis records | User direction and current report weakness | Preserves creativity while preventing raw prose publication. | Vague hypotheses enter reports. | Phase 02 rejects hypotheses without blocker id, assumptions, route, backend target, success criterion, and failure criterion. | Reviewed default |
| Backends remain certifiers/refuters/diagnostics | Repo `AGENTS.md` and existing adapters | Avoids hallucination and token-heavy proof prose. | Retrieval/proof-state traces become proof. | Phase 04 tests require direct Lean/SymPy/Sage evidence for certification. | Reviewed default |
| Blocked paths render as gap reports | User feedback on handwavy proposals | Makes inability useful and honest. | Reports become shorter but still vague. | Phase 06 tests require exact location, problem, mathematical why, blockers, and next executable action. | Reviewed default |
| Visible execution rather than detached overnight runner | `visible-gated-execution-runbook-template.md` | Recoverable in the current conversation and aligned with template boundaries. | User expected detached autonomous run. | Runbook records visible overnight-scale execution and stop condition for detached launch. | Reviewed default |

## Skeptical Plan Audit

Wrong baseline risk: the baseline is not a complete theorem prover.  It is the
current context-aware report that still leaks blocked branches into repair-like
language.  The plan therefore uses diagnostic leakage as a primary regression
target.

Proxy metric risk: more branches, more hypotheses, or more backend attempts do
not mean better repairs.  Pass criteria are closure status, evidence refs,
exact blockers, and report discipline.

Hidden assumption risk: an agent hypothesis may smuggle assumptions into a
derivation.  The schema must record assumptions explicitly and bind them to
source evidence, deterministic rule evidence, or remaining gaps.

Environment mismatch risk: Lean, LeanDojo, Sage, and other optional tools may
live in separate environments.  Backend availability is evidence to record,
not a premise.

Artifact mismatch risk: plan documents alone do not improve reports.  Each
implementation phase must add tests, code contracts, generated artifacts, or
mission-control policy.

Audit result: proceed only through gated visible phases.  Stop on unapproved
package installation, network fetch, destructive state changes, proof-boundary
weakening, or nonconvergent review.

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| 00 | Governance, Baseline, And Review Gate | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-governance-baseline-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-result-2026-07-10.md` |
| 01 | Strict Contracts And Regression Gates | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-contracts-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-result-2026-07-10.md` |
| 02 | Agent Hypothesis Expansion Interface | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-agent-hypotheses-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-result-2026-07-10.md` |
| 03 | Recursive Derivation Tree Search | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-recursive-tree-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-result-2026-07-10.md` |
| 04 | Backend Formalization Targets | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-backend-formalization-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-result-2026-07-10.md` |
| 05 | Expansion Rule Library | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-expansion-rules-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-result-2026-07-10.md` |
| 06 | Tool-Grounded Proposal Compiler | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-proposal-compiler-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-result-2026-07-10.md` |
| 07 | CLI And MCP Integration | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-cli-mcp-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-result-2026-07-10.md` |
| 08 | Parallel Search Discipline | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-parallel-search-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-result-2026-07-10.md` |
| 09 | Real-Document Regression And Mission Control | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-real-doc-mission-control-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md` |

## Stop Conditions

Stop and write a blocker result if:

- continuing requires unapproved package installation, network fetch,
  credentials, detached execution, or backend environment mutation;
- a proposed implementation would weaken proof/certification boundaries;
- Claude and Codex fallback review cannot converge after five rounds for the
  same material blocker;
- current work would overwrite unrelated dirty user changes;
- pass/fail criteria would need to change after seeing results;
- generated reports cannot preserve exact source locations, mathematical why,
  tool evidence, and remaining blockers.
