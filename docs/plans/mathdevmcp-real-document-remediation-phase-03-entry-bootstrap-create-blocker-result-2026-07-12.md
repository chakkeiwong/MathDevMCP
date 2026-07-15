# Phase 03 Entry Bootstrap Create Blocker Result

Date: 2026-07-12

Status: `BLOCKED_BEFORE_PHASE_03_ENTRY_ALLOCATION`

## Decision

Stop after the single reviewed Phase 03 `--mode create` invocation failed. Do
not retry that bootstrap, overwrite its fixed budget authorization, delete or
rewrite predecessor scratch state, weaken symlink checks, allocate the Phase 03
root manually, or begin implementation.

The failure occurred before `_mkdir_entry`. The Phase 03 evidence root remains
absent, so there is no partial Phase 03 entry to repair. The one-shot invocation
and fixed budget artifact are nevertheless consumed governance history and must
not be reused under changed planning bytes.

## Bound Inputs

- reviewed Phase 03 plan SHA-256:
  `b0172a6122205d9378c4393bee270116ca501616da0a939b960f2ac16213c4f4`;
- reviewed entry bootstrap SHA-256:
  `abb04fbff5cfbf97b0b41ce28d34c1cf93dbb45243558e0df3064c39f1e9ac8b`;
- agreeing R2 plan-review SHA-256:
  `74eecc8cca08d26a9bb35d66f3e30e3796c888c84b4cb93ea3e3b4602ed851a2`;
- canonical budget-authorization SHA-256:
  `f3e0910e670e31a4d6106fdc3f69c879e7312fe9bd710611a40e6c45875ba5b0`;
- P02 stable decision SHA-256:
  `f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d`;
- P02 terminal receipt-index SHA-256:
  `8f56a72b4575ee3c87122c8656931d7bbb5040a5a3c024edb5f2909b81a78fd0`.

## Exact Failed Invocation

```text
/usr/bin/env -i HOME=/tmp/mathdevmcp-p03-entry-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin PYTHONHASHSEED=0 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -B -S docs/plans/p03_entry_bootstrap_20260712.py --mode create
```

Exit code: `2`.

Exact bootstrap error:

```json
{"error":"EvidenceValidationError: symlink in protected evidence tree: /home/chakwong/python/MathDevMCP/.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr02/governance/tmp/pytest-of-chakwong/pytest-current","status":"ERROR"}
```

## Root Cause

The reviewed no-write preflight validated P02 semantic/governance predecessors,
runtime provenance, allowlists, and root absence, but it did not execute the
create-only protected-tree scan. Create then called `_tree_refs` over the whole
P02R3 phase tree. That helper rejects every symlink, including pytest's normal
runtime convenience links inside `result-rounds/*/governance/tmp`.

The live classification is exact:

- P00, P01, P02, and P02R2 evidence trees contain zero symlinks;
- P02R3 contains 36 symlinks;
- each of `rr01`, `rr02`, and `rr03` contains exactly 12;
- all 36 are under the exact pattern
  `result-rounds/rr0[1-3]/governance/tmp/**`;
- zero symlinks exist outside those three scratch subtrees;
- the failing `pytest-current` link targets `pytest-3` inside the same fixed
  round-local scratch root.

These paths are pytest-generated runtime scratch, not receipt-indexed stable
decisions or source documents. Their presence is inherited sealed state. It is
not evidence corruption and must not be deleted merely to satisfy Phase 03.

## Skeptical Audit

- Wrong repair rejected: removing the links would mutate predecessor state and
  conceal a reviewed preflight coverage gap.
- Broad exclusion rejected: ignoring all symlinks or all `tmp` directories
  could hide an out-of-scope or escaping link.
- Retry rejected: the plan defines create as one-shot, and the fixed budget file
  binds the now-reviewed plan/review bytes.
- Proxy rejected: P02 stable reconstruction and green tests do not establish
  that the Phase 03 protected snapshot can be created.
- Artifact-fitness failure: preflight did not execute all read-only work needed
  to decide whether create could safely allocate.

## Required Recovery Contract

A new additive Phase 03 entry-recovery plan/bootstrap must:

1. bind this blocker, the failed plan/bootstrap/review/budget bytes, R1 history,
   and the exact P02 stable/terminal identities;
2. use a new immutable recovery-plan review path and new canonical
   budget-carry-forward path; never overwrite the existing authorization;
3. retain the same absent `.local/mathdevmcp/evidence/p03-20260712` root only if
   the reviewed recovery explicitly permits a new bootstrap to allocate it, or
   select a new evidence namespace if the reviewer requires stronger one-shot
   separation;
4. define only the three exact P02R3 round-local `governance/tmp/` prefixes as
   non-evidence runtime scratch;
5. require every inherited symlink to be below one of those exact prefixes and
   require zero symlinks elsewhere in every protected predecessor tree;
6. never follow or include scratch symlink targets in the protected manifest;
7. bind an exclusion ledger containing each excluded scratch root, reason,
   round, observed entry counts, symlink count, and a non-claim that scratch is
   not formal evidence;
8. reconstruct all formal P02 decisions, receipts, referenced artifacts, and
   immutable inputs independently of scratch exclusion;
9. move implementation, dirty-state, immutable, protected-tree, exclusion, and
   payload construction into no-write preflight so create performs no new
   fallible discovery before allocation;
10. test a symlink outside the exact scratch prefixes, an escaping scratch link,
    an unexpected fourth prefix, and a formal referenced artifact hidden under
    scratch; each must fail before allocation;
11. preserve the measured Python/pytest provenance repair and the complete
    14-search plus 3-extraction-veto Phase 03 contract.

## Decision Table

| Decision | Primary criterion | Veto diagnostic | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before Phase 03 entry | Entry snapshot was not created | Create-only protected scan rejected inherited P02R3 scratch symlink | Whether a narrowly reviewed scratch-exclusion and full-preflight construction contract closes the gap | Authorize one fresh Phase 03 entry-recovery plan review round, then draft/review a new additive bootstrap | No Phase 03 entry, implementation, semantic/context correctness, mathematics, backend eligibility, publication, Phase 04 readiness, or release readiness |

## Review Budget

The additional repaired-plan R2 round was consumed by substantive `AGREE`.
Neither the reserved result-review round nor the reserved separate final-seal
audit was consumed. They remain protected and cannot be repurposed for the new
entry-recovery plan review.

The corrected R2 bundle's first file-inspection attempt returned no verdict and
does not count as a substantive review. The compact replacement produced the
sole R2 verdict.

## Preservation And Non-Claims

- Phase 03 root is absent; no entry, implementation, result round, receipt,
  candidate, or stable decision exists.
- Existing R1/R2 plans, reviews, blocker, and budget authorization are immutable
  history.
- No P02 scratch link or other predecessor artifact was modified or removed.
- No frozen source, mathematical backend, model, network, GPU, installer,
  commit, push, or publication action was performed.
- Publication remains `disabled`.

## Resume Condition

Resume only after the user authorizes one additional fresh Phase 03
entry-recovery plan review round. Draft the additive recovery plan/bootstrap,
run a complete no-write preflight including every read-only create prerequisite,
recompute exact digests, and obtain `VERDICT: AGREE` before any new allocation
attempt.
