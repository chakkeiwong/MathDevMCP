# Read-Only Review Bundle: Substantive Document Derivation Plan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

## Objective

Review whether the new MathDevMCP master program correctly targets the generic
document-derivation regression: current reports preserve proof boundaries but
do not generate enough concrete mathematical evidence for useful repairs.

## Artifacts To Inspect

- Master program:
  `docs/plans/mathdevmcp-substantive-document-derivation-master-program-2026-07-08.md`
- Runbook:
  `docs/plans/mathdevmcp-substantive-document-derivation-visible-runbook-2026-07-08.md`
- Phase 00:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-governance-subplan-2026-07-08.md`
- Phase 01:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-semantic-obligation-subplan-2026-07-08.md`
- Phase 02:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-assumption-branch-subplan-2026-07-08.md`
- Phase 03:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-formalization-subplan-2026-07-08.md`
- Phase 04:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-report-regression-subplan-2026-07-08.md`

## Review Questions

Findings first.  Check:

- Does the plan avoid a card-NPV-specific fix?
- Does it address the actual regression upstream rather than weakening the
  renderer?
- Are semantic reconstruction, assumption branches, formalization stubs,
  external-tool evidence, and patch candidates sequenced in the right order?
- Are pass criteria concrete enough to fail hand-wavy reports?
- Is the frozen regression set specific enough to prevent cherry-picking?
- Do phase results require replayable manifests and decision tables?
- Do assumption branches record external-tool-first consideration evidence
  before in-house branch expansion?
- Are proof/certification boundaries preserved?
- Are stop conditions and evidence contracts sufficient?
- Does the visible runbook incorrectly authorize detached execution or Claude
  execution authority?

End with exactly:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
