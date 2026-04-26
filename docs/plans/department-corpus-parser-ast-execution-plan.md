# Department corpus parser/AST execution plan

## Context

The AST/Kalman-recursion checkpoint added structured Python operation evidence and a conservative recursion audit. The next industrial step is to test that scaffolding against more realistic, sanitized department-style material rather than only compact synthetic snippets.

This pass should add a small but representative corpus slice for mathematical finance/economics developers working across computational econometrics, computational statistics, ML/LLMs, large-scale Bayesian learning, computational physics, and applied mathematics. The goal is not to make the tool "done." The goal is to expand measured parser and AST coverage while keeping false-confidence controls explicit.

## Safety invariant

No parser output, AST operation match, naming convention, inferred assumption, generated diagnostic, backend timeout, or LLM claim may become a verified mathematical claim. Realistic fixtures should improve measured review coverage, not weaken abstention.

## Phase 0: reset memo and planning

Work:

- Update the reset memo before implementation.
- Write this execution plan.
- Write a second-developer audit.

Tests:

- Documentation-only phase; later full verification covers repository consistency.

## Phase 1: sanitized department corpus fixtures

Goal: add realistic but small fixtures that exercise parser provenance and AST operation extraction across multiple departmental styles.

Work:

- Add a sanitized state-space/Kalman document fixture with notation, assumptions, equations, labels, and macro-style commands.
- Add a sanitized Bayesian/HMC document fixture with posterior, Hamiltonian, leapfrog, and gradient labels.
- Add Python fixtures that mimic NumPy/JAX/PyTorch-like idioms without requiring those packages at test time.
- Include one positive structural case and one seeded false-confidence case.

Tests:

- Current LaTeX index preserves target labels and section paths.
- Parser benchmark expected-label scoring includes the new labels.
- AST graph detects relevant operations in each code fixture.

## Phase 2: AST operation recognition hardening

Goal: broaden AST recognition for common scientific-computing idioms without pretending semantic equivalence.

Work:

- Recognize backend-family calls from names/attributes such as `jax.numpy`, `torch`, `numpyro`, and local wrappers.
- Add operations for gradients, posterior/log probability, leapfrog/Hamiltonian updates, particle/logsumexp normalization, and scan/vectorized-loop idioms where safely detectable.
- Preserve line/column evidence for every operation.

Tests:

- JAX-style `grad`, `vmap`, `scan`, and `slogdet` are detected.
- HMC-style leapfrog/gradient/Hamiltonian update operations are detected.
- Particle-filter `logsumexp` normalization is detected.
- Unsupported or ambiguous code remains structural evidence, not proof.

## Phase 3: parser benchmark corpus coverage

Goal: make parser behavior over the realistic fixtures visible in benchmark reports.

Work:

- Add parser-corpus benchmark cases over a dedicated realistic fixture subset.
- Require the current parser to preserve expected labels/provenance.
- Treat LaTeXML/Pandoc as optional measured backends; unavailable/failing external parser results must remain `inconclusive`, not hard crashes.

Tests:

- Parser corpus benchmark passes for the current parser.
- Benchmark results include missing expected labels if any parser loses labels.
- Benchmark gate summary includes the new category/focus.

## Phase 4: workflow benchmark expansion

Goal: connect the corpus fixtures to agent-facing audit workflows.

Work:

- Add AST operation benchmark cases for the new code fixtures.
- Add at least one false-confidence case where a realistic-looking implementation is missing a required operation.
- Keep expected abstentions explicit.

Tests:

- Full benchmark gate passes.
- New cases report operation evidence and missing-operation evidence.
- Expected benchmark totals and summaries are updated.

## Phase 5: verification, tidy, reset memo, commit

Work:

- Run targeted tests.
- Run full test suite.
- Run benchmark gate.
- Run `git diff --check`.
- Update reset memo with implemented changes, verification results, limitations, and next step.
- Commit relevant files, excluding `.serena/` and unrelated local files.

Verification commands:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

## Non-goals

- Do not add heavyweight runtime dependencies.
- Do not execute JAX/PyTorch/NumPyro code.
- Do not claim parser output is mathematical proof.
- Do not claim AST operation matches prove code/document semantic equivalence.
- Do not build a large private corpus in this public fixture slice.
