# Phase 0 Result: Governance And Baseline Freeze

Date: 2026-07-02

Status: `PASSED_BASELINE_FROZEN_V2_ROOT_CREATED`

## Phase Objective

Freeze the repaired benchmark baseline, v2 artifact root, approval boundaries,
and local execution state before creating any v2 candidate cases or prompts.

## Skeptical Audit

Checked before closing Phase 0:

- Wrong baseline: avoided. The repaired benchmark remains under
  `.mathdevmcp/downstream_agent_usefulness/`; v2 artifacts are under
  `.mathdevmcp/downstream_agent_usefulness_v2/`.
- Proxy metrics: avoided. Hash preservation is recorded only as a governance
  tripwire, not benchmark validity or response-quality evidence.
- Missing stop conditions: avoided. Response collection, Claude response-work,
  private-source excerpts, baseline mutation, and public/scientific/product
  claims remain explicit stop boundaries.
- Unfair comparisons: avoided at this phase. No v2 cases or prompts were
  created.
- Hidden assumptions: recorded. Claude review is currently unavailable after a
  tiny probe; this is not treated as approval.
- Artifact mismatch: avoided. Phase 0 artifacts answer only whether the lane is
  separated and baseline hashes are recorded.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is the repaired benchmark baseline frozen and is the v2 maintenance lane safely separated before candidate design begins? |
| Baseline/comparator | Repaired benchmark artifacts under `.mathdevmcp/downstream_agent_usefulness/` and new v2 root under `.mathdevmcp/downstream_agent_usefulness_v2/`. |
| Primary criterion | Passed: baseline hashes recorded, v2 root metadata exists, repaired baseline files were not modified by Phase 0, JSON/diff checks passed, and Phase 1 subplan is present. |
| Veto diagnostics | Passed: no repaired baseline edits, no response collection, no Claude response-worker use, no unsupported C-over-B or benchmark-validity claim. |
| Explanatory diagnostics | Hash manifest, v2 README, JSON parse checks, artifact listing, diff check, Claude probe trail. |
| Not concluded | No v2 case quality, prompt validity, downstream-agent usefulness, C-over-B superiority, public/scientific/product/release/general-reliability claim. |

## Artifacts Produced

- `.mathdevmcp/downstream_agent_usefulness_v2/README.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/baseline_hash_manifest.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-master-program-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-gated-execution-plan-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-claude-review-trail-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-execution-ledger-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-visible-stop-handoff-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-00-governance-baseline-subplan-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-benchmark-v2-phase-01-ceiling-difficulty-subplan-2026-07-02.md`

## Baseline Hash Summary

| Artifact class | Count | Status |
| --- | ---: | --- |
| Primary repaired files and governing notes | 11 | Hashes recorded |
| Repaired candidate prompt fixtures | 27 | Aggregate hash recorded |
| Repaired candidate responses | 27 | Aggregate hash recorded |

## Required Local Checks

| Check | Result |
| --- | --- |
| Parse v2 baseline hash manifest | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/baseline_hash_manifest.json` |
| Parse repaired scored responses | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json` |
| Parse repaired prompt validation | Passed: `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness/repaired_prompt_contract_validation.json` |
| List v2 files | Passed: only `README.md` and `baseline_hash_manifest.json` under v2 root at close of Phase 0 checks |
| Diff whitespace check | Passed: `git diff --check` over Phase 0-created plans/artifacts |

## Claude Review Status

Claude read-only review was attempted before Phase 0 close. The tiny probe did
not return output after about two minutes and was interrupted. A later
`claude --version` check returned `2.1.148 (Claude Code)`. This is recorded as
reviewer unavailable, not approval.

## Next Subplan Review

Phase 1 subplan was locally reviewed for:

- consistency: it uses the repaired benchmark as baseline and creates only
  analysis/requirements artifacts;
- correctness: it does not infer C-over-B superiority from tied repaired
  scores;
- feasibility: it can be answered from existing repaired scored-response
  artifacts;
- artifact coverage: it requires ceiling-effect analysis, difficulty
  requirements, result note, and Phase 2 subplan;
- boundary safety: it forbids response collection, repaired-baseline mutation,
  prompt generation, and answer leakage.

## Handoff To Phase 1

Advance to Phase 1 is allowed because:

- baseline hash manifest exists and parses;
- v2 root metadata exists;
- no Phase 0 action required modifying the repaired baseline;
- Phase 1 subplan exists and includes the required subplan fields;
- response collection remains forbidden until explicit future approval.
