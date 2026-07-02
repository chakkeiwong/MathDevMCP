# Downstream-Agent Usefulness Visible Execution Ledger

Date: 2026-07-01

Status: `LAUNCHED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

## Ledger

### 2026-07-01 - Program Draft - PRECHECK

Evidence contract:

- Question: Do MathDevMCP high-level workflow packets measurably improve
  downstream-agent task performance on governed local math tasks?
- Baseline/comparator: prior high-level workflow benchmark, reusable packet
  standard candidate, and A/B/C packet calibration non-claims.
- Primary criterion: create a governed visible runbook that either executes to
  bounded evidence or stops before crossing approval/evidence boundaries.
- Veto diagnostics: hidden retries, Claude as response worker, unapproved
  response collection, rubric mutation after responses, aggregate-only
  promotion, unsupported public/scientific/product claims.
- Non-claims: no release readiness, public benchmark validity, scientific
  validation, product capability, broad theorem proving, or general model
  reliability.

Actions:

- Drafted master program, visible runbook, phase subplans, review trail, and
  stop handoff.

Artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-master-program-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-visible-gated-execution-plan-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-subplan-2026-07-01.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local artifact checks and Claude compact read-only review.

### 2026-07-01 - Program Draft - REVIEW_UNAVAILABLE

Evidence contract:

- Question: Can the master program and visible runbook launch without treating
  Claude silence as approval?
- Baseline/comparator: compact Claude review prompt and tiny probe through the
  read-only worker wrapper.
- Primary criterion: if Claude is unavailable, record that fact and proceed
  only under local checks for non-boundary-crossing Phase 0.
- Veto diagnostics: treating silence as approval; skipping local checks;
  launching response collection or promotion decisions without review.
- Non-claims: no Claude approval, no response collection approval, no
  promotion.

Actions:

- Attempted compact Claude plan review; no usable output.
- Attempted tiny Claude probe; no usable output.
- Patched master program and runbook to record reviewer unavailability.

Artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-claude-review-trail-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-visible-gated-execution-plan-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-master-program-2026-07-01.md`

Gate status:

- `REVIEW_UNAVAILABLE_NON_APPROVAL`

Next action:

- Run local artifact checks and launch Phase 0 only if Codex skeptical review
  passes.

### 2026-07-01 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: What exact baseline and approval boundary does the downstream-agent
  usefulness program start from?
- Baseline/comparator: current commit, prior high-level workflow benchmark,
  packet-standardization result, and A/B/C calibration non-claims.
- Primary criterion: record baseline state, artifacts, checks, and approval
  boundaries without changing implementation behavior.
- Veto diagnostics: dirty state hidden, B/C tie overclaim, missing baseline
  artifact blocker, code/benchmark behavior edit, response collection.
- Non-claims: no downstream-agent usefulness, promotion, release readiness,
  scientific validation, public benchmark validity, product capability, or
  general model reliability.

Actions:

- Ran git state checks.
- Inventoried high-level workflow, packet, benchmark, and calibration
  artifacts.
- Ran focused pytest and high-level workflow quality gate.
- Wrote Phase 0 result.
- Reviewed Phase 1 subplan locally for sequencing, feasibility, artifact
  coverage, and boundary safety.

Artifacts:

- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-result-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-subplan-2026-07-01.md`

Gate status:

- `PASSED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

Next action:

- Start Phase 1 contract/rubric work without response collection.

### 2026-07-01 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: What would count as evidence that packets help downstream agents
  perform the math task better?
- Baseline/comparator: A_task_only, B_evidence_only, and C_human_framed
  conditions.
- Primary criterion: freeze a rubric before response collection that separates
  task success from packet completeness.
- Veto diagnostics: response collection, post-hoc rubric changes, C by
  definition, aggregate-only promotion, Claude worker role.
- Non-claims: no usefulness result, model reliability, proof correctness,
  release readiness, public benchmark validity, product capability, or
  promotion.

Actions:

- Read prior calibration contract/rubric and scored summary.
- Wrote downstream-usefulness benchmark contract and scoring rubric.
- Ran JSON/content validation, promotion-sensitive grep, and diff whitespace
  check.
- Attempted compact Claude review; no usable output, recorded as
  unavailability.
- Wrote Phase 1 result and reviewed Phase 2 subplan locally.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/benchmark_contract.json`
- `.mathdevmcp/downstream_agent_usefulness/scoring_rubric.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-result-2026-07-01.md`

Gate status:

- `PASSED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

Next action:

- Start Phase 2 case-corpus fixture design without response collection.

### 2026-07-01 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Which governed local cases can fairly test downstream-agent
  usefulness across high-level workflows?
- Baseline/comparator: existing real-local benchmark cases, packet report, and
  final matrix.
- Primary criterion: freeze a manifest with workflow family, evidence class,
  expected output type, source boundary, and scoring applicability.
- Veto diagnostics: response collection, case selection after model responses,
  substantial copied source text, all-one-workflow corpus, diagnostic evidence
  relabeled as proof.
- Non-claims: no response quality, usefulness result, public benchmark
  validity, release readiness, scientific validation, or product capability.

Actions:

- Inspected existing real-local manifest, packet report, final matrix, and
  holdout-local docs.
- Wrote downstream-usefulness case manifest and evidence-class matrix.
- Ran JSON/content validation, coverage check, source-boundary grep, and diff
  check.
- Wrote Phase 2 result and reviewed Phase 3 subplan locally.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/case_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/evidence_class_matrix.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-02-case-corpus-fixtures-result-2026-07-01.md`

Gate status:

- `PASSED_LOCAL_CASE_MANIFEST_FROZEN`

Next action:

- Start Phase 3 prompt harness and response-collection gate.

### 2026-07-01 - Phase 3 - ASSESS_GATE

Evidence contract:

- Question: Are prompt fixtures and collection rules frozen enough to collect
  downstream-agent responses without hidden bias or approval drift?
- Baseline/comparator: Phase 2 cases and Phase 1 A/B/C comparator contract.
- Primary criterion: freeze prompt fixtures, manifest, response-subject policy,
  retry policy, and artifact paths before any response collection.
- Veto diagnostics: response collection before approval, Claude as worker,
  hidden retries, malformed-output replacement, A/B/C imbalance.
- Non-claims: no usefulness result, model reliability, scoring result,
  response quality, or promotion decision.

Actions:

- Generated 27 prompt fixtures from frozen contract and case manifest.
- Wrote prompt manifest, response-subject policy, and approval request note.
- Validated prompt counts, hashes, approval policy, and no-response state.
- Wrote Phase 3 result as blocked pending explicit response-collection
  approval.
- Reviewed Phase 4 subplan locally.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts/`
- `.mathdevmcp/downstream_agent_usefulness/response_subject_policy.json`
- `.mathdevmcp/downstream_agent_usefulness/response_collection_approval_request.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-03-prompt-harness-collection-gate-result-2026-07-01.md`

Gate status:

- `BLOCKED_PENDING_EXPLICIT_RESPONSE_COLLECTION_APPROVAL`

Next action:

- Ask the user for explicit approval before Phase 4 response collection.

### 2026-07-02 - Phase 4 - PRECHECK

Evidence contract:

- Question: What do approved downstream responses show under the frozen
  usefulness rubric?
- Baseline/comparator: A/B/C prompt conditions frozen in Phase 3.
- Primary criterion: every approved prompt receives one recorded response or
  malformed-output record; scoring uses the frozen Phase 1 rubric; hard vetoes
  and per-case results are reported before aggregates.
- Veto diagnostics: hidden retry, missing malformed output, Claude response
  worker, changed rubric, unrecorded prompt, aggregate promotion despite hard
  veto, unsupported C superiority claim.
- Non-claims: no release readiness, public benchmark validity, scientific
  validation, product capability, broad theorem proving, or general model
  reliability.

Actions:

- User approved exact Phase 4 scope on 2026-07-02: collect one downstream-agent
  response per frozen prompt for the 27 prompts under
  `.mathdevmcp/downstream_agent_usefulness/prompts/`, using Codex subagents or
  another approved non-Claude surface, no hidden retries, malformed outputs
  recorded, and Claude read-only reviewer only.
- Discovered Codex subagent surface via `tool_search`.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/response_subject_policy.json`

Gate status:

- `IN_PROGRESS`

Next action:

- Collect one Codex subagent response per frozen prompt and record outcomes.

### 2026-07-02 - Phase 4 - ASSESS_GATE

Evidence contract:

- Question: What do approved downstream responses show under the frozen
  usefulness rubric?
- Baseline/comparator: A/B/C prompt conditions frozen in Phase 3.
- Primary criterion: every approved prompt receives one recorded response or
  malformed-output record; scoring uses the frozen Phase 1 rubric; hard vetoes
  and per-case results are reported before aggregates.
- Veto diagnostics: hidden retry, missing malformed output, Claude response
  worker, changed rubric, unrecorded prompt, aggregate promotion despite hard
  veto, unsupported C superiority claim, and condition-artifact leakage.
- Non-claims: no release readiness, public benchmark validity, scientific
  validation, product capability, broad theorem proving, general model
  reliability, or C-over-B superiority.

Actions:

- Collected 27 Codex-subagent responses, one per frozen prompt, with no hidden
  retries and no Claude response worker.
- Wrote response manifest and scored-response artifacts.
- Applied hard-veto-first scoring against the frozen rubric and Phase 1
  condition contract.
- Found that all nine `A_task_only` prompts leaked evaluator/status fields, so
  the A baseline is contaminated.
- Refreshed Phase 5 as benchmark repair and measurement-design work rather than
  capability repair.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/response_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-04-response-collection-scoring-result-2026-07-01.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-subplan-2026-07-01.md`

Gate status:

- `COMPLETED_WITH_A_CONDITION_LEAKAGE_VETO`

Next action:

- Begin Phase 5 benchmark repair taxonomy and prompt-condition validation. Do
  not run new downstream-agent response collection without explicit approval.

### 2026-07-02 - Phase 5 - ASSESS_GATE

Evidence contract:

- Question: Which Phase 4 failures can be safely repaired, and what remains a
  measurement limitation requiring new approval or a new collection phase?
- Baseline/comparator: Phase 4 scored responses, prompt manifest, Phase 1
  condition contract, and current prompt fixtures.
- Primary criterion: repairs are traceable to observed fixture leakage or
  measurement limitations, pass focused checks, and do not change scoring or
  promotion criteria post hoc.
- Veto diagnostics: repair overfits to response wording, rubric changed, A
  leakage remains in repaired candidate, B/C parity broken, hidden response
  rerun, diagnostic evidence relabeled as proof, unrelated refactor.
- Non-claims: no final usefulness promotion, repaired-benchmark result,
  C-over-B claim, release readiness, public benchmark validity, scientific
  validation, product capability, broad theorem proving, or general model
  reliability.

Actions:

- Added a local prompt-condition validator for downstream-usefulness prompt
  fixtures.
- Added focused tests proving the validator catches the existing A-condition
  leakage and accepts a minimal repaired A/B/C case.
- Generated a repaired candidate prompt manifest and 27 repaired candidate
  prompts under a separate artifact path.
- Wrote a failure taxonomy covering the A leakage hard veto and secondary
  measurement limitations.
- Ran focused pytest, JSON validation, prompt-contract validation, and diff
  whitespace checks.

Artifacts:

- `src/mathdevmcp/downstream_usefulness_prompts.py`
- `tests/test_downstream_usefulness_prompts.py`
- `.mathdevmcp/downstream_agent_usefulness/failure_taxonomy.json`
- `.mathdevmcp/downstream_agent_usefulness/prompt_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/prompts_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/repaired_prompt_contract_validation.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-05-failure-taxonomy-repairs-result-2026-07-01.md`

Gate status:

- `PASSED_REPAIRED_CANDIDATE_READY_RECOLLECTION_APPROVAL_NEEDED`

Next action:

- Begin Phase 6 final regression and bounded decision. Do not collect repaired
  prompt responses without explicit approval.

### 2026-07-02 - Phase 6 - FINAL

Evidence contract:

- Question: What bounded downstream-agent usefulness decision is justified by
  the produced artifacts?
- Baseline/comparator: Phase 4 scored results plus Phase 5 repaired candidate
  prompts.
- Primary criterion: final decision matches actual artifacts, preserves the
  A-leakage hard veto and non-claims, and records that repaired-prompt response
  collection needs approval.
- Veto diagnostics: claim exceeds evidence, aggregate score overrides hard
  veto, response sample treated as general reliability, release/public/
  scientific/product claim, undocumented test failure, Claude treated as
  authority, repaired candidate treated as scored evidence.
- Non-claims: no public benchmark validity, release readiness, scientific
  validation, product capability, broad theorem proving, general model
  reliability, C-over-B superiority, or proof correctness beyond scoped
  certified obligations.

Actions:

- Ran focused Phase 6 checks.
- Attempted compact Claude read-only final review and tiny probe; reviewer
  unavailable because the Opus wrapper reported a server-side model unavailable
  error.
- Wrote final summary and Phase 6 result.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/final_summary.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-06-regression-promotion-decision-result-2026-07-01.md`

Gate status:

- `FINAL_NO_PROMOTION_REPAIRED_CANDIDATE_READY`

Next action:

- Stop unless the user explicitly approves a new repaired-prompt response
  collection.

### 2026-07-02 - Repaired Collection Addendum - FINAL

Evidence contract:

- Question: Do repaired prompt fixtures, with A-condition leakage removed,
  produce a valid local A/B/C downstream-agent usefulness diagnostic?
- Baseline/comparator: repaired `A_task_only`, `B_evidence_only`, and
  `C_human_framed` conditions.
- Primary criterion: collect one Codex-subagent response or malformed-output
  record for each repaired prompt; score hard-veto-first against the frozen
  Phase 1 rubric.
- Veto diagnostics: hidden retry, Claude response worker, malformed output
  replaced, repaired prompt mutation after collection starts, scoring-rubric
  mutation, A leakage persists, aggregate-only promotion, unsupported
  C-over-B claim.
- Non-claims: no release readiness, public benchmark validity, scientific
  validation, product capability, broad theorem proving, proof correctness
  beyond scoped certified obligations, or general model reliability.

Actions:

- User waived the additional repaired-collection approval gate.
- Collected 27 repaired Codex-subagent responses, one per repaired prompt, with
  no hidden retries and no Claude response worker.
- Preserved original Phase 4 prompts/responses and wrote repaired-run artifacts
  under separate `*_repaired_candidate` paths.
- Scored repaired responses against the frozen Phase 1 rubric.
- Found repaired A/B/C comparison valid as a local diagnostic: no hard vetoes,
  no malformed outputs, no repaired A prompt leakage.
- Found no C-over-B promotion support: A required-pass count is 8/9, B is 9/9,
  and C is 9/9; C ties B under the frozen required dimensions.

Artifacts:

- `.mathdevmcp/downstream_agent_usefulness/responses_repaired_candidate/`
- `.mathdevmcp/downstream_agent_usefulness/response_manifest_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness/scored_responses_repaired_candidate.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-repaired-collection-result-2026-07-02.md`

Gate status:

- `REPAIRED_COLLECTION_COMPLETE_NO_PROMOTION`

Next action:

- Stop, or design a harder replicated benchmark if the project wants a stronger
  C-vs-B discriminability test.
