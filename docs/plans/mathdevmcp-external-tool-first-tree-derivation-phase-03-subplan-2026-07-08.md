# MathDevMCP External-Tool-First Tree Derivation Phase 03 Subplan

Date: 2026-07-08

## Phase Objective

Implement direct external-tool adapter evidence wrappers that convert existing
MathDevMCP backend/tool results into the Phase 1/2 `BackendAttempt` schema.
This phase is not the branch controller. It must only produce bounded evidence
objects that later search nodes can consume.

## Entry Conditions

- Phase 0 external-tool-first policy exists.
- Phase 1/2 search-tree data model and promotion guards exist.
- The current worktree is dirty from prior lanes and must be preserved.
- Claude review may be unavailable because exporting local artifacts to an
  external service was rejected by the sandbox reviewer in Phase 1/2.

## Required Artifacts

- `src/mathdevmcp/external_tool_adapters.py`
- `tests/test_external_tool_adapters.py`
- phase result note under `docs/plans`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP turn direct external/backend tool results into bounded tree-compatible evidence attempts without overclaiming certification? |
| Baseline/comparator | Phase 1/2 tree accepts manual `BackendAttempt` records; existing low-level tools return heterogeneous contracts. |
| Primary criterion | Adapter wrappers return deterministic `BackendAttempt` payloads with tool, status, evidence kind, certification status, input summary, output reference, version/timeout metadata, and the Phase 1/2 promotion boundary. |
| Veto diagnostics | Retrieval/static/proof-state adapters return certifying evidence; backend unavailable becomes refutation; Lean placeholder/inconclusive results become proof; an adapter raises instead of returning a bounded failure attempt for expected backend unavailability/errors. |
| Explanatory diagnostics | Tool availability/version, formalization-required states, timeout metadata, and source contract references. |
| Not concluded | No branch search, no document repair, no broad theorem proving, no public release readiness, no claim that optional integrations are installed. |

## Required Checks

- `python3 -m pytest tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py tests/test_external_tool_policy.py -q`
- `python3 -m py_compile src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/external_tool_policy.py`
- `git diff --check -- src/mathdevmcp/external_tool_adapters.py tests/test_external_tool_adapters.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-03-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-03-result-2026-07-08.md`

## Required Reviews

- Local skeptical review after implementation.
- Claude review only if allowed without exporting local code/test artifacts.
  If it is blocked again by policy, record that and use a fresh Codex
  read-only fallback review for material boundary issues.

## Evidence Adapter Scope

Implement wrappers for:

- SymPy/Sage algebra route via existing `derive_or_refute` result contracts;
- bounded counterexample route via existing `find_counterexample`;
- Lean direct check via existing `check_lean_source`;
- LeanSearch-v2/LeanExplore retrieval as diagnostic evidence only;
- jixia static extraction as diagnostic evidence only;
- Pantograph/LeanDojo proof-state attempts as diagnostic evidence only unless
  followed by direct Lean verification in a future phase.

## Forbidden Claims And Actions

- Do not implement the budgeted branch controller.
- Do not run long real backend searches.
- Do not require optional packages to be installed for tests.
- Do not treat retrieval, static extraction, proof-state traces, or route
  plans as certificates.
- Do not claim public release readiness.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 when:

- adapter wrappers can produce tree-compatible `BackendAttempt` records;
- tests show certification/refutation mapping works only for the allowed
  backend statuses;
- unavailable, timeout, placeholder, retrieval, static, and proof-state paths
  remain diagnostic;
- adapter exceptions are captured as bounded diagnostic attempts.

## Stop Conditions

Stop and write a blocker if:

- existing low-level contracts cannot be mapped to `BackendAttempt` without
  losing certification/refutation boundaries;
- tests cannot prevent retrieval/static/proof-state evidence from promoting a
  branch;
- adapter implementation would require installing packages or running external
  services without approval;
- unrelated dirty worktree changes make the touched files impossible to reason
  about safely.

## Skeptical Plan Audit

Wrong baseline: Phase 3 is not trying to beat a prover or produce document
repairs. It only normalizes existing heterogeneous backend outputs into the
tree evidence schema.

Proxy metric: number of adapters is not success. The pass criterion is bounded
evidence mapping and preservation of certification boundaries.

Environment mismatch: optional tools may be absent or in isolated backend
environments. Tests must use injected/mocked calls and must not depend on
installed optional packages.

Hidden assumption: a successful retrieval or proof-state trace may be useful,
but it is not a proof. Only direct backend certificates or concrete
counterexamples can promote a branch.

Audit result: proceed with a narrow adapter-evidence module and mocked tests.
