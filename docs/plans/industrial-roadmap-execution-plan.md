# Industrial roadmap execution plan

## Context

MathDevMCP is being refocused from a bespoke parser/prover implementation into an industrial coding-agent tool for large mathematical finance and economics documents and code. The target users are Claude Code, Codex, and similar agents working on mathematically dense repositories. The goal is not to prove everything automatically; it is to make agent claims auditable, route suitable obligations to mature tools, detect code/document mismatches, surface missing assumptions, and abstain safely when evidence is insufficient.

This plan expands the 10-point remaining-work roadmap into an executable sequence. Each phase follows:

```text
plan → execute → test → audit → tidy → reset memo update
```

## Phase 1: real LeanDojo proof-loop validation

Goal: separate Lean's real usefulness from our previous direct-file checker by validating an actual interactive proof loop.

Work:

- Create a minimal local Lean project or compatible traced target.
- Implement `leandojo_backend.py` with a real `Dojo(entry)` path when possible.
- Apply one tactic to prove a tiny theorem.
- Add a false-theorem/failure case.
- Reconstruct a proof script and direct-check it with `lean_check.py`.
- If local LeanDojo/toolchain compatibility blocks real Dojo interaction, return a structured `inconclusive` report with exact blocker details.

Tests:

- LeanDojo availability check.
- Tiny proof reaches `ProofFinished` or structured `inconclusive`.
- False theorem does not verify.
- Direct Lean final check is required for any `verified` result.
- Timeout/failure is not upgraded to proof.

Exit criteria:

- A truthful result contract distinguishes `proved`, `failed`, and `inconclusive`.
- Reset memo records whether LeanDojo is usable in this environment.

## Phase 2: parser backend hardening

Goal: make parser selection evidence-based.

Work:

- Improve LaTeXML adapter extraction so generated XML IDs are not counted as user labels.
- Improve environment classification for LaTeXML and Pandoc.
- Add line/source provenance scoring.
- Add macro/align/theorem fixture cases.
- Add comparison outputs suitable for agents.

Tests:

- Current parser, LaTeXML, and Pandoc preserve expected labels on fixtures.
- Generated IDs are not counted as labels.
- Align row detection is measured.
- Backend failures return `inconclusive`.

Exit criteria:

- Parser benchmark can recommend a backend per document/task.

## Phase 3: MathObligation IR

Goal: introduce a small durable intermediate representation between parsers and backends.

Work:

- Add `math_ir.py` with dataclasses/dicts for `MathBlock`, `MathObligation`, `SymbolRecord`, `AssumptionRecord`.
- Include provenance, raw text, parser backend, symbol list, obligation kind, unresolved constructs, and backend suitability.
- Convert proof-audit candidates into this IR.

Tests:

- IR preserves provenance.
- Unsupported constructs are explicit.
- Existing proof-audit cases can be represented.
- Validators reject malformed IR.

Exit criteria:

- Downstream proof audit can route on IR rather than ad hoc strings.

## Phase 4: finance/economics symbol and assumption extraction

Goal: surface the assumptions agents usually miss.

Work:

- Add lightweight extraction for notation tables and nearby assumption prose.
- Detect common finance/econ objects: state vector, shock vector, covariance, transition matrix, SDF, Euler equation, value/policy function, likelihood.
- Track domain hints: scalar/vector/matrix, positive, invertible, SPD, time index.
- Report missing assumptions for obligations.

Tests:

- Fixtures with notation table map symbols to roles.
- Missing invertibility/positivity is surfaced.
- No missing assumption is silently invented.

Exit criteria:

- Proof/code audit reports include missing-assumption diagnostics.

## Phase 5: symbolic/Sage adapter hardening

Goal: route algebraic and numeric checks to mature symbolic tools conservatively.

Work:

- Add `symbolic_backend.py` wrapping SymPy and Sage availability.
- Parse/check simple algebra, numeric mismatches, and selected matrix expressions.
- Add sanity/round-trip checks before trusting parsed expressions.
- Add Sage version/reporting through doctor if not already sufficient.

Tests:

- Simple equality verified.
- Numeric false identity refuted.
- Unsafe parser output abstains.
- Sage unavailable/timeout is inconclusive.

Exit criteria:

- Proof audit can use symbolic route with transparent evidence.

## Phase 6: Lean/Mathlib formalization path

Goal: move from bare Lean examples toward useful Mathlib-backed proof families.

Work:

- Add optional Lake/Mathlib project detection.
- Add theorem templates for simple real algebra and inequalities when Mathlib is available.
- Add tactic ladder metadata: `simp`, `ring`, `omega`, `linarith`, `nlinarith`.
- Keep direct Lean final check mandatory.

Tests:

- Bare Lean tests pass without Mathlib.
- Mathlib tests skip or return inconclusive when project unavailable.
- No `sorry` certified.

Exit criteria:

- MathDevMCP can distinguish bare Lean capability from Mathlib capability.

## Phase 7: structure-aware code/document consistency

Goal: go beyond term overlap for algorithms.

Work:

- Add operation extraction for code: solve/inverse, logdet, Cholesky, quadratic form, gradient/Hessian, expectation/integration markers.
- Add document equation operation extraction from IR.
- Add mismatch diagnostics: missing logdet, sign mismatch hint, covariance vs precision, inverse/solve mismatch, time-index mismatch.

Tests:

- Seeded Kalman/HMC examples detect missing operations.
- Correct fixtures pass.
- Audit-only extras remain non-blocking.

Exit criteria:

- Agents get actionable code/doc mismatch reports.

## Phase 8: agent workflows for Claude Code and Codex

Goal: package capabilities as useful workflows rather than raw primitives.

Work:

- Add workflows: `audit_model_spec`, `audit_likelihood_implementation`, `audit_kalman_filter`, `audit_hmc_sampler`, `extract_assumptions`, `generate_acceptance_tests_from_equations`.
- Keep outputs concise with links/provenance and detailed evidence payloads.
- Expose selected workflows through MCP and CLI.

Tests:

- Each workflow has fixture coverage and structured error handling.
- MCP facade/server tests cover key tools.

Exit criteria:

- Coding agents can call high-level tools for common department tasks.

## Phase 9: department benchmark corpus

Goal: prove the tool helps on realistic finance/economics work.

Work:

- Add curated snippets for Kalman, HMC, DSGE/state-space, asset pricing Euler equations, macro-finance likelihood/value functions.
- Add seeded false claims and code bugs.
- Track retrieval, proof routing, abstention, and mismatch metrics.

Tests:

- Benchmark gate remains all-pass under expected-abstention policy.
- False claims never pass.
- Reports remain stable and CI-friendly.

Exit criteria:

- Benchmark corpus reflects real departmental use.

## Phase 10: packaging, deployment, and maintenance

Goal: make the tool usable by a department without brittle setup.

Work:

- Add optional dependency groups.
- Document system tools and external environments.
- Add CI/smoke test strategy.
- Add troubleshooting docs for LeanDojo/pydantic conflicts.
- Keep base import free of heavy dependencies.

Tests:

- Base package imports without optional tools.
- Doctor reports missing optional tools cleanly.
- Full suite and benchmark gate pass.

Exit criteria:

- The package can be installed, diagnosed, and used by coding agents without manual debugging.

## Cross-phase audit checklist

For every phase verify:

- no backend failure becomes `verified`,
- no LLM-only claim becomes proof,
- all verified results have deterministic evidence,
- missing assumptions are explicit,
- provenance is preserved,
- tests cover happy path and false-confidence path,
- reset memo records exact commands and outcomes.
