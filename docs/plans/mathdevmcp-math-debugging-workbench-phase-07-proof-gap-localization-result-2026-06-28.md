# Phase 7 Result: Proof Gap Localization

## Status

`PASSED_LOCAL_CHECKS_CODEX_REVIEW`

## Phase Objective

Implement `localize_proof_gap`, which checks adjacent derivation steps and
reports the first unsupported, refuted, missing-assumption, not-encodable, or
backend-unavailable step.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the repo identify where a derivation stops being justified? |
| Baseline/comparator | Existing label derivation audit plus Phase 6 `prove_or_refute`. |
| Primary criterion | Met locally. The workflow stops at the first non-proved step and does not promote later steps. |
| Veto diagnostics | Passed locally. Refuted and missing/unknown steps are not summarized as whole-derivation validity. |
| Explanatory diagnostics | Step statuses, first gap record, workbench packet, and MCP sync tests. |
| Not concluded | Automatic repair of derivations or complete proof checking. |

## Artifacts

- `src/mathdevmcp/proof_gap.py`
- `tests/test_proof_gap.py`
- CLI command: `localize-proof-gap`
- MCP tool: `localize_proof_gap`
- Updated `mcp/README.md`

## Commands Run

```bash
PYTHONPATH=src python -m pytest -q tests/test_proof_gap.py tests/test_prove_or_refute.py tests/test_derive_or_refute.py
PYTHONPATH=src python -m pytest -q tests/test_mcp_facade.py tests/test_mcp_surface_sync.py
python3 -m py_compile src/mathdevmcp/proof_gap.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
git diff --check
```

## Check Results

- Gap/prove/derive tests: `19 passed`.
- MCP facade/surface sync tests: `26 passed`.
- Python compile check: passed.
- `git diff --check`: passed.

## Review

Codex reviewed the result against the Phase 7 subplan. Claude review was not
attempted for this phase because prior material phase prompts repeatedly hung
and the runbook says Claude may be used, not must be used, for material
subplans. No local boundary blocker was found.

## Phase 8 Handoff

Proceed to Phase 8: Code Implements Equation.

Handoff conditions met:

- Gap statuses can inform code/equation mismatch reports.
- First-gap behavior is tested.
- Phase 8 subplan exists.

## Non-Claims

- The workflow does not repair derivations.
- A chain is only `proved` when every checked adjacent step is proved by nested
  bounded backend evidence.
