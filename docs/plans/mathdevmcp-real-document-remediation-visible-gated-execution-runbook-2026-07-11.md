# MathDevMCP Real-Document Remediation Visible Gated Execution Runbook

Prospective execution note (2026-07-13): the automatic phase loop in
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md` supersedes the
legacy requirement below for independent agreement before every routine phase.
The historical P00-P03 review/receipt rules remain evidence, not live launch
authority. Local skeptical review launches a ready Tier 1/Tier 2 phase
automatically; substantive independent review remains required at the claim,
publication, default, and release boundaries named by the reset.

Date: 2026-07-11

Superseded prospectively: 2026-07-13 by
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`.

This file is retained as execution history. Its receipt chains, one-shot local
actions, exact review grammars, review budgets, and recovery state machines are
no longer live authority. Scientific evidence, claim, publication, security,
and human-decision boundaries remain active under the reset.

## Status

`SUPERSEDED_HISTORICAL_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only. Claude may inspect bounded review bundles,
named local artifacts, and focused diffs. Claude must not edit files, run
experiments, launch agents, execute phases, or authorize boundary crossings.

This is visible execution in the current conversation. Do not use `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, copied-workspace execution, or any nested executor.

The user explicitly approved the bounded 93-line Phase 00 disclosure on
2026-07-11, but the managed security layer still prohibited transmission to the
external Claude service. No content was sent. The execution therefore uses a
fresh independent Codex sub-agent as the local read-only material reviewer. It
has the same non-execution boundary, bounded questions, verdict contract, and
five-round limit. Supervisor self-review, silence, or timeout cannot pass a gate.

## Authority

The user authorized preparation and execution of Phase 00 and conditional
advancement one phase at a time. Advancement requires a passing predecessor
decision, false predecessor vetoes, passing phase-local skeptical and
default/assumption audits, and no human-required boundary.

The authorization does not include:

- package installation, network fetches, credentials, or environment mutation;
- destructive filesystem or git operations, commits, or pushes;
- detached execution or transferring execution authority to Claude;
- real-document backend runs before their master-plan gate;
- changing repair-publication defaults, applying a proposed source edit, or
  making release or scientific claims beyond the master plan.

## Program

Master program:

- `docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Execution ledger:

- `docs/plans/mathdevmcp-real-document-remediation-visible-execution-ledger-2026-07-11.md`

Stop handoff:

- `docs/plans/mathdevmcp-real-document-remediation-visible-stop-handoff-2026-07-11.md`

Runtime evidence root:

- `.local/mathdevmcp/evidence/<run-id>/`

Claude runtime review root:

- `.claude_reviews/<review-name>/`

## Phase Index

Only the current phase has a detailed subplan. Later subplans are drafted just
in time after the predecessor decision is sealed, so later work does not inherit
stale implementation or environment assumptions.

| Phase | Name | Detailed subplan | Required result |
| --- | --- | --- | --- |
| 00 | Publication Quarantine And Adversarial Safety | `docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-subplan-2026-07-11.md` | `docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-result-2026-07-11.md` plus `P00-decision.json` |
| 01 | Content-Addressed Evidence And Exact Binding | Just in time after P00 pass | P01 result plus `P01-decision.json` |
| 02 | Label-Scoped Obligation Extraction | Just in time after P01 pass | P02 result plus `P02-decision.json` |
| 03 | Semantic Resolution And Corpus Context | Just in time after P02 pass | P03 result plus `P03-decision.json` |
| 04 | Branch-Specific Search State Machine | Just in time after P03 pass | P04 result plus `P04-decision.json` |
| 05 | Executable External-Tool Routes | Just in time after P04 pass | P05 result plus `P05-decision.json` |
| 06 | Failure Ledgers, Ranking, And Action Selection | Just in time after P05 pass | P06 result plus `P06-decision.json` |
| 07 | Compact Agent-Facing MCP/CLI Product | Just in time after P06 pass | P07 result plus `P07-decision.json` |
| 08 | Frozen Real-Document Validation | Just in time after P07 pass | P08 experiment result plus `P08-decision.json` |
| 09 | Final Red-Team And Release Decision | Just in time after P08 result | Final bounded decision plus `P09-decision.json` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the master remediation program be executed visibly, phase by phase, while restoring the exact repair-publication boundary before expanding capability? |
| Baseline/comparator | Commit `a85fbb676eb4d551a8d78a70a5043524f308b7b9`, the recorded dirty planning paths, master-plan SHA-256 `5166192908f2a370a88538c07fefe79df984999059d85671087ddcc06a5b4182`, and the current unsafe simple-algebra publication regression. |
| Primary pass criterion | Every entered phase satisfies its own primary criterion and vetoes, writes referenced result evidence, receives bounded read-only review for its material plan and result, and advances only through the predecessor decision contract. |
| Veto diagnostics | Unsafe repair publication; hidden unresolved assumptions; evidence reuse or collision; extraction contamination; engineering errors treated as mathematics; missing artifacts; post-hoc gate changes; compact-output veto omission; Claude acting as executor or authority. |
| Explanatory diagnostics | Test counts, review rounds, tool availability, branch counts, report sizes, and wall times. These do not promote a phase. |
| Not concluded | No whole-document proof, release readiness, public readiness, global search completeness, globally minimal assumptions, or default repair-publication change. |
| Artifacts | Phase subplans/results/decisions, this runbook, ledger, stop handoff, bounded review bundles/logs, focused test logs, and evidence bundles required by the master plan. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible current-conversation execution | User authorization and visible-runbook template | Keeps execution recoverable and observable. | Detached work diverges from the dirty source workspace or crosses a gate silently. | Runbook forbids all detached launch mechanisms. | Reviewed default |
| Just-in-time detailed subplans | User prompt plus master predecessor contract | Uses actual predecessor evidence and environment. | Drafting all phases now bakes in stale symbols, tests, and routes. | Only P00 has a detailed subplan at launch. | Reviewed default |
| External Claude through `claude_review_gate.sh`, otherwise fresh local Codex reviewer | Claude review-gate guide, user-approved disclosure, managed transport denial, and prompt fallback | Preserves an independent material review without transmitting workspace data against policy. | Reviewer substitution becomes self-review or lowers the gate. | Fresh sub-agent, read-only bounded prompt, exact verdict, local checks, and five-round limit. | Reviewed environment-forced route |
| Claude model `opus`, effort `max` | User request; wrapper supports explicit model/effort | Uses requested reviewer when available. | Model alias is unavailable or auth/config failure is misdiagnosed as a bad prompt. | Gate probe and structured status; redesign only after a successful probe plus material prompt failure. | Requested route, availability hypothesis |
| Focused tests before broader tests | Repository policy and master verification ladder | Finds local contract failures cheaply. | Narrow tests miss surface regressions. | Each subplan names adjacent checks and the phase that owns broader validation. | Reviewed default |
| Preserve all current dirty paths | Repository policy | Those edits predate execution and belong to the user/current planning state. | A broad rewrite or cleanup destroys unrelated work. | Record baseline paths and inspect touched-file diffs at each gate. | Reviewed default |

## Skeptical Program Audit

- Wrong baseline: the baseline is the unsafe source-to-compiler workflow, not
  the prior Phase 09 `COMPLETE` label or a passing test suite.
- Proxy metrics: Claude agreement, test count, shorter reports, and available
  backends cannot substitute for a phase criterion or override a veto.
- Stop conditions: fixable scoped failures enter the repair loop; authority,
  destructive action, post-hoc criteria, budget exhaustion, or five repeated
  non-convergent review rounds stop visibly.
- Fair comparison: Phase 00 performs no real-document or backend-capability
  comparison. Later backend comparisons must use the same exact obligation and
  assumptions.
- Hidden assumptions: installed tools are availability evidence only; old
  backend attempts remain unbound until Phase 01.
- Environment: active Python is 3.11.15 with SymPy 1.14.0. Optional tool
  absence is recorded and does not block Phase 00.
- Artifact fitness: every consequential command must produce a bounded log or
  result artifact that directly answers its phase question.

Audit decision: `PASS_FOR_PHASE_00_PREPARATION_AND_REVIEW_ONLY`.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - Verify predecessor decision, source/git/environment state, authority, and
     exact phase entry conditions.
   - Record the phase evidence contract, skeptical audit, default/assumption
     audit, and pre-mortem.
2. `PLAN_REVIEW`
   - Run local plan checks.
   - Submit a compact project-local bundle to the permitted independent
     read-only reviewer route.
   - Advance only on explicit reviewer agreement plus passing local checks.
3. `EXECUTE_MINIMAL`
   - Implement only the current master work packages.
   - Run the smallest diagnostic first and preserve unrelated dirty work.
4. `ASSESS_GATE`
   - Run focused and adjacent checks in the stated order.
   - Evaluate primary criterion and vetoes before interpreting test counts.
   - Write the human result and machine-readable decision.
5. `RESULT_REVIEW`
   - Submit bounded implementation diff, checks, evidence, and result.
   - The independent reviewer reviews but does not execute or authorize.
6. `REPAIR_LOOP`
   - Patch a fixable scoped finding visibly, rerun focused checks, refresh the
     result/bundle, and review again.
   - Stop after five review/repair rounds for the same blocker.
7. `SEAL_OR_STOP`
   - Seal routine engineering/scientific phases when local gates pass and
     vetoes are clear; require substantive independent review when the phase
     changes a claim boundary, important interpretation, default, publication,
     or release decision.
   - Write the close record, draft or refresh the next subplan, run its local
     skeptical readiness review, and launch it automatically when ready.
   - Ask for help only at a human-required stop condition or a genuinely
     unresolved material blocker. Reviewer silence is neither agreement nor a
     routine-phase blocker.

## Automatic Close-And-Launch Loop

At every phase boundary:

1. run the subplan's required local checks;
2. write the phase result/close record;
3. draft or refresh the next subplan from current code and evidence;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, assumptions, and boundary safety;
5. if ready, immediately launch the next phase in the same visible run;
6. if not ready, repair locally when possible and otherwise ask the user for
   the specific missing decision or authority.

This loop does not broaden execution authority. It never auto-enables
publication, changes defaults, releases, installs packages, transmits private
data, performs destructive actions, or runs an unapproved external/GPU/model
action. Those remain explicit human boundaries.

## Independent Review Protocol

Use a compact bundle under `docs/reviews`. When external transmission is
permitted, the preferred Claude material command is:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name <stable-review-name> \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/<bundle>.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --probe-timeout 90 \
  --timeout-seconds 300 \
  --max-retries 1
```

Interpretation:

- `agreed`: review gate passes only with passing local gates;
- `revise`: repair visibly and rerun;
- `bounded_fallback_agree`: weaker advisory evidence, not convergence;
- successful probe followed by timeout/no verdict: inspect logs, shrink or
  redesign the bounded bundle, then retry;
- probe timeout/transport down: one bounded retry with reviewed timeout;
- model/auth/config error: configuration evidence, not a bad mathematical plan.

If Claude remains unavailable, stop the Claude route and record it. A fresh
Codex read-only reviewer then applies the same bounded questions and exact
verdict locally. For the current run, managed policy denial after informed user
approval establishes that the Claude transport route is unavailable. The fresh
reviewer cannot waive local gates or authorize any boundary.

## Quiet Execution Contract

Predeclare log and structured-result paths for commands with material output.
Redirect full output to the log, retain it, and report only exit status, key
fields, artifact paths, and a bounded tail on failure. Do not use quiet logging
to hide failures.

## Human-Required Stop Conditions

Stop and write a blocker result if continuing requires:

- a project-direction, pass-criterion, default-policy, publication, release, or
  scientific-claim decision not already authorized;
- package installation, network fetch, credentials, or environment mutation;
- destructive git/filesystem action, commit, push, or modification of unrelated
  dirty work;
- a real backend/document run before its predecessor gates;
- a budget increase after seeing the result without a reviewed amendment;
- continuing after five non-convergent review/repair rounds for one blocker;
- accepting evidence that cannot reconstruct its claim safely.

Ordinary fixable implementation defects, test failures, and review findings are
not stop reasons; they enter the bounded repair loop.

## Final Visible Handoff

At completion or a valid stop, record the final phase reached, final status,
result and decision artifacts, Claude review trail, commands/tests actually
run, unresolved blockers, explicit non-claims, and safest next human decision.
