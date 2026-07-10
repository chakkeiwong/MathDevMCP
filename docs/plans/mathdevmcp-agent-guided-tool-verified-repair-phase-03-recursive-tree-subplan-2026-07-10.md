# Phase 03 Subplan: Recursive Derivation Tree Search

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_02`

## Phase Objective

Upgrade the derivation tree from ranked static ledger to bounded recursive
search over blocker nodes, candidate hypotheses, backend attempts, and exact
new blockers.

## Entry Conditions Inherited From Previous Phase

- Agent hypotheses are structured candidate expansions.
- Strict proposal contracts prevent blocked paths from publishing as repairs.

## Required Artifacts

- Search loop with `max_depth`, `max_nodes`,
  `max_agent_expansions_per_blocker`, `max_backend_attempts`, and
  `timeout_seconds` budget fields.
- Parent/child provenance for blocker expansion.
- Tests for recursive expansion, budget exhaustion, failed-path memory, and
  no promotion without certifying evidence.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Derivation search-tree and branch-controller tests.
- New recursive-search tests.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of search state and promotion boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can exact blockers be recursively expanded into child search nodes without proof overclaims? |
| Baseline/comparator | Current one-shot branch controller and static branch ranking. |
| Primary criterion | A blocker can spawn validated child hypotheses; each child records backend evidence, exact new blockers, or budget exhaustion; promotion still requires certifying evidence. |
| Veto diagnostics | Infinite/duplicate expansion; child loses source/blocker provenance; budget exhaustion hidden; diagnostic evidence promotes branch. |
| Explanatory diagnostics | Some branches remain blocked because formalization is unavailable. |
| Not concluded | No MCTS optimality, completeness, or global proof search claim. |
| Artifact | Recursive tree code, tests, Phase 03 result. |

## Forbidden Claims Or Actions

- Do not claim search completeness.
- Do not introduce stochastic/random search unless deterministic budgets and
  seeds are recorded.
- Do not parallelize yet.

## Exact Next-Phase Handoff Conditions

Advance to Phase 04 only if recursive paths can carry formalization requests
or exact blockers without weakening promotion guards.

## Stop Conditions

Stop if recursion cannot be bounded deterministically or cannot preserve
parent/child provenance.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 03 result / close record.
3. Draft or refresh Phase 04 subplan.
4. Review Phase 04 for consistency and boundary safety.
