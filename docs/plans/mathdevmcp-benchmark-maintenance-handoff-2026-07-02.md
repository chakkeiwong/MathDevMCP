# Benchmark Maintenance Handoff

Date: 2026-07-02

Status: `HANDOFF_READY_FOR_SEPARATE_BENCHMARK_AGENT`

## Purpose

This memo hands off the benchmark-maintenance lane for the downstream-agent
usefulness benchmark. The implementation lane will improve MathDevMCP tools in
parallel. The benchmark agent must keep the measuring instrument honest without
tuning it to implementation changes.

## Current Benchmark State

The repaired benchmark is usable as a local diagnostic/regression benchmark.

Key result:

- repaired responses collected: 27/27;
- response subject: Codex subagents;
- retry policy: one attempt per prompt, no hidden retries;
- Claude role: read-only reviewer only, not a response worker;
- hard vetoes: A = 0, B = 0, C = 0;
- required passes: A = 8/9, B = 9/9, C = 9/9;
- repaired A/B/C comparison: valid as a local diagnostic;
- C-over-B promotion: not supported because C ties B under the frozen required
  dimensions.

Primary artifacts:

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/responses_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/response_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-repaired-collection-result-2026-07-02.md`

## Benchmark Agent Objective

Create a next benchmark candidate that better discriminates between:

- B: machine-evidence-only or compact evidence packet prompts;
- C: human-framed, self-contained agent-handoff packet prompts.

The new benchmark should test whether richer handoff framing helps a downstream
agent perform mathematical work, not whether it can repeat labels from a prompt.

## Entry Conditions

- The repaired benchmark remains frozen as the current baseline.
- The frozen Phase 1 rubric remains the scoring baseline unless a new benchmark
  version explicitly declares a separate rubric as a candidate, not a
  replacement.
- Original and repaired raw responses remain preserved.
- Benchmark maintenance is separate from tool implementation.

## Required Outputs

Create a new benchmark-maintenance plan and candidate artifacts under separate
paths. Suggested names:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-plan-2026-07-02.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/`

Required artifacts:

- case manifest candidate;
- prompt fixture candidate;
- prompt manifest with hashes;
- prompt-contract validation report;
- scoring applicability map;
- adversarial/ceiling-effect analysis;
- runbook for future response collection;
- result note explaining what changed relative to the repaired benchmark.

## Design Requirements

The v2 benchmark should add harder cases where:

- A task-only prompt is insufficient because it lacks decisive executable or
  source evidence;
- B contains evidence but remains terse enough that downstream agents may miss
  assumptions, route boundaries, or next actions;
- C contains self-contained framing that should help an agent decide, derive,
  refute, or abstain correctly;
- prose-only completion is not enough for a full score when a backend
  certificate, counterexample, equation-to-code trace, or assumption ledger is
  required;
- correct answers require maintaining non-claim boundaries.

Prioritize cases in these families:

1. `derive_from`: route from assumptions to target with a missing matrix/domain
   obligation.
2. `prove_or_counterexample`: symbolic claim where a backend certificate or
   concrete counterexample is decisive.
3. `assumptions_for`: likelihood, score, or optimization claim with
   route-required assumptions that are easy to miss.
4. `audit_math_to_code`: documented formula with one missing implementation
   term or ambiguous alias.
5. `debug_derivation`: local derivation gap where the first failing step must
   be localized.
6. `prepare_review_packet`: difficult derivation where the correct output is a
   diagnostic packet, not proof.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a harder local benchmark discriminate between compact machine-evidence prompts and richer human-framed handoff packets without post-hoc scoring drift? |
| Baseline/comparator | Current repaired benchmark plus proposed v2 candidate. |
| Primary criterion | v2 candidate preserves governance boundaries, avoids A leakage, avoids B/C answer leakage, and includes cases where B and C plausibly separate on predeclared dimensions. |
| Veto diagnostics | Mutating repaired baseline; selecting cases after seeing new model responses; changing frozen scores post hoc; scoring packet polish as task success; using Claude as response worker; hiding malformed outputs; adding cases that require private source excerpts without summary boundaries; claiming public/scientific/product validity. |
| Explanatory diagnostics | Ceiling-effect analysis, difficulty tags, expected evidence class distribution, prompt-contract validation, per-case rationale. |
| Not concluded | No tool improvement, no model reliability, no release readiness, no public benchmark validity, no C-over-B superiority before new scored responses. |

## Forbidden Actions

- Do not edit or overwrite `.mathdevmcp/downstream_agent_usefulness/` repaired
  baseline artifacts.
- Do not mutate `scoring_rubric.json` and call the old scores comparable.
- Do not collect new response-worker outputs unless explicitly authorized for
  the new scope.
- Do not use Claude as a response worker.
- Do not use whole-file private excerpts in prompts when a bounded summary is
  sufficient.
- Do not tune cases to implementation branches being developed in parallel.
- Do not claim benchmark validity beyond local diagnostic use.

## Suggested Work Plan

1. Inventory ceiling effects in the repaired benchmark.
   - Record why B and C tied on each case.
   - Identify which cases were too easy because the bounded summary already
     supplied the answer route.

2. Draft v2 case requirements.
   - Specify target workflows, evidence classes, and expected output family.
   - Require at least 2-3 cases where C should help over B because of framing,
     not because it leaks the answer.

3. Build candidate cases.
   - Use local summaries, synthetic fixtures, or sanitized excerpts.
   - Include expected answer family and forbidden claims in the manifest only
     where evaluator labels belong.

4. Generate prompt variants.
   - A: task plus bounded context only.
   - B: compact machine evidence.
   - C: human-framed handoff packet with background, decision criteria,
     assumptions, route gaps, and next artifact.

5. Validate prompt boundaries.
   - A must not leak evaluator-only labels or decisive backend evidence.
   - B must not include human-framing fields.
   - C may include framing but must not provide hidden scoring labels as
     authority.

6. Write the v2 runbook.
   - Include approval boundary for any new response collection.
   - Include no-hidden-retry and malformed-output rules.
   - Include response subject surface and artifact paths.

7. Stop before collection.
   - Produce a handoff asking for explicit collection approval if collection is
     desired.

## Quality Bar For The Benchmark

A candidate v2 benchmark is good only if it:

- preserves frozen baseline artifacts;
- has no prompt-contract leakage;
- has balanced workflow/evidence coverage;
- has cases with plausible B/C discrimination;
- has expected answers that are source-bounded and auditable;
- makes malformed-output and no-hidden-retry policies explicit;
- can be scored hard-veto-first;
- does not require expert panel judgment for basic pass/fail;
- records limitations honestly.

## Coordination With Tool-Improvement Lane

The implementation lane may use the repaired benchmark as a regression harness
and may add tool tests. The benchmark lane should not inspect unmerged
implementation details to design favorable cases. The benchmark lane may report
capability gaps as requirements, but must not patch implementation code.

## Stop Conditions

Stop and write a blocker if:

- the v2 benchmark cannot avoid answer leakage without becoming too vague;
- source materials require privacy/copyright decisions not already covered by
  local summaries;
- B/C discrimination requires changing the scoring rubric after seeing
  responses;
- collection is requested without explicit approval for prompt count,
  response-worker surface, retry policy, and artifact paths;
- the benchmark would make release, product, scientific, public-validity, or
  general model reliability claims.
