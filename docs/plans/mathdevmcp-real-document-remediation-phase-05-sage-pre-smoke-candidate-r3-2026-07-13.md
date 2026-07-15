# Phase 05 Sage Pre-Smoke Candidate R3

Date: 2026-07-13

Status: `EXECUTED_PASS_REVIEWED`

Result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md`

Prior results:

- `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-01-result-2026-07-13.md`
- `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-02-result-2026-07-13.md`

## Decision

Adapter v3 completed one authorized Sage smoke through the v2
`sage --python input.py` route. It repaired the R2 blocker by separating the
closed evidence-file inventory from bounded runtime scratch. Scratch was not
assumed empty and no observed Sage filename was hardcoded as acceptable.
Instead, the complete recursive scratch tree was constrained, hashed, sealed
in manifest v3, and independently reconstructed during verification.

Attempts 01 and 02 remain failed engineering diagnostics. They were not reused,
overwritten, or counted as live capability evidence. The third Sage action ran
once under the exact command below and passed; no fourth Sage action ran.

## Skeptical Repair Audit

| Risk | Result |
| --- | --- |
| Patch overfits R2 filenames | Pass. V3 permits no filename-specific exception. It inventories any bounded regular file/directory below only the exact scratch roots. |
| Scratch becomes an unbounded escape hatch | Pass. Only `home`, `dot-sage`, and `tmp` may be root directories; root evidence files remain closed. Scratch has entry, depth, path-length, link, file-type, per-read, and aggregate-byte bounds. |
| Scratch mutation is invisible | Pass. Paths, kinds, modes, byte counts, and file SHA-256 values are sealed; verification reconstructs and compares canonical typed JSON. |
| Symlink/hard-link/special-file escape | Pass. All are rejected recursively. Root evidence hard links are also rejected. |
| Sparse or growing file defeats memory bound | Pass. Descriptor metadata is bounded before reads; reads enforce a byte cap and stable size. The manifest itself has a 10 MiB absolute pre-parse cap. |
| Synthetic runner becomes capability evidence | Pass. Injected runners remain `fake_runner`. A failed live process launch is now `not_run`, not live evidence. |
| Proxy criterion replaces specialist gate | Pass. Offline tests and R2 scratch replay are engineering evidence only. The primary criterion still requires one genuine Sage result, verified v3 manifest, and exact P04 child transition. |
| Retry changes the mathematical target or budget | Pass. Target, domain, executable, version prefix, no-network boundary, CPU-only mode, and all resource limits are unchanged. |

Pre-run audit decision: `PASS_TO_ONE_NEWLY_AUTHORIZED_V3_SMOKE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can adapter v3 execute the exact polynomial equality through Sage, seal both evidence and bounded runtime scratch, independently verify the whole bundle, and advance only the bound child? |
| Comparator | Attempts 01 and 02, which failed before manifest sealing because v1/v2 modeled normal Sage filesystem behavior incorrectly. |
| Primary pass criterion | One selected pytest node exits zero; adapter returns `certified`, `live_tool_executed=true`, `manifest_verified=true`, and `can_promote=true`; v3 manifest independently verifies; exact child becomes `proved`; parent stays blocked; publication stays disabled. |
| Vetoes | Skip; timeout; nonzero exit; process not launched; malformed/truncated output; wrong target/domain/version/command/media type; unregistered root entry; scratch symlink, hard link, special file, unstable file, overflow, or inventory mismatch; invalid manifest; wrong branch transition; publication leak; outer timeout. |
| Explanatory only | Test count, version preflight, R2 scratch replay, executable digest, wall time, and byte/entry counts. |
| Non-claims | No general Sage soundness, broader algebra support, real-document repair capability, expectation theorem, search completeness, backend default, publication, release, Phase 06 result, or mission completion. |
| Result artifact | `/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json`; the live gate passed and the Phase 05 result records its interpretation. |

## V3 Scratch Contract

The run root has a closed top-level inventory:

- evidence files: `input.py`, then after sealing `stdout.bin`, `stderr.bin`,
  `result.json`, and `manifest.json`;
- scratch roots: exactly `home/`, `dot-sage/`, and `tmp/`.

Every scratch root and descendant is recursively inventoried with:

- workspace-relative POSIX path;
- kind: regular file or directory only;
- permission mode;
- byte count, with zero for directories;
- SHA-256 for files and null for directories.

Fixed additional limits:

| Limit | Value |
| --- | ---: |
| Scratch entries, including roots | 2,048 |
| Scratch depth below a declared root | 32 |
| Relative path length | 512 characters |
| Manifest read before parsing | 10 MiB |
| Evidence plus scratch file bytes plus manifest | Existing request limit of 10 MiB |

Files with multiple hard links, symlinks, FIFOs/devices/sockets, size changes,
or reads beyond the bound fail closed. Directory allocation blocks are
explanatory filesystem overhead; regular-file content bytes and the full
inventory are bound into the evidence contract.

This is post-process integrity accounting for a fresh private run root. It
detects the bounded scratch state observed when sealing and re-verifying the
completed run; it is not a hostile concurrent same-user sandbox guarantee and
does not claim to prevent another same-user process from racing filesystem
inspection. The outer fresh user/network namespace reduced exposure for this
smoke but is not represented as a general security boundary.

## Exact Inputs

| Field | Value |
| --- | --- |
| Tool | `/usr/bin/sage`, expected version prefix `9.5` |
| Observed version | `SageMath version 9.5, Release Date: 2022-01-30` |
| Sage wrapper SHA-256 | `f306bccc2981095158ba2067022ce7f0538315a67980a84e807e471efe641401` |
| Target | `(x + 1)**2 = x**2 + 2*x + 1` |
| Domain | Exact univariate polynomials over `QQ` |
| Adapter | `p05-sage-adapter@3` |
| Manifest | `p05_sage_execution_manifest@3` |
| Native input | `input.py`, `text/x-python`, 1,967 bytes, SHA-256 `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` |
| Tool timeout | 30 seconds |
| Search wall time | 45 seconds |
| Outer timeout | 60 seconds plus 5-second kill grace |
| Output/artifacts | 1 MiB aggregate output; 10 MiB aggregate artifacts |
| Scope | One target, one child, one attempt |
| Isolation | `CUDA_VISIBLE_DEVICES=-1`; fresh unprivileged user/network namespace |
| Publication | Disabled |

No seed, dataset, stochastic setting, hyperparameter, or performance comparison
applies.

## Current Code Identity

Git commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with an intentionally dirty
worktree.

| File | SHA-256 |
| --- | --- |
| `src/mathdevmcp/external_adapter_contract.py` | `a8ee620f2d0ade8df33e7393bc84f4275bd8a87f2e678870797130a4a1807125` |
| `src/mathdevmcp/sage_adapter.py` | `e78bcb2ebb51b5167f28c88f5be7e5ea7d2a0e91a7093da7ada0fbc089aaa20c` |
| `src/mathdevmcp/derivation_search_orchestrator.py` | `3e8e87702903c8fe9a73d8c171945908cda405f1179cba3a524823c841668a83` |
| `tests/test_external_adapter_real_smoke.py` | `1c9b3c5a03aeb9d4988037c2e4f5a1b874157acaca8d70fa10fd480b529cdebf` |
| `tests/test_sage_adapter.py` | `20f18a067f2b37d9ea57eef9e590e46748c562d4f231edd1980a24e7950975dc` |
| `pyproject.toml` | `d6ddae475f8f65583b161fd41a7e29c171316b2d17eda06d807128c4356c8052` |

These are the pre-execution identities bound by this candidate. Focused
review-driven verifier and test hardening after the run is recorded in the
Phase 05 result and review record; it neither changes the executed native input
nor authorizes a rerun. The preserved live artifact remains acceptable only if
the current verifier independently accepts it.

## Offline Verification

| Check | Result |
| --- | --- |
| V3 Sage adapter suite | 52 passed in 0.36 s before the final fixture replay; final scope remains included in the canonical result below |
| Canonical Phase 05 offline suite | 187 passed in 2.72 s after all v3 hardening |
| R2 artifact replay through v3 scanner | Pass: exact untouched R2 root becomes one registered `input.py`, 11 scratch entries, 55 scratch file bytes, and no unexpected root entry |
| R2 topology fixture | Pass: cache, R config, database, matplotlib, nested temp, home, and tmp forms are recursively sealed and verified |
| Adversarial scratch/manifest cases | Pass: mutation, boolean count, symlink, hard link, special file, entry overflow, sparse-byte overflow, unexpected root directory, oversized manifest, hard-linked manifest, and failed-process-launch provenance |
| Adjacent publication/document regressions | 32 passed in 386.06 s before v3; v3 changes only the isolated Sage adapter/manifest path, and the canonical branch/promotion integration passes after v3 |
| Compilation | Passed for all Phase 05 implementation modules and the live-smoke test after v3 |
| Smoke collection | Exactly one selected Sage node |
| Diff hygiene | `git diff --check` passed |

All Sage adapter pytest bodies are fake/synthetic engineering evidence. The R2
replay reads only the already-failed scratch tree. Neither satisfies the live
specialist gate.

## Exact Command Executed

```bash
env CUDA_VISIBLE_DEVICES=-1 \
  MATHDEVMCP_ENABLE_EXTERNAL_SMOKE=1 \
  MATHDEVMCP_SAGE_PATH=/usr/bin/sage \
  MATHDEVMCP_P05_ARTIFACT_ROOT=/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z \
  PYTHONPATH=src \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /usr/bin/timeout --signal=TERM --kill-after=5s 60s \
  /usr/bin/unshare --user --map-root-user --net --fork --kill-child=KILL \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -vv -rs \
  --maxfail=1 -p no:cacheprovider -p no:logging \
  tests/test_external_adapter_real_smoke.py::test_sage_exact_polynomial_branch_live_smoke \
  -m requires_external_tool
```

The test will internally invoke exactly:

```text
/usr/bin/sage --python <fresh-run-root>/input.py
```

## Executed Boundary And Handoff

- The explicit approval covered only the command above and read-only
  verification of its artifact root.
- The command passed, so no R4 retry or Lean fallback ran.
- Independent verification, the Phase 05 result, and one substantive local
  claim-boundary review completed before Phase 06 planning.
- No external-network access, GPU, installation, persistent environment
  mutation, source-document edit, publication, commit, push, release,
  model/API, Lean, or jixia action ran. The command did create the declared
  isolated network namespace.
