# MathDevMCP macro-finance product roadmap

## Purpose

This plan records a product review of MathDevMCP after using it on real
BayesFilter, DSGE, and CIP-monograph workflows.  The review agrees with the
main suggestions in `/home/chakwong/python/docs/plans/mathdevmcp-improvement-suggestions.md`:
the tool is valuable because it refuses to over-certify, but its abstentions
need to become more actionable for matrix calculus, large LaTeX roots, and
macro-finance/economics workflows.

The plan has two goals:

1. address the seven shortcomings identified in the review;
2. define the broader capability list needed for future mathematical finance
   and economics projects like `/home/chakwong/latex/CIP_monograph/main.tex`
   and `/home/chakwong/python/docs/monograph.tex`.

The source review in this plan uses the corrected CIP monograph path
`/home/chakwong/latex/CIP_monograph/main.tex` and the DSGE monograph path
`/home/chakwong/python/docs/monograph.tex`.

## Current evidence

The current repo already contains useful foundations:

- `math_ir.py`, `typed_obligation_label`, `audit_derivation_v2_label`,
  `shape_diagnostics`, `numeric_diagnostics`, `review_packet`, and
  `lean_check`;
- parser and benchmark gates with line-level provenance on release fixtures;
- conservative statuses: `verified`, `unverified`, `mismatch`, and
  `inconclusive`;
- release profiles that keep backend/Lean/LaTeXML/private-corpus evidence
  profile-scoped.

Live checks during the review showed:

- base `release_readiness` is `ready_with_caveats`;
- SymPy, Sage, LaTeXML, and LeanDojo are available in the current environment;
- direct Lean is unavailable because `lean --version` timed out;
- a Kalman score audit on `eq:kalman-innovation-score-local` correctly
  abstained and reported missing differentiability, invertibility,
  square-matrix, trace, and conformability assumptions.

This means the gap is not "build all diagnostics from nothing."  The gap is to
turn existing heuristic scaffolding into a product-quality mathematical
verification workflow.

## Source-document scope reviewed

The corrected CIP monograph at `/home/chakwong/latex/CIP_monograph/main.tex`
is titled `Asset Pricing with CIP Deviations`.  Its document spine includes:

- foundations: CIP derivation, multi-period CIP, cross-currency basis,
  theoretical foundations, SDFs, market completeness, paradoxes, and
  literature;
- affine benchmark model: state dynamics and SDFs, AFNS yield curves, FX basis,
  equity/credit pricing, mortgage/MBS pricing, state-space recursions, and
  identification;
- nonlinear extensions: stochastic volatility, regime switching, nonlinear
  drift, stationarity/ergodicity, neural asset-pricing solvers, and nonlinear
  pricing;
- filtering and likelihood: Kalman filtering, nonlinear filters,
  mixed-frequency estimation, differentiable particle filters, LEDH/PFPF,
  neural optimal transport, differentiable resampling, and analytical
  validation;
- Bayesian estimation: priors, Gibbs, HMC, advanced HMC, and HNN surrogates;
- structural extensions: macro augmentation, multi-country models,
  macro-finance endpoints, ZLB/shadow-rate models, cointegration,
  hybrid cointegrated nonlinear systems, pipeline synthesis, empirical design,
  and LLM-assisted research;
- appendices: notation, derivations, code cross-reference, affine computation,
  TensorFlow/TFP design, MCP cookbook, and practical identification.

The DSGE monograph at `/home/chakwong/python/docs/monograph.tex` is titled
`Bayesian Estimation of DSGE Models`.  Its document spine includes:

- foundations: constrained dynamic optimization, Euler equations, AR(1),
  log-linearization, Kronecker products, Bayes' theorem, MCMC, neural networks,
  Latin hypercube sampling, multi-objective optimization, and eigendecomposition
  / matrix square roots;
- DSGE models: New Keynesian, Epstein-Zin NK, and SGU models;
- solution methods: perturbation methods and neural solvers;
- filtering and likelihood: Kalman filters, square-root UKF, SVD filters, and
  stationarity/ergodicity;
- Bayesian estimation: constrained transforms, MAP/posterior geometry, mass
  matrix estimation, HMC, position-dependent geometry, transport foundations,
  neural transport literature, transport training, and advanced HMC;
- implementation and experiments: XLA/custom ops, experiments, code xrefs,
  pitfalls, detailed code documentation, and numerical-stability failures.

The two documents therefore exercise a product surface far wider than filtering:
large-root LaTeX indexing, notation governance, no-arbitrage/SDF algebra,
affine/Riccati pricing, structural macro equilibrium, perturbation and
linear-algebra adjoints, nonlinear stationarity, posterior geometry, HMC,
transport maps, particle methods, optimal transport, identification, empirical
design, code traceability, and literature support.

## Product invariant

MathDevMCP must stay conservative.

No parser output, AST match, inferred type, shape hint, route hint, numeric
diagnostic, assumption manifest, domain template, generated proof packet, or
Lean environment check may become a verified mathematical claim unless a
deterministic backend verifies the exact scoped obligation under explicit
assumptions and the result records reproducible evidence.

## Seven-shortcoming remediation plan

### 1. Matrix-calculus IR

Current issue:

The present IR is useful but mostly regex/heuristic.  It detects unresolved
constructs such as derivatives, inverses, traces, determinants, and transposes,
but it does not preserve noncommutative matrix expression structure well enough
for serious matrix-calculus derivations.

Target product behavior:

MathDevMCP should parse scoped obligations into a noncommutative matrix IR with
explicit nodes for:

- scalars, vectors, matrices, random variables, and indexed processes;
- `MatMul`, `Add`, `Scale`, `Transpose`, `Inv`, `Solve`, `Trace`, `Det`,
  `LogDet`, `QuadForm`, `Expectation`, `Derivative`, `Differential`, and
  `Jacobian`;
- shape variables and conformability constraints;
- scalar-output status;
- provenance for every subexpression.

Execution slices:

1. Add `matrix_ir.py` with dataclasses and validation.
2. Add a LaTeX-to-matrix-IR normalizer for a small grammar:
   inverse, transpose, trace, logdet, quadratic forms, and differentials.
3. Add noncommutative rewrite rules as diagnostic obligations, not automatic
   proof upgrades:
   `d(A^{-1})`, `d log det A`, `d(x' A^{-1} x)`, trace cyclicity under shape
   constraints, and solve/inverse equivalence.
4. Add a matrix-IR route in `audit_derivation_v2_label`.
5. Add fixtures from Kalman likelihood score, SVD sigma-point derivatives, and
   transform log-Jacobian derivatives.

Acceptance gates:

- The parser preserves `dS S^{-1}` and `S^{-1}(dS)S^{-1}` as ordered products.
- Noncommutative products are never flattened into commutative scalar strings.
- Unsupported notation returns `unverified:unsupported_noncommutative_algebra`
  with a proof obligation and source span.

### 2. Assumption manifests

Current issue:

Assumptions are inferred from prose and symbol names.  That is acceptable for
triage, but not enough for real matrix calculus, SDF pricing, or posterior
geometry.

Target product behavior:

Every label-level audit can accept or discover an adjacent manifest:

```yaml
objects:
  S_t:
    kind: matrix
    shape: [m, m]
    symmetric: true
    positive_definite: true
  v_t:
    kind: vector
    shape: [m]
  theta_i:
    kind: scalar
rules:
  - inverse_differential
  - logdet_differential
  - trace_cyclicity
  - scalar_objective_gradient
domains:
  - kalman_likelihood
```

Execution slices:

1. Add an `assumption_manifest.py` parser and schema validator.
2. Let `typed_obligation_label`, `audit_derivation_v2_label`, and
   `implementation_brief` accept `assumption_manifest`.
3. Report `used_assumptions`, `missing_assumptions`, `unused_assumptions`, and
   `assumption_conflicts`.
4. Support document-local manifests by convention:
   `main.assumptions.yml`, `chapter.assumptions.yml`, and
   `label.assumptions.yml`.
5. Add a manifest linter that checks symbols against the LaTeX label index.

Acceptance gates:

- Audits distinguish "not stated" from "stated but not used."
- SPD implies square/invertible where mathematically appropriate, but this is
  recorded as an assumption dependency.
- Conflicting declarations, such as scalar and matrix for the same symbol, are
  blockers for certification.

### 3. Proof packet generation

Current issue:

`review_packet` exists, but serious derivations need a durable, label-centered
artifact that combines document, assumptions, IR, backend evidence, numeric
evidence, and remaining proof gaps.

Target product behavior:

Add `proof_packet_label` as a CLI/MCP workflow that emits a JSON artifact:

- source root, file, label, line span, section path;
- proposition/equation statement;
- normalized matrix IR;
- assumption manifest and used/missing assumptions;
- parser policy and source-localization evidence;
- symbolic/Sage/Z3/Lean results when available;
- randomized numeric or finite-difference checks when supplied;
- implementation-audit links when code is supplied;
- high-priority actions;
- certification boundary.

Execution slices:

1. Generalize `review_packet.py` beyond likelihood implementation audits.
2. Add `proof_packet_label(root, label, code?, manifest?, numeric_artifacts?)`.
3. Add `--output` support in the CLI for durable packet files.
4. Add compact MCP summaries by default and full packet output on request.
5. Add release fixtures for a verified scalar identity, an unverified Kalman
   score, and a mismatch case.

Acceptance gates:

- The packet is stable JSON with schema metadata.
- Diagnostic evidence and certifying evidence are separated.
- The packet can be attached to BayesFilter/CIP derivative chapters without
  exposing private paths by default.

### 4. Domain obligation templates

Current issue:

Filtering templates exist only in fragments.  The monographs require templates
for asset pricing, macro equilibrium, posterior geometry, particle methods,
transport maps, and no-arbitrage identities.

Target product behavior:

Domain templates should split long derivations into small obligations with
known assumption needs and safe diagnostic routes.

Initial templates:

- Gaussian likelihood and Kalman prediction-error decomposition;
- logdet, solve, inverse, and quadratic-form derivatives;
- Kalman prediction/update, Joseph update, smoothing, and Lyapunov equations;
- SVD/eigen derivative spectral-gap obligations;
- sigma-point moment mean/covariance identities;
- HMC leapfrog reversibility, volume preservation, and acceptance ratio;
- constrained-parameter transforms and log-Jacobian corrections;
- affine SDF and no-arbitrage Euler equations;
- affine bond-pricing Riccati recursions;
- FX forward, CIP basis, and sign-convention reconciliation;
- state-space observation stacking and measurement-error masks;
- particle-filter unbiased likelihood, ESS, resampling bias, and flow
  logdet/Jacobian obligations;
- neural transport transformed-density and force-matching identities.

Execution slices:

1. Add `domain_templates.py` with declarative template specs.
2. Add a template matcher that suggests templates from labels and section path.
3. Add a `generate_obligations_from_template` API.
4. Add a `template_packet` section to proof packets.
5. Add seeded positive and negative fixtures for each first-wave template.

Acceptance gates:

- Templates reduce a long displayed derivation into named obligations.
- Missing assumptions are specific to the template.
- Template output is diagnostic until each obligation is backend-certified.

### 5. Large-LaTeX indexing robustness

Current issue:

Large monograph roots should not lose all search or label capability because
one file, include, macro, or backend fails.  Tool responses can also become too
large for agent use.

Target product behavior:

The LaTeX indexer should produce partial indexes with structured diagnostics:

- parsed files, failed files, skipped files, include graph, macro summary;
- duplicate-label findings;
- chapter-level indexes;
- label-neighborhood search;
- nearest-label-by-topic suggestions;
- compact default MCP payloads with optional debug expansion.

Execution slices:

1. Change index building from all-or-nothing to partial result plus findings.
2. Add per-file parser failure records and source excerpts.
3. Add chapter-level cache shards and invalidation by file hash.
4. Add "nearest labels" retrieval using lexical and section-path scoring.
5. Add payload controls: `summary_only`, `include_parser_report`, and
   `max_diagnostics`.

Acceptance gates:

- One broken chapter does not prevent lookup in unrelated chapters.
- Large-root search returns useful partial results and actionable failed-file
  diagnostics.
- Default `audit_derivation_v2_label` output is concise enough for MCP agents.

### 6. Failure taxonomy and next actions

Current issue:

Top-level statuses are good, but agents need substatus and runnable next
actions.

Target product behavior:

Keep stable top-level statuses, and add substatus:

- `unverified:missing_assumption`;
- `unverified:parser_limit`;
- `unverified:unsupported_noncommutative_algebra`;
- `unverified:manual_formalization_required`;
- `mismatch:likely_formula_error`;
- `mismatch:normalization_gap`;
- `inconclusive:backend_unavailable`;
- `inconclusive:source_label_missing`;
- `inconclusive:partial_index_only`.

Execution slices:

1. Add `status_taxonomy.py` with allowed substatuses and severity.
2. Update proof-audit v2, typed obligation, proof packet, and implementation
   audit to emit `status`, `substatus`, `reason`, and `actions`.
3. Add next-action suggestions that are command-shaped but safe:
   add manifest, split derivation row, inspect normalized expression, run
   Sage numeric check, run finite-difference check, or write Lean lemma.
4. Add tests for common failure modes.

Acceptance gates:

- Every non-verified result has at least one actionable next step.
- Backend/environment failures do not masquerade as formula mismatches.
- Likely formula errors are distinguished from parser normalization gaps.

### 7. Offline-friendly Lean readiness

Current issue:

Direct Lean checking is valuable, but the active environment can fail because
of toolchain downloads, cache isolation, or timeouts.  LeanDojo readiness is a
different question from direct Lean readiness.

Target product behavior:

Add `lean_readiness`:

- locate Lean without triggering network work when possible;
- report active toolchain and whether it is locally installed;
- compile a tiny theorem with a timeout;
- classify direct Lean, Lake project, and LeanDojo separately;
- provide profile-specific guidance for base/backend/full release checks.

Execution slices:

1. Add a `lean_readiness.py` module and CLI/MCP exposure.
2. Use no-network checks first: executable path, `lean-toolchain`, local elan
   toolchain cache, and tiny theorem.
3. Separate `direct_lean`, `lake_project`, and `lean_dojo` status.
4. Update `doctor`, `release_readiness`, and support-matrix docs to reference
   the readiness report.

Acceptance gates:

- A Lean timeout is `inconclusive:backend_unavailable`.
- A Lean proof rejection is `mismatch` only when Lean runs and rejects the
  supplied proof artifact.
- Base/public profiles remain usable without strict Lean.

## Wider product list for mathematical finance and economics

The two monographs show that future work needs a broader product surface than
filtering.  The corrected CIP monograph covers no-arbitrage/SDF foundations,
CIP basis sign conventions, affine pricing, AFNS yield curves, FX basis,
equity/credit/MBS pricing, state-space recursions, identification, nonlinear
dynamics, neural solvers, Kalman and nonlinear filters, mixed-frequency data,
differentiable particle flows, neural optimal transport, Bayesian/HMC
estimation, HNN surrogates, macro augmentation, multi-country models, ZLB,
shadow rates, cointegration, hybrid nonlinear systems, and end-to-end research
pipelines.  The DSGE monograph covers microfoundations, Euler equations,
Epstein-Zin preferences, SGU perturbation, neural solvers, Kalman/SR-UKF/SVD
filters, stationarity, constrained transforms, MAP/posterior geometry, mass
matrices, HMC/NUTS, position-dependent geometry, transport maps, XLA/custom
linear algebra, and numerical-stability failures.

To make future work like this easier, MathDevMCP should grow these capability
families.

### A. Notation and convention management

Needed because cross-chapter sign and symbol reuse errors are common in large
finance monographs.

Capabilities:

- notation index across LaTeX roots;
- symbol role manifests;
- sign-convention registry for FX quotes, CIP basis, yields, returns, SDFs,
  and covariance symbols;
- duplicate and overloaded symbol detection;
- convention-change impact report by label dependency graph.
- chapter-to-chapter consistency checks for objects like `S_t`, `M`,
  `lambda`, `K`, and `r`, which are heavily overloaded in the CIP notation
  appendix.

Useful templates:

- domestic/foreign quote convention;
- model-vs-market CIP basis convention;
- gross-vs-log return convention;
- annualized-vs-periodic yield convention;
- risk-neutral-vs-physical measure notation.

### B. No-arbitrage and SDF reasoning

Needed for CIP, asset pricing, term-structure, exchange-rate, equity, and
credit chapters.

Capabilities:

- Euler-equation obligation templates;
- SDF positivity and pricing-kernel domain checks;
- no-arbitrage replication checks;
- measure-change and Radon-Nikodym derivative templates;
- complete vs incomplete market assumption tracking;
- martingale and transversality condition checklist;
- lognormal convexity adjustment checks.
- convention-aware CIP basis formulas that know whether positive basis means
  scarce dollar funding or the opposite market quote.

Useful templates:

- SDF ratio exchange-rate identity;
- CIP from SDF/no-arbitrage;
- forward-premium decomposition;
- stochastic discount factor lognormal moment identity;
- Hansen-Jagannathan style moment bound diagnostics.

### C. Affine and term-structure model support

Needed for AFNS, yields, credit spreads, foreign bonds, dividend strips, and
macro-finance endpoints.

Capabilities:

- affine state-dynamics templates;
- continuous-to-discrete OU transition and covariance checks;
- Riccati recursion and ODE obligation templates;
- bond, coupon, par-yield, credit, and FX forward pricing recursions;
- risk-neutral/physical measure transform checks;
- Novikov and integrability diagnostics.
- discrete-time and continuous-time bridge checks for state dynamics,
  covariance integrals, and Riccati equations.

Useful templates:

- matrix exponential transition;
- discrete covariance integral;
- affine bond-price recursion;
- continuous-time Riccati-to-discrete recursion;
- yield-from-price sign check;
- credit spread and default intensity decomposition.

### D. Structural macro equilibrium and perturbation

Needed for NK, Epstein-Zin, SGU, policy rules, and macro-finance models.

Capabilities:

- Euler equation and resource constraint extraction;
- steady-state equation consistency checks;
- log-linearization and second-order expansion templates;
- QZ/Blanchard-Kahn determinacy diagnostics;
- Sylvester and Kronecker derivative templates;
- policy-rule and shock-process transform manifests.
- adjoint orientation checks for SGU/Sylvester derivatives and custom
  linear-algebra code paths.

Useful templates:

- household Euler equation;
- NK Phillips curve residual;
- Taylor rule with shock;
- Epstein-Zin SDF;
- first-order state-space solution;
- second-order perturbation tensor shape checks.

### E. State-space, filtering, and likelihood

Needed but not sufficient by itself.

Capabilities:

- linear Gaussian state-space templates;
- Kalman, square-root, SVD, UKF/CKF/GH, particle, and mixed-frequency filter
  templates;
- missing-data and ragged-edge observation masks;
- prediction-error decomposition;
- likelihood, score, Hessian, and observed-information obligations;
- finite-safe target and gradient contracts.
- mixed-frequency release-lag and ragged-edge observation manifests.

Useful templates:

- Kalman prediction/update/Joseph/RTS;
- solve-form log likelihood;
- innovation score and Hessian terms;
- SVD sigma-point generation;
- missing-data masked observation update;
- mixed-frequency aggregation and release-lag mapping.

### F. Nonlinear dynamics, stationarity, and ergodicity

Needed for neural state dynamics, stochastic volatility, regime switching,
threshold dynamics, and nonlinear filters.

Capabilities:

- Foster-Lyapunov drift-condition checklist;
- Markov kernel and transition-density diagnostics;
- Lipschitz and spectral-norm bound extraction;
- geometric ergodicity and filter-stability assumption manifests;
- stationary initialization templates.
- neural-network Lipschitz policy checks for hard constraints, soft penalties,
  and post-hoc verification.

Useful templates:

- contraction mapping condition;
- residual-network Lipschitz bound;
- drift/minorization checklist;
- invariant distribution statement;
- filter-stability-to-loglik convergence chain.

### G. Bayesian posterior geometry and HMC

Needed for MAP, mass matrix, NUTS/HMC, position-dependent geometry, and
transport-preconditioned inference.

Capabilities:

- constrained transform and log-Jacobian templates;
- posterior decomposition into prior, likelihood, and Jacobian;
- gradient/Hessian chain-rule packets;
- mass-matrix and quadratic-fit diagnostics;
- HMC leapfrog invariance templates;
- NUTS and warmup diagnostic contracts;
- finite target/finite gradient boundary tests.
- boundary-aware diagnostics for Blanchard-Kahn, ZLB, stationarity,
  positive-definiteness, and transform-support failures.

Useful templates:

- transformed density and potential;
- log-Jacobian correction;
- Hessian-at-MAP approximation;
- OPG and gradient-regression checks;
- leapfrog reversibility/volume preservation;
- acceptance probability identity.

### H. Neural solvers and transport maps

Needed for nonlinear pricing, NeuTra, OT-Flow, self-normalizing flows, neural
optimal transport, and surrogate HMC.

Capabilities:

- transformed-density and inverse-map templates;
- logdet/Jacobian trace identities;
- force-matching and score-matching obligations;
- Euler-residual neural-solver templates;
- approximation-vs-exact-correction boundary;
- out-of-distribution and residual diagnostics.
- HNN/delayed-acceptance surrogate packets that separate approximate proposal
  evidence from exact posterior correction evidence.

Useful templates:

- change-of-variables density;
- triangular/coupling logdet;
- OT-Flow HJB residual;
- neural solver Euler residual;
- delayed-acceptance HMC correction;
- surrogate error and acceptance-bound packet.

### I. Particle methods and optimal transport

Needed for differentiable particle filters, LEDH/PFPF, Sinkhorn resampling,
and particle HMC.

Capabilities:

- unbiased likelihood estimator template;
- ESS and weight-degeneracy diagnostics;
- resampling differentiability/bias templates;
- homotopy and continuity-equation obligations;
- particle-flow logdet/Jacobian ODE templates;
- Sinkhorn shape, marginal, and entropy checks.
- particle-HMC and pseudo-posterior bias packets that record what remains exact
  and what is biased by finite particles, soft resampling, or neural OT.

Useful templates:

- bootstrap particle likelihood;
- EDH/LEDH flow equations;
- flow mass preservation;
- OT resampling plan constraints;
- pseudo-posterior bias decomposition;
- PMMH vs PHMC correctness boundary.

### J. Econometric identification and data design

Needed for weak identification, prior sensitivity, macro-finance endpoints,
multi-country panels, ZLB, and cointegration.

Capabilities:

- identification assumption manifests;
- rank-condition and Fisher-information diagnostics;
- normalization and rotation-invariance detection;
- prior-likelihood conflict reports;
- cointegration rank and error-correction templates;
- mixed-frequency and data-release calendar manifests.
- multi-country block-structure and hierarchical-restriction manifests.

Useful templates:

- affine rotation invariance;
- weak-identification ridge;
- Fisher information loss under ZLB;
- cointegration rank condition;
- panel block-structure restrictions;
- prior sensitivity and posterior concentration packet.

### K. Code-document traceability

Needed because the monographs connect formulas to TensorFlow/TFP/XLA code and
custom linear algebra.

Capabilities:

- equation-to-code xref index;
- required operation manifests;
- AST operation graph coverage;
- shape and dtype policy checks;
- XLA/custom-op boundary diagnostics;
- finite-value and finite-gradient smoke contracts.
- TensorFlow/TFP shape, dtype, batch-axis, and graph/eager consistency checks.

Useful templates:

- `logdet` must be implemented as solve/Cholesky/SVD-safe operation;
- covariance update must preserve PSD/Symmetry;
- QZ/Sylvester adjoint orientation;
- column-major vs row-major vectorization;
- stable fallback for invalid HMC proposals.

### L. Literature and citation support

Needed because future finance/economics monographs rely on many claims whose
status depends on the literature, not only algebra.

Capabilities:

- claim-to-citation support packets;
- theorem provenance from cited papers;
- literature conflict report;
- known limitation registry;
- review-status manifest for local paper summaries.
- claim-status taxonomy for exact identity, assumption, diagnostic evidence,
  empirical regularity, proposed extension, and open problem.

Useful templates:

- "this theorem is standard and cited";
- "this claim is a model assumption, not a proven fact";
- "this extension is a proposed research direction";
- "this empirical regularity needs data evidence."

## Product milestones

### Milestone 1: Usable proof packets for matrix likelihoods

Scope:

- matrix-calculus IR v1;
- assumption manifests v1;
- proof packets v1;
- Kalman/logdet/quadratic-form templates.

Success criteria:

- BayesFilter Kalman derivative labels produce concise packets with exact
  missing assumptions and next actions.
- SVD sigma-point derivative cases no longer fail because ordered products are
  flattened.

### Milestone 2: Large-monograph reliability

Scope:

- partial LaTeX indexing;
- chapter cache shards;
- nearest-label search;
- compact MCP payloads;
- notation and convention index v1.

Success criteria:

- CIP and DSGE monograph roots can be searched even if one chapter fails.
- Cross-chapter sign and notation risks are surfaced as review findings.

### Milestone 3: Macro-finance domain templates

Scope:

- SDF/no-arbitrage templates;
- affine/Riccati templates;
- structural macro/perturbation templates;
- posterior geometry/HMC templates.

Success criteria:

- CIP SDF/CIP basis and DSGE Euler/HMC chapters produce named obligation sets
  instead of generic "human review" outputs.

### Milestone 4: Implementation-grade product surface

Scope:

- proof-packet CLI/MCP;
- status taxonomy;
- next-action suggestions;
- Lean readiness;
- code-document traceability upgrades.

Success criteria:

- A coding agent can ask for a label audit and receive a compact packet that
  says what is proven, what is diagnostic, what is missing, and what command or
  edit should happen next.

## Near-term execution order

1. Add status taxonomy and compact next-action summaries.
2. Add proof-packet generation over existing v2 audit output.
3. Add assumption manifest parsing and route it into typed diagnostics.
4. Add matrix-IR v1 for ordered products, inverse, trace, logdet, transpose,
   and differentials.
5. Add Kalman/logdet/quadratic-form templates.
6. Add partial large-root indexing and concise MCP payload controls.
7. Add Lean readiness.
8. Add macro-finance templates in waves: SDF/CIP, affine/Riccati, structural
   macro, HMC/transport, particle/OT.

## Risks

- Overclaiming: mitigated by the product invariant and explicit certification
  boundary.
- Parser complexity creep: mitigated by small grammar slices and
  source-localized abstention.
- Domain-template sprawl: mitigated by template manifests and benchmark
  fixtures for each supported template.
- Large payloads: mitigated by compact defaults and debug expansion flags.
- Backend instability: mitigated by profile-scoped Lean/Sage/LaTeXML readiness.

## Done definition

This roadmap is complete when MathDevMCP can take a label from a large
macro-finance monograph, locate it reliably, classify the mathematical domain,
build a typed matrix/domain obligation set, apply explicit assumptions,
run available deterministic and diagnostic checks, compare relevant code, and
emit a compact proof packet that a research agent can act on without confusing
diagnostic evidence for proof.
