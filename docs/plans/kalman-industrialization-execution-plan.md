# Kalman industrialization execution plan

## Context

The next practical industrial milestone is a Kalman likelihood/filter audit workflow. It is representative of mathematical finance/economics workloads because it involves state-space notation, covariance assumptions, matrix operations, likelihood terms, code/document consistency, and numerical diagnostic tests.

This pass should not attempt a full Kalman verifier. It should build a maintainable vertical slice using existing infrastructure: MathObligation IR, notation hints, assumption diagnostics, operation consistency, diagnostic suggestions, and review packets.

## Phase 1: typed symbol hints for Kalman/state-space notation

Goal: improve MathObligation/notation usefulness for Kalman-style equations.

Work:

- Add a small typed-hint helper for common state-space symbols.
- Detect covariance matrix candidates, residual/vector candidates, transition matrix candidates, observation matrix candidates, and time-indexed variables.
- Mark all detections as candidate hints, not proof assumptions.

Tests:

- `S_t` maps to covariance/matrix candidate.
- `v_t` maps to residual/vector candidate.
- `A_t`/`F_t` maps to transition-matrix candidate.
- Hints retain `candidate_not_assumption` status.

## Phase 2: Kalman operation audit

Goal: detect key code/document operation mismatches for Kalman likelihoods.

Work:

- Add `kalman_workflows.py`.
- Build `audit_kalman_likelihood(...)` around existing likelihood audit and review packet code.
- Require operations: logdet, inverse_or_solve, quadratic_form for likelihood score/log-likelihood style checks.
- Include recommended diagnostics.

Tests:

- Missing logdet is high severity.
- Missing solve/inverse is high severity.
- Correct operation presence leads to unverified/review rather than mismatch if assumptions remain missing.

## Phase 3: Kalman review packet

Goal: produce agent-facing review output.

Work:

- Add `build_kalman_review_packet(...)`.
- Include summary, severity, notation hints, missing assumptions, missing operations, and diagnostic suggestions.

Tests:

- Packet preserves source label and code path.
- Packet includes finite-difference or likelihood diagnostic suggestions when relevant.
- Unsupported proof obligations remain review items.

## Phase 4: benchmark manifest and reset memo

Goal: record this as a vertical workflow milestone.

Work:

- Add tests to document this as a synthetic Kalman workflow fixture.
- Update reset memo with commands, results, limitations, and next steps.

## Verification

Run:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

## Commit policy

Commit all relevant source, tests, and docs. Exclude `.serena/`.
