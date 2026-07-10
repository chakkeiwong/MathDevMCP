# MathDevMCP External-Tool-First Tree Derivation Plan

Date: 2026-07-08

## Objective

Build the tree derivation search lane as a MathDevMCP orchestration layer that
uses existing deterministic and specialist external tools before any in-house
branch search. The output must be directly consumable by agents: a gap report,
candidate assumption/derivation branches, exact tool evidence, proposed fixes,
and explicit non-claims.

## Core Decision

Do not build a new theorem prover. Use external tools directly where possible:

| Need | First tools to consider | MathDevMCP role |
| --- | --- | --- |
| Scalar algebra/equality | SymPy, then SageMath | Normalize target, call/check backend, record certificate/counterexample/blocker. |
| Matrix/domain algebra and calculus | SageMath, SymPy where encodable, Lean when formalized | Track assumptions and formalization gaps; route to backend. |
| Formal proof/certification | Lean direct check | Build or receive Lean source; only Lean success without placeholders certifies. |
| Lean premise retrieval | LeanSearch-v2, LeanExplore | Retrieve candidate declarations/premises; do not treat retrieval as proof. |
| Lean proof-state/search | Pantograph, LeanDojo | Explore proof states/tactics when a Lean project exists; final proof still needs Lean check. |
| Lean source/static extraction | jixia | Extract declarations, symbols, proof state/source spans when a Lean project exists. |
| Document localization | MathDevMCP LaTeX index/search/label lookup | Provide source spans and provenance before backend work. |
| Assumption accounting | MathDevMCP assumptions/gap tools plus backend validation | Propose sufficient assumption sets and show how they close the derivation route. |

## Evidence Contract

Question: Can MathDevMCP improve hard mathematical document repair by using an
external-tool-first tree search controller rather than one-shot agent prose?

Baseline: current high-level workflows (`derive_from`, `assumptions_for`,
`audit_and_propose_fix`, `audit_math_document_rigor`) with route plans but no
within-problem branch tree.

Primary criterion: every branch in the new lane records tool-consideration
evidence before in-house expansion, and every proposed fix includes location,
problem, mathematical why, assumptions/routes, derivation under assumptions,
exact tools used, remaining blockers, and non-claims.

Veto diagnostics:

- a branch proposes a mathematical fix without recording considered external
  tools;
- route plans or retrieval hits are described as proofs;
- an unavailable backend is treated as refutation;
- generated reports omit location, mathematical why, or derivation route;
- in-house search appears without a gap justification.

Explanatory diagnostics:

- backend availability and version mismatches;
- formalization-required states;
- budget exhaustion;
- branch count and blocker taxonomy.

Not concluded even if this passes:

- no broad theorem-proving claim;
- no public release readiness claim;
- no claim that the selected branch is globally minimal;
- no claim that retrieval/search tools replace final backend certification.

Artifact: this plan, repo policy, Python policy/route contracts, focused tests,
and later phase result notes under `docs/plans`.

## Skeptical Plan Audit

Wrong-baseline risk: comparing against a hypothetical perfect prover would hide
the real regression. Baseline is the current MathDevMCP one-shot high-level
workflows and installed optional integrations.

Proxy-metric risk: route count or retrieval count must not become success.
Only branch-level evidence and certifying backend results can support proof
claims.

Environment risk: LeanDojo/Pantograph/LeanSearch/jixia may be installed in a
separate backend environment. The planner must record active-Python, backend,
and executable availability rather than assuming importability.

Hidden-assumption risk: stochastic-economics repairs often require probability
law, measurability, integrability, differentiability, interiority, shape, and
conformability assumptions. Branches must name these assumptions and show the
derivation route they enable.

Artifact-risk: a prose-only plan would not change behavior. The first slice
must create a Python policy contract and tests so future tools can enforce the
discipline.

Audit result: proceed with a phased implementation that first makes
external-tool-first routing auditable, then builds the budgeted tree executor on
that contract.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Promotion status |
| --- | --- | --- | --- | --- | --- |
| Existing packages first | User direction and local survey | Avoid duplicate prover/search work and reduce hallucination | Package is unavailable or mismatched | `doctor` integration/version report | Reviewed default |
| Lean final certification boundary | Existing Lean/LeanDojo policies | Proof-state tools are not final certificates | Tactic trace treated as proof | require direct `lean_check` evidence | Reviewed default |
| SymPy/Sage algebra before agent derivation | Existing symbolic route planner | Deterministic CAS is cheaper and reproducible | Target not encodable or domain assumptions missing | route status `requires_formalization` or `not_encodable` | Reviewed default |
| Summary-first retrieval | Literature survey and LeanExplore/LeanSearch design | Reduces tokens and grounds premise selection | Retrieval hit hallucinated into proof | retrieval result must be evidence-only | Reviewed default |
| Budgeted branch search | Survey and weak-report regression | Hard repairs need multiple hypotheses and blocker memory | Search hides missing assumptions in branch score | branch ledger with blockers and non-claims | Hypothesis for later phases |

## Architecture

The lane has four layers:

1. Source and target localization: labels, line ranges, equations, notation,
   assumptions, and nearby definitions.
2. External-tool-first route planner: records which packages/executables are
   applicable, available, selected, blocked, or rejected.
3. Budgeted branch controller: expands assumption sets, formalization choices,
   subgoals, rewrite routes, and backend attempts; blocked nodes remain durable.
4. Agent-consumable renderer: writes a gap/proposal report with exact evidence
   and patch candidates.

The branch controller may borrow best-first/MCTS-style scheduling from the
literature, but each action is a MathDevMCP evidence operation:

- retrieve source/premises;
- add a candidate assumption set;
- split a derivation step into subgoals;
- formalize for SymPy/Sage/Lean;
- call backend;
- record blocker;
- render proposed patch.

## Phases

### Phase 0: Repo Policy And External-Tool-First Contract

Objective: make external-tool-first a repo rule and a testable Python contract.

Artifacts:

- `AGENTS.md`;
- `src/mathdevmcp/external_tool_policy.py`;
- tests for tool consideration, fallback blocking, and route-plan integration;
- MCP/CLI exposure for an agent-facing route plan.

Checks:

- focused pytest for the new policy;
- compile check for touched modules;
- diff check on touched files.

Handoff condition: agents can call one function and see which external tools
must be considered before in-house search.

### Phase 1: Backend Adapter Readiness Matrix

Objective: turn `doctor` availability into route decisions for SymPy, Sage,
Lean, LeanSearch-v2, LeanExplore, Pantograph, LeanDojo, and jixia.

Artifacts:

- per-tool evidence schema: exact command/input/output/timeout/version;
- unavailable/mismatch diagnostics;
- install/profile hints from `integration_versions.py`.

Checks:

- offline tests with mocked doctor payloads;
- optional real-env smoke tests where backends are installed.

Handoff condition: route plans distinguish available, unavailable,
requires-formalization, rejected, and evidence-only tools.

### Phase 2: Search Tree Data Model

Objective: define stable branch/node records before implementing search.

Artifacts:

- `SearchNode`, `BranchEvidence`, `BackendAttempt`, `BlockerNode`,
  `AssumptionSet`, and `PatchCandidate` records;
- JSON contract and markdown rendering expectations;
- resume/truncate format for long searches.

Checks:

- schema tests;
- deterministic serialization tests;
- non-claim boundary tests.

Handoff condition: a tree can be serialized with no backend calls and still
shows source, assumptions, routes, blockers, and non-claims.

### Phase 3: Direct External Tool Adapters

Objective: integrate direct use of installed tools without inventing parallel
logic.

Adapters:

- SymPy/Sage algebra and derivative checks;
- Lean direct final check;
- LeanSearch-v2 and LeanExplore premise retrieval;
- jixia static extraction;
- Pantograph/LeanDojo proof-state interaction when Lean project context exists.

Checks:

- unit tests with mocked subprocess/package boundaries;
- opt-in real backend smoke tests;
- timeouts and artifact capture.

Handoff condition: each adapter returns a bounded evidence object and never
claims more than the backend certifies.

### Phase 4: Budgeted Branch Controller

Objective: implement a small best-first controller over MathDevMCP evidence
actions.

Search discipline:

- safe actions: deterministic normalization, source lookup, certified backend
  checks, definition expansion with source span;
- unsafe actions: assumption addition, formalization choice, rewrite guess,
  derivation split;
- unsafe actions create branches with explicit hypotheses and blockers.

Budgets:

- `smoke`: small node/depth budget for tests;
- `standard`: larger local search for document repair;
- `deep`: opt-in longer search with result note.

Checks:

- seeded hard-document fixtures;
- budget exhaustion produces useful blocker ledger;
- no branch can be marked proved without backend/source assumption evidence.

Handoff condition: the controller can answer "can we derive X?" with proved,
refuted, partial, blocked, or budget-exhausted branches.

### Phase 5: Report Integration

Objective: replace hand-wavy fixes with branch-derived repair reports.

Artifacts:

- markdown sections per gap: location, problem, mathematical why, assumptions,
  branch derivation, exact tools, proposed patch, remaining blockers;
- JSON report preserving the full tree.

Checks:

- risky-debt and credit-card document experiments;
- report quality regression tests;
- claim-boundary audit.

Handoff condition: report text is generated from branch evidence, not generic
fallback prose.

### Phase 6: Benchmark And Mission-Control Integration

Objective: make this lane durable for future agents.

Artifacts:

- mission-control checklist entry;
- benchmark cases for assumption gaps, derivation splits, backend unavailability,
  and formalization blockers;
- support-matrix updates.

Checks:

- high-level workflow quality tests;
- MCP/CLI parity tests;
- release non-claim checks.

Handoff condition: future changes cannot regress to yes/no or hand-wavy reports
without failing tests.

## Stop Conditions

Stop and write a blocker result if:

- a needed external tool requires credentials, downloads, or runtime access that
  has not been approved;
- a backend result cannot be bounded by timeout and captured artifact;
- a branch would need an unstated scientific assumption to proceed;
- local tests show route plans can be mistaken for proof certificates.

## First Execution Slice

This turn should complete Phase 0 and the Phase 1 contract surface:

1. add repo-local policy;
2. add an agent-facing `external_tool_first_plan` function;
3. integrate it into backend route planning;
4. expose it through CLI/MCP;
5. test fallback blocking and selected external routes.

Full budgeted tree search begins only after this contract passes review and
tests, because the search executor depends on trustworthy tool-consideration
records.
