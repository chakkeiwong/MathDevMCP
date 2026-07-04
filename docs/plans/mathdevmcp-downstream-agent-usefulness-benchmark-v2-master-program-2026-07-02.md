# Downstream-Agent Usefulness Benchmark V2 Master Program

Date: 2026-07-02

Status: `LAUNCHED_VISIBLE_GATED_EXECUTION_WITH_CLAUDE_PROBE_UNAVAILABLE`

## Program Objective

Create a harder local v2 candidate for the downstream-agent usefulness
benchmark that better discriminates between:

- `B_evidence_only`: compact machine-evidence or evidence-packet prompts; and
- `C_human_framed`: self-contained human-framed agent-handoff prompts.

The v2 benchmark is a measuring-instrument maintenance effort. It must not
change tool implementation, mutate the repaired baseline, collect new response
worker outputs, or claim C-over-B superiority before a separately approved
collection and scoring run.

## Starting Point

The current repaired benchmark is frozen as the baseline local diagnostic:

- repaired responses collected: 27/27;
- response subject: Codex subagents;
- retry policy: one attempt per prompt, no hidden retries;
- Claude role: read-only reviewer only;
- hard vetoes: A = 0, B = 0, C = 0;
- required passes: A = 8/9, B = 9/9, C = 9/9;
- repaired A/B/C comparison: valid local diagnostic;
- C-over-B promotion: not supported because C ties B under frozen required
  dimensions.

Primary repaired artifacts remain under
`.mathdevmcp/downstream_agent_usefulness/` and must not be edited by this v2
maintenance lane.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review compact
briefs, subplans, result summaries, validation summaries, and boundary wording.
Claude must not edit files, run commands, launch agents, collect responses,
score as final authority, approve boundary crossings, or authorize scientific,
product, release, funding, runtime, model-file, or benchmark-validity claims.

Downstream response workers are out of scope for this program. New response
collection requires explicit human approval after v2 candidate artifacts are
frozen.

## Claude Review Availability

The user requested Claude read-only review until convergence or five rounds for
the same blocker. A tiny read-only Claude probe was launched with the narrow
worker wrapper:

`bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name mathdevmcp-v2-review-probe --model opus --effort max ...`

The probe produced no output after about two minutes and was interrupted.
`claude --version` returned `2.1.148 (Claude Code)`, so the binary is present,
but the small review prompt did not complete. This is recorded as reviewer
unavailable, not as approval. Material phase subplans and results should still
attempt compact Claude review when feasible; if Claude remains silent, Codex
must record that fact and proceed only across boundaries already authorized by
this master program and the user.

## Human Approval Boundaries

This program is approved to:

- inspect local repo artifacts;
- create v2 benchmark-maintenance plans and candidate artifacts under separate
  paths;
- run local JSON, prompt-contract, hash, grep, diff, and focused pytest checks;
- call Claude through the narrow read-only wrapper for review.

This program must stop for explicit human approval before:

- collecting new downstream-agent or model responses;
- using Claude as a response worker;
- installing packages, fetching network data, changing credentials, changing
  model files, or using paid model/API surfaces beyond read-only Claude review;
- modifying the frozen repaired baseline artifacts under
  `.mathdevmcp/downstream_agent_usefulness/`;
- mutating the frozen scoring rubric and calling old scores comparable;
- copying substantial private or neighboring-repo source excerpts into prompt
  fixtures instead of bounded summaries;
- changing release/default benchmark policy;
- making public benchmark, scientific, product, release, funding, or general
  model-reliability claims.

## Core Invariants

- Preserve the repaired benchmark as the current baseline.
- Keep v2 candidate artifacts under `.mathdevmcp/downstream_agent_usefulness_v2/`.
- Keep benchmark maintenance separate from tool implementation.
- Freeze cases before prompt variants.
- Freeze prompt variants before any future response collection.
- Score hard-veto-first under a predeclared rubric or applicability map.
- Treat prompt validity, fixture quality, and Claude agreement as diagnostics,
  not task-success evidence.
- Do not tune v2 cases to parallel implementation branches.
- Do not hide malformed artifacts; record blockers visibly.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Freeze | Freeze baseline hashes, boundaries, v2 paths, and execution state before creating candidate cases. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-00-governance-baseline-subplan-2026-07-02.md` |
| 1 | Ceiling-Effect And Difficulty Requirements | Analyze repaired ceiling effects and convert them into v2 case requirements without using new model outputs. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-subplan-2026-07-02.md` |
| 2 | Case Manifest Candidate | Create the v2 case manifest and evidence/scoring applicability maps under the v2 artifact root. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-subplan-2026-07-02.md` |
| 3 | Prompt Fixtures And Contract Validation | Generate A/B/C prompt fixtures, prompt manifest hashes, and prompt-contract validation report. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-subplan-2026-07-02.md` |
| 4 | Adversarial Analysis And Collection Runbook | Write ceiling/adversarial analysis and a future collection runbook that stops before collection approval. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-subplan-2026-07-02.md` |
| 5 | Candidate Close And Handoff | Run final checks, write result note, and stop with exact approval requirements for future collection. | `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-subplan-2026-07-02.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a harder local benchmark candidate discriminate between compact machine-evidence prompts and richer human-framed handoff prompts without post-hoc scoring drift or answer leakage? |
| Baseline/comparator | Frozen repaired benchmark artifacts under `.mathdevmcp/downstream_agent_usefulness/`; v2 candidate artifacts under `.mathdevmcp/downstream_agent_usefulness_v2/`. |
| Primary pass criterion | v2 candidate artifacts exist, validate locally, preserve governance boundaries, avoid A leakage and B/C answer leakage, include plausible B/C discrimination cases on predeclared dimensions, and stop before response collection. |
| Veto diagnostics | Repaired baseline mutation; response collection without explicit approval; Claude as response worker; hidden retries; cases selected after new responses; rubric drift after responses; prompt polish scored as task success; substantial private excerpts; unsupported C-over-B, release, public, scientific, product, or general-reliability claims. |
| Explanatory diagnostics | Ceiling-effect inventory, difficulty tags, evidence-class coverage, scoring applicability map, prompt-contract validation, adversarial leakage analysis, local checks, Claude read-only reviews if available. |
| Not concluded | No tool improvement, no model reliability, no release readiness, no public benchmark validity, no scientific validation, no product capability, no C-over-B superiority before future scored responses. |
| Artifacts | Master program, visible runbook, execution ledger, Claude review trail, phase subplans/results, v2 JSON manifests, v2 prompt fixtures, validation report, analysis, runbook, result note, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Keep repaired benchmark frozen | 2026-07-02 handoff | Preserves the current baseline and comparability | Silent mutation makes v2 impossible to interpret | Phase 0 baseline hash manifest and no-edit check | Reviewed default |
| Use v2 separate artifact root | 2026-07-02 handoff | Prevents accidental overwrite of repaired artifacts | Mixed artifacts blur baseline/candidate status | Phase 0 path inventory | Reviewed default |
| No response collection in v2 maintenance | 2026-07-02 handoff | User asked for candidate artifacts and explicit collection gate | Accidental model outputs tune cases or cross cost/auth boundary | Phase 3/4/5 stop conditions | Constraint |
| Reuse frozen Phase 1 rubric as baseline | Handoff entry condition | Avoids post-hoc scoring drift | Rubric may not fully distinguish harder v2 artifacts | Phase 2 scoring applicability map labels candidate-only additions | Baseline |
| Six workflow-family coverage | Handoff design requirements | Covers every prioritized workflow family with a bounded candidate set | Too few cases for future statistical claims | Phase 2 coverage report and non-claims | Hypothesis |
| Synthetic or bounded local summaries | Source-boundary policy | Avoids substantial private source excerpts | Cases become too artificial | Phase 2 source-boundary review and adversarial analysis | Reviewed default |
| Claude read-only review | User request and cross-agent policy | Independent critique of boundary safety | Claude silence mistaken for approval | Review trail and explicit unavailable status | Constraint |

## Sequencing Guardrails

1. Phase 0 must pass before any v2 case or prompt artifact is written.
2. Phase 1 must state difficulty requirements before Phase 2 selects cases.
3. Phase 2 must freeze case manifest candidate before Phase 3 writes prompts.
4. Phase 3 must validate prompt contracts before Phase 4 writes collection
   runbook language.
5. Phase 4 must not collect responses; it may only write a future runbook and
   approval boundary.
6. Phase 5 must close with candidate readiness or blocker, not collection.

## Repair Loop

- Each phase starts with a skeptical audit.
- If a material flaw is found, patch the active subplan or artifact visibly.
- Run focused local checks after each patch.
- Use compact Claude read-only review briefs for material subplans and results
  when Claude responds.
- If Claude returns `VERDICT: REVISE`, patch and retry up to five rounds for
  the same blocker.
- If Claude does not respond, run or record a tiny probe. If the probe
  responds, redesign the prompt smaller. If the probe remains silent, record
  reviewer unavailability and proceed only through already-authorized local
  maintenance work.
- If convergence fails after five rounds for the same blocker, write a blocker
  result and stop for human direction.

## Phase Completion Protocol

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. attempt compact Claude read-only review for material subplans unless
   reviewer unavailability is already current and recorded;
6. advance only when exact handoff conditions are met.
