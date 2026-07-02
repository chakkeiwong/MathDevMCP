# Tool Improvement Master Program

Date: 2026-07-02

Status: `DRAFT_FOR_VISIBLE_GATED_EXECUTION`

## Objective

Improve MathDevMCP so coding agents can use concrete tools, not only prose, for
high-level mathematical work:

- derive a target from assumptions or givens;
- prove a claim or produce a counterexample;
- identify assumptions required for a route;
- localize the first failing derivation step;
- audit whether code implements documented math;
- prepare self-contained review packets without overclaiming proof.

The repaired downstream-agent benchmark is a local diagnostic and regression
harness. It is not a promotion claim.

## Current Baseline

The repaired downstream-agent benchmark is valid as a local diagnostic:

- A required passes: 8/9;
- B required passes: 9/9;
- C required passes: 9/9;
- hard vetoes: A = 0, B = 0, C = 0;
- C improves over A only on the Joseph backend-certificate case;
- C ties B under the frozen rubric;
- no C-over-B promotion is supported.

Key baseline artifacts:

- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
- `docs/plans/mathdevmcp-tool-improvement-plan-from-downstream-benchmark-2026-07-02.md`
- `docs/plans/mathdevmcp-benchmark-maintenance-handoff-2026-07-02.md`

## Role Contract

Codex is supervisor and executor.

Claude Opus may be used as a read-only reviewer for material subplans,
implementation diffs, blockers, and final decisions. Claude is not an execution
authority and cannot approve crossing human, runtime, model-file, funding,
product-capability, release, public-benchmark, or scientific-claim boundaries.

## Phase Index

| Phase | Name | Subplan |
| --- | --- | --- |
| 0 | Governance Baseline And Launch | `docs/plans/mathdevmcp-tool-improvement-phase-00-governance-baseline-subplan-2026-07-02.md` |
| 1 | Workflow Evidence Ledger | `docs/plans/mathdevmcp-tool-improvement-phase-01-evidence-ledger-subplan-2026-07-02.md` |
| 2 | Assumption Route Taxonomy | `docs/plans/mathdevmcp-tool-improvement-phase-02-assumption-taxonomy-subplan-2026-07-02.md` |
| 3 | Proof And Counterexample Evidence | `docs/plans/mathdevmcp-tool-improvement-phase-03-proof-counterexample-evidence-subplan-2026-07-02.md` |
| 4 | Derive-From Route Plans | `docs/plans/mathdevmcp-tool-improvement-phase-04-derive-route-plans-subplan-2026-07-02.md` |
| 5 | Math-To-Code Trace Artifacts | `docs/plans/mathdevmcp-tool-improvement-phase-05-math-code-trace-subplan-2026-07-02.md` |
| 6 | Review Packet Compiler | `docs/plans/mathdevmcp-tool-improvement-phase-06-review-packet-compiler-subplan-2026-07-02.md` |
| 7 | MCP And CLI Surface Alignment | `docs/plans/mathdevmcp-tool-improvement-phase-07-mcp-cli-alignment-subplan-2026-07-02.md` |
| 8 | Benchmark-Guided Regression Closeout | `docs/plans/mathdevmcp-tool-improvement-phase-08-benchmark-regression-subplan-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can targeted implementation work improve MathDevMCP high-level mathematical workflows without weakening evidence boundaries? |
| Baseline/comparator | Current high-level workflow modules and repaired downstream-agent benchmark result. |
| Primary pass criterion | Each executed phase adds structured or executable evidence paths, focused tests, and bounded result artifacts while preserving non-claim discipline. |
| Veto diagnostics | Prose-only capability disguised as proof; backend diagnostics promoted to semantic truth; hidden assumptions; post-hoc benchmark/rubric mutation; tool APIs not exposed; unrelated refactor; release/public/scientific/product/general-reliability claim. |
| Explanatory diagnostics | Per-workflow unit tests, MCP facade/server checks, high-level workflow quality report, repaired benchmark regression notes. |
| Not concluded | No public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped certified obligations, or general model reliability. |
| Artifacts | Phase subplans/results, visible execution ledger, Claude review trail, stop handoff, implementation diffs, local check outputs. |

## Sequencing Rationale

Phase 1 comes before all workflow implementation because downstream-agent
usefulness depends on a richer shared evidence envelope.

Phase 2 comes before proof and derivation improvements because assumption
typing is reused by proof, derivation, and review packet outputs.

Phase 3 comes before Phase 4 because derive-from should reuse proof or
counterexample evidence rather than duplicating route logic.

Phase 5 is independent enough to follow derivation work but precedes review
packet compilation, which should be able to include math-to-code traces.

Phase 6 compiles outputs from earlier phases. Phase 7 exposes them through MCP
and CLI surfaces. Phase 8 performs regression closeout after implementation is
complete.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use repaired benchmark as diagnostic baseline | Repaired collection result | It is valid locally and preserves original artifacts | Ceiling effect hides C-vs-B differences | Phase 0 inventory and result note | Baseline |
| Keep frozen rubric for existing repaired result | Phase 1 downstream benchmark rubric | Prevents post-hoc promotion drift | New implementation tuned to old scoring only | Separate benchmark v2 handoff | Reviewed baseline |
| Start with envelope and assumption taxonomy | Tool improvement plan | Shared structure reduces duplicate ad hoc prose | Over-engineered schema without workflow value | Focused tests per workflow | Hypothesis |
| Use optional backend checks conservatively | Existing SymPy/Lean/Sage policy | Prevents hallucinated proof claims | Backend unavailable misread as false claim | Doctor/backend-unavailable tests | Reviewed default |
| Claude as reviewer only | User instruction and cross-agent policy | Provides critique without delegating execution | Claude treated as authority | Review trail must preserve verdict and Codex decision | Reviewed default |

## Forbidden Claims And Actions

- Do not claim release readiness, product capability, public benchmark validity,
  scientific validation, broad theorem proving, proof correctness beyond scoped
  certified obligations, or general model reliability.
- Do not mutate the repaired benchmark baseline to make implementation look
  better.
- Do not change pass/fail criteria after seeing results.
- Do not use Claude as an executor, response worker, or boundary authority.
- Do not treat structural, diagnostic, finite-probe, or review-packet evidence
  as proof.
- Do not install packages, fetch network resources, run destructive git
  commands, or alter unrelated dirty work without explicit approval.

## Phase-End Protocol

At the end of every phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material plans/results when available;
6. patch fixable issues visibly and rerun focused checks;
7. stop after five Claude review rounds for the same blocker.

## Overall Stop Conditions

Stop and write a visible handoff if:

- a phase would require a human decision outside this plan;
- a backend/runtime/model-file/funding/product/scientific boundary is reached;
- Claude and Codex do not converge after five review rounds on the same
  material blocker;
- local checks fail in a way that invalidates the phase artifact;
- continuing would require destructive operations or unrelated worktree
  changes.
