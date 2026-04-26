# Industrial release readiness execution plan

## Motivation

MathDevMCP now has a serious industrial scaffold: capability diagnostics, parser benchmarking, proof-audit primitives, typed/dimensional `MathObligation` diagnostics, route decisions, shape diagnostics, numeric diagnostic suggestions, conservative Lean and LeanDojo boundaries, AST operation extraction, Kalman-style workflows, benchmark gates, and agent-facing review packets.

That is enough to support careful internal experimentation, but it is not yet enough for a departmental industrial release to colleagues working on mathematical finance, economics, computational econometrics, computational statistics, machine learning, large language models, large-scale Bayesian learning, computational physics methods, and applied mathematics.

The gap is not another broad layer of scaffolding. The next agent should turn the existing scaffold into a release-quality vertical path:

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

The immediate release blocker is proof-audit v2: every extracted proof-audit obligation should carry typed diagnostics, route decisions, shape diagnostics, numeric/backend evidence, and clear abstention reasons in the primary proof-audit report. After that spine exists, the remaining release work can harden parser evidence, LeanDojo, numeric diagnostics, corpus gates, packaging, and operator documentation around one coherent workflow.

## Safety invariant

No parser output, AST match, inferred type, dimension hint, route hint, shape guard, numeric diagnostic, generated Lean skeleton, LeanDojo failure, benchmark pass, or review packet may become a verified mathematical claim unless a deterministic backend verifies the claim under explicit assumptions and MathDevMCP records reproducible evidence.

Use `verified` only for deterministic backend evidence accepted by the contract. Use `mismatch` for deterministic refutations. Use `unverified`, `inconclusive`, `human_review`, or similarly conservative statuses for missing assumptions, unsupported notation, unavailable tools, timeouts, unsafe encodings, parser loss, or diagnostic-only evidence.

## Release target

The target release is an internal department tool that colleagues can use through CLI/MCP to audit mathematical code and documents. It does not need to prove arbitrary frontier mathematics. It does need to be predictable, conservative, reproducible, and useful enough that agents and developers can locate proof gaps, implementation mismatches, missing assumptions, and backend limitations without mistaking diagnostics for proof.

Release readiness means:

- base package imports without heavyweight optional tools,
- `doctor` explains available external backends and dependency conflicts,
- proof-audit reports expose typed routes and abstentions per obligation,
- parser/provenance behavior is measured on realistic department-style fixtures,
- at least one symbolic backend and direct Lean checker provide real evidence paths,
- LeanDojo readiness is truthful and separated from direct Lean checking,
- expected abstentions and false-confidence seeds are explicit in benchmarks,
- CLI/MCP workflows are compact and documented for colleagues,
- packaging, CI, and operator docs describe exactly what is supported.

## Operating instructions for the next agent

Before implementation:

- Read `docs/plans/industrial-agent-tool-reset-memo.md`.
- Read `docs/plans/industrial-agent-tool-plan.md`.
- Read this plan end to end.
- Run `git status --short` and preserve unrelated local files such as `.codex` and `.serena/`.
- Update the reset memo with the planned slice before code changes.

For every phase below, follow this cycle:

```text
plan phase
→ execute narrowly
→ add or update focused tests
→ run targeted verification
→ audit for false-confidence risk
→ tidy
→ update reset memo
```

At the end:

- run the full test suite,
- run the benchmark gate,
- run `git diff --check`,
- commit relevant files only,
- update the reset memo with final outcomes, commands, totals, limitations, and next work.

## Phase 1: proof-audit v2 as the release spine

### Goal

Make `audit_derivation_for_label(...)` or a new v2 entry point return a release-quality obligation report. Each obligation should include parser provenance, typed diagnostics, route decisions, shape diagnostics, numeric suggestions, backend evidence, and explicit abstention reasons.

### Implementation details

Prefer a small additive module such as `src/mathdevmcp/proof_audit_v2.py` before replacing the current `proof_audit.py`. Keep the existing public behavior stable unless tests are deliberately migrated.

Recommended objects:

- `ProofAuditV2Report`
- `ProofAuditV2Obligation`
- `ProofAuditV2Route`
- `ProofAuditV2EvidenceSummary`

Each obligation should include:

- `id`
- `label`
- `source_text`
- `lhs`
- `rhs`
- `kind`
- `provenance`
- `parser_backend`
- `parser_policy`
- `typed_diagnostic`
- `route_decision`
- `shape_diagnostic`
- `numeric_diagnostics`
- `backend_attempts`
- `status`
- `reason`
- `actions`

Use existing helpers instead of duplicating logic:

- `typed_workflows.typed_obligation_for_label(...)`
- `math_ir.diagnose_typed_obligation(...)`
- `routing.route_typed_diagnostic(...)`
- `shape_diagnostics.diagnose_shape_constraints(...)`
- `numeric_diagnostics.suggest_numeric_diagnostics(...)`
- `parser_policy.decide_parser_policy(...)`
- `proof_obligations.check_proof_obligation(...)`
- `contracts.attach_contract(...)`

The v2 report should make it impossible for an agent to see a bare `inconclusive` without knowing why. It should distinguish at least:

- parser/provenance blocker,
- unsupported notation,
- missing assumptions,
- missing shape constraints,
- unsafe backend encoding,
- backend unavailable,
- backend timeout,
- backend refutation,
- backend verification.

### Tests

Add tests proving:

- simple scalar algebra includes typed diagnostics and a symbolic route,
- Kalman/state-space likelihood includes missing shape/assumption actions and does not verify,
- HMC/posterior notation routes to human review or diagnostics without proof,
- backend-safe false algebra returns `mismatch`,
- parser/provenance loss blocks certification,
- every obligation has provenance, route decision, status, reason, and contract metadata.

### Acceptance criteria

The primary release workflow can show colleagues not just "unverified", but "unverified because this obligation has matrix inverse/logdet notation, missing SPD/invertibility assumptions, no safe backend encoding, and only diagnostic numeric suggestions."

## Phase 2: CLI/MCP exposure for proof-audit v2

### Goal

Expose the v2 report through colleague-facing surfaces without flooding agents with massive payloads.

### Implementation details

Add CLI command:

```bash
python -m mathdevmcp.cli audit-derivation-v2-label LABEL --root ROOT
```

Suggested options:

- `--before`
- `--after`
- `--paragraph-context`
- `--backend`
- `--cache`
- `--summary-only`

Add MCP facade and FastMCP server tools:

- `audit_derivation_v2_label`

For compact output, include:

- top-level status,
- counts,
- high-priority actions,
- per-obligation summary,
- paths or nested fields for detailed evidence.

Do not remove the existing `audit_derivation_label` command until v2 is stable.

### Tests

Add CLI, MCP facade, and FastMCP wrapper tests. Invalid arguments should return structured errors. Backend failures should return `inconclusive` or `unverified`, not exceptions.

### Acceptance criteria

A coding agent can call one tool and receive a compact, actionable report suitable for a pull-request review comment or implementation checklist.

## Phase 3: parser evidence hardening on realistic documents

### Goal

Make parser selection evidence-based over realistic department-style LaTeX, not only small synthetic fixtures.

### Implementation details

Extend parser benchmark fixtures with sanitized examples covering:

- long align environments,
- theorem/proposition/assumption blocks,
- notation tables,
- repeated labels or nearby similar labels,
- macros around covariance, likelihood, posterior, gradients, traces, log determinants,
- multi-file documents with sections/subsections.

Harden parser benchmark scoring:

- expected label recall,
- generated-label filtering,
- environment classification,
- source line or source span availability,
- section path preservation,
- macro transparency,
- runtime and failure reason,
- provenance quality score.

Parser policy should block proof-audit routing if required labels or provenance are missing. External parser failures should remain measured `inconclusive` results.

### Tests

Add parser benchmark tests for:

- all expected labels preserved,
- missing labels reported,
- generated labels not counted as real expected labels,
- current parser selected only when line provenance is present,
- LaTeXML/Pandoc failures do not crash the benchmark.

### Acceptance criteria

The release can state which parser is trusted for proof-audit routing on the current corpus and why.

## Phase 4: executable numeric diagnostics with safe encodings

### Goal

Move from "suggest numeric checks" to "run bounded diagnostics only when safe" for selected matrix/statistical obligations.

### Implementation details

Add a small module such as `src/mathdevmcp/numeric_runner.py`.

Supported diagnostic runners should be narrow:

- logdet domain check on explicitly supplied SPD test matrices,
- solve residual check for `A x = b`,
- finite-difference gradient check for Python callables only when supplied directly by code tests,
- trace/shape sanity checks for explicit arrays,
- optional Sage availability and version evidence.

Do not parse arbitrary LaTeX into executable numeric code. Require explicit safe encodings or known test fixtures. Every runner must have:

- timeout,
- input size bound,
- deterministic seed when random data is used,
- backend/version evidence,
- result status,
- failure reason.

### Tests

Add tests for:

- successful solve residual diagnostic,
- logdet rejects non-SPD input,
- finite-difference diagnostic detects a seeded wrong gradient,
- unsafe missing encoding returns `inconclusive`,
- timeout/unavailable backend returns structured `inconclusive`.

### Acceptance criteria

Proof-audit v2 can attach executed numeric evidence where safe, while unsupported document notation still abstains.

## Phase 5: LeanDojo real interaction boundary

### Goal

Replace "LeanDojo import/API smoke" with a truthful optional backend boundary that can attempt one real traced theorem interaction when the environment supports it.

### Implementation details

Add or extend a module such as `src/mathdevmcp/leandojo_backend.py`.

Implement:

- detection of LeanDojo, Lean, Lake, Python executable, and versions,
- traced repository target configuration,
- theorem entry configuration,
- bounded tactic attempt,
- `ProofFinished` detection when available,
- reconstructed Lean proof artifact,
- final direct Lean check through existing `lean_check.py`,
- structured `inconclusive` when tracing/toolchain/network/cache requirements are not satisfied.

Keep this optional. The base test suite must not require network access or large downloads.

### Tests

Add tests that:

- policy-only mode reports missing traced repo as `inconclusive`,
- direct Lean final-check invariant is always present,
- false theorem or failed tactic does not become verified,
- environment failure is structured,
- any real Dojo integration test is skipped unless an explicit local fixture/env var is present.

### Acceptance criteria

The release documentation can truthfully say whether LeanDojo is available only as a readiness diagnostic or as a real optional proof-search backend in that environment.

## Phase 6: department benchmark corpus and release gates

### Goal

Make release quality measurable across the domains colleagues actually work on.

### Implementation details

Extend benchmark categories and fixtures around:

- Kalman/state-space likelihoods,
- HMC/NUTS/leapfrog/Hamiltonian structure,
- particle filters and logsumexp normalization,
- DSGE/macro-finance Euler equations,
- stochastic volatility models,
- SDE/PDE numerical schemes,
- ML/LLM objectives and gradients,
- Bayesian posterior/ELBO/VI objectives,
- computational-physics algorithms such as MCMC, variational methods, and linear solvers.

For each category include:

- one expected-success case where the tool should produce useful evidence,
- one expected-abstention case,
- one seeded false-confidence case.

Do not commit private documents. Add a manifest for private/sanitized corpora with expected labels and privacy classification.

Benchmark gate should report:

- total cases,
- passed cases,
- failed cases,
- expected abstentions,
- false-confidence failures,
- category breakdown,
- parser/backend availability effects.

### Tests

Add category-level tests for benchmark accounting and at least one new realistic fixture in each newly introduced category before making it a release gate.

### Acceptance criteria

Release readiness is based on measured behavior across realistic classes of problems, not just infrastructure tests.

## Phase 7: packaging, dependency isolation, and CI

### Goal

Make the project installable and runnable by colleagues without accidentally requiring the heaviest optional tools.

### Implementation details

Update `pyproject.toml` with optional dependency groups where appropriate:

```toml
[project.optional-dependencies]
dev = ["pytest"]
symbolic = ["sympy"]
mcp = ["fastmcp"]
leandojo = ["lean-dojo"]
all = ["sympy", "fastmcp", "lean-dojo"]
```

Only add dependencies that are actually imported by optional paths. System tools should remain runtime-detected:

- `latexml`,
- `pandoc`,
- `lean`,
- `lake`,
- `sage`.

Add operator-facing environment recipes:

- base install,
- parser-enabled environment,
- Lean environment,
- LeanDojo isolated environment,
- CI smoke environment.

Add CI or local release scripts for:

- unit tests,
- benchmark gate,
- parser benchmark,
- doctor report,
- docs/link sanity if available.

External commands must use timeouts and structured failure contracts.

### Tests

Add tests that:

- base package imports without optional tools,
- missing optional tools produce structured unavailable/inconclusive results,
- `doctor` reports dependency conflicts,
- benchmark gate can run without LeanDojo network access.

### Acceptance criteria

A colleague can install the base tool, run `doctor`, run the benchmark gate, and understand which advanced workers are unavailable without seeing crashes or silent degraded behavior.

## Phase 8: colleague-facing operator guide

### Goal

Write the release documentation that prevents misuse.

### Implementation details

Update or add docs covering:

- installation modes,
- `doctor`,
- proof-audit v2 workflow,
- code/document audit workflow,
- Kalman/state-space workflow,
- benchmark gate,
- expected abstentions,
- status semantics,
- how to add sanitized/private fixtures,
- how to interpret Lean/LeanDojo results,
- what MathDevMCP does not prove.

Include concrete commands and small sample outputs. Avoid marketing language. The documentation should help a colleague decide whether a result can support a mathematical claim.

### Tests

If no docs test infrastructure exists, run `git diff --check` and manually check commands against the CLI parser. If docs tests exist later, add snippets to them.

### Acceptance criteria

The release has enough operator guidance that a careful colleague does not need the maintainer present to avoid the major false-confidence traps.

## Phase 9: release candidate audit

### Goal

Audit the implementation as if reviewing another developer's release candidate.

### Checklist

- No diagnostic-only evidence can produce `verified`.
- Parser label loss blocks proof-audit certification.
- Missing assumptions are visible per obligation.
- Shape/dimension evidence is diagnostic unless backed by explicit assumptions.
- Numeric diagnostics require safe encodings.
- LeanDojo success still requires direct Lean final check.
- Expected abstentions are counted separately from failures.
- False claims never pass benchmark cases.
- Base package import does not require optional heavy tools.
- External commands have timeouts.
- CLI/MCP outputs include contract metadata.
- Reset memo records exact verification commands and totals.

Write a short plan-audit document if the slice substantially changes architecture.

## Final verification commands

Run at minimum:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli doctor
git diff --check
git status --short
```

If Lean-dependent tests require network/toolchain access, record both the sandboxed failure mode and the approved successful command. Do not hide environment-dependent behavior.

## Non-goals

- Do not build a full LaTeX parser.
- Do not build a full theorem prover.
- Do not autoformalize arbitrary finance/economics prose into Lean.
- Do not make LeanDojo mandatory for the base package.
- Do not run arbitrary code generated from LaTeX.
- Do not commit private department documents.
- Do not weaken abstention behavior to make benchmark totals look better.

## Suggested first implementation slice

Start with Phase 1 and Phase 2 only:

1. Add proof-audit v2 as an additive report.
2. Wire it to CLI/MCP.
3. Add focused tests over scalar algebra, Kalman likelihood, HMC notation, and seeded false algebra.
4. Add one benchmark-gate case for the v2 report.
5. Update the reset memo and commit.

This first slice creates the release spine. The later parser, numeric, LeanDojo, corpus, packaging, and documentation work should attach to that spine rather than creating parallel reports.
