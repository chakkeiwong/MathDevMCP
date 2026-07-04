# Read-Only Review Bundles

This directory holds durable review bundles that support project claims,
runbook gates, or benchmark-maintenance handoffs. Runtime logs from review
tools belong under `.claude_reviews/` and are ignored by git unless a specific
log is intentionally promoted into a tracked evidence note.

## Claude Review Gate

For material Claude read-only review gates, use the hardened claudecodex gate:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/python/MathDevMCP \
  --review-name <review-name> \
  --bundle /home/chakwong/python/MathDevMCP/docs/reviews/<review-name>-bundle.md \
  --probe-timeout 90 \
  --timeout-seconds 120 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Run the command with trusted/escalated permissions. Claude is a read-only
reviewer only; Codex remains supervisor and executor unless the user explicitly
changes that role boundary.

## Bundle Contract

Tracked bundles should be compact and self-contained enough for a bounded
review. Include:

- objective;
- exact artifacts to inspect;
- evidence contract;
- forbidden claims and actions;
- precise review questions;
- required verdict format.

Do not ask Claude to inspect the whole repository for a material gate. If the
primary review times out and the bounded fallback returns `AGREE`, record that
as weaker evidence than a full material review and keep the local checks as the
main evidence burden.

## What To Record

Runbooks or close records should record the gate invocation, `REVIEW_STATUS`,
`VERDICT`, `RUN_DIR` or `SUMMARY_JSON`, repair actions for any `REVISE`
findings, local checks, and explicit non-claims. Do not treat review silence,
timeouts, fallback agreement, prompt validity, or formatting polish as proof of
mathematical correctness, release readiness, public benchmark validity, or
downstream-agent reliability.
