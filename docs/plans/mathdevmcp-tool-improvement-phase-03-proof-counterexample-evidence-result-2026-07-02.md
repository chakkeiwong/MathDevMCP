# Phase 3 Result: Proof And Counterexample Evidence

Date: 2026-07-02

Status: `PASSED_AFTER_REPAIR`

## Phase Objective

Strengthen `prove_or_counterexample` so proof and refutation statuses are tied
to concrete backend evidence, counterexample artifacts, or explicit proof
obligations.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Proof/refutation outputs can expose concrete evidence without overclaiming. |
| Baseline/comparator | Existing `prove_or_counterexample` results, Phase 2 scoped assumption taxonomy, and benchmark cases RLHLB-01/RLHLB-03. |
| Primary criterion | Passed after repair locally: proof evidence is emitted only when a certifying backend attempt and proved scoped obligation artifact are present; backend-counterexample evidence is emitted only when a concrete counterexample summary is present; unavailable backends remain diagnostic. |
| Veto diagnostics | No finite probe promoted to theorem, no backend-counterexample evidence without concrete counterexample artifact, no backend failure treated as false claim, and no proof promotion without certifying artifacts. |
| Explanatory diagnostics | Backend route attempts, scoped obligation records, and counterexample summaries. |
| Not concluded | No broad theorem-proving ability or proof correctness beyond scoped certified obligations. |

## Artifacts

- `src/mathdevmcp/high_level_workflows.py`
- `tests/test_high_level_workflows.py`
- `tests/test_prove_or_counterexample.py`
- Refreshed Phase 4 subplan:
  `docs/plans/mathdevmcp-tool-improvement-phase-04-derive-route-plans-subplan-2026-07-02.md`

## Local Checks

| Check | Result |
| --- | --- |
| `python3 -m pytest tests/test_prove_or_counterexample.py tests/test_derive_from.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py` | Passed after repair: 39 tests. |
| `python3 -m pytest tests/test_prove_or_refute.py tests/test_debug_derivation.py` | Passed: 13 tests. |
| `git diff --check` over touched Phase 3 implementation/tests/docs | Passed. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 4 | Passed after repair and review | No veto triggered | Evidence metadata is explanatory and depends on existing low-level route quality | Add derivation route-plan artifacts | No broad proof capability or theorem correctness claim |

## Phase 4 Handoff

Phase 4 may reuse proof/refutation evidence metadata for derivation route plans.
It must not synthesize unchecked derivation chains or report route gaps as
proof.
