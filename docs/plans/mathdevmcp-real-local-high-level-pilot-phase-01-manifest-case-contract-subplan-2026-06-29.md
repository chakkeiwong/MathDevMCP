# Phase 01 Subplan: Manifest And Case Contract

## Phase Objective

Define a local pilot manifest contract and add five source-backed case records
with current executable probes and explicit forbidden-claim boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 00 source/privacy governance has passed.
- The selected five cases are accepted as local pilot candidates only.
- Current high-level workflow baseline tests are passing.

## Required Artifacts

- Pilot manifest:
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`
- Optional README update if needed:
  `benchmarks/real_tasks/holdout_local/README.md`
- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-result-2026-06-29.md`
- Phase 02 subplan.

## Required Checks, Tests, And Reviews

- Local checks:
  - JSON parse check for the manifest.
  - Path existence check for every referenced local source path.
  - Source snapshot check that records sibling repo, relative path, line
    anchors, and git commit/status when available.
  - `rg -n "release readiness|broad theorem|benchmark-gate evidence|scientific validity" benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-subplan-2026-06-29.md`
- Review:
  - Codex self-review required.
  - Claude read-only review required if schema fields or source tier semantics
    change materially from the master program.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the five local pilot cases represented with enough provenance, executable-probe metadata, and forbidden-claim boundaries to support a runner? |
| Baseline/comparator | Pilot inventory and existing real-task manifest style. |
| Primary pass criterion | Manifest parses, references existing relative local source paths, includes five selected cases, records frozen source snapshot metadata, and keeps source obligation, executable probe, adapter gap, and non-claim channels distinct. |
| Veto diagnostics | Absolute paths, missing source paths, missing snapshot metadata, missing forbidden claims, probe expected status unsupported by current workflows, source obligation conflated with executable probe. |
| Explanatory diagnostics | Number of cases, workflow coverage, source paths, executable probe kinds. |
| Not concluded | Runner correctness, benchmark quality, public redistributability, full derivation validity. |
| Artifacts | Manifest, optional README note, phase result, refreshed Phase 02 subplan. |

## Forbidden Claims And Actions

- Do not include large raw source excerpts.
- Do not mark the local pilot manifest as public or CI-safe.
- Do not make manifest validation equivalent to benchmark pass.
- Do not change existing public real-task manifest semantics.
- Do not report a single blended case status that merges source obligation
  support and executable probe outcome.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 02 only if:

- the manifest has exactly five selected cases;
- source paths are relative and exist locally;
- every case has a source obligation and a separate executable probe;
- every case records why the executable probe is a faithful bounded diagnostic
  for the source obligation and what it does not prove;
- every case lists forbidden claims/non-claims;
- Phase 02 can implement validation and scoring without changing the case
  contract after seeing results.

## Stop Conditions

- Stop if any selected source path is unavailable.
- Stop if a case requires substantial source copying to be adjudicable.
- Stop if expected probe behavior cannot be stated before execution.
- Stop if local vs public tier semantics are ambiguous.
- Stop if a selected case cannot be paraphrased without forbidden copying,
  cannot be deterministic locally, or cannot cleanly separate source obligation
  from executable probe.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 02 subplan.
4. Review the Phase 02 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
