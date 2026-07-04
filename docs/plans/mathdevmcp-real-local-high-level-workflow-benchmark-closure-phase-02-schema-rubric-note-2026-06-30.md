# Phase 2 Schema And Rubric Note: Real-Local High-Level Workflow Benchmark Closure

Date: 2026-06-30

Status: `DRAFTED_FOR_PHASE_2_CHECKS`

## Objective

Freeze a durable local benchmark schema for the nine real-local high-level
workflow cases before running current workflows or making repairs.

## Artifacts

- Manifest:
  `benchmarks/real_tasks/holdout_local/real_local_high_level_workflow_benchmark_cases.json`
- Validator:
  `src/mathdevmcp/real_local_high_level_benchmark.py`
- Focused tests:
  `tests/test_real_local_high_level_benchmark.py`
- CLI:
  `python3 -m mathdevmcp.cli real-local-high-level-benchmark-schema --root .`

## Schema Contract

Each case must record:

- `id`, `title`, `workflow`, `tier`, and `question`;
- bounded `source_snapshot.source_files` with relative paths, line ranges, and
  source roles;
- expected route and expected outcome type;
- expected evidence classes;
- scoring-rubric dimensions;
- negative-control status and scoring semantics where applicable;
- good-abstention definition;
- minimal review-packet schema;
- forbidden claims.

The manifest metadata freezes `expected_case_count: 9`; later phases must not
silently drop or add cases before the Phase 4 baseline run.

The schema forbids:

- `case_status`;
- `accuracy`;
- `gold_answer`;
- non-null aggregate accuracy.

## Minimal Review-Packet Schema

Every pre-repair and post-repair case packet must include:

| Field | Purpose |
| --- | --- |
| `question` | User-facing mathematical question. |
| `source_anchors` | Bounded source paths and line ranges. |
| `assumptions` | Stated, missing, or route-required assumptions. |
| `route_availability` | Source adapter/backend/probe/review route state. |
| `derivation_proof_steps` | Steps attempted or explicitly absent. |
| `backend_checks` | Symbolic/formal/numeric attempts and status. |
| `counterexamples` | Concrete counterexamples or empty list. |
| `gaps` | Localized proof/derivation/code gaps. |
| `actions` | Smallest justified next actions. |
| `evidence_classes` | Declared evidence classes, not blended verdicts. |
| `non_claims` | Boundary-preserving statements. |

## Rubric Dimensions

| Dimension | Good Evidence | Veto |
| --- | --- | --- |
| `source_grounding` | Bounded source anchors and source-route explanation. | Wholesale source copy or unanchored source claim. |
| `assumption_correctness` | Required assumptions are stated with provenance and status. | Silent insertion of assumptions or global minimality claim. |
| `derivation_proof_validity` | Backend/source-adapter support or explicit gap. | LLM prose treated as proof. |
| `counterexample_quality` | Concrete scoped counterexample for refutation. | Refutation without counterexample or scoped contradiction. |
| `backend_evidence` | Backend attempt/result separated from source and probe channels. | Backend absence treated as refutation. |
| `abstention_quality` | Missing route/evidence and next action are explicit. | Inconclusive answer hidden as success. |
| `boundary_discipline` | Forbidden claims and non-claims are preserved. | Local result promoted to release/scientific/public validity. |

## Negative-Control Semantics

Negative controls predeclare one of:

- `refuted`;
- `missing_assumptions`;
- `backend_unavailable`;
- `not_encodable`;
- `insufficient_evidence`;
- `routing_only`.

`routing_only` is diagnostic and cannot count as mathematical correctness.
`insufficient_evidence` and `missing_assumptions` can be good outcomes when
they preserve boundaries and identify the next evidence action.

## Per-Workflow Evidence Contracts

The manifest metadata freezes evidence contracts for all six workflow families:

- `derive_from`;
- `prove_or_counterexample`;
- `assumptions_for`;
- `debug_derivation`;
- `audit_math_to_code`;
- `prepare_review_packet`.

Each contract states comparator, primary criterion, veto diagnostics,
explanatory diagnostics, good-abstention definition, and forbidden claims.
Each contract also names the result-preservation artifact: the Phase 4/5
per-case review packet plus route-availability ledger row.

## Status-Specific Negative-Control Checks

The validator requires negative-control statuses to be compatible with expected
evidence and outcome text:

- `refuted` requires contradiction or counterexample evidence;
- `missing_assumptions` requires missing-assumption evidence;
- `backend_unavailable` requires backend-unavailable evidence;
- `not_encodable` requires not-encodable evidence;
- `insufficient_evidence` requires human-review, review-packet, or backend
  unavailable evidence and forbids certifying evidence;
- `routing_only` requires route-availability evidence and forbids certifying
  or refuting evidence.

## Non-Claims

This schema and rubric do not establish current workflow performance,
capability improvement, benchmark-gate readiness, public benchmark validity,
release readiness, scientific validation, production correctness, external
reproducibility, full LaTeX proof checking, or broad theorem proving.
