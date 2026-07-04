# MathDevMCP Mission Gap Closure Master Program

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_FINAL_READ_ONLY_REVIEW_AGREED`

Supervisor/executor: Codex

Reviewer: Claude read-only reviewer, advisory only

## Mission Objective

Close the current mission gaps for MathDevMCP as a conservative
agent-facing CLI/MCP math-development review tool.

This program is not a benchmark program. Benchmarks are allowed only as
regression guards or evidence instruments after product behavior is improved.

Canonical mission:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`

Immediate predecessor:

- `docs/plans/mathdevmcp-review-handoff-packet-product-improvement-result-2026-07-04.md`

## Product Gaps To Close

1. `agent_handoff` exists in packets but is still buried in raw JSON.
2. The product spine needs one representative end-to-end workflow report.
3. Realistic difficult cases need regression coverage.
4. The v2 downstream-agent usefulness diagnostic needs to become a guard, not
   the product goal.
5. Additive packet compatibility policy needs to be explicit.
6. Release/readiness claims need a conservative evidence ledger and blocker
   list.

## Phase Index

| Phase | Name | Objective | Subplan | Required result |
| --- | --- | --- | --- | --- |
| 0 | Governed Launch | Freeze reviewed program/runbook/subplans and launch visible execution. | `docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-result-2026-07-04.md` |
| 1 | CLI/MCP Handoff Presentation | Make `agent_handoff` easy for agents to consume through CLI/MCP. | `docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-result-2026-07-04.md` |
| 2 | End-To-End Workflow | Produce one representative source/code-to-report workflow. | `docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-result-2026-07-04.md` |
| 3 | Realistic Case Coverage | Cover difficult review cases with tests and handoff expectations. | `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-result-2026-07-04.md` |
| 4 | V2 Regression Guard | Use v2 only as a bounded regression/evaluation guard after product work. | `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-result-2026-07-04.md` |
| 5 | Compatibility Policy | Define additive packet compatibility and stable consumer contract. | `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-result-2026-07-04.md` |
| 6 | Release Readiness Boundary | Build conservative readiness/blocker evidence without overclaiming. | `docs/plans/mathdevmcp-mission-gap-closure-phase-06-release-readiness-boundary-subplan-2026-07-04.md` | `docs/plans/mathdevmcp-mission-gap-closure-phase-06-release-readiness-boundary-result-2026-07-04.md` |

## Runbook And Ledgers

- Runbook: `docs/plans/mathdevmcp-mission-gap-closure-visible-gated-execution-plan-2026-07-04.md`
- Execution ledger: `docs/plans/mathdevmcp-mission-gap-closure-visible-execution-ledger-2026-07-04.md`
- Stop handoff: `docs/plans/mathdevmcp-mission-gap-closure-visible-stop-handoff-2026-07-04.md`
- Program review bundle: `docs/reviews/mathdevmcp-mission-gap-closure-program-review-bundle-2026-07-04.md`

## Master Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP close the known mission gaps by improving real CLI/MCP product surfaces while preserving conservative proof boundaries? |
| Baseline/comparator | Current post-`agent_handoff` state: packets contain derived handoff data, but presentation, end-to-end workflow, case coverage, regression guard, compatibility policy, and readiness boundaries remain incomplete. |
| Primary pass criterion | Each phase produces its required artifact, passes local checks, records non-claims, and hands off exact next-phase entry conditions. |
| Veto diagnostics | A phase treats benchmark score as mission success, weakens abstention/proof boundaries, changes pass/fail criteria after seeing results, crosses external model/runtime/funding/release/scientific boundaries without approval, or modifies unrelated dirty work. |
| Explanatory diagnostics | Test coverage, CLI/MCP output shape, review comments, benchmark replay diagnostics, compatibility notes, release blocker counts. |
| Not concluded | No mathematical proof, semantic code proof, product-wide readiness, public benchmark validity, scientific validation, funding readiness, release approval, or general model reliability. |
| Artifacts | Phase subplans/results, visible ledger, review bundles/logs, tests, bounded generated outputs. |

## Anti-Drift Gate

| Field | Answer |
| --- | --- |
| Mission link | Conservative agent-facing mathematical review through CLI/MCP. |
| User served | Coding agents, maintainers, colleagues, and release operators. |
| Product artifact | CLI/MCP handoff presentation, end-to-end report workflow, coverage tests, regression guard, compatibility policy, readiness blocker report. |
| Evidence instrument | Local tests, CLI/MCP smoke checks, read-only reviews, and bounded v2 regression diagnostics. |
| Evidence-to-implementation path | Each phase either changes product behavior, protects it with regression coverage, or records release/compatibility boundaries. |
| Non-goal | Do not optimize benchmark prompts, create process artifacts as an end in themselves, or claim readiness from local diagnostics. |
| Stop-for-drift condition | Stop if a phase is only "make benchmark/pass review/write docs" without a product workflow or boundary-protection role. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start with CLI/MCP presentation | Current result says `agent_handoff` exists but presentation gap remains. | It directly improves agent-facing product consumption. | Could become pretty formatting without preserving machine JSON. | CLI/MCP tests must preserve full JSON and compact handoff fields. | Reviewed default pending program review |
| Use v2 after product phases | Mission charter and evidence ledger. | Prevents benchmark-as-mission drift. | Waiting too long could miss regressions. | Phase 4 is explicit guard with no scoring changes after outputs. | Reviewed default pending program review |
| Claude as reviewer only | User approval and cross-agent policy. | Adds boundary review without transferring authority. | Claude could be treated as executor/approver. | Review bundles say read-only; results record advisory status. | Reviewed default pending program review |
| Visible execution, no detached agents | `visible-gated-execution-runbook-template.md`. | Keeps execution recoverable in current conversation. | Long commands may produce too much output. | Runbook requires quiet logs and bounded summaries. | Reviewed default pending program review |

## Skeptical Plan Audit

- Wrong baseline: the baseline is the current post-`agent_handoff` product
  state, not pre-v2 packet output.
- Proxy metric risk: field presence, benchmark score, or Claude agreement are
  not product readiness or proof.
- Missing stop conditions: each phase subplan includes explicit stop
  conditions and exact next-phase handoff conditions.
- Unfair comparison risk: Phase 4 forbids scoring changes after new outputs.
- Hidden assumptions: exact external schema compatibility is not assumed.
- Environment mismatch: phases start with local tests and no package installs.
- Artifact fit: each phase has a product, regression, compatibility, or
  boundary artifact tied to the mission.

Audit result: `PASS_READ_ONLY_REVIEW_AGREED`.

## Program Review And Launch Status

Opus/max review attempt:

- `REVIEW_STATUS=probe_timeout`
- `VERDICT=NONE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-040234-mathdevmcp-mission-gap-closure-program-r1`
- Interpretation: Opus/max was unavailable at the probe stage; this is not a
  plan agreement or a plan defect.

Sonnet/max substitute review:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-040454-mathdevmcp-mission-gap-closure-program-sonnet-r1`
- `SUMMARY_JSON=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-040454-mathdevmcp-mission-gap-closure-program-sonnet-r1/status.json`

Visible execution status:

- Phases 0-6 completed.
- Final Phase 6 boundary review agreed.
- The lane closed without declaring unconditional release approval.

## Repair Loop

For material review findings:

1. Patch the same subplan, runbook, or result visibly.
2. Rerun focused local checks.
3. Rerun Claude review only for material issues.
4. Stop after five review rounds for the same blocker.
5. If convergence fails, write a blocker result and stop for human direction.

Claude cannot authorize crossing human, runtime, model-file, funding, product
capability, release, public-benchmark, scientific-claim, or general-reliability
boundaries.
