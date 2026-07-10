# Math Document Rigor Audit Visible Gated Execution Runbook

Date: 2026-07-07

## Status

`EXECUTED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook follows the visible template. It does not launch detached or
nested supervisors. Do not use `codex exec`, `overnight_gated_launch.sh`,
`setsid`, `nohup`, detached `tmux` supervisors, backgrounded phase runners, or
copied-workspace execution.

## Quiet Visible Execution Pattern

For commands that may produce large output, predeclare a log path, redirect
full output to the log, then summarize only exit status and bounded failure
tails in chat. Preserve logs and structured artifacts.

## Program

Master program:

- `docs/plans/mathdevmcp-document-rigor-audit-master-program-2026-07-07.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-document-rigor-audit-claude-review-trail-2026-07-07.md`

Execution ledger:

- `docs/plans/mathdevmcp-document-rigor-audit-visible-execution-ledger-2026-07-07.md`

Stop handoff:

- `docs/plans/mathdevmcp-document-rigor-audit-visible-stop-handoff-2026-07-07.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, Plan Review, And Launch | `docs/plans/mathdevmcp-document-rigor-audit-phase-00-governance-review-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-00-governance-review-result-2026-07-07.md` |
| 1 | Core Python Workflow MVP | `docs/plans/mathdevmcp-document-rigor-audit-phase-01-core-workflow-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-01-core-workflow-result-2026-07-07.md` |
| 2 | CLI And MCP Exposure | `docs/plans/mathdevmcp-document-rigor-audit-phase-02-cli-mcp-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-02-cli-mcp-result-2026-07-07.md` |
| 3 | Apply To Credit-Card NPV Document | `docs/plans/mathdevmcp-document-rigor-audit-phase-03-credit-card-application-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-03-credit-card-application-result-2026-07-07.md` |
| 4 | Regression, Review, And Handoff | `docs/plans/mathdevmcp-document-rigor-audit-phase-04-regression-closeout-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-04-regression-closeout-result-2026-07-07.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP build and apply a reusable Python workflow for mathematical document rigor gap/proposal reports? |
| Baseline/comparator | Current manual workflow plus existing lower-level MathDevMCP tools. |
| Primary pass criterion | Executed phases write results, pass focused checks, preserve backend/certification boundaries, and generate the target report artifacts. |
| Veto diagnostics | Hidden environment mismatch; yes/no-only output; target source edit; LeanDojo as certificate; unsupported full-proof/product/scientific/release claims; unrecorded failed check. |
| Explanatory diagnostics | Unit tests, CLI/MCP smokes, backend doctor/readiness, generated report excerpts, Claude review findings. |
| Not concluded | Full-document proof, scientific validation, product capability, release readiness, public benchmark validity, or general theorem-prover capability. |
| Artifacts | Master program, subplans, phase results, ledger, review trail, generated reports, logs, implementation diffs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Current-conversation visible execution | Template and user request | Keeps execution inspectable and recoverable | User expected detached automation | Runbook forbids detached supervisor explicitly | Reviewed default |
| Claude review gate | User request and guide | Provides bounded read-only critique | Prompt block or timeout mistaken for approval | Probe/gate status recorded; fallback weaker than full review | Reviewed default |
| Focused first application | Target document size | Prevents noisy report and accidental full-coverage claim | Coverage mistaken as complete | Report coverage status must be partial | Reviewed default |
| Existing tools before new logic | Repo pattern | Reduces hallucinated custom reasoning | Outputs too generic | Tests require location/problem/why/fix | Reviewed default |

## Skeptical Plan Audit

Before every phase, Codex records a skeptical audit in chat and, for material
phases, the ledger. The audit checks wrong baselines, proxy metrics, missing
stop conditions, unfair comparisons, hidden assumptions, stale context,
environment mismatch, and commands whose artifacts would not answer the phase
question.

## Visible State Machine

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands/edits needed for the phase.
3. `ASSESS_GATE`: compare outputs against primary criterion and vetoes; write
   result artifact.
4. `PASS_REVIEW`: use Claude read-only review for material artifacts.
5. `REPAIR_LOOP`: patch fixable blockers visibly, rerun focused checks, and
   stop after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after phase gate passes.

## Claude Review Gate Command

Use bounded review bundles under `docs/reviews/`. Preferred command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name <review-name> \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/<bundle>.md \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Run with trusted/escalated permissions. Record `REVIEW_STATUS`, `VERDICT`,
`RUN_DIR`, and `SUMMARY_JSON`.

## Human-Required Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
destructive git/filesystem action, unrelated dirty-worktree changes, changing
criteria after seeing results, source-document edits, or crossing scientific,
product, release, public-validity, runtime, or model-file boundaries.

## Final Visible Handoff

On completion or stop, write final phase reached, status, artifacts, review
trail, tests run, unresolved blockers, explicit non-claims, and next safest
human decision.
