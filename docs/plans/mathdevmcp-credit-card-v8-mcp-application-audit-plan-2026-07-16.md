# MathDevMCP Credit-Card v8 MCP Application Audit Plan

Date: 2026-07-16

Status: `COMPLETED`

Critical result:
`docs/reviews/credit-card-v8-mcp-audit/credit-card-v8-critical-gap-analysis.md`

Repair plan:
`docs/plans/mathdevmcp-credit-card-v8-mcp-gap-repair-plan-2026-07-16.md`

Target:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex`

Target SHA-256:
`e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`

## Objective

Apply every current public MathDevMCP tool to the v8 credit-card proposal when
the tool's input contract can be derived honestly from the source. Classify
tools that require absent code, literature mappings, temporal bindings, or
other inputs as inapplicable instead of fabricating inputs. Generate readable
Markdown reports, inspect the raw and rendered outputs critically, identify
remaining engineering, mathematical, and agent-product gaps, and write a
detailed repair plan.

This is a new source-bound audit. Results from
`credit_card_npv_component_proposal.tex` are a product comparator, not evidence
about v8.

## Source-Bound Scope

The applicability-complete tool inventory uses all current registered MCP
tools. Deep document inspection uses nine labels chosen to cover distinct
source-evidenced mathematical roles:

| Label | Source role | Why selected |
| --- | --- | --- |
| `eq:panel-npv-functional` | conditional value functional | expectation, information set, horizon, scenario, policy, and terminal value |
| `eq:incremental-cash-flow` | accounting identity | multiline extraction and source-role fidelity |
| `eq:pd-lgd-ead` | accounting/risk identity | multiplicative risk decomposition without independence overclaim |
| `eq:balance-stock-flow` | stock-flow identity | timing, signs, and component exhaustiveness |
| `eq:terminal-value-base` | transparent placeholder definition | denominator domain and bounded valuation formalization |
| `eq:ss-bellman` | proposed assembly derivation | belief-state control, expectation, policy, and feasibility semantics |
| `eq:causal-cashflow-object` | causal estimand/object | counterfactual and identification boundary |
| `eq:experiment-late` | local causal estimand | ratio domain, exclusion, monotonicity, and local-population scope |
| `eq:randomization-assumption` | identification assumption | role handling and operational violation diagnostics |

The roles above were checked against the surrounding v8 prose. A role is an
interpretation boundary for the audit; it is not a proof certificate.

## Skeptical Plan Audit

### Wrong baseline

The repaired audit of the unversioned proposal is not a v8 baseline. V8 has a
different digest, 8,963 lines, additional dynamic-control and experimental-
design content, and different label neighborhoods. The comparator is used only
to detect product regressions such as lost file selectors or false definition
refutations.

### Universal-applicability flaw

Several MCP functions require a bound implementation file, Python code,
literature theorem assumptions, or explicit temporal maps. Passing invented
values would create false coverage. Every current tool must instead have one
invocation record or a specific applicability classification.

### Role-inference flaw

Equality syntax does not identify an identity, definition, theorem, estimand,
or assumption. Deep interpretation may use a role only where surrounding
source prose supports it. Generic theorem behavior remains the default for
unbound expressions.

### Duplicate-label and sibling-contamination risk

The source directory contains historical versions with repeated labels. All
public paths that accept exact file and source digest must receive both. Legacy
reports that lack those selectors will be run only to test the real public
contract; any sibling selection is a veto on their source-specific output, not
an acceptable workaround.

### Proxy-promotion risk

Tool invocation count, report count, payload size, backend availability,
branch count, gap count, and process exit status are explanatory. They cannot
establish mathematical correctness, causal identification, economic validity,
or repair readiness.

### Whole-document illusion

Nine labels span materially different roles but do not cover all labeled
equations in the 8,963-line source. Whole-file inventory counts and selected-
scope coverage must remain separate. The audit may find a decisive defect; it
may not estimate whole-document correctness from this sample.

### Artifact fitness

Raw JSON is required for exact evidence, but multi-megabyte JSON is not an
agent-consumable report. Native Markdown renderers will be used where present;
packet and inventory results will receive compact Markdown summaries that link
to digest-bound local evidence.

### Audit decision

The plan survives skeptical review because it uses the exact v8 bytes, checks
nine source-supported roles, accounts for inapplicable tools without invented
inputs, preserves raw evidence, and forbids promotion from operational or proxy
metrics. Execution may proceed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Do all current MCP tools have an honest v8 invocation or applicability record, and do exact-file public surfaces agree without source contamination or transport drift? |
| Mathematical question | Can the system preserve nine source-evidenced roles, exact targets, assumptions, and non-claims while routing supported checks and abstaining on unsupported semantics? |
| Primary criterion | Complete current-tool accounting; unchanged source digest; exact target/file/digest on supported label workflows; readable reports; no false proof/refutation/repair/publication; critical gap ledger tied to output evidence. |
| Veto diagnostics | Wrong historical file selected; incomplete multiline target; definition/identity/assumption treated as a free-variable theorem without source qualification; caller metadata suppresses a valid theorem counterexample; unsupported causal/policy semantics promoted; source mutation; publication enabled; CLI/MCP semantic divergence. |
| Explanatory only | Tool, test, label, branch, gap, proposal, blocker, byte, runtime, and benchmark counts. |
| Will not be concluded | Whole-document correctness, complete/minimal assumptions, causal identification, economic validity, optimal policy, best repair, broad-corpus validity, publication readiness, release readiness, or production deployment. |
| Raw artifacts | `.local/mathdevmcp/evidence/credit-card-v8-mcp-audit-20260716/` |
| Markdown artifacts | `docs/reviews/credit-card-v8-mcp-audit/` |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Nine representative labels | V8 source roles and prior real-document gaps | Covers identity, definition, expectation, policy, causal, estimator, and assumption semantics | Misses other mathematical families | Report selected/available counts and non-claim | Reviewed audit sample |
| Current 65-tool MCP registry | `MCP_TOOL_SPECS` at commit `494d200` | Defines supported agent-facing inventory | Registry may change during execution | Freeze name list and compare final registry | Reviewed scope |
| Exact file plus source digest | V8 digest and duplicate-label history | Prevents silent historical-version selection where supported | Some legacy workflows lack selectors | Inspect returned provenance for every label report | Required binding |
| SymPy for scalar terminal-value algebra | Existing reviewed adapter | Smallest deterministic supported route | Algebra may be misread as finance validation | Require diagnostic severity and finance non-claims | Scoped baseline |
| `standard`, max 3 attempts, one worker | Existing document-tree audit defaults | Comparable bounded exploration without concurrency ambiguity | Budget may be too small for complex targets | Record pending branches and do not infer impossibility | Convenience baseline |
| CPU-only | No GPU method is in scope | Removes irrelevant device state | None material to mathematical audit | Set `CUDA_VISIBLE_DEVICES=-1` | Convenience choice |

## Planned Markdown Outputs

- `credit-card-v8-mcp-tool-application.md`
- `credit-card-v8-rigor-audit.md`
- `credit-card-v8-audit-and-fix.md`
- `credit-card-v8-derivation-tree-audit.md`
- `credit-card-v8-assumption-audit.md`
- `credit-card-v8-derivation-audit.md`
- `credit-card-v8-proof-and-negative-evidence-packets.md`
- `credit-card-v8-critical-gap-analysis.md`

## Execution Ladder

1. Freeze source and registry identities.
2. Run the applicability-complete public MCP audit using v8-derived inputs.
3. Generate native Markdown for exact-file rigor, fix, and derivation-tree
   workflows over the nine-label scope.
4. Generate assumption and derivation reports through their current public
   contracts and audit their returned provenance for sibling contamination.
5. Build exact-file proof and negative-evidence packets for each selected
   label, retaining raw JSON and a compact Markdown ledger.
6. Exercise CLI/FastMCP parity for the compact document workflow.
7. Inspect extraction, role, assumptions, backend attempts, evidence binding,
   actionability, payloads, and non-claims before writing conclusions.
8. Write the critical gap analysis and a separate repair plan.

## Stop Conditions

- Stop interpreting a report if its source provenance does not bind to v8.
- Stop mathematical promotion if an identity, definition, estimand, or
  assumption is routed as a generic theorem without source evidence.
- Stop backend interpretation when assumptions, types, target identity, or
  supported semantics are absent.
- Stop and preserve evidence on any source mutation, publication enablement,
  or public-surface parity divergence.
- Do not install packages, use networked retrieval, edit the target source,
  apply proposed repairs, or authorize publication/release.

## Completion Conditions

The audit is complete when all current tools are accounted for, the Markdown
set exists, raw artifacts are digest-bound, source identity is unchanged,
outputs have been critically inspected, remaining gaps are recorded with
evidence, and a detailed repair plan has been written and locally checked.
