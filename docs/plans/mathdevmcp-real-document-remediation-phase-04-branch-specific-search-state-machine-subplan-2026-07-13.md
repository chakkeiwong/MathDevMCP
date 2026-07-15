# Phase 04 Branch-Specific Search State Machine Subplan

Date: 2026-07-13

Status: `COMPLETE_PASS_ENGINEERING_ORCHESTRATION_CONTRACT`

Close result:
`docs/plans/mathdevmcp-real-document-remediation-phase-04-branch-state-machine-close-result-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Entry result:
`docs/plans/mathdevmcp-real-document-remediation-phase-03-academic-close-result-2026-07-13.md`

## Phase Objective

Replace the current root-first, one-pass expansion pipeline with a deterministic
branch-local state machine:

```text
select open branch -> formalize branch -> execute branch action
-> update exact branch blocker/evidence -> expand if justified
-> rerank -> repeat until terminal or budget -> compile final tree
```

Phase 04 passes when independently executable child branches own their exact
targets, assumptions, lineage, requests/results, blockers, and terminal state;
no child evidence can promote a parent or sibling; rule templates are not
misrepresented as model/agent execution; compilation observes the final tree;
and every declared resource limit stops further work without becoming a
mathematical refutation.

This phase establishes orchestration correctness on synthetic injected
executors. It does not establish external-backend fitness or close a real
mathematical obligation.

## Entry Conditions

- Phase 03 engineering/context contract is `PASS_ENGINEERING_CONTEXT_CONTRACT`.
- P02 decision SHA-256 remains
  `f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d`.
- P02 obligations SHA-256 remains
  `5aa6681e215d12f382e96f46f9f695cf80e1632affa0dd8bc39069eae78d85a0`.
- P03 reconstructed payload SHA-256 at handoff is
  `e775948681340d8522f13163696cd7070639ba9be7657232f5e6648597a45177`.
- Publication mode remains disabled and both frozen source digests remain
  unchanged.
- The existing 36 branch/search tests pass. This is a compatibility baseline,
  not a Phase 04 promotion criterion.

## Current-Code Gap Audit

1. `document_derivation_tree._branch_backend_attempts` ignores its branch and
   copies every root backend attempt into every assumption branch. This makes
   branch evidence non-local even though publication quarantine currently
   prevents promotion.
2. `_augment_tree` ranks and compiles branches before calling
   `expand_tree_with_hypotheses`; child nodes therefore cannot affect the
   compiled result that users see.
3. `agent_hypothesis_expansion.propose_hypothesis_expansions` is deterministic
   rule code but emits `provenance: agent_generated_candidate` and child status
   `expanded_by_agent`. No model or agent executor is called or recorded.
4. `can_derive_with_budget` executes only the root target. It has no branch
   selector, branch-local request binding, failure-signature feedback loop, or
   transition event log.
5. `BUDGET_PROFILES` covers only `max_attempts`; recursive expansion separately
   covers depth/nodes/candidates. There is no single reservation ledger for
   targets, wall time, per-tool timeout, retrieval/agent calls, input/output
   bytes, or total artifact bytes.
6. `SearchNode.id` is caller-provided and does not bind obligation, typed
   assumptions, lineage, generator provenance, or formalization plan. Parent
   lineage and shared mutable lists are not validated.
7. `branch_promotion_report` checks attempt kinds/statuses but does not itself
   prove that a v1 request/result belongs to the exact branch. P01 binding must
   be enforced at the branch transition, not inferred from a copied attempt.
8. Existing tests confirm candidate construction and one-pass controller
   behavior. They do not demonstrate child execution, parent/sibling isolation,
   final-tree compilation, serial/parallel semantic equivalence, or full budget
   exhaustion.

## Skeptical Plan Audit

- Wrong baseline avoided: the comparator is the current root-attempt projection
  and pre-expansion compilation behavior, not the green 36-test count.
- Proxy metrics rejected: branch count, expanded-node count, ranking score,
  executed attempts, wall time, and deterministic serialization are
  explanatory. The primary criterion is exact branch-local state/evidence and
  final-tree compilation.
- Fair comparison: the legacy and new orchestrators receive the same synthetic
  obligation, assumptions, injected executor outcomes, and budget.
- Hidden assumptions exposed: a generated candidate is not executed evidence;
  a matching tool/status is not branch binding; deterministic scheduling is
  not mathematical correctness; budget exhaustion is not refutation.
- Environment matched: initial work is CPython 3.11 CPU-only with injected
  executors. No GPU, network, installer, model, or live backend is required.
- Stop conditions are below. A failing new isolation test triggers repair; it
  does not require a governance recovery plan.
- Artifact fitness: a compact event log and final semantic tree digest answer
  the phase question. Command receipts and review-budget ledgers do not.

Audit decision: `PASS_TO_SYNTHETIC_IMPLEMENTATION`. Do not run a real backend
or frozen-document experiment in this phase.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Deterministic serial scheduler first | Smallest implementation that exposes state transitions | Makes ownership and budget bugs observable before concurrency | Serial semantics accidentally become the public scheduling contract | Event-log replay plus later serial/parallel digest test | Engineering baseline |
| One active transition at a time | State-machine design | Prevents ambiguous concurrent mutation during initial implementation | Throughput is lower | Synthetic two-child tree must still make independent progress | Reviewed baseline |
| Branch id binds obligation, assumptions, lineage, generator, formalization plan | P01 identity discipline and P04 master contract | Prevents sibling/root evidence substitution | Canonicalization error changes ids or omits a material field | Mutate-one-field identity tests | Reviewed default |
| Rule generator is default; model calls are opt-in | Current implementation is deterministic templates | Honest provenance and reproducible offline tests | Users mistake rule breadth for agent exploration | `rule_generated` required unless execution provenance validates | Reviewed default |
| Smoke budget: 1 target, depth 1, 3 nodes, 2 total attempts, 1 per branch, 30 s wall, 10 s/tool, 0 retrieval, 0 agent, 256 KiB input/output, 5 MiB artifacts | Master-plan initial profile | Smallest useful state-machine diagnostic | Too small can stop a valid route | One exhaustion test per field; remains non-refuting | Baseline hypothesis |
| Standard budget: 6 targets, depth 2, 12 nodes, 18 total attempts, 3 per branch, 180 s wall, 30 s/tool, 8 retrieval, 0 agent, 1 MiB input/output, 50 MiB artifacts | Master-plan initial profile | Bounded compatibility profile for later integration | Inherited values may be poor for real documents | Do not promote; Phase 08 must calibrate target-specific budgets | Baseline hypothesis |
| Compile only after terminal/budget stop | P04 master objective | Ensures child evidence can change the user-visible result | Partial streaming report becomes stale | Pre/post-expansion fixture must differ and compiler must choose final state | Reviewed default |
| Publication remains disabled | P00 and P03 handoff | P04 is orchestration, not claim promotion | A new branch path bypasses quarantine | Existing publication tests plus final-tree no-repair assertion | Hard boundary |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can MathDevMCP execute and update a branch-specific exploratory loop without evidence leakage, false provenance, pre-expansion compilation, or unbounded resources? |
| Exact baseline | Current `can_derive_with_budget`, `_attach_branch_backend_evidence`, `_augment_tree`, `propose_hypothesis_expansions`, and `expand_tree_with_hypotheses` behavior at the P03 handoff. |
| Primary pass criterion | A synthetic two-child tree produces valid branch ids and immutable lineage; executes each selected child against its own target/assumptions; records branch-local request/result/blocker transitions; prevents parent/sibling promotion; skips known failed signatures; stops exactly on every budget dimension; reranks from branch-local evidence; and compiles only the final tree. Serial and injected-parallel schedules have the same semantic tree digest. |
| Veto diagnostics | Shared attempt/evidence lists; branch id unchanged after material assumption/lineage mutation; unrecorded transition; rule output labeled agent execution; backend action before request binding; parent/sibling promotion; duplicate failed action; budget oversubscription; timeout followed by unbounded work; compiler reading pre-expansion state; nondeterministic semantic result; publication/source edit. |
| Explanatory only | Node/attempt count, ranking score, elapsed time, test count, event count, serialized byte count. |
| Not concluded | No proof/refutation, search completeness, best-first/MCTS optimality, useful model-agent generation, real backend fitness, real-document capability, publication, or release readiness. |
| Result artifact | One concise P04 result plus a synthetic two-child event log/final semantic tree fixture or test snapshot. |

## External-Tool-First Ledger

| Tool route | Phase 04 role | Selected now | Reason |
| --- | --- | --- | --- |
| Injected deterministic executor | Exercise request/result and state transitions | Yes | Answers orchestration correctness without conflating backend behavior. |
| SymPy/SageMath | Later branch execution for applicable algebra | No live invocation | Phase 05 owns adapter execution and domain contracts. |
| Lean | Later certification of explicit Lean source | No live invocation | P04 has no formal claim and must not use a successful Lean check to mask branch leakage. |
| LeanSearch-v2/LeanExplore | Later premise retrieval | No live invocation | Retrieval budget/state can be tested with injected records. Retrieval is not proof. |
| jixia/Pantograph/LeanDojo | Later Lean extraction/proof-state interaction | No live invocation | No Lean formalization exists in the P04 synthetic fixture. |
| New in-house mathematical search | Mathematical hypothesis/proof generation | No | P04 adds orchestration and rule-provenance repair, not a mathematical search algorithm. |

## Work Packages

### P04-W1: Immutable Branch Model

- Add a v1 branch record whose semantic id binds obligation digest, normalized
  branch target, typed-assumption binding digests, parent id/lineage, generator
  kind/provenance, and formalization plan.
- Store attempt/request/result manifest references; do not share mutable attempt
  lists across nodes.
- Define and validate an explicit transition table, including `open`,
  `formalization_blocked`, `ready`, `running`, `diagnostic`, `proved`,
  `refuted`, `failed`, and `budget_exhausted` as appropriate. Terminal proof
  states still require P01 exact binding.

Required tests:

- `test_child_branch_id_changes_with_assumptions`;
- `test_child_branch_id_changes_with_lineage_or_formalization`;
- `test_parent_lineage_is_immutable`;
- `test_shared_attempt_or_result_list_is_rejected`;
- `test_branch_state_transition_table_rejects_unrecorded_jump`.

### P04-W2: Honest Generator Provenance

- Rename deterministic template output and status to `rule_generated`.
- Preserve a compatibility reader for old `agent_generated_candidate` records
  as legacy, non-certifying provenance.
- Accept `agent_generated` only through an injected executor result containing
  executor/provider/model identity as applicable, request/response digests,
  timestamp, budget, and exact source/blocker refs.
- Keep failed signatures semantic and generator-scoped so a failed candidate
  is not proposed again under a new cosmetic id.

Required tests:

- `test_rule_template_is_not_agent_generated`;
- `test_agent_generated_requires_execution_provenance`;
- `test_legacy_agent_label_is_noncertifying`;
- `test_failed_signature_is_not_repeated`;
- `test_generated_hypothesis_remains_noncertifying`.

### P04-W3: Iterative Branch Orchestrator

- Add `src/mathdevmcp/derivation_search_orchestrator.py` with injected
  formalizer, executor, retriever, and optional agent-generator interfaces.
- Select one open branch deterministically; reserve budget; bind the exact
  request; execute; persist/update the exact result; close or refine the exact
  blocker; expand only when the transition permits it; rerank; repeat.
- Record a deterministic semantic event log. Execution timestamps/ids may be
  excluded from the semantic digest, but target, branch, request, result,
  transition, and budget effects may not.
- Do not call external tools directly from the orchestrator; use the existing
  adapter boundary and P01 evidence context when Phase 05 connects live routes.

Required tests:

- `test_child_executes_after_expansion`;
- `test_backend_result_changes_exact_child_state_only`;
- `test_child_evidence_cannot_close_parent_or_sibling`;
- `test_blocker_update_names_exact_request_and_result`;
- `test_event_log_replay_reconstructs_final_tree`.

### P04-W4: Unified Resource Budget

- Introduce typed limits for target count, depth, node count, attempts total and
  per branch, wall time, per-tool timeout, retrieval calls, agent calls, input
  bytes, output bytes per attempt, and total artifact bytes.
- Reserve before execution and settle after result persistence. Parallel
  reservation must not oversubscribe a shared limit.
- A timeout or exhausted limit records an engineering/search terminal state and
  stops the relevant action. It is not evidence against the mathematical
  target.

Required tests:

- one exhaustion test per budget dimension;
- `test_budget_exhaustion_is_not_mathematical_refutation`;
- `test_timeout_does_not_consume_unbounded_followup`;
- `test_parallel_reservations_do_not_oversubscribe_budget`;
- `test_oversize_output_cannot_certify_branch`.

### P04-W5: Final-Tree Ranking And Compilation

- Remove root-attempt projection from `_branch_backend_attempts`.
- Rank only from branch-local source/backend evidence and exact blockers.
- Run compilation after the iterative loop reaches a terminal/budget stop.
- Make compilation idempotent and bind it to the final semantic tree digest.
- Preserve the P00 publication quarantine on every library, facade, server,
  CLI, JSON, and Markdown surface.

Required tests:

- `test_compilation_observes_final_tree_not_preexpansion_tree`;
- `test_branch_compilation_is_idempotent`;
- `test_serial_parallel_final_tree_digests_match`;
- `test_conflicting_repeated_execution_vetoes_branch`;
- `test_final_tree_remains_publication_disabled`.

## Implementation Order

1. Add new failing identity, sharing, generator-provenance, and compiler-order
   tests without changing live behavior.
2. Implement the branch record and pure transition validator.
3. Repair rule/agent provenance with legacy compatibility.
4. Implement the injected serial orchestrator and semantic event log.
5. Add the unified budget and every exhaustion test.
6. Move ranking/compilation after the final tree and remove root-attempt
   projection.
7. Run focused tests, adjacent tree/report/publication tests, compilation, and
   diff inspection.

## Required Checks

Smallest first:

```bash
env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_derivation_search_tree.py \
  tests/test_derivation_branch_controller.py \
  tests/test_agent_hypothesis_expansion.py \
  tests/test_derivation_tree_expansion.py \
  tests/test_derivation_search_orchestrator.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_tree_derivation_lane_integration.py \
  tests/test_document_publication_quarantine.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile \
  src/mathdevmcp/derivation_search_tree.py \
  src/mathdevmcp/derivation_branch_controller.py \
  src/mathdevmcp/agent_hypothesis_expansion.py \
  src/mathdevmcp/derivation_tree_expansion.py \
  src/mathdevmcp/derivation_search_orchestrator.py \
  src/mathdevmcp/document_derivation_tree.py

git diff --check
```

If aggregate document tests exceed the command runner's duration, split them
by file or test node and record only explicit zero-exit results. Do not weaken
assertions or call an unterminated run a pass.

## Required Artifacts

- v1 branch, transition, budget, event, and final-tree schemas in code/tests;
- synthetic two-child fixture with different assumptions and injected outcomes;
- event-log replay and final semantic tree digest comparison;
- one concise Phase 04 result with decision table, exact commands/environment,
  residual risks, and non-claims;
- updated next-phase plan only if the Phase 04 criteria pass.

Content digests are required for branch identity, requests/results, event-log
semantic identity, and final-tree compilation. Digests are not required for
every test log, prose edit, or command transition.

## Forbidden Claims And Actions

- Do not copy root, parent, or sibling attempts into a child as its evidence.
- Do not execute a branch before its exact request and resource reservation
  exist.
- Do not label deterministic templates `agent_generated`.
- Do not treat retrieval, rule generation, formalization plans, proof-state
  traces, timeout, unavailability, or budget exhaustion as proof/refutation.
- Do not introduce a new in-house mathematical derivation/search algorithm in
  this phase.
- Do not run a live mathematical backend, network/model route, GPU job,
  installer, frozen-document experiment, or long benchmark under this plan.
- Do not edit either frozen source document, enable publication, change public
  defaults, commit, or push.

## Exact Phase 05 Handoff Conditions

Phase 05 planning may begin only when:

- every new primary test above passes;
- the legacy 36-test branch/search baseline remains compatible or each
  intentional schema change has an explicit legacy reader/test;
- the synthetic two-child event log replays to the final tree;
- serial and injected-parallel schedules have equal semantic tree digests;
- no attempt/result list is shared and no child evidence affects a parent or
  sibling;
- deterministic templates are `rule_generated`, and `agent_generated` requires
  execution provenance;
- all budget fields have a passing exhaustion test and no exhaustion is
  classified mathematically;
- compiler output is bound to the final tree and remains publication-disabled;
- the Phase 04 result decision is `pass` with all vetoes false.

The handoff permits Phase 05 adapter planning, not backend promotion or repair
publication.

## Stop Conditions

Stop and repair the phase before live integration if branch identity omits a
material field, evidence leaks across lineage, a transition cannot be replayed,
a budget can be oversubscribed, rule provenance remains false, or compilation
uses stale tree state.

Stop for user direction only if the remaining choice changes a public default,
requires live external/model/GPU execution, expands scientific scope, enables
publication, incurs material cost, or changes release/product direction.
Ordinary test failures and implementation defects are repair work, not human
governance blockers.
