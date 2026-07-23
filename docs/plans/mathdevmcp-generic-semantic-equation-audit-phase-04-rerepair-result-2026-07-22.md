# Phase 04 Second Repair Result

Status: implemented; pending final independent re-review.

The first re-review remained `REVISE` on four high-severity boundaries. The
replay remained stopped. This round repaired:

1. Source-local object identity. Profiles now carry specific response/return
   and ownership identities. Same-symbol bond/equity, customer/employee, and
   team/division endpoints do not pair. Distant label references must use
   affirmative relation language on the label's own source line; contrastive,
   negated, bare-citation, and unrelated references abstain.
2. Signed additive return terms. Normalization parsing now segments the
   additive term containing the return and handles parenthesized terms and
   positive scalar factors. Unsupported term prefixes abstain rather than
   defaulting positive.
3. Canonical semantic validation. The validator rebuilds all blocks from exact
   packets, all profiles from blocks, all hypotheses/checks from profiles, and
   all findings from checks, then requires exact canonical record equality.
   Coherently changed roles, values, relation bases, verdicts, IDs, finding
   summaries/evidence, and result dispositions are rejected.
4. Normalization timing ambiguity. Missing, multiple, or unsupported
   normalization return dates now produce `normalization_timing_unresolved`
   abstention, never a no-tension result.

New tests cover every targeted probe from both review rounds. The full relevant
suite passes (`152 passed`), `compileall` passes, and `git diff --check` passes.

The same-paper replay is still not launched. Final independent re-review must
find no unresolved high-severity evidence defect before rebuilding and freezing
the isolated runtime.
