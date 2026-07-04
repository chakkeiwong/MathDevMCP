# MathDevMCP Downstream-Agent Usefulness Master Program

Date: 2026-07-01

Status: `LAUNCHED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

## Program Objective

Measure and improve whether MathDevMCP high-level workflow packets help a
downstream agent do mathematically useful work on governed local tasks.

The concrete target is not merely that packets are well formed. The target is
to establish, under bounded local evidence, whether packet-backed handoffs
improve downstream-agent task performance for questions such as:

- can I derive X from Y;
- can we prove X or find a counterexample;
- what assumptions are required for X;
- where does this derivation or proof fail;
- does this code implement this math;
- can a self-contained packet help another agent continue the work.

This program may produce an internal promotion recommendation only if the
evidence supports it. It must not claim public benchmark validity, scientific
validation, release readiness, product capability, broad theorem proving, or
general model reliability.

## Starting Point

The repository already has:

- high-level workflow implementations and local tests;
- real-local high-level workflow benchmark cases and durable packet reports;
- a reusable agent-handoff packet builder/validator;
- a frozen local packet-standard candidate;
- a prior small A/B/C packet calibration where `C_human_framed` tied
  `B_evidence_only` numerically and was frozen only as a local candidate
  because it preserves evidence while adding context.

The remaining gap is downstream-agent usefulness: whether a downstream agent
actually performs better when given the structured packet, compared with task
only or evidence-only prompts, under a predeclared scoring contract.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review compact
briefs, subplans, diffs, result summaries, and boundary wording. Claude must
not edit files, run commands, launch agents, collect responses, score as final
authority, approve boundary crossings, or authorize promotion claims.

Downstream response workers, if used, must be Codex subagents or another
explicitly approved non-Claude model/agent surface. Claude must not be used as
a response worker.

## Initial Claude Review Availability

Initial compact Claude review and a tiny liveness probe were attempted through
the read-only worker wrapper. Neither returned usable output. This is recorded
as reviewer unavailable, not as approval.

Until Claude responds again, launch may proceed only under Codex skeptical
review plus required local checks. Material phases that cross response
collection, scoring, repair, or final-promotion decisions must still attempt
Claude review again or explicitly record reviewer unavailability before
advancing.

## Human Approval Boundaries

This program is approved to draft plans, run local checks, inspect local repo
artifacts, and use Claude as read-only reviewer as requested.

This program must stop for explicit human approval before:

- collecting new downstream-agent/model responses beyond existing frozen
  artifacts;
- reading or summarizing non-current repositories under `~/python` into new
  benchmark cases if the phase would copy substantial source text rather than
  create bounded local summaries;
- installing packages, fetching network data, changing model files, using paid
  external APIs beyond Claude review, or using credentials;
- changing release/default benchmark policy;
- making scientific, public benchmark, product, or general model-reliability
  claims.

## Core Invariants

- Separate packet quality from downstream-agent task improvement.
- Separate downstream-agent task improvement from mathematical certification.
- Preserve backend evidence class: certified, diagnostic, unavailable, or not
  encodable.
- Record malformed or incomplete downstream responses instead of replacing
  them.
- Use no hidden retries.
- Keep A/B/C prompt variants frozen before response collection.
- Score with predeclared rubrics only.
- Keep per-case evidence visible; no aggregate-only promotion.
- Do not mutate pass/fail criteria after seeing responses.
- Preserve unrelated dirty worktree changes.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | Freeze current repo state, existing benchmark/packet artifacts, approval boundaries, and baseline checks. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-subplan-2026-07-01.md` |
| 1 | Usefulness Contract And Rubric | Define benchmark question, A/B/C comparators, scoring rubric, vetoes, response contract, and promotion/non-claim policy. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-subplan-2026-07-01.md` |
| 2 | Case Corpus And Fixture Design | Select or design governed local cases across workflows, including expected evidence classes and source-summary boundaries. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-subplan-2026-07-01.md` |
| 3 | Prompt Harness And Collection Gate | Build or validate frozen prompt/harness artifacts and stop for response-collection approval if not already granted. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-subplan-2026-07-01.md` |
| 4 | Response Collection And Scoring | Collect approved downstream responses with no hidden retries, score them, and preserve malformed outputs. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-subplan-2026-07-01.md` |
| 5 | Failure Taxonomy And Capability Repairs | Convert scored failures into targeted workflow, packet, routing, or documentation repairs with focused tests. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-subplan-2026-07-01.md` |
| 6 | Regression And Promotion Decision | Rerun local gates and decide whether evidence supports internal promotion, revision, expansion, or blocker. | `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-subplan-2026-07-01.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do MathDevMCP high-level workflow packets measurably improve downstream-agent task performance on governed local math tasks, without boundary overclaims? |
| Baseline/comparator | A/B/C prompt conditions: task-only, evidence-only or machine-evidence packet, and human-framed agent-handoff packet. Existing packet-standardization artifacts are design input, not proof of usefulness. |
| Primary pass criterion | A predeclared downstream-agent usefulness benchmark is implemented or precisely blocked; if response collection is approved, scored results show whether C improves task/evidence quality without hard-veto regressions. |
| Veto diagnostics | Hidden retries; changed rubric after seeing responses; Claude used as response worker or authority; malformed outputs replaced; aggregate-only promotion; packet quality proxy treated as task success; C-over-B overclaim; diagnostic evidence treated as proof; missing source/evidence boundary; unapproved model/API use. |
| Explanatory diagnostics | Per-case score tables, response manifests, hard-veto counts, failure taxonomy, backend evidence-class coverage, prompt/packet completeness, focused tests, Claude read-only review findings. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, general model reliability, broad theorem proving, or proof correctness beyond backend-certified scoped obligations. |
| Preserved artifacts | Master program, phase subplans/results, visible runbook, ledger, stop handoff, Claude review trail, benchmark contracts, fixtures, prompts, manifests, responses if approved, scoring outputs, repair records, final decision. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| A/B/C comparator design | Prior packet calibration | Directly targets the C-vs-B usefulness gap | Reuses a small prior design too narrowly | Phase 1 rubric review | Baseline |
| Local governed cases first | Existing real-local benchmark policy | Keeps source boundaries auditable | Overfits to local examples | Phase 2 diversity and evidence-class matrix | Baseline |
| One response per prompt unless approved otherwise | Prior calibration discipline | Avoids hidden retries and cost drift | High variance | Phase 4 labels single-response evidence as diagnostic unless replicated | Constraint |
| Claude read-only review | User request and cross-agent policy | Independent boundary critique | Mistaken for authority | Review trail and Codex gate decision | Constraint |
| Codex or approved non-Claude response subjects | User policy from prior calibration | Keeps Claude out of worker role | Surface mismatch affects comparability | Phase 3 response-subject manifest | Hypothesis |
| Packet usefulness primary metric | User feedback | Directly tests whether packets help agents work | Subjective scoring drift | Phase 1 anchored rubric and hard vetoes | Hypothesis |

## Sequencing Guardrails

1. Phase 0 must complete before any new contract, case, or harness edits.
2. Phase 1 must freeze the scoring contract before cases are scored.
3. Phase 2 must freeze case fixtures before prompt variants are generated.
4. Phase 3 must freeze prompts and response-subject policy before response
   collection.
5. Phase 4 must not start response collection without explicit approval for
   the exact subject surface, prompt count, retry policy, and artifact paths.
6. Phase 5 may repair only after failures are classified against the frozen
   rubric.
7. Phase 6 may promote only the bounded internal claim supported by artifacts.

## Repair Loop

- Each phase starts with a skeptical audit.
- If a material flaw is found, patch the active subplan or artifact visibly.
- Run focused local checks after each patch.
- Send material subplans/results to Claude as compact read-only review briefs.
- If Claude returns `VERDICT: REVISE`, patch and retry up to five rounds for
  the same blocker.
- If Claude does not respond, run a tiny probe. If the probe responds, reduce
  and redesign the review prompt. Claude silence is never approval.
- If convergence fails after five rounds for the same blocker, write a blocker
  result and stop for human direction.

## Phase Completion Protocol

At the end of each phase:

1. run the required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. run Claude read-only review for material subplans unless Claude is
   unavailable and the unavailability is documented;
6. advance only when exact handoff conditions are met.
