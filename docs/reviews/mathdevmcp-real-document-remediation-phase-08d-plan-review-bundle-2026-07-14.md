# MathDevMCP Phase 08D Plan Review

Date: 2026-07-14
Review name: `mathdevmcp-p08d-plan-r1`
Supervisor/executor: Codex
Reviewer: Claude Opus, max effort, read-only

## Role Boundary

Do not edit files, run commands, launch agents, or authorize implementation,
publication, release, scientific claims, or any other boundary crossing. Codex
remains supervisor and executor.

## Objective

Decide whether the repaired P08D plan is safe and sufficiently specified to
implement a compact, artifact-backed response and public resolver for the exact
target-faithful P08C1 audits, without semantic loss or byte-limit evasion.

## Inspect Only

1. `docs/plans/mathdevmcp-real-document-remediation-phase-08d-p08c1-bound-compact-payload-repair-subplan-2026-07-14.md:22-181`
   for baseline, skeptical/default audits, measurements, and evidence contract.
2. The same plan at lines `183-389` for the closed v2 response/token/resolver
   contracts, checks, forbidden actions, and stop/handoff conditions.
3. `docs/plans/p08d_payload_feasibility_spike_20260714.py:21-107` for frozen
   identities, schemas, limits, and token layout.
4. The same program's functions named `build_v1_comparator`,
   `load_verified_artifact`, `verify_compact_comparator`, `project_action`,
   `encode_token`, `decode_token`, `partition_pages`, `resolve_records`, and
   `main`. Inspect only those functions and directly called local helpers when
   needed to answer the questions below.

Fresh local execution returned `PASS_P08C1_BOUND_P08D_FEASIBILITY` with a
236-byte/315-character token, five source-order pages, 52 card resolver pages,
38 risky resolver pages, 210-byte smallest canonical page margin, and 12-byte
smallest resolver full-wire margin. `py_compile` and scoped
`git diff --check` pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can this plan be implemented and tested without losing or misbinding any exact P08C1 target, claim-boundary identity, action, obligation, or resolvable record while satisfying both byte limits? |
| Baseline | Exact P08C1 audit/request identities, exact P08A obligation bindings, fresh verified v1 artifacts, and v1 compact semantic projections named in the plan. P08C is explicitly invalid as a semantic baseline. |
| Primary criterion | Every deterministic page and resolver page fits; ordered page and resolver unions reconstruct the verified persisted audit exactly; tokens authorize only recomputed page/scope boundaries; no-artifact mode preserves all targets. |
| Veto diagnostics | Wrong baseline; proxy size treated as semantic success; forgeable or ambiguous token; lossy action/obligation/table representation; unresolved record; unmeasured public wire; path leak; v1/v2 confusion; missing failure/stop condition; hidden backend, publication, or authority transfer. |
| Explanatory only | Compression ratio, page count, resolver count, and positive margins. |
| Not concluded | Mathematical truth, whole-document correctness, best repair, general compactness, publication/default/release readiness, Phase 08 closure, or mission completion. |

## Review Questions

1. Can the specified token or partition validation accept a forged,
   cross-artifact, cross-filter, cross-page, or non-boundary capability?
2. Can the registered/inline action forms, identity tables, content identities,
   or resolver collections lose or misbind any raw P08C1 semantic record while
   tests still pass?
3. Does byte-aware fill account for every required public representation,
   including fixed FastMCP content and full stdio JSON-RPC, without treating
   byte size as a proxy for semantic validity?
4. Are no-artifact compatibility, v1 rejection/migration, one-record overflow,
   empty collections, privacy, and automatic stop/handoff conditions explicit
   enough to implement without inventing a material API or claim decision?
5. Is any material default, comparator, environment assumption, artifact, or
   test missing before implementation may start?

Report only material findings with file/line or function references. Style and
the already stated non-claims are non-findings. End with exactly one line:

`VERDICT: AGREE` or `VERDICT: REVISE`.
