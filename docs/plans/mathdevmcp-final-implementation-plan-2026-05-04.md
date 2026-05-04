# MathDevMCP final implementation plan

## Purpose

This plan combines the best parts of:

- `docs/plans/mathdevmcp-improvement-review-and-product-plan.md`
- `docs/plans/mathdevmcp-macrofinance-product-roadmap-2026-05-04.md`

It turns the product review, macro-finance roadmap, and follow-up review
comments into one implementation-facing plan.

The result should guide actual engineering work. The goal is not to make
MathDevMCP more aggressive. The goal is to make conservative abstention more
useful, more structured, and easier for agents and researchers to act on.

## Source-document scope

The implementation plan is grounded in real monograph workflows:

- `/home/chakwong/latex/CIP_monograph/main.tex`
- `/home/chakwong/python/docs/monograph.tex`

The corrected CIP monograph covers CIP deviations, SDF and no-arbitrage
pricing, affine term-structure models, FX basis, nonlinear dynamics, filtering,
particle methods, Bayesian estimation, HMC, transport maps, multi-country
macro-finance, ZLB/shadow-rate structure, cointegration, identification,
empirical design, and code/document cross-references.

The DSGE monograph covers dynamic optimization, Euler equations,
log-linearization, Kronecker and eigensystem identities, New Keynesian,
Epstein-Zin and SGU models, perturbation methods, neural solvers, Kalman and
SVD filters, stationarity, constrained transforms, posterior geometry, HMC,
transport methods, XLA/custom operations, numerical stability, and experiments.

These documents show that MathDevMCP must support much more than filtering:
large-root LaTeX engineering, equation localization, notation governance,
matrix calculus, no-arbitrage algebra, structural macro equilibrium,
identification, code traceability, literature support, and durable evidence
packets.

## Product invariant

MathDevMCP must remain conservative.

No parser output, AST match, inferred type, shape hint, route hint, numeric
diagnostic, assumption manifest, convention registry, dependency graph,
domain template, proof packet, citation packet, or Lean environment check may
become a verified mathematical claim unless a deterministic backend verifies
the exact scoped obligation under explicit assumptions and records
reproducible evidence.

Diagnostic evidence can guide work. It must not be presented as proof.

## Architecture

Split the product into a reusable core platform and optional domain packs.

### Core platform

The core platform owns reusable verification infrastructure:

- public result contracts and schema versions;
- status, substatus, severity, and next-action taxonomy;
- compact MCP payload rules and debug expansion controls;
- large-root LaTeX indexing and cache shards;
- equation localization and reconstruction;
- matrix/operator IR;
- assumption manifests;
- notation and sign-convention registries;
- claim, assumption, convention, code, experiment, and packet dependency graph;
- proof packets and negative-evidence packets;
- numeric diagnostic harness;
- backend, Sage, Z3, Lean, Lake, and LeanDojo readiness diagnostics;
- workflow rules that teach agents how to use tool-provided next actions.

### Domain packs

Domain packs build on the core and remain optional:

- filtering and state-space pack;
- affine, CIP, SDF, and term-structure pack;
- DSGE and macro-perturbation pack;
- Bayesian posterior geometry, HMC, and transport pack;
- particle and optimal-transport pack;
- code-document traceability pack;
- literature and citation-support pack;
- identification and empirical-design pack.

This split prevents MathDevMCP from becoming a monolithic macro-finance
codebase while still supporting the finance and economics workflows that
motivated the review.

## Implementation phases

### Phase 0: contracts, status taxonomy, and payload ergonomics

Problem:

Current conservative statuses are valuable but too coarse for agents. Public
surfaces also need stable schemas before proof packets, manifests, templates,
and graph artifacts multiply.

Deliverables:

- `status_taxonomy.py` with stable top-level statuses, substatuses, severity,
  and reason fields;
- schema metadata for every public artifact;
- versioned JSON/YAML schemas for manifests, packets, template specs, notation
  registries, and dependency graphs;
- migration and compatibility policy for schema changes;
- redaction rules for private roots and private corpus paths;
- compact MCP summaries by default;
- optional debug expansion fields such as `summary_only`,
  `include_parser_report`, `include_graph`, and `max_diagnostics`;
- next-action payloads with stable shape across library, CLI, and MCP.

Initial substatuses:

- `unverified:missing_assumption`
- `unverified:missing_shape`
- `unverified:parser_limit`
- `unverified:unsupported_noncommutative_algebra`
- `unverified:manual_formalization_required`
- `mismatch:likely_formula_error`
- `mismatch:normalization_gap`
- `inconclusive:source_label_missing`
- `inconclusive:partial_index_only`
- `inconclusive:backend_unavailable`
- `inconclusive:toolchain_not_ready`
- `inconclusive:timeout`

Critical files:

- `src/mathdevmcp/contracts.py`
- new `src/mathdevmcp/status_taxonomy.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/_workflow_rules.py`
- `docs/clients/workflow-rules.md`

Acceptance gates:

- every non-verified public result has `status`, `substatus`, `reason`, and
  at least one actionable next step;
- backend/environment failures do not masquerade as mathematical mismatches;
- default MCP payloads are concise enough for agent use;
- public JSON artifacts declare schema version and redaction policy.

### Phase 1: large-root indexing and equation localization

Problem:

Large monographs should not fail as a unit because one chapter, include, macro,
or backend call fails. In addition, matrix IR and proof packets need precise
math slices, not just nearby text.

Deliverables:

- partial-success LaTeX indexing;
- per-file parse diagnostics;
- chapter and part cache shards with hash-based invalidation;
- include graph and macro summary;
- duplicate-label and missing-label findings;
- nearest-label and topic lookup with confidence;
- equation localization and reconstruction for `equation`, `align`,
  `aligned`, `gather`, `multline`, and common display-math forms;
- row-level and subexpression source spans;
- macro expansion boundaries that preserve provenance;
- label-to-equation reconstruction suitable for matrix IR and proof packets.

Critical files:

- `src/mathdevmcp/latex_index.py`
- `src/mathdevmcp/index_cache.py`
- new `src/mathdevmcp/equation_locator.py`
- `src/mathdevmcp/parser_policy.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/cli.py`

Acceptance gates:

- one broken chapter does not prevent search or label lookup in unrelated
  chapters;
- a multi-line `align` derivation can be split into row-level obligations with
  line/source provenance;
- localized expressions are explicitly marked when macro expansion or
  environment parsing is lossy;
- source-localization uncertainty produces `unverified:parser_limit`, not a
  formula mismatch.

### Phase 2: assumption manifests, notation registries, and dependency graph

Problem:

Real finance and economics derivations often fail because assumptions,
notation, or conventions are implicit. These must become first-class objects.

Deliverables:

- machine-readable assumption manifests attached to labels, sections,
  chapters, or roots;
- notation registries for symbol roles, object kinds, dimensions, and overloads;
- sign-convention registries for FX quotes, CIP basis, yields, returns, SDFs,
  covariance symbols, and risk-neutral vs physical measures;
- lightweight dependency graph linking labels, assumptions, conventions,
  proof packets, code references, experiments, and citations;
- impact reports for convention or transform changes;
- manifest and registry lints against the LaTeX label/symbol index.

Manifest scope:

- scalar, vector, matrix, tensor, random variable, indexed process;
- shape and conformability;
- symmetry, SPD, triangularity, diagonality, invertibility;
- trace cyclicity and scalar objective status;
- differentiability, regularity, stationarity, ergodicity, admissibility;
- spectral-gap assumptions;
- conditioning, fixed-data masks, missing-data masks, and ragged edges;
- no-arbitrage, transversality, equilibrium, identification, and support
  restrictions.

Critical files:

- existing `src/mathdevmcp/assumptions.py`
- new `src/mathdevmcp/assumption_manifest.py`
- existing `src/mathdevmcp/notation.py`
- new `src/mathdevmcp/conventions.py`
- new `src/mathdevmcp/dependency_graph.py`
- `src/mathdevmcp/typed_workflows.py`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/review_packet.py`

Acceptance gates:

- audits distinguish missing assumptions from unsupported algebra;
- explicit assumptions are reported as used, missing, unused, or conflicting;
- SPD implies square/invertible only as a recorded assumption dependency;
- overloaded symbols are reported with source locations and convention context;
- a convention change can produce a list of labels and packets to re-audit.

### Phase 3: matrix and operator IR

Problem:

String-oriented normalization is too weak for noncommutative matrix calculus,
operator identities, stochastic expectations, and derivative obligations.

Deliverables:

- matrix/operator IR with dataclasses and validation;
- LaTeX-to-IR parser for a deliberately small grammar;
- object nodes for scalars, vectors, matrices, tensors, random variables,
  indexed processes, and unresolved constructs;
- operator nodes for `MatMul`, `Add`, `Scale`, `Transpose`, `Inv`, `Solve`,
  `Trace`, `Det`, `LogDet`, `QuadForm`, `Expectation`, `ConditionalExpectation`,
  `Derivative`, `Differential`, `Jacobian`, and `Hessian`;
- shape variables and conformability constraints;
- scalar-output markers and gradient orientation metadata;
- source spans for every subexpression where available;
- noncommutative rewrite diagnostics for standard identities.

First rewrite families:

- `d(A^{-1})`;
- `d log det A`;
- `d(x' A^{-1} x)`;
- trace cyclicity under explicit shape constraints;
- solve/inverse equivalence;
- Lyapunov and Sylvester derivative obligations;
- SVD/eigen spectral-gap denominator obligations;
- transform log-Jacobian identities.

Critical files:

- existing `src/mathdevmcp/math_ir.py`
- new or expanded `src/mathdevmcp/matrix_ir.py`
- `src/mathdevmcp/math_normalization.py`
- `src/mathdevmcp/proof_audit.py`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/typed_workflows.py`
- `src/mathdevmcp/shape_diagnostics.py`
- `src/mathdevmcp/implementation_audit.py`

Acceptance gates:

- ordered products such as `S^{-1}(dS)S^{-1}` are never flattened into
  commutative scalar strings;
- unsupported notation remains explicit in the IR;
- parser limits are separated from likely formula errors;
- every IR node can carry provenance or an explicit missing-provenance marker.

### Phase 4: proof packets, negative evidence, and numeric diagnostics

Problem:

Serious derivations need durable artifacts that show what was checked, what
was only diagnostic, what assumptions were used, and what remains open.

Deliverables:

- general `proof_packet_label(root, label, code?, manifest?, numeric_artifacts?)`;
- negative-evidence packet for mismatches, failed assumptions, counterexamples,
  and unsupported constructs;
- packet sections for source localization, assumption manifest, notation and
  convention context, IR, backend evidence, numeric evidence, code links,
  citations, dependency graph links, actions, and certification boundary;
- numeric diagnostic harness with seeded randomized checks;
- finite-difference and gradient/Hessian parity policies;
- tolerance, dtype, shape, seed, and artifact metadata;
- CLI `--output` support for durable packet files;
- compact MCP summary with full-packet expansion on request.

Critical files:

- `src/mathdevmcp/review_packet.py`
- new `src/mathdevmcp/proof_packet.py`
- new `src/mathdevmcp/negative_evidence.py`
- `src/mathdevmcp/numeric_diagnostics.py`
- `src/mathdevmcp/numeric_runner.py`
- `src/mathdevmcp/diagnostic_tests.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`

Acceptance gates:

- proof packets separate diagnostic evidence from certifying evidence;
- packets are stable JSON with schema version and redaction policy;
- randomized diagnostics are reproducible from packet metadata;
- a mismatch packet identifies whether the likely cause is formula error,
  normalization gap, missing assumption, parser limit, or backend failure.

### Phase 5: domain-template governance and first packs

Problem:

Many derivations recur across filtering, asset pricing, DSGE, HMC, transport,
and particle methods. Templates should decompose these derivations into smaller
obligations without becoming ungoverned domain sprawl.

Deliverables:

- declarative domain-template spec;
- template matcher based on label, section path, localized equation, notation,
  and optional manifest;
- `generate_obligations_from_template` API;
- `template_packet` section in proof packets;
- governance rule that every template declares:
  - assumptions;
  - supported notation;
  - generated obligations;
  - diagnostic routes;
  - failure modes;
  - positive fixtures;
  - negative fixtures;
  - certification boundary.

First-wave templates:

- Gaussian likelihood and Kalman prediction-error decomposition;
- solve-form logdet, inverse, and quadratic-form derivatives;
- Kalman prediction/update/Joseph/RTS/smoothing;
- Lyapunov and Sylvester equations;
- SVD/eigen derivative spectral-gap obligations;
- sigma-point mean/covariance identities;
- constrained transforms and log-Jacobian corrections;
- HMC leapfrog reversibility, volume preservation, and acceptance ratio;
- affine SDF and no-arbitrage Euler equations;
- affine Riccati bond-pricing recursions;
- FX forward, CIP basis, and sign-convention reconciliation;
- state-space observation stacking and missing-data masks.

Critical files:

- new `src/mathdevmcp/domain_templates.py`
- possible pack modules under `src/mathdevmcp/domain_packs/`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/typed_workflows.py`
- `src/mathdevmcp/review_packet.py`

Acceptance gates:

- long displayed derivations can be decomposed into named obligations;
- missing assumptions are template-specific;
- unsupported template notation returns a conservative substatus;
- templates never upgrade diagnostic evidence into proof.

### Phase 6: code-document traceability

Problem:

The monographs connect formulas to TensorFlow, TFP, XLA, custom linear algebra,
and experiments. Operation presence is not enough; implementation contracts
must include shape, dtype, batch axes, numerical safety, and finite target or
gradient behavior.

Deliverables:

- equation-to-code cross-reference index;
- operation manifests with required operations and forbidden unstable
  substitutes;
- AST operation graph coverage;
- tensor shape, dtype, batch-axis, and graph/eager consistency checks;
- XLA/custom-op boundary diagnostics;
- finite target and finite gradient smoke contracts;
- implementation links in proof packets;
- experiment-result links to labels and claims.

Critical files:

- `src/mathdevmcp/implementation_audit.py`
- `src/mathdevmcp/ast_operation_graph.py`
- `src/mathdevmcp/operation_consistency.py`
- `src/mathdevmcp/semantic_alignment.py`
- `src/mathdevmcp/kalman_workflows.py`
- `src/mathdevmcp/review_packet.py`

Acceptance gates:

- a formula-to-code packet can say which operations are present, missing, or
  suspicious;
- dtype, batch-axis, and finite-value risks are reported separately from
  mathematical proof status;
- custom-op boundaries are explicit and do not silently count as verified.

### Phase 7: Lean and backend readiness

Problem:

Formal checking is valuable but can be blocked by toolchain downloads, cache
isolation, timeouts, or confusion between direct Lean and LeanDojo readiness.

Deliverables:

- offline-friendly `lean_readiness`;
- no-network checks before any network-triggering behavior;
- separate direct Lean, Lake project, and LeanDojo statuses;
- tiny local theorem smoke check with timeout;
- backend readiness surfaced in `doctor` and release readiness;
- profile-specific guidance for base, backend, full, and private-corpus gates.

Critical files:

- `src/mathdevmcp/doctor.py`
- `src/mathdevmcp/lean_check.py`
- `src/mathdevmcp/lean_export.py`
- `src/mathdevmcp/leandojo_backend.py`
- `src/mathdevmcp/backend_env.py`
- `src/mathdevmcp/release_evidence.py`
- `src/mathdevmcp/release_profile_analysis.py`

Acceptance gates:

- Lean timeout is `inconclusive:backend_unavailable`;
- Lean proof rejection is `mismatch` only when Lean runs and rejects the exact
  supplied proof artifact;
- direct Lean, Lake, and LeanDojo readiness are reported separately;
- base/public profiles remain usable without strict Lean availability.

### Phase 8: literature and claim-support pack

Problem:

Finance and economics monographs contain claims whose support comes from
papers, data, or empirical regularities, not algebra alone. Citation support
must be useful while staying separate from proof.

Deliverables:

- claim-support packet beside proof packets;
- claim-status taxonomy:
  - exact identity;
  - theorem from cited source;
  - model assumption;
  - diagnostic evidence;
  - empirical regularity;
  - proposed extension;
  - open problem;
- theorem provenance from local paper summaries;
- literature conflict report;
- known limitation registry;
- review-status manifest for local paper summaries.

Critical files:

- `src/mathdevmcp/literature_gate.py`
- new `src/mathdevmcp/claim_support.py`
- `src/mathdevmcp/review_packet.py`
- dependency graph integration

Acceptance gates:

- citation evidence is never labeled as mathematical proof;
- claims can be linked to supporting papers, assumptions, labels, and packets;
- unsupported or conflicting literature claims produce negative-evidence or
  review-needed packets.

## Domain capability roadmap

The following packs should be developed after the core platform surfaces are
stable.

### Filtering and state-space pack

Capabilities:

- Kalman, square-root, SVD, UKF/CKF/GH, particle, and information-form filters;
- prediction-error decomposition;
- differentiable filtering and smoothing;
- missing-data masks, ragged-edge observations, and mixed-frequency release
  lag manifests;
- covariance, factor, Joseph, RTS, and Lyapunov update diagnostics;
- likelihood, score, Hessian, observed-information, and finite-gradient checks.

### Affine, CIP, SDF, and term-structure pack

Capabilities:

- SDF identities, Euler equations, and no-arbitrage replication templates;
- FX forward, CIP basis, quote convention, and sign reconciliation;
- affine state dynamics and Riccati recursions;
- AFNS yield curve and term-structure loading checks;
- risk-neutral versus physical measure transforms;
- continuous-to-discrete OU transition and covariance integrals;
- credit spread, default intensity, equity, mortgage, and MBS pricing recursions
  where relevant.

### DSGE and macro-perturbation pack

Capabilities:

- equilibrium-condition extraction;
- Euler equation, resource constraint, Taylor rule, and Epstein-Zin templates;
- steady-state consistency;
- log-linearization and second-order perturbation checks;
- QZ/Blanchard-Kahn determinacy diagnostics;
- Sylvester, Kronecker, and adjoint orientation checks;
- policy-rule, shock-process, ZLB, and shadow-rate support manifests.

### Bayesian posterior geometry, HMC, and transport pack

Capabilities:

- posterior decomposition into prior, likelihood, and transform Jacobian;
- constrained-parameter transforms and support-boundary diagnostics;
- MAP, Hessian, OPG, curvature, and mass-matrix checks;
- HMC/NUTS leapfrog invariance, volume preservation, and acceptance identity;
- position-dependent geometry obligations;
- transport-map change-of-variables, triangular logdet, force-matching, and
  score-matching templates;
- surrogate-vs-target and delayed-acceptance correction packets.

### Particle and optimal-transport pack

Capabilities:

- unbiased particle likelihood estimator templates;
- ESS and weight-degeneracy diagnostics;
- resampling differentiability and bias packets;
- EDH/LEDH/PFPF flow equations;
- particle-flow logdet/Jacobian ODE obligations;
- Sinkhorn marginal and entropy checks;
- PMMH versus particle-HMC correctness boundary;
- pseudo-posterior bias decomposition.

### Nonlinear dynamics and neural solver pack

Capabilities:

- stationarity, ergodicity, and filter-stability manifests;
- Foster-Lyapunov drift/minorization checklist;
- Lipschitz and spectral-norm bound extraction;
- contraction and invariant-distribution templates;
- neural solver Euler residual packets;
- approximation-vs-exact-correction boundaries;
- out-of-distribution residual diagnostics.

### Identification and empirical-design pack

Capabilities:

- identification assumption manifests;
- rank-condition, Fisher-information, and weak-identification diagnostics;
- normalization and rotation-invariance detection;
- prior-likelihood conflict reports;
- cointegration rank and error-correction templates;
- multi-country block-structure and hierarchical-restriction manifests;
- data-release calendars and measurement-system documentation packets;
- empirical design checklists linking theory to observable moments.

## Release and benchmark strategy

Benchmarks must check abstention quality, not just successful verification.

Required fixtures:

- small scalar identity that can be verified;
- matrix inverse differential positive fixture;
- logdet derivative positive fixture;
- quadratic-form derivative positive fixture;
- noncommutative product-order negative fixture;
- missing-assumption fixture;
- parser-limit fixture using multi-line `align`;
- likely-formula-error fixture;
- backend-unavailable fixture;
- large-root partial-index fixture;
- duplicate-label and overloaded-symbol fixture;
- CIP sign-convention fixture;
- Kalman likelihood score fixture;
- SVD/eigen spectral-gap fixture;
- transform log-Jacobian fixture;
- code-doc traceability fixture with shape/dtype/batch-axis issue;
- literature claim-support fixture that is not mathematical proof.

Gates:

- unit tests for core schemas and contracts;
- CLI/MCP contract-sync tests;
- parser localization regression tests;
- matrix-IR provenance tests;
- manifest lint tests;
- proof-packet schema tests;
- numeric diagnostic reproducibility tests;
- domain-template positive and negative tests;
- release-readiness profile tests.

## Milestones

### Milestone 1: Agent-usable abstentions

Scope:

- status taxonomy;
- compact payloads;
- next actions;
- schema metadata.

Success criteria:

- every non-verified result says what blocked certification and what to do
  next;
- agents can follow tool-suggested next actions without guessing.

### Milestone 2: Monograph-grade source handling

Scope:

- partial large-root indexing;
- equation localization;
- chapter cache shards;
- nearest-label lookup;
- notation and convention metadata v0.

Success criteria:

- CIP and DSGE roots remain searchable under partial failure;
- multi-line derivations can be split into source-localized obligations.

### Milestone 3: Assumption-aware matrix audit

Scope:

- assumption manifests;
- matrix/operator IR v1;
- shape and conformability diagnostics;
- first numeric diagnostic harness.

Success criteria:

- Kalman, logdet, quadratic-form, and transform derivative labels produce
  precise missing-assumption and parser-limit diagnostics;
- ordered products are preserved.

### Milestone 4: Durable evidence packets

Scope:

- proof packets;
- negative-evidence packets;
- dependency graph links;
- code links;
- compact MCP packet summaries.

Success criteria:

- a label audit emits a packet that separates proof, diagnostics, assumptions,
  missing work, and next actions.

### Milestone 5: First domain packs

Scope:

- filtering/state-space templates;
- affine/CIP/SDF templates;
- posterior-geometry/HMC templates;
- template governance.

Success criteria:

- common CIP, Kalman, and HMC derivations produce named obligation sets instead
  of generic human-review outputs.

### Milestone 6: Implementation-grade product surface

Scope:

- code-document traceability;
- Lean/backend readiness;
- literature claim-support packets;
- release and benchmark gates.

Success criteria:

- a coding or research agent can ask for a label audit and receive a compact
  report saying what is proven, what is diagnostic, what is missing, what code
  is implicated, and what command or edit should happen next.

## Near-term execution order

1. Add status taxonomy, schema metadata, and compact next-action summaries.
2. Add payload controls and CLI/MCP contract-sync tests.
3. Add equation localization and partial large-root indexing together.
4. Add assumption manifest parsing and manifest linting.
5. Add notation/convention metadata v0 and dependency-graph primitives.
6. Add matrix/operator IR v1 for ordered products, inverse, solve, trace,
   logdet, transpose, differentials, Jacobians, and expectations.
7. Add numeric diagnostic harness with reproducible finite-difference checks.
8. Add proof-packet and negative-evidence packet generation over existing v2
   audit output.
9. Add first-wave templates: Kalman/logdet/quadratic form, CIP/SDF, affine
   Riccati, HMC transform/leapfrog.
10. Add code-document traceability upgrades for shape, dtype, batch axes, and
    finite target or gradient gates.
11. Add Lean/backend readiness separation.
12. Add literature and claim-support packets.

## Risks and mitigations

- Overclaiming: preserve the product invariant and separate diagnostic from
  certifying evidence.
- Parser complexity creep: start with narrow equation environments and emit
  source-localized abstentions.
- Domain-template sprawl: require template specs, assumptions, failure modes,
  and positive/negative fixtures.
- Large payloads: use compact defaults and explicit debug expansion.
- Backend instability: keep backend evidence profile-scoped and classify
  unavailability as inconclusive.
- Private-corpus leakage: enforce redaction at packet and schema level.
- False confidence from numeric checks: record seeds, tolerances, dtype, and
  mark numeric results diagnostic unless a certifying backend proves the exact
  obligation.

## Done definition

This implementation plan is complete when MathDevMCP can take a label from a
large macro-finance or economics monograph, locate the relevant equation
precisely, classify the domain, build typed matrix/domain obligations, apply
explicit assumptions and conventions, run available deterministic and
diagnostic checks, compare relevant code, link supporting claims or citations,
and emit a compact proof or negative-evidence packet that an agent can act on
without confusing diagnostic evidence for proof.
