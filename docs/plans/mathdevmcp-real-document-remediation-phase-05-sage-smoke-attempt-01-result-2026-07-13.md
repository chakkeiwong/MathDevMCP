# Phase 05 Sage Smoke Attempt 01 Result

Date: 2026-07-13

Status: `FAIL_ENGINEERING_ARTIFACT_LAYOUT`

Candidate:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-sage-pre-smoke-candidate-2026-07-13.md`

## Decision

The first trusted Sage smoke does not pass Phase 05. Sage was launched once and
returned quickly, but the adapter rejected the run before sealing stdout,
structured result, or a manifest. The P04 child therefore transitioned to
`failed`, and pytest correctly failed with `1 failed in 1.86s`.

This is an engineering integration failure, not mathematical refutation and
not capability evidence. Phase 05 remains open. No fallback tool or second live
attempt was run under the first authorization.

## Exact Failure

The v1 adapter wrote `input.sage` and invoked:

```text
/usr/bin/sage --nodotsage <run-root>/input.sage
```

SageMath 9.5 normally preparses a `.sage` file into an adjacent
`input.sage.py`. The v1 closed artifact inventory allowed only `input.sage`
before sealing, so `_validate_run_root_layout` rejected the normal pre-parser
file. The adapter classified the result as `execution_error`, retained process
provenance, set `manifest_verified=false`, and could not promote the child.

The outer test observed the safe terminal consequence:

```text
assert final_child["state"] == "proved"
AssertionError: assert 'failed' == 'proved'
```

## Artifact Inventory

Artifact root:
`/tmp/mathdevmcp-p05-sage-smoke-20260713T105448Z`

| Artifact | Bytes | SHA-256 | Interpretation |
| --- | ---: | --- | --- |
| `sage-run-exh_dx07/input.sage` | 1,967 | `9a8cf55a5b8f8e78be72257e2ad5c14caf45ec0556d78fd79463dd1614f6297a` | Exact generated v1 native input |
| `sage-run-exh_dx07/input.sage.py` | 2,416 | `068076a1bf2871b864f34b5f5983819771e46e7bac10ffc6de6a300565ab98c8` | Normal but unbound Sage pre-parser output |

No `stdout.bin`, `stderr.bin`, `result.json`, or `manifest.json` was sealed.
The two bounded environment directories were empty. The failed root is retained
and must not be reused by a later attempt.

## Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Fail for v1 live integration: normal Sage pre-parser behavior violated the registered artifact inventory. Fail-closed classification worked. |
| Mathematical validity | No admissible result. The absence of a sealed payload and manifest forbids interpreting the polynomial identity. |
| Scientific interpretation | No evidence for or against general Sage capability or real-document repair. The run exposed a wrapper-contract mismatch only. |

## Repair

The adapter was changed prospectively to v2:

- generated source remains ordinary, validated Python syntax importing
  `sage.all`;
- the bound native input is now `input.py` with media type `text/x-python`;
- the exact executable route is `/usr/bin/sage --python input.py`;
- Sage's `.sage` pre-parser is no longer in the execution path;
- `HOME`, `DOT_SAGE`, and `TMPDIR` are bound inside the run root;
- bytecode writes are disabled;
- adapter and manifest schemas were bumped to
  `p05-sage-adapter@2` and `p05_sage_execution_manifest@2`;
- a regression now rejects an `input.sage.py` byproduct explicitly.

Offline repair verification: 70 focused Sage/SymPy tests passed and the
canonical Phase 05 suite passed 174 tests. This is still not live capability
evidence.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Attempt 01 fails as an engineering artifact-layout mismatch. |
| Primary criterion | Fail: no verified manifest and no exact child promotion. |
| Veto diagnostic | Triggered: unexpected run-root artifact. |
| Main uncertainty | Whether the repaired `sage --python input.py` route produces the exact sealed payload and branch transition under trusted execution. |
| Next justified action | Prepare a new candidate and request a fresh narrow authorization for one repaired v2 smoke. |
| Not concluded | Mathematical refutation, Sage unavailability, general adapter fitness, real-document capability, Phase 05 pass, or mission completion. |

## Post-Run Red Team

The strongest alternative explanation is not that Sage failed algebraically,
but that MathDevMCP's v1 wrapper model was incomplete. The observed generated
file and Sage wrapper documentation directly support that explanation.

The weakest evidence is the unavailable Sage stdout: because sealing failed,
the adapter intentionally did not preserve or promote the payload. A repaired
live run is required; offline tests cannot fill that gap.
