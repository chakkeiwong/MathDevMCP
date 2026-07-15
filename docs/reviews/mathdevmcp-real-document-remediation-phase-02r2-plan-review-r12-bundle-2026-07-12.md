# Phase 02R2 Recovery Plan Review R12 Bundle

Date: 2026-07-12

Review name: `mathdevmcp-p02r2-recovery-plan-r12`

Role: fresh independent read-only material review. Do not edit files, create
evidence, run parser/backends, use network, install, or authorize publication,
source edits, Phase 03, product capability, funding, model-file, or scientific
claims.

## Objective

Determine whether the repaired Phase 02R2 plan/oracle/bootstrap closes the
three material R11 findings without weakening the recovery evidence contract.

Read completely:

1. `docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-plan-review-r11-result-2026-07-12.md`;
2. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md`;
3. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json`;
4. `docs/plans/p02r2_entry_bootstrap_20260712.py`.

Use the R11 bundle, frozen base plan/oracle/materialized oracle, old entry, and
current implementation only where necessary to verify regression, exact patch
baselines, or feasibility. Do not broaden into unrelated extraction grammar.

## R11 Findings And Claimed Repairs

### Downstream binding closure

R11 found that inherited `reviewed_plan_*` and
`reviewed_compact_oracle_*` fields had ambiguous meanings. The repaired plan
and `downstream_binding_contract` now require:

- inherited reviewed-plan fields bind the recovery plan;
- inherited reviewed-compact-oracle fields bind the recovery oracle;
- inherited reviewed-materialized fields bind the frozen materialized oracle;
- every reconstruction reopens recovery-oracle `base_bindings`, including base
  plan, base compact oracle, old entry, R10 review, and blocker;
- base and recovery meanings cannot alias;
- inherited exact key sets remain unchanged and no implementation-defined
  field is permitted.

### Review-history closure

R11 found that earlier `REVISE` reviews were checked only for existence and a
final verdict. The repaired oracle now contains an exact ordered
`review_history` entry for R11, including result ref/digest and all seven
reviewed digests. Bootstrap validation requires contiguous rounds from R11,
exact history schema/ref/digest, each historical result's exact seven binding
lines once, and final `REVISE`, while rejecting skipped, stale, unregistered,
later, R15+, or prior-AGREE results.

### Circular-evidence closure

R11 found no closed extractor/provenance registry. The repaired oracle now
registers exactly two raw-only extractors:

- `p02r2_latexml_structural_label_set_v1` receives only XML/log bytes;
- `p02r2_pandoc_math_label_set_v1` receives only Pandoc JSON bytes.

Both are diagnostic-only and not promotion-capable. Each has exact function,
module, input roles/types, output keys, observable field, parser grammar, and
forbidden inputs. The execution rule binds the round implementation digest,
rejects filesystem/process/network or unregistered helper calls, and validates
the exact raw-input role/ref/digest set. Expected values enter only in a
separate fixed comparison step. Formal provenance has exact fields, raw and
expected-value bindings, comparison id, and an empty forbidden-lineage list.

Malformed output yields no observation. Valid non-source-mappable output may
expose a raw-supported label-set contradiction but is never promotion-eligible.
No extractor receives source bytes/path contents, expected labels/spans,
current records, compact/materialized oracles, filesystem paths, subprocesses,
or network.

## Exact Bindings

- Recovery plan SHA-256:
  `8ec544a1068bb2840ab488ebdc287626bc58f8d5f964b58f8bbe0d858e53d04d`.
- Recovery oracle SHA-256:
  `c953a9373c78ae8530cd23a9740ac4d0a3b1525f86fd8f36c3096bab41745ccf`.
- Recovery bootstrap SHA-256:
  `559ba7703a556ac06aab33e56b35f8ce272c1ca07bafdd0c1fad3590ddbd2180`.
- Base plan SHA-256:
  `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`.
- Base compact oracle SHA-256:
  `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`.
- Materialized oracle SHA-256:
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
- Prior entry SHA-256:
  `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`.

## Local Pre-Review Evidence

- Bootstrap compiles and `git diff --check` passes.
- Strict preflight validates 13 source projections and all materialized
  environment/identity projections.
- Oracle has 33 unique entry keys, 11 exact profile patches, nine states,
  seven fields, two exact diagnostic extractors, and one exact R11 history
  record.
- Every patch expected base value matches the frozen compact oracle.
- R11 result reopens at SHA-256
  `c6a3c2690c4859230c9728b2340932806ae9f74e65a596809d2e2b06403d1226`,
  contains all seven registered binding lines, and ends `REVISE`.
- Old entry/manifests remain exact; new P02R2 root remains absent.

## Review Questions

1. Are inherited downstream bindings now unambiguous, complete, and
   reconstructible without changing inherited exact schemas?
2. Does the transitive binding rule keep the frozen base/old entry auditable,
   or can a result/candidate/final omit or substitute a recovery/base artifact?
3. Does bootstrap enforce every historical R11 binding, and will the same
   registry/algorithm safely handle R12-R13 revisions without stale or circular
   self-digests?
4. Is the extractor registry closed enough to prevent current/oracle/source
   data from entering specialist observations directly or through helpers?
5. Is the separation between raw-only extraction and expected-value comparison
   sufficient to avoid circularity while still detecting a genuine label-set
   contradiction?
6. Are malformed, capability-limited, contradictory, and promotion-eligible
   states mutually coherent under exact precedence and record rules?
7. Do the repairs preserve the exact-profile external-tool-first discipline,
   current-parser exactness, source/protected/no-backend gates, disabled
   publication, failure closure, and independent result/final reviews?
8. Identify any remaining material invention, hidden default, proxy promotion,
   stale namespace/ref, schema ambiguity, infeasible enforcement, or unsupported
   claim.

## Required Output

Findings first, severity ordered, with exact file/line references. If no
material issue remains, state that explicitly and list residual implementation
risks separately. Include exactly these seven recomputed lines:

```text
Reviewed recovery plan SHA-256: `<lowercase-64-hex>`
Reviewed recovery oracle SHA-256: `<lowercase-64-hex>`
Reviewed recovery bootstrap SHA-256: `<lowercase-64-hex>`
Reviewed base plan SHA-256: `<lowercase-64-hex>`
Reviewed base compact oracle SHA-256: `<lowercase-64-hex>`
Reviewed materialized oracle SHA-256: `<lowercase-64-hex>`
Reviewed prior entry SHA-256: `<lowercase-64-hex>`
```

End with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.
