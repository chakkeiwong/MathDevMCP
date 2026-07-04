# Phase 5 Result: Targeted Capability Repairs

Date: 2026-06-30

Status: `PASSED_WITH_CLAUDE_REVIEW_UNAVAILABLE_AFTER_PROBE_AND_REDESIGN`

## Phase Objective

Repair only the Phase 4 unexpected status-family failures while preserving the
local/non-gating benchmark boundary, negative controls, and existing seeded
high-level workflow behavior.

## Entry Conditions

- Phase 4 baseline report existed and froze the two material repair targets:
  `RLHLB-08-hmc-value-only-boundary` and
  `RLHLB-09-affine-recovery-assumption-limit`.
- Phase 4 route-gap canary `RLHLB-04-affine-pricing-recursion` had to remain a
  justified abstention/route-gap case.
- Phase 2 manifest/rubric and Phase 3 route ledger remained frozen.

## Actions

- Added a narrow opaque semantic-placeholder equality guard in
  `derive_or_refute`.
- Reused the guard in `prove_or_refute`.
- Blocked finite-domain counterexample promotion for equalities between opaque
  snake-case semantic labels unless source-backed or formal evidence is
  supplied.
- Added focused regression tests for both high-level wrappers.
- Updated real-local benchmark tests to require the repaired Phase 5 behavior.
- Regenerated the repaired real-local benchmark baseline and seeded
  high-level workflow quality report.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can targeted repairs improve real-local workflow behavior without weakening evidence boundaries? |
| Baseline/comparator | Phase 4 baseline with two unexpected status-family mismatches. |
| Primary criterion | Passed: repaired baseline has zero unexpected status-family mismatches and zero boundary violations. |
| Veto diagnostics | Passed locally: seeded quality unchanged, `RLHLB-04` route-gap canary preserved, no benchmark label changes, no aggregate accuracy introduced. |
| Explanatory diagnostics | Before/after repair table, focused pytest, repaired baseline, seeded quality report. |
| Not concluded | No release readiness, public benchmark validity, scientific validation, production correctness, full LaTeX proof checking, or broad theorem proving. |

## Repair Table

| Case | Phase 4 status/failure | Phase 5 status/failure | Evidence class | Interpretation |
| --- | --- | --- | --- | --- |
| `RLHLB-04-affine-pricing-recursion` | `inconclusive` / `correct_abstention_or_route_gap` | `inconclusive` / `correct_abstention_or_route_gap` | `human_review_required` | Canary preserved. |
| `RLHLB-08-hmc-value-only-boundary` | `refuted` / `unexpected_status_family` | `inconclusive` / `correct_abstention_or_route_gap` | `human_review_required` | Placeholder semantic equality is not finite-domain refuted without explicit source/formal evidence. |
| `RLHLB-09-affine-recovery-assumption-limit` | `refuted` / `unexpected_status_family` | `missing_assumptions` / `baseline_evaluable` | `missing_assumption` | Opaque semantic placeholder link now requires source-backed assumptions. |

## Local Checks

- `python3 -m pytest tests/test_real_local_high_level_benchmark.py tests/test_derive_or_refute.py tests/test_prove_or_refute.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_high_level_workflows.py tests/test_counterexample_search.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py -q`
  - Result: `77 passed`.
  - Artifact:
    `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase05_focused_pytest.txt`
- `python3 -m mathdevmcp.cli real-local-high-level-baseline --root .`
  - Result: `completed`.
  - Summary: `case_total=9`, `boundary_violations=0`,
    `unexpected_status_family=0`, `baseline_evaluable=7`,
    `correct_abstention_or_route_gap=2`, `aggregate_accuracy=null`.
  - Artifact:
    `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase05_repaired_baseline.json`
- `python3 -m mathdevmcp.cli high-level-workflow-quality --root .`
  - Result: `quality_thresholds_passed`, `total_results=14`.
  - Artifact:
    `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase05_seeded_quality.json`

## Claude Review

Claude Phase 5 repair review did not return a usable verdict. A small probe
responded, so the prompt was redesigned; the redesigned prompt also hung. This
is recorded as unavailable, not approval. The local close basis is the visible
patch, focused regression coverage, repaired baseline, seeded-quality report,
and frozen-manifest discipline.

## Phase 6 Subplan Review

The Phase 6 subplan remains consistent after Phase 5:

- Entry conditions are satisfied by the repaired baseline and explicit residual
  canary behavior.
- Required artifacts still cover durable packet schema/report, tests, example
  packets, result note, ledger update, and Phase 7 refresh.
- Boundary safety is adequate because Phase 6 packages evidence and non-claims;
  it does not change benchmark expectations or promote diagnostics to proof.
- The next-phase handoff remains exact: proceed only when packets represent
  sources, assumptions, backend checks, counterexamples, gaps, actions, and
  non-claims without changing benchmark pass criteria.

## Handoff

Proceed to Phase 6: derive/proof packet standard. Phase 6 must use the repaired
baseline as input, preserve `aggregate_accuracy=null`, and keep
placeholder-semantic abstentions visible rather than converting them into proof
or refutation.
