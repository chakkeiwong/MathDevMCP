# Phase 04 Subplan: Backend Formalization Targets

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_03`

## Phase Objective

Translate validated search paths into backend-native formalization targets, or
return exact non-encodability blockers.

## Entry Conditions Inherited From Previous Phase

- Recursive tree expansion exists.
- Candidate paths preserve assumptions, route, and expected backend.

## Required Artifacts

- `BackendFormalizationTarget` builder for SymPy, Sage, Lean, and diagnostic
  search aids.
- Explicit certification boundaries:
  direct Lean without `sorry`, scoped SymPy/Sage algebra, concrete
  counterexample, or diagnostic-only trace.
- Tests for certifying, diagnostic, unavailable, and invalid targets.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Backend adapter and derivation-tree tests.
- Lean/SymPy/Sage availability checks only where already supported.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of certification boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each candidate path become a runnable backend target or an exact formalization blocker? |
| Baseline/comparator | Current branch-level backend attempts and formalization stubs. |
| Primary criterion | Encodable algebra/Lean examples run through existing adapters; unsupported stochastic or macro constructs produce exact blockers. |
| Veto diagnostics | LeanDojo/Pantograph/retrieval treated as proof; Lean `sorry` certifies; backend unavailable treated as refutation; formalization target omits assumptions. |
| Explanatory diagnostics | Optional backend absence and environment mismatch. |
| Not concluded | No full-document proof or backend completeness claim. |
| Artifact | Formalization target code, tests, Phase 04 result. |

## Forbidden Claims Or Actions

- Do not install new backend packages.
- Do not mutate backend environments.
- Do not broaden certification beyond existing adapters.

## Exact Next-Phase Handoff Conditions

Advance to Phase 05 only if candidate paths can ask backends precise questions
or return exact non-encodability blockers.

## Stop Conditions

Stop if backend target generation cannot preserve assumptions and source
symbol maps.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 04 result / close record.
3. Draft or refresh Phase 05 subplan.
4. Review Phase 05 for consistency and boundary safety.
