# Phase 05 Subplan: Budgeted Repair Branch Search

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Implement budgeted branch search over assumption sets, derivation decompositions,
and backend routes using typed obligations and executable/blocker outcomes.

## Entry Conditions Inherited From Previous Phase

- Branches have typed obligations and executable/blocker backend outcomes.
- Backend evidence is bounded and non-certifying unless a certifying backend
  accepts the scoped target.
- Phase 04 branch records expose `backend_attempts`, `translation_attempts`,
  `translation_blockers`, and `backend_evidence`, so Phase 05 must consume
  those fields directly instead of inferring branch status from root-only
  controller output.

## Required Artifacts

- Branch expansion records for assumption addition, derivation split,
  formalization route, backend attempt, and blocker.
- Ranking fields: closure strength, source support, backend certification
  status, blocker specificity, non-minimality.
- Deterministic rank explanation per branch, including why a blocked stochastic
  branch is ranked above or below another branch.
- Tests for branch failure/success/blocker ranking.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-05-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_document_derivation_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/document_derivation_tree.py`
- `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the tool rank repair branches by evidence rather than listing templates? |
| Baseline/comparator | Current branch list with no real expansion/ranking. |
| Primary criterion | Report can say branch A failed for a specific blocker, branch B is partial, branch C is best-supported. |
| Veto diagnostics | Ranking based on branch count; unsupported branch promoted; budget exhaustion hides attempted actions. |
| Explanatory diagnostics | Branch budget, blocker taxonomy, backend availability. |
| Not concluded | Best-supported branch is not globally optimal unless proven. |
| Artifact | Tests and Phase 05 result. |

## Forbidden Claims Or Actions

- Do not call this complete MCTS.
- Do not claim global optimality or minimality.

## Exact Next-Phase Handoff Conditions

Advance to Phase 06 only if reports can render branch ranking and blocker
specificity without inventing repairs.

## Stop Conditions

Stop if branch search would require long runs or changing proof-boundary rules.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 05 result / close record.
3. Draft or refresh Phase 06 subplan.
4. Review Phase 06 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
