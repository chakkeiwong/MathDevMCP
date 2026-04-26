# Remaining industrial gaps execution plan

## Context

MathDevMCP has a strong scaffold: proof audit, Lean artifact checking, Lean export, LeanDojo readiness smoke, parser benchmarking, minimal MathObligation IR, assumption diagnostics, symbolic wrapper, operation consistency, and a first likelihood implementation workflow. The remaining work is to turn these pieces into a truly useful industrial tool for mathematical finance/economics coding agents.

The next execution should focus on high-leverage vertical slices that improve real usefulness without expanding bespoke infrastructure beyond what one maintainer can support.

## Phase A: real proof tooling validation boundary

Goal: make Lean/LeanDojo readiness truthful.

Work:

- Add richer LeanDojo environment diagnostics to the existing spike result.
- Record LeanDojo version, Lean version, Lake version, Python executable, and whether a real Dojo interaction was attempted.
- Keep status `inconclusive` for real Dojo interaction until a traced theorem target is available.
- Add a test that this boundary is explicit.

Exit criteria:

- Agent output cannot confuse direct Lean proof checking with real LeanDojo interaction.

## Phase B: parser benchmark scoring hardening

Goal: avoid inflated parser confidence.

Work:

- Score parser outputs against expected fixture labels.
- Add missing-label reporting.
- Record generated-label filtering behavior for LaTeXML/Pandoc.
- Keep parser recommendation conservative.

Exit criteria:

- Parser benchmark can say which backend preserved all expected labels.

## Phase C: IR and assumption diagnostics integration

Goal: make proof audit and assumption diagnostics share a durable object.

Work:

- Ensure MathObligation IR covers unresolved constructs and symbol roles.
- Extend assumption diagnostics to return explicit and inferred-missing assumption categories.
- Add finance/econ role detection for likely state/covariance/likelihood symbols.

Exit criteria:

- Kalman/Hessian-style obligations produce actionable missing-assumption diagnostics.

## Phase D: symbolic/backend evidence routing

Goal: make symbolic checking a first-class adapter, not hidden inside proof obligations.

Work:

- Keep a thin `symbolic_backend` wrapper around SymPy and Sage availability.
- Preserve backend evidence and safe grammar checks.
- Avoid implementing a full LaTeX expression parser in this slice.

Exit criteria:

- Simple algebra routes to SymPy; unsafe notation abstains.

## Phase E: structure-aware operation consistency

Goal: improve practical code/document auditing.

Work:

- Add operation extraction for logdet, inverse/solve, Cholesky, quadratic forms, trace, gradients, Hessians.
- Compare documented required operations to code operations.
- Keep this as operation presence, not full semantic equivalence.

Exit criteria:

- Likelihood-style missing logdet or solve operations are detected.

## Phase F: first industrial vertical workflow

Goal: provide one useful coding-agent workflow rather than many shallow names.

Work:

- Build `audit_likelihood_implementation` combining proof audit, assumption diagnostics, and operation consistency.
- Return concise status plus detailed nested evidence.
- Add tests for missing operation and missing assumptions.

Exit criteria:

- Agent can audit a likelihood implementation and get actionable evidence.

## Phase G: packaging/security/docs baseline

Goal: keep deployment safe and maintainable.

Work:

- Keep `doctor` as the source of truth for capabilities/conflicts.
- Ensure external commands have timeouts.
- Document that LeanDojo may need isolated environment because of dependency conflicts.
- Update reset memo with commands and evidence.

Exit criteria:

- All new backends are optional and failures remain structured.

## Phase H: commit checkpoint

Goal: preserve coherent work.

Work:

- Run full tests.
- Run benchmark gate.
- Run `git diff --check`.
- Review `git status` for unexpected files.
- Commit all relevant tracked and new files, excluding unrelated `.serena/`.

Commit message should summarize industrial scaffolding and include the required co-author trailer.
