# MathDevMCP Real-Task Master Phase 10 Subplan: Release-Policy Integration

## Phase Objective

If and only if Phase 9 nominates a reviewed narrow gate-candidate subset with
human approval, define a release/product policy integration that preserves
explicit non-claims and blocks unstable or poorly interpreted benchmark slices.

## Entry Conditions Inherited From Previous Phase

- Phase 9 produced a reviewed gate-candidate shortlist.
- Human approval exists for policy-design work.
- No subset may be integrated unless it is stable, narrow, and evidence-bounded.

## Required Artifacts

- Phase 9 gate-candidate result
- `docs/mathdevmcp-release-policy.md` if policy edits are explicitly approved
- `src/mathdevmcp/public_release.py` and release-policy tests if policy surfaces
  are explicitly approved
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-10-release-policy-result-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - No policy edits: rerun Phase 9 checks and write a blocked/not-authorized
    close record.
  - With explicit approval and edits: add focused release-policy tests and run
    all affected policy/benchmark tests.
- Review:
  - Codex self-review required.
  - Claude read-only review required for any release-policy proposal.
  - Human approval required before policy edits or gate activation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a narrow reviewed real-task subset be integrated into release/product policy without overclaiming? |
| Baseline/comparator | Phase 9 shortlist, existing release policy, current benchmark acceptance assessment. |
| Primary pass criterion | Policy integration, if any, is narrow, tested, explicit about non-claims, and approved by a human. |
| Veto diagnostics | Unstable subset becomes blocking, benchmark pass implies proof/release/science, private/local evidence leaks into public policy. |
| Explanatory diagnostics | Policy wording, test coverage, known caveats. |
| Not concluded | Broad benchmark completion, scientific validation, general real-task readiness. |
| Artifacts | Phase result, policy diff if approved, final handoff. |

## Forbidden Claims And Actions

- Do not edit release policy without explicit human approval.
- Do not activate real-task benchmark gating by default.
- Do not make benchmark pass imply mathematical proof, posterior validity,
  convergence, GPU readiness, or scientific validity.

## Exact Next-Phase Handoff Conditions

There is no next execution phase after Phase 10. The handoff is the final
visible program completion or blocker handoff.

The master program is complete only if:

- every prior phase result exists;
- Phase 9 either stopped with no candidate or produced a reviewed, approved
  candidate;
- any Phase 10 policy integration is narrow, tested, reviewed, and human
  approved;
- final handoff records tests run, non-claims, and unresolved blockers.

## Stop Conditions

- Stop immediately if human approval for policy edits is absent.
- Stop if release-policy wording would exceed the evidence contract.
- Stop if tests fail or if Claude/Codex do not converge after five repair
  rounds on the same blocker.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Write final visible handoff.
4. Review final handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
