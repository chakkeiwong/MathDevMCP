# MathDevMCP Source-Bound Semantic Repair And Re-Audit Result

Date: 2026-07-16

Status: `MISSION_SUBSTANTIALLY_ADVANCED_WITH_REMAINING_GAPS`

Plan:
`docs/plans/mathdevmcp-source-bound-semantic-repair-and-reaudit-plan-2026-07-16.md`

Predecessor:
`docs/plans/mathdevmcp-credit-card-full-mission-audit-result-2026-07-16.md`

## Executive Decision

The six-phase repair program is complete. The source-bound P0 failures found by
the first credit-card audit are closed, the exact audit was repeated, all 65
current public tools are accounted for, CLI and FastMCP parity holds, and the
full CPU-only repository suite is clean at 1593 passed and 4 skipped.

The broader mission is not complete. This four-label test now demonstrates an
exploratory, rigorous, source-faithful bounded lane, including one deterministic
terminal-value algebra check. It does not demonstrate whole-document
mathematical correctness, economic validity, autonomous formalization of the
document's conditional-expectation and policy semantics, or publication
readiness. The appropriate decision is therefore
`MISSION_SUBSTANTIALLY_ADVANCED_WITH_REMAINING_GAPS`.

## Reviewed Execution

The plan received a skeptical local audit before implementation. Claude's
read-only Round 1 review returned `REVISE`: caller-authored claim roles needed
to be separated from source-evidenced roles, and the original 57-tool
comparator needed to be frozen before adding tools. Both findings were repaired.
Claude Round 2 returned `AGREE`. The review record is
`docs/reviews/mathdevmcp-source-bound-semantic-repair-plan-review-record-2026-07-16.md`.

## Source And Comparator

| Field | Result |
| --- | --- |
| Source | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex` |
| Source SHA-256 before and after | `68625df7943b4b3f6f358c0873cf976069299484f15e9f7990c2a54466e8ade8` |
| Focus labels | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv`, `eq:terminal-value-base` |
| Frozen comparator | Original 57 registered MCP tools, with the same applicability rules |
| Current registry | 65 registered MCP tools |
| Source mutation | None |
| Publication | Disabled throughout |

## Phase Results

| Phase | Result | Evidence |
| --- | --- | --- |
| 01. Claim semantics | Passed | Closed roles and authorities distinguish `source_evidenced_role`, `caller_asserted_role`, and `role_ambiguous`; caller assertions cannot suppress theorem counterexamples |
| 02. Exact target unification | Passed | V1/V2 proof audits, typed obligations, proof packets, audit/fix, rigor, CLI, facade, and MCP share the complete canonical source target; duplicate and stale bindings fail closed |
| 03. Assumptions and valuation | Passed for bounded slice | Exact denominator nonzero assumption is discharged; SymPy reports the source-bound terminal-value definition `algebraically_consistent` with diagnostic severity |
| 04. Agent surface | Passed with residual payload gaps | Eight relevant MCP tools added; resolver enum is discoverable; review, audit/fix, rigor, and document-audit compact responses meet 30,720-byte target |
| 05. Engineering closure | Passed | Dependency parsing, bounded `Popen` governance, FOC reconstruction, pilot evidence, source adapters, and test isolation repaired |
| 06. Re-audit and decision | Passed | Frozen and current inventories complete, parity exact, source unchanged, 227-test ownership slice and full suite pass |

## Before And After

| Measure | Before | After |
| --- | ---: | ---: |
| Frozen public tools accounted | 57 / 57 | 57 / 57 |
| Current public tools accounted | 57 / 57 | 65 / 65 |
| Applicable invocations | 48 | 56 (48 frozen plus 8 added) |
| Explicitly inapplicable | 9 | 9 |
| Missing or duplicate tool records | 0 | 0 |
| Invocation error envelopes | 0 | 0 |
| False definition refutations | 4 | 0 |
| Full suite | 1531 passed, 33 failed, 4 skipped | 1593 passed, 0 failed, 4 skipped |

The eight added tools are `capability_registry`, `claim_support_packet`,
`domain_templates`, `generate_template_obligations`,
`negative_evidence_label`, `proof_packet_label`, `resolve_agent_report`, and
`suggest_domain_templates`. No original tool was removed.

## Mathematical Results

The former terminal-value false-refutation veto is closed:

| Workflow | Re-audit status | Boundary |
| --- | --- | --- |
| `derive_from` | `diagnostic_only` | Source definition, not a theorem proof |
| `prove_or_counterexample` | `diagnostic_only` | No caller assertion can suppress a real theorem counterexample |
| `derive_or_refute` | `source_defined` | Definition recognized from validated exact source bytes |
| `prove_or_refute` | `source_defined` | Definition recognized without claiming economic truth |
| `assumptions_for` | `inconclusive` | Exact denominator condition is provided; route remains non-certifying |

The terminal-value adapter checked
`dTV = rho*dCF_next/(r_disc + lambda_attrition + q)`. The exact assumption
`r_disc + lambda_attrition + q != 0` discharged the denominator obligation.
SymPy reduced the cross-multiplication residual to zero and returned
`algebraically_consistent`. This establishes only scalar algebra under the
source-evidenced definition and declared domain. It does not establish finance,
calibration, causal, expectation, dynamic-policy, or publication validity.

## Extraction And Ambiguity

`eq:incremental-cash-flow` is identical across proof audit v1, proof audit v2,
typed obligation, proof packet, and audit/fix, including the terms for PPNR,
expected loss, capital charge, tax, and relationship value. Exact file and
source-digest selectors now propagate through public label workflows. Repeated
labels without an exact selector return ambiguity, and stale source digests
return unresolved source targets. The post-full-suite proof-packet repair also
removed the last reason-string-dependent stale-binding acceptance path.

## Agent Payloads

| Response | Before | After | 30,720-byte transport target |
| --- | ---: | ---: | --- |
| Review packet | about 366 KB | 7,454 bytes | Met |
| Audit/fix | about 359 KB | 4,479 bytes | Met |
| Rigor audit | 785,023 bytes | 2,907 bytes | Met |
| Document audit | public compact lane previously available | 25,235 bytes | Met |
| Proof packet | not MCP-exposed in comparator | 116,438 bytes | Not met |
| Negative-evidence packet | not MCP-exposed in comparator | 106,817 bytes | Not met |

Compact reports retain a digest-bound resolver to their full local artifacts.
The persisted detailed document artifact is 1,751,281 bytes; its compact public
response is intentionally not a lossy scientific certificate.

## Re-Audit Result

The repeated detailed document workflow remains `partial_coverage`:

| Measure | Before | After |
| --- | ---: | ---: |
| Available equation / labeled rows | 222 / 178 | 222 / 178 |
| Selected targets | 4 | 4 |
| Context graphs / semantic packets | 4 / 4 | 4 / 4 |
| Ranked branches | 8 | 8 |
| Blockers | 100 | 101 |
| Ready for backend | 2 | 1 |
| Blocked on typed assumptions | 2 | 3 |
| Promoted claims / ready repairs | 0 / 0 | 0 / 0 |

These count changes are explanatory, not promotion criteria. The repaired
system found stricter source-bound obligations and refused to promote them.
Failure classes remain branch execution pending, formalization blocked, and
mathematical blocked. The compact rigor workflow selected 4 of 178 labeled
equations and returned four diagnostic abstentions and no concrete repair.

CLI and normalized FastMCP structured content have the same digest,
`cb9fbb325328a282c8b9a58392a93d343a5951198e82d1074405218ecc2cc288`,
with no semantic differences. Raw FastMCP retains the documented `ok: true`
transport envelope. Status is `partial_coverage`; publication is disabled.

## Separate Evidence Ledgers

### Engineering Correctness

- The source-bound public contracts, schemas, resolver, compact artifacts, and
  stale/ambiguous selectors pass focused and repository-wide tests.
- The 227-test ownership slice passed in 20m37s.
- The full suite passed with zero failures in 45m09s.
- Registry accounting and parity are complete for the repeated audit.

### Mathematical Validity

- False theorem treatment of the source definition is closed.
- Complete source targets and exact provenance are preserved across repaired
  label workflows.
- One scoped scalar definition passed deterministic SymPy algebra under an
  exact nonzero-denominator assumption.
- No source theorem, economic claim, or document-wide claim was certified.

### Scientific And Product Interpretation

- The test supports bounded usefulness for source localization, claim-role
  control, assumption accounting, branch generation, external-tool routing,
  compact evidence handoff, and honest abstention.
- The test does not support autonomous whole-document mathematical development,
  complete domain coverage, finance validation, publication, or release.

## Remaining Gaps

| Priority | Gap | Evidence | Next justified repair |
| --- | --- | --- | --- |
| P1 | Detailed document workflow remains partial | 4 of 178 labels selected; 101 blockers; 0 promoted claims | Expand source-bound execution label by label with claim-specific evidence contracts |
| P1 | Conditional-expectation, causal, dynamic-policy, and economic semantics abstain | Three of four typed repair obligations are blocked on typed assumptions | Add reviewed specialist formalizations for probability law, integrability, information set, counterfactual paths, and dynamic semantics |
| P1 | Terminal-value template selection is not robust to source LaTeX | Direct `suggest_domain_templates` returned no match, although explicit template generation and validation worked | Normalize decorated LaTeX into the domain-template matcher and add the real source as a positive fixture |
| P1 | Detailed tree has legacy evidence binding | `evidence_schema_version=0-legacy`, `integrity_binding_status=unbound_legacy_evidence` prevents promotion | Carry current exact source, assumptions, native input, result, tool version, and edit binding through document-tree execution |
| P2 | Proof and negative-evidence MCP packets are too large | 116,438 and 106,817 bytes | Add compact projections with digest-bound resolution, preserving vetoes and provenance |
| P2 | Audit/fix is source-faithful but not yet action-complete | Four-label report returns `no_proposal`; two canonical targets remain uncertified | Add source-role-aware formalizers before presenting any concrete repair |
| P2 | Breadth is unmeasured | Four representative labels cannot estimate performance over 178 labeled equations | Build a stratified real-document benchmark with definitions, identities, theorems, expectations, estimators, and policy equations |

## Negative-Result Classification

| Observation | Class | What is weakened | What remains viable |
| --- | --- | --- | --- |
| Template auto-suggestion misses the exact source equation | Integration/normalization gap | Automatic domain routing on decorated LaTeX | Explicit template generation and bounded SymPy validation |
| Three typed obligations are blocked | Formalization/evidence gap | Autonomous execution breadth | Exact extraction, assumption discovery, branch planning, and honest abstention |
| Detailed evidence remains legacy-unbound | Evidence integration gap | Promotion from document-tree branches | Diagnostic search and compact handoff |
| Proof packets exceed transport target | Agent ergonomics gap | Direct packet consumption in small contexts | Full artifact correctness and digest-bound resolution pattern |

These findings do not refute the underlying mathematical document or the
exploratory architecture. They bound what this repaired program can claim.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `MISSION_SUBSTANTIALLY_ADVANCED_WITH_REMAINING_GAPS` |
| Primary criterion | Passed for the planned bounded repair: all P0 source-role, target, ambiguity, assumption, one valuation-execution, surface, parity, and engineering gates closed |
| Veto diagnostics | No false definition refutation, silent duplicate selection, stale proof-packet binding, source mutation, parity drift, unsupported promotion, or publication enablement remains in the exercised lane |
| Main uncertainty | How much of the other 174 labeled equations can be formalized and checked without target-specific semantic adapters |
| Next justified action | Repair template auto-selection and current evidence binding, compact proof packets, then run a stratified multi-label real-document benchmark |
| Not concluded | Whole-document correctness, complete/minimal assumptions, economic validity, optimal policy, broad-corpus generalization, publication readiness, or release authorization |

## Post-Run Red Team

The strongest alternative explanation is that the improved result is mostly
API contract repair rather than scientific progress. That is partly true: exact
source binding, claim-role discipline, and payload control are engineering.
They are nevertheless prerequisites for scientific progress because the prior
system refuted a definition and changed the equation across surfaces. The new
SymPy slice is genuine but deliberately narrow.

The conclusion would be overturned if a generic theorem counterexample were
suppressed by caller metadata, a stale or ambiguous source were silently
accepted, or the algebra result were presented as economic validation. Focused
negative tests and the repeated audit found none of those outcomes.

The weakest evidence remains scientific breadth. The full suite establishes
engineering consistency, not mathematical validity, and four selected labels
do not measure the 7,566-line document. The next program should target this
breadth rather than adding more governance machinery.

## Run Manifest

| Field | Value |
| --- | --- |
| Baseline git commit | `e297b477b18ab89f3223ed94f819ea33f924fac2` |
| Branch | `main` |
| Environment | `/home/chakwong/miniconda3/envs/tfgpu`, Python 3.11.15, x86_64 |
| CPU/GPU | CPU-only; GPU intentionally hidden with `CUDA_VISIBLE_DEVICES=-1` |
| Data/source version | Exact source SHA-256 recorded above |
| Seed policy | `PYTHONHASHSEED=0`; no stochastic scientific experiment |
| Re-audit command | `CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/run_credit_card_mission_audit.py --source docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex --artifact-root .local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair` |
| Re-audit invocation time | 575.44 seconds summed across tool records |
| Ownership tests | 227 passed in 1237.33s |
| Full-suite command | `CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q` |
| Full-suite result | 1593 passed, 4 skipped in 2709.33s |
| Audit artifact root | `.local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair/` |
| Audit manifest SHA-256 | `b9381406a04dfcedc58369cfdf8f83462d3e78613eae824b32bfb543f00a8a68` |
| Parity artifact SHA-256 | `f7654a22a972c0a9725383379ede8a14ea304e402f45703b873b8988f9eee10f` |

## Non-Claims

- A clean test suite is not a mathematical proof or scientific validation.
- A successful function invocation is not evidence that its mathematical
  answer is correct.
- The SymPy residual check is not a universal terminal-value theorem.
- The four focus labels do not establish whole-document coverage.
- Diagnostic gaps and generated template obligations are not source edits.
- No source edit, publication, release, default promotion, or scientific claim
  is authorized by this program.
