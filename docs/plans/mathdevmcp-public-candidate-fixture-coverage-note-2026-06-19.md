# MathDevMCP Public Candidate Fixture Coverage Note

## Date

2026-06-19

## Scope

This note records a bounded expansion of the **committed public normalized
candidate-answer fixture set**.

The purpose of this expansion is not to change public case semantics. It is to
reduce the gap between:

- the broader committed public benchmark corpus, and
- the smaller set of public cases currently exercised through deterministic
  candidate fixtures and scored reports.

## What changed

The committed public candidate fixture set now covers additional public case
families beyond the earlier small seed.

Added representative fixture coverage for:

- `DH-05-sgu-exact-manifold-blocker`
- `DH-04-bayesfilter-engineering-qualification-boundary`
- `LP-02-basis-reconciliation-audit`
- `RA-01-parser-benchmark-inventory`
- `MF-02-large-scale-lgssm-missing-data-policy`
- `DH-01-strict-nk-convergence-audit`
- `DH-02-bayesfilter-qr-value-parity`
- `LP-01-analytical-validation-lgssm`
- `DH-07-neutra-real-nk-migration-not-complete`

This broadens public scored coverage across:

- code-document consistency / blocker-preservation style cases,
- evidence-boundary discipline,
- derivation/abstention-adjacent reconciliation behavior,
- benchmark-inventory structure discipline,
- numerical-oracle parity,
- retrieval/provenance,
- migration-gate boundary behavior.

## Why this was justified

The stronger holdout-informed calibration note identified a current imbalance:

- the public tier was broader overall,
- but the public scored fixture layer was relatively sparse.

This fixture expansion directly targets that imbalance without:

- changing the public manifest contract,
- changing the scorer contract,
- changing the scored-report contract,
- or introducing gate/release semantics.

## What this does **not** mean

This expansion does **not** mean:

- the public benchmark is now complete,
- public scored coverage is fully representative,
- holdout-backed generalization is established,
- workflow or policy integration is justified.

It only means the public deterministic scored layer now covers more of the
existing public benchmark corpus than it did before.
