# MathDevMCP Source-Bound Semantic Repair And Re-Audit Plan

Date: 2026-07-16

Status: `COMPLETED`

Result:
`docs/plans/mathdevmcp-source-bound-semantic-repair-and-reaudit-result-2026-07-16.md`

Predecessor result:
`docs/plans/mathdevmcp-credit-card-full-mission-audit-result-2026-07-16.md`

Target document:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

## Objective

Repair the concrete mission gaps exposed by the 2026-07-16 credit-card audit,
then rerun the same applicability-complete public-tool audit against the same
source, focus labels, questions, backend policy, and applicability rules. The
program must preserve exploratory breadth while preventing source definitions,
identities, diagnostics, or assumptions from being silently reinterpreted as
free-variable theorems.

The program is successful only if it produces source-bound behavior that is
both more useful and more mathematically honest. It must not obtain a cleaner
report by suppressing counterexamples, weakening validation, hiding ambiguity,
or relabeling blocked branches as successful.

## Entry Conditions

- Baseline commit:
  `e297b477b18ab89f3223ed94f819ea33f924fac2`.
- Source SHA-256:
  `68625df7943b4b3f6f358c0873cf976069299484f15e9f7990c2a54466e8ade8`.
- Prior audit: 57 public MCP tools accounted for, 48 invoked, 9 explicitly
  inapplicable, and no final-manifest invocation errors.
- Prior main workflow: `partial_coverage`, 4 selected targets, 8 ranked
  branches, 100 blockers, 2 typed obligations ready for a backend, 2 blocked on
  missing typed assumptions, 0 promoted claims, and 0 ready repairs.
- Prior full suite: 1531 passed, 33 failed, 4 skipped in 40m48s.
- The exact prior audit harness remains available at
  `/tmp/run_mathdevmcp_credit_card_tool_audit.py`; it is a runtime artifact,
  not production code.
- The worktree was clean at lane start.

## Skeptical Plan Audit

### Wrong baseline risk

The comparator is the exact 2026-07-16 audit artifact, not Phase 09, a focused
test count, or a newly simplified harness. Every re-audit comparison must state
the prior and repaired values and explain any registry-count or input-schema
change.

### Source-role inference risk

An equality string alone does not establish that a statement is a definition.
Blindly inferring `definition` from assignment-like syntax would suppress valid
counterexamples and weaken theorem checking. The repair must distinguish
`source_evidenced_role`, `caller_asserted_role`, and `role_ambiguous`. A role
may change proof routing only when an exact source span plus file/content
identity provides evidence for that role. A caller assertion is diagnostic
context and cannot suppress theorem/counterexample routing. The same generic
equality without a source-evidenced role must retain current theorem/
counterexample semantics.

### Proxy-promotion risk

No reduction in blocker count, report size, missing-assumption count, test
failures, or `refuted` statuses is itself a mathematical success criterion. A
status change passes only when the source claim role, exact source target, and
result boundary are correct.

### Extraction substitution risk

The repaired document-tree extractor already reconstructs the selected rows
correctly. Replacing it or creating a third extractor would increase semantic
drift. High-level consumers must converge on the validated label-scoped
obligation contract, with adapters only where required for backward
compatibility.

### Duplicate-label risk

The directory contains historical versions with repeated labels. A temporary
single-file copy can make one workflow appear correct while leaving the public
API ambiguous. Exact file/content identity must be accepted or propagated on
every repaired label-based public path, and an unqualified ambiguous lookup
must fail visibly.

### Formalization-overclaim risk

A valuation template can state obligations and translate a small algebraic
projection; it cannot prove the economic validity of terminal value, causal
identification, integrability, or policy optimality. The first execution slice
is limited to the explicitly declared placeholder definition and denominator
domain. It must retain those non-claims.

### Surface-expansion risk

Adding every CLI command to MCP would enlarge the registry and the repeated
audit without establishing usefulness. Only agent-relevant capabilities needed
for this source-bound lane should be exposed. Operator/release commands may
remain CLI-only when the distinction is documented and machine-discoverable.

### Full-suite attribution risk

The prior 33 failures include cascades, order-sensitive failures, and genuine
regressions. The plan must repair root causes, rerun focused cases in isolation
and grouped order, and use the full suite only after focused ownership is
established.

### Audit decision

The program is executable if independent review agrees that the phase order,
claim-role boundary, source-identity contract, exact re-audit comparator, and
stop conditions are sound. Any review finding that would allow false
definition acceptance, silent first-match lookup, or proxy promotion is
material and must be repaired before implementation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can all repaired public surfaces consume one exact source-bound target contract without regressions, silent ambiguity, or release-checker false positives? |
| Mathematical question | Can the system distinguish a source-bound definition/identity from a theorem, discharge expression-specific domain assumptions, and execute the smallest supported valuation check without claiming economic validity? |
| Exact comparator | The prior 2026-07-16 57-tool manifest, source digest, four focus labels, applicability classifications, detailed document-tree result, rigor result, parity check, and full-suite result. |
| Primary pass criterion | P0 source-role, extraction, and duplicate-label vetoes are closed; explicit denominator assumptions discharge exact denominator obligations; at least one source-bound valuation definition route executes through an installed deterministic backend with correct non-claims; relevant agent-facing capability and resolver schemas are discoverable; focused root failures pass; a frozen like-for-like audit over the original 57 tools and a separate current-registry delta audit are run, and every remaining gap is recorded. |
| Veto diagnostics | A theorem counterexample is suppressed without an explicit source role; a caller-authored role without source provenance becomes certified evidence; incomplete multiline extraction reappears; an ambiguous label silently selects a file; unsupported valuation semantics become proof; external-tool absence becomes refutation; publication becomes enabled; source bytes change; public response leaks private absolute paths; parity diverges. |
| Explanatory only | Tool count, branch count, blocker count, payload bytes, runtime, test totals, benchmark totals, and backend availability. |
| Will not be concluded | Whole-document correctness, economic validity of the terminal-value model, complete/minimal assumptions, causal identification, optimal policy, general valuation proving, broad-corpus validity, publication readiness, or release readiness merely from local checks. |
| Artifacts | This plan; a Claude review bundle and review record; focused test output; versioned local re-audit artifacts under `.local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair/`; and a final result under `docs/plans/`. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Promotion status |
| --- | --- | --- | --- | --- | --- |
| Explicit closed claim-role enum plus evidence authority | Prior false-refutation finding and Claude R1 | Prevents implicit or caller-asserted semantic reinterpretation | Too-coarse roles or caller metadata may hide theorem obligations | Unit tests for source-evidenced, caller-asserted, ambiguous, theorem, definition, identity, assumption, estimator, and invalid roles | Reviewed implementation default after plan review |
| `theorem` behavior when no role is supplied | Backward-compatible generic workflows | Preserves valid counterexample behavior | Source callers may omit role and still misuse the tool | Re-audit must supply source-bound role; generic regression must still refute a false theorem | Compatibility default |
| Exact file plus source digest for ambiguous labels | Prior duplicate-label finding | Binds the statement being audited | Digest can go stale after edits | Ambiguous fixture and stale-digest tests | Reviewed safety default |
| Validated label-scoped obligation as canonical document target | Phase 02/08 repaired contract | It already preserves complete row ownership and bytes | Legacy consumers may expect old row shape | Cross-surface parity test on `eq:incremental-cash-flow` | Reviewed default |
| SymPy for the first terminal-value algebra projection | Installed deterministic backend and scalar expression | Smallest available specialist check | Algebra pass could be misread as economic validation | Required role/domain non-claims and denominator-veto test | Scoped baseline route |
| Valuation template limited to placeholder definition and finite-horizon DCF obligations | Credit-card source and prior missing-template finding | Directly addresses tested domain without broad invention | Template could become a generic finance oracle | No causal/dynamic-policy proof status; unsupported constructs abstain | Hypothesis under target-specific tests |
| Add only agent-relevant missing MCP capabilities | Prior CLI/MCP split | Keeps registry purposeful | Registry expansion changes the repeat-audit count | Registry diff and applicability accounting | Reviewed product choice |
| Compact summary plus resolvable evidence for large repaired reports | Existing document-response pattern | Protects agent context without deleting evidence | Compaction could omit vetoes or assumptions | Byte-budget and lossless resolver tests | Reviewed product pattern |
| CPU-only repeated audit and tests | No GPU method in scope | Avoids irrelevant device state | None scientifically material here | Set `CUDA_VISIBLE_DEVICES=-1` | Convenience choice |

## Phase 01: Canonical Source Claim Contract

### Objective

Introduce one typed, source-bound claim descriptor that carries role, role
evidence authority, exact source span, file/content identity, label, target
identity, and evidence boundary through generic high-level and low-level
proof/derivation workflows.

### Required artifacts

- a small claim-semantics module with a closed role enum, closed evidence-
  authority enum, exact source-span validation, and conflict detection;
- additive optional public arguments for claim role/source binding;
- role-aware results for `derive_from`, `prove_or_counterexample`,
  `derive_or_refute`, and `prove_or_refute`;
- focused unit, facade, server, CLI where applicable, and audit regression
  tests.

### Required behavior

- only `source_evidenced_role` records with a validated exact source span and
  file/content identity may keep `definition` and `identity` targets out of
  free-variable theorem refutation;
- `caller_asserted_role` is diagnostic context and does not change proof
  routing; `role_ambiguous` fails closed and requests source evidence;
- results remain diagnostic/domain-validation records, not proofs of the
  definition's scientific validity;
- caller-authored role metadata, even with a caller-supplied path/digest, cannot
  acquire routing or certification authority unless the recorded source span
  is read and validates the role evidence;
- absent role retains existing theorem behavior and can still be refuted by a
  concrete counterexample;
- invalid or conflicting roles fail closed.

### Checks

- focused claim-semantics and four-workflow tests covering source-evidenced,
  caller-asserted, ambiguous, conflicting, and stale-span cases;
- facade/server schema parity;
- exact credit-card terminal-value and cash-flow projections;
- false theorem regression proving counterexample behavior is preserved.

### Handoff

Phase 02 begins only if both source-role and generic-theorem regressions pass.

## Phase 02: Exact Target And Extraction Unification

### Objective

Make the validated label-scoped obligation the canonical input to document
rigor, proof-audit, fix, derivation, typed-obligation, and proof-packet paths,
with exact file selection and explicit ambiguity/stale-digest results.

### Required artifacts

- adapters from the canonical obligation to legacy audit structures;
- additive file/source-digest parameters through affected CLI/facade/MCP paths;
- proof-packet provenance repair;
- complete multiline parity and ambiguous-label regression tests.

### Required behavior

- every repaired public workflow returns the same complete
  `eq:incremental-cash-flow` target;
- no public high-level lookup silently chooses among historical files;
- proof packets expose exact top-level source provenance;
- the rigor audit no longer proposes repairs based on truncated continuation
  fragments;
- existing unique-label callers remain compatible.

### Checks

- label-scoped extraction, proof audit, derivation audit, audit/fix, rigor,
  proof-packet, facade/server, and real-document tests;
- cross-surface target digest equality;
- duplicate-label and stale-source-digest negative tests.

### Handoff

Phase 03 begins only when the extraction P0 veto and silent-ambiguity P0 veto
are both closed.

## Phase 03: Expression-Aware Assumptions And Valuation Execution

### Objective

Normalize explicit assumptions against expression-specific backend
preconditions, add bounded valuation-domain templates, and execute one
source-bound terminal-value definition check through an installed specialist
backend.

### Required artifacts

- expression-aware assumption normalization/discharge records;
- `valuation_terminal_value_v1` and `valuation_finite_horizon_dcf_v1` templates
  with obligations, provenance, diagnostic routes, and non-claims;
- a target-specific formalization adapter for the scoped scalar placeholder;
- tests showing successful denominator discharge, zero-denominator veto, and
  abstention on unsupported expectation/policy semantics;
- source-bound backend evidence for the terminal-value projection.

### Required behavior

- `r_disc + lambda_attrition + q != 0` discharges the exact denominator
  precondition;
- generic text such as `denominator is nonzero` remains only when no expression
  can be identified;
- backend execution establishes algebraic consistency under the declared
  definition/domain, not economic truth or theoremhood;
- unsupported conditional expectation, causal, and policy objects abstain.

### Checks

- assumption discovery, domain template/formalization, SymPy adapter, high-level
  workflow, and credit-card integration tests;
- exact source digest and role carried into the backend attempt/evidence.

### Handoff

Phase 04 begins only if one end-to-end valuation slice executes and all
scientific non-claims remain visible.

## Phase 04: Agent Surface, Resolver, Payload, And Documentation Repair

### Objective

Expose the source-bound workflow coherently to agents, make resolver vocabulary
discoverable, compact large adjacent reports without evidence loss, and align
the top-level mission wording.

### Required artifacts

- a machine-readable capability classification covering MCP and intentional
  CLI-only commands;
- MCP exposure for agent-relevant domain-template suggestion/generation and
  proof/negative-evidence packets, or a documented reviewed reason for each
  capability that remains CLI-only;
- resolver collection enums in public schema/help/error output;
- compact modes or bounded summary views for rigor, audit/fix, and review
  packets with lossless evidence references;
- updated top-level README mission language.

### Required behavior

- all registered tools remain accounted for after any registry change;
- compact views preserve status, exact source, assumptions, vetoes, selected
  action, evidence references, and non-claims;
- resolver errors enumerate valid collections;
- product identity is exploratory and rigorous, while parser/status language
  may remain conservative where technically appropriate.

### Checks

- MCP registry/server/README parity;
- CLI/MCP capability classification tests;
- payload byte budgets and resolver round trips;
- documentation search and examples.

### Handoff

Phase 05 begins only if the agent surface is internally discoverable and no
compaction boundary loses decisive evidence.

## Phase 05: Engineering Root-Failure Repair

### Objective

Repair the independently observed repository failures without changing
scientific claims or accepting brittle tests as implementation truth.

### Required artifacts and checks

- dependency-name parsing that understands pinned requirement strings;
- subprocess governance analysis that accepts reviewed explicit deadline/kill/
  bounded-wait control flow for `Popen` while still rejecting genuinely
  unbounded calls;
- FOC reconstruction repair and regression;
- real-local pilot evidence-class/source-adapter contract repair;
- grouped-order tests for prior Phase 03/09 isolation failures;
- focused release, benchmark, pilot, and source-adapter suites.

### Handoff

Phase 06 begins only after focused root tests pass in isolation and grouped
order. A remaining unrelated full-suite failure is recorded, not hidden.

## Phase 06: Exact Re-Audit And Final Decision

### Objective

Rerun the same public-function audit and parity check against the unchanged
credit-card source, then rerun the full CPU-only suite and record every
remaining mission gap.

### Re-audit invariants

- same source file and verified SHA-256;
- same four focus labels;
- same questions, formulas, backend preference, applicability rules, and
  publication-disabled boundary;
- a frozen like-for-like accounting view over the exact original 57 tool names;
- a separate current-registry delta view for added, removed, or schema-changed
  surfaces;
- same CLI/facade/FastMCP parity check;
- any additive source-role/file-identity inputs are explicitly listed as the
  repaired contract, not hidden as a comparator change;
- prior and new raw artifacts remain separate.

### Commands

The versioned repair harness will emit both inventory views. New tools cannot
change a frozen-view count, pass rate, or applicability denominator.

The harness will use:

```text
CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_credit_card_mission_audit.py \
  --source docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex \
  --artifact-root .local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair
```

```text
CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q
```

### Required final artifact

`docs/plans/mathdevmcp-source-bound-semantic-repair-and-reaudit-result-2026-07-16.md`

It must contain:

- before/after tool accounting and output sizes;
- a frozen original-57 like-for-like result plus a separate current-registry
  delta inventory;
- before/after source-role, extraction, ambiguity, assumption, template,
  execution, payload, and full-suite results;
- separate engineering, mathematical, and interpretation ledgers;
- a decision table;
- negative-result classification;
- a run manifest;
- post-run red-team analysis;
- explicit remaining gaps and non-claims;
- one of `MISSION_ACCOMPLISHED_FOR_BOUNDED_TEST`,
  `MISSION_SUBSTANTIALLY_ADVANCED_WITH_REMAINING_GAPS`, or
  `MISSION_NOT_YET_ACCOMPLISHED`, justified by veto-first evidence.

## Review And Repair Loop

1. Run local structural checks on this plan.
2. Submit a compact plan-review bundle to Claude through the approved
   read-only review gate.
3. If Claude is unavailable, record the probe/gate result and perform a fresh
   skeptical Codex review; Claude unavailability is not plan agreement.
4. Patch every material, feasible finding visibly and rerun focused plan
   checks.
5. Repeat review only when the repair materially changes the evidence contract,
   phase boundary, or claim boundary; maximum five rounds for the same blocker.
6. Start implementation only after the plan is locally coherent and the
   independent verdict is `AGREE` or a bounded fallback is explicitly accepted
   with local evidence carrying the burden.

Round 1 review returned `REVISE` with two material findings: distinguish
source-evidenced roles from caller assertions, and separate the frozen 57-tool
comparison from registry expansion. Both repairs are incorporated above and
were confirmed by Claude R2 with `REVIEW_STATUS=agreed` and `VERDICT=AGREE`.

## Forbidden Claims And Actions

- Do not infer a definition from equality syntax alone.
- Do not suppress a valid theorem counterexample to improve the audit.
- Do not allow caller-authored role labels to alter routing or become certifying
  evidence; exact source-span validation is required for role authority.
- Do not silently choose the first duplicate label.
- Do not create a third independent document extractor.
- Do not treat CAS simplification, a domain template, generated Lean, retrieval,
  or a route plan as proof of economic or mathematical validity.
- Do not mutate the target document, enable publication, apply proposed edits,
  install packages, use networked mathematical search, or change release
  authority in this program.
- Do not treat fewer full-suite failures as mission completion.
- Do not omit or overwrite negative evidence from the repeated audit.

## Stop Conditions

- Stop before implementation if review finds an unresolved source-role,
  comparator, evidence-contract, or claim-boundary flaw.
- Stop a phase if exact source identity changes unexpectedly.
- Stop mathematical interpretation if a definition/identity is again reported
  as a theorem refutation or an unsupported valuation construct is promoted.
- Stop automatic backend execution on missing typed role, source identity,
  domain, or denominator preconditions.
- Stop publication and source editing unconditionally; neither is authorized.
- If a phase encounters a broader architectural issue, preserve the smallest
  reproducible failing test and record it as a remaining gap rather than
  expanding scope without review.

## Completion Conditions

The program is complete when the plan has passed skeptical and independent
review, all six phases have a recorded outcome, the same applicability-complete
audit and full suite have been rerun, the source digest is unchanged, and the
final result states an evidence-supported mission decision plus every remaining
gap. Completion does not require declaring the mission accomplished.
