# MathDevMCP Real-Local High-Level Pilot Master Program

Date: 2026-06-29

Status: `DRAFT_FOR_VISIBLE_GATED_EXECUTION`

## Program Objective

Turn the real-local high-level workflow inventory in
`docs/plans/mathdevmcp-real-local-high-level-workflow-pilot-cases-2026-06-29.md`
into a small, governed, executable pilot benchmark pack.

The pilot must use real source provenance from neighboring repositories under
`/home/chakwong/python`, but it must not treat local notes, structural matches,
or simplified executable probes as scientific validation. The intended outcome
is a five-case local pilot that can exercise current high-level workflow
behavior, identify adapter gaps, and preserve forbidden-claim boundaries.

## Selected Pilot Cases

The first pilot formalizes the five recommended cases from the inventory:

1. IFT gradient-bias sign consistency.
2. Kalman prediction-error log-likelihood.
3. Joseph covariance update equivalence.
4. Affine pricing master recursion.
5. Kalman score same-scalar derivative contract.

Each case may contain two layers:

- source-backed case metadata: the real user question, provenance, evidence
  contract, forbidden claims, and expected adjudication boundary;
- current executable probe: a bounded simplification that the current
  high-level workflow layer can honestly run today.

The manifest must keep these layers in separate channels. A case-level source
obligation status and a probe execution status must not be collapsed into a
single accuracy score.

If the current workflow layer cannot execute the real mathematical obligation,
the case must be marked as requiring an adapter rather than failed or passed.

## Core Invariants

- Codex is supervisor and executor.
- Claude is a read-only reviewer only.
- Claude cannot authorize human, runtime, model-file, funding, product,
  release, benchmark-promotion, or scientific-claim boundary crossings.
- Local sibling-repo provenance is allowed for this local pilot; public/CI
  promotion requires a later reviewed sanitization decision.
- Current executable probes are not substitutes for full LaTeX/domain
  derivation checking.
- A pass on this pilot is not release readiness, external benchmark validity,
  broad theorem proving, or scientific correctness.

## Phase Index

| Phase | Name | Primary Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Source Boundary | Confirm baseline, source scope, stop conditions, and skeptical audit | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-00-governance-source-boundary-subplan-2026-06-29.md` |
| 1 | Manifest And Case Contract | Define local pilot manifest schema and five source-backed case records | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-subplan-2026-06-29.md` |
| 2 | Loader, Runner, And Scoring | Implement manifest validation, executable probes, and boundary scoring | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-02-loader-runner-scoring-subplan-2026-06-29.md` |
| 3 | Pilot Calibration And Reports | Run the five-case pilot and classify executable vs adapter-required gaps | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-03-calibration-report-subplan-2026-06-29.md` |
| 4 | CLI, Docs, And Non-Gating Integration | Expose the pilot as local/non-gating tooling and document boundaries | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-04-cli-docs-integration-subplan-2026-06-29.md` |
| 5 | Final Regression And Handoff | Run final checks and write final result/handoff | `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-subplan-2026-06-29.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP construct and execute a five-case local pilot benchmark from real repo materials for high-level derivation/proof/assumption/debug workflows while preserving evidence boundaries? |
| Baseline/comparator | Existing seeded high-level workflow benchmark, current high-level workflow functions, and the real-local pilot inventory. |
| Primary pass criterion | The five selected cases have source-backed manifest records, the current executable probes run deterministically, scoring catches boundary violations, and reports clearly separate pilot evidence from benchmark-gate or scientific claims. |
| Veto diagnostics | Absolute/private source material promoted to public fixture; executable probe treated as full derivation proof; adapter-required case treated as passed/failed; Claude treated as execution authority; pilot pass claimed as release readiness or broad theorem proving. |
| Explanatory diagnostics | Manifest validation, focused unit tests, pilot run report, seeded high-level quality report, benchmark gate, docs grep, Claude read-only review. |
| Not concluded | External benchmark validity, release readiness, public redistributability, scientific validity of source documents, full LaTeX derivation competence, or general theorem proving. |
| Artifacts | Master program, subplans, visible runbook, review trail, ledger, pilot manifest, loader/runner/scorer, tests, reports, phase results, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Five-case first pilot | Prior inventory recommendation | Broad enough for derivation, proof, assumptions, and gradient boundary behavior | Too small to measure generality | Mark as pilot only and keep non-claims | Reviewed baseline |
| Sibling repo source paths | User explicitly pointed to `~/python` repos | Keeps real provenance without copying large/private docs | CI/public portability confusion | Path tier marked local; no benchmark-gate promotion | Reviewed default |
| Executable probes may be simplified | Current high-level workflows are bounded symbolic/structural tools | Allows honest execution without hallucinating full LaTeX proof ability | Probe pass misread as case proof | Case metadata separates source obligation from probe | Reviewed default |
| Non-gating local pilot report | Existing benchmark gate is strict seeded local evidence | Prevents unstable real-local pilot from changing release gates prematurely | Pilot never becomes actionable | Phase 5 recommends adapter/formalization next steps | Reviewed baseline |
| Claude read-only reviewer | User instruction and cross-agent policy | Independent plan critique without delegating execution | Prompt blocks or reviewer overclaims | Bounded prompt, probe if silent, max 5 review rounds | Reviewed default |
| Frozen source snapshot metadata | Claude review R1 and reproducibility discipline | Sibling repos can move independently of this checkout | Later report cannot reproduce source context | Record repo, relative path, line anchors, and git commit/status when available | Reviewed default |
| Known-bad scorer fixtures | Claude review R1 and benchmark-boundary policy | Happy-path scoring can miss false-confidence promotions | Boundary violations pass silently | Must-fail scorer tests for forbidden claims, blended statuses, and missing non-claims | Reviewed default |

## Promotion And Non-Promotion Rules

This program may produce a local pilot report if all gates pass.

It may not:

- add real-local pilot results to formal benchmark-gate pass/fail totals;
- claim public redistributability of sibling repo material;
- claim that a simplified probe proves the full source derivation;
- report a single aggregate "pilot accuracy" that merges source obligations and
  executable probe outcomes;
- claim release readiness, external benchmark validity, or broad theorem
  proving capability;
- change default workflow or release policy.

Future promotion to a formal benchmark requires a separate reviewed program
covering sanitization, oracle adjudication, adapter maturity, and stability
thresholds.

## Execution Rules

- Before each phase, perform and record a skeptical plan audit.
- At phase end: run required local checks, write the phase result, draft or
  refresh the next subplan, and review the next subplan for consistency,
  correctness, feasibility, artifact coverage, and boundary safety.
- Use Claude Opus max effort as read-only reviewer for material plans/results
  with compact prompts only.
- If Claude returns `VERDICT: REVISE`, patch visibly, rerun focused checks, and
  retry up to five rounds for the same blocker.
- If Claude does not respond, run a tiny probe. If the probe responds, redesign
  the prompt and retry smaller. Claude silence is never approval.
- Stop after five failed review/repair rounds for the same blocker.

## Human-Required Boundaries

Stop and ask the user before:

- copying substantial unpublished/private source text into committed fixtures;
- sending whole source documents or whole plans to Claude;
- making the pilot gating for release or CI;
- retaining a case that cannot be paraphrased without forbidden copying, cannot
  run deterministically, or cannot cleanly separate source obligation from
  executable probe;
- package installation, network fetches, credentials, or environment setup;
- destructive git/filesystem actions;
- changing scientific claims in neighboring repositories.
