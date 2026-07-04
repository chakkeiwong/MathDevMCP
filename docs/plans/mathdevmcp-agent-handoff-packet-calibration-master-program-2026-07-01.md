# MathDevMCP Agent-Handoff Packet Calibration Master Program

Date: 2026-07-01

Status: `REVISED_AFTER_CLAUDE_R1`

## Program Objective

Measure whether the new human-framed review packets help a downstream AI agent
produce better next-step work than either task-only prompts or evidence-ledger
prompts without framing.

The calibration target is downstream work quality, not whether the packet reads
well to a human. Human readability remains a prerequisite, but the central
question is whether the packet reduces hallucinated claims, improves next-action
selection, preserves boundaries, and helps an agent produce a reviewable or
executable artifact.

This program measures local handoff usefulness only. It does not decide whether
the packet standard is generally optimal, whether a model is reliable, or
whether any mathematical result is true.

## Scope

Local/non-gating agent-handoff calibration over five frozen real-local
high-level workflow cases:

- `RLHLB-01-ift-sign-gap`;
- `RLHLB-03-joseph-equivalence`;
- `RLHLB-04-affine-pricing-recursion`;
- `RLHLB-06-state-space-code-missing-solve`;
- `RLHLB-09-affine-recovery-assumption-limit`.

Each case receives three prompt conditions:

- `A_task_only`: task question plus minimal source anchors;
- `B_evidence_only`: old-style status/evidence ledger without human framing;
- `C_human_framed`: current human-framed packet plus bounded machine ledger
  summary.

The three conditions must share the same task skeleton, requested output
sections, source-anchor policy, retry policy, and response length band.
Condition C may add human framing; condition B must include the same machine
evidence classes/status/gap/action ledgers available to C; condition A may not
include either ledger or framing beyond the task and bounded anchors.

## Role Contract

Codex is supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review compact
briefs, subplans, scoring rubrics, and result interpretations. Claude must not
execute phases, authorize boundary crossings, edit files, launch model runs, or
approve claims.

Downstream model-response collection is a calibration subject, not an execution
authority. If a phase would require new model/API usage beyond local prompt
fixture generation, it must stop for explicit approval unless the relevant
model-use path is already approved and documented in the phase subplan.

## Core Invariants

- Do not treat agent output as proof.
- Do not treat a single model run as calibrated reliability evidence.
- Do not claim release readiness, public benchmark validity, scientific
  validation, product capability, or broad theorem proving.
- Do not let a proxy score become a promotion criterion.
- Do not compare conditions unfairly by leaking framing into the baseline
  prompts.
- Do not let condition C receive extra non-framing evidence beyond condition B.
- Hard vetoes dominate all numeric or qualitative summaries.
- Do not let Claude act as worker, scorer authority, or boundary approver.
- Do not treat downstream agents as adjudicators of packet correctness.
- Preserve source/backend/probe/residual/non-claim ledgers separately.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | Freeze current packet artifacts, cases, and evaluation boundary. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-00-governance-baseline-subplan-2026-07-01.md` |
| 1 | Calibration Contract And Rubric | Define conditions, scoring rubric, hard vetoes, and evidence contract. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-01-contract-rubric-subplan-2026-07-01.md` |
| 2 | Prompt Fixture Generation | Generate local prompt fixtures and scoring templates for five cases x three conditions. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-02-prompt-fixtures-subplan-2026-07-01.md` |
| 3 | Response Collection Protocol | Define and, if approved, run bounded downstream-agent response collection. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-03-response-collection-subplan-2026-07-01.md` |
| 4 | Scoring And Analysis | Score responses, compare conditions, and classify failure modes. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-04-scoring-analysis-subplan-2026-07-01.md` |
| 5 | Contract Decision And Handoff | Decide whether to freeze, revise, or expand the packet handoff standard. | `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-05-contract-decision-handoff-subplan-2026-07-01.md` |

## Required Cross-Phase Artifacts

- Baseline packet artifact and final matrix paths from Phase 0.
- Calibration case list and frozen condition definitions from Phase 1.
- Rubric JSON or Markdown table with hard vetoes from Phase 1.
- Prompt fixture corpus from Phase 2.
- Response manifest from Phase 3, or a blocker result if model-use approval is
  required.
- Scored comparison table from Phase 4.
- Final decision/handoff note from Phase 5.
- Claude read-only review trail for material plan and scoring artifacts.
- Visible execution ledger and final stop handoff.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do human-framed packets improve downstream agent next-step work compared with task-only and evidence-only prompts? |
| Baseline/comparator | `A_task_only` and `B_evidence_only` prompt conditions generated from the same frozen cases. |
| Primary criterion | For at least the selected local cases, the framed-packet condition improves or preserves required dimensions: correct next action, boundary discipline, evidence use, assumption discipline, and overclaim avoidance, without hard-veto regressions. |
| Veto diagnostics | Prompt leakage between conditions; condition C gets more non-framing evidence than B; unequal task skeleton/output sections/length band/retry policy; scorer changes rubric after seeing outputs; single aggregate score hides hard vetoes; agent output treated as proof; Claude used as worker or authority; model-response phase runs without approval when required. |
| Explanatory diagnostics | Per-dimension scores, hard-veto counts, qualitative failure taxonomy, response length/context-use notes, Claude read-only review findings. `Artifact usefulness` and `context reuse` are explanatory unless correctness, boundary, assumption, and overclaim-veto criteria also pass. |
| Not concluded | General model reliability, release readiness, public benchmark validity, scientific validation, correctness of any mathematical claim, or proof that the packet standard is universally optimal. |
| Preserved artifacts | Master program, subplans/results, runbook, ledger, review trail, prompt fixtures, scoring rubric, response manifest, scored table, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Five representative cases | User discussion and prior packet review | Covers refutation, proof, abstention, code mismatch, and missing assumptions | Too small to generalize | Report as local/non-gating only | Baseline sample |
| Three prompt conditions | Calibration design | Separates task context, evidence ledger, and human framing effects | Leakage or unfair detail imbalance | Phase 1 prompt-equivalence checklist | Reviewed hypothesis |
| 0-2 or 0-3 rubric dimensions | Prior benchmark practice | Captures qualitative improvement without pretending precision | False numerical certainty | Hard vetoes and per-case notes | Convenience metric |
| Claude as reviewer only | User instruction | Independent critique without delegating execution | Claude output treated as authority | Review trail requires Codex assessment | Reviewed constraint |
| Visible runbook execution | Template constraint | Recoverable and auditable in current conversation | Slower than detached run | Ledger entries per phase | Reviewed default |

## Freeze And Fairness Requirements

Phase 0 must record:

- git commit or `git rev-parse HEAD` plus dirty-worktree summary;
- SHA256 hashes for the packet artifact, final matrix, and benchmark manifest;
- packet generator command and result summary;
- selected-case rationale and the fact that the cases were chosen before any
  response collection.

Phase 1/2 must enforce:

- identical task skeleton across A/B/C;
- identical requested output sections across A/B/C;
- identical response length band and retry/malformed-output policy;
- B and C share the same machine-evidence payload, while C additionally gets
  human framing;
- A gets only task and bounded source-anchor context;
- no prompt includes large raw source excerpts.

Phase 3 must stop with a blocker if model-use approval is missing. Without
approved response collection, the program must not proceed to partial scoring,
surrogate interpretation, or prompt tweaking based on imagined responses.

Phase 4 must surface hard-veto status before any per-dimension or aggregate
summary. A condition with hard-veto regressions cannot be declared improved by
soft dimensions such as artifact polish, response length, or context reuse.

Phase 5 final decisions are bounded:

- `freeze_local_standard_candidate`;
- `revise_packet_template`;
- `expand_calibration`;
- `blocked_no_model_use_approval`;
- `blocked_inconclusive_scoring`.

All decisions must restate non-claims.

## Repair Loop

- Each phase starts with a skeptical audit.
- If a material flaw is found, patch the active subplan or artifact visibly.
- Run focused local checks after each patch.
- Use Claude read-only review for material subplans/rubrics/results when safe.
- If Claude returns `VERDICT: REVISE`, patch the same artifact and retry up to
  five rounds for the same blocker.
- If Claude hangs, run a tiny probe. If the probe responds, redesign the prompt
  smaller. Claude silence is never approval.
- If the issue cannot converge after five rounds, write a blocker result and
  stop for human direction.

## Phase Completion Protocol

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans/results when available and
   safe;
6. advance only when exact handoff conditions are met.
