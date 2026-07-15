# Phase 05 Sage Pre-Smoke Candidate R2

Date: 2026-07-13

Status: `EXECUTED_FAILED_ENGINEERING_RUNTIME_SCRATCH_CONTRACT`

Result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-02-result-2026-07-13.md`

Prior result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-01-result-2026-07-13.md`

## Decision

One repaired Sage adapter v2 smoke is ready for fresh authorization. The scope,
target, mathematical domain, budgets, network isolation, CPU-only policy, and
non-claims are unchanged from candidate R1. The material repair is the exact
Sage invocation and evidence schema: v2 runs manifest-bound ordinary Python as
`/usr/bin/sage --python input.py`, avoiding Sage 9.5's `.sage` pre-parser.

Attempt 01 is frozen as failed engineering evidence and is not reused or
counted. No second live attempt has run.

## Repair Audit

| Question | Result |
| --- | --- |
| Does the repair address the observed cause? | Yes. The `.sage` input and pre-parser are removed from the route rather than silently allowing an unbound generated file. |
| Is the executed source still Sage specialist work? | Yes. `/usr/bin/sage --python` selects Sage's configured Python environment, and the bound source imports `sage.version` and `sage.all` before constructing `PolynomialRing(QQ, ...)`. |
| Is the exact executed source preserved? | Yes. `input.py` is the native input, command target, request-digest input, and manifest artifact. |
| Did the acceptance schema change visibly? | Yes. Adapter and manifest versions are bumped to v2; media type is `text/x-python`; command and environment checks are exact. |
| Could the old failure recur silently? | No. A new test injects `input.sage.py` and requires closed-inventory rejection. The live root must contain only the v2 inventory. |
| Is this a retry fishing for a pass? | No. It is one repaired attempt for a diagnosed wrapper-contract defect. The target, positive criterion, budgets, and tool are unchanged. |

Audit decision: `PASS_TO_ONE_FRESH_AUTHORIZED_V2_SMOKE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can adapter v2 execute the exact `QQ[x]` polynomial equality through `/usr/bin/sage --python`, seal and independently verify its exact evidence, and advance only the bound P04 child? |
| Comparator | Failed adapter v1 attempt 01 plus the passing v2 fake-runner contract. |
| Primary pass criterion | The one selected test exits zero; adapter status is `certified`; live process provenance and v2 manifest verify; only the exact child becomes `proved`; parent remains blocked; publication remains disabled. |
| Vetoes | Skip, timeout, nonzero exit, `.sage` or `.sage.py` artifact, malformed/truncated output, v1 schema, wrong command/media type/environment, invalid manifest, target/domain mismatch, wrong branch, budget overflow, publication leak, or outer timeout. |
| Explanatory only | Test count, version preflight, executable digest, wall time, byte counts. |
| Non-claims | No general Sage soundness, broader expression support, real-document repair, expectation theorem, search completeness, default/release/publication readiness, or mission completion. |
| Artifact | Fresh `/tmp/mathdevmcp-p05-sage-smoke-r2-20260713T112100Z` run root and a post-run Phase 05 result if successful. |

## Fixed Inputs And Limits

| Field | Value |
| --- | --- |
| Tool | `/usr/bin/sage`, expected version prefix `9.5` |
| Target | `(x + 1)**2 = x**2 + 2*x + 1` |
| Domain | Exact univariate polynomials over `QQ` |
| Adapter | `p05-sage-adapter@2` |
| Manifest | `p05_sage_execution_manifest@2` |
| Native input | `input.py`, `text/x-python`, 1,967 bytes, SHA-256 `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` |
| Tool timeout | 30 seconds |
| Branch-search wall time | 45 seconds |
| Outer timeout | 60 seconds plus 5-second kill grace |
| Output | 1 MiB aggregate |
| Artifacts | 10 MiB aggregate |
| Attempts | One target, one child, one attempt |
| Hardware/network | `CUDA_VISIBLE_DEVICES=-1`; fresh unprivileged user/network namespace |
| Publication | Disabled |

No seed, data version, stochastic setting, benchmark comparator, or
hyperparameter applies.

## Current Code Identity

Git commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with an intentionally dirty
worktree. Relevant exact bytes:

| File | SHA-256 |
| --- | --- |
| `src/mathdevmcp/external_adapter_contract.py` | `a8ee620f2d0ade8df33e7393bc84f4275bd8a87f2e678870797130a4a1807125` |
| `src/mathdevmcp/sage_adapter.py` | `dbac49e90dba650e2338b07f13d6f2f17df3868600add27ac56acbf952db3829` |
| `src/mathdevmcp/derivation_search_orchestrator.py` | `3e8e87702903c8fe9a73d8c171945908cda405f1179cba3a524823c841668a83` |
| `tests/test_external_adapter_real_smoke.py` | `1c9b3c5a03aeb9d4988037c2e4f5a1b874157acaca8d70fa10fd480b529cdebf` |
| `tests/test_sage_adapter.py` | `728fcd8ea68940ce987c7b017ad8991fca5163a387e66d193c120a0f35d66914` |
| `pyproject.toml` | `d6ddae475f8f65583b161fd41a7e29c171316b2d17eda06d807128c4356c8052` |

Any digest change makes this candidate stale.

## Verification

| Check | Result |
| --- | --- |
| V2 focused Sage/SymPy suite | 70 passed in 1.99 s |
| V2 canonical Phase 05 offline suite | 174 passed in 2.80 s |
| V2 compilation | Passed for adapter, contract, orchestrator, Lean binding, bridge, and smoke test modules |
| Smoke collection | Exactly one node: `test_sage_exact_polynomial_branch_live_smoke` |
| Diff hygiene | `git diff --check` passed |
| Publication, document-tree, and frozen real-document regressions | 32 passed in 386.06 s with an explicit zero exit |

All Sage test bodies above use fake runners. They are not live capability
evidence.

## Exact Command Requiring Fresh Approval

```bash
env CUDA_VISIBLE_DEVICES=-1 \
  MATHDEVMCP_ENABLE_EXTERNAL_SMOKE=1 \
  MATHDEVMCP_SAGE_PATH=/usr/bin/sage \
  MATHDEVMCP_P05_ARTIFACT_ROOT=/tmp/mathdevmcp-p05-sage-smoke-r2-20260713T112100Z \
  PYTHONPATH=src \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /usr/bin/timeout --signal=TERM --kill-after=5s 60s \
  /usr/bin/unshare --user --map-root-user --net --fork --kill-child=KILL \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -vv -rs \
  --maxfail=1 -p no:cacheprovider -p no:logging \
  tests/test_external_adapter_real_smoke.py::test_sage_exact_polynomial_branch_live_smoke \
  -m requires_external_tool
```

The smoke test will internally invoke exactly:

```text
/usr/bin/sage --python <fresh-run-root>/input.py
```

Expected closed inventory: `input.py`, `stdout.bin`, `stderr.bin`,
`result.json`, `manifest.json`, plus empty `home/`, `dot-sage/`, and `tmp/`
directories. Any `.sage`, `.sage.py`, `__pycache__`, or other file is a veto.

## Stop Rules

- This authorization, if granted, covers only the exact R2 command and
  read-only verification of its new artifact root.
- Any failure stops live execution; do not retry again or switch to Lean.
- A successful run still requires independent manifest verification, a Phase
  05 result, and one substantive claim-boundary review before Phase 06 opens.
- No network, GPU, install, environment mutation, source-document edit,
  publication, commit, push, release, model/API, Lean, or jixia action is
  authorized.
