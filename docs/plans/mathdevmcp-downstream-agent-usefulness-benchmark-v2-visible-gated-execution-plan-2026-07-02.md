# Downstream-Agent Usefulness Benchmark V2 Visible Gated Execution Plan

Date: 2026-07-02

## Status

`LAUNCHED_VISIBLE_GATED_EXECUTION_WITH_CLAUDE_PROBE_UNAVAILABLE`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook is based on
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
It is overnight-compatible in the sense that it is gated, ledgered, and
recoverable, but it must remain visible in the current conversation. It must
not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

## Program

Master program:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-master-program-2026-07-02.md`

Reviewed plan artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-claude-review-trail-2026-07-02.md`

Execution ledger:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-execution-ledger-2026-07-02.md`

Stop handoff:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-stop-handoff-2026-07-02.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-00-governance-baseline-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-00-governance-baseline-result-2026-07-02.md` |
| 1 | Ceiling-Effect And Difficulty Requirements | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-result-2026-07-02.md` |
| 2 | Case Manifest Candidate | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-result-2026-07-02.md` |
| 3 | Prompt Fixtures And Contract Validation | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-result-2026-07-02.md` |
| 4 | Adversarial Analysis And Collection Runbook | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-result-2026-07-02.md` |
| 5 | Candidate Close And Handoff | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-subplan-2026-07-02.md` | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-result-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a harder local benchmark candidate discriminate between compact machine-evidence prompts and richer human-framed handoff prompts without post-hoc scoring drift or answer leakage? |
| Baseline/comparator | Frozen repaired benchmark artifacts under `.mathdevmcp/downstream_agent_usefulness/` plus the proposed v2 candidate under `.mathdevmcp/downstream_agent_usefulness_v2/`. |
| Primary pass criterion | The visible execution produces locally validated v2 candidate artifacts, analysis, and runbook while stopping before response collection. |
| Veto diagnostics | Baseline mutation; response collection; Claude as response worker; hidden retries; prompt leakage; rubric drift; substantial private excerpts; unsupported C-over-B, release, public, scientific, product, or general-reliability claims. |
| Explanatory diagnostics | Hash manifest, ceiling-effect inventory, difficulty coverage, prompt-contract report, scoring applicability map, adversarial analysis, local checks, review trail. |
| Not concluded | Tool improvement, model reliability, release readiness, public benchmark validity, scientific validation, product capability, or C-over-B superiority. |
| Artifacts | Master program, subplans/results, ledger, review trail, v2 artifact root, runbook, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution | Template and current conversation | Keeps supervisor/executor accountable and recoverable | Detached state could hide failures | Ledger entry per phase | Required |
| Claude read-only reviewer | User request | Adds independent critique without authority transfer | Silent or broad prompts stall execution | Compact briefs and probe record | Constraint |
| V2 separate artifact root | Handoff | Avoids baseline overwrite | Mixed root invalidates baseline comparison | Phase 0 root check | Reviewed default |
| Stop before collection | Handoff | Prevents post-hoc tuning and cost/auth drift | Candidate treated as result evidence | Phase 4/5 approval boundary | Constraint |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

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

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase subplans, results, repairs, or final decisions to
     Claude as compact read-only briefs when Claude responds.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
   - If Claude remains unavailable after a compact review and tiny probe,
     record reviewer unavailability and use Codex-only skeptical review only
     for phases that do not cross human approval, response collection,
     scoring, implementation repair, runtime, model-file, funding, product, or
     scientific-claim boundaries.
5. `REPAIR_LOOP`
   - For fixable blockers, patch the active subplan or artifact visibly.
   - Get Claude review when material and available.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker or repair result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Ledger Entry Template

```markdown
### <timestamp> - Phase <N> - <STATE>

Evidence contract:

- Question:
- Baseline/comparator:
- Primary criterion:
- Veto diagnostics:
- Non-claims:

Actions:

- <commands/edits/reviews>

Artifacts:

- <paths>

Gate status:

- <PASSED/BLOCKED/FAILED/IN_PROGRESS>

Next action:

- <next visible step>
```

## Claude Read-Only Review Template

Use compact briefs rather than whole files.

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, collect responses, score
responses, or change state.

Review this compact brief:
- program/phase:
- objective:
- baseline:
- artifacts:
- checks:
- evidence contract:
- forbidden claims/actions:
- handoff:
- stop conditions:

Check wrong baseline, proxy metrics, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim,
artifact mismatch, and boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude does not respond, run or record a tiny probe. If the probe responds,
redesign the prompt smaller. Claude silence is never approval.

## Human-Required Stop Conditions

Stop if continuing would require:

- collecting new downstream-agent/model responses;
- using Claude as response worker;
- package installation, network fetch, credentials, or model-file changes;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing responses;
- changing release/default benchmark policy;
- modifying repaired baseline artifacts;
- copying substantial private or neighboring-repo content into prompts;
- making scientific, product, release, public benchmark, funding, or general
  model-reliability claims;
- continuing after Claude and Codex do not converge after five review rounds
  for the same blocker.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- checks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
