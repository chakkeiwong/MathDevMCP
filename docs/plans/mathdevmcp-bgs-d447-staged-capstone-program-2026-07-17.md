# MathDevMCP BGS D447 Staged Capstone Program

Date: 2026-07-17

Status: `EXECUTED_PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS`

Supervisor and executor: Codex

Target repository under test: MathDevMCP

Read-only source repository: DynareMCP

## Mission

Test whether the current MathDevMCP can operate as an exploratory,
high-standard, rigorous, agent-facing mathematical development system on a
large, versioned macro-finance report without confusing operational success,
source prose, symbolic diagnostics, or abstention with scientific proof.

The program uses D447 as a regression and scale capstone. It does not use D447
as an independent generalization holdout because D447 was created by repairing
D446 with an earlier MathDevMCP audit.

## Frozen Sources

| Role | Path | SHA-256 | Status |
| --- | --- | --- | --- |
| Repaired capstone | `/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d447.tex` | `c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690` | contaminated regression/capstone |
| Pre-repair comparator | `/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d446.tex` | `2bbf997d5de2bf2d8eba65f899b5b74cedfe12d5129be432f4ec9c5ee8090553` | contaminated regression baseline |

D447 contains 19,144 lines, 117,188 words, 593 unique physical labels, and 580
top-level `equation`/`align` starts. The pre-repair index exposed 566 of those
labels. The initial capstone run found 20 figure labels outside the
mathematical-label surface and seven equation labels after nested `aligned`
structures. The repair loop now indexes those seven as exact lookup-only
labels with `nested_display_ownership_required`; it does not pretend their row
ownership is extractable. The repaired accounting target is 573/573 exact
mathematical-label resolution, with 566 extractable and seven lookup-only, plus
20 figure labels. D446 and D447
reside in the same directory and intentionally exercise the real
version-collision problem.

## Research Intent Ledger

| Field | Predeclared intent |
| --- | --- |
| Main engineering question | Can MathDevMCP retain exact file/digest/label identity, useful localization, bounded evidence, and actionable abstention as the input grows from the nine-label v8 lane to a 593-label report beside an almost-identical predecessor? |
| Main scientific-usefulness question | On the C.71--C.77 bank block, can the system separate algebraic checks, linearization obligations, source-dependent sign/timing choices, alternative asset-base branches, and unproved implementation/scientific claims? |
| Candidate under test | Current MathDevMCP at the execution commit/worktree, not the correctness of BGS or D447. |
| Exact baseline | D446/D447 known-repair pair plus the current nine-label credit-card-v8 evidence lane; seeded benchmarks are explanatory only. |
| Expected failure modes | Version ambiguity, repeated full-directory parsing, lost source digest, incomplete align-row extraction, generic `inconclusive`, source prose mistaken for proof, branch alternatives collapsed, output transport blow-up, or unsupported whole-document claims. |
| Primary promotion criterion | Exact-file ingestion accounts for all 593 physical labels, resolves all 573 mathematical labels, and distinguishes 566 extractable from seven lookup-only labels; paired repair neighborhoods remain correctly scope-classified; all 18 bank-block labels are localized and receive source-bound evidence or actionable typed abstention; the extractable-label capstone completes within its declared resource boundary without source drift or claim promotion. |
| Promotion veto | Wrong source/version, missing selected label, stale digest accepted, diagnostic promoted to proof, D447 prose treated as proof of an unchanged equation, C.75/C.77 branches collapsed into a single certified answer, or raw evidence that cannot be resolved. |
| Continuation veto | Source digest changes, target repository is mutated, corrupt/missing required artifacts, repeatable unhandled tool crash, or the run exceeds the declared full-capstone wall-time/memory boundary without a valid partial result. |
| Repair trigger | A localized engineering defect with a safe repository-local fix and focused regression test. Scientific uncertainty or backend absence triggers a gap record, not an invented repair. |
| Explanatory diagnostics | Counts, elapsed time, output size, status distributions, parser diagnostics, and benchmark/test totals. |
| Must not be concluded | BGS correctness, exact replication, source-author error, implementation equivalence, theorem proof, publication readiness, broad generalization, or superiority over another system. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does each public result bind the exact requested version and remain replayable at report scale? |
| Scientific question | Does the selected financial block yield the right categories of obligations and nonclaims, even when certifying backends cannot settle the macroeconomic claim? |
| Comparator | D446 before the four documented D447 reader-facing repairs; D447 after those repairs. Equation/backend status is compared separately because the underlying displayed equations are mostly unchanged. |
| Primary pass criterion | The machine-readable phase gates in the execution summary pass without an integrity or claim-boundary veto. |
| Veto diagnostics | Digest drift; exact-file lookup failure; unresolved selected label; cross-version result; unsafe edit; false proof/certification language; missing result artifact; unbounded crash; branch erasure. |
| Explanatory only | Runtime, memory, output bytes, label counts, aggregate status counts, and successful invocation counts. |
| Artifact | `docs/reviews/bgs-d447-capstone-audit/` plus replay evidence under `.local/mathdevmcp/evidence/bgs-d447-capstone-20260717/`. |
| Non-claim | A pass establishes only the tested workflow behavior on contaminated regression sources. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Same-directory D446/D447 corpus | Real DynareMCP layout | Exercises version collision rather than a sanitized copy | Global label map becomes ambiguous | Compare unscoped and exact-file resolution | reviewed baseline |
| Four known repair neighborhoods | D447 developer feedback and close record | Gives an exact regression target | Overfitting or mistaking prose for proof | Keep claim-boundary and derivation ledgers separate | contaminated regression baseline |
| Eighteen C.71--C.77 labels | D447 financial-block structure | Covers FOCs, shadow recursions, SDF timing/sign, net-worth laws, and entrant asset-base branches | Slice omits upstream primitives or downstream code | Require source/external-route blockers and nonclaims | reviewed difficult slice |
| SymPy | Current deterministic adapter | Appropriate for bounded scalar algebra only | CAS syntax failure or economic overpromotion | Record exact backend result and boundary | diagnostic route |
| Lean/Sage/specialist routes | Repository external-tool-first policy | Must be considered for certification/formalization | Backend absence mistaken for refutation | Record doctor/route plan and availability | considered route, not assumed available |
| Full physical label inventory | Frozen D447 bytes | Defines complete accounting while respecting ownership boundaries | Lookup-only labels could be misreported as extractable | Account for 20 non-indexed figures, seven lookup-only equations, and 566 extractable labels separately | primary accounting gate |
| Deep all-label wall budget of 20 minutes per workflow | Academic proportionality and one-megabyte input | Long enough to expose scale behavior without indefinite execution | Timeout hides partial evidence | Preserve stdout/stderr/status and classify timeout as scale gap | engineering boundary |
| CPU-only execution | No GPU-relevant kernel is under test | Reproducible and proportionate | Environment differs from unrelated GPU workflows | Set `CUDA_VISIBLE_DEVICES=-1` in manifest | convenience choice |
| No independent holdout in this run | Provenance inspection | Obvious candidate documents already mention or used MathDevMCP | False broad-generalization claim | Status must be `not_tested_no_verified_clean_holdout` | reviewed nonclaim |

## Skeptical Pre-Execution Audit

| Risk | Finding and repair |
| --- | --- |
| Wrong baseline | Repaired: D447 is explicitly a contaminated capstone; D446 is a contaminated pre-repair comparator. Neither is called a holdout. |
| Proxy promotion | Repaired: parse success, test totals, status counts, and runtime are explanatory. Exact identity and claim-boundary checks are the gates. |
| Unfair paired comparison | Repaired: D447 added reader-facing boundary prose around mostly unchanged equations. The program does not require backend proof status to improve between D446 and D447. |
| Hidden version sanitization | Repaired: index the real directory containing both files; exact-file selection must recover D447 despite unscoped ambiguity. |
| Missing stop conditions | Repaired: digest drift, cross-version selection, scientific overclaim, artifact corruption, and bounded time/resource failures are explicit. |
| Environment mismatch | Repaired: CPU-only mode and backend doctor evidence are recorded; absent optional backends cannot be reported as mathematical refutation. |
| Commands not answering the question | Repaired: all-label lightweight coverage answers scale/identity; selected deep workflows answer mathematical usefulness; seeded tests cannot substitute for either. |
| In-house algorithm drift | Repaired: the run exercises current orchestration and deterministic external routes. It does not authorize a new proof/search algorithm. |
| Independent generalization leakage | Repaired: no available candidate is silently declared clean. The result must preserve an untested-generalization gap. |
| Full-run resource explosion | Repaired: use one reusable index for inventory/search, bounded subprocesses for deep all-label workflows, and preserve explicit timeout/failure evidence. |

Audit decision: `PASS_AFTER_VISIBLE_REPAIRS`. The program is executable under
the stated boundaries.

## Phase 0: Readiness And Source Integrity

Objective: freeze the target identity and record the executable environment.

Required artifacts:

- source manifest with both SHA-256 digests;
- MathDevMCP git commit and dirty-state summary;
- Python/platform/CPU-only manifest;
- backend doctor and external-tool route records;
- DynareMCP pre/post status digest showing no source mutation.

Checks:

- both files exist and match the frozen digests;
- D447 physical label inventory is nonempty and duplicate-free within the file;
- target report bytes remain unchanged throughout execution.

Handoff: Phase 1 may start only with exact frozen bytes.

## Phase 1: Full-Document Ingestion And Version Resolution

Objective: test the full report as a scale, indexing, search, and localization
object before asking scientific questions.

Required execution:

1. Build one cached index over the real `finalBGS` directory.
2. Record blocks, equation rows, duplicate labels, elapsed time, and peak
   process memory where available.
3. Account for all 593 physical labels, resolve all 573 mathematical D447
   labels with the exact D447 file selector, classify 566 as extractable and
   seven nested-suffix labels as lookup-only, and classify 20 figure labels as
   outside the mathematical-label surface.
4. Probe unscoped sibling ambiguity and exact D446/D447 filters.
5. Run exact lookup/search probes on introduction, SW/BGS conversion, OBC,
   likelihood bridge, C.75, and C.77 neighborhoods.

Pass conditions:

- all 593 physical labels are accounted for and all 573 mathematical D447 labels
  resolve to D447;
- the 20 figure labels are classified as outside the mathematical-label surface
  and the seven nested-alignment equation labels remain explicit ownership gaps;
- no D446 block appears in an exact D447 result;
- unresolved/ambiguous unscoped behavior is reported rather than used as
  scientific evidence;
- source digest is stable.

Forbidden claim: ingestion success says nothing about mathematical correctness.

## Phase 2: Paired D446/D447 Regression

Objective: test whether current MathDevMCP rediscovers the earlier scope
problems and recognizes the D447 reader-facing repairs without treating those
repairs as proof.

Repair neighborhoods:

1. opening MathDevMCP audit boundary;
2. `eq:sw-bgs-risk-premium-conversion`;
3. `eq:bgs-obc-policy-shortfall` with its shadow-rate neighborhood;
4. `eq:crosscheck-kernel-decomposition`.

Required checks:

- exact D446 and D447 context extraction;
- expected repair-language delta detection;
- `audit_report_claim_boundary` on each D447 repair statement;
- paired `audit_derivation_label` evidence for the three labeled equations;
- math-to-code scope check for the fixed-point likelihood example;
- structural sign/term check for the deposit-return bridge;
- OBC external-tool/domain-obligation route consideration.

Pass conditions:

- D447 contains all four documented boundary repairs and D446 does not;
- boundary prose is classified as document-evidence/nonclaim material rather
  than theorem certification;
- equation/backend ledgers do not claim that new prose proves unchanged math;
- fixed-point and function-level claims remain distinct.

## Phase 3: C.71--C.77 Scientific Slice

Objective: perform a difficult but diagnosable mathematical-development audit
on the financial block.

Frozen labels:

```text
eq:bgs-linear-incentive-foc
eq:bgs-linear-shadow-values
eq:bgs-linear-bank-sdf
eq:bgs-sdf-product-rule
eq:bgs-sdf-printed-branch
eq:bgs-sdf-discounting-check-branch
eq:bgs-linear-surviving-bank
eq:bgs-linear-new-bank
eq:bgs-c71-level-repeat
eq:bgs-c71-networth-expansion
eq:bgs-c71-liquidity-expansion
eq:bgs-c72-expanded
eq:bgs-c74-expanded
eq:bgs-c75-product-rule-expanded
eq:bgs-c76-excess-return-form
eq:bgs-c77-bank-held-expanded
eq:bgs-c77-total-asset-expanded
eq:bgs-c77-branch-difference-expanded
```

Required workflows:

- exact lookup and source digest binding for all labels;
- math-document rigor audit;
- document derivation tree with resolvable detailed evidence;
- audit-and-propose-fix in diagnostic, no-source-edit mode;
- representative proof and negative-evidence packets;
- assumption/derivation proposals;
- external-tool-first plans for algebra/linearization, source comparison, and
  temporal/branch formalization;
- targeted claim-boundary audit of C.75 and C.77 language.

Scientific usefulness criteria:

- distinguish the C.75 printed positive branch from the discounting-check
  negative branch;
- preserve both C.77 bank-held and total-asset alternatives;
- distinguish level identities, first-order expansions, expectations/timing,
  balance-sheet accounting, and source-dependent assertions;
- name exact blockers, tools, evidence needs, next actions, and nonclaims when
  certification is unavailable;
- never infer official-code correctness or author error from local algebra.

A branch may remain unresolved and still pass the workflow gate. Collapsing an
unresolved branch into a certified answer is a veto.

## Phase 4: Full D447 Capstone

Objective: extend from the 18-label slice to the complete document without
weakening the evidence boundary.

Required tiers:

1. complete 593-label physical inventory, exact-file localization for all 573
   mathematical labels, and explicit separation of 566 extractable, seven
   lookup-only, and 20 figure labels;
2. whole-document rigor-audit plan;
3. whole-document diagnostic audit/fix coverage with source edits disabled;
4. all-label rigor and derivation-tree workflows within the declared bounds;
5. compact/detailed artifact resolution and output-size accounting.

The tier is `complete_with_predeclared_ownership_gaps` only if all 593 physical
labels are explicitly accounted for, all 573 mathematical labels resolve, and
all 566 extractable labels are audited. A
bounded timeout or unsupported target must be recorded by label or workflow;
it cannot be dropped and counted as a pass. The seven nested-alignment labels
remain lookup-only ownership gaps even if every extractable-label gate passes.

## Phase 5: Independent Generalization Control

Objective: prevent the capstone result from becoming a false generalization
claim.

Current preflight result:

`not_tested_no_verified_clean_holdout`

The inspected earlier BGS forensic report explicitly names MathDevMCP and was
created in a MathDevMCP-assisted workflow. It is therefore not an independent
control. A future control must have provenance demonstrating no MathDevMCP
repair or selection influence before results are unblinded.

This phase does not block a D447 regression/capstone result. It vetoes only a
broad-generalization claim.

## Phase 6: Review, Repair Loop, And Close

Required close artifacts:

- execution summary;
- ingestion/version-resolution report;
- paired-regression report;
- C.71--C.77 scientific-slice report;
- full-capstone report;
- remaining-gap and post-run red-team report;
- raw manifest with commands, commit, environment, source digests, elapsed
  time, artifact paths, and CPU-only status.

Repair loop:

1. Inspect every failed hard gate and unexpected status.
2. Classify it as harness invalidity, implementation defect, backend/scale
   limitation, source/scientific uncertainty, or expected abstention.
3. Repair only localized MathDevMCP/harness defects supported by a focused
   test; do not repair DynareMCP or rewrite the target report.
4. Rerun the smallest affected phase, then the exact comparator.
5. Stop only on a continuation veto or after preserving an explicit blocker.

## Final Decision Classes

- `CAPSTONE_WORKFLOW_ACCOMPLISHED_WITH_LIMITS`: all hard identity, boundary,
  slice, and bounded capstone gates pass; unresolved scientific claims remain
  explicit.
- `PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS`: source integrity and claim boundaries
  hold, but one or more complete all-label deep workflows do not finish or
  account for every target.
- `CAPSTONE_CANDIDATE_FAILED`: the evaluation is valid, but MathDevMCP selects
  the wrong version, erases a live branch, promotes diagnostic evidence, or
  fails another primary behavior gate.
- `EVALUATION_INVALID`: source drift, corrupt/missing required evidence,
  broken harness assumptions, or another continuation veto prevents a valid
  verdict about the candidate.

No decision class authorizes publication, source modification, or a claim of
independent generalization.

## Execution Close

The program was executed against the frozen D446/D447 bytes. Final decision:

`PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS`

The outcome is not a failed evaluation and not a completed whole-document
capstone. Phase 1 exact identity/accounting, Phase 2 paired regression, and the
18-label Phase 3 scientific slice passed. The three monolithic 566-label deep
workflows each exceeded the predeclared 20-minute bound:

| Workflow | Outcome | Interpretation |
| --- | --- | --- |
| `audit_and_propose_fix` | timeout after 1200.1 seconds | valid scale failure; no detailed artifact |
| `audit_math_document_rigor` | timeout after 1200.1 seconds | valid scale failure; no detailed artifact |
| `audit_document_derivation_tree` | timeout after 1200.0 seconds | valid scale failure; publication state not observed |

The repair loop fixed concrete defects exposed before and during execution:

- exact lookup-only retention for seven labels after nested `aligned` blocks;
- all three C.75 branch-label retention;
- valid extraction of the C.72 number-suppressed equality chain;
- digest-keyed reuse of source obligation parsing;
- cache-schema invalidation;
- bounded compact audit/rigor previews with exact detailed-artifact resolution;
- exact validation before reuse of audit/fix evidence;
- bounded subprocess isolation and restart-safe finalization;
- normalized full-source detection of documented D447 repair phrases.

The remaining gaps are recorded in
`docs/reviews/bgs-d447-capstone-audit/bgs-d447-staged-capstone-result.md`.

Final repository verification:

- focused repaired-contract suite: 60 passed;
- post-close focused suite: 44 passed;
- complete CPU-only repository suite: 1,649 passed and 4 skipped in
  4,124.33 seconds;
- Python compilation and `git diff --check`: passed;
- frozen D446/D447 SHA-256 digests: unchanged.
