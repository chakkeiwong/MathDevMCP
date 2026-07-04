# Phase 5 Result: Derive Or Refute

## Status

`PASSED_LOCAL_CHECKS_CLAUDE_REVIEW_UNAVAILABLE`

## Phase Objective

Implement a high-level `derive_or_refute` workflow that accepts a target
equality, givens, and assumptions, then returns a bounded derivation,
refutation, missing-assumption, not-encodable, unavailable-backend, or unknown
result.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the repo answer "can I derive X from Y?" in a bounded, evidence-backed way? |
| Baseline/comparator | Existing `derive_step`, `check_proof_obligation`, router, counterexample search, and assumption discovery. |
| Primary criterion | Met locally. Results include route evidence, assumptions, optional counterexamples, workbench records, CLI exposure, and experimental MCP exposure. |
| Veto diagnostics | Passed locally. No unchecked multi-step proof is synthesized; unknown remains unknown; missing assumptions are visible. |
| Explanatory diagnostics | Focused workflow, CLI, MCP facade, and MCP sync tests. |
| Not concluded | Complete derivability over arbitrary givens or broad proof search. |

## Artifacts

- `src/mathdevmcp/derive_or_refute.py`
- `tests/test_derive_or_refute.py`
- CLI command: `derive-or-refute`
- MCP tool: `derive_or_refute`
- Updated `mcp/README.md`

## Commands Run

```bash
PYTHONPATH=src python -m pytest -q tests/test_derive_or_refute.py tests/test_counterexample_search.py tests/test_assumption_discovery.py tests/test_math_debugging_router.py
PYTHONPATH=src python -m pytest -q tests/test_mcp_facade.py tests/test_mcp_surface_sync.py
python3 -m py_compile src/mathdevmcp/derive_or_refute.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
git diff --check
```

## Check Results

- Workflow stack tests: `23 passed`.
- MCP facade/surface sync tests: `26 passed`.
- Python compile check: passed.
- `git diff --check`: passed.

## Claude Review

Phase 5 read-only review was attempted once with a verdict-only prompt. It
produced no substantive output before interruption and returned a generic
execution error after interrupt.

## Phase 6 Handoff

Proceed to Phase 6: Prove Or Refute.

Handoff conditions met:

- `derive_or_refute` can be reused by prove/refute.
- Router, counterexample, and assumption diagnostics are integrated.
- CLI/MCP exposure is synchronized.

## Non-Claims

- This phase does not implement arbitrary multi-step derivation.
- A `proved` status is only for the scoped target obligation and only through
  nested backend evidence.
- Unknown is not false.
