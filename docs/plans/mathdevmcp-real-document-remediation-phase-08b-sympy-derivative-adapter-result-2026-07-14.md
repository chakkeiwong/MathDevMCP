# MathDevMCP Phase 08B SymPy Derivative Adapter Result

Date: 2026-07-14

Status: `PASS_P08B_BACKEND_CHECKED_COMPUTATIONAL_SUPPORT`

## Outcome

The fresh post-repair run independently verified `backend_checked` for the
pre-registered `eq:cashflow-rate-derivative` candidate. SymPy 1.14.0
constructed the derivative of

```text
bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))
```

with respect to `rt`, holding `bp`, `r`, and `tau` constant. A separately
parsed source target compared with the constructed expression at exact
difference `0` under real scalars, `1 + r != 0`, `1 + rt != 0`, and the
registered differentiability assumption on that nonsingular domain.

This is computational support for one scoped source claim. It is not formal
proof, general CAS soundness, whole-document correctness, an applicable source
repair, publication evidence, or P04/P05 promotion authority.

## Run Manifest

| Field | Value |
| --- | --- |
| Run root | `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0` |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` |
| Code identity | `4ff3eb7d75707ee355ea093830e6b829736284b16b807ea6a0e82a18231e878c` |
| Run binding | `14a49479769439925a6e3f9ad293b1b0fcea5a61f81ec454fbaea5ea80da8fb0` |
| Interpreter | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3` (CPython 3.11.15) |
| Environment | `CUDA_VISIBLE_DEVICES=-1`; CPU-only by design |
| Data/source version | Frozen source manifest and obligation digests in the run root |
| Seeds | N/A; deterministic exact CAS route |
| Worker wall time | 1,876 ms |
| Plan | `docs/plans/mathdevmcp-real-document-remediation-phase-08b-sympy-derivative-adapter-repair-subplan-2026-07-14.md` |
| Result | This file |

The worktree was intentionally dirty and is fully enumerated in
`run-manifest.json`; exact execution and verification code bytes are preserved
under `code-snapshot/`.

## Actual Commands

All commands used `CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src` and the pinned
interpreter.

```text
scripts/run_p08_frozen_validation.py freeze-extract --artifact-root .local/mathdevmcp/evidence/p08-20260714 --new-run
scripts/run_p08_frozen_validation.py resolve-context --run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0
scripts/run_p08_frozen_validation.py verify-p08a --run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0
scripts/run_p08_frozen_validation.py capability-preflight --run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0
scripts/run_p08_frozen_validation.py capability-run --run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0 --candidate eq:cashflow-rate-derivative --timeout-seconds 10 --max-output-bytes 262144 --max-artifact-bytes 1048576
scripts/run_p08_frozen_validation.py verify-capability --run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0
```

## Evidence

| Artifact | Identity/result |
| --- | --- |
| P08A decision | `PASS_P08A_FROZEN_EXTRACTION_CONTEXT`; decision digest `9ca9db79c1911dc4e72bca2fd13a13aebea4eb5c23994d0b6607c5137f88bf3f` |
| Capability preflight | `READY_EXACT_REGISTERED_ROUTE`; zero backend requests; digest `4094d30b2c3e41a36cf6da2aa76c70ba93a01002076864cd121c9978476c4786` |
| Native request | 1,639 bytes; SHA-256 `3c7074050095fae7d1bb688cad20e6e63a932d25fb1006937a49bbca3190139d` |
| Raw stdout | 3,443 bytes; SHA-256 `73db1b363bdefdf14fc74eb3a81a988070d9a7a12b55e4bdd5d2fde249817d68` |
| Raw stderr | 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Structured result | 6,930 bytes; result digest `1dfaace0ef1b244f0b2ce4b2b1d00e822a281bb8d70ce6783e4ed4979b6641e6` |
| Bundle manifest | 966 bytes; SHA-256 `14a316ce594771b1e5d8a265ca0ba0d97fc5d03a75a4d273432aa70ef4713412` |
| Verified aggregate | 12,978 counted bytes plus 16,384 fixed overhead = 29,362 of 1,048,576 bytes |
| Capability decision | `backend_checked`; digest `8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c` |

The exact worker command used isolated/no-site/source-only startup with
`-I -S -B -X pycache_prefix=/dev/null`. The worker and parent independently
bound the reviewed SymPy and mpmath trees and observed only those two loaded
site-packages roots.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept scoped computational support | Met: backend construction followed by independent exact-zero comparison | Passed: source, request, assumptions, code, tool trees, raw bytes, command, bundle, and aggregate reconstruct; no vetoes | A CAS result is not a proof and does not establish neighboring claims or omitted assumptions | Launch P08C frozen agent-facing workflow comparison without rerunning the backend | Proof, whole-document correctness, best repair, publication/default/release readiness |

## Separate Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Fresh P08A reconstruction, exact preflight, bounded worker, five-file bundle, and independent verifier passed under one code identity. |
| Mathematical validity | `backend_checked` computational support for exactly the registered derivative under explicit assumptions; `formal_proof_certified: false`. |
| Scientific interpretation | The direct external-tool route can validate one nontrivial frozen real-document calculus subclaim. No broader capability is inferred. |

## Negative/Failure Accounting

No formal-run engineering, tuning, or diagnostic failure occurred. Earlier
implementation diagnostics exposed provenance defects involving shadow imports,
valid bytecode caches, and unbound mpmath. Those were implementation failures,
not evidence against the mathematical idea, and were repaired before this run.

## Post-Run Red Team

The strongest alternative explanation is that SymPy and the source target
share an unnoticed semantic convention that is inappropriate for the broader
economic model. The run narrows that risk by binding the exact partial
derivative, held constants, real domain, and denominator assumptions, but it
does not settle whether `rt` should be treated as an independent argument in
every downstream use. A formal derivation or a source-level modeling dispute
could overturn broader interpretation without contradicting this scoped CAS
check. The weakest evidence is therefore applicability beyond the exact
source-local partial derivative, not the recorded exact algebra.

## Handoff

P08C may proceed automatically because P08B ended in independently verified
`backend_checked` with no unresolved engineering veto. P08C must consume this
decision read-only, must not rerun the capability backend, and must keep all
publication, source-edit, promotion, proof, default, and release boundaries
disabled.
