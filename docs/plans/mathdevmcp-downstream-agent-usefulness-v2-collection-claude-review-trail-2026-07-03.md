# V2 Collection And Scoring Claude Review Trail

Date: 2026-07-03

Status: `FINAL_STATE_REVIEW_AGREED`

## Role Boundary

Claude is read-only reviewer only. Claude cannot authorize response
collection, runtime, model-file, funding, product, release, public-benchmark,
scientific-claim, or general-reliability boundaries.

## Review Gate Policy

Use compact project-local bundles under `docs/reviews/`. Use
`claude_review_gate.sh`, not direct `claude_worker.sh`, for material gates.

Record for each gate:

- command;
- `REVIEW_STATUS`;
- `VERDICT`;
- `RUN_DIR`;
- `SUMMARY_JSON`;
- whether the result was primary or bounded fallback;
- repair actions if any.

## Review Attempts

### 2026-07-03 - `mathdevmcp-v2-collection-phase-00`

Bundle:

- `docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md`

Intended command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name mathdevmcp-v2-collection-phase-00 \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md \
  --model opus \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Status:

- Initial permission-layer attempt timed out before execution.
- Launched gate attempt 1:
  `REVIEW_STATUS=probe_timeout`, `VERDICT=NONE`,
  `RUN_DIR=.claude_reviews/20260703-210129-mathdevmcp-v2-collection-phase-00`,
  `SUMMARY_JSON=.claude_reviews/20260703-210129-mathdevmcp-v2-collection-phase-00/status.json`.
- Launched gate attempt 2 with longer probe timeout:
  `REVIEW_STATUS=probe_timeout`, `VERDICT=NONE`,
  `RUN_DIR=.claude_reviews/20260703-211758-mathdevmcp-v2-collection-phase-00-r2`,
  `SUMMARY_JSON=.claude_reviews/20260703-211758-mathdevmcp-v2-collection-phase-00-r2/status.json`.
- Launched gate attempt 3 after explicit informed human approval for sending
  the bounded Phase 0 bundle to Claude/Anthropic:
  `REVIEW_STATUS=transport_down`, `VERDICT=NONE`,
  `RUN_DIR=.claude_reviews/20260703-215201-mathdevmcp-v2-collection-phase-00-r3`,
  `SUMMARY_JSON=.claude_reviews/20260703-215201-mathdevmcp-v2-collection-phase-00-r3/status.json`.
- Primary/fallback: neither; material review did not start because the small
  probe did not return `OK`.

Reason:

- Claude did not answer the small probe within 90 seconds on the first
  launched gate or within 240 seconds on the second launched gate.
- The third launched gate reached the gateway, but probe stdout reported:
  `API Error: 500 model is not available. model: claude-opus-4-7`.
- A no-bundle `sonnet` probe returned `OK`.
- No-bundle `claude-opus-4-6` and `claude-opus-4-5` probes were unavailable
  or unsupported.

Interpretation:

- This is an Opus model-availability blocker, not a material `REVISE`,
  prompt-design failure, material `timeout`, or `no_verdict`.
- Since the probe prompt is just `Reply exactly: OK`, redesigning the material
  review prompt is not indicated by this failure.
- Phase 0 remains blocked pending human direction: retry later with Opus,
  approve Sonnet max effort as a substitute reviewer for this planning-only
  gate, or explicitly waive Claude review for this planning-only boundary.

## Human Approval

The human explicitly approved sending the bounded Phase 0 review bundle from
`/home/chakwong/python/MathDevMCP` to Claude/Anthropic for read-only review
despite the non-public workspace artifact exfiltration risk.

That approval did not waive Claude review and did not authorize response
collection, Claude as response worker, scoring criteria changes after
responses, runtime/model-file/funding boundaries, or product/release/public
benchmark/scientific/general-reliability claims.

## Reviewer-Model Direction

### 2026-07-03 - Option 1: Retry Opus

The human selected `1`, interpreted as retry Opus later.

Action:

- Ran a no-bundle Opus probe before sending any review bundle:
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name mathdevmcp-v2-phase0-opus-retry-probe --model opus --effort low 'Reply exactly: OK'`.

Outcome:

- Probe failed before any review bundle was sent.
- Output:
  `API Error: 500 model is not available. model: claude-opus-4-7`.

Interpretation:

- Opus remains unavailable through the current gateway.
- The bounded Phase 0 review bundle was not sent on this retry.
- The program remains stopped pending reviewer-model direction or explicit
  collection approval; collection remains unauthorized.

### 2026-07-03 - Sonnet Max Substitute Review Round 1

The human approved Sonnet max as substitute read-only reviewer.

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name mathdevmcp-v2-collection-phase-00-sonnet-r1 \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md \
  --model sonnet \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Status:

- `REVIEW_STATUS=revise`
- `VERDICT=REVISE`
- `RUN_DIR=.claude_reviews/20260703-230309-mathdevmcp-v2-collection-phase-00-sonnet-r1`
- `SUMMARY_JSON=.claude_reviews/20260703-230309-mathdevmcp-v2-collection-phase-00-sonnet-r1/status.json`

Finding:

- Phase 0 was coherent, but Phase 1 next-phase handoff was too weak because
  it permitted advance to Phase 2 while external-review status was merely
  pending reviewer-model direction.

Repair:

- Patch Phase 1 handoff so pending reviewer-model direction is a stop state.
  Advance requires either a successful bounded reviewer verdict or explicit
  human waiver/direction that local-only Phase 2 preflight planning may
  continue without treating the phase as externally reviewed.

### 2026-07-04 - Final-State Continuation Repair

The 2026-07-04 continuation found that the workspace had advanced beyond the
stale Phase 0/1 review state:

- response artifacts exist: 18;
- scored rows exist: 18;
- collection authorization record currently says collection was authorized for
  the exact Phase 3 scope;
- hard vetoes A/B/C: 0/0/0;
- required passes A/B/C: 6/5/6;
- Claude response-worker markers: 0;
- retry issues: 0.

Repair:

- Do not rerun the old Phase 0 bundle as current-state evidence because it
  states that no v2 response artifacts exist.
- Patch stale status/handoff records so the current state is a local
  diagnostic complete pending final external review.
- Create a bounded final-state review bundle that names only specific current
  artifacts and asks for boundary-safety/correctness review.
- Continue the repair loop on the final-state bundle with Sonnet max as the
  approved substitute read-only reviewer. If review returns `REVISE`, patch
  visibly and rerun focused checks, stopping after five rounds for the same
  blocker.

### 2026-07-04 - Final-State Sonnet Review Round 1

Human approval:

- Standing bounded approval granted for Codex-supervised Claude/Anthropic
  read-only review gates in `/home/chakwong/python/MathDevMCP`, using Opus max
  when available or Sonnet max as substitute, on compact bounded repo-local
  review bundles despite non-public workspace artifact exfiltration risk.
  Claude remains read-only reviewer only.

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name mathdevmcp-v2-collection-final-state-sonnet-r1 \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/mathdevmcp-v2-collection-final-state-review-bundle-2026-07-04.md \
  --model sonnet \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Status:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- `RUN_DIR=.claude_reviews/20260704-014647-mathdevmcp-v2-collection-final-state-sonnet-r1`
- `SUMMARY_JSON=.claude_reviews/20260704-014647-mathdevmcp-v2-collection-final-state-sonnet-r1/status.json`

Findings:

- No material blocker.
- Current final-state artifacts are internally consistent on counts, hashes,
  missing-artifact checks, no-Claude-worker markers, and no hidden retries.
- Final handoff separates historical Phase 2 stop from later local
  collection/scoring state.
- Phase 5 result preserves local-diagnostic limitation and no longer treats
  absent review as agreement.
- Scored-result interpretation uses the frozen per-case rule, avoids
  aggregate-only promotion, and preserves non-claims.

Repair required:

- None beyond clerical status closure.
