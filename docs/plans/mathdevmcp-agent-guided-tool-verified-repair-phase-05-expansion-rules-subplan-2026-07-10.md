# Phase 05 Subplan: Expansion Rule Library

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_04`

## Phase Objective

Implement reusable deterministic expansion families for common mathematical
blockers so the agent/tree loop has useful generic paths.

## Entry Conditions Inherited From Previous Phase

- Recursive search exists.
- Backend formalization targets can run or block candidate paths.

## Required Artifacts

- Expansion rules for:
  conditional law, integrability, conditioning scope, macro translation,
  finite-horizon NPV/accounting identities, and differentiability/interchange.
- Tests using card-NPV and risky-debt snippets.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Focused expansion-rule tests.
- Document derivation-tree regression tests.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of mathematical assumptions and non-claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can common blockers generate concrete candidate paths rather than generic "collect more evidence" text? |
| Baseline/comparator | Current typed translation blockers and static sufficient assumption branches. |
| Primary criterion | Each supported blocker yields candidate assumptions, derivation route, backend target or exact blocker, and evidence refs. |
| Veto diagnostics | Generic handwavy expansion; assumptions not explicit; no backend route; no source-local symbols; claim of minimal assumptions. |
| Explanatory diagnostics | Multiple sufficient branches, unresolved notation, unsupported stochastic operator. |
| Not concluded | No claim that generated branches are necessary or globally minimal. |
| Artifact | Rule library code, tests, Phase 05 result. |

## Forbidden Claims Or Actions

- Do not hard-code card-NPV-only repairs.
- Do not hide unresolved stochastic assumptions.
- Do not skip backend target generation when a branch is encodable.

## Exact Next-Phase Handoff Conditions

Advance to Phase 06 only if expansion outputs can be consumed by the strict
proposal compiler and preserve exact blockers.

## Stop Conditions

Stop if the rule library drifts into document-specific edits instead of
generic blocker expansions.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 05 result / close record.
3. Draft or refresh Phase 06 subplan.
4. Review Phase 06 for consistency and boundary safety.
