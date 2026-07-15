# Phase 05 Sage Pre-Smoke Candidate

Date: 2026-07-13

Status: `EXECUTED_FAILED_ENGINEERING_ARTIFACT_LAYOUT`

Result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-01-result-2026-07-13.md`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Phase subplan:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-subplan-2026-07-13.md`

## Decision

The Phase 05 offline implementation and pre-smoke checks pass. One narrowly
scoped trusted Sage action is ready to run after explicit approval. The action
will execute exactly one generated univariate polynomial equality over `QQ`,
inside a fresh unprivileged network namespace, with CPU-only and bounded
process, output, artifact, target, node, and attempt budgets.

The read-only `/usr/bin/sage --version` preflight ran and reported SageMath
9.5. No Sage polynomial action has run. Version output is availability evidence
only and does not satisfy the Phase 05 specialist gate.

Publication remains disabled. The smoke does not read or edit either frozen
source document.

## Skeptical Pre-Execution Audit

| Risk | Audit result |
| --- | --- |
| Wrong baseline | Pass. The comparator is the completed P04 branch-local orchestration contract plus the P05 fake-runner adapter contract, not an older generic Sage route. |
| Proxy metric promoted | Pass. Test count, collection, path existence, and version output are explanatory only. The primary criterion requires a real Sage polynomial process, verified manifest, and exact child transition. |
| Missing stop condition | Pass. Any skip, timeout, nonzero exit, malformed or truncated result, manifest failure, target mismatch, version drift, wrong branch, or publication leak fails this candidate. |
| Unfair comparison | Not applicable. This is a one-route capability discriminator, not a method ranking or performance comparison. |
| Hidden mathematical assumptions | Pass for the scoped target. The generated script constructs both sides independently in `PolynomialRing(QQ, names=('x',))`; no prose assumption is consumed. |
| Stale context | Pass. P04 is closed at semantic tree digest `deae0b2142d19c83c424a7178675cff9a686a4519ea9134f0e0f1f18ca89390a`; the current dirty-worktree implementation is bound below by file digests. |
| Environment mismatch | Pass to smoke. `/usr/bin/sage` is a regular executable and reports SageMath 9.5; CPython is 3.11.15; CPU hiding and a no-network namespace are enforced by the exact command. |
| Artifact cannot answer question | Pass. The adapter persists the exact script, stdout, stderr, structured result, request, command, environment, execution record, and sealed manifest. The test independently verifies that manifest before the child can advance. |

Audit decision: `PASS_TO_ONE_AUTHORIZED_TRUSTED_SAGE_SMOKE`.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Sage is the first live specialist | P05 subplan and local preflight | It is the smallest installed, non-SymPy, no-network executable route | Installed wrapper is incompatible with generated code | Exact version guard and one generated target | Baseline hypothesis |
| Expected version prefix is `9.5` | Fresh `/usr/bin/sage --version` output | Binds the reviewed generated script to the locally observed family | Wrapper or runtime drifts after preflight | Generated script exits `unavailable` before importing algebra modules | Reviewed smoke default |
| Domain is `QQ` | P05 accepted-scope contract | Exact rational polynomial equality has explicit semantics and a deterministic result | Expression is silently interpreted over another ring | Payload and manifest must record `domain=QQ` and exact input sides | Reviewed scope |
| Target is `(x + 1)**2 = x**2 + 2*x + 1` | P05 subplan | Non-textual expansion with independently built sides | Adapter certifies a different or normalized-away target | Request, payload sides, native script, and P04 child must bind exactly | Reviewed smoke target |
| One attempt and one child | Master P05 gate | Answers whether an applicable specialist route can advance an exact branch | A sibling or parent is updated, or retries hide instability | Test asserts parent remains blocked and only the child is proved | Hard boundary |
| 30-second tool timeout | P05 subplan | Bounded capability discriminator | Cold Sage startup exceeds the budget | Classify as timeout/under-budgeted, not mathematics | Smoke hypothesis |
| 1 MiB aggregate output and 10 MiB artifacts | P05 subplan | Ample for one sentinel result while bounding failure output | Startup logs or artifacts exceed limits | Adapter returns truncation/error and cannot promote | Smoke hypothesis |
| CPU-only and no network | Academic run policy and P05 subplan | Neither GPU nor network is relevant to exact local polynomial algebra | Sage tries an undeclared external route | `CUDA_VISIBLE_DEVICES=-1` plus a fresh unprivileged network namespace | Hard execution boundary |

No seed applies. No data version applies. No hyperparameter, stochastic, or
performance default is being evaluated.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering/capability question | Can the current MathDevMCP Sage adapter execute one supported exact polynomial obligation and advance only the exact bound P04 child with independently verified on-disk evidence? |
| Exact comparator | P04 branch-local state-machine pass plus P05 fake-runner conformance, which cannot establish live specialist capability. |
| Primary pass criterion | The one selected test exits zero after `/usr/bin/sage` actually evaluates the generated polynomial script; adapter status is `certified`; `live_tool_executed=true`; the manifest independently verifies; only the exact child transitions to `proved`; the parent stays `formalization_blocked`; publication stays disabled. |
| Veto diagnostics | Test skip; wrong selected-node count; path/version drift; timeout; nonzero exit; proxy import; malformed/truncated output; missing or invalid manifest; target/input-side/domain mismatch; fake provenance; parent/sibling transition; artifact/output overflow; publication enabled; outer timeout. Any veto means no Phase 05 pass. |
| Explanatory only | Sage version preflight, executable existence/digest, pytest count, wall time, script byte count, and stdout/stderr byte counts. |
| Will not be concluded | No general Sage soundness, non-polynomial or multivariate support, real-document repair capability, expectation theorem, search completeness, default-backend decision, publication readiness, release readiness, or mission completion. |
| Preserved result artifact | Fresh run directory below `/tmp/mathdevmcp-p05-sage-smoke-20260713T105448Z`, followed by a Phase 05 result note. |

## External-Tool-First Ledger

| Tool | Candidate role | Decision |
| --- | --- | --- |
| SageMath 9.5 | Exact polynomial equality over `QQ` | Selected for this one trusted action. |
| SymPy | Offline typed scalar adapter baseline | Not selected because the master gate requires one non-SymPy specialist. |
| Lean | Exact theorem certification | Not selected. Exact binding is implemented offline, but Sage is the pre-registered first rung. |
| jixia | Static Lean evidence | Not selected; diagnostic only. |
| LeanSearch-v2 / LeanExplore | Premise retrieval | Not selected; no Lean goal or network route is needed. |
| Pantograph / LeanDojo | Proof-state interaction | Not selected; no proof-state route is needed. |
| New in-house search | None | Forbidden for this smoke; the existing external Sage executable answers the scoped question. |

## Preflight Evidence

All preflight actions were read-only. `/usr/bin/sage --version` launched the
Sage wrapper only to report its version; it did not evaluate the candidate
polynomial and is not recorded as a specialist attempt.

| Check | Result |
| --- | --- |
| Sage path | `/usr/bin/sage`, regular executable, mode 755 |
| Sage version | `SageMath version 9.5, Release Date: 2022-01-30` |
| Sage wrapper SHA-256 | `f306bccc2981095158ba2067022ce7f0538315a67980a84e807e471efe641401` |
| Python | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, CPython 3.11.15 |
| Network isolation | `/usr/bin/unshare` 2.37.2; an unprivileged user/network-namespace `true` probe exited zero |
| Outer timeout | `/usr/bin/timeout` from GNU coreutils 8.32 |
| Artifact root | `/tmp/mathdevmcp-p05-sage-smoke-20260713T105448Z`; confirmed absent before launch |
| Selected target | `(x + 1)**2 = x**2 + 2*x + 1` over `QQ[x]` |
| Generated native input | 1,967 bytes; SHA-256 `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` |
| Smoke collection | Exactly `tests/test_external_adapter_real_smoke.py::test_sage_exact_polynomial_branch_live_smoke` |

## Current Code Identity

Git commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9`.

The worktree is intentionally dirty. The exact relevant bytes to be run are:

| File | SHA-256 |
| --- | --- |
| `src/mathdevmcp/external_adapter_contract.py` | `a8ee620f2d0ade8df33e7393bc84f4275bd8a87f2e678870797130a4a1807125` |
| `src/mathdevmcp/sage_adapter.py` | `29e70e81b0b24116b63d2157258e0b21283fade217cf96ec3f0170a1698babfb` |
| `src/mathdevmcp/derivation_search_orchestrator.py` | `3e8e87702903c8fe9a73d8c171945908cda405f1179cba3a524823c841668a83` |
| `tests/test_external_adapter_real_smoke.py` | `1c9b3c5a03aeb9d4988037c2e4f5a1b874157acaca8d70fa10fd480b529cdebf` |
| `tests/test_sage_adapter.py` | `89b799a647ea1cd0aeea4521f306347d2af60430e61e5162637ee31ac1b3824d` |
| `pyproject.toml` | `d6ddae475f8f65583b161fd41a7e29c171316b2d17eda06d807128c4356c8052` |

If any listed digest changes before launch, this candidate is stale and the
focused checks plus candidate review must be refreshed.

## Offline Verification

Environment: `CUDA_VISIBLE_DEVICES=-1`, `PYTHONPATH=src`, and pytest plugin
autoload disabled.

| Check | Result |
| --- | --- |
| Focused Sage and SymPy adapters | 69 passed in 2.23 s |
| Required P05 adapter/orchestrator ladder | 166 passed in 2.40 s |
| Canonical P05 offline suite including P04 tree and promotion integration | 173 passed in 2.76 s |
| Adjacent tree, promotion, route, external policy, publication, and document regressions | 49 collected nodes passed; command exit zero |
| Post-candidate Sage/conformance/orchestrator focus | 85 passed in 0.30 s after adding the fresh-artifact-root assertion |
| Live-smoke collection | Exactly one test collected; no test body executed |
| Compilation | `py_compile` passed for the seven P05 implementation modules |
| Diff hygiene | `git diff --check` passed |

Fake runners were used for all Sage adapter test bodies above. These results
are engineering evidence only and cannot satisfy the specialist gate.

## Exact Authorized Command

The command has two timeout layers: the adapter enforces 30 seconds for Sage,
the P04 budget enforces 45 seconds overall, and `/usr/bin/timeout` bounds the
complete pytest process at 60 seconds. The user/network namespace has no host
network interfaces. The exact test node prevents selector drift.

```bash
env CUDA_VISIBLE_DEVICES=-1 \
  MATHDEVMCP_ENABLE_EXTERNAL_SMOKE=1 \
  MATHDEVMCP_SAGE_PATH=/usr/bin/sage \
  MATHDEVMCP_P05_ARTIFACT_ROOT=/tmp/mathdevmcp-p05-sage-smoke-20260713T105448Z \
  PYTHONPATH=src \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /usr/bin/timeout --signal=TERM --kill-after=5s 60s \
  /usr/bin/unshare --user --map-root-user --net --fork --kill-child=KILL \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -vv -rs \
  --maxfail=1 -p no:cacheprovider -p no:logging \
  tests/test_external_adapter_real_smoke.py::test_sage_exact_polynomial_branch_live_smoke \
  -m requires_external_tool
```

No fallback route is authorized by this command. In particular, a Sage
timeout, execution error, malformed result, or mathematical failure does not
authorize a Lean or second Sage attempt.

## Expected Artifact Contract

Exactly one `sage-run-*` directory must be created beneath the fresh root. It
must contain only:

- `input.sage`;
- `stdout.bin`;
- `stderr.bin`;
- `result.json`;
- `manifest.json`;
- empty bounded `home/` and `dot-sage/` directories.

The verified manifest must bind the exact request, executable, version,
command, environment allowlist, input digest, output digests, resource limits,
result payload, exact input lhs/rhs, and publication-disabled non-claims.

## Stop And Classification Rules

- Exit zero plus the verified postconditions permits writing the Phase 05
  result and requesting one independent claim-boundary review.
- Exit 124/137 is an outer engineering timeout, not a mathematical result.
- Pytest skip is `BLOCKED_UNAVAILABLE`, not a pass.
- Adapter `unavailable`, `timeout`, `execution_error`, `malformed_output`, or
  `truncated_output` is a capability blocker, not refutation.
- Adapter `refuted` would refute only the exact scoped polynomial target if its
  concrete witness and manifest verify; it would still fail this positive
  capability candidate and authorize no fallback.
- Any manifest, target-binding, branch-isolation, budget, or publication veto
  stops Phase 05 closure.
- Do not open Phase 06 until the live evidence passes and one substantive
  independent review agrees that the capability and non-claim boundaries are
  correctly stated.

## Post-Run Requirements

After an authorized zero-exit smoke:

1. independently call the Sage manifest verifier on the produced manifest;
2. inspect the closed artifact inventory and record byte counts/digests;
3. write the Phase 05 result with separate engineering, mathematical-validity,
   and interpretation ledgers plus a decision table and post-run red team;
4. obtain one substantive read-only independent review of the live evidence
   and claim boundary;
5. repair any material review finding with focused verification;
6. open Phase 06 only if the live gate and review both pass.

## Authorization Boundary

Approval authorizes only the exact command above and read-only verification of
its new `/tmp` artifact bundle. It does not authorize Lean, jixia, model/API,
network, GPU, installation, environment mutation, source-document editing,
publication, commit, push, release, or Phase 06 execution.
