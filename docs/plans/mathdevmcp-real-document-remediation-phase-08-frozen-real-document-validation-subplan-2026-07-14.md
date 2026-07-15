# MathDevMCP Real-Document Remediation Phase 08 Subplan

Date: 2026-07-14

Status: `COMPLETE_PASS_SAFE_REAL_DOCUMENT_VALIDATION_CAPABILITY_COMPLETE`

## Phase Objective

Determine whether the repaired, publication-disabled workflow is safe and
substantively useful on the two frozen real documents that exposed the original
failures.

Phase 08 has three internal gates:

```text
P08A frozen source, extraction, and context
  -> P08B source-bound capability formalization and one eligible backend route
       -> P08C compact/detailed frozen workflow comparison
```

The gates are ordered. Parser success, context retrieval, a small payload, a
CAS simplification, or a reviewer verdict may not substitute for a source-bound
mathematical result. Publication and source editing remain disabled.

## Entry Conditions

1. Phase 07 is closed as `PASS_COMPACT_AGENT_FACING_PRODUCT` in
   `docs/plans/mathdevmcp-real-document-remediation-phase-07-compact-agent-facing-product-result-2026-07-14.md`.
2. The fresh Phase 07 result rereview is `VERDICT: AGREE` in
   `docs/reviews/mathdevmcp-real-document-remediation-phase-07-review-record-2026-07-14.md`.
3. Phase 00 publication quarantine, Phase 01 evidence identity, Phase 02
   extraction, Phase 03 context, Phase 04 branch isolation, Phase 05 specialist
   execution, and Phase 06 ledger/promotion boundaries remain retained inputs;
   none is treated as proof of Phase 08 capability.
4. The Phase 08 plan receives a skeptical independent read-only review with no
   material unresolved finding.
5. The frozen source digests below match before parsing. Drift invokes the
   two-version rule and blocks the current commands.
6. The existing dirty worktree is intentional. No unrelated change may be
   reverted, reformatted, committed, or published.

## Frozen Inputs

| Artifact | Required SHA-256 | Role |
| --- | --- | --- |
| `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8` | Frozen card source |
| `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1` | Frozen risky-debt source |
| `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json` | `d5f6705c2d5ed8779086aa38cddc380b31045801dddfd26c784e30123f96f3d6` | Diagnostic comparator only |
| `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json` | `6c3928f098262c801d9a94d23030f37df173fd873e232b8d49366fa89491e2aa` | Diagnostic comparator only |

The old reports are not certifying baselines. They expose prior target counts,
operator contamination, blocker volume, actionability, and response size.

### Pre-Registered Extraction Groups

| Group | Requested labels | Expected logical result |
| --- | --- | --- |
| `card_capability` | `eq:panel-cf-primitive`, `eq:incremental-cash-flow` | One complete label-scoped obligation per label; neither owns expectation or summation operators |
| `card_focus` | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | Three distinct obligations in request order; cash flow excludes NPV operators and sibling spans |
| `risky_capability` | `eq:risky-cash-flow`, `eq:cashflow-rate-derivative`, `eq:cashflow-total-k`, `eq:cashflow-total-b` | Four distinct complete obligations with exact source provenance |
| `risky_focus` | `prop:interior-foc` | Context container with exactly two ordered child obligations: `eq:foc-k`, `eq:foc-b`; no merged adapter target |

The retained Phase 02 comparator binds these overlapping obligation digests:

| Label | Retained obligation digest |
| --- | --- |
| `eq:incremental-cash-flow` | `7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0` |
| `eq:incremental-npv` | `d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac` |
| `eq:foc-k` | `d987e605da2d4e509d0d65289a56e9b7f5d121273543bdf74276b9fb4c23bba5` |
| `eq:foc-b` | `8d04797cf7e394624890ab2e0b0688f22d86d9194de94af3aa1407fb1a45edca` |

Newly exercised capability-label digests are measured from the same canonical
Phase 02 obligation contract and become part of the P08 source/extraction
artifact. No expected digest is invented before extraction.

### Pre-Registered Context Requests

Context requests are fixed before P08A output. The runner must not synthesize a
new predicate from observed candidates or tune subjects to obtain a
`source_supported` result.

Every request uses:

- `required_node_kinds`: `definition`, `assumption`,
  `notation_declaration`, `proposition`;
- `required_edge_kinds`: `input`, `include`, `contains`, `references`;
- `required_files`: the exact frozen source file that owns the obligation;
- the source-specific context budget registered below;
- `requirement_id`: `p08_context_<label-with-nonalphanumerics-as-underscores>`;
- the exact predicate and subjects in this table.

| Label | Requirement predicate | Exact subjects |
| --- | --- | --- |
| `eq:panel-cf-primitive` | Source declarations applicable to the one-period incremental cash-flow components, baseline contrast, scenario, and downstream policy are available. | `Delta CF`, `Delta PPNR`, `Delta EL`, `Delta Kchg`, `Delta Tax`, `Delta RelValue`, `a`, `pi`, `s` |
| `eq:incremental-cash-flow` | Source declarations applicable to the one-period incremental cash-flow components, baseline contrast, scenario, and downstream policy are available. | `Delta CF`, `Delta PPNR`, `Delta EL`, `Delta Kchg`, `Delta Tax`, `Delta RelValue`, `a`, `pi`, `s` |
| `eq:panel-npv-functional` | Source declarations applicable to acquisition cost, discounted cash flow, terminal value, conditioning information, scenario, and downstream policy are available. | `Delta NPV`, `C acq`, `Delta CF`, `Delta TV`, `delta`, `H`, `X d`, `pi`, `s` |
| `eq:incremental-npv` | Source declarations applicable to acquisition cost, discounted cash flow, terminal value, conditioning information, scenario, and downstream policy are available. | `Delta NPV`, `C acq`, `Delta CF`, `Delta TV`, `delta`, `H`, `I id`, `pi`, `s` |
| `eq:risky-cash-flow` | Source declarations applicable to risky-rate cash flow, tax, adjustment cost, capital, debt, and state variables are available. | `e`, `widetilde r`, `tau`, `psi`, `pi`, `k`, `k prime`, `b`, `b prime`, `z` |
| `eq:cashflow-rate-derivative` | The source definition and declarations needed to interpret the partial derivative of cash flow with respect to the risky-rate argument are available. | `eq:risky-cash-flow`, `e`, `widetilde r`, `tau`, `b prime`, `r` |
| `eq:cashflow-total-k` | The source declarations needed for the total derivative with respect to next-period capital, including investment and risky-rate dependence, are available. | `eq:risky-cash-flow`, `I`, `psi I`, `e widetilde r`, `widetilde r`, `k prime`, `b prime`, `z` |
| `eq:cashflow-total-b` | The source declarations needed for the total derivative with respect to next-period debt, including risky-rate dependence, are available. | `eq:risky-cash-flow`, `e widetilde r`, `widetilde r`, `tau`, `r`, `k prime`, `b prime`, `z` |
| `eq:foc-k` | The proposition assumptions and source declarations needed for the interior capital first-order condition and conditional continuation derivative are available. | `prop:interior-foc`, `m`, `bar e`, `beta`, `V star k`, `k prime`, `b prime`, `z`, `z prime` |
| `eq:foc-b` | The proposition assumptions and source declarations needed for the interior debt first-order condition and conditional continuation derivative are available. | `prop:interior-foc`, `m`, `bar e`, `beta`, `V star b`, `k prime`, `b prime`, `z`, `z prime` |

These are search requirements, not assertions that the source supplies every
item. Lexical overlap is only a candidate. `source_supported` still requires
the resolver's exact applicability and dependency-path contract; otherwise the
result remains ambiguous, not found, not searched, or candidate-only.

The obligation's own label is intentionally absent from every subject list,
and equation nodes are excluded from this declaration search. P08 verification
must additionally reject any explicit support candidate with
`target_span_match == true`, and require every accepted support source ref to
name the exact `required_files` entry. The current resolver uses
`required_files` chiefly for diagnostic scoping rather than node filtering, so
this file equality is a Phase 08 postcondition, not an assumed resolver
property. A focused self-evidence microfixture containing only a labeled target
equation and no independent declaration/assumption/proposition must terminate
as `candidate_assumption` or `not_found_after_search`, never `stated` or
`source_supported`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the repaired system preserve label/source/assumption boundaries and close at least one nontrivial source-local frozen-document subclaim through an appropriate external backend, while returning an actionable compact report? |
| Exact comparator | The four frozen byte identities above; retained Phase 02/P03 obligations for overlapping labels; the old Phase 09 reports as diagnostic behavior only; and the exact execution/verification code bytes bound by the run's `code-identity.json` and preserved `code-snapshot/`. HEAD `a85fbb676eb4d551a8d78a70a5043524f308b7b9` and dirty paths are provenance fields, not substitutes for content identity. |
| Primary safety criterion | Source digests match; extraction owns exact label rows without sibling contamination; context provenance is exact and bounded; engineering failures veto affected targets; publication and applicable source edits remain absent; compact/detailed status, promotion, veto, assumption, action, and evidence identities agree. |
| Primary substantive criterion | At least one pre-registered nontrivial real-document subclaim is constructed and checked by an appropriate external backend under explicit source-bound assumptions, with a persisted manifest binding source spans, obligation, formalization, variables/constants, native input, tool/version, raw result, and exact conclusion. A CAS route may earn only `backend_checked`; `formal_proof_certified` requires a proof-checking backend. |
| Veto diagnostics | Source or relevant code-byte drift; an unbound in-repo execution/verification module; duplicate/merged/cross-label extraction; incomplete source spans; invented context; backend execution before P08A; post-output target/rung/criterion change; omitted domain or held-constant assumption; identity-only checking of an unverified agent-written derivative counted as construction; backend/manifest mismatch; engineering failure followed by target shopping; compact omission; private path leak; publication/source edit. |
| Explanatory only | Test counts, target/blocker/branch counts, wall time, response bytes, tool availability, retrieval hits, and an identity simplification after the derivative is independently constructed. |
| What will not be concluded | A CAS `backend_checked` result is not mathematical proof. No whole-document proof, globally minimal assumptions, general CAS/Lean soundness, search completeness, best repair, source-document correctness, publication/default/release readiness, or mission completion. |
| Preserved artifacts | P08 run manifest; `code-identity.json` and exact relevant source snapshots; exact source/extraction/context records; capability ladder; formalization and external-tool ledger; backend-native request/result manifest when executed; compact/detailed responses; Phase 08 result and independent result review. |

## Pre-Registered Capability Ladder

Candidate order is fixed before observing Phase 08 outputs.

1. Risky-debt deterministic calculus, in this exact internal order:
   `eq:cashflow-rate-derivative`, `eq:cashflow-total-k`, then
   `eq:cashflow-total-b`.
2. Card-NPV scoped accounting consequence from `eq:panel-cf-primitive`, then
   `eq:incremental-cash-flow`.
3. A finite-support conditional-expectation bridge for one of
   `eq:panel-npv-functional`, `eq:foc-k`, or `eq:foc-b`, followed by a separate
   algebra/calculus check.

A candidate may be skipped only for a recorded pre-execution source,
formalization, mathematical-applicability, or supported-input-class blocker.
An unavailable executable, adapter error, timeout, malformed/truncated result,
or tuning defect is an engineering stop-and-repair event. It does not authorize
selection of an easier target. Stop the ladder after the first qualifying
source-bound closure.

Capability states are closed as follows:

| State | Meaning | Claim boundary |
| --- | --- | --- |
| `backend_checked` | A deterministic specialist backend constructed the scoped result from the exact bound input and its independent exact check passed under recorded assumptions. | Reproducible computational support for this scoped subclaim; not proof or publication authority. |
| `formal_proof_certified` | A proof-checking kernel accepted an exact source-bound theorem under explicit assumptions and project/toolchain identity. | Formal proof only for that theorem and assumptions; still not whole-document proof or publication authority. |
| `blocked` | A source, mathematical, assumption, formalization, or supported-input-class prerequisite is unresolved. | No result on truth or falsity. |
| `inapplicable` | A pre-execution reviewed route/candidate does not apply to the exact source obligation. | No result on truth or falsity. |
| `engineering_failed` | Execution, environment, timeout, truncation, malformed output, or manifest verification failed. | No mathematical evidence; repair the same candidate. |
| `not_reached` | An earlier ladder state stopped the phase. | No evidence for this candidate. |

Either `backend_checked` or `formal_proof_certified` may satisfy Phase 08's
pre-registered substantive-capability criterion. The result must say which one;
it may not abbreviate `backend_checked` to `certified`, `proved`, or
`mathematically valid`.

Pure commutativity, normalization, parser success, restating a source identity,
checking `lhs == lhs`, or generating a theorem whose proposition is `True`
does not satisfy substantive capability.

### Rung 1 Candidate 1 Formalization Contract

The exact source-local construction target is the partial derivative with
respect to `\widetilde r` of the only two `\widetilde r`-dependent terms in
`eq:risky-cash-flow`:

```text
g(rt) = bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))
d g(rt)/d rt = bp/(1 + rt)^2 * (-1 + tau/(1 + r))
```

Bindings:

| Formal symbol | Source symbol | Role |
| --- | --- | --- |
| `rt` | `\widetilde r` | Differentiated scalar |
| `bp` | `b'` | Held constant |
| `tau` | `\tau` | Held constant |
| `r` | `r` | Held constant |

Required assumptions are real scalar variables on the scoped calculation,
`1 + rt != 0`, `1 + r != 0`, and differentiability on that domain. The source
definition and the claimed derivative label must both be bound. The calculation
does not differentiate the composite risky-rate function with respect to `k'`
or `b'`; those chain-rule targets belong to later candidates.

The construction and equality check must be distinct in the artifact:

1. the selected backend constructs the derivative from `g` and `rt`;
2. the backend independently simplifies constructed derivative minus the
   source target to exact zero under the explicit domain;
3. an adversarial neighbor that flips a sign or drops one term must not pass;
4. a finite substitution diagnostic away from singularities is explanatory
   only and cannot replace the symbolic construction.

## External-Tool-First Ledger

| Tool | Considered role | Current evidence | Phase 08 selection boundary |
| --- | --- | --- | --- |
| SymPy 1.14.0 | Deterministic scalar differentiation and exact simplification | Installed in `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`; Phase 05 identity adapter is typed but has no derivative-construction contract | Preferred candidate only after a bounded derivative input/result adapter or equally closed direct route binds construction, assumptions, resource limits, and artifact bytes |
| SageMath 9.5 | Exact specialist algebra/calculus | Phase 05 live route is restricted to univariate polynomials over `QQ` | Not selected for rational differentiation unless a reviewed supported input class is added; polynomial success is not transfer evidence |
| Lean 4 | Final theorem certification | Exact binding contract exists; no Phase 08 Lean formalization yet | May be considered after an exact theorem statement/source/toolchain binding exists; not selected merely because Lean is installed |
| LeanSearch-v2 / LeanExplore | Premise retrieval | Retrieval only; environment availability has varied | Not useful before a Lean goal exists; cannot certify |
| jixia | Static Lean extraction | Diagnostic only | Not useful without scoped Lean source; cannot certify |
| Pantograph / LeanDojo | Lean proof-state/search interaction | Environment support has varied | Optional only after formalization; traces cannot certify |
| MathDevMCP native search | Orchestration, ledgers, routing, artifact/report generation | Phases 02-07 engineering contracts | Must not replace derivative construction or proof |

No new in-house differentiation or proof algorithm is authorized. A Phase 08
adapter repair must directly orchestrate an existing deterministic specialist
tool and explain any gap it closes.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Earliest diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Frozen source bytes | Master-plan pinned corpus; remeasured 2026-07-14 | Prevents comparator drift | New file silently replaces failed baseline | SHA-256 before parsing; two-version stop on mismatch | Hard binding |
| Dirty implementation bytes | Phase 08 necessarily exercises intentional uncommitted remediation code | HEAD plus a dirty-path list cannot reproduce the implementation that produced or verified an artifact | A later edit or an unrecorded dynamic import changes scientific behavior without changing HEAD | Snapshot relevant repo Python bytes before MathDevMCP import; enumerate loaded repo modules; compare before/after every command and before interpretation | Hard binding |
| Label groups/order above | Master pre-registration plus exact source labels | Prevents target shopping and cross-label merging | Easier or contaminated target selected post hoc | Dedicated extraction boundary and exact requested-label record | Hard binding |
| W1 uses `extract_document_derivation_obligations` | Function contract says it stops before semantic/backend work | Its artifact answers ownership/operator/span questions directly | `max_attempts=0` full workflow is mistaken for extraction-only | Assert `backend_request_count == 0`; no doctor/controller records | Reviewed route |
| W2 context budgets | Retained Phase 03 frozen budgets | Each source is one file and current byte limit covers its exact frozen bytes | Exhaustion is hidden as absence or inherited budget is too broad | Record traversed/unsearched files, bytes/nodes/edges, and terminal state | Baseline hypothesis, not promoted default |
| Card context budget | 1 file, 469,323 bytes, 4,096 nodes, 8,192 edges, 1 dependency expansion | Matches retained card source-specific P03 budget | Source growth or parser expansion exceeds coverage | Stop on any unsearched/exhausted state relevant to a claim | Reviewed baseline |
| Risky context budget | 1 file, 117,506 bytes, 4,096 nodes, 8,192 edges, 1 dependency expansion | Matches retained risky source-specific P03 budget | Same | Same | Reviewed baseline |
| Serial workers | Reproducible scientific baseline | Avoids scheduling as an explanation during first validation | Hides parallel-only bugs | Parallelism remains a later engineering adjacency, not Phase 08 evidence | Convenience baseline |
| Rung 1 candidate order | Master plan | Smallest source-local nontrivial derivative first | Success chosen after results | Capability ladder artifact records every candidate state | Hard binding |
| SymPy preference | Direct specialist fit for rational differentiation | Small deterministic expression; existing package version known | Existing identity adapter is mistaken for a derivative proof/certifier | Preflight must report current route gap; construction artifact required; successful state is at most `backend_checked` | Hypothesis pending route validation |
| 10 s / 256 KiB result / 1 MiB total capability artifact | Existing Phase 05 scalar timeout/output scale plus small target size | Ample for one four-symbol deterministic derivative without encouraging runaway work | Timeout reflects import/environment rather than mathematics; truncation hides evidence | One source-independent syntax/limit smoke plus exact target; no silent budget increase | Baseline hypothesis |
| CPU-only | Deterministic symbolic tools need no GPU | Avoids irrelevant device initialization | Hidden GPU/environment differences | Set `CUDA_VISIBLE_DEVICES=-1` before Python/backend imports | Reviewed default for P08 |
| Seeds | Deterministic extraction/context/CAS | No stochastic route is selected | Stochastic search slips in without replication | Run manifest says N/A; any stochastic route requires a new evidence contract | N/A with reason |
| Publication | Always disabled; no Phase 08 publication argument exists | Phase 08 is validation, not publication | Legacy master flags re-enable an output path | Surface scan and every response/decision asserts disabled/false | Hard boundary |

## Scope And Work Packages

### P08-W0: Runner And Contract Tests

Add a small Phase 08 runner only if needed to preserve canonical artifacts. It
may orchestrate existing public extraction/context APIs and, after P08A passes,
an explicitly reviewed specialist derivative route. It must support separate
subcommands so each gate can veto the next.

Required artifacts:

- `scripts/run_p08_frozen_validation.py`;
- a stdlib-only startup identity bootstrap in that runner which, before any
  `mathdevmcp` import, writes or verifies `code-identity.json` and the exact
  files under `code-snapshot/`;
- focused tests for exact source binding, requested-label order, no-backend W1,
  source-slice reconstruction, sibling exclusion, context budget accounting,
  self-label/target-span context non-support, exact support-file equality,
  capability candidate order, no target shopping, code-identity drift and
  unbound-dynamic-import rejection, and publication absence;
- a derivative adapter module/test only if the P08B preflight confirms the
  current registered routes cannot construct the pre-registered derivative.

The code-identity bootstrap has this closed contract:

1. At fresh-run creation, before importing project code, copy the runner and
   every regular `*.py` file under `src/mathdevmcp/` into
   `code-snapshot/<relative-path>` without following symlinks. Record relative
   path, byte length, SHA-256, HEAD, and dirty-path provenance in canonical
   `code-identity.json`. This deliberately snapshots a narrow scientific-code
   tree, not plans, reviews, logs, tests, or unrelated repository files.
2. The required minimum set is the runner plus
   `document_derivation_tree.py`, `derivation_target_extraction.py`,
   `latex_index.py`, `document_context_graph.py`, `context_evidence.py`,
   `document_derivation_response.py`, `mcp_facade.py`,
   `external_tool_adapters.py`, `external_adapter_contract.py`, and every
   derivative adapter/verifier introduced for P08B. Absence of a required file
   for a gate is a pre-execution blocker, not an omitted identity entry.
3. At the end of every subcommand, enumerate `sys.modules` entries whose
   resolved source file is a regular file inside this repository. Every loaded
   runner/`mathdevmcp` execution or verification module must map to an exact
   snapshot entry. Record the per-command loaded-module set and reject an
   unbound path, symlink escape, non-source loader without separately preserved
   bytes, or digest mismatch.
4. Rehash the runner and snapshotted implementation tree immediately before
   each production, verification, and interpretation command and again before
   that command writes its decision. Producer and verifier records must name
   the same code-identity digest. Code drift is a veto even when outputs happen
   to match.
5. Keep project imports out of runner module top-level scope so identity
   verification precedes them. Static adapter version strings and HEAD/dirty
   metadata are explanatory only and cannot satisfy this contract.

If a P08B preflight shows that a derivative adapter/verifier must be added or
changed, preserve the current attempt as diagnostic, review the repair, and
start a fresh run from P08A with a new code identity. No artifact set may mix
pre-repair P08A bytes with post-repair P08B/P08C bytes.

Run selection is equally closed. `freeze-extract --new-run` is the sole command
that accepts the shared artifact parent. It atomically creates a new regular
directory with a collision-resistant immutable `run_id` and returns canonical
JSON containing that `run_id`, the logical relative `run_root`, and their
binding digest. Every later subcommand requires the exact literal
`--run-root .local/mathdevmcp/evidence/p08-20260714/runs/<run-id>` returned by
that command. It must reject a parent directory, absent or reused creation
request, symlink in any path component, `current`/`latest` pointer, glob,
implicit newest-run lookup, run-id/root mismatch, or artifact/code identity
from another run. The supervisor records the literal path in every actual
command; a placeholder below is a plan-time notation only.

### P08-W1: Freeze And Extract

1. Verify the four frozen artifact digests.
2. Create and verify the code snapshot/identity before project imports; record
   commit, relevant dirty state, Python path/version, CPU-only setting, and zero
   backend requests.
3. Run the four extraction groups through
   `extract_document_derivation_obligations` only.
4. Reconstruct every owned source slice from the exact frozen bytes.
5. Verify complete lhs/rhs where required, exact label order, distinct digests,
   and excluded sibling spans/operators.
6. Write canonical `source-manifest.json`, `extraction.json`, and a W1 decision.

W1 passes only if all requested labels resolve exactly, all expected
obligations are valid and source-bound, the proposition container stays a
container, and `backend_request_count` is zero. Any drift, ambiguity, duplicate,
contamination, incomplete provenance, or backend record stops P08A.

### P08-W2: Resolve Context Without Mathematical Backends

1. Reopen and verify W1 bytes and source digests.
2. Build one entry-rooted dependency graph per frozen source under the exact
   source-specific budgets above.
3. Resolve explicit context requirements for each W1 obligation, keeping
   `source_supported`, `ambiguous`, `not_found_after_search`, `not_searched`,
   and `candidate_assumption` distinct.
4. Produce symbol/notation, source-assumption, candidate-assumption,
   mathematical-requirement, encoding-blocker, engineering, and interpretation
   lanes.
5. Record all considered/reachable/excluded/unsearched files and exact source
   refs. Do not call doctor, SymPy, Sage, Lean, retrieval, or a model.

W2 passes when source/context identity reconstructs, no relevant integrity or
engineering veto remains, no candidate is promoted to source support, and each
open capability/focus target has a complete next-discriminator record. A
bounded `not_searched` state is honest but blocks a claim that depends on the
unsearched context.

### P08-W3: Capability Preflight And Rung 1

1. Reopen P08A and select only the first pre-registered candidate not already
   blocked by source/formalization evidence.
2. Write the exact formalization, symbol map, assumptions, held-constant map,
   candidate/rung identity, external tools considered, selected route, and
   reason each other route was not used.
3. Check whether an existing registered route constructs the derivative and
   persists verifiable exact evidence. Identity-only checking is insufficient.
4. If the route gap is fixable locally, write/refresh a bounded P08B adapter
   repair section/subplan, add the smallest direct specialist wrapper and
   adversarial tests, and rereview before running the real candidate.
5. Execute exactly one candidate under the registered limits. Persist native
   input, raw output, structured result, request/result digests, tool/version,
   source/obligation/assumption bindings, resource outcome, and non-claims.
6. Independently reopen and verify the artifact before interpreting it.

An engineering failure repairs and reruns the same candidate; it does not move
the ladder. A mathematical/formalization/input-class blocker recorded before
execution may move to the next candidate. Stop at the first qualifying closure
or after the ladder is honestly exhausted.

### P08-W4: Rungs 2-3 Only If Justified

Rung 2 may start only after all rung-1 candidates are pre-execution
inapplicable/blocked for mathematical or formalization reasons. It must define
a nontrivial consequence beyond repeating the source component identity and
bind an explicit component/sign map.

Rung 3 may start only after the same rule for rungs 1-2. It requires a separate
finite-support law contract, normalized weights, conditioning event,
integrability, law-dependence/choice-independence statement, expectation-to-sum
bridge evidence, and a second algebra/calculus artifact. A finite-sum CAS check
alone cannot certify the expectation replacement.

### P08-W5: Frozen Agent-Facing Workflow

After the capability ladder stops without an unresolved engineering veto:

1. Run each focus group once through the raw document workflow with serial,
   publication-disabled, zero-backend-attempt diagnostic settings.
   The current raw workflow calls `doctor_report`, which may launch bounded
   local `--version`/package-availability probes for LaTeXML, Pandoc, Lean,
   Sage, and configured integrations. These are pre-registered operational
   provenance probes, not mathematical backend attempts. The runner must count
   and classify them separately, retain their command/timeout/outcome, and
   reject any non-version mathematical input or execution in P08C.
2. Compile `compact` and `detailed` from the same completed audit mapping so
   semantic parity is not confounded by two executions.
3. Persist the detailed artifact and return only logical artifact metadata in
   transport.
4. Verify exact target labels/order, complete global veto/assumption/action/ref
   inventories, one smallest action per blocked target, compact/detailed parity,
   no private-path leak, and no source/applicable edit.
5. Measure canonical and pretty JSON bytes. The compact target is 25,600 bytes
   per document; any overage preserves the full boundary and is recorded as a
   product issue, never repaired by omission.

W5 does not rerun the capability backend or claim that zero-backend focus
reports prove the documents. It validates the product surface over the frozen
targets after the separate capability decision.

The exact raw requests and expected response partition are:

| Document | Exact `focus_labels` caller order | Expected paginated `targets` order | Expected non-paginated context coverage |
| --- | --- | --- | --- |
| Card | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | The same three equation labels in source order | No context-only focus label; `missing_focus_labels` empty |
| Risky debt | `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | `eq:foc-k`, then `eq:foc-b` | `context_target_labels == [prop:interior-foc]`; `missing_focus_labels` empty |

The proposition is deliberately not a paginated mathematical target. The raw
workflow represents it as a separate `context_target`, while its two equation
children are the target/action records. Compact actionability therefore
requires one complete selected/fallback action for each blocked `eq:foc-k` and
`eq:foc-b` target. Proposition completeness is checked through the unpaginated
coverage/global inventories and the detailed artifact's exact context packet;
the plan does not require a nonexistent compact target action for
`prop:interior-foc`.

## Artifact Layout

Use a fresh, non-symlinked run directory under:

```text
.local/mathdevmcp/evidence/p08-20260714/runs/<run-id>/
```

The `run-id` is created once by `freeze-extract --new-run`; later gates never
discover or select a run by directory ordering. Every artifact contains the
same `run_id` and `run_binding_digest`, and verification rejects a record whose
logical root, code identity, or artifact binding belongs to a different run.

Required logical contents:

```text
run-manifest.json
code-identity.json
code-snapshot/scripts/run_p08_frozen_validation.py
code-snapshot/src/mathdevmcp/*.py
source-manifest.json
p08a/extraction.json
p08a/context.json
p08a/decision.json
p08b/capability-ladder.json
p08b/formalization.json
p08b/external-tool-ledger.json
p08b/backend/<candidate-id>/request.json       # only when executed
p08b/backend/<candidate-id>/native-input.*     # only when executed
p08b/backend/<candidate-id>/stdout.bin         # only when executed
p08b/backend/<candidate-id>/stderr.bin         # only when executed
p08b/backend/<candidate-id>/result.json        # only when executed
p08b/backend/<candidate-id>/manifest.json      # only when executed
p08c/card-compact.json
p08c/card-detailed.json
p08c/risky-compact.json
p08c/risky-detailed.json
p08c/parity-and-size.json
phase-decision.json
```

Content digests are required for sources, obligations, source/context refs,
formalization, backend-native inputs/results, and evidence supporting any
capability decision. They are also required for the execution and verification
code that constructs or interprets those artifacts. Ordinary logs, prose
plans, reviews, and command-transition receipts remain outside this identity
chain.

The Phase 08 result note must record the actual artifact root. Local absolute
paths remain in the run manifest only and must not appear in MCP/CLI transport.

## Exact Planned Commands

The exact selected Python is
`/home/chakwong/miniconda3/envs/tfgpu/bin/python3` (CPython 3.11.15). Every
Python command sets CPU-only mode before import.

### Preflight And Focused Engineering Checks

```bash
sha256sum \
  docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex \
  docs/risky-debt-maliar-deep-learning-lecture-note.tex \
  docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json \
  docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest \
  tests/test_document_derivation_real_regressions.py \
  tests/test_context_real_regressions.py \
  tests/test_document_derivation_response.py -q

python3 -m py_compile \
  scripts/run_p08_frozen_validation.py \
  src/mathdevmcp/document_derivation_response.py

git diff --check
```

If the runner or derivative adapter does not yet exist, its focused compile/test
path replaces the corresponding command before execution; absence is an
implementation task, not evidence that the scientific plan passed.

### P08A

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py freeze-extract \
  --artifact-root .local/mathdevmcp/evidence/p08-20260714 \
  --new-run
```

The command returns one canonical JSON object. Before any later launch, the
supervisor replaces `<returned-run-id>` below with the literal returned value
and records the expanded command. It does not use a shell `latest` lookup or
directory scan.

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py resolve-context \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py verify-p08a \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

### P08B

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py capability-preflight \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

Only when that command records `READY_EXACT_REGISTERED_ROUTE` for the current
candidate may the runner execute:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py capability-run \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id> \
  --candidate eq:cashflow-rate-derivative \
  --timeout-seconds 10 \
  --max-output-bytes 262144 \
  --max-artifact-bytes 1048576

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py verify-capability \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

The candidate argument is closed to the ladder state. Supplying a later
candidate while an earlier one is ready or has an engineering failure must be
rejected.

### P08C

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py frozen-workflow \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id> \
  --budget-profile smoke \
  --max-attempts 0 \
  --workers 1 \
  --target-limit 20

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py verify-final \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

No command contains the stale `--publication-mode`, experimental publication,
or `--promotion-gate-manifest` arguments.

## Required Checks And Reviews

1. Focused runner/adapter tests, then existing frozen extraction/context,
   response, publication-quarantine, evidence-reader, and Phase 06 promotion
   adjacency.
2. One mutation per primary binding: source digest, owned span, excluded sibling
   span, obligation digest, context dependency path, candidate order,
   differentiated variable, held constant, domain assumption, native input,
   tool/version, raw result digest, code snapshot byte, loaded-module path,
   run-id/root binding, cross-run artifact transplant, and compact
   veto/action/reference set.
3. Independent read-only plan review before P08A.
4. Focused review of any new derivative adapter before the real backend run.
5. One substantive independent result review before a Phase 08 mathematical or
   substantive-capability close claim.

Reviewers are read-only. They do not authorize publication, source edits,
default changes, release, external disclosure, or scientific claims beyond the
verified artifact.

## Evidence Ledgers

The result keeps three ledgers separate:

| Ledger | May conclude | May not conclude |
| --- | --- | --- |
| Engineering | Source/extraction/context/runner/manifest/response contracts behaved as tested | Mathematical correctness or scientific usefulness |
| Mathematical validity | For CAS, record only `backend_checked` computational support for the exact scoped conclusion under named assumptions; for a proof kernel, record `formal_proof_certified` for the exact theorem | CAS-as-proof, whole-document proof, omitted-assumption validity, or neighboring targets |
| Scientific interpretation | Whether one nontrivial real subclaim and the compact workflow meet the pre-registered Phase 08 criteria | General theorem-proving ability, best repair, or publication readiness |

Veto diagnostics are interpreted before speed, payload size, branch count, or
other secondary metrics.

## Required Phase Result

The Phase 08 result must include:

- actual commands, environment, commit/dirty state, CPU/GPU status, source
  versions, seeds, wall time, artifact paths, code-identity digest, and the
  producer/verifier loaded-module identity comparison;
- extraction/context comparison tables for every pre-registered group;
- a capability ladder table with `backend_checked`,
  `formal_proof_certified`, `blocked`, `inapplicable`,
  `engineering_failed`, or `not_reached` for every candidate;
- exact source-to-formalization symbol/assumption map for an executed candidate;
- backend request/native input/raw output/manifest verification or an explicit
  capability-incomplete reason;
- compact/detailed semantic parity and byte measurements for both documents;
- separate engineering, mathematical-validity, and scientific-interpretation
  decisions;
- a veto-first decision table and post-run red-team note.

Allowed Phase 08 statuses are:

- `PASS_SAFE_REAL_DOCUMENT_VALIDATION_CAPABILITY_COMPLETE`;
- `PASS_SAFE_REAL_DOCUMENT_VALIDATION_CAPABILITY_INCOMPLETE`;
- `BLOCKED_ENGINEERING_OR_PERMISSION`;
- `FAIL_UNSAFE_BOUNDARY`.

These are Phase 08 outcomes. Final program status belongs to Phase 09.

## Forbidden Claims And Actions

- Do not claim proof from extraction, context, retrieval, route plans,
  generated formalization, CAS construction/simplification, payload size, or
  review agreement. A successful CAS route is `backend_checked`, never
  `formal_proof_certified`.
- Do not change the target, candidate order, criterion, domain, assumptions,
  held constants, timeout, or output/artifact limit after seeing a result
  without a visible plan revision and scientific justification.
- Do not move to a later target after an engineering, timeout, malformed,
  truncation, environment, or tuning failure on the current target.
- Do not treat unavailable/unsupported/error/unknown as refutation.
- Do not enable publication, expose experimental publication, apply a source
  edit, produce an applicable repair, change a default, release, commit, push,
  install, use GPU, access network/model services, or run Claude under this
  subplan.
- Do not execute Sage/Lean/retrieval/proof-state tools unless the exact current
  candidate selects that route after the relevant preflight and review.
  P08C's bounded `doctor_report` executable-version probes are the sole
  exception: they may query `--version` for provenance but may not submit a
  mathematical target, import a proof project, search premises, or certify a
  claim.
- Do not overwrite or delete a prior P08 run. Ordinary failed attempts remain
  classified evidence in their fresh run directory.
- Do not alter the frozen documents or comparator reports.

## Exact Handoff Conditions

### P08A to P08B

P08B preflight launches automatically only when:

1. all four frozen artifact digests match;
2. the immutable run-id/root binding is exact and every P08A artifact belongs
   to that run without symlink or cross-run selection;
3. all extraction groups meet exact label/ownership/operator/span contracts;
4. every owned slice reconstructs from frozen bytes;
5. context graphs/manifests verify under the recorded budgets;
6. no relevant integrity/engineering veto remains;
7. candidate/source/context assumptions remain explicit;
8. backend request/execution count is zero;
9. P08A producer and verifier use the same complete code identity with no
   before/after drift or unbound loaded module;
10. P08A artifacts and decision are written and independently reopen.

### P08B to P08C

P08C launches automatically when the capability ladder has stopped with either:

- one verified qualifying source-bound `backend_checked` or
  `formal_proof_certified` result and no veto; or
- honest capability incompleteness after all reachable candidates are
  pre-execution inapplicable/blocked or the reviewed budget is exhausted,
  without unresolved engineering failure.

P08C must not launch over an unresolved implementation/environment/timeout/
manifest defect or code-identity drift. Capability construction, verification,
and interpretation must share the exact recorded code identity.

### Phase 08 to Phase 09

Phase 09 planning begins only after P08C, the Phase 08 result, all required
artifacts, and a substantive independent result review are complete. The
handoff does not authorize publication, defaults, release, or source edits.

## Stop And Repair Conditions

Stop the current gate and repair or ask for help when:

- a frozen digest drifts or the two-version comparator cannot be preserved;
- the runner or a relevant in-repo execution/verification module differs from
  its snapshot, is loaded without a snapshot entry, or changes between
  preflight, execution, verification, and interpretation;
- a command lacks the exact returned run root, discovers a run implicitly,
  encounters a symlink, or imports an artifact/code identity from another run;
- extraction merges labels, owns a sibling span/operator, duplicates a target,
  or lacks exact provenance;
- context invents support, collapses `not_searched`, or exceeds a relevant
  budget;
- a backend would run before P08A passes;
- the current candidate lacks an appropriate registered construction route;
- an adapter/runtime/timeout/truncation/manifest defect occurs;
- mathematical assumptions or held-constant choices cannot be resolved from
  source plus explicit candidate assumptions;
- compact/detailed semantics differ or a required boundary item is omitted;
- publication/source editing/default/release/external disclosure becomes
  necessary;
- the remaining choice materially changes the scientific criterion, project
  direction, permissions, privacy, irreversible state, or cost.

Ordinary local implementation/test defects enter the repair loop. They are not
reasons to abandon the phase. A missing derivative route triggers a bounded
external-tool adapter repair, not an agent-only derivation and not target
shopping.

## Skeptical Plan Audit

The pre-execution audit explicitly checked:

| Risk | Audit outcome |
| --- | --- |
| Wrong baseline | The old Phase 09 reports are diagnostic only; exact source/report bytes and retained P02/P03 bindings are the comparators. |
| Proxy promoted to criterion | Extraction, context, test count, branch count, compact size, and identity simplification are explanatory or veto-only; substantive capability requires backend construction and a bound artifact. CAS output is labeled `backend_checked`, not proof. |
| Missing stop conditions | Digest, extraction, context, route, engineering, manifest, parity, publication, and human-boundary stops are explicit. |
| Unfair/post-hoc comparison | Candidate and internal order are fixed; engineering failure cannot authorize an easier target. No method-speed ranking is attempted. |
| Hidden defaults | Source, labels, context budgets, workers, backend hypothesis, resource limits, CPU mode, seeds, and publication state are audited above. |
| Stale master commands | Removed `--publication-mode`, experimental publication, and promotion-gate arguments; W1 uses the dedicated extraction API instead of mislabeling `max_attempts=0` as extraction-only. |
| Environment mismatch | Python 3.11.15 and SymPy 1.14.0 are measured planning facts; Sage 9.5 evidence is narrow and not transferred to rational calculus. Actual tool/version is rebound at execution. |
| Dirty-code identity | HEAD and dirty-path metadata are insufficient. The runner snapshots the exact scoped implementation bytes before project import, records loaded repo modules, and vetoes drift through interpretation. Adapter repair forces a fresh P08A run. |
| Ambiguous attempt selection | Only fresh-run creation accepts the shared parent. It returns an immutable run root required literally by all later commands; latest-run, symlink, parent-only, and cross-run selection are vetoed. |
| Artifact does not answer question | W1 binds ownership; W2 binds context; W3 separates derivative construction from equality checking; W5 compares product views over the same audit. |
| Misleading pass | An identity-only CAS pass, source restatement, generated `True`, or missing assumption cannot meet capability. |
| Failure for wrong reason | Engineering/tuning failure stops and repairs the same target; it is not evidence against the mathematics. |

Local skeptical verdict: `PASS`. The plan is feasible through P08A with current
public APIs. P08B is feasible only after its preflight either identifies an
already closed derivative-construction route or introduces a bounded direct
specialist adapter with focused review. No real-document or backend execution
has occurred during this audit.

Independent read-only review initially found four material specification gaps:
pre-registration of context requests and the proposition/equation partition;
CAS language that crossed the proof boundary; target-span/self-evidence that
could support its own requirement; and exact identity of dirty implementation
bytes. After those repairs, the reviewer found one execution ambiguity in
selecting a run after multiple attempts. The final repair requires an immutable
literal run root for every command after fresh-run creation and rejects
implicit/latest/symlink/cross-run selection. The rereview reported no material
findings and returned `VERDICT: AGREE`. The durable record is
`docs/reviews/mathdevmcp-real-document-remediation-phase-08-plan-review-record-2026-07-14.md`.

At the end of Phase 08, run the required checks, write the phase result, draft
or refresh Phase 09, review it, and launch it automatically only if ready.
