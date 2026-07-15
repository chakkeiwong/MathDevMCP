# Phase 05 Sage Smoke Attempt 02 Result

Date: 2026-07-13

Status: `FAIL_ENGINEERING_RUNTIME_SCRATCH_CONTRACT`

Candidate:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-pre-smoke-candidate-r2-2026-07-13.md`

## Decision

The repaired adapter-v2 smoke does not pass Phase 05. The exact one-node test
failed in 1.87 seconds because the final child was `failed`, not `proved`.
No third Sage attempt or fallback tool was launched.

Adapter v2 removed the `.sage` pre-parser mismatch, but retained an invalid
assumption: it required the bounded `DOT_SAGE`, `HOME`, and `TMPDIR` runtime
scratch directories to stay empty. A normal Sage 9.5 import populated
`DOT_SAGE` before the adapter could seal stdout, the structured result, or the
manifest. This is an engineering evidence-contract failure, not mathematical
refutation and not Sage capability evidence.

## Exact Diagnostic

The v2 route wrote the exact 1,967-byte `input.py` and invoked Sage through its
documented `--python` mode. The resulting run root contained no `.sage` or
`.sage.py` file. It did contain normal Sage runtime scratch:

- `DOT_SAGE/cache/<sage-lib-digest>-lazy_import_cache.pickle`;
- `DOT_SAGE/R/Makevars.user`;
- empty `DOT_SAGE/db`, `DOT_SAGE/matplotlib-1.5.1`, and nested
  `DOT_SAGE/temp/<hostname>` directories.

The installed Sage source confirms that these are expected side effects:

- `sage.misc.lazy_import_cache.get_cache_file()` deliberately returns a path
  below `DOT_SAGE/cache`;
- `sage.misc.misc` creates `DOT_SAGE`, `DOT_SAGE/db`, and
  `DOT_SAGE/temp/<hostname>/<pid>` for normal runtime use.

Therefore, "runtime scratch must remain empty" is the wrong baseline. The
correct boundary is: evidence files must have a closed inventory, while
runtime scratch must be contained, bounded, recursively inventoried, free of
symlinks/special files, and bound into the manifest.

## Artifact Inventory

Artifact root:
`/tmp/mathdevmcp-p05-sage-smoke-r2-20260713T112100Z`

Run root: `sage-run-6pkjl2j0`.

| Artifact | Bytes | SHA-256 | Interpretation |
| --- | ---: | --- | --- |
| `input.py` | 1,967 | `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` | Exact adapter-v2 native input |
| `dot-sage/cache/971645406fd8089013bdc1c964f4f7292e2d5525d21def56d28a5a0f73e70ca4-lazy_import_cache.pickle` | 5 | `926248e52d1fa532c317e37da24ed652ae64110f8219cb5e061668bd3091f048` | Sage lazy-import scratch cache |
| `dot-sage/R/Makevars.user` | 50 | `95406dc42ef49a7df96dc5625fc4cc524f916dc828098d50fde1d6ee9b6c1dd1` | Sage/R scratch configuration |

The entire run root occupied 42,982 bytes by `du -ab`, well below the 10 MiB
budget. No `stdout.bin`, `stderr.bin`, `result.json`, or `manifest.json` was
sealed. Their absence is a capability veto, not a negative mathematical
result.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Unanswered: there is still no verified live manifest and exact child transition. |
| Primary criterion | Fail. The child did not reach `proved`. |
| Veto | Triggered: the v2 manifest contract rejected normal bounded runtime scratch. |
| Explanatory only | Sage source inspection, scratch filenames, byte counts, and pytest wall time. |
| Not concluded | No polynomial proof/refutation, general Sage fitness, Sage unavailability, real-document repair capability, Phase 05 pass, publication, release, or mission completion. |

## Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Fail for adapter v2 live evidence sealing. Exact `--python input.py` routing worked far enough to expose normal Sage scratch creation, but the scratch contract was invalid. |
| Mathematical validity | Empty. No sealed payload or independently verified manifest exists. |
| Scientific interpretation | The failure weakens the adapter's runtime model, not the mathematical target or the external-tool-first strategy. |

## Next Justified Repair

An adapter-v3 design may proceed offline. It must:

1. preserve the closed root evidence inventory;
2. allow only the declared `home`, `dot-sage`, and `tmp` scratch roots;
3. recursively reject symlinks, special files, hard-linked files, traversal,
   excessive entry counts, and aggregate-byte overflow;
4. record every scratch directory/file path, type, mode, byte count, and file
   digest in the manifest;
5. independently reconstruct and compare that inventory during verification;
6. include scratch bytes in the 10 MiB artifact limit;
7. retain `sage --python input.py`, exact target/domain binding, no network,
   CPU-only execution, and publication quarantine.

Offline tests may establish this contract. They cannot authorize or substitute
for another live specialist action.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Attempt 02 fails as an engineering runtime-scratch contract mismatch. |
| Primary criterion | Fail: no verified manifest or promoted child. |
| Veto status | Runtime scratch incorrectly rejected before evidence sealing. |
| Main uncertainty | Whether a recursively inventoried scratch contract can seal the exact Sage result without admitting unbounded or unbound side effects. |
| Next justified action | Implement and test adapter v3 offline; stop before live execution for a new plan and explicit authorization. |
| Not concluded | Mathematical failure, tool failure, Phase 05 closure, Phase 06 entry, or mission completion. |

## Post-Run Red Team

The strongest alternative explanation is directly supported by Sage's local
source: the adapter confused bounded scratch with evidence artifacts. Merely
adding the two observed files to a fixed allowlist would overfit this machine
and remain wrong for other Sage imports or versions.

The conclusion would be overturned if the files were shown to come from user
startup hooks or an unbounded external route. The run used a fresh `DOT_SAGE`,
bounded home/tmp roots, no network, and exact Sage 9.5 source paths; current
evidence instead supports normal runtime creation.
