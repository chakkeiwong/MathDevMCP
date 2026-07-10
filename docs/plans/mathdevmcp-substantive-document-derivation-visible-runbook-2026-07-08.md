# MathDevMCP Substantive Document Derivation Visible Runbook

Date: 2026-07-08

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook is based on the visible gated execution template.  It must not
launch a detached or nested agent.  It must not use `codex exec`,
`overnight_gated_launch.sh`, detached `tmux`, `nohup`, `setsid`, backgrounded
phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/mathdevmcp-substantive-document-derivation-master-program-2026-07-08.md`

Reviewed plan artifacts:

- `docs/reviews/mathdevmcp-substantive-document-derivation-plan-review-bundle-2026-07-08.md`

Execution ledger:

- `docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`

Stop handoff:

- `docs/plans/mathdevmcp-substantive-document-derivation-visible-stop-handoff-2026-07-08.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Gate | `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-governance-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-result-2026-07-08.md` |
| 1 | Semantic Obligation Reconstruction | `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-semantic-obligation-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-01-result-2026-07-08.md` |
| 2 | Assumption Branch Closure | `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-assumption-branch-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-result-2026-07-08.md` |
| 3 | Formalization Stub And Backend Attempt Integration | `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-formalization-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-result-2026-07-08.md` |
| 4 | Report Integration And Regression Gate | `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-report-regression-subplan-2026-07-08.md` | `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-result-2026-07-08.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic document derivation tool produce concrete mathematical repair evidence rather than generic fallback prose? |
| Baseline/comparator | Current `audit_document_derivation_tree` reports and existing external-tool-first tree lane. |
| Primary pass criterion | Phase 04 reports include source-local semantic obligations, branch-linked assumptions, derivation routes, backend/formalization evidence, patch candidates or precise blockers, and non-claims. |
| Veto diagnostics | Hand-wavy fixes, card-specific logic, row-fragment proof targets, route plans described as proofs, missing external-tool evidence. |
| Explanatory diagnostics | Backend absence, unsupported formalization, branch budget exhaustion, uncertain source extraction. |
| Not concluded | Whole-document proof, global assumption minimality, release readiness, or theorem-prover completeness. |
| Artifacts | Phase results, logs, review bundles, tests, generated reports. |

## Frozen Regression Set

The Phase 04 gate must use these labels and baseline artifacts:

| Case | File | Labels | Baseline artifact |
| --- | --- | --- | --- |
| Risky debt pricing and FOC | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `eq:risky-pricing`, `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | `docs/reviews/risky-debt-derivation-gap-proposals-v2.md` |
| Credit-card NPV valuation | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | `docs/reviews/credit-card-npv-generic-document-derivation-tree-smoke-2026-07-08.md` |

Exploratory labels may be added, but they cannot replace the frozen regression
set in the pass/fail decision.

## Phase Result Manifest

Each phase result must record:

- git commit or `git diff` state summary;
- command(s) actually run;
- Python/backend environment when applicable;
- wall time or `N/A`;
- artifact paths;
- pass/veto status;
- decision table with decision, primary criterion status, veto diagnostic
  status, main uncertainty, next justified action, and non-claims.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Visible execution | Template boundary | Recoverable and inspectable in current conversation | User expected detached overnight execution | Runbook states no detached launch | Reviewed default |
| Focused Phase 01 implementation first | Regression diagnosis | Renderer cannot fix missing upstream evidence | Upstream packet still too generic | Tests assert full display and inventories | Hypothesis |
| Existing tests as regression base | Current repo | Keeps blast radius narrow | Tests pass while report remains weak | Add quality assertions, not field-only assertions | Reviewed default |

## Skeptical Plan Audit

Before each phase, Codex must record a skeptical audit in this ledger checking:

- wrong baselines;
- proxy metrics being treated as pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material flaw appears, patch the subplan or write a blocker before
running implementation.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run the smallest implementation or diagnostic that
   answers the phase question.
3. `ASSESS_GATE`: compare outputs against pass/veto criteria, write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material gates when
   available.
5. `REPAIR_LOOP`: patch fixable issues, rerun focused checks, stop after five
   Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes.

## Anticipated Approval Needs

- Claude review gate command:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh ...`
- No package installation is anticipated for Phase 00 or Phase 01.
- No network fetch, detached launch, destructive git operation, or long backend
  search is anticipated in the first execution slice.

## Human-Required Stop Conditions

Stop if continuing would require:

- package installation, network fetch, credentials, or new environment setup;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- modifying unrelated dirty user work;
- treating Claude as execution authority;
- continuing after five nonconvergent review rounds.
