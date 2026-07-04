# Phase 3 Result: Prompt Fixtures And Contract Validation

Date: 2026-07-02

Status: `PASSED_PROMPTS_VALIDATED_NO_RESPONSES`

## Phase Objective

Generate v2 A/B/C prompt fixtures, a prompt manifest with hashes, and a
prompt-contract validation report from the Phase 2 case manifest candidate,
while preserving the repaired baseline and stopping before any response
collection.

## Skeptical Audit

Checked before closing Phase 3:

- Wrong baseline: avoided. Prompt generation used the v2 case manifest; the
  repaired baseline was only rechecked by hash.
- Proxy metrics: avoided. Prompt validation is boundary evidence, not response
  quality or usefulness evidence.
- Missing stop conditions: avoided. Response collection remains explicitly
  forbidden.
- Unfair comparison: controlled. Each of six cases has exactly A/B/C prompts
  and shared task identity.
- Hidden assumptions: recorded. C framing is a design hypothesis; future
  response collection and scoring are not authorized by prompt validity.
- Leakage risk: repaired. Initial validation found A-condition leakage from
  reused titles/summaries; prompts were regenerated with sanitized A-visible
  fields and revalidated.
- Artifact mismatch: avoided. Phase 3 produced prompts/manifest/validation
  only; no response artifacts were created.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can v2 A/B/C prompt fixtures be generated from the candidate cases while preserving condition boundaries and avoiding answer leakage? |
| Baseline/comparator | Phase 2 case manifest candidate, frozen repaired prompt-contract helper, and Phase 0 baseline hashes. |
| Primary criterion | Passed: 18 prompt fixtures exist, manifest hashes match, prompt-contract validation has zero errors, v2 leakage checks pass, no responses were collected, and Phase 4 subplan is ready. |
| Veto diagnostics | Passed after focused repair: no A decisive-evidence/evaluator leakage, no B human-framing leakage, no C evaluator-label leakage, no response artifacts, no baseline mutation, no unsupported claim. |
| Explanatory diagnostics | Condition counts, hash check, leakage check report, validator output, focused pytest. |
| Not concluded | No response quality, downstream-agent usefulness, C-over-B superiority, model reliability, release/public/scientific/product claim. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness_v2/prompts_candidate/`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-04-analysis-runbook-subplan-2026-07-02.md`

## Prompt Summary

| Metric | Result |
| --- | --- |
| Cases | 6 |
| Conditions | A/B/C |
| Prompt files | 18 |
| Validation errors | 0 |
| Response artifacts | 0 |

## Repair Record

Initial validation found 11 prompt-boundary errors. The substantive issue was
that A prompts reused case titles/summaries containing decisive evidence terms
such as counterexample, witness, logdet, solve, and matched/missing audit
language. The repair regenerated all prompt fixtures from sanitized A-visible
fields while leaving evaluator labels in the manifest only. A second focused
validation found one remaining A source-boundary leakage term, which was
removed. Final validation reports zero errors.

## Required Local Checks

| Check | Result |
| --- | --- |
| Prompt manifest parse | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json` |
| Prompt-contract and v2 leakage/hash validation | Passed: `errors 0` and validation report has empty `validation_errors` |
| Prompt fixture count | Passed: 18 |
| Response artifact absence | Passed: no v2 response files |
| Primary baseline hash recheck | Passed: 11/11 primary artifacts match Phase 0 manifest |
| Focused pytest | Passed: `python3 -m pytest tests/test_downstream_usefulness_prompts.py` produced `3 passed` |
| Diff whitespace check | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-*.md` |

## Claude Review Status

Claude remains unavailable from the recorded tiny read-only probe. Phase 3 did
not cross response collection, scoring, implementation repair, runtime,
model-file, funding, product, scientific, release, or public-benchmark
boundaries. Phase 4 subplan was locally reviewed under the required checklist.

## Next Subplan Review

Phase 4 subplan was locally reviewed for:

- consistency: it consumes validated prompts and writes analysis/runbook only;
- correctness: it keeps collection approval explicit and forbids hidden
  retries;
- feasibility: required checks are JSON/runbook grep/hash/diff checks;
- artifact coverage: it requires adversarial analysis, future collection
  runbook, result note, and Phase 5 subplan;
- boundary safety: it forbids response collection, Claude as worker, scoring
  drift, prompt-polish proxy claims, and baseline mutation.

## Handoff To Phase 4

Advance to Phase 4 is allowed because:

- prompt manifest and validation report exist and parse;
- 18 prompt fixtures exist and are covered by hashes;
- validation reports zero errors;
- no response artifacts exist;
- Phase 4 has exact handoff and stop conditions.
