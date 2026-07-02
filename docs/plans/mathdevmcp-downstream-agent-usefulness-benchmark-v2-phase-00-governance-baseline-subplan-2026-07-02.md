# Phase 0 Subplan: Governance And Baseline Freeze

Date: 2026-07-02

Status: `READY_FOR_PHASE_0_EXECUTION`

## Phase Objective

Freeze the repaired benchmark baseline, v2 artifact root, approval boundaries,
and local execution state before creating any v2 candidate cases or prompts.

## Entry Conditions Inherited From Previous Phase

- The 2026-07-02 benchmark-maintenance handoff is loaded.
- The repaired benchmark remains the current baseline.
- No v2 candidate cases, prompts, or response artifacts have been created.
- Claude reviewer availability has been probed and recorded as unavailable for
  the initial tiny prompt.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-00-governance-baseline-result-2026-07-02.md`.
- Baseline hash manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/baseline_hash_manifest.json`.
- V2 artifact-root README or metadata file:
  `.mathdevmcp/downstream_agent_usefulness_v2/README.md`.
- Draft Phase 1 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-subplan-2026-07-02.md`.
- Updated execution ledger and review trail if review is attempted.

## Required Checks, Tests, Reviews

- Confirm `.mathdevmcp/downstream_agent_usefulness/` exists and is not edited
  by Phase 0.
- Confirm v2 root is separate:
  `.mathdevmcp/downstream_agent_usefulness_v2/`.
- Compute hashes for repaired baseline primary artifacts.
- JSON parse primary repaired baseline JSON files and the new hash manifest.
- Run `git diff --check` on created v2 plans/artifacts.
- Local skeptical audit for wrong baseline, proxy metrics, missing stop
  conditions, hidden approval crossings, and artifact mismatch.
- Attempt compact Claude read-only review for the Phase 1 subplan only if
  Claude becomes responsive; otherwise record current reviewer unavailability.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the repaired benchmark baseline frozen and is the v2 maintenance lane safely separated before candidate design begins? |
| Baseline/comparator | Repaired benchmark artifacts under `.mathdevmcp/downstream_agent_usefulness/` and the new v2 root under `.mathdevmcp/downstream_agent_usefulness_v2/`. |
| Primary criterion | Phase 0 passes if baseline hashes are recorded, v2 root metadata exists, no repaired baseline files are modified, local JSON/diff checks pass, and Phase 1 has a reviewed or locally audited subplan. |
| Veto diagnostics | Edited repaired baseline file; response collection; Claude as response worker; missing v2 root separation; hash manifest missing primary repaired artifacts; unsupported benchmark-validity or C-over-B claim. |
| Explanatory diagnostics | Hash count, baseline artifact list, git status, JSON parse results, diff check, review availability. |
| Not concluded | No v2 case quality, no prompt validity, no downstream-agent usefulness, no C-over-B superiority, no public/scientific/product/release/general-reliability claim. |

## Forbidden Claims Or Actions

- Do not edit files under `.mathdevmcp/downstream_agent_usefulness/`.
- Do not collect responses.
- Do not create prompt fixtures before Phase 2 case manifest candidate exists.
- Do not treat hash preservation as benchmark validity.
- Do not use Claude as a response worker or authority.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- baseline hash manifest exists and parses as JSON;
- v2 root metadata exists;
- Phase 0 result records no repaired-baseline mutation;
- Phase 1 subplan exists and includes objective, entry conditions, artifacts,
  checks, evidence contract, forbidden claims/actions, handoff conditions, and
  stop conditions;
- the execution ledger records Phase 0 close.

## Stop Conditions

Stop if:

- repaired baseline artifacts appear to need mutation;
- v2 root cannot be created separately;
- baseline JSON or primary artifacts are missing in a way that prevents a
  frozen baseline statement;
- continuing would require response collection, external data, package
  installation, private-source decisions, or a policy/release/scientific claim.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 0 result/close record;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. attempt compact Claude read-only review if available, or record current
   reviewer unavailability.
