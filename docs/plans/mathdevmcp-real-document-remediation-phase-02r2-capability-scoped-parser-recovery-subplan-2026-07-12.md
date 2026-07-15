# Phase 02R2 Capability-Scoped Parser Recovery Subplan

Date: 2026-07-12

Status: `DRAFT_FOR_INDEPENDENT_REVIEW`

Supervisor/executor: Codex

Reviewer: Claude Code read-only when the approved review transport is
available; otherwise a fresh independent Codex read-only reviewer

## Phase Objective

Recover Phase 02 from the pre-round parser-contract contradiction without
altering or overwriting any R9-reviewed artifact or the sealed
`.local/mathdevmcp/evidence/p02-20260711/entry` snapshot.

The objective remains label-scoped, byte-accurate obligation extraction from
real mathematical documents before semantic or mathematical backend routing.
The explorative system may consider multiple parsers, but claim boundaries are
rigorous: a tool is authoritative only for fields it can independently observe
and map to source. Tool availability, exit zero, label count, or parse volume
never substitutes for source-fidelity evidence.

Phase 02R2 passes only if the current byte-preserving scanner independently
reconstructs all 17 reviewed obligations exactly, every capability-scoped
specialist observation is correctly classified, no independently observable
specialist contradiction exists, no mathematical backend is requested, no
source or protected input changes, publication remains disabled, and the full
append-only governance chain is independently reviewed and sealed.

## Relationship To Frozen Phase 02

The following artifacts are immutable predecessors, not editable inputs:

- base subplan:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md`, SHA-256
  `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`;
- base compact oracle:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`, SHA-256
  `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`;
- materialized obligation oracle:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json`, SHA-256
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`;
- sealed R9 entry record:
  `.local/mathdevmcp/evidence/p02-20260711/entry/entry-record.json`, SHA-256
  `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`;
- runtime-contract review:
  `docs/reviews/mathdevmcp-real-document-remediation-phase-02-runtime-parser-contract-review-r10-result-2026-07-11.md`, SHA-256
  `e455fd0532ff7416339357c2dbc3d532d9f0d42aeaa9d730f79d696bbe75eef1`;
- pre-round blocker result:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02-pre-round-parser-contract-blocker-result-2026-07-11.md`, SHA-256
  `b5ccb1ed03a7cdc0d1c2515b24f487ac438891c84c15e6af1b75f62370981148`.

This subplan and
`docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json`
form an additive overlay. Every base Phase 02 requirement remains in force
unless the recovery oracle lists an exact replacement path and value. The 17
materialized obligations, extraction grammar, normalization, identity, action
ordering, receipt model, failure suffix, publication quarantine, source set,
and no-backend boundary are unchanged. The only implementation-allowlist
change is the reviewed addition of the future pure module
`src/mathdevmcp/parser_capability_extractors.py`, increasing the sorted compile
inventory from 22 to 23 paths. That file must remain absent until the one-shot
entry snapshot has sealed the current implementation bytes.

Inherited downstream binding names have one exact R2 meaning. In every
`init_round` receipt, machine result, run manifest, candidate, final decision,
round close, and independent reconstruction:

- `reviewed_plan_ref/sha256` binds this recovery subplan;
- `reviewed_compact_oracle_ref/sha256` binds the recovery oracle;
- `reviewed_materialized_oracle_ref/sha256` binds the frozen materialized
  oracle.

Reopening the recovery oracle then transitively and mandatorily reopens and
verifies the frozen base plan, base compact oracle, old entry, runtime review,
and blocker record. No inherited `reviewed_*` field may bind the base plan or
base compact oracle, omit the recovery pair, or copy a transitive digest
without reopening it.

The new evidence family is
`.local/mathdevmcp/evidence/p02r2-20260712`. The old Phase 02 family is protected
read-only evidence and is never treated as a pass or as a successful result
round.

## Entry Conditions

All conditions must hold before the one-shot Phase 02R2 entry snapshot:

1. P00 remains sealed `pass` with publication disabled.
2. P01 stable decision and terminal receipt index reopen with exact digests
   `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`
   and `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.
3. Every frozen predecessor listed above reopens no-follow with its exact
   digest; the old Phase 02 entry contains exactly its four sealed files.
4. No old Phase 02 result round or stable Phase 02 decision exists.
5. The new `.local/mathdevmcp/evidence/p02r2-20260712` root is absent.
6. The recovery plan, oracle, bootstrap, and review bundle pass local schema,
   digest, compilation, Markdown, and `git diff --check` checks.
7. A material read-only review returns `AGREE` and binds the exact recovery
   plan, recovery oracle, recovery bootstrap, base plan/oracles/materialized
   oracle, and old entry. Review rounds R11 through R14 are the remaining
   authorized budget. Every earlier substantive recovery review must be present,
   bind the exact seven digests of the bytes it reviewed, and end `REVISE`; no
   stale binding, skipped round, prior `AGREE`, or R15 is accepted.
8. The one-shot bootstrap snapshots the current `src`, `tests`, and `scripts`
   bytes before any further implementation edit. A pre-existing or partially
   created new phase root is a human-recovery stop, not permission to retry.

## Skeptical Plan Audit

### Wrong baseline

The baseline is not “specialist parser unavailable.” The measured baseline is:

- current scanner: exact source-byte reconstruction of 17/17 materialized
  obligations in focused diagnostics;
- LaTeXML 0.8.6: available, but representative exact-profile output contains
  malformed-label/undefined-environment errors and lacks row ownership byte
  mapping;
- Pandoc 2.9.2.1: available and preserves useful raw display text, but its
  reviewed JSON invocation exposes no independent byte-offset channel.

### Proxy promotion

Exit zero, version availability, requested-label string presence, output size,
runtime, and test count are explanatory. They cannot promote a specialist or
veto an independently exact current reconstruction unless the tool produces a
contradictory observation for a field it can independently and validly observe.

### Hidden assumptions

- “Independent” forbids deriving specialist source spans by calling the current
  scanner or copying compact/materialized oracle spans.
- A raw-only specialist observes a document-wide structural label set, not the
  reviewed requested-label projection. The two frozen real documents contain
  298 and 116 explicit source labels respectively, while this phase requests
  only two from each. Equality between the raw document set and requested set
  would therefore be a deterministic false veto.
- A malformed specialist result supplies no positive or negative ownership
  evidence, even if some requested labels occur in its bytes.
- Capability absence is not agreement and is not refutation. It must be
  recorded as a limitation.
- The current scanner is not trusted because it is current; it passes only by
  exact three-way compact/materialized/source reconstruction and mutation tests.
- Frozen identities cannot be rewritten from specialist output in this phase.

### Environment mismatch

Formal specialist calls retain the exact `/usr/bin/latexml` and
`/usr/bin/pandoc` paths, measured versions, argv, clean environment, source
allowlist, timeouts, and scratch-only outputs from the base oracle. A mismatch
remains a veto. No install, network access, alternate executable, document
wrapper, filter, shell escape, or retry is authorized.

### Artifact fitness

The parser comparison must preserve raw stdout/stderr/output/logs, exact
argv/environment, timeout/exit, source pre/post digests, structured validity,
declared observable fields, per-field observation provenance, capability
status, contradiction state, promotion eligibility, and non-claims. Summary
booleans are reconstructed from raw records and cannot authorize a pass.

### Audit decision

`PASS_FOR_RECOVERY_PLAN_REVIEW_ONLY`. Implementation and a new formal round
remain closed until this plan and the recovery oracle agree under independent
review and the new entry snapshot succeeds.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Earliest diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Exact-byte current scanner is primary for the frozen corpus | 17 source-derived R9 identities and R10 specialist limitations | It uniquely exposes the required byte ownership fields | Self-confirming implementation agrees with its own output | Three-way compact/materialized/source equality plus 93/5 mutations and adversarial fixtures | Reviewed hypothesis, must pass again |
| LaTeXML/Pandoc are capability-scoped diagnostics | Direct R10 disposable probes | Their exact profiles do not expose all seven fields | Capability failure is hidden as agreement, malformed bytes create a false veto, or a document-global label set is compared directly with the requested subset | Raw-output validity, requested-set projection, and observable-field registry checks | Recovery default |
| Malformed/non-source-mappable output blocks specialist promotion only | R10 contradiction and external-tool-first policy | Absence of evidence is not evidence against exact source reconstruction | A genuine contradiction is ignored | Per-field independent-observation and contradiction gate | Recovery default |
| Independently observable contradiction remains a phase veto | Rigorous claim boundary | Multiple tools disagree on a field both can validly observe | Current implementation wins by fiat | Mutated specialist record and disagreement fixtures | Mandatory boundary |
| Specialist source mapping may not reuse current spans | Independence requirement | Prevents circular validation | Oracle/current spans are relabeled as specialist evidence | Provenance graph and sentinel rejecting current/oracle-derived mapping | Mandatory boundary |
| New evidence namespace | Sealed R9 entry and R10 blocker | Preserves audit history and snapshots current repaired code | Old entry is silently reinterpreted or overwritten | Exact old/new tree closure and no-overwrite tests | Mandatory boundary |

## Evidence Contract

### Engineering question

Can MathDevMCP extract the 17 reviewed label-scoped obligations exactly from
source bytes, preserve ambiguity and ownership boundaries, integrate them
without backend routing, and classify specialist parser evidence without
treating unsupported capability as either agreement or refutation?

### Baseline and comparators

- primary baseline: the R10-measured pre-recovery implementation under the new
  entry manifest;
- identity comparator: exact base compact/materialized oracle and source bytes;
- specialist diagnostics: exact-profile LaTeXML 0.8.6 and Pandoc 2.9.2.1;
- no weak parser, label-count, or exit-only comparator is promotional.

### Primary criterion

All inherited twelve base Phase 02 criteria remain required. The inherited
`parser_fidelity_contract_pass` criterion is replaced by the conjunction:

1. all 13 current-parser source cases reconstruct the expected requested
   obligations and seven-field source-fidelity vector exactly;
2. exactly two version calls and 26 source calls occur under the fixed profile;
3. every raw artifact, argv, environment, source pre/post digest, version,
   timeout, and exit classification reopens and verifies;
4. every specialist result has one closed capability state and exact observable
   field set;
5. malformed or non-source-mappable results are ineligible for promotion and
   record explicit limitations;
6. no specialist record claims a field without independent raw-output
   provenance;
7. no independently observable specialist/current contradiction exists;
8. frozen identities remain current / `p02_lightweight_locator@1` and unchanged.

### Veto diagnostics

The inherited `parser_fidelity_or_provenance_failure` veto is true for any:

- current-parser compact/materialized/source mismatch;
- missing, duplicated, unreviewed, or mismatched specialist invocation;
- executable/version/argv/environment/source/output/log binding failure;
- source mutation, timeout, or unclassified nonzero exit;
- malformed output classified as valid evidence;
- capability limitation omitted or promoted;
- claimed observable field without independent provenance;
- independently valid specialist observation contradicting the current result;
- frozen identity rewrite or unjustified specialist selection.

Malformed or non-source-mappable specialist output, correctly classified and
kept ineligible, is explanatory and does not alone set the veto.

### Explanatory diagnostics

Availability, parse exit, error counts, label-string recovery, output bytes,
runtime, and capability coverage are reported but non-promotional.

### What will not be concluded

No mathematical truth, proof, semantic correctness, complete LaTeX coverage,
general parser ranking, backend conformance, source-document repair,
publication eligibility, Phase 03 correctness, or release readiness is claimed.

### Preserved artifact

The result is preserved below
`.local/mathdevmcp/evidence/p02r2-20260712`, including entry bindings, raw parser
artifacts, extraction bundle, mutation matrix, guard ledgers, manifests,
append-only receipts, result, reviews, final candidate, and stable hard link or
a canonical blocker close.

## Revised Parser Capability Contract

Each specialist source record has exactly one `capability_status`:

- `valid_source_mappable`;
- `valid_not_source_mappable`;
- `malformed_output`;
- `timed_out`;
- `nonzero_exit`;
- `version_mismatch`;
- `invocation_mismatch`;
- `source_mutated`;
- `missing_artifact`.

Only `valid_source_mappable` may be considered for specialist selection. It
must include a nonempty set of independently observable fidelity fields and
raw-output provenance for every claimed field. A status other than
`valid_source_mappable` has an empty promotional fidelity vector, is explicitly
ineligible, and records one or more limitation codes.

For `valid_source_mappable`, comparison is lexicographic over only the leading
field prefix for which both current and specialist have independent evidence.
No unobserved field is filled from source, current output, or an oracle. Any
contradiction on an independently observed field vetoes the frozen case. Equal
or weaker valid observations do not rewrite a frozen identity. Materially
better evidence requires a new reviewed oracle; it cannot be adopted in-place.

LaTeXML error nodes, `Error:` log diagnostics, undefined environments/macros
that affect the target display, absent output, or structurally collapsed label
ownership are `malformed_output`, even with process exit zero. Pandoc raw math
without independent byte positions is normally `valid_not_source_mappable`.
These expected classifications are hypotheses to measure, not hard-coded pass
answers.

Specialist observations are restricted to the recovery oracle's closed
extractor registry. Both registered extractors must live in the dedicated
future module `src/mathdevmcp/parser_capability_extractors.py`, which has no
project imports, constants, data loaders, or import-time calls. Its exact three
standard-library imports, two top-level functions, function signatures,
referenced import globals, referenced builtins, imported calls, value-method
calls, and empty callable-dependency lists are frozen. Static validation rejects
extra top-level statements, decorators, defaults, annotations, nested
functions/classes, lambdas, comprehensions, `global`, `nonlocal`, dynamic
import/evaluation, filesystem/process/network APIs, unregistered helpers, or
any loaded name/call outside those exact registries. Runtime validation requires
plain function objects with `__closure__ is None`, `__defaults__ is None`,
`__kwdefaults__ is None`, and empty `co_freevars` and `co_cellvars`.

Governance reopens the round-manifest-bound module bytes, performs that static
and runtime closure audit, and then passes only the reopened raw artifact bytes
in registry role order. The extractors receive no invocation metadata, source
bytes, source path contents, current-scanner record, compact oracle,
materialized oracle, expected spans, or expected labels. Their raw-only return
object has exactly `raw_observable_field` and `observed_value`, where the raw
field is `document_structural_label_set`; no expected value, requested-set
projection, or comparison result is available during extraction.

Every `raw_inputs` array is ordered exactly like the registry and each entry
has exactly `role`, `value_type`, `artifact_ref`, `artifact_sha256`,
`artifact_byte_count`, `invocation_receipt_ref`, and
`invocation_receipt_sha256`. Governance reopens each regular no-follow raw
artifact and canonical invocation receipt, checks digest and byte count, and
requires the receipt field registered for that role to bind the same artifact
triple. Raw observation provenance contains only the extractor/module binding,
that exact input array, the exact raw-only output, and an empty forbidden
lineage. Expected labels enter later through a separately bound canonical
per-source projection and a separate comparison-provenance object; the
projection and comparison are never extractor inputs. Comparison derives the
sorted requested-label intersection, missing requested labels, and unscoped
extra structural labels. `exact_requested_label_set` is true exactly when the
requested-label intersection equals the frozen requested set, equivalently
when the missing set is empty. Extra document labels are expected on the two
real documents, remain explanatory, and can neither contradict nor promote.
The diagnostic,
observation-provenance, and comparison-provenance key sets must agree exactly.
Unregistered extractors, globals, calls, inputs, fields, expected-position
seeds, receipt mismatches, or lineage through current/oracle/source data set the
parser veto.

## Required Artifacts

- this recovery subplan and machine recovery oracle;
- bounded review bundles/results R11 through at most R14;
- one-shot `p02r2_entry_bootstrap_20260712.py` and new entry record/manifests;
- the exact 23-path effective implementation allowlist: the inherited 22 paths
  plus `src/mathdevmcp/parser_capability_extractors.py`;
- strict parser capability schemas and raw invocation records;
- all inherited extraction, bundle, governance, result, repair, review, final,
  and publication artifacts under the new evidence root;
- a Phase 02R2 result/close record and refreshed master handoff;
- a Phase 03 subplan only after a stable Phase 02R2 pass.

## Required Checks, Tests, And Reviews

All base Phase 02 commands remain required with `RR` rooted below
`.local/mathdevmcp/evidence/p02r2-20260712/result-rounds`. Add or strengthen:

- parser schema tests for all nine capability states;
- malformed LaTeXML exit-zero fixtures;
- valid-but-non-source-mappable Pandoc fixtures;
- missing/duplicate invocation and raw-artifact tampering;
- source mutation and version/argv/environment mismatch;
- sentinel proving a specialist crosswalk cannot call the current scanner or
  import compact/materialized spans as observations;
- static and runtime pure-module closure tests covering extra imports/globals,
  module data, import-time calls, decorators/defaults/closures, helper calls,
  dynamic evaluation, and filesystem/process/network access;
- production validation of every extractor id, implementation digest, exact
  raw input role/ref/digest/byte-count/receipt binding, raw-only output,
  separate comparison provenance, field set, and forbidden lineage;
- independently observable contradiction mutation that sets the parser veto;
- real-document regression proving 298-versus-2 and 116-versus-2 raw/requested
  label sets do not create false contradictions while a missing requested label
  does;
- limitation-only records that preserve current exact reconstruction without a
  veto or specialist promotion;
- exact old/new namespace isolation and old-entry tamper rejection;
- all inherited governance CLI, receipt, transition, reconstruction,
  failure-injection, stable-link, and no-backend tests.

Before formal `rr01`, run the real 28-call parser profile and the entire
governance success/failure chain in a disposable mirror. The disposable result
must show raw malformed/non-source-mappable limitations classified according
to this contract, no independently observable contradiction, no source edit,
and no mathematical backend request. A surprising valid source-mappable result
is not auto-promoted; it triggers focused audit against the selection rule.

Material result review and final-seal audit remain read-only and independent.
R11 and R12 ended `REVISE`; R13 is the current repaired-plan review and R14 is
the last already authorized recovery-plan round. An R13 agreement does not
consume or merge the later independent result-review and final-seal-audit
gates. Before either later gate, the supervisor must confirm sufficient
human-authorized review budget; otherwise execution stops after local/formal
artifacts are safely closed. No gate is skipped or merged to fit a budget.

## Evidence Reconstruction

No generated summary is authoritative. Independent reconstruction reopens:

- new entry and all frozen predecessor bindings;
- every receipt/index prefix and exact command/environment;
- all source/oracle bytes and implementation/protected/immutable manifests;
- all 28 parser invocations and their raw artifacts;
- capability states, observable-field provenance, limitations, and
  contradictions;
- all 17 obligation identities, bundle artifacts, mutation matrix, backend
  ledgers, result bytes, reviews, final candidate, and audit.

The reconstructed candidate uses the same closed primary/veto maps as the base
plan, with only the parser criterion/veto source semantics replaced above.
Publication remains a no-overwrite hard link and records mode `disabled`.

## Forbidden Claims And Actions

- Do not edit, overwrite, rename, delete, relink, or reinterpret the base R9
  plan/oracles/materialized oracle, old entry, P00, or P01 evidence.
- Do not create the new entry before an agreeing material review.
- Do not edit `src`, `tests`, or `scripts` between recovery-plan review and the
  one-shot entry snapshot.
- Do not create formal `rr01` before disposable parser and governance dry-runs
  pass the skeptical audit.
- Do not call a mathematical backend, network, installer, GPU, or source-edit
  path in Phase 02R2.
- Do not use current/oracle spans as specialist evidence.
- Do not compare a document-global structural label set directly for equality
  with the requested-label projection or treat unscoped extra labels as a
  contradiction.
- Do not treat malformed, absent, or non-source-mappable output as agreement.
- Do not let those limitations alone refute an exact current reconstruction.
- Do not promote a specialist from exit zero, labels, counts, runtime, or
  scalar scores.
- Do not claim publication eligibility, mathematics, Phase 03 execution, or
  release readiness.

## Exact Next-Phase Handoff Conditions

Phase 03 planning may resume only when:

1. the new entry, all formal receipts, candidate, agreeing result review, final
   candidate, agreeing final-seal audit, and stable decision independently
   reconstruct;
2. every inherited primary criterion including the revised parser criterion is
   true and every inherited veto is false;
3. backend requests and source edits are zero;
4. old/new evidence trees and protected inputs remain exact;
5. publication mode remains disabled;
6. the Phase 02R2 result states all non-claims and the master ledger/handoff is
   refreshed;
7. a Phase 03 subplan inherits the stable decision digest and does not infer
   semantic or mathematical correctness from extraction success.

## Stop Conditions

Stop and write a blocker without opening or continuing a formal round when:

- recovery review does not converge by R14;
- the new entry root exists before its one-shot bootstrap or snapshot creation
  partially fails;
- any frozen predecessor, source, oracle, fixture, protected path, or P01 pair
  drifts;
- current source reconstruction differs from the 17 materialized identities;
- the real parser dry-run reveals an unclassified state, source mutation,
  missing raw evidence, or independently observable contradiction;
- a specialist is promoted without independent source mapping;
- implementation changes escape the inherited allowlist;
- receipt/index append, repair close, or post-link sealing loses trustworthy
  succession;
- publication becomes enabled, a backend is requested, or a source document is
  edited;
- a human, runtime, funding, model-file, product-capability, or scientific-claim
  boundary is reached.

At a fixable implementation failure after formal round creation, follow the
inherited `bind_scoped_repair -> close_round` suffix and use the next result
round. Never retry or overwrite an action in place.

## End-Of-Phase Procedure

After the final required check:

1. write the twelve-section human result and bind it through governance;
2. construct and independently validate the machine result and run manifest;
3. construct the candidate and obtain an independent result review;
4. construct and validate the final candidate and obtain a final-seal audit;
5. publish the disabled-mode stable hard link only after complete
   reconstruction;
6. write the Phase 02R2 close/handoff, refresh the visible execution ledger,
   and draft/review Phase 03 only if the stable decision is `pass`.
