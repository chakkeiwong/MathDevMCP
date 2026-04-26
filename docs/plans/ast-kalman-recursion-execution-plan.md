# AST/Kalman recursion execution plan

## Context

The current Kalman workflow can detect operation presence in likelihood code, but it still relies on regex-style operation matching. The next industrial slice should add AST-level Python operation extraction and a conservative Kalman recursion audit. The goal is not a full Kalman verifier. The goal is to give coding agents a more structured way to review whether a documented state-space recursion is plausibly represented in code, with provenance, missing-operation findings, shape-guard diagnostics, and expected abstention.

## Safety invariant

No AST match, symbol-name guess, shape hint, parser output, backend failure, or LLM claim may become a verified mathematical claim. This pass may report `consistent`, `mismatch`, `unverified`, or `inconclusive`, but it should reserve strong claims for deterministic evidence. Operation and recursion matches are review evidence, not proof.

## Phase 0: reset memo and planning

Work:

- Record the current request in the reset memo.
- Write this execution plan.
- Write a second-developer audit before code changes.

Tests:

- Documentation-only phase; no test run required beyond later full verification.

## Phase 1: AST operation graph

Goal: replace a purely regex operation view with a small, maintainable AST-backed graph for Python code.

Work:

- Add an `ast_operation_graph` module.
- Parse Python source with `ast.parse`.
- Extract assignment, return, call, binary-matrix operation, subscript, loop, and variable-use nodes.
- Classify operations such as `logdet`, `inverse_or_solve`, `cholesky`, `quadratic_form`, `matmul`, `prediction_update`, `innovation_update`, `covariance_update`, `kalman_gain`, and `state_update`.
- Preserve line/column provenance for extracted nodes.
- Return structured `inconclusive` payloads for syntax errors rather than crashing.

Tests:

- Detect `np.linalg.slogdet`, `np.linalg.solve`, and `v @ solve(S, v)`.
- Detect Kalman recursion assignments from realistic variable names.
- Syntax errors return `inconclusive`.
- Findings include line numbers.

## Phase 2: Kalman recursion audit

Goal: audit whether a Python implementation contains the core state-space recursion operations expected from a documented Kalman filter.

Work:

- Extend `kalman_workflows.py` with `audit_kalman_recursion(...)`.
- Require prediction, innovation covariance, solve/gain, state update, and covariance update operations.
- Include AST operation graph evidence and source provenance.
- Keep status conservative: `mismatch` for missing required recursion operations, `unverified` when operations are present but assumptions/shape guards are incomplete, and `consistent` only when the structural audit and required shape guards are present.

Tests:

- Good fixture/code snippet has all required recursion operations but remains `unverified` when proof/assumptions are outside scope.
- Bad fixture missing covariance update reports `mismatch`.
- AST evidence is included in the contract payload.

## Phase 3: shape/dimension diagnostics

Goal: add practical diagnostics for shape guards without attempting dependent typing.

Work:

- Detect shape assertions and dimension checks in Python AST.
- Require conservative guard evidence for state-space code: matrix/vector dimensions, square covariance, observation/state compatibility, and covariance symmetry/PSD hints when explicitly present.
- Report missing guards as diagnostics, not proof failures.

Tests:

- Code with explicit shape assertions reports guard evidence.
- Code without shape assertions reports missing shape diagnostics.
- Missing guards prevent overconfident `consistent` status.

## Phase 4: benchmark and agent surface

Goal: make the new slice visible to benchmark gates and coding agents.

Work:

- Add realistic fixture code for a Kalman recursion.
- Add benchmark cases for AST/Kalman recursion.
- Expose the workflow through the MCP facade and CLI if the local pattern supports doing so without broad churn.
- Keep benchmark failures strict and expected abstentions explicit.

Tests:

- Targeted AST/Kalman tests pass.
- Benchmark totals and summaries are updated.
- CLI/MCP facade tests cover the new workflow if exposed.

## Phase 5: verification, tidy, reset memo, commit

Work:

- Run targeted tests.
- Run the full test suite.
- Run the benchmark gate.
- Run `git diff --check`.
- Update reset memo with implementation outcome, verification commands, limitations, and next steps.
- Commit relevant source, tests, fixtures, and docs. Exclude `.serena/`.

Verification commands:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

## Non-goals

- Do not implement a full Kalman verifier.
- Do not infer mathematical assumptions as proof premises.
- Do not add a custom symbolic matrix algebra system.
- Do not require external backends for this slice.
- Do not replace Lean/Sage/SymPy paths.
