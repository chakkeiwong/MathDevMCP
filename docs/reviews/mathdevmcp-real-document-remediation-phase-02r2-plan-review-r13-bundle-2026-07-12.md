# Phase 02R2 Recovery Plan Review R13 Bundle

Date: 2026-07-12

Review name: `mathdevmcp-p02r2-recovery-plan-r13`

Role: fresh independent Codex read-only material review. Do not edit files,
create evidence, run parser/backends, use network, install, or authorize
publication, source edits, Phase 03, product capability, funding, model-file,
or scientific claims.

Claude review status: the approved Claude gate was policy-rejected before
execution and before bundle transmission. Do not retry or work around that
gate. This R13 uses the approved fresh-Codex fallback.

## Objective

Determine whether the delta from R12 closes the one remaining material finding:
circular-evidence closure was incomplete because the proposed extractors lived
beside oracle/current-state loaders and the nested raw-input/provenance schemas
were not exact.

Read completely:

1. `docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-plan-review-r12-result-2026-07-12.md`;
2. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md`;
3. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json`;
4. `docs/plans/p02r2_entry_bootstrap_20260712.py`.

Use the R11/R12 bundles, frozen base plan/oracles/materialized oracle, old entry,
and current implementation only where necessary to verify regression, exact
patch baselines, or feasibility. Do not broaden into unrelated extraction
grammar or implementation quality that remains gated behind the entry snapshot.

## R12 Finding And Claimed Repair

### Dedicated future pure module

Both raw-only extractors move from `parser_benchmark.py` to the future post-entry
file `src/mathdevmcp/parser_capability_extractors.py`. The module must be absent
through entry creation. One exact JSON-pointer patch adds it to the inherited
sorted compile allowlist, changing only 22 paths to 23.

### Closed computation surface

The pure-module contract freezes:

- exactly three standard-library imports and two top-level functions;
- no project import, relative/import-from/star import, module assignment/data,
  import-time call, decorator, default, annotation, closure, nested callable,
  comprehension, `global`, `nonlocal`, or dynamic evaluation;
- lexical-local-only store targets, no attribute/subscript/imported/global
  mutation, and no delete target;
- exact function parameters, referenced globals/builtins, imported attributes
  and calls, value attributes/methods, and empty callable dependencies;
- no filesystem, process, network, serialization, dynamic import/evaluation,
  or dunder traversal capability;
- an exact runtime module namespace containing only interpreter metadata, the
  three standard-library modules, and the two functions, with no preloaded
  project/current/oracle/source state;
- runtime plain-function identity, no defaults/annotations/closures/freevars/
  cellvars, exact signatures, and exact function-global namespace.

Governance must audit the round-manifest-bound module bytes statically before
loading them, then audit the runtime closure before passing only reopened raw
bytes in registry order.

### Exact raw evidence chain

The repaired oracle freezes exact schemas for:

- raw artifact bindings;
- source invocation receipts, including fixed refs, exact invocation/artifact
  fields, version receipt binding, source pre/post digests, and the exclusion of
  any expected/current/oracle/observation data;
- ordered `raw_inputs`, with role/type/artifact ref/digest/byte count and exact
  invocation receipt ref/digest binding;
- raw-only extractor output;
- a separately written expected-label projection after raw outputs are sealed;
- raw observation provenance;
- separate expected-value comparison provenance.

Every object key registry is in project-canonical UTF-8 order. The `raw_inputs`
array remains in exact extractor-role order. Raw receipts cannot contain later
observations, and raw extractor output cannot contain expected values or
comparison results. Raw artifact bindings represent missing output/log paths
with an exact `present: false` plus null digest/count, while extractor inputs
can bind only present regular artifacts.

### Real-document scope correction

The supervisor's pre-review audit found that a raw-only specialist observes a
document-wide structural label set, not the frozen requested-label projection.
The two real documents contain respectively 298 and 116 distinct explicit
source label tokens, while Phase 02 requests only two labels from each.
Comparing raw and requested sets for equality would therefore manufacture false
contradictions from 296 and 114 legitimate unscoped labels.

The repaired contract now requires raw extractors to return only
`document_structural_label_set`. After raw output is sealed, the separate
comparison computes requested intersection, missing requested labels, and
unscoped extras. `exact_requested_label_set` passes when every requested label
is present; unscoped extras are explanatory and cannot veto or promote. A
missing requested label remains a diagnostic contradiction. Bootstrap
independently strict-decodes the frozen documents, derives requested labels
from the frozen base projection, and reproduces exact 298/2/296 and 116/2/114
counts before entry.

### Review history and bootstrap

The oracle registers the exact R12 result digest and its seven reviewed digests.
Bootstrap validation now requires 12 exact patches, the exact compile-pointer
patch, a sorted 22-to-23 allowlist delta containing only the pure module, the
pure module and nested schemas above, and the future module's absence before the
one-shot entry snapshot. R11/R12 still reopen at fixed digests and end `REVISE`.

## Exact Bindings

- Recovery plan SHA-256:
  `6ed09b8c1c177c6e76b9547ae350454907047c66c5f62b91c42800bd2c2d1a71`.
- Recovery oracle SHA-256:
  `92d75deb5fc30311a46c4d4f077939c594e667269a96ca56de8bf3be928d5562`.
- Recovery bootstrap SHA-256:
  `ecffbe248313888300f482204c3599167d96795cc59b11349080c95b9cb15ee2`.
- Base plan SHA-256:
  `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`.
- Base compact oracle SHA-256:
  `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`.
- Materialized oracle SHA-256:
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
- Prior entry SHA-256:
  `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`.
- R12 result SHA-256:
  `f8230e07204d46ef5ab6f1dd64fb809fd30178dbb78599cb021d1285dfd38a97`.

## Local Pre-Review Evidence

- Bootstrap compiles and the recovery oracle is strict JSON.
- Bootstrap's read-only preflight validates frozen bindings, old entry/manifests,
  12 unique overlay patches, two historical review records, all parser/pure/
  nested schemas, and the exact 23-path effective allowlist.
- Every patch expected base value equals the frozen compact oracle value.
- Every nested key registry equals project-canonical UTF-8 order.
- The real-document scope audit reconstructs exact distinct source/requested/
  unscoped-extra counts 298/2/296 and 116/2/114, with no duplicate source label
  tokens and every requested label contained in the corresponding source set.
- R11 and R12 reopen at fixed digests, contain their registered seven bindings,
  and end `REVISE`.
- `git diff --check` passes.
- The P02R2 root and future pure extractor module remain absent.

## Skeptical Review Questions

1. Does the pure-module contract actually prevent source/current/oracle data or
   import-time/global/closure state from entering either raw observation?
2. Are all name, attribute, call, helper, dynamic evaluation, filesystem,
   process, and network avenues closed in a statically and runtime enforceable
   way, or can accepted code still obtain unregistered state?
3. Are the exact function allowlists feasible for the stated LaTeXML XML/log and
   Pandoc JSON traversal, without requiring an unregistered helper or hidden
   default?
4. Do the raw artifact, source-invocation receipt, `raw_inputs`, raw output,
   expected projection, observation provenance, and comparison provenance
   schemas form an acyclic, reconstructible chain with exact types and bindings?
5. Can correct raw bytes from another backend/source/invocation be substituted,
   or can expected/current/oracle data enter before raw extraction is sealed?
6. Does the requested-coverage comparison correctly avoid false contradictions
   from 296/114 legitimate extra labels while still vetoing a missing requested
   label, without feeding requested labels back into raw extraction?
7. Is the 22-to-23 compile/implementation allowlist change exact, minimal,
   sorted, and enforceable while the future module remains absent at entry?
8. Does bootstrap bind R12 and reject stale review history, stale patch counts,
   stale extractor modules, or an already-created pure module/root?
9. Did the R13 delta regress the already-closed downstream-binding and
   review-history findings or weaken exact-profile, source/protected/no-backend,
   disabled-publication, failure-closure, or independent-review gates?
10. Identify any remaining material invention, hidden default, proxy promotion,
   circularity, schema ambiguity, infeasible enforcement, or unsupported claim.

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish a
material plan defect from a post-entry implementation risk already governed by
the exact contract. If no material issue remains, state that explicitly and
list residual implementation risks separately.

Include exactly these seven recomputed lines:

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
