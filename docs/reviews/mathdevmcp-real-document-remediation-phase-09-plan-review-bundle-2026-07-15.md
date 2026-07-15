# Phase 09 Final Red-Team Plan Review Bundle

Date: 2026-07-15
Review name: `mathdevmcp-phase09-final-red-team-plan`
Supervisor/executor: Codex
Reviewer: Claude Opus/max, read-only

## Role Boundary

Review only. Do not edit files, launch a backend/model/agent, approve
publication/default/release/source-edit authority, or act as execution
supervisor. Codex remains supervisor and executor.

## Objective

Determine whether the Phase 09 plan is internally consistent, feasible, and
sufficient to assign the final bounded remediation status without rerunning a
mathematical backend, trusting summary-only evidence, mutating accepted Phase
08 artifacts, repairing a discovered defect before classification, or
transferring scientific status into publication/release authority.

## Bounded Artifacts To Inspect

Primary plan sections:

- `docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-subplan-2026-07-15.md:7-186`
  for objective, entry, evidence/default/external-tool contracts, work packages,
  attacks, reconciliation, and status algorithm;
- the same file at lines `203-356` for commands, manifest, pre-mortem,
  skeptical audit, forbidden actions, handoff, and stops.

Predecessor/final-status comparators:

- `docs/plans/mathdevmcp-real-document-remediation-phase-08-aggregate-close-result-2026-07-15.md:7-123`;
- `docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md:1629-1670`;
- `docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md:63-121`.

Inspect only these implementation contracts as needed to assess feasibility:

- `scripts/run_p08c1_target_fidelity_replay.py:140-330,371-550`;
- `scripts/run_p08d_frozen_payload_replay.py:229-722,786-839`;
- `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0/code-snapshot/src/mathdevmcp/sympy_derivative_adapter.py:531-926`;
- `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0/p08b/capability-decision.json`;
- `.local/mathdevmcp/evidence/p08-20260714/p08d/20260714T174031Z-879741d6df52/decision.json`.

Do not inspect the whole repository or rerun commands.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can this plan reconstruct the accepted chain, test the registered attacks, reconcile the ledgers, and mechanically assign the correct bounded status without crossing authority boundaries? |
| Baseline | Literal accepted P08A/P08B/P08C/P08C1/P08D roots and decisions; old Phase 09 reports and superseded P08D runs are not comparators. |
| Primary criterion | Every material claim is tied to a reconstructable artifact or named adversarial check; historical/current code treatment is coherent; status conditions are exhaustive and non-overlapping in practice; publication remains disabled. |
| Veto findings | A planned command reruns a mathematical backend/document audit; summary fields can pass without raw reconstruction; predecessor artifacts can be mutated; expected code evolution is misclassified; a required master red-team case is absent; test/result repair can occur before classification; or safe status implicitly enables publication/default/release. |
| Explanatory only | Wording, clerical density, test count, and optional strengthening that does not affect the final status boundary. |
| Not concluded | Agreement is not Phase 09 execution evidence, proof, mission completion, publication authority, release readiness, or full-suite health. |

## Specific Review Questions

1. Is the split between P08A/P08B historical-snapshot reconstruction and
   P08C1/P08D current-reader replay scientifically and technically sound, or
   does it create an unchecked gap?
2. Can P08B be independently reconstructed from its preserved adapter,
   request, raw stdout/stderr, result, manifest, source projection, and decision
   without executing SymPy as a CAS? Is any material source/tool/result binding
   missing from the plan?
3. Does the P08D fresh temporary-root reconstruction plus predecessor
   before/after inventory prevent accepted-evidence mutation and exercise all
   public payload/resolver/privacy boundaries?
4. Does the adversarial matrix cover every master-plan red-team case, including
   unknown/legacy schema, path/symlink, stale source, truncation, repeated run,
   cursor omission/forgery, and gate tamper, with correct ledger treatment?
5. Is the full-suite failure classification principled enough to prevent both
   ignoring a relevant regression and allowing unrelated release debt to
   override the scoped evidence contract?
6. Is the final status algorithm faithful to the master plan, including the
   distinction between `UNSAFE`, `BLOCKED`, and capability incompleteness?
7. Do the no-repair-after-create and publication-disabled rules prevent the
   final audit from editing itself into a pass or turning a scientific status
   into experimental/publication authority?
8. Is there any other material correctness, feasibility, evidence, privacy, or
   claim-boundary defect that should block implementation?

## Known Residuals, Not Omissions

- P08B is `backend_checked`, never formal proof.
- Only two frozen documents and one qualifying candidate were exercised.
- The worst P08D resolver has a one-byte full-stdio margin.
- The earlier full suite reported 38 residual failures; the plan reruns and
  classifies them, but does not predeclare them as passing.
- `experimental_mode_available=false` is intentional under the academic
  governance reset; the final status does not decide publication.

## Required Output

Return concise file/line findings, ordered by materiality. End with exactly one
final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
