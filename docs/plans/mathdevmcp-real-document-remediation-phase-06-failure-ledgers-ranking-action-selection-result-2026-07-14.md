# Phase 06 Failure Ledgers, Ranking, And Action Selection Result

Date: 2026-07-14

Status: `PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Phase subplan:
`docs/plans/mathdevmcp-real-document-remediation-phase-06-failure-ledgers-ranking-action-selection-subplan-2026-07-13.md`

## Close Decision

Phase 06 passes its engineering selection and eligibility contract. The
implementation classifies failures in separate typed ledgers, compares branches
by a validity-gated partial order, selects one closed discriminating action,
reruns native evidence readers at every authority-bearing consumption, and
recomputes claim eligibility independently from publication.

The first substantive review returned `REVISE` with four high-severity
claim-boundary findings. All four were repaired, their adversarial tests pass,
and a fresh bounded read-only Codex rereview returned `AGREE` with no material
findings. Publication remains disabled on every document, library, CLI,
MCP-facade, and server surface.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can MathDevMCP separate engineering, evidence-integrity, mathematical-validity, and interpretation failures; compare repair branches without scalar compensation; select one exact next discriminator; and compute claim eligibility only from native-reader-authorized evidence while keeping product publication quarantined? |
| Comparator | The pre-Phase-06 scalar branch score, repeated untyped blockers, cached promotion fields, raw normalized JSON, and legacy document reports. |
| Primary criterion | Pass: typed closed ledgers, semantic deduplication, partial-order relations, closed actions, native-reader-revalidated evidence, and the twelve-invariant promotion decision pass focused, adjacent, product-quarantine, and fresh rereview gates. |
| Veto diagnostics | No engineering/evidence failure may improve order; no genuine tradeoff may become a false winner; caller-authored or redigested JSON may not acquire native-reader authority; any failed claim invariant vetoes eligibility; product publication or applicable edits must remain absent. |
| Explanatory diagnostics | Test count, wall time, peak RSS, deterministic serialization order, and the retained Phase 05 result are explanatory. |
| Not concluded | No new theorem, proof/refutation, best repair, calibrated ranking, general Sage/Lean capability, real-document usefulness, publication readiness, Phase 07 result, release readiness, or mission completion. |

## Implementation Result

### Typed ledgers and deduplication

- `src/mathdevmcp/failure_ledgers.py` implements closed engineering,
  evidence-integrity, mathematical-validity, and interpretation entries.
- Unknown statuses fail closed. Every veto names a smallest discriminator and
  required bound artifact.
- Deduplication uses semantic scope and retains all target, source, evidence,
  and origin references. Repeated attempts or blockers cannot improve rank or
  change action semantics.

### Partial-order branch comparison and actions

- `rank_repair_branches()` no longer emits an authoritative scalar score.
- It exposes dominance, equality, and incomparability reasons, nondominated
  branch ids, true tie groups, and a unique top id only when exactly one
  nondominated branch exists.
- Deterministic ordering is serialization-only. The real FOC regression now
  retains three incomparable nondominated assumption routes instead of
  selecting the conditional-kernel route as a scientific winner.
- One closed action records its bound ledger ids, prerequisites, launch
  vetoes, tool route, budget, expected artifact, every terminal outcome, and
  non-claims.

### Evidence provenance and promotion

- Generic `evidence_manifest@1` and Sage
  `p05_sage_execution_manifest@3` keep their native schemas and readers.
- Normalized JSON remains inspectable but never carries authority. Eligibility
  and exact ranking accept only an inert `RevalidatingClaimEvidence` request;
  every consumption reruns the registered native reader against its current
  artifact and immutable Phase 04 input snapshots.
- Exact Phase 04 branch, request, result, obligation, target, assumptions,
  native input, outcome, and manifest bindings are recomputed.
- Ranking receives evidence separately from branches and requires full branch
  validation, lineage, complete branch digest, obligation, target, typed
  assumptions, and typed-assumption digest equality. A legacy or mutated
  same-id branch cannot replay exact evidence.
- The Sage native reader regenerates the exact expected script from the
  verified target, version prefix, and sole `QQ` domain assumption. Only its
  reader-derived assumption digest and script evidence can satisfy normalized
  encoding completeness.
- `evaluate_phase06_promotion()` is additive to the Phase 01 policy and checks
  the twelve Phase 06 invariant groups. Claim eligibility excludes the
  publication invariant; publication requires exact claim eligibility plus
  explicit mode, the independently recorded runtime flag, and the pure
  test-only aggregate fixture.
- Persisted decisions use the closed v2 schema and explicitly declare
  `internal_consistency_only_requires_native_evidence_reevaluation`. Their
  verifier reconstructs all locally knowable semantics, edit integrity,
  manifest references, typed-veto consistency, eligibility, decision, vetoes,
  and reason. Product proposal validation rejects persisted-only authority.

### Document and surface quarantine

- Document reports consume nondominated sets and label their context branch as
  serialization-only when there is no unique nondominated branch.
- Full ledger entries occur once at the ranking root; branch rows retain entry
  and veto ids. Reports refer to the root action by id. This removed redundant
  closed evidence copies without deleting evidence.
- The exact library/facade/server/CLI parity regression that previously aborted
  now passes. All recursive quarantine scans find zero promoted repairs, no
  applicable edit field, and `publication_enabled=false` on product surfaces.
- No Phase 06 experimental mode argument is exposed through the document
  workflow, CLI, MCP facade, or server.

## Repair Loop

| Finding | Repair | Focused evidence |
| --- | --- | --- |
| Cross-surface parity aborted while four large results were retained. | Store one authoritative ranking-level ledger bundle, replace per-branch copies with ids, and reference the root selected action by id in nested reports. | Exact parity test passed in 32.12 s with about 132 MB peak RSS. |
| Persisted verification inferred the runtime publication flag from mode. | Preserve `publication_enabled` as an independent boolean; a mode/flag mismatch is valid but report-only. | Added mutation test; promotion/normalization suite passed. |
| Self-digested normalized JSON could not prove that a native reader produced it. | Added a process-local reader-verification handle issued only by functions that rerun the registered reader; promotion and exact ranking require the handle. | Redigested JSON is ineligible and cannot improve ranking; affected suites passed. |
| A real-document test required the serialization-only branch to contain one particular assumption family. | Require the context to be labeled serialization-only and require the conditional-kernel route to remain in the nondominated alternative set. | Focused FOC regression and complete document suite passed. |
| R1: ordinary mutable Python state was treated as reader authority. | Replace the sealed handle with inert immutable revalidation inputs and rerun the registered native reader at every consumption. | Direct construction, caller JSON, and artifact-mutation-after-construction attacks fail closed. |
| R1: evidence could be replayed onto a mutated same-id branch. | Supply evidence separately and require a valid full Phase 04 record plus exact content digest, lineage, target, obligation, and assumption bindings. | A valid same-id branch with changed blocker state remains non-exact in ranking. |
| R1: persisted decisions trusted self-reported invariant booleans. | Version the schema, add the internal-consistency-only authority marker, validate edit/manifest/id projections, and reconstruct exact decision semantics. | Fully redigested veto, manifest, edit, placement, reconstruction, and reason attacks are rejected. |
| R1: Sage assumption encoding was asserted. | Regenerate the exact script in the native reader and emit assumption encoding only from the verified byte-for-byte projection. | A fully redigested arbitrary script with refreshed request/artifact/manifest hashes is rejected. |

## Verification

All Python and pytest commands used the pinned interpreter
`/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, `PYTHONPATH=src`, disabled
pytest plugin autoload where specified, and `CUDA_VISIBLE_DEVICES=-1`. GPU was
intentionally hidden. No Sage, Lean, network, model/API, or GPU execution was
launched by the local verification ladder.

| Check | Result |
| --- | --- |
| Typed ledger suite | `25 passed in 0.03s` |
| Final native-reader/Sage/promotion focused suite | `95 passed in 1.24s` |
| Final plan-prescribed Phase 04-06 focused matrix | `185 passed in 1.79s` |
| Broader Phase 04-06 adjacency ladder | `211 passed, 1 skipped in 2.06s`; skip is the pre-existing environment-dependent real-adapter smoke |
| Full document derivation plus publication-quarantine suite | `29 passed in 316.44s`; peak RSS `148940 KB`, no swap |
| Exact four-surface parity diagnostic | Passed inside the full product suite; compacted reports remained below the prior crash-level memory footprint |
| Python compilation | Passed for all six Phase 06 implementation modules |
| Diff hygiene | `git diff --check` passed |
| Product surface scan | Experimental mode occurs only in the pure policy module/tests; document surfaces retain disabled mode and false publication flags |

Test counts are explanatory. The primary engineering evidence is the mutation
matrix at each validity boundary and the recursive product quarantine scan.

## Preserved R3 Artifact Limitation

The Phase 06 plan named the ephemeral Phase 05 path
`/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json`
for read-only compatibility verification. After the editor crash and `/tmp`
turnover, that exact path is absent. It was not reconstructed, copied from a
synthetic fixture, or regenerated by running Sage.

The retained Phase 05 result continues to record its historical digest
`7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2`
and prior independent native-reader verification. Current Phase 06 evidence for
the Sage-v3 normalization code is synthetic contract coverage only. Phase 06
does not claim a fresh read of the original R3 bytes or infer its missing Phase
04/source/edit history.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9`; intentionally dirty worktree preserved |
| Branch | `main` |
| Python/environment | CPython 3.11.15 at `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`; pytest 9.0.2 |
| Platform | Linux 6.6.87.2 WSL2 x86_64 |
| CPU/GPU | Deliberate CPU-only checks with `CUDA_VISIBLE_DEVICES=-1`; no GPU action |
| Network/model APIs | Not used for implementation or local checks; independent review is recorded separately |
| Data version | Synthetic current-schema fixtures plus existing focused document regression sources; no frozen-document experiment |
| Random seeds | N/A: deterministic contract and document tests |
| Wall time | Final focused matrix 1.79 s; full combined document/product suite 316.44 s pytest time and 345.68 s measured wall time |
| Output artifacts | This result, Phase 06 source/tests, R1 review result, repair bundle, and fresh rereview result |
| Plan | `docs/plans/mathdevmcp-real-document-remediation-phase-06-failure-ledgers-ranking-action-selection-subplan-2026-07-13.md` |
| Result | `docs/plans/mathdevmcp-real-document-remediation-phase-06-failure-ledgers-ranking-action-selection-result-2026-07-14.md` |

## Separate Ledgers

### Engineering ledger

Closed: typed classification, semantic deduplication, partial-order
serialization, action validation, report compaction, cross-surface parity,
native rerevalidation, branch replay prevention, decision reconstruction,
reader-derived Sage encoding, compilation, diff hygiene, and substantive
rereview pass.

### Mathematical-validity ledger

No new mathematical claim was attempted. Synthetic exact polynomial fixtures
exercise evidence and promotion contracts. They do not establish general Sage
soundness, document repair correctness, or any theorem in a source document.
Missing assumptions and unresolved constructs remain mathematical vetoes.

### Interpretation ledger

The implementation supports honest incomparability and can distinguish claim
eligibility from publication. That is evidence of a safer selection contract,
not evidence that the selected action is likely to succeed or that the system
is useful on the frozen real-document corpus.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT` |
| Primary criterion | Pass: required mutation, adjacency, document/quarantine, and substantive rereview gates pass after all R1 repairs. |
| Veto status | No open Phase 06 engineering, evidence-integrity, mathematical-policy, product-quarantine, or independent-review veto. |
| Main uncertainty | Native artifacts must be available whenever authority is consumed; persisted decisions intentionally cannot stand in for native reevaluation. The original R3 `/tmp` bytes remain unavailable. |
| Next justified action | Launch a compact, publication-disabled Phase 07 product phase under the academic-governance reset. |
| Not concluded | Publication/default enablement, real-document usefulness, backend soundness in general, release readiness, or mission completion. |

## Post-Run Red Team

The strongest alternative explanation is fixture closure: the contracts may be
internally consistent on synthetic Sage and current document regressions while
still being awkward or incomplete for a future persistent service. That is why
the revalidation request is deliberately non-authoritative and a service must
retain native artifacts and rerun their registered readers.

The close decision would be overturned by a native-reader bypass, same-id branch
replay, redigested decision forgery, asserted rather than reader-derived
assumption encoding, validity compensation, false scientific winner, or
applicable edit/publication leakage. Focused attacks cover each current route.

The weakest evidence is downstream actionability and response size. The
compaction repair fixed one parity/resource failure but is not the Phase 07
compact-product benchmark and does not establish the 25,600-byte target.

## Handoff

Phase 07 entry is open for compact agent-facing response engineering. The stale
master-plan requirements for an aggregate cryptographic phase gate and exposed
experimental publication are superseded by the active academic-governance
reset and this result's internal-consistency-only decision boundary. Phase 07
must preserve publication mode `disabled`, add no experimental publication
argument, execute no new backend, and treat payload size as a product guardrail
rather than mathematical evidence.
