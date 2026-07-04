# Tool Improvement Plan From Downstream Benchmark

Date: 2026-07-02

Status: `IMPLEMENTATION_PLAN_READY`

## Goal

Improve MathDevMCP so it genuinely helps agents answer high-level mathematical
work questions:

- "Can I derive X from Y?"
- "Can we prove X, or find a counterexample?"
- "What assumptions are required to derive or prove X?"
- "Where does this derivation first fail?"
- "Does this code implement the documented math?"
- "Can we prepare a review packet without overclaiming proof?"

The repaired downstream benchmark should be used as a local diagnostic and
regression harness, not as a promotion claim.

## Current Benchmark Signal

The repaired benchmark is valid locally but has a ceiling effect:

- A required passes: 8/9;
- B required passes: 9/9;
- C required passes: 9/9;
- C improves over A only on the Joseph backend-certificate case;
- C ties B under frozen required dimensions;
- no hard vetoes;
- no C-over-B promotion.

Interpretation:

- The benchmark hygiene problem is repaired.
- The main codebase problem is capability, not measurement hygiene.
- Current workflow envelopes are useful but often summarize evidence rather
  than producing deeper executable artifacts.
- The next implementation cycle should improve tools while a separate agent
  hardens benchmark v2.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can targeted tool improvements make MathDevMCP more useful for derivation, proof/counterexample, assumption discovery, derivation debugging, math-to-code audit, and review-packet preparation? |
| Baseline/comparator | Current high-level workflow modules and repaired downstream benchmark result. |
| Primary criterion | Each phase adds executable or structured evidence paths, focused tests, and benchmark-case regression checks without weakening non-claim boundaries. |
| Veto diagnostics | Prose-only capability disguised as proof; backend diagnostics treated as semantic truth; hidden assumptions; broad theorem-proving/product/scientific claims; tool APIs not exposed through MCP; benchmark overfitting; unrelated refactor. |
| Explanatory diagnostics | Per-workflow tests, MCP facade checks, high-level workflow quality report, repaired benchmark rerun notes if applicable. |
| Not concluded | No public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, proof correctness beyond scoped certified obligations, or general model reliability. |

## Implementation Phases

### Phase 1: Workflow Result Evidence Ledger

Objective:

Strengthen the shared high-level workflow envelope so every high-level result
has a self-contained evidence ledger suitable for downstream agents.

Targets:

- `src/mathdevmcp/high_level_contracts.py`
- `src/mathdevmcp/high_level_workflows.py`
- tests in `tests/test_high_level_workflows.py`

Changes:

- Add optional structured fields or evidence extras for:
  - `decision_criteria`;
  - `proof_obligations`;
  - `route_attempts`;
  - `what_would_change_conclusion`;
  - `residual_risks`;
  - `forbidden_claims_avoided`.
- Preserve backward compatibility with existing `high_level_workflow_result`.
- Update validators so new fields are checked when present.

Checks:

- focused high-level contract tests;
- existing high-level workflow tests;
- MCP surface sync tests.

Benchmark link:

This directly addresses the benchmark need for self-contained reasoning and
next-agent actionability.

### Phase 2: Derive-From Route Plans

Objective:

Make `derive_from` return a derivation route plan, not just a packaged
low-level result.

Targets:

- `src/mathdevmcp/derive_from.py`
- `src/mathdevmcp/derive_or_refute.py`
- `src/mathdevmcp/proof_obligations.py`
- `tests/test_derive_from.py`

Changes:

- Include explicit distinction between:
  - givens as context;
  - assumptions used by route;
  - assumptions still missing;
  - backend-certified steps;
  - unresolved proof obligations.
- For equality-like targets, include a route table:
  - normalized target;
  - backend attempted;
  - certificate/counterexample/unknown;
  - obligation text;
  - next artifact.
- For matrix/domain/proxy failures, return `inconclusive` or
  `missing_assumptions` with named route gaps rather than a weak derivation.

Checks:

- symbolic identity proof case;
- counterexample case;
- matrix/domain route-gap case mirroring affine pricing recursion;
- missing-assumptions case mirroring neural-solver guarantees.

Benchmark link:

Targets RLHLB-04 and RLHLB-09, where the correct result is route gap or missing
assumptions, not a proxy derivation.

### Phase 3: Prove-Or-Counterexample Backend Evidence

Objective:

Improve `prove_or_counterexample` so proof/refutation claims are tied to
concrete backend evidence objects.

Targets:

- `src/mathdevmcp/prove_or_counterexample.py`
- `src/mathdevmcp/prove_or_refute.py`
- `src/mathdevmcp/symbolic_backend.py`
- `src/mathdevmcp/counterexample_search.py`
- `src/mathdevmcp/lean_check.py`
- tests in `tests/test_prove_or_counterexample.py`

Changes:

- Preserve backend route attempts in a structured list.
- Require proof-level pass to include either:
  - backend certificate summary;
  - accepted source-backed derivation artifact;
  - explicit proof obligation for human/formal follow-up.
- Require refutation to include a concrete counterexample artifact.
- Separate SymPy/Sage-style symbolic results, finite numeric probes, and Lean
  checks so proxy evidence cannot be promoted.

Checks:

- Joseph exact-arithmetic equivalence with certificate-like evidence;
- noncommuting matrix counterexample;
- malformed claim returns `not_encodable`;
- backend unavailable remains diagnostic only.

Benchmark link:

Targets RLHLB-03 and RLHLB-01.

### Phase 4: Assumption Discovery With Route Taxonomy

Objective:

Upgrade `assumptions_for` from keyword-style assumption detection toward a
route-specific assumption ledger.

Targets:

- `src/mathdevmcp/assumptions_for.py`
- `src/mathdevmcp/assumption_discovery.py`
- `src/mathdevmcp/domain_templates.py`
- `tests/test_assumptions_for.py`

Changes:

- Categorize assumptions as:
  - domain;
  - differentiability;
  - covariance/invertibility;
  - masking/selection;
  - model/distribution;
  - parameterization;
  - route-linking;
  - training/optimization.
- Add templates for:
  - Kalman prediction-error likelihood;
  - Kalman score same-scalar route;
  - neural-solver approximation guarantee;
  - Gaussian MGF/affine recursion route.
- Keep the non-claim that route-required assumptions are not globally minimal.

Checks:

- Kalman likelihood assumptions include selected innovation covariance
  positive definiteness.
- Kalman score assumptions include same-scalar, differentiability, covariance
  domain, masking, and route-linking.
- Neural-solver guarantee assumptions include theorem, domain, function class,
  architecture/capacity, training, norm, and bridge.

Benchmark link:

Targets RLHLB-02, RLHLB-05, and RLHLB-09.

### Phase 5: Math-To-Code Trace Artifacts

Objective:

Make `audit_math_to_code` and likelihood implementation audit produce a
traceability artifact that maps documented math terms to code terms.

Targets:

- `src/mathdevmcp/audit_math_to_code.py`
- `src/mathdevmcp/equation_code_match.py`
- `src/mathdevmcp/agent_workflows.py`
- `src/mathdevmcp/operation_consistency.py`
- tests in `tests/test_audit_math_to_code.py` and
  `tests/test_agent_workflows.py`

Changes:

- Return a term map with:
  - documented term;
  - matched code operation or symbol;
  - missing term;
  - alias used;
  - extra code terms;
  - structural-only boundary.
- Add a focused likelihood route helper for logdet plus solve/quadratic-form
  checks.
- Preserve alternatives: hidden helper, whitening, cached solve, or equivalent
  transformed route.

Checks:

- missing solve/quadratic-form case;
- alias-supported match;
- extra terms remain audit-only;
- structural match is not semantic proof.

Benchmark link:

Targets RLHLB-06.

### Phase 6: Review Packet Compiler

Objective:

Make `prepare_review_packet` compile nested workflow outputs into a
self-contained downstream-agent packet.

Targets:

- `src/mathdevmcp/prepare_review_packet.py`
- `src/mathdevmcp/agent_handoff_packet.py`
- `tests/test_prepare_review_packet.py`
- `tests/test_agent_handoff_packet.py`

Changes:

- Include:
  - target statement;
  - background/framing;
  - assumptions;
  - route attempts;
  - backend checks;
  - proof obligations;
  - gap ledger;
  - decision criteria;
  - residual risks;
  - what would change the conclusion;
  - non-claims.
- Ensure proof-like nested evidence is preserved as nested evidence, not
  promoted to packet-level proof.

Checks:

- diagnostic packet validates;
- proof-like overclaim fails validation;
- missing source/background fails validation;
- nested proof/refutation/missing-assumption/structural mismatch outputs remain
  bounded.

Benchmark link:

Targets RLHLB-07 and improves C-condition packet quality.

### Phase 7: MCP And CLI Surface Alignment

Objective:

Expose the improved high-level functions consistently through MCP/server/CLI
surfaces so coding agents can actually use them.

Targets:

- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `src/mathdevmcp/cli.py`
- `tests/test_mcp_surface_sync.py`
- `tests/test_mcp_server.py`

Changes:

- Confirm improved result fields pass through MCP.
- Add or update CLI commands only where existing CLI patterns support them.
- Update tool descriptions so agents know when each workflow is certifying,
  diagnostic, or review-only.

Checks:

- MCP facade tests;
- server sync tests;
- CLI smoke if commands are added.

Benchmark link:

Ensures downstream agents can call improved workflows rather than relying on
free-form prose.

### Phase 8: Benchmark-Guided Regression

Objective:

Use the repaired benchmark as a regression harness after tool improvements,
without claiming C-over-B promotion from the current result.

Targets:

- repaired benchmark artifacts under `.mathdevmcp/downstream_agent_usefulness/`;
- high-level workflow quality report;
- new tests that encode the nine benchmark cases as tool-level workflow
  expectations.

Changes:

- Add a small tool-level regression suite derived from the nine repaired cases.
- Do not rerun downstream response subjects unless explicitly authorized.
- Record before/after tool capability evidence separately from downstream
  response evidence.

Checks:

- focused unit tests for all five/six high-level workflows;
- high-level workflow quality report;
- JSON and prompt-contract validation remains clean.

Benchmark link:

Turns the benchmark from one-off response measurement into a local regression
suite for actual tool behavior.

## Proposed Execution Order

1. Phase 1 result envelope.
2. Phase 4 assumption taxonomy, because multiple benchmark cases depend on it.
3. Phase 3 proof/counterexample evidence.
4. Phase 2 derive-from route plans.
5. Phase 5 math-to-code trace.
6. Phase 6 review packet compiler.
7. Phase 7 MCP/CLI alignment.
8. Phase 8 benchmark-guided regression.

This ordering improves shared evidence structure first, then the most reusable
mathematical engines, then packet/output surfaces.

## Stop Conditions

Stop and write a blocker if:

- a phase would require changing benchmark scores or rubric post hoc;
- an implementation can only produce prose without structured evidence;
- a backend failure would be promoted as proof/refutation;
- a planned claim crosses release, public benchmark, scientific, product, broad
  theorem-proving, or general model reliability boundaries;
- tests cannot distinguish implementation failure from missing mathematical
  assumptions.

## Near-Term Recommendation

Start with Phase 1 and Phase 4. They are low-risk, improve every workflow, and
directly address the benchmark ceiling effect by making outputs more
self-contained and assumption-aware before adding more backend sophistication.
