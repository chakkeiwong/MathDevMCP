# Phase 01 Subplan: Semantic Obligation Reconstruction

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Add a generic Python contract that reconstructs complete labeled LaTeX display
environments and turns them into semantic obligation packets rich enough for
assumption branching and backend routing.

## Entry Conditions Inherited From Previous Phase

- Phase 00 plan/review gate has passed or has a documented bounded fallback.
- Existing row-local extraction is known to be insufficient for multiline
  alignments and hard document repair.
- Renderer boundaries remain in force: no invented patches.

## Required Artifacts

- A source reconstruction helper, preferably within
  `src/mathdevmcp/document_derivation_tree.py` unless extraction complexity
  warrants a new module.
- Packet fields for:
  - full display source;
  - display line span;
  - label row count;
  - target row and grouped target;
  - operator inventory;
  - symbol inventory;
  - lhs/rhs candidates;
  - source-local blockers.
- Focused tests in `tests/test_document_derivation_tree.py`.
- Phase result:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-result-2026-07-08.md`
- Phase result must include a run manifest and decision table as specified in
  the master program.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py`
- `git diff --check`
- Read-only review of Phase 01 result if runtime behavior materially changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the document workflow stop auditing row fragments and preserve complete local proof targets? |
| Baseline/comparator | Current locator row packets with `label_row_count` blocker but no full display source packet. |
| Primary criterion | A multiline label packet includes full display text, display span, grouped source target, row target, operators, and symbol inventory. |
| Veto diagnostics | Full display missing; label line span wrong; packet drops row-level provenance; source uncertainty hidden. |
| Explanatory diagnostics | Macros not expanded, alignment markers preserved, ambiguous lhs/rhs. |
| Not concluded | No proof or patch-quality claim from reconstruction alone. |
| Artifact | Tests and Phase 01 result note. |

## Forbidden Claims Or Actions

- Do not claim semantic packets prove the target.
- Do not rewrite the equation locator globally unless a focused helper is
  insufficient.
- Do not introduce card-specific parsing.

## Exact Next-Phase Handoff Conditions

Advance to Phase 02 only if:

- tests prove grouped display reconstruction works on a generic multiline
  fixture;
- semantic packets expose enough symbol/operator data for branch instantiation;
- no proof boundary was weakened.

## Stop Conditions

Stop if:

- source reconstruction needs a full LaTeX parser or external package not
  already available;
- line-span reconstruction is unreliable enough that patch locations would be
  misleading;
- tests show existing locator behavior regresses.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write the Phase 01 result / close record.
3. Draft or refresh Phase 02 subplan.
4. Review Phase 02 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
