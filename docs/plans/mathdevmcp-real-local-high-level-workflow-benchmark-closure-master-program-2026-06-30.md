# MathDevMCP Real-Local High-Level Workflow Benchmark Closure Master Program

Date: 2026-06-30

Status: `REVISED_AFTER_CLAUDE_R1`

## Program Objective

Close the gap between seeded high-level workflow tests and realistic
derivation/proof usage by building a real-local benchmark from local repo
materials, running the current workflows honestly against it, and repairing the
workflow layer only against observed evidence-backed failures.

Target operator questions:

- Can I derive `X` from `Y`?
- Can we prove `X`, refute it, or find a counterexample?
- What assumptions are required for `X`?
- Where does this derivation first fail?
- Does this code implement this equation or derivation?
- Can I get a durable review packet with sources, assumptions, checks, gaps,
  and non-claims?

## Baseline

The predecessor high-level workflow program completed on seeded cases with:

- benchmark gate `70/70`;
- high-level workflow benchmark `14/14`;
- six high-level workflow surfaces implemented;
- explicit residual risk that real local tasks still need collection and
  evaluation.

The predecessor source-adapter runbook completed with:

- frozen local manifest preserved as `partial`;
- governed repaired manifest closing `RLHL-04` locally/non-gating;
- no benchmark-gate or release-readiness promotion.

## Core Invariants

- LLM prose is never proof.
- Backend unavailable is not refutation.
- Numeric, structural, generated-test, and review-packet evidence is diagnostic
  unless linked to a certifying backend or source-anchored local schema.
- Source/probe/backend/residual ledgers stay separate.
- Real-local materials remain local/non-gating unless a later reviewed
  promotion policy explicitly changes that.
- No public benchmark validity, release readiness, scientific validation,
  production correctness, or broad theorem-proving claim is made.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Current Baseline | Freeze current high-level workflow, source-adapter, and benchmark state. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-00-governance-current-baseline-subplan-2026-06-30.md` |
| 1 | Real Local Case Inventory | Inventory 5-10 candidate cases from local repos without copying large source text. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-01-real-local-case-inventory-subplan-2026-06-30.md` |
| 2 | Benchmark Schema And Rubric | Define durable case schema, scoring rubric, negative controls, and quality metrics. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-02-benchmark-schema-rubric-subplan-2026-06-30.md` |
| 3 | Backend Grounding Evidence Layer | Strengthen evidence routing to source adapters, symbolic checks, counterexample search, and abstention. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-03-backend-grounding-evidence-subplan-2026-06-30.md` |
| 4 | Current Workflow Baseline Run | Run existing workflows on the new benchmark before capability repairs. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-04-current-workflow-baseline-run-subplan-2026-06-30.md` |
| 5 | Targeted Capability Repairs | Repair `assumptions_for`, `derive_from`, `prove_or_counterexample`, `debug_derivation`, `audit_math_to_code`, and `prepare_review_packet` against observed failures. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-05-targeted-capability-repairs-subplan-2026-06-30.md` |
| 6 | Derivation And Proof Packet Standard | Standardize durable review packets for benchmarked high-level answers. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-06-derivation-proof-packet-standard-subplan-2026-06-30.md` |
| 7 | Promotion Policy And Operator Docs | Decide and document local/non-gating versus candidate benchmark-gate policy. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-07-promotion-policy-operator-docs-subplan-2026-06-30.md` |
| 8 | Final Regression And Handoff | Run final checks, write reports, and state residual gaps/non-claims. | `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-08-final-regression-handoff-subplan-2026-06-30.md` |

## Mandatory Cross-Phase Artifacts

- Baseline freeze manifest from Phase 0 with exact manifests, commands, scorer
  or runner versions, backend/adapter availability state, expected seeded
  verdict snapshots, and dirty-worktree boundary.
- Candidate coverage matrix from Phase 1 covering workflow type, route type,
  outcome type, source family, negative-control status, and expected evidence.
- Minimal review-packet schema from Phase 2 so pre-repair and post-repair runs
  emit comparable evidence.
- Route-availability ledger from Phase 3 with source adapter present/absent,
  symbolic backend present/absent, counterexample path attempted/skipped,
  proof/formal backend state, and residual unresolved per case.
- Current-workflow baseline report from Phase 4 with per-workflow evidence
  contracts, good-abstention semantics, and no post-hoc criteria changes.
- Anti-overfitting rerun set from Phase 5: unchanged seeded regression plus
  preregistered cross-case rerun cases before accepting repairs.
- Final matrix from Phase 8 with per case: expected route, actual route,
  verdict, failure class, repair round, remaining limitation, and whether the
  case is local-regression-only or future governed benchmark candidate.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP make its high-level derivation/proof workflows useful on realistic local repo cases while preserving source/tool evidence boundaries? |
| Baseline/comparator | Seeded high-level workflow program result plus source-adapter Phase 11 addendum; no real-local high-level benchmark closure yet. |
| Primary pass criterion | A 5-10 case real-local high-level workflow benchmark exists; current baseline results are recorded; targeted repairs improve or correctly abstain on observed failures; final reports preserve source/backend/probe/residual ledgers and non-claims. |
| Veto diagnostics | LLM prose treated as proof; backend absence treated as refutation; source snippets overcaptured; source/probe/backend ledgers collapsed; benchmark pass promoted to release/scientific/public validity; repaired behavior hides residual gaps; scoring uses only an aggregate pass rate; artifact does not answer the phase question; local closure promoted to default policy. |
| Explanatory diagnostics | Case inventory coverage, benchmark quality metrics, focused pytest, CLI reports, per-case workflow reports, negative controls, mutation probes, docs/forbidden-claim grep, Claude read-only review where available. |
| Not concluded | Release readiness, public benchmark validity, scientific validation, production implementation correctness, external reproducibility, full LaTeX proof checking, or broad theorem proving. |
| Preserved artifacts | Master program, phase subplans/results, visible runbook, ledger, review trail, benchmark manifest/report, repaired code/tests/docs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Real-local benchmark before repairs | Prior high-level handoff next step | Prevents abstract feature work from substituting for operator evidence | Cases may be too easy or too narrow | Phase 1 coverage table and Phase 2 quality rubric | Reviewed default |
| 5-10 local cases | User request and repo/source availability | Enough to expose realistic gaps without becoming an open-ended corpus effort | Overfitting or cherry-picking | Negative controls and source-family diversity checks | Baseline target |
| Local-only source anchors | Source-adapter governance | Avoids public redistributability and source-copy issues | Portability confusion | Path/provenance ledger and no-wholesale-copy checks | Reviewed default |
| Existing workflows as baseline | Completed high-level program | Measures current product surface before modifying it | Baseline may look worse than seeded tests | Phase 4 baseline result is diagnostic, not failure of idea | Reviewed baseline |
| Targeted repairs only after failure table | Scientific coding policy | Prevents changing defaults after seeing vague results | Repairs could chase metrics | Per-case failure taxonomy and non-claim checks | Reviewed default |
| Claude read-only reviewer | User instruction | Independent critique of material subplans | Tenant policy may block repo-derived review prompts | Compact sanitized prompts; record blocker if blocked | Conditional reviewer |

## Benchmark Evidence Semantics

Each workflow family must have a pre-run evidence contract before Phase 4:

- comparator;
- primary pass/fail criterion;
- veto diagnostics;
- explanatory-only diagnostics;
- good-abstention definition;
- forbidden claims.

Negative controls must predeclare expected status and scoring semantics:

- `refuted` only when a scoped backend/source route supplies a valid
  counterexample or contradiction;
- `missing_assumptions` or `insufficient_evidence` when assumptions are absent;
- `backend_unavailable` when the route is known but unavailable;
- `not_encodable` when the current grammar cannot represent the question;
- routing-only tests cannot be counted as mathematical correctness.

Good abstention means the workflow identifies the unavailable or insufficient
evidence route, preserves non-claims, and gives the smallest justified next
action without pretending to prove or refute the claim.

## Repair Loop

- Codex is supervisor and executor.
- Claude Opus max effort is read-only reviewer only where tenant policy permits.
- Claude cannot authorize crossing human, runtime, model-file, funding,
  product-capability, release-policy, source-repository, or scientific-claim
  boundaries.
- If Claude returns `REVISE`, patch the same artifact visibly, rerun focused
  checks, and retry up to five rounds for the same blocker.
- If Claude does not respond, run a tiny probe. If the probe responds, redesign
  the prompt smaller. Claude silence is never approval.
- If Claude review is blocked by policy, record the block and use only local
  Codex review if the runbook explicitly permits it; otherwise write a blocker
  result and stop for human direction.
- Stop after five review rounds for the same blocker.

## Claude Review Trail

- R1 verdict: `REVISE`.
- R1 repairs applied: stronger baseline freeze artifact contract; workflow
  family evidence contracts before Phase 4; case coverage matrix requirement;
  predeclared negative-control semantics; Phase 3 route-availability ledger;
  Phase 5 anti-overfitting rerun guard; minimal packet schema moved earlier to
  Phase 2; stronger no-promotion boundary; artifact-does-not-answer stop
  condition; Phase 8 final matrix requirement.

## Phase Completion Protocol

At the end of each phase:

1. run the required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans/results when available
   and safe.
