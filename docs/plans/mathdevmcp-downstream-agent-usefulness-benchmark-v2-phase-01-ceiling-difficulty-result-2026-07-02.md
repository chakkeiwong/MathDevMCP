# Phase 1 Result: Ceiling-Effect And Difficulty Requirements

Date: 2026-07-02

Status: `PASSED_REQUIREMENTS_FROZEN_NO_PROMPTS_CREATED`

## Phase Objective

Inventory why the repaired benchmark produced a B/C ceiling effect and convert
that diagnosis into v2 difficulty requirements that can guide case design
without inspecting new response-worker outputs or tuning to implementation
changes.

## Skeptical Audit

Checked before closing Phase 1:

- Wrong baseline: avoided. Analysis uses
  `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
  and repaired prompt validation as the baseline.
- Proxy metrics: avoided. B/C tied scores are treated as a measurement-design
  ceiling, not proof that C is useless or that B is generally sufficient.
- Missing stop conditions: avoided. Requirements explicitly forbid response
  collection and future hidden retries without approval.
- Unfair comparison: controlled. Requirements target equal A/B/C case
  identities with different allowed information boundaries.
- Hidden assumptions: recorded. Future C-sensitivity is a design hypothesis,
  not a result.
- Artifact mismatch: avoided. Phase 1 artifacts are analysis and requirements
  only; no case manifest, prompts, or responses were created.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Why did B and C tie in the repaired benchmark, and what predeclared difficulty requirements should v2 cases satisfy to plausibly separate them without answer leakage? |
| Baseline/comparator | Repaired scored responses and repaired prompt-contract validation under `.mathdevmcp/downstream_agent_usefulness/`. |
| Primary criterion | Passed: B/C ceiling-effect causes recorded, v2 requirements mapped across six workflow families, and no-collection boundaries preserved. |
| Veto diagnostics | Passed: no new response collection, no frozen-score changes, no prompt fixtures, no C-over-B claim, no answer-leakage requirement. |
| Explanatory diagnostics | Per-case repaired B/C tie inventory, global ceiling causes, workflow requirement coverage, artifact-kind check. |
| Not concluded | No v2 case validity, prompt validity, downstream-agent usefulness, model reliability, C-over-B superiority, public/scientific/product/release claim. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness_v2/ceiling_effect_analysis.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/difficulty_requirements.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-02-case-manifest-subplan-2026-07-02.md`

## Ceiling Summary

| Finding | Result |
| --- | --- |
| B required passes | 9/9 |
| C required passes | 9/9 |
| B required-dimension total | 108/108 |
| C required-dimension total | 108/108 |
| C-over-B criterion | Not met |
| Repaired prompt-contract errors | 0 |

Main diagnosis: the repaired benchmark was valid as a local diagnostic but too
easy for B/C discrimination because compact B evidence was usually already
decisive, bounded summaries supplied safe routes, and one response per prompt
could not establish stable model-level differences.

## Required Local Checks

| Check | Result |
| --- | --- |
| Parse ceiling-effect analysis | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/ceiling_effect_analysis.json` |
| Parse difficulty requirements | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/difficulty_requirements.json` |
| Workflow coverage | Passed: all six families present |
| Per-case ceiling inventory | Passed: 9 repaired cases covered |
| Prompt/response artifact absence | Passed: no v2 files matching prompt/response artifact names at Phase 1 close |
| Diff whitespace check | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-*.md` |

## Claude Review Status

Claude remains unavailable from the recorded tiny read-only probe. Phase 1 did
not cross response collection, scoring, implementation repair, runtime,
model-file, funding, product, scientific, release, or public-benchmark
boundaries. Phase 2 subplan was locally reviewed under the required checklist.

## Next Subplan Review

Phase 2 subplan was locally reviewed for:

- consistency: it consumes Phase 1 requirements and writes only manifest/map
  artifacts;
- correctness: it keeps evaluator-only answer families in the manifest, not
  prompt-visible text;
- feasibility: the candidate cases can be synthetic or bounded summaries;
- artifact coverage: it requires case manifest, scoring applicability map,
  result note, and Phase 3 subplan;
- boundary safety: it forbids prompt fixtures, responses, baseline mutation,
  substantial private excerpts, and C-over-B claims.

## Handoff To Phase 2

Advance to Phase 2 is allowed because:

- Phase 1 JSON artifacts exist and parse;
- all six workflow families have predeclared difficulty requirements;
- no v2 prompts or responses exist;
- Phase 2 has exact handoff and stop conditions;
- response collection remains forbidden.
