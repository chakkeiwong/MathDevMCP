# MathDevMCP Context-Aware Executable Repair Master Program

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Objective

Close the remaining gap between a structured diagnostic proposal and a good
mathematical repair proposal.  A good proposal must be context-aware,
branch-searchable, and backed by executable or precisely blocked external-tool
attempts.  It must not merely repackage deterministic templates into nicer
Markdown.

## Overall Goal

For a document label such as `prop:interior-foc`, MathDevMCP should produce an
agent-consumable repair packet containing:

- proposition or equation source span;
- nearby hypotheses, proof text, referenced equations, and definitions;
- a typed obligation IR with variables, operators, assumptions, domains, and
  unresolved constructs;
- candidate assumption and derivation branches;
- executable SymPy/Sage/Lean attempts whenever the branch is encodable;
- precise translation blockers when it is not encodable;
- ranked branch outcomes;
- polished document-ready LaTeX repair text only when supported by branch
  evidence;
- explicit non-claims for proof, minimality, and whole-document correctness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP generate context-aware, backend-attempted repair proposals rather than template-derived assumption paragraphs? |
| Baseline/comparator | Current `audit_document_derivation_tree` Phase 04 frozen reports: structured branches, patch candidates, and non-certifying stubs, but no proposition-level context graph or executable translated backend attempt. |
| Primary pass criterion | Frozen targets produce proposal packets where proposition labels are localized, local context is separated into stated/missing assumptions, at least one branch reaches an executable backend attempt or a precise typed translation blocker, and document-ready repair text is generated from branch evidence. |
| Veto diagnostics | Template-only proposal text; proposition labels reported only as missing focus labels; branch without typed obligation; backend route not considered; stub represented as proof; retrieval/proof-state evidence promoted to proof; unsupported assumptions treated as already stated. |
| Explanatory diagnostics | Context not found, ambiguous symbol role, unsupported stochastic operator, backend absence, branch budget exhaustion, non-minimal assumption set. |
| Not concluded | No whole-document proof, global minimality claim, release-readiness claim, or theorem-prover completeness claim. |
| Artifacts | Master program, phase subplans/results, visible execution runbook/ledger, review bundles, tests, and frozen regression reports. |

## Frozen Regression Set

| Case | File | Labels | Required behavior |
| --- | --- | --- | --- |
| Risky debt FOC proposition | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | `prop:interior-foc` must produce a proposition/context packet and must not remain only a missing display label. |
| Risky debt pricing proposition | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `prop:risky-pricing`, `eq:risky-pricing` | Proposition hypotheses/proof context must be attached to the pricing equation obligation. |
| Credit-card NPV valuation | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | Reports must retain display-equation improvements and add executable or precisely blocked formalization attempts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Reuse `derivation_target_extraction.py` for proposition labels | Existing tests show `prop:interior-foc` extraction | Avoid duplicate proposition parser and preserve provenance | Existing extractor loses proof context | Phase 01 test requires proposition statement/proof snippet/context packet | Reviewed default |
| Reuse `math_ir.py` typed diagnostics | Existing typed obligation machinery | Avoid another ad hoc IR | IR too generic for stochastic economics | Phase 03 tests require expectation/derivative blockers and route hints | Reviewed default |
| External tools first | Repo `AGENTS.md` and user direction | Minimize hallucination and token-heavy agent math | Templates treated as search | Each branch records considered tools and backend attempt/blocker | Reviewed default |
| Executable attempts only for encodable subgoals | Backend boundaries | Prevent false proof claims | Hard targets get no useful backend evidence | Translation blocker must name exact unsupported constructs | Reviewed default |
| Visible execution | Template boundary | Current conversation remains recoverable | User expected detached execution | Runbook states no detached launch and records why | Reviewed default |

## Skeptical Plan Audit

Wrong baseline risk: the baseline is not an ideal theorem prover.  The baseline
is the current improved Phase 04 display-equation report, which still lacks
proposition context and executable translated attempts.

Proxy metric risk: number of branches, stubs, or retrieved premises is not a
pass criterion.  Pass requires context-aware typed obligations and executable
attempts or precise translation blockers.

Hidden assumption risk: surrounding text may already state assumptions.
Missing-assumption proposals must distinguish stated, inferred, missing, and
unresolved assumptions.

Environment risk: LeanDojo, Pantograph, LeanSearch, Sage, and Lean may be
available only in backend environments.  Availability must be evidence, not an
assumption.

Artifact mismatch risk: a plan-only lane would not fix the report.  Each
implementation phase must add a Python contract, tests, or a frozen regression
artifact.

Audit result: proceed through gated visible phases; stop if a phase requires
new package installation, network fetch, or proof-boundary weakening.

## Phase Index

| Phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| 0 | Governance And Review Gate | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-governance-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-result-2026-07-08.md` |
| 1 | Proposition And Context Packet Extraction | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-proposition-context-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-result-2026-07-08.md` |
| 2 | Local Mathematical Context Graph | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-context-graph-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-result-2026-07-08.md` |
| 3 | Typed Repair Obligation IR | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-typed-ir-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-result-2026-07-08.md` |
| 4 | Executable Backend Translators | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-executable-backends-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-result-2026-07-08.md` |
| 5 | Budgeted Repair Branch Search | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-branch-search-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-result-2026-07-08.md` |
| 6 | Document-Ready Repair Report Regression | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-report-regression-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-result-2026-07-08.md` |

## Stop Conditions

Stop and write a blocker result if:

- continuing requires package installation, network access, credentials, or a
  new backend environment not already approved;
- Claude and Codex fallback review cannot converge after five rounds;
- a branch would require weakening proof/certification boundaries;
- implementation would modify unrelated dirty user work;
- a frozen regression command cannot produce bounded artifacts.
