# MathDevMCP improvement review and product plan

## Context

This plan responds to field-use feedback in `/home/chakwong/python/docs/plans/mathdevmcp-improvement-suggestions.md`. The review is credible because it praises the same thing MathDevMCP is designed to protect — conservative abstention — while identifying where real work still becomes brittle: matrix calculus, large-monograph indexing, assumption handling, actionable failures, proof packaging, and reusable domain workflows.

The immediate goal is not to make MathDevMCP more aggressive. The goal is to make it more useful while preserving the current proof boundary:

- diagnostic evidence is not proof,
- missing assumptions should surface explicitly,
- backend unavailability should not collapse into opaque failure,
- large-document use should degrade gracefully rather than fail monolithically.

This plan addresses the seven highest-value shortcomings from the review and then extends the roadmap to the broader mathematical-finance and economics workflows implied by:

- `/home/chakwong/latex/CIP_monograph/main.tex`
- `/home/chakwong/python/docs/monograph.tex`

The corrected CIP monograph path matters because its structure makes clear that the future scope is much broader than filtering. Together, the two monographs span:

- asset pricing and CIP basis structure,
- affine benchmark models and no-arbitrage pricing recursions,
- nonlinear dynamics and neural solvers,
- filtering, mixed-frequency systems, and differentiable particle methods,
- Bayesian estimation, HMC, transport, and surrogate geometry,
- macro/DSGE structure, identification, and empirical design,
- monograph-scale code/document/derivation traceability.

This amended plan should be read alongside the more finance-specific roadmap in [mathdevmcp-macrofinance-product-roadmap-2026-05-04.md](mathdevmcp-macrofinance-product-roadmap-2026-05-04.md). The present document is the product-review response and prioritization layer; the roadmap document contains the deeper macro-finance expansion picture.

## Review judgment

The review suggestions are valid overall.

Most valid and highest-priority:

1. matrix-calculus IR,
2. assumption manifests,
3. large-LaTeX robustness,
4. failure taxonomy plus next-action suggestions.

Also valuable but dependent on the above:

5. proof packet generation,
6. domain obligation templates,
7. offline-friendly Lean readiness mode.

The central product insight is correct: MathDevMCP should not claim more certainty; it should turn each abstention into a more precise proof obligation with explicit assumptions, source labels, and next verification steps.

## Product direction

### What to preserve

- conservative top-level statuses,
- explicit provenance,
- separation between parser evidence, symbolic evidence, numeric evidence, and formal proof,
- thin CLI/MCP adapters over shared library logic,
- benchmark-driven false-confidence control.

### What to improve

- richer internal representation for matrix and operator calculus,
- stronger assumption handling,
- robust large-root indexing behavior,
- better failure explanations and next actions,
- reusable proof packets and domain templates,
- readiness checks for formal backends that do not depend on fragile network/toolchain state,
- first-class notation and sign-convention management,
- explicit claim/assumption dependency tracking,
- cleaner separation between core platform capabilities and domain-specific packs,
- literature/citation support for monograph-scale claims.

## Platform decomposition

To keep the product maintainable, split future work into two layers.

### Core platform

The reusable platform should own:

- contracts and status/substatus taxonomy,
- matrix/operator IR,
- assumption manifests,
- large-root indexing and cache/shard logic,
- proof packets and negative-evidence packets,
- notation/sign-convention registry primitives,
- dependency-graph infrastructure,
- backend readiness and capability diagnostics.

### Domain packs

Domain packs should build on the core and remain optional:

- filtering/state-space pack,
- affine/CIP/SDF/term-structure pack,
- DSGE/macro-perturbation pack,
- HMC/transport/posterior-geometry pack,
- particle/optimal-transport pack,
- literature/citation-support pack.

This split reduces the risk that MathDevMCP becomes a monolithic macro-finance codebase rather than a maintainable verification/orchestration tool.

## Workstream 0: notation, convention, and dependency graph infrastructure

### Problem

Large finance monographs are unusually vulnerable to errors caused by overloaded symbols, silent sign-convention changes, chapter-to-chapter notation drift, and hidden assumption dependencies. These are not secondary documentation issues; they directly affect whether downstream derivations are interpreted correctly.

### Deliverable

Add first-class infrastructure for:

- notation registries,
- sign-convention registries,
- claim/assumption dependency graphs,
- impact tracing when notation, transforms, or conventions change.

The initial scope should support at least:

- FX quote conventions,
- CIP basis model-vs-market sign conventions,
- yield/return annualization conventions,
- risk-neutral vs physical measure notation,
- overloaded symbols across chapters,
- label-to-assumption and label-to-label dependency links.

### Approach

1. Add a notation/convention schema that can be attached to chapters or labels.
2. Add a lightweight dependency-graph representation linking:
   - labels,
   - assumptions,
   - conventions,
   - proof packets,
   - code references.
3. Surface impact reports such as:
   - which labels depend on a convention,
   - which obligations use a symbol in multiple roles,
   - what must be re-audited after a notation or transform change.
4. Keep this diagnostic; it must not claim mathematical validity by itself.

### Critical files

- new notation/convention module(s)
- new dependency-graph module(s)
- `src/mathdevmcp/latex_index.py`
- `src/mathdevmcp/review_packet.py`
- `src/mathdevmcp/_workflow_rules.py`

### Acceptance hypotheses

- H0.1: the tool can detect and report cross-chapter notation/convention reuse risks.
- H0.2: proof packets and claims can be linked to assumptions and conventions through a stable graph.
- H0.3: sign-convention changes can trigger actionable re-audit suggestions without pretending to re-prove anything.

## Workstream 1: matrix-calculus IR

### Problem

Current token/text-oriented normalization is too fragile for noncommutative matrix products and differential identities. Real derivations such as inverse differentials, logdet identities, solve-form derivatives, Kalman/SVD updates, affine pricing recursions, and HMC transport Jacobians need object-level structure.

### Deliverable

Introduce a small matrix-calculus IR that preserves:

- ordered noncommutative products,
- differentials (`dS`, `dP`, `dF`, etc.),
- transpose,
- inverse / solve,
- trace,
- scalar-objective markers,
- shape variables,
- symmetry / SPD / triangular / diagonal annotations,
- expectations and conditional-expectation markers where feasible,
- unresolved constructs.

### Approach

1. Add a new IR module rather than forcing this into string normalization.
2. Start with a narrow operator set sufficient for:
   - inverse differential,
   - log determinant,
   - quadratic forms,
   - trace identities,
   - Kalman covariance/innovation recursions,
   - SVD/eigen denominator structure,
   - affine pricing and transform Jacobian identities.
3. Keep unsupported algebra explicit in the IR rather than guessing.

### Critical files

- `src/mathdevmcp/` new IR module(s)
- `src/mathdevmcp/proof_audit.py`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/typed_workflows.py`
- `src/mathdevmcp/implementation_audit.py`

### Acceptance hypotheses

- H1: expressions like `d(S^{-1}) = -S^{-1}(dS)S^{-1}` can be represented without collapsing product order.
- H2: mismatch vs parser-limit can be separated for standard matrix differential identities.
- H3: the IR improves audit precision without weakening the abstention boundary.

## Workstream 2: assumption manifests

### Problem

For matrix and macro-finance derivations, missing assumptions are often the real issue. Today they are too easy to leave as prose.

### Deliverable

Support adjacent assumption manifests attached to labels, sections, or proof packets.

Manifest scope should cover:

- shape and conformability,
- scalar/vector/matrix/tensor type,
- symmetry / SPD / invertibility,
- trace cyclicity,
- fixed-data / conditioning masks,
- spectral-gap assumptions,
- stationarity / ergodicity / admissibility conditions,
- differentiability and regularity assumptions,
- no-arbitrage, transversality, and equilibrium restrictions where relevant.

### Approach

1. Define a minimal machine-readable manifest format first.
2. Add parser support for locating adjacent manifests or sidecar files.
3. Make audits report:
   - assumptions consumed,
   - assumptions missing,
   - assumptions irrelevant,
   - assumptions inconsistent with the statement.

### Critical files

- new assumption schema/parser module(s)
- `src/mathdevmcp/typed_workflows.py`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/review_packet.py`
- workflow-rule docs if new surfaces are exposed

### Acceptance hypotheses

- H4: common Kalman, affine, and transport derivative identities can be audited with explicit assumption usage.
- H5: `unverified` results can be split into missing-assumption vs parser-limit vs unsupported-algebra cases.

## Workstream 3: large-LaTeX indexing robustness

### Problem

Monograph-scale roots should not fail all-at-once because one included file, macro, chapter, or appendix is problematic.

### Deliverable

Add robust indexing for large roots with:

- cached label/block extraction,
- partial-success indexing,
- failed-file reporting,
- chapter-level and part-level indexing,
- nearest-label/topic lookup with confidence,
- explicit provenance-quality diagnostics,
- notation- and sign-convention-aware retrieval hooks for large monographs.

### Approach

1. Extend current index caching rather than replacing it.
2. Distinguish:
   - successful indexed files,
   - skipped files,
   - failed files,
   - stale cache state.
3. Add partial-result contracts so search and lookup can still operate when some files fail.

### Critical files

- `src/mathdevmcp/latex_index.py`
- `src/mathdevmcp/index_cache.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/cli.py`
- tests and benchmark fixtures for large documents

### Acceptance hypotheses

- H6: a large monograph root can return usable partial search results even when some inputs fail.
- H7: failed-file diagnostics are structured enough to guide the next safe step.

## Workstream 4: failure taxonomy and next actions

### Problem

Current conservative statuses are useful, but often too coarse for action.

### Deliverable

Keep top-level statuses stable where possible, but add substatus / blocker taxonomy and next-action fields.

Suggested substatus families:

- `unverified:missing_assumption`
- `unverified:parser_limit`
- `unverified:unsupported_noncommutative_algebra`
- `unverified:missing_shape`
- `unverified:missing_source_label`
- `mismatch:likely_formula_error`
- `mismatch:normalization_gap`
- `inconclusive:backend_unavailable`
- `inconclusive:toolchain_not_ready`
- `inconclusive:timeout`

Every blocked or abstaining result should include runnable next steps.

### Approach

1. Add substatus fields before adding many new tools.
2. Standardize next-action payload shape across CLI/MCP/library.
3. Extend workflow rules so agents prefer tool-suggested next commands over free-form guessing.

### Critical files

- `src/mathdevmcp/contracts.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/_workflow_rules.py`
- `docs/clients/workflow-rules.md`
- result-producing workflow modules

### Acceptance hypotheses

- H8: the same top-level abstention can be made operationally clearer without increasing false certification.
- H9: actionable next steps reduce agent misuse and repeated dead-end calls.

## Workstream 5: proof packet generation

### Problem

Serious derivations need a durable artifact that bundles source, assumptions, checks, and remaining gaps.

### Deliverable

Create proof-packet generation that records:

- source file and label,
- proposition statement,
- assumptions and manifest,
- normalized / IR expression,
- MathDevMCP audit result,
- symbolic result,
- numeric evidence if run,
- Sage/Z3 result if run,
- Lean status if run,
- remaining gaps,
- explicit certification boundary,
- optional links to code paths, experiment notes, and chapter-level claim context.

### Approach

1. Build packet generation on top of the new IR and assumption manifests.
2. Keep packet generation pure at the library layer; CLI can write a packet file.
3. Preserve redaction for private artifacts.

### Critical files

- `src/mathdevmcp/review_packet.py`
- new proof-packet module if needed
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`

### Acceptance hypotheses

- H10: a single packet can summarize proof state without conflating diagnostic evidence with theorem certification.

## Workstream 6: domain obligation templates

### Problem

Many derivations recur across filtering, affine pricing, macro-finance, DSGE, and HMC work. Reusable obligation templates would reduce reinvention and improve audit consistency.

### Deliverable

Add templates for:

- Gaussian log likelihood score,
- solve-form log determinant derivative,
- quadratic form derivative,
- Kalman prediction/update differentials,
- Hessian finite-difference-on-gradient parity,
- Lyapunov derivative,
- SVD/eigen spectral-gap denominators,
- sigma-point mean/covariance derivatives,
- affine SDF / no-arbitrage / Riccati recursions,
- CIP forward/basis sign-convention reconciliation,
- parameter-transform Jacobian and transport-map identities,
- HMC leapfrog and acceptance-ratio obligations.

### Approach

1. Build templates as decomposition tools, not one-shot proof claims.
2. Each template should emit smaller obligations plus required assumptions.
3. Measure success by reduced false confidence and improved audit traceability.

### Critical files

- new template/workflow modules
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/typed_workflows.py`
- benchmark fixtures and tests

### Acceptance hypotheses

- H11: template decomposition improves audit usefulness on recurrent derivation families.
- H12: templates remain conservative when assumptions are absent.

## Workstream 7: local Lean readiness mode

### Problem

Direct Lean checking is valuable, but local usefulness is reduced by toolchain/network friction and confusion between direct Lean vs LeanDojo readiness.

### Deliverable

Add an offline-friendly Lean readiness mode that reports:

- Lean executable availability,
- active toolchain,
- tiny local theorem check,
- whether direct proof checking is available,
- whether LeanDojo is separately available.

### Approach

1. Separate direct Lean readiness from LeanDojo readiness in `doctor` and related checks.
2. Avoid network-triggered behavior where possible.
3. Add a tiny stable smoke theorem.

### Critical files

- `src/mathdevmcp/doctor.py`
- Lean-related wrappers
- backend validation scripts

### Acceptance hypotheses

- H13: users can tell the difference between “Lean is locally usable” and “LeanDojo proof search is ready.”

## Broader capability roadmap for mathematical finance and economics

The monograph scopes show that future work needs much more than filtering support. To make future work like the corrected CIP monograph path and the DSGE/HMC monograph easier, MathDevMCP should expand toward the following capability families.

### A. Literature and citation support

Needed capabilities:

- claim-to-citation support packets,
- theorem provenance from cited papers,
- literature conflict reports,
- distinction between exact identity, model assumption, empirical regularity, proposed extension, and open problem,
- review-status manifests for local paper summaries,
- chapter-level claim support reports that can sit beside proof packets.

### B. State-space and filtering algebra

Needed capabilities:

- Kalman / square-root / SVD / information-form identities,
- differentiable filtering and smoothing recursions,
- mixed-frequency observation handling,
- particle-filter and differentiable resampling obligations,
- missing-data masks and ragged-edge assumptions,
- numerical-stability audits for covariance and factor updates.

### C. Asset-pricing and macro-finance structure

Needed capabilities:

- stochastic discount factor identities,
- affine pricing recursions,
- term-structure loading checks,
- cross-currency pricing and CIP basis sign-convention tracking,
- no-arbitrage consistency templates,
- cointegration / trend / shadow-rate structural assumptions,
- equilibrium restrictions and identification diagnostics,
- mortgage/MBS and credit spread recursion support where relevant.

### D. DSGE solution and perturbation workflows

Needed capabilities:

- equilibrium-condition decomposition,
- perturbation and policy-function derivative templates,
- steady-state existence and local regularity checks,
- Jacobian/Hessian structure audits,
- mapping between model equations, code, and solution blocks.

### E. Bayesian estimation and HMC geometry

Needed capabilities:

- log posterior decomposition,
- transform / Jacobian templates,
- mass-matrix and curvature diagnostics,
- position-dependent geometry obligations,
- transport-map and surrogate-model verification boundaries,
- finite-difference vs analytic derivative parity checks.

### F. Neural and differentiable numerical methods

Needed capabilities:

- neural-solver objective and residual audits,
- surrogate-vs-target distinction enforcement,
- gradient/Hessian parity workflows,
- autodiff traceability from equations to implementation,
- numerical counterexample / stress-test packets.

### G. Identification and econometric design

Needed capabilities:

- identification assumption manifests,
- observational-equivalence warnings,
- parameter restriction and normalization audits,
- measurement-system documentation packets,
- empirical design checklists linking theory to observable moments.

### H. Monograph-scale document engineering

Needed capabilities:

- chapter-level indexing and caching,
- notation cross-reference packets,
- sign-convention tracking,
- nearest-label retrieval across very large roots,
- “proof debt” tracking for unresolved derivations,
- document/code/experiment linkage at chapter granularity,
- claim and assumption dependency graphs.

### I. Research-decision artifacts

Needed capabilities:

- proof packets,
- negative-evidence packets,
- experiment-result linkage to labels/claims,
- claim-support reports suitable for monograph chapters,
- structured reset memos for major mathematical decisions.

## Relationship to the macro-finance roadmap

This document and [mathdevmcp-macrofinance-product-roadmap-2026-05-04.md](mathdevmcp-macrofinance-product-roadmap-2026-05-04.md) are complementary.

- This plan is the response to the field-use review and prioritizes the seven shortcomings plus cross-domain product implications.
- The macro-finance roadmap goes deeper on macro-finance-specific work packages, including affine pricing, CIP basis, posterior geometry, particle methods, and broader state-space/asset-pricing template families.

Recommended usage:

- use this plan to prioritize near-term product work,
- use the macro-finance roadmap to scope later domain expansion once the core shortcomings are addressed.

## Suggested implementation order

### Phase A: high-value foundation

1. failure taxonomy + next-action fields,
2. assumption manifests,
3. notation/convention metadata v0 and dependency-graph primitives,
4. large-root indexing robustness.

### Phase B: mathematical core

5. matrix-calculus IR,
6. proof packet generation.

### Phase C: reusable workflows

7. domain obligation templates,
8. local Lean readiness mode.

### Phase D: broader finance/econ productization

9. asset-pricing / affine / DSGE / HMC template families,
10. literature/citation-support packets,
11. identification and empirical-design packets,
12. monograph-scale notation / proof-debt / claim-support tooling.

## Verification strategy

- Add small synthetic fixtures for every new algebra/operator family.
- Add large-root stress fixtures and partial-failure fixtures.
- Add regression tests that check abstention quality, not only successful verification.
- Add CLI/MCP contract-sync tests for every new public surface.
- For finance/econ templates, use scoped obligations and explicit assumptions rather than giant end-to-end proofs.

## Success criteria

MathDevMCP is improved if it can do all of the following better than today:

1. distinguish formula error from parser limitation,
2. distinguish missing assumption from unsupported algebra,
3. keep working on large monographs with partial failure,
4. package evidence into durable proof packets,
5. support repeated finance/econ derivation families without hand-rebuilding every audit,
6. remain conservative about certification boundaries.

## Final recommendation

The right product move is not “make MathDevMCP prove more things automatically.” The right move is:

- stronger internal mathematical representation,
- explicit assumptions,
- better abstention diagnostics,
- durable evidence packets,
- reusable finance/econ obligation templates,
- robust monograph-scale workflows.

That would make future work like the corrected CIP monograph and the DSGE/HMC monograph materially easier while staying faithful to the tool’s core safety model.
