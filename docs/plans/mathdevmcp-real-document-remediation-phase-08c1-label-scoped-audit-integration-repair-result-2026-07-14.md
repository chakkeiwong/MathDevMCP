# MathDevMCP Phase 08C1 Label-Scoped Audit Integration Repair Result

Date: 2026-07-14

Status: `PASS_P08C1_TARGET_FIDELITY`

## Outcome

The document derivation workflow now routes focused equation labels through
validated label-scoped obligations before semantic or tree construction. The
fresh P08C1 replay preserves all five frozen P08A obligations exactly,
including complete `lhs`/`rhs`, normalized target, source math, owned/excluded
spans, scoped operator/symbol inventories, and obligation ID/digest.

The defect that blocked P08D is repaired: `eq:incremental-cash-flow` is now the
complete equality under obligation digest
`7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0`,
not its final continuation row. Proposition focus remains context-only, failed
or ambiguous extraction has no legacy-row fallback, and a scoped target no
longer inherits sibling mathematics from its enclosing display.

## Run Manifest

| Field | Value |
| --- | --- |
| Passing run root | `.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801` |
| Decision digest | `8c2ca339fc5a360be7abaa4264a6b33d773995a160437d11ffdcab5d54d86c7b` |
| Decision file SHA-256 | `9b98b29de3bf6b8237370e12e3c3776855619a373b8333c1207b064e197e5d17` |
| Target-fidelity file SHA-256 | `4fd07445dd796fba570fe46c9fa6daf4362ba5f12a740b64ff942a0cea81872b` |
| P08A comparator SHA-256 | `8a0386d360068ff3ee481ea88a170a41abeae6dce5716a55a7c75660859e4da0` |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with intentional dirty remediation work |
| Interpreter | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, CPython 3.11.15 |
| CPU/GPU | CPU-only; `CUDA_VISIBLE_DEVICES=-1` before Python startup |
| Audit controls | `smoke`, `max_attempts=0`, `workers=1`, one invocation per document |
| Mathematical backend attempts | 0 |
| Seeds | N/A; deterministic parsing/audit |
| Wall time | 41.194894 seconds |

The first replay attempt reached audit and target-fidelity construction, then
failed before manifest/decision creation due to a bytes-handling error in git
status bookkeeping. It is visibly marked
`INCOMPLETE_ENGINEERING_ERROR` under
`.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T120726Z-929a05b1b9f6`
and has no passing decision. The type error was regression-tested and the
passing replay was created from scratch without reusing that attempt.

## Actual Commands

```text
CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTHONPATH=src python3 scripts/run_p08c1_target_fidelity_replay.py create

CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0 PYTHONPATH=src python3 scripts/run_p08c1_target_fidelity_replay.py verify --run-root .local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801 --expected-decision-digest 8c2ca339fc5a360be7abaa4264a6b33d773995a160437d11ffdcab5d54d86c7b
```

Create returned `PASS_P08C1_TARGET_FIDELITY`; verify independently reopened
the artifacts, reconstructed all comparisons and mutations, and returned
`verified: true` without rerunning document audit.

## Target Evidence

| Document | Label | P08A obligation digest | Complete lhs/rhs | Exact obligation record | Typed tree input |
| --- | --- | --- | --- | --- | --- |
| Card | `eq:panel-npv-functional` | `cb3a701e28d1da9d837de2f34f14ec8267e223400d153720b688a5b7e05b7b88` | Pass | Pass | Pass |
| Card | `eq:incremental-cash-flow` | `7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0` | Pass | Pass | Pass |
| Card | `eq:incremental-npv` | `d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac` | Pass | Pass | Pass |
| Risky | `eq:foc-k` | `d987e605da2d4e509d0d65289a56e9b7f5d121273543bdf74276b9fb4c23bba5` | Pass | Pass | Pass |
| Risky | `eq:foc-b` | `8d04797cf7e394624890ab2e0b0688f22d86d9194de94af3aa1407fb1a45edca` | Pass | Pass | Pass |

The replay rejected all 14 registered target-text, lhs, obligation-digest,
owned-span, operator-inventory, obligation-record, and target-order mutations.
Its read-only diagnostic also reconstructs the stale P08C failure: the prior
cash-flow packet had `lhs=null`, `rhs=null`, no label-scoped obligation, and
only the final continuation row.

## Local Checks

| Check | Result |
| --- | --- |
| Target/extractor/obligation focus | `19 passed in 130.64s` |
| Full document-tree workflow | `17 passed in 218.28s` |
| Document response compiler | `52 passed in 1.66s` |
| Publication quarantine | `13 passed in 101.03s` |
| MCP surface and P08 frozen runner adjacency | `73 passed in 180.16s` |
| P08C runner guards | `35 passed in 7.63s` |
| P08C1 replay unit checks | `3 passed in 0.04s` |
| Focused `py_compile` | Pass |
| `git diff --check` | Pass |

The old Bellman regression was corrected because it required a focused
`eq:bellman` target to absorb the unlabeled sibling equation `J_c(s)`. The new
assertion enforces scoped ownership and absence of the obsolete multiline-
grouping blocker.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept P08C1 locally, pending substantive review | All five exact P08A obligation records survive target selection, semantic packets, typed obligations, and tree consumption in request order | No fallback, incomplete lhs/rhs, sibling contamination, order/identity, mutation, backend, engineering, publication, or promotion veto in the passing run | Whether the compact representation designed against stale P08C bytes remains feasible for the larger target-faithful audit | Obtain substantive read-only review; if no material finding, refresh P08D feasibility and plan against the passing P08C1 audit | No equation proof, whole-document correctness, compact-product pass, best repair, publication/default/release readiness, Phase 08 closure, or mission completion |

## Separate Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Focused and adjacent suites pass; failed extraction cannot fall back; replay create/verify and all mutations pass. |
| Mathematical validity | Mathematical target identity is repaired and bound to P08A. No backend ran and no mathematical truth claim was added. |
| Scientific interpretation | P08D now has a faithful candidate baseline. The prior P08C payload evidence remains historical and cannot be used for promotion. |

## Post-Run Red Team

The strongest alternative explanation is that exact packet equality merely
duplicates P08A bytes without proving the downstream controller used them.
The replay addresses this by requiring the typed repair obligation embedded in
the compact tree to equal the packet-derived typed record and to carry the same
target/lhs/rhs. The weakest remaining evidence is compact product feasibility:
the repaired audit is materially different and somewhat larger, so all old
P08D payload measurements are stale.

This conclusion would be overturned by a focused label whose packet differs
from its P08A obligation, a mutation accepted by the replay validator, a
backend attempt in the replay, or substantive review finding an alternate
legacy-row ingress. None was observed locally.

## Handoff

P08C1 is closed after a full primary Claude Opus/max read-only R2 review found
no material findings and returned `VERDICT: AGREE`. Refresh P08D's comparator
hashes, feasibility measurements, schema/partition assumptions, and replay
contract against the passing P08C1 audits. Phase 08 and Phase 09 remain closed
until the compact product criterion passes on the target-faithful baseline.

## Independent Review

The first broad primary review timed out with no output despite a healthy
`OK` probe. Its `bounded_fallback_agree` result inspected only the bundle
summary and was explicitly not treated as substantive agreement. The prompt
was narrowed to the exact target-ingress, packet adapter, replay validator,
critical regressions, and 7.4 KB decision/fidelity evidence.

The fresh R2 primary review completed normally:

```text
REVIEW_STATUS=agreed
VERDICT=AGREE
RUN_DIR=.claude_reviews/20260714-202440-mathdevmcp-p08c1-target-fidelity-r2
```

The reviewer found no path for a focused label to re-enter as a physical row
or enclosing display, confirmed exact single-candidate/deduplicated selection
and fail-closed obligation validation, and found the replay/verify comparison
strict across identity, target/lhs/rhs, source, spans, inventories, order,
typed-tree input, artifact inventory, and zero-backend boundaries.

## Non-Claims

- Target fidelity is not mathematical proof or refutation.
- P08C1 adds no backend evidence and authorizes no source repair.
- Publication, promotion, defaults, releases, commits, pushes, and network or
  model execution remain outside the result.
