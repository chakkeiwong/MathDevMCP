# Benchmark fixtures

This directory will hold small documents, code snippets, and expected outputs for evaluating MathDevMCP tools.

Initial benchmark classes:

1. Long-document retrieval
2. Code-document consistency
3. Derivation auditing
4. Document-grounded code generation
5. Dense-math reading support

For a benchmark program grounded in real cross-repo mathematical/code-document tasks rather than only synthetic fixtures, see [real_tasks/README.md](real_tasks/README.md).

## Mathematical debugging workbench benchmark

The `math_debugging_workbench` category is a seeded local benchmark for the
question-centered workflows:

- derive or refute a scoped equality;
- prove or refute when a deterministic backend can certify the claim;
- identify missing assumptions;
- localize the first bad derivation step;
- preserve boundaries for structural, numeric, generated-test, review-packet,
  impact, notation, and literature/local applicability evidence.

Run the formal gate:

```bash
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
```

Run the seeded quality report:

```bash
PYTHONPATH=src python -m mathdevmcp.cli workbench-benchmark-quality --root "$PWD"
```

The quality report checks tool coverage, oracle-class coverage, negative-control
rate, boundary preservation, deterministic rerun stability, run-manifest
coverage, and a small in-memory mutation panel for proof-promotion mistakes.
It is not a release-readiness claim, external benchmark score, or broad theorem
proving claim.

## High-level workflow benchmark

The `high_level_math_workflows` category is a seeded local benchmark for the
operator-facing workflow layer:

- `derive_from`;
- `prove_or_counterexample`;
- `assumptions_for`;
- `debug_derivation`;
- `audit_math_to_code`;
- `prepare_review_packet`.

Run the high-level quality report:

```bash
PYTHONPATH=src python -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"
```

The report requires at least two cases per workflow, a negative-control rate of
at least 40 percent, full seeded pass, boundary preservation, deterministic
rerun stability, and mutation probes that catch proof-boundary promotions such
as structural matches or review packets being mislabeled as proofs. It measures
whether the local seeded cases preserve the declared evidence contract. It does
not establish external benchmark validity, release readiness, scientific
validity, or general theorem-proving ability.

## Real-local high-level workflow closure

The real-local high-level workflow benchmark under
`real_tasks/holdout_local/real_local_high_level_workflow_benchmark_cases.json`
is a local/non-gating regression surface for the same operator-facing workflows
on real local repo/document material.

Run the schema, route, baseline, and durable packet reports:

```bash
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-benchmark-schema --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-routes --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-baseline --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-packets --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli real-local-high-level-final-matrix --root "$PWD"
```

The current closure target is per-case boundary behavior, not aggregate
accuracy. The reports must keep `aggregate_accuracy` as `null`, preserve
negative-control abstentions and missing assumptions, and keep durable packets
as review artifacts rather than proof certificates.
The final matrix is a case-accountability artifact for local regression
handoff; it is not a promotion decision.

These reports are not included in `benchmark-gate` and are not release-readiness
evidence, public benchmark validity evidence, scientific validation, external
reproducibility evidence, or a general theorem-proving claim. Promotion into a
formal gate would require a separate reviewed policy decision and a public or
properly governed corpus boundary.

Licensed external benchmark adaptations use placeholder-only protocol files
under [workbench_external/](workbench_external/). Populated external packs remain
diagnostic and local/provenance-controlled unless a later reviewed phase
promotes a public redistributable subset.
