# MathDevMCP External-Tool-First Tree Derivation Phase 01/02 Subplan

Date: 2026-07-08

## Phase Objective

Define the backend evidence and search-tree data model that the later budgeted
tree derivation controller will write into. This phase must remain a contract
and serialization phase: no new prover, no tree-search executor, and no
mathematical proof claims.

## Entry Conditions

- Phase 0 external-tool-first policy and `external_tool_first_plan` exist.
- Backend route plans can embed an external-tool-first ledger.
- The current worktree is dirty from prior lanes and must be preserved.
- Public release clean-tree checks are non-gating for this development phase.

## Required Artifacts

- `src/mathdevmcp/derivation_search_tree.py`
- `tests/test_derivation_search_tree.py`
- phase result note under `docs/plans`
- optional integration into `backend_route_planner` only if it remains
  diagnostic and non-certifying

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP serialize a derivation-search branch/tree with source, assumptions, backend attempts, blockers, patch candidates, external-tool-first evidence, and non-claims before implementing search? |
| Baseline/comparator | Phase 0 route plans plus one-shot high-level workflow results. |
| Primary criterion | A tree can be built from a target and `external_tool_first_plan`, serialized deterministically, and marked proved only when supplied certifying evidence satisfies the promotion guard. |
| Veto diagnostics | A node can be marked proved from route/retrieval evidence alone; backend unavailability becomes refutation; in-house branch lacks tool-consideration evidence; schema omits blockers or assumptions. |
| Explanatory diagnostics | Branch status counts, blocker taxonomy, selected-route summary, missing evidence. |
| Not concluded | No search expansion, no backend execution, no proof of target document correctness, no public release readiness. |

## Required Checks

- `python3 -m pytest tests/test_derivation_search_tree.py tests/test_external_tool_policy.py tests/test_backend_route_planner.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/external_tool_policy.py src/mathdevmcp/backend_route_planner.py`
- `git diff --check -- src/mathdevmcp/derivation_search_tree.py tests/test_derivation_search_tree.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-result-2026-07-08.md`

## Required Reviews

- Local skeptical review after implementation.
- Claude review if available; if Claude returns the same server-side
  model-unavailable error as Phase 0, record unavailability and proceed on
  local review plus tests.

## Forbidden Claims And Actions

- Do not claim the tree search engine is implemented.
- Do not run long external backend searches.
- Do not treat `external_tool_first_plan` as proof.
- Do not make public release or clean-tree claims.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 when:

- tree serialization is deterministic;
- branch promotion guards prevent proof/refutation overclaims;
- every branch records external-tool-first evidence or a blocker;
- tests pass.

## Stop Conditions

Stop and write a blocker if:

- the data model cannot express certifying vs diagnostic evidence separately;
- tests cannot prevent route/retrieval evidence from being promoted to proof;
- implementation would require unavailable external backend execution;
- unrelated dirty worktree changes make the touched files impossible to reason
  about safely.

## Skeptical Plan Audit

Wrong baseline: the comparison is not a full prover; it is the current absence
of a branch/tree ledger. The phase should only improve representation.

Proxy metric: node count or selected-tool count is not success. The pass
criterion is schema discipline and promotion-guard behavior.

Environment mismatch: backend tools may be missing or in separate envs. This
phase only records backend attempt metadata supplied by callers.

Hidden assumption: a branch may include assumptions, but they are hypotheses or
accepted/source-backed assumptions, not global truth.

Audit result: proceed with a small data-model implementation and focused tests.
