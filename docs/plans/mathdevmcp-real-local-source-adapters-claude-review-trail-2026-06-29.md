# MathDevMCP Real-Local Source Adapters Claude Review Trail

Date: 2026-06-29

Status: `INITIALIZED`

Claude is a read-only reviewer only. Codex remains supervisor and executor.
Review prompts must be compact briefs and must not include whole source files or
whole plans.

## Review Rounds

### R1: Master Program / Runbook / Subplan Structure

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r1 --model opus --effort max '...compact read-only review brief...'
```

Verdict: `REVISE`

Key findings:

- Baseline needed exact frozen artifacts: pilot result path, case ids, manifest
  hash, and source/local provenance.
- Bounded deterministic adapters needed fallback/stop rules for cases requiring
  broader semantic judgment or excessive source context.
- Source/probe/residual ledger separation needed to be enforced in IR before
  adapter phases, not only in Phase 08.
- Residual `adapter_required = 0` needed a sharper non-claim.
- `pytest`, high-level quality, and benchmark gate needed explicit
  engineering/regression-only classification.
- Packet and IR deliverables needed concrete artifact names.
- Packet caps and oversized/ambiguous packet stop rules needed to be explicit.
- Local-only execution boundary needed to say network/model access is unused
  for adapter execution/certification.

Resolution:

- Patched master program, Phase 00, Phase 01, Phase 02, Phase 08, and visible
  runbook to address the R1 findings before execution.

### R2: Repaired Master Program / Runbook Brief

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r2 --model opus --effort max '...compact repaired read-only review brief...'
```

Verdict: `REVISE`

Key findings:

- Add a drift veto: if manifest hash, selected case ids, packet content hash,
  source line anchors, or repo commit/dirty provenance change after Phase 00,
  stop and write a blocked result.
- Specify the sufficient evidence needed to clear `adapter_required`: a
  source-anchored local-schema check over bounded packets, never probe success,
  absence of blockers, adapter confidence, `pytest`, high-level quality, or
  benchmark-gate outcomes.

Resolution:

- Patched master program, Phase 00, Phase 01, Phase 02, Phase 08, and visible
  runbook with drift guards and explicit adapter-clearance criteria.

### R3: Narrow Review Retry And Prompt Redesign

Commands:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r3 --model opus --effort max '...narrow R3 review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-claude-probe --model opus --effort max 'Reply with OK only.'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r3b --model opus --effort max '...smaller R3 review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r3c --model opus --effort high '...minimal R3 review...'
```

Outcome:

- R3 and R3b were interrupted after silence; the probe returned `OK`, so the
  prompts were redesigned smaller.
- R3c returned `REVISE`, noting that drift and clearance rules are necessary
  but not sufficient unless the full evidence contract and skeptical-audit
  fields remain explicit.

Resolution:

- Patched the master program and runbook to state that drift and clearance are
  additional launch gates, not substitutes for the phase evidence contract.
  Phase prechecks must still name baseline/comparator, primary criterion, veto
  diagnostics, stop conditions, artifact provenance, and non-claims.

### R4/R5: Final Plan Gate Attempts

Commands:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r4 --model opus --effort high '...short R4 review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r4b --model opus --effort high '...verdict-only review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-claude-probe-2 --model opus --effort high 'Say OK.'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r4c --model opus --effort high '...OK/FIX review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r5 --model opus --effort high '...one material launch fix...'
```

Outcome:

- R4 and R4b were interrupted after silence.
- Probe 2 returned `OK`.
- R4c returned `FIX` without explanation because the prompt required one-word
  output.
- R5 returned `REVISE`: add an explicit pre-launch blocking checklist that
  re-verifies source-only `adapter_required` planning blockers before
  execution.

Resolution:

- Patched the visible runbook and Phase 00 subplan with a pre-launch blocking
  checklist.
- Because R5 was the fifth review round for the plan gate and did not converge
  to `AGREE`, execution must not launch until the user explicitly directs how
  to proceed.

### User-Authorized Extra Review Budget

After the blocked handoff, the user accepted that the review concerns were
legitimate and authorized five more review/repair rounds to handle them.

Additional rounds are labeled `R6` through `R10`. Codex remains supervisor and
executor; Claude remains read-only reviewer only.

### R6: Additional Launch Review Attempts

Commands attempted:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r6 --model opus --effort high '...compact patched plan review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-claude-probe-r6 --model opus --effort high 'Say OK.'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r6b --model opus --effort high '...launch readiness only...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r6c --model opus --effort high '...mechanical checklist...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r6d --model opus --effort high '...prelaunch checklist excerpt...'
```

Outcome:

- R6, R6b, R6c, and R6d were interrupted after silence.
- The R6 liveness probe returned `OK`.
- Since Claude was responsive to probes but not to review prompts, Codex will
  retry one longer single review run before deciding whether R6 is a
  reviewer-availability blocker.

### R6-Long: Converged Launch Review

Command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-plan-review-r6-long --model opus --effort high '...patched launch gates review...'
```

Verdict: `AGREE`

Claude finding:

```text
I do not see a material launch gate missing for starting Phase 00. The listed
gates cover the main failure modes I would worry about at launch: claim
inflation, provenance drift, packet overreach, adapter leakage across channels,
and accidental promotion from local diagnostics or benchmark confidence.

VERDICT: AGREE
```

Resolution:

- The plan gate converged under the user-authorized additional review budget.
- Proceed to visible runbook Phase 00.
