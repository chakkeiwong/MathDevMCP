# Phase 04 Subplan: CLI, Docs, And Non-Gating Integration

## Phase Objective

Expose the pilot through a local/non-gating command or documented Python entry
point and update operator documentation/README boundaries as needed.

## Entry Conditions Inherited From Previous Phase

- Phase 03 pilot report exists and preserves non-claims.
- The pilot is explicitly non-gating and local.
- No source/publication decision is required for the local pilot tier.

## Required Artifacts

- CLI integration if implemented:
  `src/mathdevmcp/cli.py`
- Documentation updates if implemented:
  `benchmarks/real_tasks/holdout_local/README.md`
  and/or `benchmarks/README.md`
- Tests:
  `tests/test_real_local_high_level_pilot.py`
  and any focused CLI smoke test.
- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-04-cli-docs-integration-result-2026-06-29.md`
- Phase 05 subplan.

## Required Checks, Tests, And Reviews

- Local checks:
  - Focused tests for the pilot module and CLI behavior.
  - Run the pilot command if CLI is added.
  - Grep docs for forbidden promotion language.
- Review:
  - Codex self-review required.
  - Claude read-only review required if docs or CLI wording could affect
    operator interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can operators run or inspect the local pilot without mistaking it for release-gated/public benchmark evidence? |
| Baseline/comparator | Existing CLI/high-level quality commands and benchmark docs. |
| Primary pass criterion | Pilot is discoverable locally, tests pass, docs preserve local/non-gating boundaries, and no formal gate totals are changed. |
| Veto diagnostics | CLI command exits like a release gate, docs imply public benchmark validity, benchmark gate totals change unintentionally, or source material is exposed. |
| Explanatory diagnostics | CLI output, docs grep, focused tests. |
| Not concluded | Release readiness, external benchmark validity, public corpus promotion. |
| Artifacts | CLI/docs/tests, phase result, refreshed Phase 05 subplan. |

## Forbidden Claims And Actions

- Do not add the pilot to `benchmark-gate` pass/fail totals.
- Do not document the pilot as public or CI-safe.
- Do not expose private source excerpts.
- Do not change release policy.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 05 only if:

- CLI/docs integration is either complete or explicitly deferred with rationale;
- focused tests and docs grep pass;
- the pilot remains non-gating;
- Phase 05 has a concrete final regression list.

## Stop Conditions

- Stop if exposing the pilot would confuse local/holdout/public tier semantics.
- Stop if docs require a publication or privacy decision.
- Stop if CLI integration risks changing benchmark-gate behavior.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 05 subplan.
4. Review the Phase 05 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
