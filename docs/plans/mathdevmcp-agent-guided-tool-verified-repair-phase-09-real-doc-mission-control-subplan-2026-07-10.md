# Phase 09 Subplan: Real-Document Regression And Mission Control

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_08`

## Phase Objective

Apply the strict workflow to the frozen real documents, compare against the
baseline reports, and update mission-control policy to prevent future
regressions.

## Entry Conditions Inherited From Previous Phase

- Strict workflow is implemented and exposed.
- Optional parallelism is either validated or explicitly disabled.

## Required Artifacts

- Frozen card-NPV strict report JSON/Markdown.
- Frozen risky-debt strict report JSON/Markdown.
- Comparison note against Phase 06 baseline.
- Mission-control or policy update encoding:
  agent proposes, tree verifies, reports publish evidence only.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Focused real-document report generation.
- Report content assertions:
  location, problem, mathematical why, proposed fix or exact gap, evidence
  refs, remaining blockers, tool-use ledger.
- Relevant test suite subset.
- `git diff --check`.
- Final read-only review of evidence claims and mission-control policy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the strict workflow improve honesty and usefulness on the real card-NPV and risky-debt documents? |
| Baseline/comparator | Phase 06 frozen reports. |
| Primary criterion | Reports separate closed repairs, partial repairs, refutations, and blocked gap reports; no diagnostic-only branch is rendered as a fix. |
| Veto diagnostics | Same handwavy proposal regression; missing exact blocker; no tool-use ledger; unsupported improvement claim; final policy omits agent/tree/backend role split. |
| Explanatory diagnostics | Fewer final repairs may appear because blocked items are now honest gap reports. |
| Not concluded | No document is claimed publication-ready or fully mathematically verified. |
| Artifact | Frozen reports, comparison note, mission-control update, Phase 09 result. |

## Forbidden Claims Or Actions

- Do not edit the target scientific documents as part of this generic tool
  lane.
- Do not claim the generated fixes are sufficient for publication.
- Do not hide blocked branches to make the report look stronger.

## Exact Next-Phase Handoff Conditions

This is the closeout phase.  Mark the runbook complete only if final artifacts,
tests, review trail, non-claims, and remaining blockers are recorded.

## Stop Conditions

Stop if real-document runs expose a generic workflow defect that must be fixed
before policy closeout.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 09 result / close record.
3. Write or refresh the visible stop handoff.
4. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
