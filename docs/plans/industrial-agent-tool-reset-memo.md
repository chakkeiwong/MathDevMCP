# Reset memo: industrial agent-tool direction

## Why this memo exists

The project direction changed after evaluating the early proof-audit and Lean scaffolding work. The original instinct was to add more custom MathDevMCP parsing, proof decomposition, Lean export, Lean checking, and domain formalization code. After discussion, that is too much bespoke infrastructure for a one-person-maintained departmental tool.

The new direction is to build MathDevMCP as a thin industrial orchestration layer around mature open-source tools, while preserving the current strengths: provenance, conservative contracts, benchmark gates, and MCP/CLI surfaces for coding agents.

## Current environment observations

The following tools are now available at smoke-test level in the active environment:

```text
LaTeXML: /usr/bin/latexml, version 0.8.6
Pandoc: /usr/bin/pandoc, version 2.9.2.1
Lean: /home/chakwong/.elan/bin/lean, version 4.30.0-rc2
LeanDojo: Python package lean_dojo, version 4.20.0
```

Smoke tests completed:

- LaTeXML converted a tiny LaTeX document to XML and preserved label `eq:one`.
- Pandoc converted a tiny LaTeX snippet to JSON and preserved label `eq:one`.
- Lean compiled a tiny `Nat.add_comm` theorem.
- LeanDojo imported successfully and exposed `LeanGitRepo`, `Theorem`, and `Dojo`.
- MathDevMCP Lean-related tests passed:

```text
12 passed
```

Important caveat: LeanDojo has only been import/API smoke-tested. A real Dojo theorem interaction loop has not yet been validated.

## Decision

Use mature external systems wherever possible:

- LaTeXML as the primary candidate for mathematical LaTeX structure extraction,
- Pandoc as a secondary parser/baseline/fallback,
- SymPy/SageMath for symbolic and numeric obligations,
- Lean direct invocation as the final certificate checker,
- LeanDojo as the preferred candidate for interactive Lean proof search.

MathDevMCP should own:

- backend orchestration,
- provenance,
- result contracts,
- abstention policy,
- benchmark gates,
- coding-agent MCP/CLI workflows.

MathDevMCP should avoid owning:

- a full LaTeX parser,
- macro expansion infrastructure,
- full LaTeX math-to-Lean formalization,
- custom Lean tactic interaction,
- large domain proof libraries.

## Why this is the right direction

The department needs an industrial coding-agent tool, not a research project in parser/prover implementation. A one-person-maintained package must minimize custom code and failure modes. Thin adapters around battle-tested tools are more maintainable than expanding bespoke parsing and formalization logic.

The key product value is not that MathDevMCP proves everything itself. The key value is that it makes agent claims auditable:

```text
source document → extracted obligation → backend route → evidence or abstention → reproducible artifact
```

## Current code state to remember

Recent scaffolding exists and is useful, but should be treated as a prototype/baseline rather than the final architecture:

- `proof_audit.py`: decomposes simple labeled equation/align blocks into obligations.
- `lean_export.py`: creates Lean theorem skeletons without certification.
- `lean_check.py`: checks explicit Lean source and rejects placeholders.
- `domain_formalization.py`: toy narrow domain formalization for Nat-valued scalar identities.

These modules demonstrate desired contracts and guardrails, but future work should not keep expanding custom parsing/formalization logic when an external backend can do the job.

## New plan file

The industrial plan is now recorded in:

- [industrial-agent-tool-plan.md](industrial-agent-tool-plan.md)

That plan supersedes the earlier ad hoc Lean/domain-formalization direction. The immediate next implementation sequence is:

1. Add capability diagnostics.
2. Add parser adapter benchmark for current parser, LaTeXML, and Pandoc.
3. Add a LeanDojo spike that proves one tiny theorem and fails one false theorem.
4. Decide whether LeanDojo is stable enough to become an optional backend.
5. Refactor proof audit to use parser/backend adapters rather than growing custom parsing logic.
6. Add department-real snippets only after adapter behavior is measurable.

## Audit policy going forward

Every new backend integration should include:

- availability detection,
- version reporting,
- tiny smoke test,
- structured success/failure contract,
- false-confidence regression test,
- provenance preservation test,
- expected-abstention behavior,
- reset-memo update after meaningful changes.

Do not treat backend output as verified unless the backend itself provides deterministic evidence and the result passes MathDevMCP contract checks.

## Current AST/Kalman-recursion request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is AST-level Python operation extraction plus a Kalman filter recursion audit. This should improve practical code/document review beyond operation-presence string matching while remaining conservative.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- implement maintainable AST operation graph and Kalman recursion workflow slices,
- test and benchmark-gate the work,
- commit relevant files while excluding `.serena/`.

Planning artifacts for this pass:

- [ast-kalman-recursion-execution-plan.md](ast-kalman-recursion-execution-plan.md),
- [ast-kalman-recursion-plan-audit.md](ast-kalman-recursion-plan-audit.md).

## AST/Kalman-recursion checkpoint outcome

This pass added an AST-level Python operation graph and a conservative Kalman recursion audit workflow. The slice improves code/document review beyond string operation matching, while still treating matches as structural review evidence rather than mathematical proof.

### Changes implemented

Added planning/audit docs:

- `docs/plans/ast-kalman-recursion-execution-plan.md`,
- `docs/plans/ast-kalman-recursion-plan-audit.md`.

Added `src/mathdevmcp/ast_operation_graph.py` with:

- Python AST parsing for assignments, calls, returns, matrix multiplications, loops, assertions, comparisons, and subscripts,
- operation classification for logdet, inverse/solve, Cholesky, quadratic forms, prediction updates, innovation updates, innovation covariance, Kalman gain, state update, and covariance update,
- line/column evidence for extracted operations,
- structured `inconclusive` results for Python syntax errors.

Extended `src/mathdevmcp/kalman_workflows.py` with:

- `audit_kalman_recursion(...)`,
- required Kalman recursion operation checks,
- AST-backed shape/covariance guard diagnostics,
- recommended actions for missing recursion operations and missing guards.

Added agent/benchmark surfaces:

- CLI command: `python -m mathdevmcp.cli audit-kalman-recursion CODE.py`,
- MCP facade/FastMCP tool: `audit_kalman_recursion`,
- benchmark category: `kalman_recursion`,
- fixtures `doc_kalman_recursion_good.py` and `doc_kalman_recursion_bad.py`.

Added tests covering:

- AST operation graph extraction,
- syntax-error abstention,
- Kalman recursion missing-operation detection,
- explicit shape/covariance guard diagnostics,
- CLI/MCP wrappers,
- benchmark gate accounting for the new category.

### Verification completed

Targeted AST/Kalman/MCP/benchmark tests passed:

```text
41 passed
```

Lean-backed tests initially failed under sandboxed network restrictions because `elan` attempted to resolve `release.lean-lang.org`. Re-running the Lean-dependent tests with approved network access passed:

```text
17 passed
```

Full suite passed with the same Lean-capable environment:

```text
154 passed
```

Benchmark gate passed:

```text
passed=true, total=19, passed_count=19, failed_count=0, expected_abstentions=8, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not a full Kalman filter verifier. The AST graph provides structured operation evidence and source locations; it does not prove semantic equivalence, update ordering, numerical stability, or stochastic assumptions. Shape and covariance guards are detected only when explicitly present in code. Missing guards keep otherwise plausible recursion code in `unverified` status. Missing required recursion operations, such as the covariance update, produce `mismatch`.

The next industrial step should add realistic sanitized department snippets for state-space implementations across NumPy/JAX/PyTorch styles and broaden AST recognition for common linear algebra wrappers without weakening the abstention policy.

## Current department-corpus/parser-AST request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is a realistic sanitized department-style corpus plus parser/AST benchmark expansion. This should test the existing parser, AST operation graph, and Kalman/likelihood scaffolding against more realistic mathematical finance/economics materials without claiming full industrial completion.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- add sanitized department-style LaTeX/Python fixtures,
- harden AST recognition for common scientific-computing idioms,
- add parser/AST benchmark coverage and false-confidence cases,
- test and benchmark-gate the work,
- commit relevant files while excluding `.serena/` and unrelated local files.

Planning artifacts for this pass:

- [department-corpus-parser-ast-execution-plan.md](department-corpus-parser-ast-execution-plan.md),
- [department-corpus-parser-ast-plan-audit.md](department-corpus-parser-ast-plan-audit.md).

## Department corpus/parser-AST checkpoint outcome

This pass added a small sanitized department-style corpus and expanded parser/AST benchmark coverage. The slice tests the existing parser, AST graph, and benchmark gate against more realistic mathematical finance/economics materials without adding heavyweight runtime dependencies or claiming semantic proof.

### Changes implemented

Added planning/audit docs:

- `docs/plans/department-corpus-parser-ast-execution-plan.md`,
- `docs/plans/department-corpus-parser-ast-plan-audit.md`.

Added sanitized LaTeX fixtures:

- `benchmarks/fixtures/doc_department_state_space.tex`, covering state-space assumptions, Kalman recursion, and likelihood labels,
- `benchmarks/fixtures/doc_department_bayesian_hmc.tex`, covering posterior, leapfrog, and Hamiltonian labels.

Added sanitized Python fixtures:

- `benchmarks/fixtures/doc_department_state_space_jax.py`, a JAX-style state-space scan with shape/covariance guards, slogdet, solve, and Kalman updates,
- `benchmarks/fixtures/doc_department_state_space_missing_solve.py`, a seeded false-confidence case missing the solve/inverse operation,
- `benchmarks/fixtures/doc_department_hmc_jax.py`, an HMC/leapfrog-style kernel with gradient, log probability, and Hamiltonian energy structure,
- `benchmarks/fixtures/doc_department_particle_filter.py`, a particle-filter-style logsumexp normalization slice.

Hardened `src/mathdevmcp/ast_operation_graph.py` so AST structural evidence now recognizes:

- JAX/scientific-computing calls such as `grad`, `scan`, `vmap`, `slogdet`, and `logsumexp`,
- posterior/log-likelihood calls,
- leapfrog/Hamiltonian update patterns,
- particle normalization patterns,
- vectorized-loop evidence.

Extended `src/mathdevmcp/benchmarks.py` with:

- `parser_corpus` benchmark coverage for the realistic LaTeX fixture labels,
- `ast_corpus` benchmark coverage for realistic state-space, HMC, particle-filter, and missing-solve cases.

Added tests covering:

- department fixture label and section-path preservation,
- current parser preservation of department corpus labels,
- AST recognition over JAX-style state-space, HMC, and particle-filter fixtures,
- benchmark gate accounting for parser/AST corpus categories,
- false-confidence control for the missing-solve state-space fixture.

### Verification completed

Targeted parser/AST/corpus tests passed:

```text
35 passed
```

Full suite passed:

```text
161 passed
```

Benchmark gate passed:

```text
passed=true, total=24, passed_count=24, failed_count=0, expected_abstentions=8, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is still a corpus and structural-audit milestone, not full industrial completion. The new AST recognizers provide line-level operation evidence for realistic code idioms, but they do not execute JAX/PyTorch/NumPyro code, prove semantic equivalence, or verify stochastic assumptions. The current parser is now gated on the new realistic labels; LaTeXML/Pandoc remain measured optional backends rather than required production parsers. The seeded missing-solve case protects false-confidence behavior for realistic-looking state-space code.

The next industrial step should broaden private/sanitized corpus collection and add stronger typed/dimensional `MathObligation` semantics for matrix shapes, random variables, stochastic processes, and likelihood/posterior objects.

## Current typed/dimensional MathObligation request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is typed/dimensional `MathObligation` semantics for matrix shapes, random variables, stochastic processes, likelihood/posterior objects, derivatives, and backend route diagnostics.

This pass should:

- plan the typed/dimensional IR slice,
- update this reset memo before and after work,
- write a second-developer audit,
- extend `MathObligation` conservatively without replacing existing contracts,
- expose typed obligation diagnostics through CLI/MCP,
- add benchmark-gate coverage,
- test, tidy, and commit relevant files while excluding `.serena/` and unrelated local files.

Planning artifacts for this pass:

- [typed-dimensional-ir-execution-plan.md](typed-dimensional-ir-execution-plan.md),
- [typed-dimensional-ir-plan-audit.md](typed-dimensional-ir-plan-audit.md).

## Typed/dimensional MathObligation checkpoint outcome

This pass added conservative typed/dimensional `MathObligation` metadata and exposed typed obligation diagnostics to coding agents. The slice improves routing and review for matrix, stochastic, likelihood/posterior, derivative, and HMC-style obligations without treating inferred roles or shapes as proof assumptions.

### Changes implemented

Added planning/audit docs:

- `docs/plans/typed-dimensional-ir-execution-plan.md`,
- `docs/plans/typed-dimensional-ir-plan-audit.md`.

Extended `src/mathdevmcp/math_ir.py` with:

- typed symbol candidates for scalar, vector, matrix, covariance matrix, transition matrix, observation matrix, stochastic process, likelihood, posterior, gradient, and Hamiltonian roles,
- dimension constraints for inverse/invertibility, determinant/logdet square-matrix requirements, trace square-matrix requirements, derivative differentiability requirements, and conformable product requirements,
- stochastic object candidates for time-indexed symbols, expectations, and conditional/posterior expressions,
- backend route hints for symbolic, Sage/numeric diagnostic, Lean formalization, and human-review paths,
- `diagnostic_status` values that distinguish `ready_for_backend`, `typed_review`, and `needs_assumptions`,
- `diagnose_typed_obligation(...)` for compact typed diagnostics.

Added `src/mathdevmcp/typed_workflows.py` with:

- `typed_obligation_for_label(...)`, which audits a labeled equation and returns typed/dimensional diagnostics with provenance.

Exposed typed diagnostics through:

- CLI: `python -m mathdevmcp.cli typed-obligation-label LABEL --root ROOT`,
- MCP facade/FastMCP tool: `typed_obligation_label`.

Extended benchmark coverage with:

- `typed_ir_state_space_likelihood`, checking missing invertibility, square-matrix, and conformable-product diagnostics,
- `typed_ir_hmc_leapfrog`, checking missing differentiability diagnostics for HMC/posterior notation.

Added tests covering:

- backward-compatible `MathObligation` validation,
- typed symbol extraction for state-space likelihoods,
- explicit assumption context reducing missing constraints,
- HMC/posterior typed diagnostics,
- CLI/MCP/FastMCP wrappers,
- benchmark-gate accounting for the new `typed_ir` category.

### Verification completed

Focused typed-IR, benchmark, MCP, server, and CLI tests passed:

```text
51 passed
```

Full suite passed:

```text
168 passed
```

Benchmark gate passed:

```text
passed=true, total=26, passed_count=26, failed_count=0, expected_abstentions=10, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not dependent typing or formal matrix calculus. Typed roles, shape classes, stochastic objects, and backend route hints are diagnostic metadata. They remain `candidate_not_assumption` unless explicit context or a deterministic backend establishes more. The new diagnostics make missing assumptions visible to agents and benchmark gates, but they do not upgrade any mathematical claim to `verified`.

The next industrial step should connect typed IR more deeply into proof-audit routing and symbolic/Sage numeric diagnostics, so suitable obligations can be routed automatically while unsupported stochastic/matrix notation continues to abstain with actionable missing-assumption reports.

## Current seven-phase industrial closure request

The next request is to plan, audit, execute, test, tidy, commit, and update this memo for the seven-phase roadmap after typed/dimensional `MathObligation`:

1. make typed IR the proof-audit routing spine,
2. add shape/dimension reasoning,
3. harden symbolic/Sage/numeric diagnostics,
4. expand department corpus strategy,
5. define parser adapter v2 policy,
6. clarify the LeanDojo backend boundary,
7. package agent workflows plus deployment/governance.

This pass should implement conservative, maintainable scaffolding across all seven phases. It should not claim full industrial completion.

Planning artifacts for this pass:

- [seven-phase-industrial-closure-execution-plan.md](seven-phase-industrial-closure-execution-plan.md),
- [seven-phase-industrial-closure-plan-audit.md](seven-phase-industrial-closure-plan-audit.md).

## Seven-phase industrial closure checkpoint outcome

This pass implemented conservative scaffolding across the seven requested industrial phases. It does not claim full industrial completion; it makes typed routing, shape diagnostics, numeric diagnostic suggestions, corpus strategy, parser policy, LeanDojo readiness boundaries, deployment policy, and agent review packets measurable and contract-backed.

### Changes implemented

Added planning/audit docs:

- `docs/plans/seven-phase-industrial-closure-execution-plan.md`,
- `docs/plans/seven-phase-industrial-closure-plan-audit.md`.

Phase 1, typed IR routing spine:

- Added `src/mathdevmcp/routing.py`.
- Added `route_typed_diagnostic(...)` and `route_label_obligation(...)`.
- Routes backend-ready scalar obligations to symbolic candidates.
- Routes missing assumptions and unsupported stochastic/matrix notation to human review.
- Preserves missing constraints and typed diagnostics in the route decision.

Phase 2, shape/dimension reasoning:

- Added `src/mathdevmcp/shape_diagnostics.py`.
- Added `diagnose_shape_constraints(...)`.
- Reports missing typed constraints, explicitly satisfied constraints, and AST shape/covariance guard evidence as diagnostic support only.

Phase 3, symbolic/Sage/numeric diagnostics:

- Added `src/mathdevmcp/numeric_diagnostics.py`.
- Suggests logdet domain checks, linear solve residual checks, finite-difference gradient checks, and trace shape checks from typed unresolved constructs.
- Does not run unsafe numeric encodings or upgrade diagnostic suggestions to proof.

Phase 4, department corpus roadmap:

- Added `src/mathdevmcp/corpus_roadmap.py`.
- Records corpus categories, privacy policy, public fixture status, required false-confidence seeds, and expected abstention policy for Kalman/state-space, HMC/NUTS, particle filters, DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objectives, Bayesian ELBO/VI, and computational-physics algorithms.

Phase 5, parser adapter v2 policy:

- Added `src/mathdevmcp/parser_policy.py`.
- Selects current parser for proof-audit routing when expected labels and provenance are preserved.
- Records blocking findings for missing labels or unavailable provenance.
- Keeps external parser failures measured rather than fatal.

Phase 6, LeanDojo backend boundary:

- Added `src/mathdevmcp/leandojo_policy.py`.
- Separates import/API smoke readiness from true `Dojo(entry)` readiness.
- Requires pinned Lean/Lake toolchain, traced repository target, theorem entry, bounded tactic script, and direct Lean final check artifact.
- Allows policy-only checks without importing LeanDojo during benchmark-gate paths.

Phase 7, agent workflow and deployment packaging:

- Added `src/mathdevmcp/industrial_review.py`.
- Builds an industrial review packet combining typed obligation diagnostics, route decision, shape diagnostics, numeric suggestions, parser policy, LeanDojo policy, corpus roadmap, and deployment policy.
- Extended `src/mathdevmcp/deployment.py` with optional worker recommendations for parser, Sage, Lean, and LeanDojo workers plus sandboxing policy.
- Added benchmark category `industrial_review` for the state-space review packet.

Added tests covering:

- typed route decisions,
- shape diagnostic AST guard support,
- numeric diagnostic suggestions,
- corpus roadmap privacy and false-confidence policy,
- parser policy selection,
- LeanDojo backend boundary,
- industrial review packet actions,
- deployment worker isolation policy,
- benchmark-gate accounting for the new `industrial_review` category.

### Verification completed

Focused industrial closure and benchmark tests passed:

```text
35 passed
```

Full suite passed:

```text
178 passed
```

Benchmark gate passed:

```text
passed=true, total=27, passed_count=27, failed_count=0, expected_abstentions=11, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint makes the seven-phase roadmap executable and measurable, but it remains scaffolding. Route decisions are not proof, shape evidence is not dependent typing, numeric diagnostics are suggestions unless safely executed and checked, parser policy depends on measured corpus behavior, and LeanDojo remains inconclusive until a traced repository theorem target is available. The industrial review packet is an agent-facing prioritization layer, not a certificate.

The next highest-value implementation step is proof-audit v2: every extracted proof-audit obligation should carry typed diagnostics, route decisions, and backend evidence or abstention in the primary proof-audit report.

## Current industrial release-readiness request

The next request is to execute the industrial release-readiness plan:

- [industrial-release-readiness-execution-plan.md](industrial-release-readiness-execution-plan.md)

The goal is to turn the existing scaffold into a release-quality vertical path for colleagues:

```text
source label or code path
→ parser/provenance evidence
→ typed MathObligation diagnostics
→ route decision
→ shape/dimension diagnostics
→ backend evidence or explicit abstention
→ compact colleague-facing report
→ benchmark/release artifact
```

This pass should update the reset memo, audit the plan as a second developer, execute the phases with tests and audit notes, commit relevant files, and update this memo again upon completion.

The primary implementation target is proof-audit v2 as the release spine. The later release-readiness phases should attach conservative, measurable increments around that spine:

1. proof-audit v2 report with per-obligation typed diagnostics, route decisions, shape diagnostics, numeric suggestions, backend evidence, and actions,
2. CLI/MCP exposure for proof-audit v2,
3. parser evidence hardening on realistic sanitized fixtures,
4. safe executable numeric diagnostics for explicit encodings,
5. truthful optional LeanDojo backend boundary,
6. benchmark/release-gate expansion,
7. packaging/dependency isolation metadata,
8. colleague-facing operator documentation,
9. release-candidate audit.

Safety invariant for this pass: no parser output, AST match, inferred type, dimension hint, route hint, shape guard, numeric diagnostic, generated Lean skeleton, LeanDojo readiness result, benchmark pass, or review packet may become a verified mathematical claim unless a deterministic backend verifies the claim under explicit assumptions and MathDevMCP records reproducible evidence.

Planning/audit artifacts for this pass:

- [industrial-release-readiness-execution-plan.md](industrial-release-readiness-execution-plan.md),
- [industrial-release-readiness-plan-audit.md](industrial-release-readiness-plan-audit.md).

### Industrial release-readiness mid-pass checkpoint

Phases 1-7 have been implemented as conservative release-readiness increments rather than as a claim of full industrial completion.

Implemented so far:

- `src/mathdevmcp/proof_audit_v2.py`, an additive proof-audit v2 release spine that combines the existing proof audit with parser policy, typed `MathObligation` diagnostics, route decisions, shape diagnostics, numeric diagnostic suggestions, backend attempts, per-obligation actions, and high-priority report actions.
- CLI command `audit-derivation-v2-label`.
- MCP facade/FastMCP tool `audit_derivation_v2_label`.
- Parser benchmark hardening fields for expected-label recall, generated-like labels, provenance score, environment count, and align-like count.
- `src/mathdevmcp/numeric_runner.py`, a safe explicit-encoding numeric diagnostic runner for logdet domain checks, linear solve residual checks, and finite-difference gradient checks.
- `src/mathdevmcp/leandojo_backend.py`, a conservative LeanDojo attempt boundary that records environment/toolchain evidence and keeps real Dojo interaction inconclusive unless explicitly configured.
- Benchmark category `proof_audit_v2` with scalar verification, false-claim mismatch, and state-space abstention cases.
- Optional dependency metadata in `pyproject.toml`.
- Operator-guide coverage for installation modes and proof-audit v2.

Focused release-readiness tests passed:

```text
68 passed
```

Audit note: proof-audit v2 is intentionally additive. The old proof-audit command remains stable. Numeric execution is limited to explicit safe encodings; it does not execute code generated from LaTeX. LeanDojo remains a truthful boundary, not a default real proof-search backend.

## Industrial release-readiness checkpoint outcome

This pass executed the industrial release-readiness plan as a conservative checkpoint. It does not claim full industrial completion for arbitrary frontier mathematics. It creates a stronger internal release spine that colleagues and coding agents can use to see parser evidence, typed diagnostics, route decisions, shape/dimension issues, backend evidence, numeric suggestions, and abstention reasons in one primary report.

### Changes implemented

Added planning/audit docs:

- `docs/plans/industrial-release-readiness-execution-plan.md`,
- `docs/plans/industrial-release-readiness-plan-audit.md`.

Added proof-audit v2:

- `src/mathdevmcp/proof_audit_v2.py`,
- `audit_derivation_v2_for_label(...)`,
- per-obligation contract `proof_audit_v2_obligation`,
- top-level contract `proof_audit_v2_result`,
- per-obligation parser policy, typed diagnostics, route decision, shape diagnostics, numeric suggestions, backend attempts, status, reason, provenance, and actions,
- compact `summary_only` mode for agent-facing output.

Exposed proof-audit v2 through:

- CLI command `audit-derivation-v2-label`,
- MCP facade tool `audit_derivation_v2_label`,
- FastMCP server tool `audit_derivation_v2_label`.

Added release-readiness backend scaffolding:

- parser benchmark hardening fields for expected-label recall, generated-like labels, provenance score, environment count, and align-like count,
- `src/mathdevmcp/numeric_runner.py` with explicit safe-encoding checks for logdet domains, linear solve residuals, and finite-difference gradients,
- `src/mathdevmcp/leandojo_backend.py` with a conservative LeanDojo attempt boundary that stays `inconclusive` unless a real traced repo/theorem target is explicitly configured.

Updated release surfaces:

- benchmark category `proof_audit_v2`,
- benchmark total increased to 30 cases,
- expected abstentions increased to 12,
- optional dependency groups in `pyproject.toml` for `symbolic`, `mcp`, `leandojo`, and `all`,
- operator guide installation-mode and proof-audit v2 sections.

Added tests:

- proof-audit v2 scalar verification, false-claim mismatch, state-space abstention, compact summary, CLI, MCP facade, and FastMCP paths,
- safe numeric runner diagnostics,
- LeanDojo boundary behavior,
- parser hardening fields,
- optional dependency metadata,
- benchmark accounting for `proof_audit_v2`.

### Verification completed

Focused release-readiness tests passed:

```text
60 passed
```

Full suite passed:

```text
188 passed
```

Benchmark gate passed:

```text
passed=true, total=30, passed_count=30, failed_count=0, expected_abstentions=12, policy=all_benchmarks_must_pass
```

Doctor command passed and reported:

- LaTeXML available,
- Pandoc available,
- Sage available,
- LeanDojo import available,
- SymPy available,
- Lean executable present, but the version command returned `error: error during download` in this environment,
- existing `magic-pdf` / `pydantic` conflict warning remains visible.

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

Proof-audit v2 is now the preferred release spine, but it remains additive. The existing proof-audit command is preserved. Verified status is still reserved for deterministic bounded backend evidence. Shape evidence, parser policy, route decisions, numeric suggestions, and LeanDojo readiness do not certify mathematical claims.

The safe numeric runner only accepts explicit arrays or callables supplied by code/tests. It intentionally does not parse arbitrary LaTeX into executable code. The LeanDojo backend boundary records readiness and final-check evidence, but real `Dojo(entry)` interaction still requires a pinned traced repository target and remains future work.

The next highest-value release step is to run proof-audit v2 on larger sanitized/private department corpora and expand parser/AST/shape coverage for the recurring frontier domains before declaring a colleague-wide release.

## Kalman industrialization checkpoint outcome

This pass added a Kalman likelihood vertical workflow as the next realistic department-facing milestone.

### Changes implemented

Added planning/audit docs:

- `docs/plans/kalman-industrialization-execution-plan.md`,
- `docs/plans/kalman-industrialization-plan-audit.md`.

Updated `src/mathdevmcp/notation.py` so symbol hints distinguish common Kalman/state-space candidates:

- `S_t`: covariance/matrix candidate,
- `v_t`: residual/vector candidate,
- `F_t`/`A_t`/`T_t`: transition-matrix candidate,
- `H_t`/`Z_t`: observation-matrix candidate.

Added `src/mathdevmcp/kalman_workflows.py` with:

- `audit_kalman_likelihood(...)`, combining likelihood audit, Kalman operation requirements, symbol hints, and diagnostic suggestions,
- `build_kalman_review_packet(...)`, producing an agent-facing Kalman review packet with severity-ranked actions and diagnostics.

Added `tests/test_kalman_workflows.py`, covering:

- candidate-not-assumption status for symbol hints,
- missing logdet/solve detection,
- unverified status when operations are present but assumptions/proof remain incomplete,
- review packet action and diagnostic suggestion propagation.

### Verification completed

Targeted Kalman workflow tests passed:

```text
4 passed
```

Full suite passed:

```text
144 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not a full Kalman filter verifier. It is a maintainable operation/assumption/provenance review workflow. It can detect missing likelihood operations such as logdet and inverse/solve, preserve Kalman-style symbol hints as non-proof candidate metadata, surface missing assumptions, and produce review-packet actions for coding agents.

The next industrial step should be AST-level code operation graphs and shape/dimension diagnostics for a realistic state-space implementation.

## Current Kalman-industrialization request

The next request is to repeat the industrial cycle for the latest remaining-gap assessment. The practical next milestone is a realistic Kalman likelihood/filter audit workflow because it exercises parsing, notation, assumptions, matrix operations, likelihood code, missing logdet/solve/shape bugs, diagnostic suggestions, and review packets.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- implement maintainable slices rather than claiming full industrial completion,
- run tests and benchmark gate,
- commit relevant files while excluding `.serena/`.

## Frontier industrialization checkpoint outcome

The latest pass added an agent-facing frontier-industrialization layer on top of the prior scaffolding.

### Changes implemented

Added planning/audit docs:

- `docs/plans/frontier-industrialization-execution-plan.md`,
- `docs/plans/frontier-industrialization-plan-audit.md`.

Added new modules:

- `src/mathdevmcp/review_packet.py`: builds compact likelihood review packets from nested audit evidence,
- `src/mathdevmcp/notation.py`: extracts explicit notation records and candidate symbol hints,
- `src/mathdevmcp/diagnostic_tests.py`: suggests diagnostic tests from audit findings,
- `src/mathdevmcp/benchmark_manifest.py`: records benchmark corpus categories and private-corpus policy,
- `src/mathdevmcp/deployment.py`: records optional backend/dependency/deployment policy.

Added `tests/test_frontier_industrialization.py`, covering:

- high-severity review-packet actions for missing likelihood operations,
- explicit notation extraction and candidate symbol hints,
- diagnostic test suggestions for missing logdet/solve and derivative obligations,
- private benchmark corpus manifest policy,
- LeanDojo/backend isolation deployment policy.

### Verification completed

Targeted frontier-industrialization tests passed:

```text
5 passed
```

Full suite passed:

```text
140 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This pass improves usability and governance rather than claiming full industrial completeness. The new review packet is the most important product-facing addition: it converts nested likelihood audit evidence into severity-ranked actions that coding agents can act on. Notation and symbol hints remain explicitly diagnostic and are not proof assumptions. Diagnostic test suggestions are plans, not generated files or long experiments. Benchmark and deployment metadata now make private-corpus and optional-backend policies machine-readable.

### Remaining gaps

The largest remaining gaps are still:

- true LeanDojo `Dojo(entry)` interaction,
- parser benchmarking on real/sanitized department documents,
- typed/dimensional MathObligation semantics,
- Sage-backed matrix/numeric checks,
- AST-level code operation graphs,
- real private benchmark corpora,
- CI/deployment packaging for optional backend worker environments.

## Current frontier-industrialization request

The next request is to plan, audit, execute, test, tidy, update this memo, and commit another industrialization pass toward a department-scale tool for mathematical finance/economics developers working across computational econometrics, computational statistics, ML/LLMs, large-scale Bayesian learning, computational physics, and applied mathematics.

The highest-value next pass should not claim full industrial completion. It should add maintainable scaffolding for:

- parser/proof/code review packets,
- typed/dimensional MathObligation improvements,
- notation/assumption extraction,
- generated diagnostic test suggestions,
- benchmark corpus organization,
- deployment/dependency documentation in machine-readable form.

The work should keep the same safety invariant: no parser guess, inferred assumption, LLM claim, generated skeleton, backend timeout, or external-tool failure may become a verified mathematical claim.

## Remaining industrial gaps checkpoint outcome

The latest request asked for a reset-memo update, an execution plan for the remaining industrial gaps, an independent audit of that plan, execution with the established cycle, verification, commit, and final reset-memo update.

### Changes implemented in this checkpoint

Added planning/audit docs:

- `docs/plans/remaining-industrial-gaps-execution-plan.md`,
- `docs/plans/remaining-industrial-gaps-plan-audit.md`.

The implemented code from the preceding industrial slices now covers the approved high-leverage scaffolding:

- capability diagnostics,
- parser backend benchmarking and hardened expected-label scoring,
- LeanDojo readiness boundary,
- minimal MathObligation IR,
- finance/econ missing-assumption diagnostics,
- symbolic backend wrapper,
- operation-level code/document consistency,
- likelihood implementation vertical workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint should be understood as an industrial scaffolding milestone, not a claim of full industrial completion. The remaining high-value gaps are:

- true `Dojo(entry)` interaction over a traced Lean theorem target,
- real/sanitized department parser benchmark corpus,
- richer MathObligation semantics for dimensions, random variables, stochastic processes, and matrix calculus,
- stronger Sage/SymPy parsing and numeric counterexample generation,
- Mathlib-backed theorem families,
- AST-level code/document consistency,
- deployment isolation for LeanDojo and heavy optional tools.

The most important safety invariant remains intact: no backend failure, inferred assumption, parser guess, generated Lean skeleton, or LLM-only claim is treated as proof.

## Current execution request

The next request is to turn the remaining industrial gaps into an execution plan, audit that plan as a second developer, execute implementable phases with the established cycle, commit the modified files, and update this reset memo again upon completion.

The key remaining industrial gaps are:

- true LeanDojo theorem interaction,
- parser hardening on real or realistic documents,
- MathObligation IR expansion without overbuilding,
- finance/economics assumption extraction,
- symbolic/Sage backend hardening,
- Lean/Mathlib formalization path,
- structure-aware code/document consistency,
- agent workflows for Claude Code and Codex,
- department benchmark corpus,
- packaging/deployment/security/docs.

The implementation should keep the project maintainable by preferring thin adapters, conservative contracts, and one high-value vertical workflow over broad unsupported feature expansion.

## Industrial roadmap implementation outcome

A broad first pass over the 10-point industrial roadmap was implemented after writing and auditing [industrial-roadmap-execution-plan.md](industrial-roadmap-execution-plan.md) and [industrial-roadmap-plan-audit.md](industrial-roadmap-plan-audit.md).

### Changes implemented

Added planning/audit docs:

- `docs/plans/industrial-roadmap-execution-plan.md`,
- `docs/plans/industrial-roadmap-plan-audit.md`.

Added or hardened industrial modules:

- `src/mathdevmcp/leandojo_spike.py`: conservative LeanDojo readiness and direct-checked proof-artifact spike,
- `src/mathdevmcp/parser_benchmark.py`: hardened scoring against expected fixture labels rather than raw generated IDs,
- `src/mathdevmcp/math_ir.py`: minimal `MathObligation` IR with provenance, symbols, unresolved constructs, and backend suitability,
- `src/mathdevmcp/assumptions.py`: lightweight finance/econ missing-assumption diagnostics,
- `src/mathdevmcp/symbolic_backend.py`: conservative symbolic backend wrapper around the existing SymPy proof-obligation path,
- `src/mathdevmcp/operation_consistency.py`: structure-aware operation extraction for code/document consistency,
- `src/mathdevmcp/agent_workflows.py`: first vertical workflow, `audit_likelihood_implementation(...)`.

Added tests for:

- MathObligation IR,
- assumption diagnostics,
- symbolic backend checks,
- operation-level consistency,
- likelihood implementation audit workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This pass intentionally implements thin, maintainable slices rather than full industrial completion. It covers every roadmap area at least as a scaffold or first vertical slice:

- LeanDojo remains conservative: no real `Dojo(entry)` interaction yet.
- Parser hardening now scores expected labels rather than arbitrary generated IDs.
- Math IR is deliberately minimal and audit-oriented, not a full symbolic algebra system.
- Assumption extraction reports explicit vs inferred-missing assumptions but does not use inferred assumptions as proof premises.
- Symbolic backend keeps the strict safe grammar boundary.
- Operation consistency starts structure-aware code/document comparison with operation presence, not full semantic equivalence.
- The first high-level agent workflow focuses on likelihood implementation audit rather than adding many untested workflow names.

### Remaining work

The next highest-value work is still a true LeanDojo interaction loop:

- create or trace a tiny Lean repository theorem target,
- invoke `Dojo(entry)`,
- apply a tactic and observe `ProofFinished`,
- reconstruct and direct-check the proof artifact,
- record LeanDojo/Lean/Lake/toolchain compatibility.

After that, the parser benchmark should be run on real or sanitized department snippets, not just fixtures.

## LeanDojo spike outcome

The third industrial-tool slice added a conservative LeanDojo spike helper. It validates that LeanDojo is available and records the boundary between import/API readiness and a real Dojo theorem interaction.

### Changes implemented

Added `src/mathdevmcp/leandojo_spike.py` with:

- `leandojo_import_smoke()`, which imports LeanDojo and checks for `LeanGitRepo`, `Theorem`, and `Dojo`,
- `leandojo_tiny_proof_spike()`, which records a tiny `Nat.add_comm` tactic script and direct-checks the resulting Lean proof artifact using the existing Lean checker.

Added `tests/test_leandojo_spike.py`.

### Verification completed

Targeted LeanDojo spike tests passed:

```text
2 passed
```

Full suite passed:

```text
121 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

### Audit notes

This is not yet a true LeanDojo proving loop. It proves that LeanDojo imports and that MathDevMCP can attach a LeanDojo-oriented tactic trace to a proof artifact that direct Lean verifies. The missing industrial step is a real `Dojo(entry)` interaction over a traced Lean repository theorem target. That should be implemented only after creating a tiny local Lean project or using a pinned LeanGitRepo compatible with LeanDojo 4.20.0.

This conservative result is intentional: it avoids overstating LeanDojo readiness while preserving the correct final-check invariant.

### Next slice

The next slice should create a minimal traced Lean target for real Dojo interaction:

- create or locate a tiny Lean repository with a theorem statement,
- invoke `Dojo(entry)` on that theorem,
- apply one tactic,
- confirm `ProofFinished`,
- reconstruct the proof script,
- direct-check the final Lean file,
- record version/toolchain compatibility constraints.

## Parser adapter benchmark outcome

The second industrial-tool slice added a parser comparison harness so MathDevMCP can evaluate external LaTeX parsers before depending on them.

### Changes implemented

Added `src/mathdevmcp/parser_benchmark.py` with:

- `run_parser_backend(root, backend)` for `current`, `latexml`, and `pandoc`,
- `compare_parser_backends(root, backends=None)`,
- structured `parser_backend_result` and `parser_benchmark_report` contracts,
- quality checks for label preservation, environment recognition, align detection, and provenance availability,
- conservative `inconclusive` behavior when a backend is missing or fails.

Exposed parser benchmarking through CLI:

```bash
python -m mathdevmcp.cli parser-benchmark --root benchmarks/fixtures
```

Added `tests/test_parser_benchmark.py`.

### Verification completed

Targeted parser benchmark tests passed:

```text
4 passed
```

Full suite passed:

```text
119 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI parser benchmark on the fixture corpus reported:

```text
current: parsed, labels_found=41, environments_found=41, align_like_found=1, provenance=line, runtime≈0.002s
latexml: parsed, labels_found=126, environments_found=0, align_like_found=1, provenance=source, runtime≈7.0s
pandoc: parsed, labels_found=41, environments_found=78, align_like_found=2, provenance=source, runtime≈0.17s
```

### Audit notes

The first benchmark result is informative but not yet a final parser choice. Pandoc matched the fixture label count and was much faster than LaTeXML. LaTeXML preserved labels, but the first extraction pass over-counts generated XML IDs and does not yet classify environments well. The current parser still has the best line provenance. This supports the industrial plan: do not replace the parser blindly; use external parser adapters behind measured contracts and improve extraction scoring before routing production proof-audit workflows through them.

### Next slice

The next slice is the LeanDojo spike:

- validate a real Dojo theorem interaction, not just import/API smoke,
- prove one tiny theorem if the installed LeanDojo/toolchain combination supports it,
- fail or abstain on one false theorem,
- direct-check any produced proof artifact with `lean_check.py`,
- record version/toolchain mismatch as `inconclusive` if LeanDojo cannot run against the current Lean setup.

## Capability diagnostics outcome

The first industrial-tool slice added environment/capability diagnostics so coding agents can inspect backend readiness before selecting parser or prover workflows.

### Changes implemented

Added `src/mathdevmcp/doctor.py` with `doctor_report()`, reporting:

- Python executable, version, prefix, and PATH head,
- LaTeXML executable/version,
- Pandoc executable/version,
- Lean executable/version,
- Sage executable/version,
- LeanDojo import/version,
- SymPy import/version,
- known dependency conflicts.

Exposed diagnostics through:

- CLI: `python -m mathdevmcp.cli doctor`,
- MCP facade: `doctor`,
- FastMCP server: `doctor`.

Added `tests/test_doctor.py` for direct library, CLI, MCP facade, and FastMCP wrapper coverage.

### Verification completed

Targeted diagnostics tests passed:

```text
5 passed
```

Full suite passed:

```text
115 passed in 60.17s
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI `doctor` currently reports all core external tools available:

```text
latexml: available, /usr/bin/latexml, LaTeXML 0.8.6
pandoc: available, /usr/bin/pandoc, pandoc 2.9.2.1
lean: available, /home/chakwong/.elan/bin/lean, Lean 4.30.0-rc2
sage: available, /usr/bin/sage, SageMath 9.5
lean_dojo: available, lean-dojo 4.20.0
sympy: available, SymPy 1.14.0
```

It also correctly reports the current Python dependency warning:

```text
magic-pdf 1.3.12 declares pydantic<2.11, but active pydantic is 2.13.3; use a separate LeanDojo env if this matters.
```

### Audit notes

This slice is intentionally infrastructure-only. It makes backend availability observable and machine-readable without changing proof, parser, or benchmark semantics. The dependency-conflict warning is important because LeanDojo's dependencies altered the active Python environment; future industrial deployment should isolate LeanDojo in an optional environment if `magic-pdf` compatibility matters.

### Next slice

The next slice remains the parser adapter benchmark:

- compare current parser, LaTeXML, and Pandoc on the existing fixture corpus,
- score label preservation, environment recognition, align preservation, provenance quality, macro behavior, and runtime,
- keep failures as structured `inconclusive` results rather than hard crashes.

## Immediate next slice

Implement `mathdevmcp doctor` / capability diagnostics first. This gives coding agents a reliable way to know which external backends are available before selecting parser/prover workflows.

The second slice should compare parser backends on current fixtures:

- current lightweight parser,
- LaTeXML,
- Pandoc.

Only after that should the proof-audit pipeline be refactored around external parser adapters.
