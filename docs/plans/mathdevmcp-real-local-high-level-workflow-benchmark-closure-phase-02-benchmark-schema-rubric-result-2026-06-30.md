# Phase 2 Result: Benchmark Schema And Rubric

Date: 2026-06-30

Status: `PASSED_WITH_CLAUDE_R2_UNAVAILABLE_AFTER_R1_REPAIRS`

## Objective

Convert the Phase 1 real-local case inventory into a durable local benchmark
schema and rubric before any current-workflow baseline run or repair.

## Skeptical Audit

- Wrong baseline checked: Phase 2 uses the Phase 1 inventory and seeded
  high-level benchmark conventions; it does not use current workflow outputs.
- Proxy metric checked: case count is frozen for reproducibility but is not a
  benchmark-quality claim.
- Stop conditions checked: the schema must represent assumptions,
  counterexamples, abstentions, boundary violations, and minimal packets
  separately.
- Hidden assumptions checked: local source paths are local/non-gating anchors
  only; they are not public fixtures or source-truth certificates.
- Artifact fit checked: a machine-readable manifest plus validator answers the
  Phase 2 question better than prose-only rubric text.
- Environment mismatch checked: no package install, network fetch, GPU action,
  sibling-repo edit, release policy change, or benchmark promotion was used.

Audit result: `PASSED`.

## Artifacts Written

```text
benchmarks/real_tasks/holdout_local/real_local_high_level_workflow_benchmark_cases.json
src/mathdevmcp/real_local_high_level_benchmark.py
tests/test_real_local_high_level_benchmark.py
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-02-schema-rubric-note-2026-06-30.md
```

Updated:

```text
src/mathdevmcp/cli.py
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-03-backend-grounding-evidence-subplan-2026-06-30.md
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-claude-review-trail-2026-06-30.md
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-visible-execution-ledger-2026-06-30.md
```

Saved check artifacts:

```text
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase02_schema_validation.json
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase02_focused_pytest.txt
```

## Schema Summary

```text
case_total: 9
workflow_total: 6
negative_control_total: 5
aggregate_accuracy: null
workflow_coverage:
  - assumptions_for
  - audit_math_to_code
  - debug_derivation
  - derive_from
  - prepare_review_packet
  - prove_or_counterexample
```

The manifest freezes `expected_case_count: 9`; later phases must not silently
add, drop, or reclassify cases before the Phase 4 baseline.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. The manifest and validator cover all cases, six workflow contracts, negative-control semantics, status/evidence compatibility, minimal packet schema, scoring dimensions, good abstention, and forbidden claims. |
| Veto diagnostics | No aggregate accuracy or gold-answer field is allowed; source/backend/probe/abstention channels remain separate; `routing_only` requires route availability and cannot carry certifying/refuting evidence. |
| Explanatory diagnostics | Validator findings, focused pytest, rubric note, and Claude R1 review. |
| Not concluded | Current workflow performance, repair success, benchmark-gate readiness, public benchmark validity, release readiness, scientific validation, production correctness, full LaTeX proof checking, or broad theorem proving. |

## Required Checks

Schema check:

```text
python3 -m mathdevmcp.cli real-local-high-level-benchmark-schema --root .
```

Result:

```text
consistent
case_total: 9
workflow_total: 6
negative_control_total: 5
aggregate_accuracy: null
```

Focused pytest:

```text
python3 -m pytest tests/test_real_local_high_level_benchmark.py tests/test_real_local_high_level_pilot.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py -q
```

Result:

```text
36 passed
```

## Claude Review

Phase 2 Claude R1 returned `REVISE` with four valid findings:

1. per-case negative-control status/evidence compatibility was missing;
2. workflow contracts lacked result-preservation artifacts;
3. `routing_only` did not require route-availability evidence;
4. the validator allowed 5-10 cases rather than the frozen nine-case manifest.

Repairs:

- status-specific required/forbidden evidence constraints and outcome keyword
  checks;
- required `result_artifact` in workflow contracts;
- required `route_availability` for `routing_only` and forbade
  certifying/refuting evidence there;
- required and validated `expected_case_count: 9`;
- added regression tests for all four findings.

Claude R2 was unavailable after the repair:

- original delta review hung without output;
- tiny probe returned `PROBE_OK`;
- redesigned checklist prompt hung without output;
- final one-line verdict prompt hung without output.

No R2 `REVISE` finding was produced. The phase closes on visible R1 repairs,
focused regression tests, and local checks rather than treating Claude silence
as approval.

## Next-Phase Review

Phase 3 subplan was refreshed to inherit:

- frozen nine-case manifest;
- per-workflow `result_artifact` requirement;
- route-availability ledger per case;
- Phase 2 minimal packet stubs for all nine cases;
- a stop condition for any unreviewed manifest/rubric change.

Consistency review:

- Correctness: Phase 3 now answers routing and packet feasibility, not
  benchmark pass rate.
- Feasibility: it can be implemented with existing source-adapter, symbolic,
  counterexample, proof-gap, code/equation, and review-packet modules.
- Artifact coverage: route ledger plus packet stubs preserve the Phase 2
  result artifact contract.
- Boundary safety: Phase 3 explicitly forbids silent schema/rubric changes,
  backend absence as refutation, and diagnostic evidence as proof.

## Handoff

Proceed to Phase 3 backend grounding evidence layer.
