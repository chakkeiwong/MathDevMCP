# MathDevMCP External-Tool-First Tree Derivation Phase 04 Subplan

Date: 2026-07-08

## Phase Objective

Implement the first budgeted branch controller over the Phase 1/2 search-tree
records and Phase 3 adapter evidence wrappers. The controller should answer a
scoped "can we derive/refute this target?" question with a tree status and
durable evidence ledger: `proved`, `refuted`, `partial`, `blocked`, or
`budget_exhausted`.

## Entry Conditions

- Phase 0 external-tool-first policy exists.
- Phase 1/2 search-tree data model and promotion guards exist.
- Phase 3 adapter evidence wrappers exist and map direct backend/tool results
  into tree-compatible `BackendAttempt` records.
- The current worktree is dirty from prior lanes and must be preserved.
- Claude review is not available unless local artifact export is explicitly
  permitted; use local Codex fallback review if needed.

## Required Artifacts

- `src/mathdevmcp/derivation_branch_controller.py`
- `tests/test_derivation_branch_controller.py`
- phase result note under `docs/plans`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP run a small budgeted controller that records branch evidence and returns useful non-yes/no derivation status without overclaiming proof/refutation? |
| Baseline/comparator | Phase 1/2 can serialize trees manually; Phase 3 can create evidence attempts manually; no controller schedules evidence actions yet. |
| Primary criterion | Given a target and budget profile, the controller initializes an external-tool-first tree, attempts bounded evidence actions in deterministic order, records backend attempts/blockers, and sets root status only through the Phase 1/2 promotion guard. |
| Veto diagnostics | Controller marks proved/refuted without promotable evidence; in-house search runs when external-tool-first plan is blocked; budget exhaustion loses blocker/evidence state; adapter errors escape instead of becoming diagnostic blockers. |
| Explanatory diagnostics | Attempt counts, budget profile, selected tools, exhausted actions, blockers, and non-claims. |
| Not concluded | No MCTS, no completeness, no global minimality, no real document repair, no public release readiness. |

## Required Checks

- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py`
- `git diff --check -- src/mathdevmcp/derivation_branch_controller.py tests/test_derivation_branch_controller.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-04-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-04-result-2026-07-08.md`

## Required Reviews

- Local skeptical review after implementation.
- Fresh Codex read-only fallback review for material boundary issues if time
  permits. Do not use Claude if it requires exporting local artifacts without
  explicit permission.

## Controller Scope

Implement:

- budget profiles `smoke` and `standard`;
- deterministic action order: algebra check, counterexample search, Lean check
  when explicit Lean source is supplied, retrieval/static/proof-state
  diagnostics only when supplied as precomputed evidence;
- blocker creation for external-tool-first gate failure, adapter diagnostic
  failures, missing Lean source for Lean certification, and budget exhaustion;
- tree summary update after attempts.

Defer:

- MCTS or learned search policies;
- automatic assumption expansion;
- automatic LaTeX-to-Lean formalization;
- report rendering.

## Forbidden Claims And Actions

- Do not implement full MCTS.
- Do not run long real backend searches.
- Do not generate document repair reports.
- Do not treat retrieval/static/proof-state evidence as proof.
- Do not ignore the external-tool-first blocked gate.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 when:

- the controller returns a tree contract with durable backend attempts and
  blockers;
- tests show proved/refuted only occur through promotion-guard evidence;
- budget exhaustion leaves a useful blocker ledger;
- blocked external-tool-first plans do not run in-house search;
- adapter errors become diagnostic blockers.

## Stop Conditions

Stop and write a blocker if:

- the controller cannot reuse the Phase 1/2 promotion guard;
- implementing useful branch control requires installing external services or
  running long backends;
- test fixtures cannot distinguish blocked, partial, proved, refuted, and
  budget-exhausted states;
- unrelated dirty worktree changes make touched files unsafe to edit.

## Skeptical Plan Audit

Wrong baseline: this phase is not implementing complete theorem search. It is
only adding the first budgeted controller over existing evidence actions.

Proxy metric: number of attempted actions is not success. The pass criterion is
evidence preservation and status discipline under the promotion guard.

Hidden assumption: no branch should assume a missing formalization or
assumption set. Missing formalization must be a blocker or partial state.

Environment mismatch: tests must inject adapter results and avoid optional
backend requirements.

Audit result: proceed with a small deterministic controller skeleton and
focused tests.
