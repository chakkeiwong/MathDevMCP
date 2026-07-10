# MathDevMCP Substantive Document Derivation Master Program

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Objective

Repair the generic document derivation path so MathDevMCP reports no longer
regress to hand-wavy fixes when a document is mathematically hard.  The tool
must build evidence-rich, agent-consumable gap reports from source-local
semantic obligations, candidate assumption branches, formalization attempts,
backend evidence, and concrete patch candidates.

Card NPV and risky-debt documents are regression targets only.  This program is
not a card-specific or risky-debt-specific plan.

## Overall Goal

For a localized mathematical claim in a LaTeX document, an agent should be able
to call one high-level workflow and receive:

- the exact source span and full display environment;
- the mathematical problem;
- why the problem blocks a derivation;
- candidate sufficient assumption sets, instantiated in the document notation;
- a derivation route under each assumption set;
- external tools considered and attempted;
- SymPy/Sage/Lean formalization stubs or explicit formalization blockers;
- concrete proposed text for the document when the evidence supports it;
- explicit non-claims when proof, minimality, or global document validity is
  not certified.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic document derivation workflow produce concrete mathematical repair evidence instead of generic fallback prose? |
| Baseline/comparator | Current `audit_document_derivation_tree` behavior: deterministic templates plus `can_derive_with_budget`, often with diagnostic-only backend blockers and weak patch content. |
| Primary pass criterion | For heldout document labels, each reported gap includes source location, full local obligation, mathematical why, at least one instantiated candidate assumption branch, a route showing how the branch would close the derivation, tool evidence, and either concrete proposed patch text or a specific formalization blocker. |
| Veto diagnostics | Hand-wavy patch text; row-fragment targets where a full environment is needed; route plans or retrieval hits described as proofs; missing external-tool consideration; proposed assumptions not tied to a derivation closure; patch candidates without source location. |
| Explanatory diagnostics | Backend availability, version mismatch, unsupported LaTeX formalization, branch budget exhaustion, no matched domain template, non-minimal sufficient assumptions. |
| Not concluded | No claim that reports prove whole documents, find globally minimal assumptions, solve all theorem search, or replace Lean/Sage/SymPy certification. |
| Artifacts | This master program, phase subplans/results, visible runbook/ledger, compact review bundles, tests, and generated regression reports. |

## Frozen Regression Set

The final regression gate must not choose easy labels after seeing results.  It
must run at least the following generic hard-document labels unless a result
artifact records a source-file absence or parser blocker:

| Case | File | Labels | Baseline artifact |
| --- | --- | --- | --- |
| Risky debt pricing and FOC | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `eq:risky-pricing`, `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | `docs/reviews/risky-debt-derivation-gap-proposals-v2.md` |
| Credit-card NPV valuation | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | `docs/reviews/credit-card-npv-generic-document-derivation-tree-smoke-2026-07-08.md` |

Additional labels may be added for coverage, but passing the program cannot
depend on replacing these frozen labels with easier cases.

## Phase Result Manifest Requirement

Every phase result must include:

- git commit or `git diff` state summary;
- command(s) actually run;
- Python/backend environment when applicable;
- wall time or `N/A` for pure document edits;
- artifact paths;
- pass/veto status;
- decision table with decision, primary criterion status, veto diagnostic
  status, main uncertainty, next justified action, and non-claims.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure Mode | Early Diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| External-tool-first policy | `AGENTS.md` and prior lane | Reduces hallucination and token-heavy agent math | Tool considered but not actually attempted when formalizable | Assert each branch has tool-consideration evidence | Reviewed default |
| Semantic obligation packets before tree search | Regression diagnosis | Renderer cannot render evidence the tree never records | Packets remain generic templates | Fixture asserts full display text and instantiated symbols | Hypothesis to implement |
| Sufficient assumption branches, not yes/no | User requirement and prior assumption-tool feedback | Agents need closure proposals, not boolean answers | Assumptions are not linked to a derivation route | Tests require `closes_obligations` and route steps | Reviewed default |
| Formalization stubs before proof claims | Lean/Sage/SymPy boundary | Makes missing backend evidence precise without hallucinated proof | Stub is treated as certificate | Promotion guard rejects stub-only evidence | Reviewed default |
| Small phase slices | Dirty repo and broad scope | Prevents a large speculative rewrite | Partial improvement mistaken for complete solution | Phase result records non-claims and next handoff | Reviewed default |

## Skeptical Plan Audit

Wrong baseline risk: comparing against a hypothetical theorem prover would make
the current tool look reasonable.  The comparator is the current generic
workflow and its weak reports on hard documents.

Proxy metric risk: branch count, matched templates, generated assumptions, and
retrieval hits are not pass criteria.  The pass criterion is whether a branch
explains a concrete derivation closure or records a precise blocker.

Missing stop-condition risk: this work could drift into a full theorem prover.
The stop condition is any branch requiring a new search algorithm before source
reconstruction, assumption branching, and formalization stubs are stable.

Environment mismatch risk: LeanDojo, Pantograph, LeanSearch, Sage, and Lean may
live in separate environments.  The tool must record availability and version
evidence; absence is a blocker, not a refutation.

Artifact mismatch risk: a prose-only plan would not answer the user's
complaint.  Each execution phase must add a Python contract, tests, or a
regression artifact.

Audit result: proceed only through gated phases with local checks and
read-only review.  Phase 1 is intentionally scoped to upstream evidence
generation because loosening the renderer would hide the real problem.

## Phase Index

| Phase | Name | Subplan | Required Result |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Gate | `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-governance-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-result-2026-07-08.md` |
| 1 | Semantic Obligation Reconstruction | `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-semantic-obligation-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-result-2026-07-08.md` |
| 2 | Assumption Branch Closure | `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-assumption-branch-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-result-2026-07-08.md` |
| 3 | Formalization Stub And Backend Attempt Integration | `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-formalization-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-result-2026-07-08.md` |
| 4 | Report Integration And Regression Gate | `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-report-regression-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-result-2026-07-08.md` |

## Phase Objectives

### Phase 0: Governance And Baseline Gate

Confirm the regression diagnosis, preserve boundaries, and define the exact
quality checks that later phases must satisfy.

### Phase 1: Semantic Obligation Reconstruction

Create a generic Python path that reconstructs full labeled display
environments and emits typed semantic obligation packets with extracted
operators, source spans, lhs/rhs candidates, and symbol inventory.

### Phase 2: Assumption Branch Closure

Replace single canned assumption lists with candidate branches.  Each branch
must state what assumptions it adds, what obligation it closes, and how the
derivation proceeds under those assumptions.  Each branch must also carry an
external-tool-first ledger recording tools considered, role, availability or
version evidence, selected route, and why any available tool was not used for
that branch.

### Phase 3: Formalization Stub And Backend Attempt Integration

Generate bounded SymPy/Sage/Lean formalization stubs when possible and attach
them to backend attempts.  Stub-only evidence remains non-certifying.

### Phase 4: Report Integration And Regression Gate

Make `audit_document_derivation_tree` render from the richer tree evidence.
Run generic fixtures and hard-document smoke reports to confirm reports improve
without card-specific logic.

## Non-Claims

- This master program is not a proof of any target document.
- This program does not claim global minimality of assumptions.
- This program does not authorize release readiness.
- This program does not permit agent prose to replace deterministic backend
  checks when a backend can be used.

## Stop Conditions

Stop and write a blocker result if:

- a phase needs package installation, network fetch, credentials, or
  environment mutation not already approved;
- Claude and Codex review do not converge after five rounds for the same
  material blocker;
- a proposed implementation would modify unrelated dirty worktree changes;
- a report improvement requires weakening proof-claim boundaries;
- a backend output cannot be captured in a bounded artifact.
