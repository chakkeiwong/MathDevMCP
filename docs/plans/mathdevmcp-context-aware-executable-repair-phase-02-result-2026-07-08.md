# Phase 02 Result: Local Mathematical Context Graph

Date: 2026-07-09

Status: `PASSED`

## Objective

Build a deterministic context graph around document derivation targets so the
workflow separates source-stated assumptions from missing or unresolved route
requirements before repair proposals are generated.

## Implementation Summary

- Added `build_local_context_graph` in
  `src/mathdevmcp/document_derivation_tree.py`.
- Attached context graphs to proposition/context packets and semantic target
  packets.
- Added paragraph-context inheritance for equation rows so display-equation
  targets can see nearby proposition hypotheses.
- Added Markdown rendering and coverage counters for context graph statuses.
- Added regression tests for `prop:interior-foc` and `eq:foc-k`.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the workflow avoid proposing assumptions that are already stated nearby? |
| Baseline/comparator | Prior document-tree reports had route-required assumptions but no local stated/missing graph. |
| Primary criterion | Passed. `prop:interior-foc` marks interiority and differentiability as `stated`; row-level `eq:foc-k` marks them `nearby_stated`; expectation law/integrability/interchange remain `missing` or `unresolved`. |
| Veto diagnostics | No veto triggered: not all assumptions are missing, not all are stated, source refs are present, and the graph has an explicit non-proof boundary. |
| Not concluded | Context graph statuses are diagnostics only; they do not prove adequacy, sufficiency, backend encodability, or global minimality. |

## Frozen Smoke Artifact

- Markdown: `docs/reviews/risky-debt-context-graph-phase02-smoke-2026-07-09.md`
- JSON: `docs/reviews/risky-debt-context-graph-phase02-smoke-2026-07-09.json`

Smoke summary:

- Context graphs: `3`
- Context graph statuses:
  `{'stated': 6, 'nearby_stated': 17, 'inferred_candidate': 15, 'unresolved': 12, 'missing': 4}`
- Proposition graph:
  - `assumption_interior_action`: `stated`
  - `assumption_relevant_functions_differentiable`: `stated`
  - `requirement_conditional_integrability`: `unresolved`
  - `requirement_expectation_derivative_interchange`: `unresolved`
- Row graph for `eq:foc-k`:
  - `assumption_interior_action`: `nearby_stated`
  - `assumption_relevant_functions_differentiable`: `nearby_stated`
  - `route_assumption_target_function_is_differentiable_on_the_stated_domain`: `nearby_stated`
  - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`: `missing`
  - `route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present`: `missing`

## Checks

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_assumption_discovery.py -q`
  - Passed: `13 passed in 67.46s`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/assumption_discovery.py`
  - Passed.
- `git diff --check`
  - Passed.
- Targeted whitespace/final-newline check on touched Phase 02 files and smoke
  Markdown:
  - Passed.

## Review

Claude review was not retried in Phase 02 because the Phase 00 gate already
recorded external-service review rejection in this environment.

A fresh subagent reviewer was attempted, but the local agent thread limit was
already reached.  No code was delegated.  Codex performed a local read-only
skeptical review against the Phase 02 evidence contract:

- Proof overclaim check: passed.  Context graphs carry an explicit non-proof
  boundary and do not certify sufficiency.
- Source-reference check: passed for the frozen FOC requirements.
- Consistency check: passed after row-level packets inherited paragraph context;
  differentiability is no longer marked missing for `eq:foc-k` when the parent
  proposition states it.
- Remaining risk: graph rules are deterministic and intentionally bounded; they
  may miss differently worded assumptions until Phase 03 typed IR and later
  backend routes add stronger structure.

## Phase 03 Handoff

Phase 03 may start.

Entry evidence available:

- Context graph records are attached to proposition/context packets and
  semantic target packets.
- Graph records include `status`, `mathematical_role`, `why_status`,
  `source_refs`, `required_next_evidence`, and `evidence_refs`.
- Frozen FOC targets preserve expectation/derivative blockers for typed IR.

Phase 03 must not treat these graph statuses as proof.  It should convert them
into typed repair obligations that record operators, variables, assumptions,
unresolved constructs, and backend route hints.
