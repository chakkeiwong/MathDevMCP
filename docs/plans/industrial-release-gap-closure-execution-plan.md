# Industrial release gap-closure execution plan

## Motivation

The latest release-readiness pass added the most important missing spine: proof-audit v2. A colleague or coding agent can now ask for a labeled mathematical audit and receive parser policy, typed `MathObligation` diagnostics, route decisions, shape diagnostics, numeric suggestions, backend attempts, provenance, actions, and conservative status aggregation in one report.

That is a large step forward, but it is not yet a department-wide industrial release. The remaining risk is no longer "the tool has no spine." The remaining risk is that the spine has only been tested on fixture-scale corpora and intentionally narrow backends. For colleagues working on mathematical finance, economics, computational econometrics, computational statistics, machine learning, LLMs, large-scale Bayesian learning, computational physics methods, and applied mathematics, release readiness now depends on measured behavior over realistic private/sanitized corpora, stronger parser and shape evidence, safer executable diagnostics, real optional LeanDojo proof-search boundaries, and reproducible deployment governance.

This plan closes the nine remaining gaps identified after commit `e35367d Add industrial release readiness spine`:

1. real corpus validation,
2. parser production hardening,
3. true LeanDojo backend,
4. executed numeric diagnostics integration,
5. richer shape/dimension semantics,
6. code-document semantic matching,
7. deployment and CI hardening,
8. security/governance,
9. release policy.

The desired outcome is an internal colleague-wide release candidate, not a claim that MathDevMCP proves arbitrary frontier mathematics.

## Safety invariant

No parser output, AST match, inferred type, dimension hint, route hint, shape guard, numeric diagnostic, generated Lean skeleton, LeanDojo tactic result, benchmark pass, release checklist, or review packet may become a verified mathematical claim unless a deterministic backend verifies the claim under explicit assumptions and MathDevMCP records reproducible evidence.

Use these semantics consistently:

- `verified`: deterministic backend evidence accepted by a MathDevMCP contract,
- `mismatch`: deterministic refutation or required-operation absence,
- `unverified`: plausible or partially supported but not certified,
- `inconclusive`: insufficient parser/backend/environment evidence,
- `human_review`: unsupported notation or assumptions require manual formalization/review.

Expected abstention is a quality property, not a failure. Never weaken abstention to make release numbers look better.

## Operating instructions for the next agent

Before implementation:

- Read `docs/plans/industrial-agent-tool-reset-memo.md`.
- Read `docs/plans/industrial-release-readiness-execution-plan.md`.
- Read `src/mathdevmcp/proof_audit_v2.py`.
- Run `git status --short`; preserve unrelated local `.codex` and `.serena/`.
- Update the reset memo before code changes with the selected slice and intended phases.

For each phase:

```text
plan phase
→ execute narrowly
→ add focused tests and benchmark cases
→ run targeted verification
→ audit false-confidence risk
→ tidy
→ update reset memo
```

After all selected phases:

- run full tests,
- run benchmark gate,
- run parser benchmark on public fixtures,
- run doctor,
- run `git diff --check`,
- record verification totals and environment caveats,
- commit relevant files only.

## Recommended slice ordering

Do not try to finish all nine gaps in one enormous patch unless explicitly requested. The recommended order is:

1. corpus manifest plus public sanitized stress fixtures,
2. parser/proof-audit-v2 stress gate,
3. shape/dimension and code-document semantic matching,
4. executed numeric diagnostic integration,
5. LeanDojo real backend fixture,
6. deployment/CI/security/release policy.

This ordering is deliberate. Larger corpora should reveal where parser, shape, AST, and diagnostic integrations actually fail before investing in heavier backend automation.

## Phase 1: real corpus validation

### Goal

Move release evidence from fixture-scale examples to realistic sanitized/private corpora while preserving privacy and expected-abstention accounting.

### Motivation

The current benchmark gate has 30 cases and passes, but the corpus is still small. Industrial release for colleagues requires evidence on documents and code shaped like actual department work: long documents, project-specific macros, multi-file LaTeX, dense state-space notation, HMC kernels, particle filters, DSGE equations, stochastic volatility models, SDE/PDE schemes, ML/LLM losses, ELBO/VI objectives, and computational-physics-inspired algorithms.

### Implementation details

Add or extend a corpus manifest module, preferably building on `src/mathdevmcp/corpus_roadmap.py`.

Suggested new module:

- `src/mathdevmcp/release_corpus.py`

Suggested contracts:

- `release_corpus_manifest`,
- `release_corpus_entry`,
- `release_corpus_validation_report`.

Each corpus entry should include:

- `id`,
- `domain`,
- `privacy_class`: `public_fixture`, `sanitized_internal`, `private_external`,
- `document_root`,
- `code_roots`,
- `expected_labels`,
- `expected_operations`,
- `expected_abstentions`,
- `seeded_false_confidence_cases`,
- `required_parser_backends`,
- `release_gate_enabled`,
- `notes`.

Public fixture domains to add first:

- `kalman_state_space_extended`,
- `hmc_nuts_leapfrog`,
- `particle_filter_logsumexp`,
- `dsge_macro_finance_euler`,
- `stochastic_volatility_likelihood`,
- `sde_pde_numerics`,
- `ml_llm_objective`,
- `bayesian_elbo_vi`,
- `computational_physics_mcmc`.

Do not commit private corpora. For private corpora, commit only a manifest stub with expected labels and privacy class.

Add CLI/MCP only if small:

```bash
python -m mathdevmcp.cli release-corpus-manifest
python -m mathdevmcp.cli validate-release-corpus --root /path/to/corpus
```

### Tests

Add tests that:

- manifest contains every required domain,
- private entries are marked external/not-in-git,
- every release-gated public fixture has at least one expected label,
- each domain declares at least one expected abstention or seeded false-confidence case,
- benchmark gate accounts for release-corpus categories without treating private files as missing failures.

### Acceptance criteria

The release has a machine-readable map of what has and has not been validated. Colleagues can distinguish public fixture evidence from private/sanitized evidence.

## Phase 2: parser production hardening

### Goal

Make parser selection robust enough for proof-audit v2 over realistic LaTeX projects.

### Motivation

The current parser benchmark records expected-label recall, generated-like labels, provenance score, environment count, and align-like count. That is useful but not enough for production documents with macros, theorem environments, multi-file projects, and repeated labels.

### Implementation details

Extend `src/mathdevmcp/parser_benchmark.py` and `src/mathdevmcp/parser_policy.py`.

Add parser scoring fields:

- `expected_label_precision`,
- `expected_label_recall`,
- `generated_label_count`,
- `source_span_quality`,
- `section_path_quality`,
- `macro_visibility`,
- `environment_types`,
- `duplicate_label_findings`,
- `multi_file_coverage`,
- `fatal_errors`,
- `warnings`.

Add parser policy levels:

- `selected_for_proof_audit`,
- `selected_for_context_only`,
- `measured_optional`,
- `blocked`.

Proof-audit v2 should treat parser policy as follows:

- `selected_for_proof_audit`: obligations may route to deterministic backends,
- `selected_for_context_only`: report context but do not certify,
- `measured_optional`: benchmark evidence only,
- `blocked`: force `inconclusive`.

Add stress fixtures:

- nested macros around `\label`,
- theorem/assumption/proposition environments,
- `align`, `aligned`, `split`, `gather`, and equation arrays,
- multi-file `\input` or `\include` documents,
- repeated nearby labels,
- generated labels from external parser outputs.

### Tests

Add tests that:

- current parser preserves line provenance on stress fixtures,
- generated labels do not inflate expected-label recall,
- missing expected labels block proof-audit certification,
- duplicate labels are reported,
- external parser crashes return structured `inconclusive`,
- proof-audit v2 downgrades to `inconclusive` when parser policy is blocked.

### Acceptance criteria

The release can state which parser is trusted for proof-audit routing on each corpus and why.

## Phase 3: true optional LeanDojo backend

### Goal

Move from a truthful LeanDojo boundary to a real optional proof-search backend when a pinned local traced theorem target exists.

### Motivation

Lean direct checking already provides certificate evidence. LeanDojo is still not a true backend. Industrial release should either provide a real local Dojo fixture or explicitly report that LeanDojo remains readiness-only in the current environment.

### Implementation details

Extend `src/mathdevmcp/leandojo_backend.py`.

Add configuration:

- env var `MATHDEVMCP_LEANDOJO_FIXTURE`,
- env var `MATHDEVMCP_LEANDOJO_THEOREM`,
- optional config object for traced repo path, theorem name, timeout, tactic ladder.

Workflow:

```text
detect LeanDojo/Lean/Lake
→ locate pinned traced repo fixture
→ create theorem entry
→ enter Dojo(entry)
→ observe initial goal
→ apply bounded tactics
→ detect ProofFinished
→ reconstruct Lean proof source
→ run direct Lean final check
→ return leandojo_attempt_result
```

Initial tactics:

- `rfl`,
- `simp`,
- exact known lemma for tiny theorem,
- optional `omega`, `ring`, or `linarith` only when Mathlib/toolchain evidence exists.

Hard boundaries:

- no network requirement in the default test suite,
- no unbounded tactic search,
- no generated proof accepted without direct Lean final check,
- failed tactics do not imply theorem falsehood.

### Tests

Add tests that:

- no fixture configured returns `inconclusive`,
- false theorem or failed tactic does not verify,
- direct Lean final-check invariant is always present,
- real Dojo fixture test is skipped unless env vars are configured,
- any successful Dojo proof includes tactic trace and final Lean check evidence.

### Acceptance criteria

The release can truthfully classify LeanDojo as either:

- `real_optional_backend_available`, or
- `readiness_only_in_this_environment`.

## Phase 4: executed numeric diagnostics integration

### Goal

Wire safe executed numeric diagnostics into proof-audit v2 and code-document workflows when explicit safe encodings are available.

### Motivation

`numeric_runner.py` can run explicit checks, but proof-audit v2 currently mostly attaches suggestions. Industrial use needs a path from extracted obligations and code fixtures to bounded numeric evidence without ever executing code generated from arbitrary LaTeX.

### Implementation details

Extend `src/mathdevmcp/numeric_runner.py` and add:

- `NumericDiagnosticPlan`,
- `NumericDiagnosticArtifact`,
- `run_numeric_diagnostic_plan(...)`,
- `numeric_artifact_from_fixture(...)`.

Add safe encodings only from:

- explicit arrays/functions supplied by tests,
- whitelisted fixture modules,
- manually supplied JSON artifacts,
- code paths that are imported under a test-only safe fixture policy.

Do not import arbitrary project modules by default. If importing a fixture module, require:

- path under `benchmarks/fixtures` or explicit allowlist,
- timeout,
- max matrix size,
- deterministic seed,
- no file/network side effects,
- structured failure.

Integrate with proof-audit v2:

- if typed diagnostic suggests `logdet_domain_check` and a matching safe artifact exists, run it,
- if `linear_solve_residual_check` has a safe matrix/vector artifact, run it,
- if derivative/gradient check has callable artifact, run finite differences,
- attach executed results under `numeric_diagnostics.executed`,
- never upgrade document obligation to `verified` unless the executed diagnostic actually certifies the same scoped claim under explicit assumptions.

### Tests

Add tests that:

- proof-audit v2 attaches executed logdet evidence for an explicit SPD fixture,
- non-SPD fixture gives `mismatch` diagnostic but not broad theorem refutation,
- missing safe artifact keeps suggestion-only behavior,
- unsafe path outside allowlist returns `inconclusive`,
- timeout and max-size limits are enforced.

### Acceptance criteria

Numeric diagnostics become actionable evidence where safe, while unsupported notation still abstains.

## Phase 5: richer shape and dimension semantics

### Goal

Improve shape/dimension diagnostics for matrix/statistical code without pretending to implement dependent typing.

### Motivation

Current shape diagnostics identify missing constraints and some AST guards. Industrial use needs clearer handling of matrix dimensions, SPD/invertibility, conformable products, stochastic indexing, batch axes, and broadcasting in NumPy/JAX/PyTorch-style code.

### Implementation details

Extend or add:

- `src/mathdevmcp/shape_diagnostics.py`,
- `src/mathdevmcp/shape_semantics.py`,
- `src/mathdevmcp/ast_operation_graph.py`.

Add diagnostic records:

- `ShapeSymbol`,
- `ShapeRelation`,
- `MatrixProperty`,
- `BatchAxisEvidence`,
- `BroadcastingRisk`,
- `StochasticIndexEvidence`.

Recognize:

- `.shape`,
- `assert x.shape[...]`,
- `jax.debug.check_shape`-style patterns,
- `torch.Tensor`/NumPy/JAX shape references,
- Cholesky/SVD/eigendecomposition as SPD or rank evidence only when explicit guards exist,
- covariance update symmetry/PSD guards,
- batch axes in `vmap`, `scan`, `einsum`, `matmul`.

Add missing-assumption categories:

- `square_matrix_required`,
- `spd_required`,
- `invertibility_required`,
- `conformable_product_required`,
- `broadcasting_policy_required`,
- `batch_axis_policy_required`,
- `time_index_alignment_required`.

### Tests

Add tests that:

- explicit shape assertions reduce missing constraints to diagnostic support,
- AST guards do not upgrade to proof,
- missing batch-axis policy is reported,
- broadcasting ambiguity is reported,
- covariance/SPD guard evidence is preserved with line numbers.

### Acceptance criteria

Proof-audit v2 and code audits can explain shape risks in the language department developers use.

## Phase 6: code-document semantic matching

### Goal

Strengthen code-document consistency beyond operation presence by mapping documented obligations to implementation structures.

### Motivation

AST operation extraction currently finds operations like logdet, solve, gradients, leapfrog updates, and particle normalization. Industrial use needs richer checks: variable correspondences, update ordering, required guards, likelihood terms, and semantic roles.

### Implementation details

Add a module:

- `src/mathdevmcp/semantic_alignment.py`

Suggested contracts:

- `semantic_alignment_report`,
- `semantic_alignment_finding`.

Inputs:

- proof-audit v2 report,
- AST operation graph,
- optional symbol map,
- optional required role map.

Alignment dimensions:

- documented operation present in code,
- required operation missing,
- operation order plausible,
- shape guard present,
- covariance/SPD guard present,
- variable role mapped,
- update recurrence terms present,
- suspicious extra operation.

Start with narrow workflows:

- state-space likelihood,
- Kalman recursion,
- HMC leapfrog/Hamiltonian,
- particle filter normalization.

Do not attempt general semantic equivalence. Return `consistent`, `mismatch`, `unverified`, or `inconclusive` with findings.

### Tests

Add tests that:

- state-space likelihood aligns logdet, solve, and quadratic form,
- missing solve remains `mismatch`,
- HMC leapfrog checks gradient and momentum/position update roles,
- particle filter checks logsumexp normalization,
- unmapped variables remain `unverified`, not verified.

### Acceptance criteria

The tool can tell a colleague not only "logdet exists" but "the documented likelihood requires logdet, solve, and quadratic form; this implementation has logdet and quadratic form but no solve/inverse evidence."

## Phase 7: deployment and CI hardening

### Goal

Make installation, testing, and backend availability reproducible for colleagues.

### Motivation

Optional dependency groups now exist, but release still needs CI jobs, scripts, pinned environment recipes, and clear worker isolation.

### Implementation details

Add or update:

- `.github/workflows/ci.yml` if GitHub Actions is accepted,
- `scripts/release_smoke.sh`,
- `scripts/parser_benchmark_smoke.sh`,
- `scripts/doctor_smoke.sh`,
- `docs/mathdevmcp-deployment-guide.md`.

CI jobs:

- base import and unit tests,
- benchmark gate,
- parser benchmark with current parser,
- doctor report,
- optional Lean direct-check smoke if toolchain cache available,
- no LeanDojo network-dependent job by default.

Environment recipes:

- base,
- symbolic,
- MCP,
- parser system tools,
- Lean direct checker,
- isolated LeanDojo.

Record exact commands in docs. External commands must have timeouts. CI should store benchmark and doctor outputs as artifacts if available.

### Tests

Add tests/scripts checks that:

- scripts exit nonzero on failed gate,
- base package import does not import LeanDojo,
- doctor handles missing tools,
- benchmark gate does not require network.

### Acceptance criteria

A colleague can reproduce local release smoke results from a fresh clone.

## Phase 8: security and governance

### Goal

Define and enforce the safety policy for external tools, private corpora, generated artifacts, and agent use.

### Motivation

MathDevMCP runs parsers, proof tools, and numeric checks around sensitive research documents. Industrial release needs explicit governance: what may be run, what may be committed, what may be sent to agents, and what counts as evidence.

### Implementation details

Add docs and lightweight policy code:

- `docs/mathdevmcp-security-governance.md`,
- `src/mathdevmcp/governance.py`.

Policy fields:

- external command allowlist,
- timeout policy,
- max file size policy,
- private corpus no-commit policy,
- artifact retention policy,
- no-exfiltration statement,
- generated proof/code artifact labeling,
- expected-abstention policy,
- verified-claim policy.

Governance report should be machine-readable:

```bash
python -m mathdevmcp.cli governance-policy
```

Add high-level MCP tool only if useful:

- `governance_policy`.

### Tests

Add tests that:

- policy includes no-private-corpus-commit rule,
- external tools require timeouts,
- verified-claim policy names deterministic backend evidence,
- generated artifacts are classified non-certifying unless checked,
- governance report has contract metadata.

### Acceptance criteria

The release has an explicit safety/governance artifact that agents and humans can cite.

## Phase 9: formal release policy

### Goal

Define the release checklist and versioning criteria for colleague-wide internal release.

### Motivation

Passing tests is necessary but not sufficient. A release needs a documented go/no-go policy: benchmark thresholds, schema compatibility, known limitations, environment status, changelog, and rollback path.

### Implementation details

Add:

- `docs/mathdevmcp-release-policy.md`,
- `src/mathdevmcp/release_policy.py`,
- optional CLI `release-readiness`.

Release readiness report should include:

- package version,
- git commit,
- dirty worktree flag,
- benchmark gate status,
- category breakdown,
- expected abstentions,
- doctor summary,
- parser policy summary,
- Lean/LeanDojo status,
- governance policy version,
- schema version,
- known blockers,
- recommendation: `ready`, `ready_with_caveats`, or `not_ready`.

Release gates:

- full tests pass,
- benchmark gate passes,
- parser corpus gate passes,
- no unexpected private files staged,
- doctor has no critical missing base capabilities,
- Lean/LeanDojo caveats explicitly recorded,
- docs updated,
- reset memo updated.

### Tests

Add tests that:

- release-readiness report is `not_ready` when benchmark gate fails,
- dirty worktree is reported,
- expected abstentions are counted,
- Lean version/download issue is represented as caveat, not hidden,
- report carries contract metadata.

### Acceptance criteria

The final release decision is machine-readable and auditable.

## Final verification commands

Run at minimum:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli benchmark-gate --root /home/chakwong/MathDevMCP
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli parser-benchmark --root /home/chakwong/MathDevMCP/benchmarks/fixtures --backend current
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli doctor
git diff --check
git status --short
```

If adding CI or release scripts, also run:

```bash
/home/chakwong/MathDevMCP/scripts/release_smoke.sh /home/chakwong/MathDevMCP
```

Record all outputs in the reset memo, including environment caveats such as Lean toolchain download/version failures.

## Non-goals

- Do not implement a full LaTeX parser.
- Do not implement a full theorem prover.
- Do not autoformalize arbitrary economics/finance prose into Lean.
- Do not make LeanDojo mandatory for base install.
- Do not execute arbitrary code generated from LaTeX.
- Do not commit private department documents.
- Do not claim AST/shape/numeric diagnostics are mathematical proof.
- Do not reduce expected-abstention cases to make release metrics look stronger.

## Suggested first slice

The best first slice is:

1. add `release_corpus.py` and a machine-readable release corpus manifest,
2. add one public sanitized fixture each for DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objective, ELBO/VI, and computational-physics MCMC,
3. add proof-audit-v2/parser benchmark cases for those fixtures,
4. keep expected abstentions explicit,
5. update the reset memo and commit.

This will reveal the most important practical failures before deeper LeanDojo, numeric-execution, or CI work.
