# Phase 6 Subplan: Regression And Promotion Decision

Date: 2026-07-01

Status: `REFRESHED_AFTER_PHASE_5_REPAIRED_CANDIDATE`

## Phase Objective

Run final regression checks and make a bounded decision: promote to a stronger
internal downstream-agent usefulness gate, keep the current local candidate,
revise/expand the benchmark, or stop with a blocker.

After Phase 5, promotion is not available for this runbook because the only
collected A baseline is contaminated by fixture leakage. The expected bounded
decision is to close with benchmark repair completed and repaired-prompt
response collection requiring explicit human approval.

## Entry Conditions Inherited From Previous Phase

- Phase 5 result exists.
- Repairs, deferrals, and residual limitations are recorded.
- Required local checks for touched surfaces are known.
- No pass/fail criteria were changed after response scoring.
- Repaired candidate prompts validate, but no repaired-prompt response
  collection has been approved or run.

## Required Artifacts

- Phase 6 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-result-2026-07-01.md`.
- Final usefulness summary:
  `.mathdevmcp/downstream_agent_usefulness/final_summary.json` or markdown
  equivalent.
- Final test output summaries.
- Final Claude review entry.
- Updated visible ledger and stop handoff.

## Required Checks, Tests, Reviews

- Focused pytest for all touched high-level workflow, packet, benchmark, and
  scoring modules.
- Focused prompt-contract validation for current and repaired candidate
  manifests.
- Existing high-level workflow quality or benchmark gates only if Phase 6
  touches those surfaces.
- Manifest/schema validations for benchmark artifacts.
- Forbidden-claim grep over touched docs/results.
- Claude read-only review of final decision brief.
- Codex skeptical audit before final decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What bounded downstream-agent usefulness decision is justified by the produced artifacts? |
| Baseline/comparator | Phase 0 baseline, Phase 1 rubric, Phase 4 scored results, and Phase 5 repaired candidate prompts. |
| Primary criterion | Final decision matches actual artifacts, preserves the A-leakage hard veto and non-claims, and records that repaired-prompt response collection needs approval. |
| Veto diagnostics | Claim exceeds evidence; aggregate score overrides hard veto; response sample treated as general reliability; release/public/scientific/product claim; undocumented test failure; Claude treated as authority; repaired candidate treated as scored evidence. |
| Explanatory diagnostics | Final score summaries, failure taxonomy, repair/test summaries, prompt-contract validation, review trail. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, product capability, broad theorem proving, general model reliability, or C-over-B superiority. |

## Forbidden Claims Or Actions

- Do not claim general downstream-agent reliability from a local diagnostic
  sample.
- Do not claim mathematical truth beyond backend-certified scoped obligations.
- Do not promote if hard vetoes or artifact gaps remain unresolved.
- Do not change scoring criteria to obtain a pass.
- Do not treat repaired candidate prompts as response evidence.
- Do not collect repaired-prompt responses without explicit human approval.

## Exact Next-Phase Handoff Conditions

This is the final phase. Close the program only if:

- Phase 6 result exists;
- final artifacts and checks are listed;
- unresolved blockers and non-claims are explicit;
- safest next human decision is stated.

## Stop Conditions

Stop if:

- final checks fail and cannot be repaired within scope;
- evidence does not support any bounded decision except blocker or
  recollection-needed;
- Claude/Codex final review does not converge within five rounds;
- continuing would require new response collection, package/network access,
  or project-direction approval.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 6 result or blocker record;
3. update the visible ledger and stop handoff;
4. review the final decision for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
