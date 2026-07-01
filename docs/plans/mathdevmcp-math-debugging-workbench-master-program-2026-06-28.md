# MathDevMCP Mathematical Debugging Workbench Master Program

## Status

`DRAFT_FOR_VISIBLE_GATED_EXECUTION`

## Program Objective

Turn MathDevMCP from a mostly document-audit and release-gate oriented repo
into a question-centered mathematical debugging workbench.

Target user questions:

- Can I derive `X` from `Y`?
- Can we prove `X`, or find a counterexample?
- What assumptions are required for `X`?
- Where does this derivation stop being justified?
- Does this code implement this equation?
- What downstream math, code, tests, and claims are affected by changing this
  equation?

## Core Invariant

No workflow may answer with prose-only mathematical confidence. Every high-level
answer must decompose into explicit obligations, assumptions, backend attempts,
counterexamples, code/doc evidence, or abstentions. Only deterministic backend
certificates for scoped obligations may certify a mathematical claim.

## Non-Goals

- No release-readiness claim.
- No benchmark-gate activation.
- No claim that broad natural language proof search is solved.
- No claim that numeric probing proves identities.
- No default-policy movement for external projects.
- No replacement for human mathematical review on unsupported obligations.

## Phase Index

| Phase | Name | Primary Function | Subplan |
| --- | --- | --- | --- |
| 0 | Governance and Baseline Audit | Program safety and current surface audit | `docs/plans/mathdevmcp-math-debugging-workbench-phase-00-governance-baseline-subplan-2026-06-28.md` |
| 1 | Common Workbench Kernel | Shared schemas and statuses | `docs/plans/mathdevmcp-math-debugging-workbench-phase-01-common-kernel-subplan-2026-06-28.md` |
| 2 | Backend Router | Route obligations to safe backends | `docs/plans/mathdevmcp-math-debugging-workbench-phase-02-backend-router-subplan-2026-06-28.md` |
| 3 | Counterexample Search | Find concrete refutations | `docs/plans/mathdevmcp-math-debugging-workbench-phase-03-counterexample-search-subplan-2026-06-28.md` |
| 4 | Assumption Discovery | Report required or sufficient assumptions | `docs/plans/mathdevmcp-math-debugging-workbench-phase-04-assumption-discovery-subplan-2026-06-28.md` |
| 5 | Derive Or Refute | Derive target from givens or explain failure | `docs/plans/mathdevmcp-math-debugging-workbench-phase-05-derive-or-refute-subplan-2026-06-28.md` |
| 6 | Prove Or Refute | Prove theorem/identity or refute it | `docs/plans/mathdevmcp-math-debugging-workbench-phase-06-prove-or-refute-subplan-2026-06-28.md` |
| 7 | Proof Gap Localization | Identify first unjustified step | `docs/plans/mathdevmcp-math-debugging-workbench-phase-07-proof-gap-localization-subplan-2026-06-28.md` |
| 8 | Code Implements Equation | Compare code to math obligation | `docs/plans/mathdevmcp-math-debugging-workbench-phase-08-code-implements-equation-subplan-2026-06-28.md` |
| 9 | Claim Classification | Classify support status of claims | `docs/plans/mathdevmcp-math-debugging-workbench-phase-09-claim-classification-subplan-2026-06-28.md` |
| 10 | Notation Reconciliation | Detect convention and alias conflicts | `docs/plans/mathdevmcp-math-debugging-workbench-phase-10-notation-reconciliation-subplan-2026-06-28.md` |
| 11 | Generate Tests From Math | Emit diagnostic test plans or pytest snippets | `docs/plans/mathdevmcp-math-debugging-workbench-phase-11-generate-tests-from-math-subplan-2026-06-28.md` |
| 12 | Human Review Packet | Compact evidence packet for reviewers | `docs/plans/mathdevmcp-math-debugging-workbench-phase-12-human-review-packet-subplan-2026-06-28.md` |
| 13 | Mathematical Change Impact | Trace downstream impact of changed math | `docs/plans/mathdevmcp-math-debugging-workbench-phase-13-change-impact-subplan-2026-06-28.md` |
| 14 | Literature To Local Audit | Compare theorem assumptions to local setting | `docs/plans/mathdevmcp-math-debugging-workbench-phase-14-literature-local-audit-subplan-2026-06-28.md` |
| 15 | Operator UX And Regression Closure | Docs, CLI/MCP sync, regression suite | `docs/plans/mathdevmcp-math-debugging-workbench-phase-15-operator-ux-regression-subplan-2026-06-28.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP expose a coherent mathematical debugging workbench for derivation, proof/refutation, assumptions, code matching, and review packets without weakening certification boundaries? |
| Baseline/comparator | Current low-level tools: `derive_step`, `check_proof_obligation`, `audit_derivation_v2_label`, `typed_obligation_label`, `proof_packet`, `lean_check`, symbolic/numeric diagnostics, and code-document audit helpers. |
| Primary pass criterion | All planned user-facing workflows have reviewed schemas, local tests, CLI/MCP exposure where appropriate, and conservative evidence boundaries. |
| Veto diagnostics | Any prose-only proof claim, numeric evidence promoted to proof, unsupported backend treated as refutation, release/gate/readiness claim, hidden assumption promotion, or broad semantic proof-search claim. |
| Explanatory diagnostics | Focused pytest results, CLI smoke outputs, MCP surface sync, seeded fixtures, and Claude read-only review. |
| Not concluded | Mathematical completeness, scientific validity, benchmark generalization, release readiness, autonomous formal proof generation, or theorem applicability beyond checked assumptions. |
| Artifacts | Phase subplans/results, visible execution ledger, Claude review trail, code/tests/docs diffs, final stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure Mode | Early Diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use existing `check_proof_obligation` before new backends | Current repo | Preserves deterministic SymPy/normalizer behavior | Misses non-scalar or richer logic | Seed scalar true/false tests | Reviewed baseline |
| Treat Sage/Z3/Lean as optional routes | Current support matrix | Avoids depending on unavailable tooling | Tool unavailable could be misread as false | Backend availability status in result | Reviewed baseline |
| Start with conservative schemas and composition | Current release policy | Reduces blast radius | Workflows may initially abstain often | Tests require explicit abstention reasons | Reviewed baseline |
| Numeric counterexamples are refutation evidence only when evaluated concretely | Scientific policy | Prevents simulation as proof | Random probe could be overclaimed | Store assignments, lhs/rhs values, seed | Reviewed baseline |
| Assumption discovery reports route-required or sufficient assumptions by default | Scientific policy | Necessity is hard to prove | Overclaiming necessary assumptions | Status field distinguishes required/sufficient/unknown | Reviewed default |

## Execution Rules

- Codex is the supervisor and executor.
- Claude Opus max effort may review material subplans, diffs, and results as a
  read-only reviewer only.
- Claude cannot authorize human, runtime, model-file, funding, product,
  release, or scientific-claim boundary crossings.
- If Claude review returns a fixable `REVISE`, patch visibly, rerun focused
  checks, and retry up to five rounds for the same blocker.
- If Claude does not respond, run a small probe. If the probe responds, redesign
  the prompt and retry with a smaller review brief.
- Do not stop for vague uncertainty. Stop only for explicit stop conditions,
  failed gates that cannot be repaired locally, or human-required boundaries.

## Phase Completion Protocol

At the end of each phase:

1. Run required local checks.
2. Write a phase result or blocker record.
3. Draft or refresh the next phase subplan.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
5. Use Claude read-only review for material subplans or material changes.
