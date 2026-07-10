# Phase 08 Subplan: Parallel Search Discipline

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_07`

## Phase Objective

Add bounded parallel execution for independent branch/backend attempts while
preserving deterministic reports, exact budgets, and failure records.

## Entry Conditions Inherited From Previous Phase

- Serial agent-guided strict workflow is exposed through CLI/MCP.
- Backend attempts and blockers are already represented structurally.

## Required Artifacts

- Optional parallel executor for independent search branches.
- Deterministic ordering of output nodes.
- Timeout/error records as blockers.
- Serial/parallel agreement tests.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Serial/parallel equivalence tests.
- Timeout/error blocker tests.
- Existing derivation-tree and CLI tests.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review if concurrency touches backend execution boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can independent branches be tested faster without changing logical results or hiding failures? |
| Baseline/comparator | Serial strict workflow from Phase 07. |
| Primary criterion | Serial and parallel runs agree on logical statuses; timeouts/errors become exact blockers; output order remains deterministic. |
| Veto diagnostics | Nondeterministic report order; lost backend errors; timeout treated as refutation; parallel run changes closure status. |
| Explanatory diagnostics | Parallelism may be disabled by default for fragile backends. |
| Not concluded | No speedup guarantee or benchmark claim unless separately measured. |
| Artifact | Parallel executor code, tests, Phase 08 result. |

## Forbidden Claims Or Actions

- Do not make parallel mode the default without evidence.
- Do not launch detached/background supervisors.
- Do not share mutable backend state unsafely.

## Exact Next-Phase Handoff Conditions

Advance to Phase 09 only if real-document runs can use serial strict mode and
optionally parallel mode without semantic drift.

## Stop Conditions

Stop if concurrency makes results nondeterministic or unsafe for backend
adapters.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 08 result / close record.
3. Draft or refresh Phase 09 subplan.
4. Review Phase 09 for consistency and boundary safety.
