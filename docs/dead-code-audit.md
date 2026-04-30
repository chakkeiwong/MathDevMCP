# MathDevMCP — dead code audit

A follow-up to [`mcp-simplification.md`](mcp-simplification.md). After the
MCP-surface refactor, the production-reachable graph (CLI → library
modules → MCP facade → primitives) is much clearer, and a handful of
modules turn out to have **no production consumer** — only their own
test files import them.

This audit is read-only; it does not delete anything. It catalogues
what's removable so a maintainer can decide the scope of a follow-up
cleanup PR.

## Method

For every `src/mathdevmcp/*.py`, count importers across `src/`,
`tests/`, and `scripts/`. Flag any module whose only importers are test
files (or whose only "importer" is a string literal in a comment /
roadmap / capability label, not an actual `import`).

Two such string mentions exist and are red herrings:

- `src/mathdevmcp/tool_matrix.py` lists `"lean_export"` inside a
  `later_tools` recommendation — a literal string, not an import.
- `src/mathdevmcp/mcp_facade.py` tags the `check_equality` MCP spec
  with `optional_capability="symbolic_backend"` — also a label string;
  the actual sympy call lives in `proof_obligations.py`.

Neither keeps the corresponding module live.

## Findings

**7 modules are dead** (no production consumer; only tests reference
them):

### Cleanly deletable (dead module + dedicated test file)

| Module | LOC | Test file | Test LOC |
|---|---|---|---|
| `src/mathdevmcp/symbolic_backend.py` | 34 | `tests/test_symbolic_backend.py` | 23 |
| `src/mathdevmcp/domain_formalization.py` | 111 | `tests/test_domain_formalization.py` | 64 |

These are pure `git rm` candidates — module + test go together, no
other code touches either side. **232 LOC total.**

### Dead module, mixed test file (needs surgical edit)

| Module | LOC | Test file with dead-only tests | Notes |
|---|---|---|---|
| `src/mathdevmcp/benchmark_manifest.py` | 25 | `test_frontier_industrialization.py` | drop one import + the one test fn that calls `benchmark_manifest`; keep the rest |
| `src/mathdevmcp/lean_export.py` | 153 | `test_lean_export.py` | drop the `export_lean_obligations` tests; keep the proof_audit / doctor / backend_env coverage |
| `src/mathdevmcp/semantic_alignment.py` | 65 | `test_industrial_release_gap_closure.py` | drop the `align_document_to_code` test fn |
| `src/mathdevmcp/shape_semantics.py` | 33 | `test_industrial_release_gap_closure.py` | drop the `analyze_shape_semantics` test fn |
| `src/mathdevmcp/leandojo_backend.py` | 337 | `test_remaining_release_gaps.py` + `test_proof_audit_v2.py` | drop `attempt_leandojo_tiny_theorem` callers; `leandojo_policy.py` is live and stays |

**613 LOC of source** plus a couple hundred LOC of test edits.

The largest single module is `leandojo_backend.py` (337 LOC) — a
substantial helper layer with structured readiness gates and traced-repo
metadata that was clearly built ahead of an integration that never
landed. The live surface uses `lean_check.py` for actual Lean
invocations.

## Importer counts (sorted ascending)

For context, the full importer count per module — modules at the top of
this list are the dead candidates, modules at the bottom are core
infrastructure:

```
  0  cli                      (entry point, invoked via `python -m`, not imported)
  1  benchmark_manifest       (test only)
  1  domain_formalization     (test only)
  1  lean_export              (test only)
  1  semantic_alignment       (test only)
  1  shape_semantics          (test only)
  1  symbolic_backend         (test only)
  2  leandojo_backend         (test only — both importers are tests)
  2  assumptions              → live via agent_workflows
  2  code_search              → live via cli
  2  corpus_roadmap           → live via industrial_review
  2  diagnostic_tests         → live via kalman_workflows
  2  industrial_review        → live via benchmarks
  2  leandojo_policy          → live via industrial_review
  2  leandojo_spike           → live via leandojo_policy
  2  operation_consistency    → live via agent_workflows
  2  performance              → live via cli
  2  release_evidence         → live via scripts/collect_release_evidence.sh
  2  review_packet            → live via kalman_workflows
  ...
 13  latex_index              (used by every workflow that touches a label)
 15  proof_audit              (used by proof_audit_v2 and the audit-derivation chain)
 50  contracts                (envelope shared by every tool result)
```

Modules at counts 3+ all have at least one live consumer in the
production chain (`cli` → workflow modules → primitives).

## Caveats

- **This is preexisting dead code, not caused by the simplification.**
  The slim MCP refactor only touched the surface layer; these modules
  were already test-only before that. The refactor just made the
  picture easier to see.
- **No `__all__`, no public-API docs, no scripts entry** for any of the
  7 modules. Nothing in the package treats them as a library surface
  for outside callers, so "deletable from the codebase" matches
  "deletable from the public contract."
- **`leandojo_backend.py` is the most surprising one.** It is a
  carefully-built helper that simply was never wired into a workflow.
  Worth a quick maintainer check before deletion in case it represents
  in-progress work.

## Suggested cleanup shape

Two natural follow-up PRs, each independently mergeable:

1. **Conservative cleanup** — delete the 2 cleanly-deletable pairs
   only (~232 LOC source + tests). Low risk, no test surgery,
   uncontroversial.

2. **Full sweep** — all 7 modules plus surgical test edits in three
   mixed-test files (~700+ LOC source plus ~250 LOC test edits).
   Larger change but completes the cleanup and brings the source tree
   into alignment with the simplification framing.

Both are scoped separately from the simplification refactor in
[`mcp-simplification.md`](mcp-simplification.md), which deliberately
left library code intact.
