# Phase 2 Subplan: Case Corpus And Fixture Design

Date: 2026-07-01

Status: `READY_FOR_PHASE_2_EXECUTION`

## Phase Objective

Create or refine a governed local case corpus for downstream-agent usefulness
measurement, covering the high-level workflow types and preserving source,
evidence, and copyright/privacy boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 1 contract and rubric are frozen.
- Source/evidence boundaries are explicit.
- Response collection has not started.

## Required Artifacts

- Phase 2 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-result-2026-07-01.md`.
- Case manifest draft, preferably:
  `.mathdevmcp/downstream_agent_usefulness/case_manifest.json`.
- Per-case evidence-class matrix.
- Source-boundary note documenting whether cases come from current repo,
  neighboring local repos, existing benchmark artifacts, or synthetic variants.
- Updated ledger and stop handoff if execution stops.

## Required Checks, Tests, Reviews

- JSON/schema validation for case manifest if written.
- Coverage check across workflow families.
- Source-boundary grep/review for excessive copied text from neighboring repos.
- Claude read-only review for material case-corpus design.
- Local skeptical audit for overfitting, unfair comparisons, and missing stop
  conditions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which governed local cases can fairly test downstream-agent usefulness across high-level workflows? |
| Baseline/comparator | Existing real-local benchmark cases and any new bounded cases derived from local repo summaries. |
| Primary criterion | Case manifest covers multiple workflow families, records evidence class, expected task, source boundary, and scoring applicability. |
| Veto diagnostics | Copying substantial external/local repo text without boundary; cases selected after seeing model responses; expected answers missing; all cases from one workflow; unsupported mathematical claims. |
| Explanatory diagnostics | Coverage table, evidence-class matrix, source-provenance summaries, excluded-case list. |
| Not concluded | No response quality, no benchmark validity beyond local governed use, no scientific validation. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not copy substantial neighboring-repo text into fixtures when a bounded
  summary and provenance is enough.
- Do not label diagnostic expected answers as certified proofs.
- Do not alter the frozen Phase 1 rubric to fit cases.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- case manifest is present or a precise blocker explains why not;
- every case has workflow family, evidence class, expected output type, source
  boundary, and scoring applicability;
- the Phase 3 prompt-harness subplan is reviewed for frozen-prompt discipline,
  no-hidden-retry policy, and approval boundary.

## Stop Conditions

Stop if:

- source boundaries cannot be maintained;
- expected answers cannot be stated with acceptable evidence classes;
- the only feasible corpus would be too narrow to test the stated question;
- human approval is needed for neighboring-repo content use and has not been
  granted.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 2 result/close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
