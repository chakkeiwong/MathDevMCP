# Seven-phase industrial closure execution plan

## Context

The latest typed/dimensional `MathObligation` slice added typed symbol candidates, dimension constraints, stochastic objects, backend route hints, CLI/MCP exposure, and benchmark coverage. The next user request asks for a plan and execution over the seven remaining industrial phases:

1. make typed IR the routing spine,
2. add shape/dimension reasoning,
3. harden symbolic/Sage/numeric diagnostics,
4. expand real department corpus strategy,
5. define parser adapter v2 policy,
6. move LeanDojo toward a true backend boundary,
7. productize agent workflows plus deployment/governance.

This pass should implement maintainable, benchmarked scaffolding across all seven phases. It must not claim full industrial completion.

## Safety invariant

No parser output, AST match, inferred type, dimension hint, route hint, symbolic result, Lean skeleton, LeanDojo failure, or generated review packet may become a verified mathematical claim unless a deterministic backend verifies it under explicit assumptions and the MathDevMCP contract accepts the evidence.

## Phase 0: plan, memo, and audit

Work:

- Update the reset memo before implementation.
- Write this detailed execution plan.
- Write a second-developer audit of the plan.

Tests:

- Documentation-only phase; later full verification covers repository consistency.

## Phase 1: typed IR routing spine

Goal: make proof-audit routing explicit through typed `MathObligation` diagnostics.

Work:

- Add a `routing.py` module that consumes typed diagnostics and emits structured route decisions.
- Route simple backend-ready obligations to symbolic checking candidates.
- Route matrix/logdet/trace/inverse obligations to optional Sage/numeric diagnostics when safe.
- Route missing assumptions or unsupported stochastic notation to human review.
- Preserve route reason, source label, missing constraints, and provenance.

Tests:

- Scalar algebra routes to symbolic candidate.
- State-space likelihood routes to human review plus Sage diagnostic candidate.
- HMC derivative/posterior notation routes to human review.

## Phase 2: shape/dimension reasoning

Goal: consolidate typed IR constraints and AST shape evidence into a small diagnostic layer.

Work:

- Add a `shape_diagnostics.py` module.
- Evaluate whether required typed constraints are explicitly satisfied, missing, or evidenced by AST guards.
- Keep all shape evidence diagnostic.

Tests:

- Explicit positive-definite/square context satisfies logdet/inverse requirements.
- Missing shape assumptions remain `needs_assumptions`.
- AST shape/covariance guards can be reported as supporting evidence without proof upgrade.

## Phase 3: symbolic/Sage/numeric diagnostics

Goal: harden symbolic routing with typed-diagnostic gates.

Work:

- Add a `numeric_diagnostics.py` module for safe diagnostic suggestions/results.
- For matrix-heavy typed obligations, suggest logdet/solve/finite-difference/numeric counterexample diagnostics rather than running unsafe encodings.
- Attach Sage availability metadata if available through existing doctor/capability style.

Tests:

- Matrix inverse/logdet obligations suggest logdet/solve diagnostics.
- Derivative obligations suggest finite-difference checks.
- Unsupported notation returns `inconclusive`/diagnostic suggestions, not verification.

## Phase 4: department corpus roadmap

Goal: make private/sanitized corpus expansion machine-readable.

Work:

- Extend benchmark manifest or add a corpus roadmap module with categories, privacy policy, required false-confidence seeds, and expected abstentions.
- Include Kalman/state-space, HMC/NUTS, particle filters, DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objectives, Bayesian posterior/ELBO, and computational-physics algorithms.

Tests:

- Corpus roadmap contains privacy classification and required seeded-failure policy.
- Existing public fixtures map into the roadmap categories.

## Phase 5: parser adapter v2 policy

Goal: define evidence-based parser routing.

Work:

- Add parser policy code that consumes parser benchmark reports.
- Prefer current parser for line provenance when it preserves labels.
- Mark LaTeXML/Pandoc as measured optional backends until realistic corpus performance is sufficient.
- Report parser loss of labels/provenance as blocking for proof-audit routing.

Tests:

- Current parser preserving labels is selected for proof-audit routing.
- Missing labels or lost provenance produces `inconclusive`/blocked parser policy.
- External parser failures remain measured, not fatal.

## Phase 6: LeanDojo backend boundary

Goal: clarify and test the boundary between current LeanDojo readiness and true `Dojo(entry)` interaction.

Work:

- Add a conservative LeanDojo backend policy/helper that reports required traced-repo artifacts, toolchain compatibility, and final Lean direct-check requirement.
- Do not pretend to run a real Dojo loop unless a traced repo target exists.

Tests:

- Policy reports import-smoke readiness separately from real Dojo readiness.
- Missing traced repo target returns `inconclusive`.
- Direct Lean final-check invariant is present in the contract.

## Phase 7: agent workflow and deployment packaging

Goal: turn the above into compact agent-facing review output and deployment policy.

Work:

- Add an industrial review packet that summarizes typed routing, shape diagnostics, numeric diagnostics, parser policy, LeanDojo readiness, and deployment cautions.
- Extend deployment policy with pinned optional-worker recommendations and timeout/sandbox requirements.
- Add CLI/MCP exposure only if it is small and tested.

Tests:

- Review packet includes high-priority actions and does not mark unsupported obligations verified.
- Deployment policy includes isolated optional workers for LeanDojo/Sage/LaTeXML/Pandoc.
- Benchmark gate includes a representative industrial closure case.

## Final verification

Run:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
git diff --check
```

## Non-goals

- Do not claim full industrial completion.
- Do not implement full dependent typing.
- Do not run untrusted numeric encodings.
- Do not require external parsers/provers for the base package.
- Do not perform a real LeanDojo `Dojo(entry)` loop unless a traced repository target exists.
