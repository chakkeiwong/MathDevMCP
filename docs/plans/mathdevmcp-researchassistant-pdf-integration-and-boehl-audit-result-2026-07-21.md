# MathDevMCP ResearchAssistant PDF Integration And Boehl Audit Result

Date: 2026-07-21

Plan: `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-plan-2026-07-21.md`

Status: complete with limits

## Result

The experimental ResearchAssistant bridge and the bounded Boehl paper/appendix
case audit are complete. The bridge is source-bound, provider-bound, compact by
default, detailed only by opt-in, and explicit that PDF equation/citation output
is non-certifying. It fails closed on missing source/provider, invalid modes or
limits, provider timeout/nonzero exit, malformed/schema-invalid JSON, oversized
provider output, no usable parser text, and source mutation during execution.

The live case used only `pdftotext`; all four optional parsers were unavailable.
ResearchAssistant's paper title/author result and appendix author result were
wrong, so the adapter now explicitly warns that low-confidence consensus
metadata is not verified source identity. The provider worktree was dirty due
to unrelated untracked LaTeX build files and is also reported as such.

## Scientific Audit Result

All seven final paper/appendix issues in the committee report were reproduced at
their proper boundaries. C.79 is wrong relative to the appendix's own C.47 level
return identity unless an unstated signed-variable convention applies. C.75
remains a sign/timing branch because the printed positive term conflicts with
literal log-discounting, but the executable convention was not independently
settled. Two further appendix defects were localized: the Appendix N posterior
draw multiplication is off by a factor of ten, and Figure H.8's note names
capital rather than government-bond purchases.

The focused MathDevMCP rigor workflow did not reproduce these issues by itself.
For seven exact committee labels it produced one generic C.59 formalization
issue, no concrete repair, a 706 KB detailed JSON, and a 1.3 KB actionable report.
This is evidence of a real remaining PDF/document-semantic gap, not a claim that
the workflow is useless for localization or formal backend routing.

## Evidence

- `docs/reviews/boehl-qe-pdf-audit-2026-07-21/source-and-run-manifest.md`
- `docs/reviews/boehl-qe-pdf-audit-2026-07-21/issue-comparison-matrix.md`
- `docs/reviews/boehl-qe-pdf-audit-2026-07-21/final-gap-report.md`
- compact/detailed extraction packets, direct text baselines, committee index,
  and focused rigor artifacts in the same review directory.

## Verification

- Focused adapter/facade/server/stdio suite: `60 passed in 27.47s`.
- Maintainability, profile, adapter, and stdio regression slice after CLI
  refactor: `28 passed in 12.15s`.
- Broad real-worktree suite excluding the two clean-only release-policy files:
  `1776 passed, 4 skipped in 1476.25s`.
- Clean temporary snapshot release-hypothesis and release-smoke files:
  `13 passed in 138.80s`.
- Clean temporary snapshot MCP stdio: stable profile `23` tools, all profile
  `69` tools, both passed and called `doctor`.
- Clean temporary snapshot public release-hypothesis check: `consistent` with
  no blockers. The real worktree base release report is `ready_with_caveats`
  only because this authorized implementation is uncommitted; no commit or
  push was requested.
- `git diff --check`: passed.

The first full real-worktree run produced `1783 passed, 4 skipped, 6 failed`.
Two failures were genuine and repaired: CLI maintainability ratchets and the
explicit nonstable MCP count. Four were the expected downstream clean-release
policy failures caused by the uncommitted worktree; the clean snapshot proves
those gates pass with the current bytes.

## Decision

Keep the new tool experimental and out of the stable MCP profile. The engineering
bridge is ready for further testing; the combined system is not ready to claim
general PDF mathematical audit capability. The next repair program should first
freeze issue-level regression fixtures from this case, then improve provider
metadata/page/formula packets and MathDevMCP cross-equation semantic checks.

## Non-Claims

- no exact PDF-to-LaTeX recovery;
- no proof or certification of the paper, appendix, or committee report;
- no exact OBC, posterior, likelihood, or counterfactual validation;
- no general PDF performance or department-release conclusion;
- no change to DynareMCP or ResearchAssistant source files.
