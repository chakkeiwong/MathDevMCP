# MathDevMCP External-Tool-First Tree Derivation Mission Control

Date: 2026-07-08

Status: `ACTIVE_INTERNAL_LANE`

## Purpose

This mission-control document governs the external-tool-first tree derivation
lane. The lane exists to make hard derivation and repair questions useful to
agents without reverting to yes/no answers, generic prose, or hallucinated math.

The lane is an orchestration layer, not a new theorem prover. It considers
existing deterministic and specialist tools first, records evidence and
blockers in a durable tree, and renders reports from that evidence.

## Completed Master-Program Slice

| Phase | Artifact class | Status | Boundary |
| --- | --- | --- | --- |
| 0 | External-tool-first policy and route plan | Completed | Route plans are not proofs. |
| 1/2 | Search-tree data model and promotion guards | Completed | Tree records are ledgers, not certificates. |
| 3 | External-tool adapter evidence wrappers | Completed | Adapters certify only what backend results certify. |
| 4 | Deterministic budgeted branch controller | Completed | Controller is a bounded scheduler, not complete search. |
| 5 | Branch-derived report renderer | Completed | Renderer does not invent patches or assumptions. |
| 6 | Mission-control and regression durability | This phase | No release-readiness claim. |

## Callable Contracts

- `external_tool_first_plan_result`
- `derivation_search_tree_result`
- `external_tool_adapter_attempt_result`
- `derivation_tree_report_result`
- `agent_hypothesis_expansion`
- `agent_hypothesis_expansion_set`
- `backend_formalization_target`
- `tool_grounded_proposal_compiler_result`
- `document_derivation_tree_parallel_execution`

## Core Invariants

1. External tools must be considered before in-house branch expansion.
2. Retrieval, route planning, static extraction, proof-state traces,
   unavailable backends, timeouts, and placeholders are diagnostic only.
3. `proved` requires scoped certifying backend evidence accepted by the
   promotion guard.
4. `refuted` requires a concrete counterexample or scoped contradiction
   accepted by the promotion guard.
5. Lean evidence can certify a controller branch only when the Lean source is
   conservatively bound to the controller target.
6. Budget exhaustion must preserve attempted actions, exhausted actions, and
   blockers.
7. Reports must render location, problem, mathematical why, exact tools,
   assumptions/routes, patch candidates, blockers, promotion guard status, and
   non-claims from the tree.
8. Reports must not fabricate patches, assumptions, proofs, or document edits.
9. Agent hypotheses are candidate branches only.  They may unblock search by
   proposing assumptions, routes, or formalization targets, but they cannot be
   published as repairs until the derivation tree records backend-closed or
   partially backend-closed evidence.
10. `audit_document_derivation_tree` must default to
    `search_mode="agent_guided"` and `grounding_policy="strict"`.  The strict
    compiler may publish repair proposals only from closed or partially closed
    tree/backend paths.  Blocked paths must be rendered as exact gap reports.
11. Optional parallel execution may change scheduling only.  Outputs must be
    sorted back to deterministic source order, and worker failures must become
    blockers rather than refutations or repairs.

## Required Regression Checks

Run these before modifying this lane:

```bash
python3 -m pytest \
  tests/test_tree_derivation_lane_integration.py \
  tests/test_derivation_branch_controller.py \
  tests/test_derivation_tree_report.py \
  tests/test_external_tool_adapters.py \
  tests/test_derivation_search_tree.py -q
```

For the agent-guided, tool-verified document repair lane, also run:

```bash
python3 -m pytest \
  tests/test_document_derivation_tree.py \
  tests/test_agent_hypothesis_expansion.py \
  tests/test_derivation_tree_expansion.py \
  tests/test_backend_formalization_target.py -q
```

For focused edits, also run:

```bash
python3 -m py_compile \
  src/mathdevmcp/derivation_branch_controller.py \
  src/mathdevmcp/derivation_tree_report.py \
  src/mathdevmcp/external_tool_adapters.py \
  src/mathdevmcp/derivation_search_tree.py \
  src/mathdevmcp/document_derivation_tree.py \
  src/mathdevmcp/agent_hypothesis_expansion.py \
  src/mathdevmcp/derivation_tree_expansion.py \
  src/mathdevmcp/backend_formalization_target.py
```

Before claiming real-document report improvement, regenerate the frozen strict
reports:

```bash
python3 -m mathdevmcp.cli audit-document-derivation-tree \
  docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex \
  --focus-label eq:panel-npv-functional \
  --focus-label eq:incremental-cash-flow \
  --focus-label eq:incremental-npv \
  --search-mode agent_guided --grounding-policy strict --workers 2 --max-attempts 1

python3 -m mathdevmcp.cli audit-document-derivation-tree \
  docs/risky-debt-maliar-deep-learning-lecture-note.tex \
  --focus-label prop:interior-foc \
  --focus-label eq:foc-k \
  --focus-label eq:foc-b \
  --search-mode agent_guided --grounding-policy strict --workers 2 --max-attempts 1
```

## Future Work

- Expose controller/report functions through CLI/MCP.
- Add benchmark fixtures for strict compiler, assumption expansion, and
  formalization blockers.
- Add MCTS/best-first expansion only after deterministic adapter and report
  boundaries remain stable.
- Add optional real-backend smoke tests under explicit backend profiles.

## Non-Claims

- This lane does not prove whole documents.
- This lane does not establish public release readiness.
- This lane is not a complete theorem prover or MCTS implementation.
- Passing local regression tests does not certify mathematical correctness of a
  target document.
