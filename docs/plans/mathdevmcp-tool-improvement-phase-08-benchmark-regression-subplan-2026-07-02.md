# Phase 8 Subplan: Benchmark-Guided Regression Closeout

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE_7`

## Phase Objective

Close the implementation program by running focused workflow regressions and
recording how the improved tools address the repaired downstream benchmark
signals.

## Entry Conditions

- Phases 1 through 7 passed or have bounded review-gate notes.
- No benchmark baseline artifacts were mutated.
- Improved workflows are exposed through relevant local surfaces.
- Phase 7 repaired the seeded high-level workflow oracle to align with the
  already-approved diagnostic `review_packet` route-plan companion on
  `derive_from` outputs.

## Required Artifacts

- Tool-level regression note mapping improvements to benchmark cases.
- Final result record.
- Updated stop handoff.
- Optional focused benchmark-quality report if local commands support it.

## Required Checks/Tests/Reviews

- High-level workflow tests touched by all phases.
- MCP/server checks touched by Phase 7.
- JSON/prompt-contract checks for downstream benchmark artifacts.
- `git diff --check` over touched files.
- Claude read-only final review when available.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What bounded tool-improvement evidence is justified after the implementation phases? |
| Baseline/comparator | Current repaired benchmark result and pre-program high-level workflow behavior. |
| Primary criterion | Focused tests pass, benchmark mapping is written, and claims remain local/diagnostic. |
| Veto diagnostics | C-over-B promotion from tool tests; benchmark mutation; aggregate-only claim; unsupported release/product/scientific/general-reliability claim. |
| Explanatory diagnostics | Test pass/fail table, benchmark-case mapping, residual gap ledger. |
| Not concluded | No public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, or general model reliability. |

## Skeptical Plan Audit

- Wrong baseline risk: compare against the repaired local seeded benchmark and
  the repaired downstream-agent benchmark diagnostics, not against public or
  external benchmark claims.
- Proxy metric risk: 70/70 local seeded tests and downstream-agent packet
  diagnostics are regression evidence only; they do not prove mathematical
  correctness or agent reliability.
- Hidden assumption risk: the Phase 7 oracle repair could be mistaken for
  benchmark tuning. The closeout must state that it aligns the oracle with the
  pre-existing Phase 4 diagnostic route-plan artifact and does not loosen
  certifying evidence requirements.
- Environment mismatch risk: Phase 8 should run local focused checks and
  reports only; it must not collect new downstream-agent responses or mutate
  frozen benchmark artifacts without explicit approval.
- Artifact-answer fit: final artifacts must answer what changed, what passed,
  what benchmark gaps are addressed, and what remains non-claimed.

Audit result: `READY_FOR_PHASE_8_EXECUTION`.

## Forbidden Claims/Actions

- Do not rerun downstream response collection without explicit approval.
- Do not claim benchmark promotion from unit tests.
- Do not overwrite repaired benchmark artifacts.
- Do not represent the Phase 7 oracle alignment as improved model/agent
  performance.

## Exact Next-Phase Handoff Conditions

This is the final phase. Handoff must state final status, artifacts, checks
actually run, unresolved blockers, and next safe human decision.

## Stop Conditions

Stop if regression checks fail, if benchmark artifacts are accidentally
modified, or if final claims would exceed local implementation evidence.
