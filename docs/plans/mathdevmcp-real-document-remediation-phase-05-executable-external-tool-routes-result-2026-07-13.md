# Phase 05 Executable External-Tool Routes Result

Date: 2026-07-13

Status: `PASS_ENGINEERING_SPECIALIST_CAPABILITY`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Phase subplan:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-subplan-2026-07-13.md`

Successful candidate:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-pre-smoke-candidate-r3-2026-07-13.md`

## Decision

Phase 05 satisfies its engineering and live-specialist capability criterion.
MathDevMCP executed one exact non-SymPy specialist action through
`/usr/bin/sage`, independently verified its adapter-v3 manifest, and advanced
only the exact bound synthetic P04 child from `ready` to `proved`. The synthetic
parent remained `formalization_blocked`, publication remained disabled, and a
fresh local read-only reviewer agreed with the scoped result after identifying
four low-severity repairs that were applied and rechecked.

The successful action certified only the exact polynomial equality

```text
(x + 1)**2 = x**2 + 2*x + 1
```

over `QQ[x]`. It does not establish real-document repair capability, general
Sage soundness, expectation replacement, search completeness, publication
readiness, Phase 06 results, or mission completion.

No Lean, jixia, retrieval/model, external-network access, GPU, installation,
environment mutation, source-document edit, publication, commit, or push
action ran. The outer command created an isolated network namespace as stated
in the run manifest.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Engineering/capability question | Pass: the current adapter can execute and seal one supported exact Sage computation and bind it to the exact P04 branch request. |
| Comparator | P04 injected orchestration plus P05 fake-runner conformance; neither could establish live specialist capability. Attempts 01 and 02 exposed and safely classified wrapper/runtime-contract defects. |
| Primary criterion | Pass: exactly one marked node ran with no skip; Sage exited zero; adapter status was `certified`; live process and manifest evidence verified; only the exact child became `proved`; parent stayed blocked; publication stayed disabled. |
| Veto diagnostics | Pass on R3: no timeout, truncation, malformed output, version/path drift, target/domain mismatch, root-layout violation, unsafe scratch, manifest mismatch, wrong branch transition, skip, or publication leak. Attempts 01 and 02 remain failed vetoed diagnostics and are not counted as passes. |
| Explanatory only | Test counts, executable/version preflight, wall time, scratch count, byte counts, and the two repair iterations. |
| Not concluded | No general CAS/Sage soundness, broader expression support, proof of arbitrary document mathematics, real-document repair capability, expectation theorem, default backend, publication, release, or mission completion. |
| Preserved artifact | `/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json`, SHA-256 `7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2`. |

## Live Result

| Field | Value |
| --- | --- |
| Manifest schema | `p05_sage_execution_manifest@3` |
| Adapter | `p05-sage-adapter@3` |
| Request digest | `57f2ffcce6ba84a151f70483764062e462d03a7979e493208fc2f8762014dacd` |
| Branch id | `branch_350c0cfc891deb8140fbc75529f953a356a55de620f8c10d73f22f04596e598e` |
| Parent id | `branch_85552c491e92c2fe50e543972a2b8ec1d3c7ed38237211fc02d686f59ea53c88` |
| Obligation digest | `5555555555555555555555555555555555555555555555555555555555555555` |
| Target/domain | `(x + 1)**2 = x**2 + 2*x + 1` over exact `QQ[x]` |
| Native input | `input.py`, 1,967 bytes, SHA-256 `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` |
| Exact command | `/usr/bin/sage --python <run-root>/input.py` |
| Sage version | 9.5 |
| Process result | Exit 0; no timeout; no truncation; 1,786,090,688 ns |
| Mathematical payload | `status=certified`, `difference=0`, independently constructed lhs/rhs both `x^2 + 2*x + 1`, no witness |
| Stdout | 336 bytes; SHA-256 `ec40186ecac126291d55ba1c283a5a87e706dec96d0d757f880b8066059f3d57` |
| Stderr | 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Structured result | 308 bytes; SHA-256 `e2095973ee92a8aa4f0e1abd3c167d9b7ee5d3c7d42dbc82ea2b8395b03eea13` |
| Scratch | 11 recursively verified entries; 55 regular-file bytes; exact roots `home`, `dot-sage`, `tmp` |
| Manifest | 4,566 bytes; SHA-256 `7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2` |
| Publication | `false` |

Independent post-run invocation of
`verify_sage_execution_manifest(...)` returned `integrity_state=verified` and
reconstructed the same request, command, environment, payload, evidence-file
digests, and scratch inventory.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9`; intentionally dirty worktree, with candidate-bound source digests |
| Python/environment | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, CPython 3.11.15, pytest 9.0.2 |
| Exact outer command | The command registered in candidate R3: one explicit pytest node under `/usr/bin/timeout` and `/usr/bin/unshare --user --map-root-user --net` |
| CPU/GPU | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; no GPU action |
| Network | Fresh unprivileged network namespace; no host network route |
| Data version | N/A: deterministic synthetic polynomial target; frozen documents were not read by the live smoke |
| Random seeds | N/A: exact deterministic algebra and deterministic branch fixture |
| Tool wall time | 1.786090688 s |
| Pytest wall time | 1.83 s; `1 passed`, zero skips |
| Output artifact | `/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json` |
| Plan | `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-pre-smoke-candidate-r3-2026-07-13.md` |
| Result | `docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md` |

## Implementation Result

### Closed adapter contract

- External results have closed statuses and exact request, branch, assumption,
  native-input, tool, limit, execution, evidence, and non-claim bindings.
- Fake runners remain synthetic engineering evidence and cannot set live
  capability or promote a real branch.
- Live P04 promotion independently re-verifies the on-disk specialist
  manifest rather than trusting cached adapter fields.

### SymPy

- The typed scalar adapter supports only reviewed domains and assumptions.
- Unsupported expression-level assumptions fail closed.
- Nonzero/domain requirements remain explicit; scalar CAS success does not
  promote measure-theoretic or document-level conclusions.

### Sage

- User text is parsed into a bounded polynomial AST and emitted as ordinary
  deterministic Python; no `eval` or Sage parser evaluates user text.
- The exact route is Sage's configured Python via `sage --python input.py`.
- Manifest v3 closes the evidence-file inventory and recursively seals bounded
  runtime scratch without hardcoding version-specific cache filenames.
- Scratch sealing is post-process integrity accounting for a fresh private run
  root. It is not a hostile concurrent same-user sandbox guarantee.
- Target, input sides, `QQ` domain, variable, version, command, environment,
  stdout/stderr, structured result, and process state are cross-checked.

### Lean and diagnostics

- Direct Lean results require exact target/statement, assumptions, imports,
  source, project, toolchain, and executable binding before certification.
- Source-only or injected `verified` results remain diagnostic.
- Lean rejection is not mathematical refutation.
- jixia, retrieval, and proof-state routes remain diagnostic/unavailable unless
  separately configured; none ran in Phase 05.

### Finite-support expectation bridge

- The bridge records finite support, normalized weights, conditioning,
  integrability/measurability, and law/choice dependence as explicit proof
  obligations.
- A finite-sum CAS result cannot certify expectation replacement or
  differentiation under expectation.

## Failed Attempts Retained

Attempt 01 used a `.sage` input and correctly rejected Sage's unbound generated
`input.sage.py`; it is classified `FAIL_ENGINEERING_ARTIFACT_LAYOUT`.

Attempt 02 used the correct `sage --python input.py` route but incorrectly
required normal bounded `DOT_SAGE` scratch to remain empty; it is classified
`FAIL_ENGINEERING_RUNTIME_SCRATCH_CONTRACT`.

Neither attempt produced a verified manifest or a mathematical result. They
are negative engineering diagnostics that motivated v3, not hidden retries or
evidence against the polynomial target.

## Verification

Environment for offline checks: `CUDA_VISIBLE_DEVICES=-1`, `PYTHONPATH=src`,
pytest plugin autoload disabled.

| Check | Result |
| --- | --- |
| Final canonical Phase 05 offline suite | 187 passed in 2.72 s |
| V3 Sage adapter focused suite | 52 passed in 0.36 s before final integrated run; all nodes are included in the final 187 |
| Post-review Sage adapter suite | 54 passed in 0.39 s, including fully re-digested domain and variable mismatch mutations |
| Post-review master Phase 05 suite | 195 passed in 3.50 s across the eight master-plan files, including branch-controller integration |
| R2 scratch replay under v3 | Exact untouched failed root accepted as one input plus 11 bounded scratch entries and 55 scratch bytes |
| Adjacent publication/document regressions | 32 passed in 386.06 s; Phase 05 live smoke separately asserts publication disabled and parent/child isolation |
| Live specialist smoke | Exactly one selected node, `1 passed in 1.83s`, zero skips |
| Independent manifest verification | Pass: `integrity_state=verified` and exact digest match |
| Compilation | Passed for Phase 05 implementation and smoke modules |
| Diff hygiene | `git diff --check` passed |

The 187-test row is the historical pre-review R3 run; the 195-test row is the
current post-review master scope. Test counts are explanatory. The live process,
exact branch transition, and verified v3 manifest are the primary evidence.

## External-Tool Ledger

| Tool | Phase 05 result | Boundary |
| --- | --- | --- |
| SymPy | Typed offline scalar adapter implemented and tested | Does not satisfy the required non-SymPy live gate; no measure/document claim |
| SageMath 9.5 | One exact supported `QQ[x]` action executed and verified | Only this exact scoped polynomial result and capability route |
| Lean | Exact-binding repairs implemented and tested offline | No live Lean action or certificate in this phase |
| jixia | Diagnostic contract retained | No execution; cannot promote |
| LeanSearch-v2 / LeanExplore | Considered for premise retrieval | No formal Lean goal/network route; not run; cannot certify |
| Pantograph / LeanDojo | Considered for proof-state interaction | No selected environment/goal; not run; cannot certify |
| New in-house mathematical search | None | Not introduced; external-tool-first policy preserved |

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Pass Phase 05 engineering/live-specialist capability after substantive independent review and focused repair. |
| Primary criterion | Pass: a non-SymPy specialist actually ran, produced a verified branch-local manifest, and advanced only the exact applicable child. |
| Veto status | R3 clear; R1/R2 remain separately failed engineering vetoes and do not contaminate the successful artifact. |
| Engineering ledger | Adapter contracts, execution classification, resource bounds, scratch/evidence sealing, independent verification, and P04 integration pass. |
| Mathematical-validity ledger | One exact Sage certificate for the named polynomial equality over `QQ[x]`; no other mathematical claim. |
| Interpretation ledger | MathDevMCP now has demonstrated breadth beyond SymPy for one supported action. This is not evidence of real-document repair utility. |
| Main uncertainty | The reviewed scope is intentionally narrow; additional Sage expressions, Lean, diagnostics, and frozen-document targets remain untested live. |
| Next justified action | Close P05 and draft/skeptically audit P06; do not execute P06 under this result. |
| Not concluded | General proof ability, scientific repair quality, ranking/default policy, publication, release, Phase 06 pass, or whole-program completion. |

## Post-Run Red Team

The strongest alternative explanation is fixture fit: adapter v3 is correct
for one exact univariate `QQ` polynomial and the Sage 9.5 runtime topology, but
may encounter different bounded scratch or semantic issues on other supported
expressions or versions. The result therefore demonstrates one scoped route,
not a generally robust Sage integration.

The conclusion would be overturned by any digest-preserving way to substitute
the target, input sides, domain, executable, command, payload, branch, or
scratch; by failure of independent manifest reconstruction; or by evidence
that the parent/sibling advanced. Current mutation tests and the live smoke
reject or directly assert each of those conditions.

The weakest evidence is downstream scientific usefulness: the target is a
synthetic algebra identity, deliberately chosen to test integration breadth.
Frozen real-document capability belongs to Phase 08, after Phase 06 ranking
and Phase 07 product contracts, and remains a non-claim here.

## Independent Review

The planned Claude Opus review was blocked before transmission by the external-
data exfiltration policy. No Claude verdict is claimed, and no retry or
workaround was attempted. A fresh local Codex read-only reviewer inspected the
bounded result, implementation, tests, and live manifest and returned
`VERDICT: AGREE` with no material blocker.

The reviewer identified four low-severity repairs: remove stale prospective R3
wording; bind payload domain and variable to the request's typed domain
assumption; add domain/variable mutation tests; and state the scratch threat
model precisely. All four were applied. Focused and canonical checks and
read-only verification of the original R3 manifest were then rerun; Sage was
not rerun.

Review record:
`docs/reviews/mathdevmcp-real-document-remediation-phase-05-result-local-review-2026-07-13.md`.

## Handoff

Phase 05 is closed. Phase 06 may now be drafted and skeptically audited under
the proportional academic governance reset. Publication remains disabled, and
no Phase 06 execution is authorized by this result.
