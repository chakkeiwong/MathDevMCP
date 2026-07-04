# Phase 4 Result: Adversarial Analysis And Collection Runbook

Date: 2026-07-02

Status: `PASSED_ANALYSIS_RUNBOOK_NO_COLLECTION`

## Phase Objective

Write adversarial/ceiling-effect analysis for the v2 candidate prompts and a
future response-collection runbook that preserves no-hidden-retry discipline
and stops before explicit human collection approval.

## Skeptical Audit

Checked before closing Phase 4:

- Wrong baseline: avoided. Phase 4 used validated v2 prompts and rechecked the
  frozen repaired baseline hashes.
- Proxy metrics: avoided. Adversarial analysis and prompt polish are not scored
  task-success evidence.
- Missing stop conditions: repaired and passed. The future runbook explicitly
  states collection is not authorized and names required approval fields.
- Hidden retries: controlled. The runbook requires one attempt per prompt and
  preservation of malformed outputs unless a different replicated design is
  approved before launch.
- Claude boundary: repaired and passed. The runbook now explicitly states
  Claude is forbidden as a response worker.
- Artifact mismatch: avoided. Phase 4 created analysis/runbook artifacts only;
  no response artifacts were created.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the v2 candidate have documented leakage/ceiling risks and a future collection runbook that preserves approval, retry, malformed-output, and Claude-role boundaries? |
| Baseline/comparator | Phase 3 validated v2 prompt fixtures and frozen repaired baseline. |
| Primary criterion | Passed: adversarial analysis and future collection runbook exist, checks pass, no responses were collected, and Phase 5 handoff subplan is ready. |
| Veto diagnostics | Passed: no response collection, no hidden retries, no Claude worker role, no scoring drift, no prompt-polish proxy scoring, no unsupported claims, no repaired baseline mutation. |
| Explanatory diagnostics | Risk table, ceiling-effect risks, collection approval checklist, artifact-path plan, baseline hash recheck. |
| Not concluded | No scored v2 result, C-over-B superiority, model reliability, release/public/scientific/product claim. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness_v2/adversarial_ceiling_analysis.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/future_collection_runbook.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-05-final-handoff-subplan-2026-07-02.md`

## Required Local Checks

| Check | Result |
| --- | --- |
| Parse adversarial/ceiling analysis | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/adversarial_ceiling_analysis.json` |
| Runbook guardrail grep/check | Passed after wording repair: approval boundary, prompt count, worker surface, retry policy, malformed-output policy, and Claude worker prohibition present |
| Response artifact absence | Passed: no v2 response/scored-response/response-manifest artifacts |
| Primary baseline hash recheck | Passed: 11/11 primary artifacts match Phase 0 manifest |
| Diff whitespace check | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-*.md` |

## Repair Record

The initial runbook guardrail check found that the Claude worker prohibition was
present in meaning but not in the exact explicit wording required by the local
check. The runbook was patched to include: `Claude is forbidden as a response
worker.` The guardrail check then passed.

## Claude Review Status

Claude remains unavailable from the recorded tiny read-only probe. Phase 4 did
not cross response collection, scoring, implementation repair, runtime,
model-file, funding, product, scientific, release, or public-benchmark
boundaries. Phase 5 subplan was locally reviewed under the required checklist.

## Next Subplan Review

Phase 5 subplan was locally reviewed for:

- consistency: it consumes all v2 candidate artifacts and closes the program;
- correctness: it stops before response collection;
- feasibility: final checks are JSON parse, prompt validation, hash, pytest,
  response absence, and diff checks;
- artifact coverage: it requires result note, Phase 5 result, stop handoff,
  and ledger update;
- boundary safety: it forbids responses, scoring files, baseline mutation,
  unsupported claims, and fake Claude approval.

## Handoff To Phase 5

Advance to Phase 5 is allowed because:

- adversarial analysis exists and parses;
- future collection runbook exists and states the approval boundary;
- no response artifacts exist under v2 root;
- repaired baseline hashes match Phase 0 manifest;
- Phase 5 has exact close and stop conditions.
