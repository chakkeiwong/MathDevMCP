# Phase 03 Result: Canonical Relation And Role Contract

Date: 2026-07-16

Decision: `PASS`

## Objective Result

The label-scoped extraction boundary now represents standalone conditional
expectation objects and conditional independence relations. A separate
digest-bound source-routing-role record attaches the nearest explicit source
cue to each obligation without changing established equality obligation bytes.

## Evidence

- `eq:causal-cashflow-object` extracts as
  `conditional_expectation_object` with explicit integrand and conditioning
  members.
- `eq:randomization-assumption` extracts as `conditional_independence` with
  left object, right object, and conditioning population members.
- All nine v8 labels extract exactly and carry the expected source-evidenced
  routing role.
- Cue examples include `causal object`, `assignment is independent`,
  `stock-flow identity`, `Bellman recursion`, and `transparent placeholder` or
  `initial convention`.
- Cue-free generic objects remain `unsupported_or_ambiguous` and cannot control
  routing.
- Role records bind source digest, context/cue spans and digests, and obligation
  digest; mutation controls fail closed.
- All 17 reviewed equality obligations reconstruct byte-identically under the
  existing oracle.
- Relation/role/oracle suite: `28 passed`.
- Downstream extraction/proof/tree/report suite: `79 passed`.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 03 | Nine exact typed objects and routing roles; equality identity preserved | No syntax-only role, caller promotion, or stale role binding observed | Some consumers still use lightweight targets/roles | Unify all report consumers in Phase 04 | Truth, identification, assumption satisfaction, or proof |

## Residual Risks

- The source-role cue classifier is deliberately local and closed; unseen prose
  may abstain or require registry extension.
- Non-equality targets retain empty legacy `lhs/rhs` fields; their complete
  relation lives in `normalized_target` and must be used by migrated consumers.
- Other planned relation types such as inequalities and optimization objects
  remain fail-closed unless already represented as equality-style recursions;
  the two audited P0 shapes are closed.

## Non-Claims

- A source role controls routing only.
- A stated identification assumption is not empirically satisfied.
- A conditional expectation object is not thereby identified or integrable.
- No source or publication state changed.

## Phase 04 Handoff

Rigor, audit/fix, proof, negative-evidence, and document-tree consumers can now
read one exact obligation and routing role. Phase 04 must remove decisive
lightweight/keyword paths, preserve complete multiline targets, and produce a
nine-row parity ledger including typed abstentions.
