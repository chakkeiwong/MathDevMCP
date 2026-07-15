# Claude Read-Only Review Bundle

Date: 2026-07-13
Review name: `mathdevmcp-p05-result-review`
Supervisor/executor: Codex
Reviewer: Claude Opus read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, invoke Sage
or another backend, or approve boundary crossings. Read only the bounded paths
below. Codex remains supervisor and executor.

## Objective

Decide whether the Phase 05 result may be closed as a narrow engineering and
live-specialist capability pass, while preserving the explicit non-claims. The
review is not being asked to authorize Phase 06 execution, publication,
release, or a general mathematical/scientific claim.

## Artifacts To Inspect

- `docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md`
- `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-01-result-2026-07-13.md`
- `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-smoke-attempt-02-result-2026-07-13.md`
- `docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-pre-smoke-candidate-r3-2026-07-13.md`
- `src/mathdevmcp/sage_adapter.py`
- `src/mathdevmcp/external_adapter_contract.py`
- `tests/test_sage_adapter.py`
- `tests/test_external_adapter_real_smoke.py`
- `/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json`

Do not inspect the whole repository. The master gate being reviewed is simply:
at least one applicable non-SymPy specialist tool must genuinely run, carry an
exact branch-local manifest, and advance only its bound test child.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the successful R3 evidence honestly establish one exact Sage route and exact child transition, with no material integrity or claim-boundary defect? |
| Baseline/comparator | P04 injected orchestration and P05 fake-runner tests, plus failed attempts R1/R2 that exposed artifact-layout and runtime-scratch contract defects. |
| Primary criterion | Exact Sage 9.5 process, target/domain/native input, verified manifest v3, bounded scratch, exact child `proved`, parent still blocked, publication disabled. |
| Veto diagnostics | Fake or missing process provenance; invalid scratch/evidence accounting; target/domain/branch mismatch; manifest verifier trusts mutable summary fields; failed attempts misrepresented as mathematics; result overclaims real-document/general capability; publication or next-phase authority leak. |
| Explanatory diagnostics | Test counts, repair count, wall time, and scratch topology. |
| Not concluded | General Sage/CAS soundness, broad algebra support, real-document repair capability, expectation theorem, backend default, publication/release readiness, Phase 06 result, or mission completion. |

## Key Evidence Summary

- Exact marked smoke: one node selected, `1 passed in 1.83s`, zero skips.
- Sage execution: exit 0, no timeout/truncation, 1.786090688 seconds.
- Exact target: `(x + 1)**2 = x**2 + 2*x + 1` over `QQ[x]`.
- Result: `certified`, exact difference `0`, no witness.
- Manifest v3 SHA-256:
  `7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2`.
- Independent local verifier returned `integrity_state=verified` and the same
  request, result, evidence digests, command, environment, and scratch tree.
- Scratch: exactly 11 inventoried entries and 55 file bytes below only
  `home`, `dot-sage`, and `tmp`; symlink/hardlink/special/overflow/mutation
  adversarial tests pass.
- Offline canonical suite: 187 passed after v3.
- Publication remains false; the synthetic parent remains blocked.

## Review Questions

1. Is there any material correctness defect in the v3 manifest or scratch
   contract that invalidates the narrow capability result?
2. Does the live-smoke test actually require exact live process evidence and
   exact P04 child isolation, or can a fake/stale/mismatched result pass?
3. Are attempts 01 and 02 classified honestly as engineering failures rather
   than hidden mathematical evidence?
4. Does the result make any unsupported claim or transfer authority to Phase
   06, publication, release, or general mathematics?
5. If no material blocker remains, is
   `PASS_ENGINEERING_SPECIALIST_CAPABILITY` an accurate final Phase 05 status?

## Required Output

Return findings ordered by severity with exact file/field references. Treat
style-only comments as non-blocking. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
