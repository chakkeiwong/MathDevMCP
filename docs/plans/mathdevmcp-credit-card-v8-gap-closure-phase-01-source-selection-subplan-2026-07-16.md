# Phase 01 Subplan: Exact Source Selection

## Phase Objective

Make assumption and derivation report APIs select the same exact
file/digest/label obligation already used by source-bound proof workflows.

## Entry Conditions Inherited From Previous Phase

- Frozen v8 digest matches the master program.
- Duplicate-label directory behavior is reproduced: unqualified labels are
  ambiguous and current assumption/derivation reports inspect zero targets.
- Existing untracked v8 audit artifacts are preserved.

## Required Artifacts

- Core, CLI, facade, FastMCP/server schema changes for `file` and
  `source_digest` selectors.
- Exact/ambiguous/stale/absent selection regressions. Unsupported relation
  shapes may remain target-extraction gaps until Phase 03, but must retain exact
  source binding and must not be reported as absent.
- `mathdevmcp-credit-card-v8-gap-closure-phase-01-result-2026-07-16.md`.

## Required Checks

- Focused assumption/derivation, facade, CLI, server, and schema tests.
- Duplicate-corpus order tests.
- Exact target/obligation digest comparison against source-bound proof input.
- `git diff --check` and compile checks for edited Python.

## Evidence Contract

- Pass: all nine exact v8 labels are source-bound; currently supported targets
  are inspected; unsupported relation shapes are exact-bound typed coverage
  gaps rather than absence; unqualified duplicates return `ambiguous_label`;
  stale digest returns `source_digest_mismatch`; absent labels return
  `label_absent`; no sibling is silently selected.
- Veto: a selector is accepted by one public surface but omitted by another.
- Non-claim: successful selection is not mathematical validation.

## Forbidden Claims And Actions

- Do not weaken unqualified duplicate handling.
- Do not select by filename alone when a supplied digest mismatches.
- Do not edit source documents.

## Exact Next-Phase Handoff Conditions

Phase 02 may start when source selection is exact and identical across public
surfaces, no selected v8 label is called absent, and relation-shape gaps are
explicitly handed to Phase 03 rather than hidden.

## Stop Conditions

Stop on source drift, selector ambiguity that cannot fail closed, or a required
breaking API change with no compatibility path.
