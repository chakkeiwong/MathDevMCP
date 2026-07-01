# MathDevMCP Real-Task Master Phase 1 Subplan: Category Scoring

## Phase Objective

Confirm and, if needed, repair the category scoring contracts so each real-task
benchmark family has explicit precision/recall meaning, hard-veto semantics,
and aggregation boundaries before public corpus changes are evaluated.

## Entry Conditions Inherited From Previous Phase

- Phase 0 governance has passed or is being closed as already satisfied by
  current artifacts.
- The master program's safety invariant is active.
- Category metrics remain subordinate to hard false-certification and
  evidence-boundary vetoes.

## Required Artifacts

- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `src/mathdevmcp/real_tasks_scoring.py`
- `tests/test_real_tasks_scoring.py`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-01-category-scoring-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-02-public-corpus-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `rg -n "Hard veto|Global F1 is secondary|Global benchmark score|false-certification|evidence-boundary" docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_scoring.py tests/test_real_tasks_candidate_fixtures.py`
- Review:
  - Codex self-review required.
  - Claude read-only review required if scoring semantics are changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are category scoring contracts explicit enough to guide public corpus and reporting without ad hoc case scoring? |
| Baseline/comparator | Existing category scoring subplan and deterministic structural scorer tests. |
| Primary pass criterion | Each category has precision/recall meaning plus hard-veto rules, and aggregation cannot wash out veto failures. |
| Veto diagnostics | A global score or F1 becomes governing; unsupported verification can pass; category ambiguity requires ad hoc scoring. |
| Explanatory diagnostics | Structural scorer pass/fail counts and fixture coverage. |
| Not concluded | Semantic evaluator maturity, free-form model performance, policy readiness. |
| Artifacts | Phase result, test output, refreshed Phase 2 subplan. |

## Forbidden Claims And Actions

- Do not treat global F1 or any aggregate score as a safety or release signal.
- Do not broaden the scorer into a semantic evaluator in this phase.
- Do not weaken false-confidence or forbidden-claim checks to improve totals.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- scoring contracts cover all current benchmark families;
- deterministic scorer tests pass;
- any metric deferrals are explicit;
- Phase 2 subplan states how public cases will preserve these contracts.

## Stop Conditions

- Stop if any family cannot be scored without inventing case-specific rules.
- Stop if test failures suggest the scorer no longer preserves hard-veto
  behavior.
- Stop if fixing scoring would require changing benchmark purpose or safety
  invariant.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 2 subplan.
4. Review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
