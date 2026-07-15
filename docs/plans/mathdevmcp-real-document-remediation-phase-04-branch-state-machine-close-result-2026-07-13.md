# Phase 04 Branch-State-Machine Close Result

Date: 2026-07-13

Status: `PASS_ENGINEERING_ORCHESTRATION_CONTRACT`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Plan:
`docs/plans/mathdevmcp-real-document-remediation-phase-04-branch-specific-search-state-machine-subplan-2026-07-13.md`

Entry result:
`docs/plans/mathdevmcp-real-document-remediation-phase-03-academic-close-result-2026-07-13.md`

Synthetic snapshot:
`docs/plans/mathdevmcp-real-document-remediation-phase-04-synthetic-snapshot-2026-07-13.json`

## Decision

Phase 04 passes its bounded engineering-orchestration contract. MathDevMCP now
has an injected-only branch state machine whose semantic branch identity binds
the obligation, target, typed assumptions, lineage, generator provenance, and
formalization plan. Requests reserve shared resources before executor entry,
results update only the exact branch, event replay reconstructs the final tree,
and compilation is bound to the post-expansion semantic tree digest.

The document workflow no longer copies a root backend attempt into each
assumption branch. A child without a branch-bound request and result remains
`branch_execution_pending`; formalization work and mathematical assumption
gaps are reported separately. Deterministic templates are `rule_generated`,
not agent execution. Generated document-tree children remain explicitly
unexecuted and non-certifying in Phase 04.

Publication remains disabled. No frozen source was edited. No Phase 04 live
external-backend, model, network, GPU, installer, publication, commit, or push
action was performed.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Engineering question | Pass: branch selection, formalization, request binding, injected execution, exact update, expansion, reranking, replay, budgeting, and final compilation form one bounded branch-local loop. |
| Comparator | The P03 handoff behavior that copied root attempts into every assumption branch and compiled before recursive expansion. |
| Primary criterion | Pass: a synthetic two-child tree executes each child against its own target and typed assumptions, retains empty parent ledgers, replays to the final tree, produces equal serial/parallel semantic digests, and compiles only that final tree. |
| Veto diagnostics | Pass: material identity mutation, shared mutable ledgers, illegal transitions, result-binding mismatch, parent/sibling leakage, repeated failed signatures, contradictory repeated results, rule/agent provenance confusion, every declared budget dimension, parallel reservation oversubscription, stale compilation, digest instability, and publication leakage are rejected or stopped explicitly. |
| Explanatory only | Test count, event count, ranking order, serialized bytes, and wall time. |
| Not concluded | No mathematical proof/refutation, search completeness, optimality, useful model-agent generation, live backend fitness, real-document repair capability, publication readiness, release readiness, or mission completion. |

## Implementation Result

### Branch identity and transitions

- `p04_branch_record@1` binds all material branch-local inputs and uses a
  closed transition table.
- Parent lineage and mutable branch ledgers are validated; parent, child, and
  sibling request/result refs remain disjoint.
- Event records form a replayable semantic chain. Replay and live final-tree
  digests must match before compilation.

### Generator provenance

- Deterministic hypothesis templates emit `rule_generated` provenance and
  `expanded_by_rule` state.
- Historical `agent_generated_candidate` records normalize to
  `legacy_rule_generated` with an explicit non-agent-execution non-claim.
- Real `agent_generated` provenance requires executor/provider/model fields as
  applicable, request/response digests, timestamp, budget, and source refs.

### Execution and resource accounting

- `src/mathdevmcp/derivation_search_orchestrator.py` supports serial, reverse,
  and actual injected-parallel schedules.
- Parallel mode reserves attempts, retrieval/agent calls, aggregate input
  bytes, request artifacts, and bounded result-artifact capacity before
  dispatch. Executor calls beyond a shared limit never start.
- Result reservations settle to zero on success, binding failure, output
  overflow, artifact rejection, and contradictory repeated observations.
- Target, depth, node, total/per-branch attempt, wall-time, tool-timeout,
  retrieval, agent, input, output, and artifact limits stop work without
  becoming mathematical refutation.
- Two materially conflicting observations for one exact request are retained
  diagnostically and fail the branch; neither result ref can promote it.

### Document integration

- `_branch_backend_attempts` accepts only attempts already bound to the exact
  child `branch_id`, `request_ref`, and `result_ref`; root evidence remains on
  the root.
- Recursive expansion completes before assumption-branch ranking,
  expanded-node ranking, and report compilation.
- The compiler derives and records the final document-tree digest, expanded
  node ids, and publication-disabled state. Recompilation of the same final
  tree is byte-for-byte idempotent.
- Gap reports distinguish `branch_execution_pending`,
  `formalization_blocked`, `mathematical_blocked`,
  `evidence_binding_error`, and `engineering_error` instead of interpreting
  every unexecuted path as evidence against the mathematics.
- A proposition label without an exact extractable obligation now remains
  `needs_evidence`; the old full-block fallback does not launch route planning
  or backend work.

## Synthetic Snapshot

The compact two-child snapshot has SHA-256
`26471e2af89686bbc549518b4cc90500c9414fa38277e448d37016e34d51f6a2`
and size 2,587 bytes. Its serial and injected-parallel semantic tree digest is:

```text
deae0b2142d19c83c424a7178675cff9a686a4519ea9134f0e0f1f18ca89390a
```

Both children have distinct semantic ids, request refs, result refs, typed
assumption digests, and terminal transitions. The root has no request or result
refs. Serial and parallel rankings agree, replay reconstructs the same final
tree, publication is disabled, and `artifact_reserved_bytes` returns to zero.
The fixture's synthetic `proved` states are state-machine evidence only.

## Verification

Environment: CPython 3.11.15, pytest 9.0.2, git commit
`a85fbb676eb4d551a8d78a70a5043524f308b7b9`, CPU-only with
`CUDA_VISIBLE_DEVICES=-1`. The worktree remained intentionally dirty.

Frozen source identities remained:

- risky debt: `d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1`;
- card NPV: `dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8`.

| Check | Result |
| --- | --- |
| Phase 04 branch, controller, provenance, expansion, orchestrator | 65 passed in 0.34 s |
| Source-aware audit report and tree-lane integration | 10 passed in 28.96 s |
| Bounded real-document regressions | 3 passed in 29.32 s |
| Document derivation tree | All 17 nodes passed with explicit zero exits; context-heavy nodes were rerun sequentially rather than counting unterminated aggregates |
| Publication quarantine | 11 pytest nodes passed individually; the remaining combined library/facade/server/CLI parity contract passed as four separate zero-exit surface invocations |
| Public document integration focus | Final-tree order/idempotence/child-isolation: 3 passed; worker order and CLI artifacts: 2 passed |
| Snapshot JSON | Standard-library JSON parser passed; snapshot digest and byte size recorded above |
| Compilation | `py_compile` passed for all six Phase 04 implementation modules |
| Diff hygiene | `git diff --check` passed |

Several aggregate commands exceeded the command runner's practical duration
and returned no pytest verdict. They are not counted. Their complete test-node
sets were rerun in bounded processes with explicit zero exits. `jq` was not
installed, so snapshot JSON was validated with `python -m json.tool`.

Existing document regression tests may invoke the already-connected root
adapter on local algebra fixtures. Those attempts remained root-only,
publication-disabled diagnostics and are not Phase 04 branch/backend capability
evidence. No live generated child was executed by the document workflow.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Pass Phase 04 engineering-orchestration contract. |
| Primary criterion | Pass: exact branch-local execution, replay, shared-budget reservation, schedule-independent semantic tree, and final-tree compilation. |
| Veto diagnostics | Pass: no shared evidence, stale compilation, false generator provenance, contradictory-result promotion, unbounded followup, shared-budget overrun, or publication leak. |
| Engineering ledger | Branch identities, transitions, request/result binding, replay, reservations, expansion, ranking, compilation, and public document surfaces pass focused and adjacent checks. |
| Mathematical-validity ledger | Empty for Phase 04. Injected outcomes and existing root diagnostics have no mathematical authority at the document branch boundary. |
| Interpretation ledger | The implementation is safe to connect to separately planned live adapters; it does not yet show that an external tool can advance a real branch. |
| Main uncertainty | Synthetic fixtures may miss adapter-specific process, timeout, native-input, version, and artifact failures that only appear at the live boundary. |
| Next justified action | Write and audit a Phase 05 subplan for supported external-tool adapters, beginning with preflight and injected/fake-runner contract tests before any trusted live smoke. |
| Not concluded | Proof, backend breadth, substantive real-document capability, repair publication, release readiness, or mission completion. |

## External-Tool Ledger

The selected Phase 04 route was the injected deterministic executor because the
question was orchestration correctness. SymPy, SageMath, Lean, LeanSearch-v2,
LeanExplore, jixia, Pantograph, and LeanDojo were considered for Phase 05 but
were not invoked as Phase 04 branch executors. No new in-house mathematical
search algorithm was introduced.

## Post-Run Red Team

The strongest alternative explanation is fixture fit: immutable branch ids and
shared reservations work on compact injected records, while a real subprocess
adapter may expose encoding, cancellation, output-framing, tool-version, or
artifact-persistence behavior not represented here.

The conclusion would be overturned by a reproducible case where a child accepts
a parent/sibling result, a parallel executor starts beyond a reserved limit,
conflicting exact-request observations promote a branch, replay differs from
the live final tree, compilation changes when repeated on the same final tree,
or any public surface enables an applicable repair.

The weakest evidence is live process integration because Phase 04 deliberately
did not execute a generated branch through an external backend. The improvement
is orchestration correctness and safer classification, not mathematical closure
or substantive capability.

## Handoff

Phase 05 planning may begin. The handoff authorizes adapter-plan design,
preflight inspection, and fake/injected-runner tests. It does not by itself
authorize network/model/GPU work, environment mutation, a trusted live backend
smoke, frozen-document capability execution, publication, source edits, or a
default/release change. Those actions require the Phase 05 evidence contract,
skeptical audit, and applicable approval.
