# Downstream-Agent Usefulness V2 Collection Visible Gated Execution Plan

Date: 2026-07-03

## Status

`COMPLETE_BOUNDED_LOCAL_DIAGNOSTIC_FINAL_REVIEW_AGREED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is the requested read-only reviewer. If Opus is
unavailable, a human may explicitly approve Sonnet max as a substitute
read-only reviewer for a bounded gate. Claude remains advisory only.

This runbook is based on
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
Execution is visible and recoverable inside the current conversation. It must
not launch detached supervisors, copied-workspace execution, or response
collection without explicit approval.

## Program

Master program:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-scoring-master-program-2026-07-03.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-claude-review-trail-2026-07-03.md`

Execution ledger:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-execution-ledger-2026-07-03.md`

Stop handoff:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-stop-handoff-2026-07-03.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Candidate Freeze | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-result-2026-07-03.md` |
| 1 | Approval Packet And Scoring Contract | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-result-2026-07-03.md` |
| 2 | Preflight And Collection Gate | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-result-2026-07-03.md` |
| 3 | Response Collection | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-result-2026-07-03.md` |
| 4 | Hard-Veto-First Scoring | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-result-2026-07-03.md` |
| 5 | Review And Decision | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-subplan-2026-07-03.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-result-2026-07-03.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Under a predeclared local collection/scoring contract, do v2 C_human_framed prompts improve downstream-agent task performance over B_evidence_only prompts without hard-veto regressions? |
| Baseline/comparator | V2 A/B/C prompts; repaired benchmark is a historical baseline only. |
| Primary pass criterion | Complete preflight and either stop for missing collection approval or, if explicitly approved, collect/score responses and produce a hard-veto-first bounded decision. |
| Veto diagnostics | Missing approval, Claude as response worker, hidden retries, replaced malformed outputs, scoring drift, prompt mutation after approval, aggregate-only promotion, unsupported claims. |
| Explanatory diagnostics | Validation reports, hashes, response manifest, score tables, candidate stressors, review statuses, limitations. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped obligations, general model reliability. |

## Quiet Visible Execution Pattern

Use the quiet pattern from the template for Claude review gates and any future
collection/scoring command with potentially large output. Full stdout/stderr
belongs in logs or generated artifacts; chat receives bounded summaries.

## Skeptical Plan Audit

Before executing any phase, Codex records a skeptical audit in chat and, for
material phases, in the execution ledger.

Check wrong baselines, proxy metrics, missing stop conditions, unfair
comparisons, hidden assumptions, stale context, environment mismatch, and
commands whose artifacts would not answer the phase question.

## Claude Review Gate Policy

For material reviews, use:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name <name> \
  --bundle <project-local-bundle> \
  --model opus \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Record `REVIEW_STATUS`, `VERDICT`, `RUN_DIR`, and `SUMMARY_JSON`. Treat
`bounded_fallback_agree` as weaker than full primary review. Claude cannot
authorize collection or claims.

If a reviewer-model substitution is approved, record the model and human
direction in the review trail and ledger. Pending reviewer-model direction is a
stop state, not a phase handoff condition.

## Human-Required Stop Conditions

Stop if continuing requires:

- response collection without explicit approval;
- a response-worker surface not already approved;
- package installation, network fetch, credentials, or model-file changes;
- destructive git/filesystem action;
- changing scoring criteria after seeing responses;
- changing release/default benchmark policy;
- Claude as response worker;
- unsupported scientific, product, release, public benchmark, funding, or
  general-reliability claims;
- continuing after five failed review/repair rounds for the same blocker.

## Final Visible Handoff

When execution completes or stops, write final phase reached, status,
artifacts, Claude review trail, checks run, unresolved blockers, non-claims,
and safest next human decision.

## 2026-07-04 Continuation Correction

The current workspace contains completed local Phase 3-5 artifacts, including
18 response artifacts and 18 scored rows. Older Phase 0/1/2 review bundles and
handoffs that describe a no-response pre-collection state are historical and
must not be reused as current-state review bundles.

Current continuation policy:

- do not collect additional responses;
- do not change the frozen scoring criteria;
- do not use Claude as response worker or scoring authority;
- validate the existing artifacts locally;
- patch stale handoff/status records visibly;
- final-state Sonnet max read-only review converged on 2026-07-04:
  `REVIEW_STATUS=agreed`, `VERDICT=AGREE`,
  `RUN_DIR=.claude_reviews/20260704-014647-mathdevmcp-v2-collection-final-state-sonnet-r1`;
- close the runbook only as a bounded local diagnostic with the non-claims
  preserved.
