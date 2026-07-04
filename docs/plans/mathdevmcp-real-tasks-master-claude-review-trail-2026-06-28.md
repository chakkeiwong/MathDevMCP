# MathDevMCP Real-Task Master Claude Review Trail

## Review Contract

Claude is a read-only reviewer only. Claude cannot authorize execution,
crossing human boundaries, runtime/model-file/funding/product-capability
boundaries, scientific claims, release-policy changes, or gate activation.

Claude prompts must use bounded excerpts or artifact lists rather than dumping
whole long files.

## Probe

### 2026-06-28 - Worker Probe

Command shape:

- `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name mathdevmcp-approval-probe --model opus --effort max ...`

Prompt summary:

- Read-only probe.
- Do not edit files, run commands, or change state.
- Reply exactly `VERDICT: AGREE` if responsive.

Result:

- `VERDICT: AGREE`

Interpretation:

- Claude wrapper is reachable for bounded read-only reviews.

## Reviews

### 2026-06-28 - Plan/Subplan Index Review Round 1

Prompt summary:

- Read-only review only.
- Compact index, not whole files.
- Asked Claude to check sequencing, missing stop conditions, artifact mismatch,
  proxy metric promotion, hidden assumptions, stale context risk, and launch
  feasibility.

Findings summary:

- Phase 4 needed an explicit human-approval boundary for anything beyond
  candidate policy/options.
- Phase 4 needed a revalidation edge if privacy/admissibility/provenance
  constraints change Phase 2/3 assumptions.
- Phase 8 needed stronger protection against de facto gate behavior.
- Setup checks needed explicit non-promoting diagnostic status.
- Five-round repair stop needed a stronger handoff artifact.
- Each phase needed a freshness check at launch.
- Phase 5 schema needed provisional-contract language until post-pilot review.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched the visible execution plan, Phase 4, Phase 5, Phase 8, stop handoff,
  and ledger.

### 2026-06-28 - Plan/Subplan Index Review Round 2

Prompt summary:

- Read-only repair review only.
- Reviewed only whether Round 1 repairs closed the prior blockers and whether
  Phase 0 launch was safe under the visible state machine.

Verdict:

- `VERDICT: AGREE`

Key review conclusion:

- Phase 4 human boundary, Phase 4-to-Phase 5 revalidation edge, Phase 8 de facto
  gate risk, non-promoting diagnostics, concrete blocker handoff, per-phase
  freshness check, and provisional Phase 5 schema language were all materially
  repaired.

### 2026-06-28 - Phase 7 Calibration Review Round 1

Prompt summary:

- Read-only review only.
- Compact Phase 7 calibration result summary.
- Asked whether interpretation overclaimed or whether Phase 8 handoff should
  stop.

Findings summary:

- The interpretation was mostly bounded, but "structurally healthy enough for
  calibration" was slightly too permissive.
- Public and local mismatch/false-confidence-veto failures need first-class
  treatment before any workflow/gate drift.
- Phase 8 handoff is justified only as a decision/audit phase with immediate
  stop conditions for pass/fail workflow, release evidence, public benchmark
  evidence, or default-policy promotion.

Verdict:

- `VERDICT: REVISE`

Repair:

- Patched Phase 7 result and Phase 8 subplan to tighten mismatch/veto treatment
  and frame Phase 8 as boundary/failure-semantics diagnosis plus
  calibration-policy options.

### 2026-06-28 - Phase 7 Calibration Repair Review Round 2

Prompt summary:

- Read-only repair review only.
- Asked whether the Phase 7/8 repair closed the prior blocker and whether Phase
  8 can launch as decision/audit only.

Verdict:

- `VERDICT: AGREE`

Key review conclusion:

- Prior blocker closed. Phase 7 now limits the claim to bounded
  calibration-policy review; Phase 8 is constrained to decision/audit work with
  mismatch/veto mechanisms treated as first-class blockers to workflow/gate
  drift.
