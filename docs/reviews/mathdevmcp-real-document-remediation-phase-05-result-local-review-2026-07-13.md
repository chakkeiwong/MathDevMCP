# Phase 05 Result Local Independent Review

Date: 2026-07-13

Status: `AGREE_AFTER_FOCUSED_REPAIR`

Reviewed result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md`

Review bundle:
`docs/reviews/mathdevmcp-real-document-remediation-phase-05-result-review-bundle-2026-07-13.md`

## Reviewer Route

The planned Claude Opus read-only review was blocked before any workspace data
was transmitted because the external-data exfiltration policy rejected that
route. No Claude process was launched, no Claude verdict is claimed, and no
retry or workaround was attempted.

A fresh local Codex read-only reviewer inspected the bounded Phase 05 result,
Sage adapter and contract, Sage tests, live-smoke test, failed-attempt records,
and preserved R3 manifest. Codex remained the implementation supervisor; the
reviewer did not execute Sage, edit files, authorize publication, or authorize
Phase 06 execution.

## Review Decision

The reviewer returned `VERDICT: AGREE` with no material blocker to the narrow
status `PASS_ENGINEERING_SPECIALIST_CAPABILITY`.

The accepted claim is only that MathDevMCP genuinely executed one supported
Sage 9.5 exact-polynomial action, verified its branch-bound manifest, and
advanced only the exact synthetic child while the parent and publication state
remained blocked. Reviewer agreement is explanatory; the verified manifest and
branch transition remain the primary evidence.

## Findings And Repairs

| Severity | Finding | Repair | Focused evidence |
| --- | --- | --- | --- |
| Low | The R3 candidate retained prospective wording after the smoke completed, including a false statement that no third Sage action ran. | Converted the record to historical wording, named the one executed action, and retained that no fourth action ran. | Stale-wording scan is clear for the R3 candidate and final result. |
| Low | `verify_sage_execution_manifest()` matched payload sides to the target but did not require payload `domain` and `variable` to equal the request's typed domain assumption. | Require exactly one closed Sage domain assumption with `id`, `kind`, `symbol`, and exact `QQ` domain, then match both payload fields to it. | Sage adapter suite passes; the preserved R3 manifest still verifies. |
| Low | There were no fully re-digested payload mutation tests for domain or variable substitution. | Added two mutations that rewrite both stdout and structured result, refresh artifact/result/manifest digests, and require semantic rejection. | Both `domain=ZZ` and `variable=y` mutations fail at the request/payload binding check. |
| Low | The scratch discussion could be read as a stronger hostile-concurrency guarantee than the implementation provides. | State that scratch sealing is post-process integrity accounting for a fresh private run root, not a hostile concurrent same-user sandbox guarantee. | Candidate and final result now state the threat boundary explicitly. |

## Post-Repair Checks

Environment: CPython 3.11.15 from the `tfgpu` environment with
`CUDA_VISIBLE_DEVICES=-1`, `PYTHONPATH=src`, and pytest plugin autoload disabled.

| Check | Result |
| --- | --- |
| `tests/test_sage_adapter.py` | `54 passed in 0.39s` |
| Seven-file Phase 05 subplan suite | `182 passed in 3.09s` |
| Eight-file Phase 05 master-plan suite, including branch controller | `195 passed in 3.50s` |
| Phase 05 implementation/test compilation | Passed |
| `git diff --check` | Passed |
| Original R3 manifest verification under repaired verifier | `integrity_state=verified` |

The current eight-file count is the post-review code state. The historical
`187 passed in 2.72s` remains the correctly dated pre-review R3 result and is
not rewritten as though it occurred after these repairs.

## Preserved Live Evidence

| Field | Verified value |
| --- | --- |
| Manifest | `/tmp/mathdevmcp-p05-sage-smoke-r3-20260713T115057Z/sage-run-9s970jdv/manifest.json` |
| Manifest SHA-256 | `7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2` |
| Request digest | `57f2ffcce6ba84a151f70483764062e462d03a7979e493208fc2f8762014dacd` |
| Payload binding | `domain=QQ`, `variable=x` |
| Scratch inventory | 11 entries |
| Verification | `integrity_state=verified` |

Sage was not rerun during review repair. The original native input, result,
manifest bytes, mathematical target, and process evidence remain unchanged.

## Boundary

This review does not establish general Sage or CAS soundness, arbitrary
polynomial support, real-document repair capability, scientific usefulness,
expectation replacement, proof-search completeness, publication or release
readiness, Phase 06 correctness, or mission completion. It does not authorize
source edits, publication, default changes, or Phase 06 execution.

VERDICT: AGREE
