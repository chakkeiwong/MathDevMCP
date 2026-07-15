# MathDevMCP Phase 08C1 Target-Fidelity Blocker Reset

Date: 2026-07-14

Status: `P08D_BLOCKED_BY_UPSTREAM_TARGET_FIDELITY_DEFECT`

## Finding

The Phase 08D skeptical audit rejected the immutable P08C audit as a valid
payload baseline. P08A extracted `eq:incremental-cash-flow` as one complete
label-scoped equality:

```text
\Delta CF_{i,t+h}(a,\pi;s)
= \Delta PPNR_{i,t+h}(a,\pi;s)
- \Delta EL_{i,t+h}(a,\pi;s)
- \Delta Kchg_{i,t+h}(a,\pi;s)
- \Delta Tax_{i,t+h}(a,\pi;s)
+ \Delta RelValue_{i,t+h}(a,\pi;s)
```

Its retained obligation digest is
`7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0`.
P08C instead audited only:

```text
&\quad
  - \Delta Tax_{i,t+h}(a,\pi;s)
  + \Delta RelValue_{i,t+h}(a,\pi;s)
```

The P08C semantic packet has `lhs=None` and `rhs=None`. It therefore cannot be
treated as the same mathematical target, regardless of whether a smaller
transport representation could preserve it exactly.

## Scope Audit

The other four frozen workflow targets are equivalent to their P08A
`normalized_target.display_text` records under the repository's label-scoped
normalization rules. Raw string equality differs only through whitespace,
alignment markers, and terminal punctuation. The defect is localized to the
cash-flow label whose explicit label occurs on the final row of a multi-row
`align` environment.

The root cause is an incomplete Phase 02 integration: the extraction-only
boundary calls `extract_derivation_targets_for_label`, while
`audit_document_derivation_tree` still selects `locate_equations_in_file`
rows through `_select_label_rows` and builds row-level semantic packets. The
legacy locator correctly reports the physical label row, but that row is not a
complete mathematical obligation.

## Decision

Preserve both immutable evidence roots unchanged:

```text
.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0
.local/mathdevmcp/evidence/p08-20260714/continuations/20260714T080342Z-3a1e3445eeab
```

They remain valid evidence of what their snapshotted code produced, but P08C
is now additionally classified as target-unfaithful and cannot authorize P08D
or Phase 09. Repair the document-audit ingress, replay into a new evidence
root, and refresh the payload plan only from a target-faithful audit.

## Non-Claims

- This finding does not refute the source equality or prove any document claim.
- It does not invalidate the separately scoped P08B derivative check.
- Equality of the other four normalized target strings is extraction-fidelity
  evidence only, not proof of those equations.
- No frozen source, publication state, default, or release decision is changed.
