# Tool Improvement Visible Gated Execution Runbook

Date: 2026-07-02

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This runbook must not launch a detached or nested supervisor. Do not use
`codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`
supervisors, backgrounded phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/mathdevmcp-tool-improvement-master-program-2026-07-02.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-tool-improvement-claude-review-trail-2026-07-02.md`

Execution ledger:

- `docs/plans/mathdevmcp-tool-improvement-visible-execution-ledger-2026-07-02.md`

Stop handoff:

- `docs/plans/mathdevmcp-tool-improvement-visible-stop-handoff-2026-07-02.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance Baseline And Launch | `docs/plans/mathdevmcp-tool-improvement-phase-00-governance-baseline-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-00-governance-baseline-result-2026-07-02.md` |
| 1 | Workflow Evidence Ledger | `docs/plans/mathdevmcp-tool-improvement-phase-01-evidence-ledger-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-01-evidence-ledger-result-2026-07-02.md` |
| 2 | Assumption Route Taxonomy | `docs/plans/mathdevmcp-tool-improvement-phase-02-assumption-taxonomy-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-02-assumption-taxonomy-result-2026-07-02.md` |
| 3 | Proof And Counterexample Evidence | `docs/plans/mathdevmcp-tool-improvement-phase-03-proof-counterexample-evidence-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-03-proof-counterexample-evidence-result-2026-07-02.md` |
| 4 | Derive-From Route Plans | `docs/plans/mathdevmcp-tool-improvement-phase-04-derive-route-plans-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-04-derive-route-plans-result-2026-07-02.md` |
| 5 | Math-To-Code Trace Artifacts | `docs/plans/mathdevmcp-tool-improvement-phase-05-math-code-trace-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-05-math-code-trace-result-2026-07-02.md` |
| 6 | Review Packet Compiler | `docs/plans/mathdevmcp-tool-improvement-phase-06-review-packet-compiler-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-06-review-packet-compiler-result-2026-07-02.md` |
| 7 | MCP And CLI Surface Alignment | `docs/plans/mathdevmcp-tool-improvement-phase-07-mcp-cli-alignment-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-07-mcp-cli-alignment-result-2026-07-02.md` |
| 8 | Benchmark-Guided Regression Closeout | `docs/plans/mathdevmcp-tool-improvement-phase-08-benchmark-regression-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-tool-improvement-phase-08-benchmark-regression-result-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP high-level tools be improved under visible gates using the repaired benchmark as diagnostic guidance? |
| Baseline/comparator | Current high-level workflow implementation plus repaired downstream-agent benchmark result. |
| Primary pass criterion | Every executed phase writes result evidence, passes focused checks, preserves non-claims, and hands off safely to the next phase. |
| Veto diagnostics | Hidden retries; Claude as executor; benchmark mutation; post-hoc criteria changes; unsupported proof/product/scientific/release claims; unrecorded local check failure. |
| Explanatory diagnostics | Unit tests, MCP/server checks, benchmark-case mapping, Claude review findings. |
| Not concluded | No release readiness, public benchmark validity, scientific validation, product capability, broad theorem proving, or general model reliability. |
| Artifacts | Master program, subplans, results, ledger, review trail, stop handoff, implementation diffs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible current-conversation execution | Template | Recoverable and auditable | User expected detached automation | Runbook states no detached supervisor | Reviewed default |
| Claude read-only review transport | User instruction | Material plan critique, with Opus/max preferred when available | Opus unavailable, fallback model mistaken for equivalent approval, or prompt blocked | Small probe, compact prompt redesign, and review trail recording model/effort/fallback status | Approved requested path with bounded availability fallback |
| Focused tests per phase | Repo policy | Limits blast radius | Missing cross-surface breakage | Phase 7/8 broader checks | Baseline |
| Preserve repaired benchmark artifacts | Benchmark result | Prevents measurement drift | Accidental mutation | Phase 0/8 git and prompt checks | Reviewed default |

## Skeptical Plan Audit

Before executing each phase, Codex records a skeptical audit in chat and the
ledger. The audit checks wrong baselines, proxy metrics, missing stop
conditions, unfair comparisons, hidden assumptions, stale context, environment
mismatch, and commands whose artifacts would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands/edits needed for the phase.
3. `ASSESS_GATE`: compare outputs against primary criterion and vetoes; write
   result artifact.
4. `PASS_REVIEW`: send material result or next subplan to Claude read-only
   reviewer; continue only after convergence or bounded unavailability.
5. `REPAIR_LOOP`: patch fixable blockers visibly, rerun focused checks, loop
   Claude review at high/max effort for material issues up to five rounds.
6. `ADVANCE_OR_STOP`: advance only after the phase gate passes; otherwise write
   stop handoff.

## Claude Read-Only Review Prompt Contract

Claude prompts must be compact and must not paste whole files. They must ask
Claude to read named local artifacts only as needed, perform read-only review,
and end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem actions, unrelated dirty-worktree
changes, product/release/scientific/public-validity claims, funding decisions,
or continuing after five failed review rounds for the same material blocker.

## Final Visible Handoff

On completion or stop, write final phase reached, final status, result
artifacts, Claude review trail, tests actually run, unresolved blockers,
non-claims, and safest next human decision.
