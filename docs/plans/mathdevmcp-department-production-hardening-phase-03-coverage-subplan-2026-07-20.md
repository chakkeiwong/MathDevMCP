# Phase 03 Coverage And Production-Boundary Tests

## Objective

Measure executable coverage and close the missing production-boundary tests
without treating coverage percentage as mathematical evidence.

## Entry Conditions

Phase 01 package path is testable; optional scanner/coverage dependencies may be
installed only in disposable environments or CI.

## Required Artifacts

- Coverage configuration with line and branch reporting for
  `src/mathdevmcp`, excluding generated/legacy scripts where justified.
- CI artifact upload and a reviewed minimum threshold for critical packages.
- Direct tests for modules without direct coverage, beginning with
  `assumption_gap_proposals`, `role_obligations`, `specialist_execution`,
  `parser_capability_extractors`, `mcp_entrypoint`, and `release_profiles`.
- Wheel-installed runtime tests.
- Required department-profile tests and an explicit skipped-capability report.
- Performance/memory budget test for representative document sizes.
- POSIX/fallback transport tests or a documented Linux/WSL-only support claim.
- Bounded property/mutation probes for artifact/path/parser boundaries.

## Checks

- Full pytest with coverage and branch data.
- Focused critical-package threshold.
- Negative tests for missing dependency, malformed output, timeout, symlink,
  traversal, digest tamper, and private-path leakage.
- External-tool marker report with required-vs-optional classification.
- Performance smoke with declared descriptive thresholds.

## Evidence Contract

Coverage measures executed code paths only. It cannot establish mathematical
truth, backend certification, or scientific validity. Thresholds are engineering
promotion criteria and must not be presented as scientific quality scores.

## Forbidden Claims/Actions

- Do not raise thresholds to hide uncovered risk.
- Do not convert optional external skips into passes.
- Do not add brittle source-string assertions as a substitute for behavior.

## Handoff Conditions

Coverage and skip artifacts are retained, all critical path tests pass, and each
remaining uncovered module has an owner and explicit rationale.

## Stop Conditions

Stop if coverage cannot run in any authorized disposable/CI environment, if
the full test run is not settled, or if a new test reveals contract drift.
