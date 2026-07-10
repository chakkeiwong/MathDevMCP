# MathDevMCP External-Tool-First Tree Derivation Phase 03 Result

Date: 2026-07-08

## Objective

Implement bounded external-tool adapter evidence wrappers that convert existing
MathDevMCP backend/tool results into Phase 1/2 `BackendAttempt` records.

## Artifacts

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-03-subplan-2026-07-08.md`
- `src/mathdevmcp/external_tool_adapters.py`
- `tests/test_external_tool_adapters.py`

## What Changed

Added `external_tool_adapter_attempt_result`, a narrow adapter contract that
wraps heterogeneous backend/tool outputs into tree-compatible attempts.

Implemented adapter wrappers for:

- scoped algebra derivation/refutation through existing `derive_or_refute`;
- bounded counterexample search through existing `find_counterexample`;
- direct Lean checking through existing `check_lean_source`;
- LeanSearch/LeanExplore-style retrieval evidence as non-certifying;
- jixia-style static extraction evidence as non-certifying;
- Pantograph/LeanDojo-style proof-state evidence as non-certifying.

The wrappers support injected runners so tests and future branch search can use
bounded, deterministic calls. Expected adapter exceptions are caught and
returned as diagnostic attempts rather than escaping as unbounded failures.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Primary criterion | Passed for Phase 3: direct adapter wrappers now return tree-compatible `BackendAttempt` payloads with tool, status, evidence kind, certification status, input summary, output reference, timeout/version metadata, and the Phase 1/2 promotion boundary. |
| Veto diagnostics | Passed in focused tests: backend unavailable, Lean inconclusive/placeholder, adapter exceptions, retrieval, static extraction, and proof-state evidence remain diagnostic; certifying algebra, concrete counterexample, and direct Lean verification map to promotable attempts only under the Phase 1/2 guard. |
| Explanatory diagnostics | Tests use injected/mocked runner results; no optional packages or long real backend calls were required. |
| Not concluded | No branch search, no document repair, no broad theorem proving, no public release readiness, no claim that optional integrations are installed. |

## Checks

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py tests/test_external_tool_policy.py -q` | Passed after repair: 26 passed. |
| `python3 -m py_compile src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/external_tool_policy.py` | Passed. |
| `git diff --check -- src/mathdevmcp/external_tool_adapters.py tests/test_external_tool_adapters.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-03-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-03-result-2026-07-08.md` | Passed after repair. |

## Review

Local skeptical review found no phase blocker. The main boundary is preserved:
adapters produce evidence attempts; they do not schedule branch search or
certify beyond the underlying backend result.

Claude review was not attempted for this phase because Phase 1/2 established
that exporting bounded local plan/code/test artifacts to the external Claude
service was rejected by the sandbox reviewer.

A fresh Codex read-only fallback review returned `VERDICT: REVISE` with two
test-coverage findings:

1. Timeout-like adapter evidence was required to remain diagnostic, but the
   initial tests did not pin that behavior.
2. `scoped_contradiction` refutation mapping was implemented for algebra
   refutation and Lean mismatch, but not tested.

Both findings were repaired. Tests now cover timeout-like counterexample
evidence as diagnostic, algebra scoped-contradiction refutation, and Lean
mismatch scoped-contradiction refutation. The added algebra test exposed a real
robustness bug: `_derive_status_mapping` assumed `counterexample_search` was a
dict. That mapping now handles `None` safely. The focused pytest, py-compile,
and diff checks passed after repair.

## Next Handoff

Proceed to Phase 4 if closeout checks and fallback review pass. Phase 4 should
implement the budgeted branch controller over these evidence-producing actions:

- initialize a search tree from an external-tool-first plan;
- schedule safe and unsafe branch actions under a small budget;
- record assumptions, formalization blockers, backend attempts, and patch
  candidates;
- stop with `proved`, `refuted`, `partial`, `blocked`, or
  `budget_exhausted` only under the Phase 1/2 promotion guard.
