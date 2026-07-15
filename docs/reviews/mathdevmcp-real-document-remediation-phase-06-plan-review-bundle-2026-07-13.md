# Phase 06 Subplan Read-Only Review Bundle

Date: 2026-07-13

Review name: `mathdevmcp-phase-06-plan-review`

Supervisor/executor: Codex root agent

Reviewer: fresh local Codex read-only reviewer

## Role Boundary

Review only. Do not edit files, run mutating commands, launch agents, execute
Phase 06, invoke Sage/Lean or any other backend, inspect frozen documents, or
authorize publication/default/release changes. The root agent remains
supervisor and any later implementation worker.

Claude is not part of this review. The earlier external Claude route was
blocked before transmission by the external-data exfiltration policy, and no
retry or workaround is authorized.

## Objective

Decide whether the Phase 06 subplan is consistent, correct, feasible,
artifact-complete, and boundary-safe enough to begin synthetic implementation
in a later turn. The review does not authorize that implementation now.

## Primary Artifact

- `docs/plans/mathdevmcp-real-document-remediation-phase-06-failure-ledgers-ranking-action-selection-subplan-2026-07-13.md`

## Bounded Context

- `docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`
- `docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`, especially the `PromotionDecision`, exact invariants, and Phase 06 sections
- `docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md`
- `src/mathdevmcp/derivation_branch_controller.py`, ranking functions only
- `src/mathdevmcp/promotion_policy.py`
- `src/mathdevmcp/external_adapter_contract.py`, live-manifest verification and Phase 04 mapping only
- `src/mathdevmcp/document_derivation_tree.py`, publication constants, branch construction/ranking, proposal generation/validation only
- `src/mathdevmcp/derivation_search_tree.py`, Phase 04 branch schema only
- `src/mathdevmcp/derivation_search_orchestrator.py`, request/result and artifact output only

Do not inspect the whole repository unless a precise finding cannot otherwise
be verified.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the subplan repair current scalar ranking/mixed-ledger/promotion gaps without fabricating evidence, forcing incomparable branches, or prematurely exposing publication? |
| Baseline | Current numeric rank, Phase 01 quarantine-only promotion function, Phase 04 branch records, Phase 05 Sage-native manifest/verifier, and legacy document compiler. |
| Primary criterion | Work packages and tests are sufficient to establish typed ledger separation, semantic dedup, dominance/incomparability, discriminating actions, registered native-evidence normalization, and pure exact eligibility while product publication stays disabled. |
| Vetoes | Count/score compensation; ambiguous comparison; missing action/evidence bindings; R3 history reconstructed from missing records; synthetic/test-only evidence presented as real eligibility; cached booleans trusted; manifest schema impersonation; experimental mode exposed to document/CLI/MCP/server; circular P06 aggregate gate; missing stop/handoff conditions. |
| Explanatory only | Plan length, test count, number of work packages, or reviewer agreement. |
| Not concluded | No implementation correctness, mathematical result, real-document utility, publication authorization, default/release readiness, Phase 07 authority, or mission completion. |

## Review Questions

1. Is the partial-order contract mathematically and operationally precise enough
   to avoid hidden scalar compensation and false winners?
2. Are ledger classification and dedup scopes closed enough to prevent errors
   or duplicate volume from changing mathematical interpretation?
3. Does the discriminating-action contract name enough information to be
   executable later without claiming success in advance?
4. Is native specialist-evidence normalization feasible without converting
   Sage v3 into fake generic-v1 evidence or reconstructing missing R3 records?
5. Is the synthetic exact-eligibility fixture clearly separated from real
   execution authority and product publication?
6. Are all twelve master promotion invariant groups and the independent
   publication gate covered by explicit tests?
7. Does the plan preserve legacy compatibility and current publication
   quarantine while providing a feasible Phase 07 handoff?
8. Are required artifacts, checks, forbidden actions, handoff conditions, and
   stop conditions complete and mutually consistent?

## Required Output

Return findings first, ordered by severity, with exact file/section or current
code references. Treat style-only issues as non-blocking. State residual risks
if agreeing. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
