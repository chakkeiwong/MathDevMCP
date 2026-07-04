# MathDevMCP Real-Local Source Adapters Master Program

Date: 2026-06-29

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Program Objective

Close the known source/probe gap in the five-case real-local high-level pilot.
The previous pilot proved that MathDevMCP can run bounded probes while honestly
reporting that all five full source obligations remain `adapter_required`.
This program builds the smallest source-linked adapter layer needed to evaluate
those five obligations without promoting simplified probes into source proof.

The intended final state is:

- line-linked source packets for all five local cases;
- normalized obligation records with notation/domain assumptions;
- bounded domain adapters for the IFT sign, Kalman likelihood, Joseph
  covariance, affine recursion, and Kalman score obligations;
- source-obligation scoring that reports adapter evidence separately from
  executable-probe evidence;
- a non-gating local report where the five source obligations are no longer
  merely `adapter_required`.

## Baseline

Baseline artifact:
`docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-result-2026-06-29.md`.

Frozen local inputs:

- pilot manifest:
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`;
- selected case ids:
  `RLHL-01-ift-gradient-bias-sign`,
  `RLHL-04-kalman-prediction-error-loglik`,
  `RLHL-06-joseph-covariance-equivalence`,
  `RLHL-07-affine-pricing-master-recursion`,
  `RLHL-10-kalman-score-same-scalar-contract`;
- source manifests are local-only sibling paths already listed in the pilot
  manifest; Phase 00 must record current file existence, line anchors, and
  manifest content hash before adapter execution.

Baseline result:

- five source-backed local cases exist;
- five executable probes pass;
- five full source obligations remain `adapter_required`;
- no aggregate pilot accuracy is emitted.

The repo and sibling repos may be dirty. Dirty status is provenance context,
not a reason to reinterpret the baseline after execution starts.

## Scope

In scope:

- local files already referenced by
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`;
- source packet extraction using line ranges and short excerpts;
- bounded packets capped to the manifest line ranges plus at most two context
  lines when explicitly needed for a label/definition;
- deterministic symbolic/domain adapters for the five selected cases;
- focused unit tests and local CLI/report integration.

Out of scope:

- public redistribution or CI promotion of sibling-repo material;
- release-gate integration;
- claims about broad theorem proving or full LaTeX proof checking;
- modifying neighboring repositories;
- package installation, network fetches, credentials, or model-file changes.
- relying on model/API output to execute or certify mathematical adapter
  results.

## Phase Index

| Phase | Name | Primary Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Source Freeze | Confirm baseline, source paths, evidence boundaries, and skeptical audit | `docs/plans/mathdevmcp-real-local-source-adapters-phase-00-governance-source-freeze-subplan-2026-06-29.md` |
| 1 | Source Packet Extraction | Build line-linked source packet schema, loader, and validator | `docs/plans/mathdevmcp-real-local-source-adapters-phase-01-source-packet-extraction-subplan-2026-06-29.md` |
| 2 | Math IR And Notation Normalization | Convert packets into normalized obligation records and enforce source/probe/residual channel separation before adapters run | `docs/plans/mathdevmcp-real-local-source-adapters-phase-02-math-ir-notation-subplan-2026-06-29.md` |
| 3 | IFT Sign Adapter | Evaluate the IFT gradient-bias sign consistency obligation | `docs/plans/mathdevmcp-real-local-source-adapters-phase-03-ift-sign-adapter-subplan-2026-06-29.md` |
| 4 | Kalman Likelihood Adapter | Evaluate the prediction-error log-likelihood derivation obligation | `docs/plans/mathdevmcp-real-local-source-adapters-phase-04-kalman-likelihood-adapter-subplan-2026-06-29.md` |
| 5 | Joseph Equivalence Adapter | Evaluate exact-arithmetic Joseph/compact covariance equivalence | `docs/plans/mathdevmcp-real-local-source-adapters-phase-05-joseph-equivalence-adapter-subplan-2026-06-29.md` |
| 6 | Affine Recursion Adapter | Evaluate Gaussian-MGF affine coefficient recursion | `docs/plans/mathdevmcp-real-local-source-adapters-phase-06-affine-recursion-adapter-subplan-2026-06-29.md` |
| 7 | Kalman Score Adapter | Evaluate solve-form score and same-scalar assumption boundary | `docs/plans/mathdevmcp-real-local-source-adapters-phase-07-kalman-score-adapter-subplan-2026-06-29.md` |
| 8 | Source Obligation Scorer | Integrate adapter results into separate source/probe/adapter report ledgers | `docs/plans/mathdevmcp-real-local-source-adapters-phase-08-source-obligation-scorer-subplan-2026-06-29.md` |
| 9 | CLI Docs And Non-Gating Integration | Expose the source-adapter report locally and document boundaries | `docs/plans/mathdevmcp-real-local-source-adapters-phase-09-cli-docs-integration-subplan-2026-06-29.md` |
| 10 | Final Regression And Handoff | Run final checks, write report, and preserve non-claims | `docs/plans/mathdevmcp-real-local-source-adapters-phase-10-final-regression-handoff-subplan-2026-06-29.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP convert the five real-local high-level pilot source obligations from `adapter_required` to bounded source-linked adapter results while preserving evidence boundaries? |
| Baseline/comparator | Completed real-local high-level pilot: five probes pass, five full source obligations remain `adapter_required`. |
| Primary pass criterion | All five cases have validated source packets, normalized obligation records, adapter-specific evidence, and a source-obligation report whose residual `adapter_required` count is zero under this local source-obligation schema while probe and source ledgers remain separate. |
| Veto diagnostics | Source text copied beyond bounded excerpts; source packet treated as full proof; hard-coded conclusion without anchors and deterministic checks; probe result promoted to source-obligation evidence; local report added to benchmark-gate totals; public/release/scientific/broad-theorem claims. |
| Explanatory diagnostics | Packet validation, IR validation, per-adapter unit tests, source-obligation report, original pilot report, high-level workflow quality report, benchmark-gate observation, Claude read-only review. These are engineering/regression diagnostics only except where a phase explicitly states a bounded adapter criterion. |
| Not concluded | Public benchmark validity, release readiness, scientific validation of neighboring documents, full LaTeX proof checking, external reproducibility, broad theorem proving, or correctness of production implementations in sibling repos. |
| Artifacts | Master program, subplans/results, visible runbook, ledger, Claude review trail, source adapter module, tests, packet records with line spans and content hashes, IR schema/examples, per-case adapter evidence records, source/probe/residual report ledgers, CLI report, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Promotion Status |
| --- | --- | --- | --- | --- | --- |
| Five-case source adapter target | Prior pilot final handoff | Directly addresses the only unresolved pilot gap | Overgeneralizing from five examples | Non-claims and local-only scope | Reviewed baseline |
| Line-range source packets | Pilot manifest and user source inventory | Minimal provenance without copying whole docs | Moving sibling repos or stale anchors | Source-exists and line-range checks | Reviewed default |
| Deterministic rule adapters | Current codebase uses bounded symbolic/structural tools | Avoids hallucinated proof prose | Hard-coded fragile conclusions | Tests require source anchors, extracted terms, and checks | Hypothesis with diagnostics |
| SymPy-backed algebra where feasible | Existing MathDevMCP low-level route | Provides deterministic algebra checks | Matrix/probability assumptions exceed SymPy scope | Adapter-specific exact checks and caveats | Reviewed baseline |
| No single source accuracy metric | Pilot boundary policy | Prevents false precision and channel blending | Operators may ask for one score | Report separate ledgers and counts | Reviewed default |
| Existing benchmark gate as regression only | Prior pilot policy | Keeps local source pack out of release gates | Gate pass misread as adapter promotion | Result wording and docs grep | Reviewed default |
| Claude compact read-only review | User instruction and cross-agent policy | Independent critique without delegating execution | Prompt block, silence, or overclaim | Probe if silent; retry smaller; max 5 | Reviewed default |
| Bounded packet caps | Claude review R1 and source/privacy discipline | Prevents accidental whole-document capture | Missing context for an obligation | Stop/escalate if cap is insufficient | Reviewed default |

## Skeptical Plan Audit

The drift guard and adapter-clearance rule are not standalone substitutes for
the evidence contract. They are additional launch gates. Every phase must still
record the baseline/comparator, pass criterion, veto diagnostics, stop
conditions, artifact provenance, and non-claims before execution.

Potential issue: treating extraction or pattern recognition as proof.
Mitigation: packet extraction and IR phases cannot emit `supported` or
`inconsistent` source results; only domain adapters with deterministic checks
can do so.

Potential issue: adapter conclusions could be hard-coded to case IDs.
Mitigation: tests must mutate relevant extracted terms and verify the adapter
does not pass when the required source pattern is absent or inconsistent.

Potential issue: existing executable probes could be reused as source evidence.
Mitigation: Phase 02 must encode source-adapter, executable-probe, and
residual-gap channel separation in the IR before adapter phases start. Phase 08
must preserve those ledgers and must not emit aggregate accuracy.

Potential issue: not all five cases may be closable by bounded deterministic
adapters. Mitigation: any case requiring broader semantic judgment, missing
notation conventions, or source context beyond bounded packets must remain
`adapter_required` or `human_review_required`; the program must then write a
blocker/partial result instead of forcing residual `adapter_required = 0`.

Potential issue: local sibling repos are dirty and may move.
Mitigation: Phase 0 records current path/commit/dirty status and line anchors;
reports remain local/non-gating. If the manifest hash, selected case ids,
source line anchors, packet content hashes, or repo commit/dirty provenance
drift after Phase 00 capture and before final handoff, execution must stop and
write a blocked or partial result rather than mix worktree states.

Potential issue: the plan could silently expand into scientific validation.
Mitigation: every phase repeats forbidden claims/actions and final handoff
states non-claims.

Audit status: `PASSED_FOR_REVIEW`. The plan has explicit baselines, criteria,
veto diagnostics, stop conditions, and artifacts that answer the stated
source-adapter question.

## Promotion And Non-Promotion Rules

This program may report that a specific local source obligation has a bounded
adapter result when the adapter has line-linked source evidence and deterministic
checks.

If the final residual `adapter_required` count is zero, that means only that no
case remains adapter-required under this local source-obligation schema. It does
not mean mathematical correctness, source-document truth, scientific validity,
or public benchmark readiness.

An `adapter_required` status may be cleared only by a source-anchored
local-schema check over the bounded source packet that records source anchors,
required-term coverage, adapter route, deterministic check evidence, and
non-claims. It may never be cleared by executable-probe success, absence of
blockers, adapter confidence, `pytest`, high-level quality, or benchmark-gate
outcomes.

This program must not:

- add local source-adapter results to benchmark-gate totals;
- claim full proof of the surrounding paper, monograph, or implementation;
- copy whole source documents into fixtures;
- report a blended source/probe accuracy;
- claim public redistributability, release readiness, external benchmark
  validity, scientific validation, or broad theorem proving.

## Execution Rules

- Codex is supervisor and executor.
- Claude Opus max effort is a read-only reviewer only.
- Before each phase, record a skeptical audit in the ledger.
- Run all local checks against the frozen local-only corpus; do not use network
  or model/API access for adapter execution or certification.
- At phase end, run local checks, write the result, draft or refresh the next
  subplan, and review the next subplan for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.
- For material review gates, send Claude compact briefs only.
- If Claude returns `VERDICT: REVISE`, patch visibly, rerun focused checks, and
  retry up to five times for the same blocker.
- If Claude is silent, run a tiny probe. If the probe works, redesign the prompt
  smaller. Silence is not approval.

## Human-Required Stop Conditions

Stop and ask the user before:

- copying substantial unpublished/private source text into repo fixtures;
- sending whole source files or whole plans to Claude;
- using network/package installation/credentials/model-file changes;
- changing release gates, public benchmark policy, or scientific claims;
- editing neighboring repositories;
- using destructive git/filesystem commands;
- continuing after five failed Claude review/repair rounds for the same
  blocker.

Stop without asking first, and write a blocked/partial result, if frozen
manifest/case/source/packet provenance drifts during execution.
