# Downstream-Agent Usefulness V2 Collection And Scoring Master Program

Date: 2026-07-03

Status: `COMPLETE_BOUNDED_LOCAL_DIAGNOSTIC_FINAL_REVIEW_AGREED`

## Program Objective

Close the remaining empirical and governance gaps for the downstream-agent
usefulness v2 benchmark candidate:

- freeze the response-collection approval packet;
- freeze the scoring contract before any collection;
- run final preflight checks;
- collect and score responses only if explicit human approval names the
  response-worker surface, retry policy, malformed-output policy, scoring
  contract, and artifact paths;
- run Claude read-only review gates on material plans/results;
- stop with a bounded decision that does not overclaim beyond local diagnostic
  evidence.

This program is separate from the v2 benchmark-construction program, which
closed with a validated candidate and Claude `VERDICT=AGREE`.

Mission alignment:

- Canonical mission spine:
  `docs/plans/mathdevmcp-mission-charter.md`.
- Anti-drift gate:
  `docs/plans/mathdevmcp-anti-drift-gate.md`.
- Evidence-to-implementation ledger:
  `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`.

This collection/scoring program is an evidence instrument. Its product purpose
is to decide whether MathDevMCP should invest in richer
review-packet/handoff-packet generation for downstream agents. It is not a
goal to keep iterating benchmarks for their own sake.

## Starting Point

The v2 candidate is ready for human collection approval:

- candidate cases: 6;
- prompt fixtures: 18;
- prompt validation errors: 0;
- v2 response artifacts: 0;
- Claude review gate: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`;
- future collection runbook:
  `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`.

The repaired baseline remains frozen under
`.mathdevmcp/downstream_agent_usefulness/`. V2 candidate artifacts remain under
`.mathdevmcp/downstream_agent_usefulness_v2/`.

## Current Continuation State

As of the 2026-07-04 continuation, the workspace contains a later local
collection/scoring state:

- collection authorization record status:
  `collection_authorized_by_current_human_approval_for_exact_scope`;
- prompt manifest hash:
  `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe`;
- prompt count: 18;
- response manifest count: 18;
- scored row count: 18;
- Claude response-worker markers: 0;
- retry issues: 0;
- prompt validation errors: 0;
- hard vetoes A/B/C: 0/0/0;
- required passes A/B/C: 6/5/6.

This later state supersedes the earlier Phase 2 stop as the current workspace
state, but it does not erase the historical Phase 2 stop record. The current
result is a bounded local diagnostic. Sonnet max read-only final-state review
converged with `REVIEW_STATUS=agreed`, `VERDICT=AGREE` on 2026-07-04. This is
not a public benchmark, release, scientific, product, funding,
proof-correctness, broad theorem-proving, or general-reliability claim.

## Role Contract

Codex in the current conversation is supervisor and executor.

Claude Opus max effort is read-only reviewer only. Claude may review compact
bundles through `claude_review_gate.sh`; Claude must not edit files, run
experiments, launch response workers, collect responses, score as final
authority, approve boundary crossings, or authorize human, runtime,
model-file, funding, product, release, public-benchmark, or scientific-claim
boundaries.

Response collection, if later approved, must use the explicitly approved
non-Claude response-worker surface only.

## Human Approval Boundaries

This program is approved to:

- write plans, subplans, approval packets, scoring contracts, preflight
  reports, and stop handoffs;
- inspect local artifacts;
- run local JSON, hash, prompt-contract, pytest, and diff checks;
- run Claude read-only review gates on compact bundles.

This program must stop before response collection unless a human explicitly
approves all of:

- prompt manifest and prompt count;
- response-worker surface;
- retry policy;
- malformed-output policy;
- scoring contract;
- artifact paths for responses, response manifest, and scored responses.

This program must also stop before:

- using Claude as response worker;
- changing scoring criteria after seeing responses;
- changing default/release benchmark policy;
- installing packages, fetching network data, or changing credentials/model
  files;
- making release, public benchmark, scientific, product, funding, or general
  model-reliability claims.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Candidate Freeze | Freeze v2 candidate state, approval boundaries, role contract, and review-gate process before collection planning. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-subplan-2026-07-03.md` |
| 1 | Approval Packet And Scoring Contract | Write the collection approval packet and freeze the scoring contract before any response collection. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md` |
| 2 | Preflight And Collection Gate | Run final local preflight checks and stop or proceed only if explicit collection approval is complete. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-subplan-2026-07-03.md` |
| 3 | Response Collection | If explicitly approved, collect responses with no hidden retries and preserve malformed outputs. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-subplan-2026-07-03.md` |
| 4 | Hard-Veto-First Scoring | Score collected responses under the frozen contract and produce scored JSON/Markdown. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-subplan-2026-07-03.md` |
| 5 | Review And Decision | Run Claude review gate on scored results and write bounded decision/handoff. | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-subplan-2026-07-03.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Under a predeclared local collection/scoring contract, do v2 C_human_framed prompts improve downstream-agent task performance over B_evidence_only prompts without hard-veto regressions? |
| Baseline/comparator | V2 A/B/C prompt fixtures under `.mathdevmcp/downstream_agent_usefulness_v2/`; repaired benchmark baseline remains historical comparator only unless explicitly referenced. |
| Primary criterion | If collection is approved and completed, hard-veto-first scored results determine whether C beats B under the frozen primary dimensions; otherwise the program stops with an approval-needed blocker. |
| Veto diagnostics | Missing collection approval; Claude as response worker; hidden retries; malformed outputs replaced; prompt mutation after approval; scoring criteria changed after responses; hard-veto regression; aggregate-only promotion; unsupported public/scientific/product/release/general-reliability claims. |
| Explanatory diagnostics | Prompt validation, baseline hash rechecks, response manifest, malformed-output counts, per-case score table, candidate-only stressors, Claude review status, limitations. |
| Not concluded | No public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped obligations, or general model reliability. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| 18 v2 prompts | V2 candidate manifest | Fixed candidate scope reviewed by Claude | Prompt scope drift | Phase 2 prompt count/hash check | Reviewed default |
| No Claude response worker | User instruction and runbook | Keeps Claude as reviewer only | Authority/worker role confusion | Approval packet and runbook checks | Constraint |
| One attempt per prompt default | Candidate runbook | Preserves no-hidden-retry discipline and comparability | High variance | Result limitations and optional replication approval | Baseline |
| Frozen repaired required dimensions as primary | Candidate scoring map | Avoids post-hoc scoring drift | May under-detect v2 stressors | Phase 1 scoring-contract decision | Baseline |
| Candidate-only stressors explanatory by default | Phase 2 v2 scoring map | Avoids silently changing primary criterion | C benefit may remain explanatory only | Phase 1 explicit freeze | Reviewed default |
| Claude review gate, not direct worker | Review-gate guide | Provides probe, timeout, verdict parsing, logs | Fallback mistaken for full review | Record REVIEW_STATUS and VERDICT | Reviewed default |

## Repair Loop

- Every phase begins with skeptical audit.
- Every phase has a dedicated subplan before execution.
- At phase close, run required checks, write result, draft/refresh next
  subplan, and review the next subplan for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.
- Material subplans/results use Claude read-only review gates with compact
  bundles. Do not send whole files to Claude beyond bounded review bundles.
- If Claude returns `VERDICT=REVISE`, patch visibly and rerun focused checks.
- Stop after five Claude review rounds for the same blocker.
- If Claude probe/transport fails, use the review-gate status, redesign the
  bundle if the probe responds but review fails, and stop if the material gate
  cannot converge.

## Stop Conditions

Stop if:

- collection approval is incomplete;
- response-worker surface is not named;
- Claude is proposed as response worker;
- scoring criteria would change after seeing responses;
- prompt validation fails and cannot be repaired;
- baseline/candidate hashes mismatch unexpectedly;
- response collection would require network/API/funding/model-file decisions
  not explicitly approved;
- any public/scientific/product/release/general-reliability claim would be
  required.
