# Phase 06 Result: Maintainability, Review, And Closeout

Date: 2026-07-22

Status: complete with explicit remaining gaps

## Delivered

- A general applied-math audit orchestrator:
  `audit_applied_math_document`.
- Library, CLI, facade, and experimental all-profile MCP surfaces.
- PDF/TeX/code/data source records with SHA-256 identity.
- ResearchAssistant PDF transport with detailed internal evidence and compact
  public output.
- Twelve discipline-neutral obligation families and exact disposition coverage.
- Optional DynareMCP routing for `.mod` inputs; non-Dynare inputs are explicitly
  `not_applicable`.
- High-signal literal source detectors for arithmetic mismatch, external
  specification dependence, zero-steady/log boundaries, and uncertainty
  terminology conflicts.
- Cross-domain fixtures for finance, marketing, and management-style inputs.
- Phase plans, close records, and benchmark/evidence boundaries.

## Verification

- Focused final slice: `66 passed`.
- Stable MCP stdio smoke: passed, 23 tools.
- All-profile MCP stdio smoke: passed, 70 tools.
- Cross-domain smoke: finance, marketing, and management obligation families
  selected as expected.
- Real Boehl PDF smoke: 12/12 obligation families selected; 4 source-supported
  findings; 8 explicit `not_checkable` dispositions; artifact size 269,316 bytes
  after the arithmetic-evidence formatting fix.
- `python -m compileall -q src tests`: passed.
- `git diff --check`: passed.

The broad repository run completed with `1,789 passed, 4 skipped, 5 failed`.
The five failures were not all new regressions: four are expected clean-release
policy failures caused by this uncommitted worktree. The remaining compact
packet parity failure is an existing environment-provenance mismatch between
in-process and CLI runs (`CUDA_VISIBLE_DEVICES` differs), reproduced in
isolation and outside the orchestrator code. It must not be hidden by removing
provenance; it remains a release-worktree gap.

## Scientific/Product Verdict

The program successfully creates one usable LLM-facing entry point and improves
evidence routing and obligation coverage. It does not yet achieve autonomous
mathematical-error discovery for arbitrary PDF papers. The new Boehl smoke found
literal source problems but did not reproduce the equation-pair C.75/C.77/C.79
reasoning automatically.

## Remaining Gaps

1. PDF equations are not normalized into reliable equation objects.
2. Cross-equation relation discovery is not implemented; C.47/C.79-style
   comparisons remain `not_checkable` without agent formalization.
3. No general code/data execution or equivalence checking is performed by the
   orchestrator; specialist routes are recorded but not yet invoked.
4. Causal identification, likelihood, posterior, algorithm convergence, and
   empirical estimand validators are obligation categories, not complete
   method-specific checkers.
5. ResearchAssistant source-package/code discovery is not automatically wired
   into this function; the current PDF bridge remains the default for PDFs.
6. The existing CLI/facade compact-packet environment-provenance parity issue
   remains open, as do clean-release gates for the uncommitted worktree.

These are continuation items, not reasons to misclassify the completed
engineering work as a scientific failure.
