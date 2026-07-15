# MathDevMCP Credit-Card Full Mission Audit Result

Date: 2026-07-16

Status: `MISSION_NOT_YET_ACCOMPLISHED`

Plan:
`docs/plans/mathdevmcp-credit-card-full-mission-audit-plan-2026-07-16.md`

## Executive Decision

MathDevMCP is now substantially useful for source-bound exploration of the
credit-card proposal, but it has not yet accomplished its broader mission as an
exploratory, high-standard, rigorous, agent-facing mathematical development
system.

The strongest current lane can reconstruct selected multiline equations from
the exact requested file, discover context and candidate assumptions, construct
and rank materially different branches, preserve evidence and non-claim
boundaries, and return a compact continuation-capable response. It correctly
keeps publication disabled and promotes no unsupported repair.

The same document also exposes a critical semantic failure: four generic proof
workflows treat the source's terminal-value definition as a free-variable
theorem and report it as `refuted`. Other high-level workflows still consume a
weaker extraction path, duplicate labels across document versions are not
consistently disambiguated, and exploratory branches stop before autonomous
formalization and specialist-tool execution. These failures cross the mission's
claim-boundary and agent-usefulness criteria.

## Scope Decision

The phrase "run all our functions against the document" was audited before
execution. A literal call of every function with invented document inputs would
produce false coverage. The completed scope was therefore:

- all 57 registered public MCP tools;
- the relevant CLI-only document and mathematical packet workflows;
- an explicit applicability record for tools whose required code, literature,
  temporal, or theorem inputs cannot be derived from this document;
- CLI, in-process facade, and FastMCP parity checks for the main persisted
  document workflow and resolver;
- direct external-tool diagnostics only where a source-bound or explicitly
  diagnostic input could be stated.

This is applicability-complete public-surface coverage. It is not a claim that
every internal helper or every CLI command has a meaningful document-path input.

## Source Identity

| Field | Value |
| --- | --- |
| Source | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex` |
| SHA-256 before and after | `68625df7943b4b3f6f358c0873cf976069299484f15e9f7990c2a54466e8ade8` |
| Size | 384,772 bytes; 7,566 lines |
| Directory corpus | 11 `.tex` files, including historical versions |
| Selected labels | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv`, `eq:terminal-value-base` |
| Source mutation | None |

## Public Function Accounting

| Classification | Count | Interpretation |
| --- | ---: | --- |
| Registered public MCP tools | 57 | Registry, facade, and server inventory |
| Invoked with valid bounded inputs | 48 | Operational invocation, not mathematical success |
| Inapplicable because a source-derived input is absent | 9 | Explicitly classified; no input was fabricated |
| Missing registered records | 0 | Complete inventory |
| Duplicate records | 0 | One record per registered tool |
| Invocation errors in final manifest | 0 | Process/API behavior only |

The nine inapplicable functions were:

- `compare_doc_code`, `code_implements_equation`, `audit_math_to_code`,
  `audit_implementation_label`, `compare_label_code`, and
  `implementation_brief`: no implementation file is bound by the source;
- `literature_local_audit`: the function requires already-extracted paper
  theorem assumptions and a local mapping, while the document supplies
  citations rather than that typed input;
- `audit_kalman_recursion`: the proposal is not a Python Kalman implementation;
- `audit_temporal_contract`: no bound DSGE-style code file or explicit temporal
  field map is supplied.

The final manifest is stored locally at
`.local/mathdevmcp/evidence/mission-audit-credit-card-20260716/tool-audit-manifest.json`
with SHA-256
`adc0718c7f0c8b8affdc3194d7a340cfe8a96c1b193845603e7518d2cb743671`.
The `.local` tree is intentionally ignored and is not a source or release
artifact.

## Main Workflow Result

The detailed document-tree workflow returned `partial_coverage`:

| Measure | Result |
| --- | ---: |
| Localized equation rows in the selected file | 222 |
| Labeled rows in the selected file | 178 |
| Selected targets | 4 |
| Context graphs / semantic packets | 4 / 4 |
| Ranked branches | 8 |
| Recorded blockers | 100 |
| Typed obligations ready for a backend | 2 |
| Typed obligations blocked on missing assumptions | 2 |
| Promoted claims | 0 |
| Ready repair proposals | 0 |
| Partial-evidence repair reports | 0 |
| Failure classifications | 4 branch execution pending; 4 formalization blocked; 2 mathematical blocked |

The detailed persisted artifact is 1,724,820 bytes and has SHA-256
`64ff8b6a94141989ecf9ab4e961f4c56c5294616fd1207fd52f36d7793d6e852`.
The smaller public invocation record has SHA-256
`5c8d48a319b03e30edfc30987d847791e6c02c45377a4ec5b82786abbf47a429`.

The adjacent generic rigor workflow returned 26 gaps, 3 concrete repair
records, and 23 diagnostic abstentions. Its response was 785,023 bytes. The
different counts are not merely alternate summaries; the two workflows operate
on materially different extraction semantics.

## What Now Works

- Exact requested-file filtering is available in the repaired document-tree
  lane, despite repeated labels in sibling versions.
- The selected multiline equations are reconstructed with their complete
  source span, stable identity, label, file, and digest.
- Context graphs expose definitions, nearby assumptions, inferred candidates,
  missing conditions, and unresolved relations without promoting them to facts.
- The search tree constructs distinct assumption, formalization, and backend
  routes and ranks them using a validity-gated partial order rather than a scalar
  score that can compensate for vetoes.
- External tools are considered explicitly. SymPy, SageMath, Lean, and jixia
  availability was diagnosed; absent optional tools remain engineering
  diagnostics, not mathematical refutations.
- The compact document response, persisted continuation token, and record
  resolver preserve CLI/facade/FastMCP semantics in the exercised lane.
- Publication remains disabled. No diagnostic, retrieval hit, skeleton,
  unexecuted branch, or proxy metric became a verified claim or applicable edit.

## Remaining Mission Gaps

### P0: Definition And Identity Semantics Are Lost

The source says the terminal-value expression is a transparent placeholder and
not a universal truth. In context, the equality defines the chosen placeholder
model:

`dTV = rho*dCF_next/(r_disc + lambda_attrition + q)`.

`derive_from`, `prove_or_counterexample`, `derive_or_refute`, and
`prove_or_refute` instead treat `dTV` as an unconstrained independent variable
and return `refuted` with a counterexample. That counterexample is valid only
for the different proposition that arbitrary free variables always satisfy the
equality. It is not a source-faithful refutation of a definition.

Required repair: introduce a typed claim role such as definition, identity,
assumption, derived proposition, estimator, or diagnostic; preserve it from
source extraction through formalization and proof routing; prohibit theorem
refutation when the scoped source construct is definitional.

### P0: High-Level Workflows Do Not Share One Extraction Contract

The repaired document-tree lane reconstructs all terms in
`eq:incremental-cash-flow`. The generic rigor locator can reduce the same target
to its final continuation:

```latex
-\Delta Tax + \Delta RelValue
```

This produces inconsistent obligations, gaps, and proposed repairs depending
on which public API an agent happens to call. Some generated repairs omit terms
that are present in the source.

Required repair: make the label-scoped, requested-file, complete-row obligation
the single high-level extraction contract. All audits, packets, and generic
proof workflows should consume it or return a typed incompatibility.

### P0: Duplicate Labels Are Not Safely Bound Across The Public Surface

The directory index contains 2,710 blocks and 2,078 equation rows. Only 55 label
names are unique across the directory; 235 names are ambiguous because the
directory includes historical proposal versions. Primitive lookup accepts a
`file` selector, but many high-level and proof-packet APIs do not. A proof packet
can have empty top-level source provenance while nested logic silently chooses
the first match.

Required repair: require or propagate an exact file/content identity whenever a
label is ambiguous, expose ambiguity as a first-class result, and reject silent
first-match selection in every high-level workflow.

### P1: Exploration Stops Before Specialist Execution

The tree produces useful routes, assumptions, external-tool ledgers, and next
discriminating actions, but every selected branch remains
`blocked_before_backend_certification`. Even the two backend-ready targets
produce pending or `not_encodable` attempts. The system does not yet translate
source-bound obligations into supported SymPy, SageMath, or Lean input and run
the smallest suitable check autonomously.

Required repair: add claim-role-aware formalization adapters, route supported
obligations to installed tools, feed results back into branch state, and retain
explicit abstention for unsupported semantics.

### P1: Valuation-Domain Formalization Is Missing

The domain-template catalog contains only Kalman likelihood, CIP/SDF sign, and
HMC Jacobian templates. It returns no match for the terminal-value formula.
Discounted cash flow, accounting identities, conditional expectations, causal
estimands, state-space policy value, and dynamic programming are absent.

Required repair: add reviewed templates incrementally, starting with valuation
definitions and finite-horizon discounted cash flow. Templates must encode
domain, timing, denominator, integrability, information-set, and claim-role
obligations without pretending that a template proves the source claim.

### P1: Assumption Matching Is Not Expression Aware

The explicit assumption
`r_disc + lambda_attrition + q != 0` does not discharge the generic requirement
`denominator is nonzero`. This leaves a supplied condition reported as missing.

Required repair: normalize typed assumptions against the actual expression and
record which source assumption discharges which backend precondition.

### P1: Relevant Capabilities Are Split Between CLI And MCP

The CLI exposes 79 commands while MCP exposes 57 tools. Relevant CLI-only
capabilities include parser benchmarking, domain-template suggestion and
generation, claim-support packets, proof packets, and negative-evidence packets.
An agent restricted to MCP cannot access the complete workflow exercised here.

Required repair: define one product capability registry and either expose each
agent-relevant capability through MCP or mark it intentionally operator-only
with a reason and an equivalent supported handoff.

### P2: Resolver Vocabulary Is Not Discoverable

Resolver collection names are closed in code but not enumerated in MCP
documentation or CLI help. An intuitive `targets` request fails with only an
out-of-scope message, while the valid `label_scoped_obligation` collection
succeeds.

Required repair: publish the accepted collection enum in schema/help, include
valid choices in validation errors, and provide them in the page metadata.

### P2: Several Agent Payloads Remain Too Large

Representative JSON sizes were 1.72 MB for the detailed document audit, 785 KB
for the rigor audit, approximately 366 KB for a review packet, and 359 KB for an
audit/fix packet. The compact document page is usable, but neighboring workflows
can still overwhelm model context and hide the decisive action.

Required repair: apply the compact summary plus evidence-resolver pattern to
all large agent-facing reports and set explicit payload budgets in public
contracts.

### P2: Top-Level Mission Language Has Drifted

`AGENTS.md` and the mission charter correctly say "exploratory in search,
rigorous at the claim boundary." The top-level `README.md` still introduces an
industrial-release-centered product and says the tools are "conservative."
Lower-level references to a conservative parser or status are technically
appropriate; the product identity is stale.

Required repair: align the top-level introduction and examples with the current
academic mission while preserving conservative claim-boundary behavior.

## Full Repository Check

The full CPU-only suite was run with Python plugin autoload disabled:

```text
1531 passed, 33 failed, 4 skipped in 40m48s
```

The result is not release-clean. Failure triage found:

- one concrete real-document FOC proposal regression where a reconstructed
  `math_fix` was expected but `None` was returned;
- one real-local high-level pilot contract drift involving evidence classes;
- five real-local pilot cases that still declare absent source adapters;
- three order/isolation failures whose Phase 03/Phase 09 tests pass in fresh
  processes;
- a large release-readiness cascade rooted in reproducible checker failures.

Two release checker failures are themselves defects rather than evidence that
the installed packages or Sage process control are unsafe:

1. The packaging check compares unversioned names such as `mcp` and `sympy`
   against exact strings such as `mcp==1.27.0` and `sympy==1.14.0`.
2. The governance scanner requires a literal `timeout=` keyword on every
   `subprocess.Popen`. `sage_adapter.py` instead enforces an explicit monotonic
   deadline, bounded selector loop, kill, and bounded wait.

Those false positives cascade into benchmark and release-profile tests, but
they do not justify ignoring the independent FOC, pilot, source-adapter, and
test-isolation gaps.

Focused reruns established that the Phase 03 guard and two Phase 09
reconstruction tests pass independently. Packaging/governance checks fail
reproducibly. Four of five current real-local pilot probes pass. `git diff
--check` and a repository Python compile check pass.

## External Tool Inventory

| Tool | Audit result | Boundary |
| --- | --- | --- |
| SymPy 1.14.0 | Available | Useful for supported scalar identities; no source-role inference |
| SageMath 9.5 | Available | Adapter/process route available; no valuation formalizer |
| Lean 4.29.1 | Available | Direct reflexive diagnostic accepted; not source-faithful proof |
| jixia | Available | Static Lean extraction only; not a certifier |
| LaTeXML 0.8.6 | Available | Parser diagnostic only |
| Pandoc 2.9.2.1 | Available | Parser diagnostic only |
| LeanDojo | Unavailable in active Python | Engineering availability result |
| LeanExplore | Unavailable in active Python | Engineering availability result |
| Pantograph | Unavailable in active Python | Engineering availability result |
| LeanSearch-v2 | Unavailable | Retrieval availability result |

Direct Lean accepted an agent-authored reflexive diagnostic theorem. This shows
that the executable is live; it does not establish that the source equation was
faithfully formalized or proved.

## Separate Evidence Ledgers

### Engineering Correctness

- Public-tool registry accounting is complete and final invocations did not
  raise.
- The repaired selected-file document lane, persistence, resolver, and parity
  checks operate on this document.
- The full suite has 33 failures and therefore vetoes a clean engineering or
  release claim.
- Release checker defects, test-order leakage, the FOC regression, and source
  adapter gaps require separate repairs.

### Mathematical Validity

- No source mathematical claim was promoted.
- The source definition was misclassified as a refuted theorem by four generic
  workflows; their refutation verdict is rejected as semantically unbound.
- Two selected typed obligations are structurally ready for a backend, but no
  source-faithful valuation formalization or certificate was produced.
- Missing optional tools are not mathematical evidence.

### Scientific And Product Interpretation

- The result supports the claim that the repaired lane is useful for exact
  localization, context discovery, exploratory route generation, evidence
  accounting, and bounded handoff on this document.
- It does not support whole-document correctness, autonomous mathematical
  repair, optimal search, broad domain coverage, publication, release, or
  mission completion.

## Negative-Result Classification

| Observed failure | Class | What is weakened | What remains viable | Smallest discriminating next artifact |
| --- | --- | --- | --- | --- |
| Definition reported as refuted | Semantic/implementation failure | Generic proof workflow correctness on source-bound claims | Backend counterexample machinery for actual free-variable propositions | Typed claim-role regression spanning extraction through proof routing |
| Truncated multiline target | Extraction integration failure | Generic rigor/fix workflow fidelity | Repaired label-scoped document-tree extraction | One shared-obligation parity test across all high-level APIs |
| Branches never execute | Formalization/product gap | Autonomous agent-facing development loop | Route generation and explicit abstention | One valuation identity formalized and executed end to end |
| Explicit denominator assumption remains missing | Assumption normalization failure | Assumption discovery/actionability | Raw assumption discovery | Expression-to-precondition discharge record |
| 33 suite failures | Engineering integration failure | Clean repository/release claim | Focused repaired lanes | Fix root checkers, isolation, FOC, and pilot failures; rerun suite |

The audit provides evidence against current end-to-end mission completion. It
does not provide evidence against the underlying exploratory architecture or
against the mathematical content of the credit-card proposal.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `MISSION_NOT_YET_ACCOMPLISHED` |
| Primary criterion | Failed: public functions are accounted for and the strongest lane is source-bound, but semantic consistency, automatic specialist execution, and full-surface usability are not met |
| Veto diagnostics | Fired: definition-as-theorem false refutation, inconsistent extraction, silent duplicate-label risk, and non-clean full suite |
| Main uncertainty | How much of the broader 7,566-line document becomes tractable after unifying claim roles and extraction, since this audit selected four representative valuation-spine labels |
| Next justified action | Execute a focused semantic target-unification program, then add one end-to-end valuation formalization/execution slice and rerun this same document audit |
| Not concluded | Document correctness, proof, complete assumptions, best repair, broad-corpus generalization, publication readiness, release readiness, or production reliability |

## Post-Run Red Team

The strongest alternative explanation is that this test is unfair because a
long applied proposal contains definitions, empirical claims, citations,
policy constructs, and equations that no generic prover should be expected to
certify automatically. That explains many abstentions, but it does not explain
the false refutation, inconsistent extraction of the same label, or silent
duplicate-file selection. Those are product correctness defects under the
stated orchestration mission.

The conclusion would materially improve if one shared typed obligation carried
exact file identity and claim role through every high-level surface, the
definition stopped entering theorem-refutation routes, and at least one
valuation branch automatically formalized and executed through an appropriate
installed specialist backend. A clean focused and full regression run would be
required for an engineering promotion.

The weakest part of this evidence is breadth of deep mathematical validation:
all tools were accounted for, but detailed source-faithful development focused
on four valuation-spine labels rather than every one of 178 labeled rows. This
is sufficient to reject mission completion because critical vetoes were found;
it is insufficient to estimate a whole-document success rate.

## Run Manifest

| Field | Value |
| --- | --- |
| Baseline git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` |
| Git state | Intentional dirty Phase 00-09 worktree; final commit occurs after this result is written |
| Main test command | `CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q` |
| Audit environment | `/home/chakwong/miniconda3/envs/tfgpu`, Python 3.11.15 |
| CPU/GPU | CPU-only; GPU intentionally hidden with `CUDA_VISIBLE_DEVICES=-1` |
| Data version | N/A; exact source digest recorded above |
| Random seed | `PYTHONHASHSEED=0`; no stochastic scientific experiment |
| Wall time | Full pytest suite: 40m48s; individual tool times retained in manifest |
| Audit artifact root | `.local/mathdevmcp/evidence/mission-audit-credit-card-20260716/` |
| Plan | `docs/plans/mathdevmcp-credit-card-full-mission-audit-plan-2026-07-16.md` |
| Result | `docs/plans/mathdevmcp-credit-card-full-mission-audit-result-2026-07-16.md` |

## Non-Claims

- A successful function invocation does not mean its mathematical answer is
  correct.
- The 48 invoked functions do not imply 48 successful mathematical tasks.
- Inapplicability is not a tool failure and is not mathematical evidence.
- The direct Lean diagnostic is not a formalization or proof of the document.
- The four selected labels do not establish whole-document coverage.
- The three generic-rigor repair records are not approved source edits.
- No source edit, publication action, default promotion, release authorization,
  or scientific claim is made by this audit.
