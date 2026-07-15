# MathDevMCP Phase 03R1 Entry Bootstrap Recovery Subplan

Date: 2026-07-13

Status: `DRAFT_PENDING_INDEPENDENT_RECOVERY_REVIEW_R3`

Base Phase 03 plan:
`docs/plans/mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-subplan-2026-07-12.md`

## Phase Objective

Create the already-authorized Phase 03 immutable entry without mutating sealed
predecessors, retrying the failed bootstrap, weakening formal-evidence symlink
checks, or performing any new fallible discovery after allocation starts.

This recovery is entry engineering only. It does not alter the Phase 03
semantic/context implementation contract, allowlist, 14-search plus
3-extraction-veto partition, evidence criteria, governance action order,
mathematical/backend boundaries, or publication-disabled state.

## Entry Conditions

The recovery binds these immutable inputs:

```text
BASE_P03_PLAN_SHA256=b0172a6122205d9378c4393bee270116ca501616da0a939b960f2ac16213c4f4
FAILED_P03_BOOTSTRAP_SHA256=abb04fbff5cfbf97b0b41ce28d34c1cf93dbb45243558e0df3064c39f1e9ac8b
P03_R1_REVIEW_SHA256=4e4c2c235f53b035ec4a5780f02165a4662630782e3f5862a524edbd4ab9cd03
P03_R1_BLOCKER_SHA256=0b76111e955eb6e555b9bb711ad4c876ed487ad878cbe53f62a63021d7eedf90
P03_R2_AGREE_REVIEW_SHA256=74eecc8cca08d26a9bb35d66f3e30e3796c888c84b4cb93ea3e3b4602ed851a2
P03_BASE_BUDGET_SHA256=f3e0910e670e31a4d6106fdc3f69c879e7312fe9bd710611a40e6c45875ba5b0
P03_CREATE_BLOCKER_SHA256=30542fb098c853b8cdc5c35b9d0b60220ee3dfd2d5c78e41537624c7db3e41cd
P02_STABLE_DECISION_SHA256=f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d
P02_TERMINAL_RECEIPT_INDEX_SHA256=8f56a72b4575ee3c87122c8656931d7bbb5040a5a3c024edb5f2909b81a78fd0
P02_EXTRACTION_BUNDLE_SEMANTIC_DIGEST=98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395
```

The Phase 03 root
`.local/mathdevmcp/evidence/p03-20260712` must remain absent. No partial entry,
implementation, result round, receipt, candidate, or stable decision may exist.
The original bootstrap and budget authorization are consumed immutable history
and may not be invoked or overwritten.

## Create Failure Audit

The single reviewed create invocation exited `2` before allocation because the
old bootstrap performed its full protected-tree scan only in create and rejected
pytest-owned symlinks under P02R3 round-local `governance/tmp`.

Exact live classification:

| Scratch root | Regular files | Directories including root | Symlinks | Formal references outside scratch |
| --- | ---: | ---: | ---: | ---: |
| `p02r3.../rr01/governance/tmp` | 151 | 69 | 12 | 0 |
| `p02r3.../rr02/governance/tmp` | 151 | 69 | 12 | 0 |
| `p02r3.../rr03/governance/tmp` | 151 | 69 | 12 | 0 |

P00, P01, P02, and P02R2 have zero symlinks. P02R3 has exactly 36,
all inside the three roots above, and zero elsewhere. The three scratch trees
have the same observed byte size and inventory shape, but equality is
explanatory only.

## Skeptical Plan Audit

- Wrong baseline avoided: the baseline is the failed R2-reviewed create path,
  not the passing preflight, P02 stable decision, or green tests.
- Proxy rejected: scratch confinement, equal counts, and no formal text
  reference justify a bounded exclusion candidate; they do not prove scratch
  safety or permit broad `tmp` exclusion.
- Hidden default exposed: only three literal paths are excludable. No wildcard,
  new round, alternate phase, nested symlink root, or caller-supplied exclusion
  is accepted.
- Stop conditions are pre-allocation. Any changed count, escaping/relative or
  dangling link, formal reference, unexpected symlink, special file, runtime
  drift, history drift, review/budget mismatch, or payload mismatch stops.
- Artifact fitness repaired: audit and preflight execute the same `_prepare()`
  discovery and byte construction used by create. Create receives the exact
  readiness digest and may only allocate/write/reopen fixed prepared bytes.
- No retry ambiguity: this is a new additive bootstrap and review/budget
  namespace. The failed bootstrap remains unmodified and uncallable here.
- Environment matched: exact CPython 3.11.15, `-B -S`, clean environment,
  measured pytest provenance, CPU-only, no network/backend/model/GPU/install.

Audit decision: `PASS_TO_RECOVERY_REVIEW_ONLY`. Allocation remains closed until
the new plan/bootstrap receive exact independent `AGREE` and the new carry-
forward authorization validates.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Reuse absent P03 root | Create blocker proves no allocation occurred | Preserves planned result namespace without pretending the failed create succeeded | Hidden partial path exists | root absence check in every mode | Reviewed recovery hypothesis |
| Exclude exactly three scratch roots | Live classification and P02 governance layout | They are round-local pytest runtime trees, not formal decision paths | Broad exclusion hides evidence or malicious link | literal registry, counts, reference scan, symlink target checks | Reviewed recovery hypothesis |
| Require exact scratch counts | Observed 151/69/12 per round | Detects any post-review drift before allocation | Benign cleanup blocks entry | stop and re-review; never silently update | Frozen recovery observation |
| Absolute in-root symlink targets only | All 36 observed links use this form | Simple deterministic confinement check | Relative or escaping target is followed or ignored | target must map to inventoried regular file/directory | Reviewed integrity default |
| Same `_prepare()` for preflight/create | Create-blocker root cause | Removes create-only discovery | prepare output changes between calls | readiness digest supplied in exact create argv | Reviewed engineering default |
| Five entry files | Four base files plus exclusion ledger | Makes exclusion visible and immutable | downstream assumes four-file entry | recovered schema/version and exact tree test | Reviewed additive schema |
| Single writer during create | Supervisor-controlled gated execution | Filesystem traversal cannot provide an adversarial atomic snapshot without a cooperating lock/snapshot facility | Another process mutates reviewed inputs after their final scan | preflight/create readiness equality catches earlier drift; any observed concurrent writer or reopen mismatch stops | Explicit execution assumption |

No scientific default, mathematical search, or backend policy changes.

## External-Tool-First Ledger

No mathematical derivation, proof, counterexample, or premise search occurs.
SymPy, SageMath, Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph, and LeanDojo
remain considered but inapplicable to filesystem entry recovery and are not
run. Repository-native canonical evidence helpers and OS descriptor APIs are
the selected deterministic tools. This produces engineering provenance only.

## Recovery Design

### Exact Namespaces

- recovery plan:
  `docs/plans/mathdevmcp-real-document-remediation-phase-03r1-entry-bootstrap-recovery-subplan-2026-07-13.md`;
- recovery bootstrap:
  `docs/plans/p03r1_entry_recovery_bootstrap_20260713.py`;
- independent review:
  `docs/reviews/mathdevmcp-real-document-remediation-phase-03r1-entry-recovery-plan-review-r3-result-2026-07-13.md`;
- carry-forward authorization:
  `docs/plans/mathdevmcp-real-document-remediation-phase-03r1-review-budget-carry-forward-2026-07-13.json`;
- entry root remains:
  `.local/mathdevmcp/evidence/p03-20260712/entry`.

### Exact Scratch Policy

The only excluded roots are:

```text
.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr01/governance/tmp
.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr02/governance/tmp
.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/governance/tmp
```

Each root is opened through a descriptor chain with `O_NOFOLLOW`. Its complete
inventory is traversed descriptor-relative without following links. Every
regular file is hashed; every directory is counted; every symlink target must
be absolute, remain inside the same exact scratch root, and map to a separately
inventoried regular file or directory. Counts must equal 151 files, 69
directories including root, and 12 symlinks per root. Each root must contain
exactly 74,331 regular-file bytes and reproduce its reviewed ordered inventory
digest; counts alone cannot pass.

Before any scratch inventory is accepted, the bootstrap enumerates direct
P02R3 `result-rounds/<round>/governance/tmp` nodes through `O_NOFOLLOW`
descriptor chains. The complete discovered set must equal the three literal
registered roots. An unregistered fourth root is a veto even when it contains
no symlink and would otherwise look like formal content.

Formal predecessor trees are traversed separately with those exact directory
nodes skipped before descent. Every symlink outside them is a veto. All formal
P00-P02R3 evidence files are scanned for either logical or absolute references
to any excluded root; any reference is a veto. Recovery control/history files
necessarily name the excluded roots and are instead protected by exact digests.
Scratch files, directories, links, and targets are never included in the
protected manifest.

### No-Write Readiness

`--mode audit` requires no review/budget and constructs all base payloads in
memory. `--mode preflight` additionally requires exact agreeing review and
carry-forward authorization and constructs the exact final five payloads in
memory. Both write nothing.

The authority-bound preflight returns a canonical readiness digest over:

- exact review/budget digests;
- all five payload digests;
- every scratch inventory digest;
- manifest/reference counts;
- measured runtime provenance;
- all ordered P02 obligation state/eligibility bindings;
- P03 root absence.

To avoid a self-referential record hash, payload construction uses two levels.
The canonical `p03r1_entry_preparation@1` digest covers authority, predecessor
state, runtime, reference counts, and the four non-record payload digests; that
digest and the final readiness schema identifier are embedded in
`entry-record.json`. The canonical `p03r1_entry_readiness@2` projection then
covers the complete preparation projection, its digest, and the serialized
entry-record digest, so all five exact payloads are bound before allocation.

Create requires the exact readiness digest in argv and reruns the same complete
`_prepare(require_authority=True)` before allocation. A mismatch fails before
allocation. `_allocate()` independently requires the exact five payload keys,
rehashes each prepared payload against the readiness fields, and reconstructs
the canonical final readiness projection before `_mkdir_entry`. After
`_prepare`, create may only allocate fixed directories, write
the five precomputed byte payloads with no-replace operations, reopen those
fixed output paths, and enumerate only the new output directories to verify the
exact tree. There is no post-prepare input/history/runtime/source/scratch
discovery, create-only input scan, or payload construction.

### Carry-Forward Authorization

The existing budget artifact remains immutable. After recovery review `AGREE`,
write strict canonical JSON with schema
`p03r1_review_budget_carry_forward@1` binding:

- old budget ref/digest;
- old R2 review ref/digest;
- new recovery plan ref/digest;
- new recovery review ref/digest;
- one result-review reservation;
- one separate final-seal-audit reservation;
- `authority: human_user` and date `2026-07-13`;
- the non-claim that carry-forward is authority only, not a verdict/signature.

No review count is replenished or repurposed.

### Recovered Entry Schema

The exact five files are:

```text
entry-record.json
implementation-entry-sha256.txt
protected-entry-sha256.txt
immutable-input-sha256.txt
scratch-exclusion-ledger.json
```

`p03_entry_record@2` preserves the base plan, failed bootstrap/blocker, R1/R2
history, recovery plan/bootstrap/review/carry-forward, master/P02 artifacts,
ordered obligations, action registry, runtime measurement, allowlist, the four
non-record payload bindings, entry-preparation digest, final-readiness schema,
CPU-only mode, and disabled publication. The non-self-referential final
readiness digest and entry-record hash are preserved together in the preflight/
create result and visible execution ledger.

The exclusion ledger records each exact root, result round, inventory digest,
counts, byte count, all link records and targets, exclusion reason, formal
reference count zero, formal protected-file count, and non-claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can Phase 03 allocate its exact immutable entry while excluding only proven non-evidence pytest scratch and preserving every formal predecessor byte? |
| Exact baseline | Failed R2-reviewed create with whole-tree `_tree_refs`, passing but incomplete old preflight, absent P03 root, and exact live P02R3 scratch inventory. |
| Primary pass criterion | Full audit and authority-bound preflight construct exact five payloads without writes; only three literal scratch roots are excluded; all 36 links are confined and target inventoried in-root nodes; formal references are zero; every other predecessor path is symlink-free and protected; create readiness digest matches and exact five files reopen. |
| Veto diagnostics | History/runtime/source drift; changed scratch count/inventory; relative, dangling, escaping, or unexpected symlink; special file; formal scratch reference; broad/caller exclusion; review/budget mismatch; create-only discovery; P03 root preexistence; payload/readiness mismatch; any backend/source edit/publication. |
| Explanatory only | Equal scratch sizes, green tests, scan duration, reviewer agreement, and scratch contents. |
| Not concluded | No validation of scratch test outputs, semantic/context correctness, mathematical claim, backend fitness, source-edit eligibility, publication, Phase 04 readiness, or release readiness. |
| Preserved artifact | Five-file recovered entry with exact exclusion ledger and all predecessor/recovery bindings. |

## Required Checks And Tests

Before review:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -B -S -c 'from pathlib import Path; compile(Path("docs/plans/p03r1_entry_recovery_bootstrap_20260713.py").read_bytes(), "docs/plans/p03r1_entry_recovery_bootstrap_20260713.py", "exec")'
/usr/bin/env -i HOME=/tmp/mathdevmcp-p03r1-entry-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin PYTHONHASHSEED=0 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -B -S docs/plans/p03r1_entry_recovery_bootstrap_20260713.py --mode audit
git diff --check
```

Required disposable mutation cases, each before allocation:

- symlink outside all exact scratch roots;
- relative, dangling, or out-of-root scratch symlink;
- fourth scratch root or caller-supplied exclusion;
- scratch count/file-byte drift;
- formal artifact containing a logical or absolute scratch reference;
- special file in formal or scratch tree;
- changed history/runtime/review/budget digest;
- pre-existing or partial P03 root;
- changed readiness digest;
- changed, missing, or extra prepared payload;
- create path attempting discovery after prepare.

The last mutation check poisons every prepare-time input-discovery helper and
then calls `_allocate()` with fixed disposable prepared bytes. It must create,
reopen, and shape-check only those outputs without invoking a poisoned helper.

The formal post-review sequence is:

1. exact `--mode preflight`, producing `READY_NO_WRITE` and readiness digest;
2. confirm P03 root absent and all reviewed/history digests unchanged;
3. invoke exact `--mode create --readiness-digest <digest>` once;
4. independently reopen and verify the exact five files, digests, schema,
   exclusion ledger, runtime, obligations, allowlist, and disabled publication;
5. update visible ledger/handoff and only then begin Phase 03 implementation.

## Required Artifacts

- reviewed recovery plan/bootstrap and exact agreeing R3 review;
- immutable carry-forward authorization;
- audit and authority-bound preflight outputs recorded in the execution ledger;
- five-file recovered entry;
- post-create independent verification note;
- updated visible ledger and stop handoff.

Audit/preflight stdout is diagnostic execution history, not an entry artifact or
mathematical claim. If create fails after allocation, preserve partial state and
require human recovery; never retry.

## Forbidden Claims And Actions

- Do not edit/reinvoke the failed bootstrap or overwrite the old budget.
- Do not delete, rewrite, chmod, relink, dereference, or normalize P02 scratch.
- Do not exclude any path except the three literal roots.
- Do not accept a symlink outside them or a target not inventoried inside its
  own root.
- Do not treat scratch exclusion as evidence that scratch tests passed.
- Do not omit a formal predecessor file merely because it is large, temporary-
  sounding, unreferenced, or inconvenient.
- Do not allocate before exact recovery review and carry-forward validation.
- Do not run Phase 03 implementation, mathematical backends, models, network,
  GPU, installers, source edits, publication, commit, push, or Phase 04.

## Exact Handoff Conditions

Phase 03 implementation may begin only after:

- R3 `AGREE` binds exact recovery plan/bootstrap and all failure history;
- carry-forward JSON validates and preserves one result/final review each;
- full no-write preflight returns `READY_NO_WRITE`;
- exact readiness-bound create succeeds once;
- entry has exactly five regular non-symlink files;
- exclusion ledger has three roots, 453 files, 207 directories, 36 links,
  zero formal references, and every target confined/inventoried;
- all P02 stable/terminal/source/runtime/obligation/action bindings reconstruct;
- base Phase 03 allowlist and non-claims remain unchanged;
- publication is disabled and zero backend/source-edit activity occurred.

## Stop Conditions

Stop before allocation for review `REVISE`, missing/malformed carry-forward,
history/runtime/P02/source drift, any scratch inventory/count/reference/link
failure, unexpected symlink/special path, incomplete protected manifest,
pre-existing P03 root, readiness mismatch, or inability to maintain the
single-writer execution window.

Stop after allocation for any write/reopen/tree/schema/digest mismatch. Preserve
the partial root, write a blocker, and require human direction. Never retry or
reinterpret the failed state.

## End Procedure

1. Run audit and mutation checks.
2. Obtain exact R3 review.
3. On `AGREE`, write/validate carry-forward JSON.
4. Run full no-write preflight and capture readiness digest.
5. Run one exact readiness-bound create.
6. Independently verify and record the recovered entry.
7. Update ledger/handoff and proceed to base Phase 03 implementation only if all
   entry handoff conditions hold.
