# High-Level Math Workflows Claude Review Trail

Date: `2026-06-29`

## Role Contract

Claude is a read-only reviewer only. Claude cannot authorize human, runtime,
model-file, funding, product, release, or scientific-claim boundary crossings.

Reviews must be compact and must not send whole large files.

## Master Program Review Round 1

Verdict: `REVISE`

Findings:

- Phase 9 needed a stricter per-workflow baseline ladder.
- Benchmark schema and CLI/MCP exposure could mismatch if Phase 9 only tested
  internal outputs.
- Repair loop needed an explicit hard stop after five failed rounds.
- Claude silence/probe handling needed to state that silence is never approval.
- Phase 1 needed negative-evidence fields.
- Phase-local mutation/negative controls were needed before integrated
  benchmark.
- `prepare_review_packet` needed task-specific scoring.
- `assumptions_for` and `debug_derivation` needed set/rubric scoring.
- Global stop gates were needed for schema ambiguity, poor benchmark
  adjudicability, backend-unavailable dominance, and forbidden claims.

Repair:

- Patched master program, Phase 1, Phases 3-9, and visible runbook with the
  requested baseline ladder, negative-evidence contract, local negative
  controls, rubric scoring, hard repair stop, silence handling, and global stop
  gates.

## Master Program Review Round 2

Outcome: `CLAUDE_REVIEW_UNAVAILABLE_AFTER_SUCCESSFUL_PROBE`

- Compact repaired-delta prompt hung without verdict.
- Tiny probe returned `OK`.
- Smaller repaired-delta prompt also hung without verdict.
- Proceeding under the runbook's reviewer-unavailable path because Round 1
  material findings were visibly patched and local plan checks passed.

## Phase 1 Contract/Evidence Schema Review

Outcome: `REVISE_NONCONVERGED_AFTER_5_ROUNDS`

Claude remained read-only reviewer only. Codex retained execution authority.

Rounds:

1. `REVISE`: requested status-to-evidence matrix, refutation evidence rule,
   `claim_class` taxonomy, and evidence/evidence-class consistency.
2. `REVISE`: requested actual matrix values, claim-class enum values,
   `evidence_classes` derivation/deduplication semantics, and per-status
   presence/absence rules.
3. `REVISE`: requested exact veto/non-claim/action predicates, status enum,
   assumption shape/cardinality, and precedence for multiple evidence classes.
4. `REVISE`: requested collection/cardinality rules, duplicate handling,
   unknown-field policy, and certification-source justification rules.
5. `REVISE`: requested still more explicit enum/matrix wording,
   `evidence_classes=[]` behavior when `evidence=[]`, certification-source
   matching semantics, and counterexample cardinality.

Repair:

- Patched Phase 1 subplan visibly after each fixable finding.
- `git diff --check` passed after repairs.

Stop:

- Stopped per user/runbook hard stop after five failed review/repair rounds
  for the same blocker.

Resume:

- Human directed Codex to continue with the runbook despite Phase 1 Claude
  nonconvergence.
- This was human override, not Claude approval.

Post-implementation review:

- Compact and shorter Phase 1 implementation review prompts did not return a
  verdict and produced `Execution error` on interrupt.
- Tiny Claude probe returned `OK`.
- Recorded as post-implementation reviewer unavailable after successful probe.
