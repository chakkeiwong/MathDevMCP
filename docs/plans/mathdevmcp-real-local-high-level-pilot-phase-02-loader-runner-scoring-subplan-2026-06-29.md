# Phase 02 Subplan: Loader, Runner, And Scoring

## Phase Objective

Implement local pilot loading, validation, executable probe dispatch, and
boundary-preserving scoring.

## Entry Conditions Inherited From Previous Phase

- Phase 01 manifest exists, parses, and records five cases.
- Expected probe outcomes were declared before any runner execution.
- Source paths are local and relative.

## Required Artifacts

- Implementation:
  `src/mathdevmcp/real_local_high_level_pilot.py`
- Tests:
  `tests/test_real_local_high_level_pilot.py`
- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-02-loader-runner-scoring-result-2026-06-29.md`
- Phase 03 subplan.

## Required Checks, Tests, And Reviews

- Local checks:
  - `python3 -m pytest tests/test_real_local_high_level_pilot.py`
  - Focused high-level workflow tests if runner dispatch touches workflow
    invocation.
  - Known-bad scorer fixtures must fail when forbidden claims are present,
    source/probe channels are blended, required non-claims are absent, or
    adapter-required gaps are hidden.
- Review:
  - Codex self-review required.
  - Claude read-only review required if scoring or pass criteria change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo load, validate, execute, and score the five local high-level pilot probes without overclaiming source-case proof? |
| Baseline/comparator | Existing high-level workflow result contracts and real-task structural scoring discipline. |
| Primary pass criterion | Loader validates manifest fields/path/snapshot policy; runner dispatches declared probes; scoring checks probe status/evidence class/non-claims separately from source-obligation and adapter-gap channels; known-bad scorer tests fail as intended. |
| Veto diagnostics | Runner mutates source files, ignores expected non-claims, treats candidate metadata as executable proof, changes expected statuses after seeing output, hides adapter-required cases, or emits a single blended accuracy score. |
| Explanatory diagnostics | Per-case result details, source/probe separation, validation findings. |
| Not concluded | Full semantic correctness of source derivations, release readiness, benchmark-gate evidence. |
| Artifacts | Implementation, tests, phase result, refreshed Phase 03 subplan. |

## Forbidden Claims And Actions

- Do not add pilot results to formal benchmark-gate totals.
- Do not score prose quality as proof quality.
- Do not let a status match pass if required boundary non-claims are absent.
- Do not merge source obligation status and executable probe status into one
  case status.
- Do not run commands outside the current repo except reading declared source
  paths.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 03 only if:

- focused tests pass;
- manifest validation rejects malformed/missing-path cases;
- scoring fails when a forbidden boundary is violated;
- scoring keeps source, probe, and adapter-gap ledgers separate;
- Phase 03 can run the actual pilot without changing expected outcomes.

## Stop Conditions

- Stop if current high-level workflow outputs cannot support any declared
  executable probe.
- Stop if scoring cannot distinguish source obligation from simplified probe.
- Stop if implementation would need package installation or external network.
- Stop if a known-bad scorer fixture passes.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 03 subplan.
4. Review the Phase 03 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
