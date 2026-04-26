# Typed/dimensional MathObligation execution plan

## Context

The project now has parser/AST benchmark coverage over sanitized department-style fixtures. The next highest-value gap is richer `MathObligation` semantics: matrix shapes, random-variable/stochastic-process hints, likelihood/posterior objects, derivative objects, and explicit missing-dimension diagnostics. This should turn structural parser/AST evidence into a more useful audit object without claiming full formal verification.

## Safety invariant

Typed and dimensional records are audit metadata. They are not proof premises unless a backend independently verifies a claim under explicit assumptions. Candidate roles, inferred shapes, and missing assumptions must remain diagnostic and must not upgrade status to `verified`.

## Phase 0: plan, reset memo, and second-developer audit

Work:

- Update the reset memo with the current request.
- Write this execution plan.
- Write a second-developer audit.

Tests:

- Documentation-only phase; later full verification covers repository consistency.

## Phase 1: typed IR records

Goal: extend `MathObligation` with conservative typed/dimensional metadata.

Work:

- Add typed symbol descriptors for scalar, vector, matrix, random variable, stochastic process, likelihood/posterior, derivative, and unknown candidates.
- Add dimension constraints such as square matrix, conformable product, inverse requires invertibility, determinant/logdet requires square matrix, and derivative requires differentiability.
- Add stochastic/process markers for time-indexed symbols, expectations, conditional objects, posterior/log-likelihood expressions, and Hamiltonian/HMC expressions.
- Preserve existing fields and contract compatibility.

Tests:

- Existing minimal IR tests still pass.
- State-space/Kalman fixture obligation records matrix/vector/time-indexed candidates and missing shape assumptions.
- HMC/posterior fixture records posterior, gradient, and Hamiltonian-style requirements.

## Phase 2: diagnostics and routing helpers

Goal: expose typed IR as a workflow-ready diagnostic, not just a passive data structure.

Work:

- Add a `diagnose_typed_obligation(...)` helper.
- Add `typed_obligation_for_label(...)` to audit a labeled equation and return its typed IR.
- Add result status `typed_review`/`needs_assumptions`-style diagnostics inside the payload while keeping the contract conservative.
- Include recommended backend route hints: symbolic, lean candidate, numeric diagnostic, or human review.

Tests:

- Missing shape/invertibility assumptions are reported for state-space likelihood.
- Explicit assumption context reduces missing diagnostics when applicable.
- Unsupported stochastic notation remains human-review oriented.

## Phase 3: CLI/MCP and benchmark gate

Goal: make typed IR useful to coding agents and benchmark it.

Work:

- Add CLI command `typed-obligation-label`.
- Add MCP facade/FastMCP tool `typed_obligation_label`.
- Add benchmark category `typed_ir` with realistic state-space and HMC/posterior cases.
- Include one expected abstention/review case where typed metadata is useful but not proof.

Tests:

- CLI returns the `typed_math_obligation_diagnostic` contract.
- MCP facade/server expose and call the new tool.
- Benchmark gate totals and summaries are updated.

## Phase 4: verification, audit, tidy, reset memo, commit

Work:

- Run targeted tests.
- Run full suite.
- Run benchmark gate.
- Run `git diff --check`.
- Update reset memo with the final checkpoint outcome.
- Commit relevant source, docs, tests, and fixtures while excluding `.serena/` and unrelated local files.

Verification commands:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

## Non-goals

- Do not implement dependent types.
- Do not prove matrix calculus.
- Do not infer assumptions as proof premises.
- Do not execute external numerical libraries.
- Do not replace Lean/Sage/SymPy routing.
