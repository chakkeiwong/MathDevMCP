# Frontier industrialization execution plan

## Context

MathDevMCP now has industrial scaffolding for proof audit, parser benchmarking, Lean checking/export, LeanDojo readiness, MathObligation IR, assumption diagnostics, symbolic checks, operation consistency, and a first likelihood implementation workflow. The remaining challenge is making these outputs useful for department developers and coding agents on real mathematical finance/economics frontier projects without overbuilding bespoke theorem-proving infrastructure.

This pass focuses on review packets, richer but still minimal IR, notation/assumption extraction, diagnostic test suggestions, benchmark corpus organization, and deployment/dependency metadata.

## Phase 1: review packet workflow

Goal: create compact agent-facing review packets that combine existing evidence into one actionable artifact.

Work:

- Add `review_packet.py`.
- Build `build_likelihood_review_packet(...)` around `audit_likelihood_implementation(...)`.
- Include summary, severity, source label, code path, missing assumptions, missing operations, backend statuses, and recommended next actions.

Tests:

- Missing operation becomes high-severity action.
- Missing assumptions become review actions.
- Packet preserves provenance.

## Phase 2: MathObligation IR v2 shape/type hints

Goal: improve IR usefulness without building a full symbolic algebra system.

Work:

- Add optional fields or helper functions for symbol role/domain/shape hints.
- Detect simple matrix/vector/scalar/time-index hints from notation and context.
- Keep all hints diagnostic unless explicitly stated in assumptions.

Tests:

- `S_t` is classified as covariance/matrix candidate in Kalman context.
- `v_t` is classified as vector/residual candidate.
- Hints do not become proof premises.

## Phase 3: notation and assumption extraction

Goal: extract department-relevant notation/assumption candidates.

Work:

- Add `notation.py` for lightweight notation-table/prose pattern extraction.
- Extract roles such as state vector, shock vector, covariance, transition matrix, likelihood, SDF, Euler equation.
- Distinguish explicit assumptions from nearby candidates and inferred missing assumptions.

Tests:

- Fixture notation prose maps symbols to roles.
- Explicit SPD/invertibility/differentiability assumptions are recognized.
- Missing assumptions remain marked as missing when not stated.

## Phase 4: diagnostic test suggestions

Goal: produce suggested numerical/code diagnostics from audit findings.

Work:

- Add `diagnostic_tests.py`.
- Suggest finite-difference gradient checks, shape checks, logdet/solve synthetic tests, HMC energy checks, simulation-based calibration placeholders, and parser/proof follow-ups.
- Keep suggestions as plans, not generated files.

Tests:

- Missing logdet suggests synthetic likelihood/logdet test.
- Derivative obligations suggest finite-difference gradient check.
- HMC/Hamiltonian context suggests energy conservation check.

## Phase 5: benchmark corpus manifest

Goal: organize real/synthetic/private benchmark strategy.

Work:

- Add `benchmark_manifest.py` with benchmark categories and privacy policy.
- Keep private/sanitized corpora outside git by default.
- Expose machine-readable manifest for agents.

Tests:

- Manifest contains parser, proof, code-doc, assumptions, workflow, false-confidence, and private-corpus categories.
- Private corpus entries are marked external/not-in-git.

## Phase 6: deployment/dependency policy metadata

Goal: make installation/deployment constraints visible to agents.

Work:

- Add `deployment.py` policy report.
- Include optional backend groups, external executables, recommended isolation for LeanDojo, timeout/resource policy, no-exfiltration statement.
- Integrate with `doctor` if small and maintainable.

Tests:

- Policy report includes LeanDojo isolation warning.
- Base package policy says heavy tools are optional.

## Phase 7: final verification and reset memo

Run:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

Update reset memo with outcomes and commit all relevant files, excluding `.serena/`.
