# MathDevMCP High-Level Math Workflows Master Program

Date: `2026-06-29`

## Status

`DRAFT_FOR_VISIBLE_GATED_EXECUTION`

## Program Objective

Build and benchmark question-level mathematical workflows on top of the
existing MathDevMCP workbench tools. The workflows should answer common
operator questions such as:

- Can I derive `X` from `Y`?
- Can we prove `X`, or find a counterexample?
- What assumptions are required for `X`?
- Where does this derivation first fail?
- Does this code implement this equation?
- Can I get a review-ready packet for this question?

The program must rely on concrete local tools such as symbolic backends,
structured diagnostics, proof-gap localization, and code/equation comparison
where available. It must not use LLM prose as proof, and it must preserve
evidence boundaries.

## Core Invariant

The high-level workflows are orchestration and evidence packaging functions.
They do not create a general theorem prover.

They must preserve these boundaries:

- numeric evidence is diagnostic unless a certifying backend proves the claim;
- structural code/equation evidence is not semantic proof;
- backend unavailable is not refutation;
- missing assumptions are explicit and not silently inserted;
- generated tests and review packets are diagnostic/review aids;
- external benchmark success, release readiness, and broad theorem-proving
  ability are not concluded.

## High-Level Functions

| Function | User question | Required evidence behavior |
| --- | --- | --- |
| `derive_from` | Can I derive target from givens? | Return scoped proof, refutation/counterexample, missing assumptions, not-encodable, backend-unavailable, or inconclusive. |
| `prove_or_counterexample` | Can we prove this claim? | Use deterministic backend evidence where available; separate backend absence from refutation. |
| `assumptions_for` | What assumptions are required? | Return explicit assumptions with reasons and affected terms. |
| `debug_derivation` | Where does the derivation fail? | Localize first unsupported/refuted step without overclaiming global theorem failure. |
| `audit_math_to_code` | Does code implement the math? | Report structural match/mismatch and proof boundary. |
| `prepare_review_packet` | Give me a review-ready answer. | Aggregate evidence, non-claims, actions, and human-review boundaries. |

## Result Contract Targets

Every high-level workflow must return a stable envelope:

- `status`;
- `workflow`;
- `question`;
- `claim_class`;
- `answer`;
- `evidence`;
- `evidence_classes`;
- `certification_source`;
- `veto_reasons`;
- `assumptions`;
- `counterexamples`;
- `actions`;
- `non_claims`;
- `metadata`.

The status set is scoped:

- `proved`;
- `refuted`;
- `missing_assumptions`;
- `backend_unavailable`;
- `not_encodable`;
- `structural_match`;
- `structural_mismatch`;
- `diagnostic_only`;
- `gap_found`;
- `inconclusive`.

## Phase Index

| Phase | Name | Primary Function | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Baseline | Confirm current workbench/benchmark baseline and dirty-worktree boundaries | `docs/plans/mathdevmcp-high-level-math-workflows-phase-00-governance-baseline-subplan-2026-06-29.md` |
| 1 | Contract And Evidence Schema | Define high-level result contract, statuses, evidence classes, and non-claims | `docs/plans/mathdevmcp-high-level-math-workflows-phase-01-contract-evidence-schema-subplan-2026-06-29.md` |
| 2 | Orchestration Kernel | Add shared route/evidence orchestration helpers over existing tools | `docs/plans/mathdevmcp-high-level-math-workflows-phase-02-orchestration-kernel-subplan-2026-06-29.md` |
| 3 | Derive From Workflow | Implement `derive_from` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-03-derive-from-subplan-2026-06-29.md` |
| 4 | Prove Or Counterexample Workflow | Implement `prove_or_counterexample` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-04-prove-or-counterexample-subplan-2026-06-29.md` |
| 5 | Assumptions For Workflow | Implement `assumptions_for` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-05-assumptions-for-subplan-2026-06-29.md` |
| 6 | Debug Derivation Workflow | Implement `debug_derivation` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-06-debug-derivation-subplan-2026-06-29.md` |
| 7 | Audit Math To Code Workflow | Implement `audit_math_to_code` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-07-audit-math-to-code-subplan-2026-06-29.md` |
| 8 | Prepare Review Packet Workflow | Implement `prepare_review_packet` | `docs/plans/mathdevmcp-high-level-math-workflows-phase-08-prepare-review-packet-subplan-2026-06-29.md` |
| 9 | Question-Level Benchmark | Add high-level workflow benchmark and quality checks | `docs/plans/mathdevmcp-high-level-math-workflows-phase-09-question-level-benchmark-subplan-2026-06-29.md` |
| 10 | CLI And MCP Exposure | Expose high-level functions after benchmark pass | `docs/plans/mathdevmcp-high-level-math-workflows-phase-10-cli-mcp-exposure-subplan-2026-06-29.md` |
| 11 | Docs And Operator UX | Document high-level workflows and boundaries | `docs/plans/mathdevmcp-high-level-math-workflows-phase-11-docs-operator-ux-subplan-2026-06-29.md` |
| 12 | Final Regression And Handoff | Run final checks and write handoff | `docs/plans/mathdevmcp-high-level-math-workflows-phase-12-final-regression-handoff-subplan-2026-06-29.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP provide benchmarked high-level mathematical workflows that answer common derivation/proof/assumption/debug/code-review questions while preserving evidence boundaries? |
| Baseline/comparator | Existing lower-level workbench tools and seeded workbench benchmark: `math_debugging_workbench`, `workbench-benchmark-quality`, and formal benchmark gate. |
| Primary pass criterion | High-level workflows exist, share a stable evidence contract, are covered by question-level benchmark cases with false-confidence traps, and are exposed through CLI/MCP only after benchmark and quality checks pass. |
| Veto diagnostics | LLM/prose treated as proof; backend unavailable treated as refutation; numeric/structural/generated-test evidence promoted to proof; high-level benchmark pass rate used as sole quality signal; CLI/MCP exposed before benchmark pass. |
| Explanatory diagnostics | Unit tests, question-level benchmark report, mutation/negative-control checks, CLI/MCP tests, docs forbidden-claim grep, Claude read-only review. |
| Not concluded | General theorem proving, release readiness, external benchmark performance, scientific validity, or correctness beyond the stated scoped evidence. |
| Artifacts | Master program, phase subplans/results, visible runbook, ledger, Claude review trail, code/tests/docs, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Build high-level workflows as wrappers/orchestrators | Existing workbench tools already implement scoped primitive behaviors | Avoids duplicating proof/backend logic and preserves tested boundaries | Wrapper may overclaim by summarizing too aggressively | Contract tests for evidence classes and non-claims | Reviewed baseline |
| Question-level benchmark after workflow implementation | Previous workbench benchmark program established seeded gate/quality pattern | Tests user-facing behavior rather than only tool internals | Benchmark may overfit local seed cases | False-confidence traps and mutation checks | Reviewed baseline |
| CLI/MCP exposure after benchmark pass | User requested benchmarked higher-level usage functions | Prevents premature public API surface | Useful functions hidden until late phase | Phase 10 handoff requires Phase 9 pass | Reviewed default |
| No external data fetch | Current local/provenance and approval policy | High-level workflows can be tested with local seeded cases first | External benchmark adaptation remains future work | Phase 9 seeded-only benchmark and docs non-claims | Convenience choice |
| Claude read-only reviewer | User instruction and cross-agent policy | Independent critique without delegating execution | Claude hang or prompt block | Compact prompts, tiny probe, retry smaller prompt, max 5 rounds | Reviewed default |

## Promotion Thresholds

The high-level workflow benchmark may enter the formal benchmark report only if:

- every high-level function has at least two seeded question cases;
- every workflow has a baseline ladder covering refusal/insufficient-evidence,
  structural-only or diagnostic-only evidence, backend-certified positive cases
  where applicable, and backend-unavailable/non-claim cases where applicable;
- all result statuses in the scoped status set are exercised where applicable;
- at least `40%` of cases are negative controls or false-confidence traps;
- phase-local negative controls for each workflow have already passed before
  the integrated benchmark;
- deterministic rerun preserves case ids, statuses, pass/fail, evidence classes,
  and non-claims;
- mutation probes detect at least:
  - backend unavailable promoted to refutation;
  - structural match promoted to proof;
  - numeric/generated-test evidence promoted to proof;
  - missing assumptions silently promoted to proof;
  - review packet promoted to certificate;
- the report records non-claims and a run manifest.

Automatic benchmark vetoes:

- any output implying release readiness;
- any output implying broad theorem-proving ability;
- any output treating prose as proof;
- any output treating backend unavailable as refutation;
- any output promoting structural/numeric/generated-test/review-packet evidence
  to proof without a certifying backend.

`assumptions_for` and `debug_derivation` require set/rubric-based scoring
rather than brittle single-string gold answers. `prepare_review_packet` is
scored on evidence completeness, provenance, uncertainty/actionability, and
boundary preservation rather than a single "correct answer" string.

## Execution Rules

- Codex is supervisor and executor.
- Claude Opus max effort is read-only reviewer only.
- Claude cannot authorize human, runtime, model-file, funding, product,
  release, or scientific-claim boundary crossings.
- If Claude returns `REVISE`, patch visibly, rerun focused checks, and retry up
  to five rounds for the same blocker.
- If Claude does not respond, run a tiny probe. If the probe responds, redesign
  the prompt and retry smaller.
- Claude silence is never approval. A probe is only liveness debugging. If
  review cannot produce an explicit verdict after the allowed repair/probe
  loop, write a blocker or proceed only when the runbook explicitly allows
  reviewer-unavailable continuation and local gates answer the same question.
- After five failed review/repair rounds for the same blocker, stop hard, write
  a blocked-phase result and failure packet, and do not advance.
- Stop only for explicit stop conditions, failed gates that cannot be repaired
  locally, or human-required boundaries.

## Phase Completion Protocol

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans/results when feasible.
