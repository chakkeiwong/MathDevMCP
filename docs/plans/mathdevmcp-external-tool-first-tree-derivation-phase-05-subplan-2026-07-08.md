# MathDevMCP External-Tool-First Tree Derivation Phase 05 Subplan

Date: 2026-07-08

## Phase Objective

Implement branch-derived report rendering so derivation/search results become
agent-consumable repair reports instead of yes/no answers or fallback prose.
This phase should render a tree into Markdown and JSON-ready sections that show
location, problem, mathematical why, assumptions/routes, derivation evidence,
exact tools, proposed patch, and remaining blockers.

## Entry Conditions

- Phase 1/2 search-tree contract exists.
- Phase 3 adapter evidence wrappers exist.
- Phase 4 deterministic budgeted controller exists.
- The current worktree is dirty from prior lanes and must be preserved.
- Claude review is unavailable unless artifact export is explicitly approved.

## Required Artifacts

- `src/mathdevmcp/derivation_tree_report.py`
- `tests/test_derivation_tree_report.py`
- phase result note under `docs/plans`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP render tree evidence into a useful gap/proposal report without inventing fixes not present in the tree? |
| Baseline/comparator | Phase 4 returns a JSON tree but no human/agent report; prior audit reports could regress to hand-wavy prose. |
| Primary criterion | Renderer produces sections from tree evidence with location, problem, mathematical why, assumptions/routes, backend/tool evidence, proposed patches, blockers, non-claims, and exact tool ids/statuses. |
| Veto diagnostics | Renderer omits location/problem/why for a gap; claims a fix is proved without promotable evidence; fabricates assumptions or patch text not present in the tree; hides blockers or diagnostic-only evidence. |
| Explanatory diagnostics | Evidence counts, branch status, budget exhaustion, and missing-patch warnings. |
| Not concluded | No automatic document patch application, no full audit command integration, no proof of target document correctness, no public release readiness. |

## Required Checks

- `python3 -m pytest tests/test_derivation_tree_report.py tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_tree_report.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/derivation_search_tree.py`
- `git diff --check -- src/mathdevmcp/derivation_tree_report.py tests/test_derivation_tree_report.py docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-05-subplan-2026-07-08.md docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-05-result-2026-07-08.md`

## Required Reviews

- Local skeptical review after implementation.
- Fresh Codex read-only fallback review for boundary issues if time permits.

## Renderer Scope

Implement:

- `render_derivation_tree_report(tree)` returning a contract payload with
  structured sections and Markdown;
- explicit non-claim text from the tree;
- location rendering from `source_span` and patch candidate locations;
- exact tool ledger from backend attempts;
- blockers rendered as remaining evidence requirements;
- missing-patch warning when no patch candidate exists.

Defer:

- writing `.md` files from CLI/MCP;
- running the controller on full LaTeX documents;
- applying patches to documents;
- report quality benchmark integration.

## Forbidden Claims And Actions

- Do not fabricate patch candidates.
- Do not convert diagnostic evidence into proof.
- Do not hide blockers.
- Do not run long document experiments.
- Do not integrate into public release claims.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 when:

- renderer output includes the required fields for proof/refutation, partial,
  blocked, and budget-exhausted trees;
- tests enforce no fabricated patches and no hidden blockers;
- reports name exact tools and evidence ids;
- non-claims are preserved.

## Stop Conditions

Stop and write a blocker if:

- the tree contract lacks enough information to render location/problem/why;
- useful reports would require inventing assumptions or patches not present in
  evidence;
- tests cannot prevent diagnostic evidence from being described as proof.

## Skeptical Plan Audit

Wrong baseline: this is not a full document audit integration. It is the
renderer layer that later audit tools can consume.

Proxy metric: Markdown length is not quality. The pass criterion is required
fields grounded in tree evidence and blockers.

Hidden assumption: a proposed fix must come from a patch candidate or be
reported as missing, not synthesized by the renderer.

Environment mismatch: no external backend calls are required; tests use local
tree fixtures.

Audit result: proceed with a focused renderer and tests.
