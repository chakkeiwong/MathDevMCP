# Phase 01 Subplan: Proposition And Context Packet Extraction

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Make proposition labels first-class high-level targets by producing a context
packet for labels such as `prop:interior-foc`.

## Entry Conditions Inherited From Previous Phase

- Phase 00 review gate passed or has documented fallback review agreement.
- Existing `derivation_target_extraction.py` can extract equation rows inside
  proposition blocks.
- Current document-derivation report records proposition labels as missing
  focus labels when they are not display-equation labels.

## Required Artifacts

- A Python contract for proposition/context packets, reusing existing
  derivation target extraction where possible.
- Integration path from `audit_document_derivation_tree` or a helper module to
  include proposition-level packets.
- Tests showing `prop:interior-foc` produces a packet with proposition source,
  equation targets, statement context, and proof/context snippet.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-01-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py`
- `git diff --check`
- Read-only review if the public report contract changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can proposition labels produce context packets rather than missing-focus entries? |
| Baseline/comparator | Current Phase 04 risky-debt report with `prop:interior-foc` in `missing_focus_labels`. |
| Primary criterion | `prop:interior-foc` yields proposition source, equation targets `eq:foc-k`/`eq:foc-b`, hypotheses/proof context, and non-proof boundary. |
| Veto diagnostics | Proposition label still only missing; equation rows detached from parent proposition; proof context silently omitted; parser uncertainty hidden. |
| Explanatory diagnostics | Proposition without display equations; nested environment ambiguity; macro uncertainty. |
| Not concluded | Context extraction is not proof or repair. |
| Artifact | Tests and Phase 01 result. |

## Forbidden Claims Or Actions

- Do not claim proposition context proves the FOC.
- Do not rewrite the global LaTeX index unless necessary.
- Do not add card-specific or risky-debt-specific parsing.

## Exact Next-Phase Handoff Conditions

Advance to Phase 02 only if proposition packets expose enough local context to
distinguish stated assumptions from missing assumptions.

## Stop Conditions

Stop if proposition extraction requires a new parser package or line spans
would be misleading.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 01 result / close record.
3. Draft or refresh Phase 02 subplan.
4. Review Phase 02 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
