# Phase 2 Result: Case Manifest Candidate

Date: 2026-07-02

Status: `PASSED_CASE_MANIFEST_CANDIDATE_FROZEN`

## Phase Objective

Create the v2 case manifest candidate and scoring applicability map under the
separate v2 artifact root, using the Phase 1 difficulty requirements and
without creating prompt fixtures or collecting responses.

## Skeptical Audit

Checked before closing Phase 2:

- Wrong baseline: avoided. Phase 2 used Phase 1 requirements and rechecked
  Phase 0 primary repaired-baseline hashes.
- Proxy metrics: avoided. Case difficulty and C-sensitivity are design
  hypotheses, not scored response evidence.
- Missing stop conditions: avoided. Prompt generation and response collection
  remain separate gated phases.
- Unfair comparison: controlled. Each candidate case has one task identity and
  predeclared A/B/C information-boundary designs.
- Hidden assumptions: recorded. Candidate-only stressors are explanatory unless
  a future v2 rubric is explicitly approved before collection.
- Source boundary: preserved. Cases use synthetic fixtures or bounded local
  summaries and require no substantial private or neighboring-repo excerpts.
- Artifact mismatch: avoided. Phase 2 artifacts are manifest/map artifacts
  only; no prompts or responses were created.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the v2 candidate case set cover the target workflow families with harder, source-bounded cases that plausibly separate B and C without leaking expected answers? |
| Baseline/comparator | Phase 1 difficulty requirements and the frozen repaired benchmark baseline. |
| Primary criterion | Passed: case manifest and scoring map parse, cover all six workflow families, include four high C-sensitivity cases, preserve source boundaries, and stop before prompt generation. |
| Veto diagnostics | Passed: no prompt fixtures, no response collection, no repaired baseline mutation, no substantial private excerpts, no C-over-B or benchmark-validity claim. |
| Explanatory diagnostics | Workflow coverage, C-sensitivity count, source-boundary summary, baseline hash recheck, local review. |
| Not concluded | No prompt validity, scored response evidence, C-over-B superiority, model reliability, release/public/scientific/product claim. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness_v2/case_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-03-prompts-validation-subplan-2026-07-02.md`

## Candidate Coverage

| Metric | Result |
| --- | --- |
| Cases | 6 |
| Workflow families | 6/6 covered |
| High C-sensitivity cases | 4 |
| Required artifact types | 6 |
| Source material | Synthetic or bounded local-summary fixtures |

## Required Local Checks

| Check | Result |
| --- | --- |
| Parse case manifest | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/case_manifest_candidate.json` |
| Parse scoring applicability map | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json` |
| Required case fields | Passed for all 6 cases |
| Workflow coverage | Passed: all six target families present |
| High C-sensitivity count | Passed: 4 >= 3 |
| Map/manifest case id match | Passed |
| Primary baseline hash recheck | Passed: 11/11 primary artifacts match Phase 0 manifest |
| Prompt/response absence | Passed: no Phase 3 prompt/response artifacts under v2 root |
| Diff whitespace check | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-*.md` |

## Claude Review Status

Claude remains unavailable from the recorded tiny read-only probe. Phase 2 did
not cross response collection, prompt generation, scoring, implementation
repair, runtime, model-file, funding, product, scientific, release, or
public-benchmark boundaries. Phase 3 subplan was locally reviewed under the
required checklist.

## Next Subplan Review

Phase 3 subplan was locally reviewed for:

- consistency: it consumes the Phase 2 manifest and map;
- correctness: it requires prompt-condition validation and separate
  leakage/hash checks;
- feasibility: 6 cases x 3 conditions = 18 prompts can be generated from
  manifest fields;
- artifact coverage: it requires prompt fixtures, prompt manifest, validation
  report, result note, and Phase 4 subplan;
- boundary safety: it forbids response collection, repaired-baseline mutation,
  evaluator-label leakage, and prompt-validation-as-task-success claims.

## Handoff To Phase 3

Advance to Phase 3 is allowed because:

- case manifest candidate and scoring applicability map exist and parse;
- all required workflow families are represented;
- high C-sensitivity coverage exceeds the minimum requirement;
- no v2 prompt or response artifacts exist at Phase 2 close;
- Phase 3 has exact handoff and stop conditions.
