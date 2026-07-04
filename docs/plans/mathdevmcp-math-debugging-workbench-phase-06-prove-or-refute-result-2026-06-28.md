# Phase 6 Result: Prove Or Refute

## Status

`PASSED_LOCAL_CHECKS_CLAUDE_REVIEW_UNAVAILABLE`

## Phase Objective

Implement `prove_or_refute` for theorem/identity-like target equalities, routing
to bounded backend evidence, optional explicit Lean source, counterexample
search, or conservative abstention.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the repo answer "can we prove X?" with proof/refutation/unknown boundaries? |
| Baseline/comparator | Existing `check_proof_obligation`, `lean_check`, router, and counterexample search. |
| Primary criterion | Met locally. Tool returns proved/refuted/unknown/not-encodable/backend-unavailable style outcomes with evidence and CLI/MCP exposure. |
| Veto diagnostics | Passed locally. Lean without source is not encodable, not refuted; unavailable/not-encodable routes are diagnostic; counterexample fallback is bounded. |
| Explanatory diagnostics | Workflow, CLI, MCP sync, and Lean boundary tests. |
| Not concluded | Complete theorem proving or autonomous formalization. |

## Artifacts

- `src/mathdevmcp/prove_or_refute.py`
- `tests/test_prove_or_refute.py`
- CLI command: `prove-or-refute`
- MCP tool: `prove_or_refute`
- Updated `mcp/README.md`

## Commands Run

```bash
PYTHONPATH=src python -m pytest -q tests/test_prove_or_refute.py tests/test_derive_or_refute.py tests/test_counterexample_search.py tests/test_math_debugging_router.py
PYTHONPATH=src python -m pytest -q tests/test_mcp_facade.py tests/test_mcp_surface_sync.py tests/test_lean_check.py
python3 -m py_compile src/mathdevmcp/prove_or_refute.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
git diff --check
```

## Check Results

- Workflow stack tests: `24 passed`.
- MCP/Lean boundary tests: `36 passed`.
- Python compile check: passed.
- `git diff --check`: passed.

## Claude Review

Phase 6 read-only review was attempted once with a verdict-only prompt. It
produced no substantive output before interruption and returned a generic
execution error after interrupt.

## Phase 7 Handoff

Proceed to Phase 7: Proof Gap Localization.

Handoff conditions met:

- Proof/refutation statuses can be consumed per derivation step.
- Lean/unavailable/not-encodable boundaries are preserved.
- Phase 7 subplan exists.

## Non-Claims

- This phase does not implement complete theorem proving.
- Lean routes require explicit supplied Lean source.
- Timeout/unavailable/not-encodable outcomes are not refutations.
