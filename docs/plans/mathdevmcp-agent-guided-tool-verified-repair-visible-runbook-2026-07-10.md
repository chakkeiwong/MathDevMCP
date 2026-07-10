# MathDevMCP Agent-Guided Tool-Verified Repair Visible Runbook

Date: 2026-07-10

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook is for visible, recoverable, overnight-scale execution in the
current conversation.  It must not launch detached or nested agents.  Do not
use `codex exec`, `overnight_gated_launch.sh`, detached `tmux`, `nohup`,
`setsid`, backgrounded phase runners, or copied-workspace execution.  If the
user wants detached execution, stop and write a separate detached-supervisor
plan.

## Program

Master program:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-master-program-2026-07-10.md`

Review bundle:

- `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-plan-review-bundle-2026-07-10.md`

Execution ledger:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-ledger-2026-07-10.md`

Stop handoff:

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-stop-handoff-2026-07-10.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 00 | Governance, Baseline, And Review Gate | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-governance-baseline-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-result-2026-07-10.md` |
| 01 | Strict Contracts And Regression Gates | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-contracts-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-result-2026-07-10.md` |
| 02 | Agent Hypothesis Expansion Interface | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-agent-hypotheses-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-result-2026-07-10.md` |
| 03 | Recursive Derivation Tree Search | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-recursive-tree-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-result-2026-07-10.md` |
| 04 | Backend Formalization Targets | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-backend-formalization-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-result-2026-07-10.md` |
| 05 | Expansion Rule Library | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-expansion-rules-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-result-2026-07-10.md` |
| 06 | Tool-Grounded Proposal Compiler | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-proposal-compiler-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-result-2026-07-10.md` |
| 07 | CLI And MCP Integration | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-cli-mcp-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-result-2026-07-10.md` |
| 08 | Parallel Search Discipline | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-parallel-search-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-result-2026-07-10.md` |
| 09 | Real-Document Regression And Mission Control | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-real-doc-mission-control-subplan-2026-07-10.md` | `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP implement agent-guided, tree/tool-verified derivation repair without hallucinated proposal text? |
| Baseline/comparator | Phase 06 context-aware executable repair reports and tests. |
| Primary pass criterion | The completed lane exposes a strict workflow where agent hypotheses are candidate branches, derivation-tree search verifies/refutes/blocks them, and reports publish only evidence-grounded repairs or exact gap reports. |
| Veto diagnostics | Raw agent text published as fix; diagnostic evidence promoted to proof; blocked branches rendered as repairs; missing exact blockers; hidden budget exhaustion; no review/result artifact. |
| Explanatory diagnostics | Optional backend unavailable, all branches blocked, parallelism disabled, Claude unavailable. |
| Not concluded | Whole-document proof, publication readiness, release readiness, global completeness, or minimal assumptions. |
| Artifacts | Phase plans/results, review bundle/trail, tests, generated reports, ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible runbook | `visible-gated-execution-runbook-template.md` | Keeps execution recoverable in this conversation. | User expected detached overnight run. | Runbook forbids detached launch and records approval boundary. | Reviewed default |
| Agent hypotheses as schema records | User direction and current weakness | Uses agent creativity while preserving evidence discipline. | Vague route passes into reports. | Phase 02 validation rejects vague hypotheses. | Reviewed default |
| Tool-grounded reports | Repo policy and user feedback | Prevents hallucinated repairs. | Reports become too terse or still vague. | Phase 06 report tests require exact why/fix/evidence/blockers. | Reviewed default |
| Serial before parallel | Scientific workflow policy | Establishes correctness before speed. | Slow real-document runs. | Phase 08 adds parallelism only after serial tests. | Reviewed default |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Quiet Visible Execution Pattern

Full stdout/stderr from long checks and Claude review gates must be redirected
to log artifacts when practical.  The chat should receive bounded summaries:
exit status, artifact paths, pass/fail fields, and at most the last 20-40 lines
on failure.

## Anticipated Approval Needs

- Claude read-only review gate may require trusted execution:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh ...`.
- Existing approved test prefix `python3 -m` should cover local pytest and
  compile checks.
- No package installation, network fetch, destructive filesystem action, or
  detached execution is anticipated for Phase 00.
- Later phases may request trusted Lean commands only if a direct Lean
  certification check is necessary and already scoped.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, restate evidence contract, append ledger entry.
2. `EXECUTE_MINIMAL`: implement or diagnose the smallest bounded slice.
3. `ASSESS_GATE`: compare outputs to pass/veto criteria and write result.
4. `PASS_REVIEW`: use Claude read-only review when available; otherwise record
   unavailability and perform fresh Codex fallback review.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, and stop
   after five review rounds for the same material blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes.

## Claude Read-Only Review Template

Claude prompts must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the bounded artifacts only.

Check wrong baseline, proxy metrics, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim, and
artifact mismatch.

End with exactly VERDICT: AGREE or VERDICT: REVISE.
```

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, credentials, or environment setup;
- detached execution or nested agent launch;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- modifying unrelated dirty user work;
- proof-boundary weakening;
- continuing after five nonconvergent review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude or fallback review trail;
- tests/checks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
