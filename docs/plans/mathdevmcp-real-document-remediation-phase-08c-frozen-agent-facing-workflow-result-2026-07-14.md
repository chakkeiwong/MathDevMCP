# MathDevMCP Phase 08C Frozen Agent-Facing Workflow Result

Date: 2026-07-14

Status: `INCOMPLETE_P08C_PRODUCT_CRITERION`

## Outcome

The frozen Phase 08C workflow ran once per document and independently verified
the resulting continuation. Source, parent, code, request, target order,
actionability, compact/detailed semantic parity, path privacy, publication
quarantine, and zero-mathematical-backend boundaries all passed. The compact
product criterion did not pass:

| Document | Compact canonical bytes | Limit | Detailed canonical bytes | Result |
| --- | ---: | ---: | ---: | --- |
| Card NPV | 159,837 | 25,600 | 1,960,616 | `exceeded_complete_boundary_preserved` |
| Risky debt | 131,379 | 25,600 | 1,518,994 | `exceeded_complete_boundary_preserved` |

The overage was preserved rather than repaired by dropping a veto, assumption,
action, or reference. This is a product-transport failure, not a safety failure,
mathematical refutation, or loss of the independently verified P08B scoped
computational result.

## Run Manifest

| Field | Value |
| --- | --- |
| Continuation root | `.local/mathdevmcp/evidence/p08-20260714/continuations/20260714T080342Z-3a1e3445eeab` |
| Continuation binding | `ab95aa4e9843d9bd2dc934c7a6215c26139aaefbb686f4e3ba2517fe584bd726` |
| Parent run | `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0` |
| Parent run binding | `14a49479769439925a6e3f9ad293b1b0fcea5a61f81ec454fbaea5ea80da8fb0` |
| P08C code identity | `95778da5fb56ec58208d6d937700c8d107abd675f74b73e450e34e4302ba9584` |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with intentional uncommitted remediation work |
| Interpreter | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3` (CPython 3.11.15) |
| Startup | `-I -S -B -X pycache_prefix=/dev/null` |
| CPU/GPU | CPU-only; GPU intentionally hidden with `CUDA_VISIBLE_DEVICES=-1` |
| Request controls | `smoke`, `max_attempts=0`, `workers=1`, `target_limit=20` |
| Seeds | N/A; deterministic local workflow |
| Created | `2026-07-14T08:03:42Z` |
| Plan | `docs/plans/mathdevmcp-real-document-remediation-phase-08c-frozen-agent-facing-workflow-subplan-2026-07-14.md` |
| Result | This file |

The exact implementation-review bytes were:

| Artifact | SHA-256 |
| --- | --- |
| `scripts/run_p08c_frozen_workflow.py` | `3d048ed23869fa2f8c547ce4a4540c80299cfd86c5017102d12a52de8981a5f8` |
| `tests/test_p08c_frozen_workflow_runner.py` | `f6eacca69ed1e6f5de3f745bc3f2a7c33e791f69b217afe0b508c3017e7ead55` |
| P08C subplan | `c9495b70f340a94dd007b5c1992d0ff9acb2758984d657ce222b023c78b0bd85` |

Fresh independent implementation review returned `VERDICT: AGREE` before
execution.

## Actual Commands

Both commands used the plan's exact scrubbed environment and a 900-second
supervisor deadline. The create command returned the literal continuation root
and decision digest; the verify command executed the snapshotted runner and
used both literal values.

```text
scripts/run_p08c_frozen_workflow.py create --parent-run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0 --continuation-root .local/mathdevmcp/evidence/p08-20260714/continuations --budget-profile smoke --max-attempts 0 --workers 1 --target-limit 20

.local/mathdevmcp/evidence/p08-20260714/continuations/20260714T080342Z-3a1e3445eeab/code-snapshot/scripts/run_p08c_frozen_workflow.py verify --continuation-root .local/mathdevmcp/evidence/p08-20260714/continuations/20260714T080342Z-3a1e3445eeab --expected-decision-digest 0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3
```

Create and verify both returned `INCOMPLETE_P08C_PRODUCT_CRITERION`; verify
returned `verified: true`.

## Preserved Evidence

| Artifact/result | Identity or measurement |
| --- | --- |
| P08C decision digest | `0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3` |
| P08C decision file SHA-256 | `4b9fdc196892cf13ebb4cbc3587ef4e6d5d0c25b04ff2d800f4edafe2c6c7a3c` |
| Parity/size file SHA-256 | `8eedfc5d1a93bb0fa00ccdc03bea5374f79eb34ec3e0168b7a20b269a0a5ca03` |
| Card request/audit SHA-256 | `32a7793e5f1674edb2e9690429d2a4998316bd780385bce8867355c61fda3a45` / `25360385c7fab0012965ac14cf9bdb11eef0687296e9f1ff46c616c882f6fcfd` |
| Risky request/audit SHA-256 | `fee205368a9af4d2a399d43827352d14830a02ade2e0ba35b3ff7ec231a638be` / `010247eb5c1f2532e1ba13d4934fe0dd79106485d69400d1c6031c404cb1c443` |
| Raw audit invocations | Card 1; risky debt 1 |
| Mathematical backend attempts | 0 |
| Operational probes | 66 total; 33 per document; all returned 0 |
| Probe classes per document | 21 Conda environment listings, 8 backend-Python package/version probes, 4 executable version probes |
| Publication/promotion/proof | `false` / `false` / `false` |
| Decision veto | `compact_product_criterion_not_met` only |

P08C did not execute SymPy, Sage, Lean, proof search, retrieval, a model, or a
network service. It consumed the independently verified P08B result read-only.
The doctor calls were bounded local provenance probes and carried no
mathematical authority.

## Payload Diagnosis

The overage is structural repetition, not one unusually long mathematical
statement:

| Contributor | Card bytes | Risky bytes |
| --- | ---: | ---: |
| Current-page target records | 89,957 | 73,743 |
| Global blocker catalog | 38,122 | 29,277 |
| Global reference inventory | 18,712 | 16,103 |
| Global veto IDs | 5,419 | 4,087 |
| Global non-claims | 2,527 | 2,629 |

Each target repeats full assumption records, blocker IDs, evidence/source
records, and a complete Phase 06 action. The action itself contains required
outcome and veto semantics and must not simply be truncated. A read-only
feasibility projection using deterministic one-target pagination, exact global
veto/assumption/action IDs, one complete current-target action, and
content-addressed detailed-record selectors measured about 21.2 KB for card
and 20.6 KB for risky debt. That projection is diagnostic only; it is not the
implemented repair or a passing artifact.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Preserve P08C as product-incomplete and repair transport structure | Failed only the 25,600-byte compact criterion; semantic parity, actionability, path privacy, source/code identity, and quarantine passed | No integrity, engineering, mathematical-attempt, omission, publication, promotion, or proof veto; exact size veto present | Whether normalized references plus byte-aware pagination can remain directly agent-usable across every page | Implement a schema-versioned Phase 08D compact repair against the immutable P08C audits, then replay without rerunning mathematical backends | Phase 08 pass, final mission status, document correctness, proof, best repair, publication/default/release readiness |

## Separate Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Producer and snapshotted verifier agree; exact parent/code/artifact/request identities reconstruct; zero workflow failures and compiler validation errors. |
| Mathematical validity | Inherited P08B `backend_checked` support remains scoped to one derivative. P08C added no mathematical evidence. |
| Scientific interpretation | The system safely exposes actionable frozen-document diagnostics, but the default compact transport is not yet usable within its registered context budget. |

## Negative Result Classification

This is an implementation/product-design failure. It is not a tuning failure,
backend diagnostic failure, or evidence against the mathematical-development
mission. The result weakens the claim that Phase 07's synthetic compact design
generalizes to real documents. The viable repair is deduplication,
content-addressed resolution, and deterministic pagination; omission of
claim-boundary content is not a viable rescue.

## Post-Run Red Team

The strongest alternative explanation is that the 25,600-byte target is too
small for the registered real-document boundary rather than that the compiler
is poorly normalized. The feasibility projection argues against that
explanation for one-target pages, but only an implemented all-page replay can
settle it. The result would be overturned by a repaired response whose page
union reconstructs every target association and whose global boundary is exact
on every page while staying below both canonical and transport limits. The
weakest current evidence is downstream usability across continuations, because
P08C measured only the oversized all-target first page.

## Handoff

Phase 08 is not closed and Phase 09 is not open. Phase 08D may proceed as a
bounded presentation repair using the immutable P08C request/audit files as
replay inputs. It must not rerun or reinterpret the P08B mathematical backend,
weaken publication quarantine, or replace explicit veto and unresolved-
assumption identities with unexplained counts.
