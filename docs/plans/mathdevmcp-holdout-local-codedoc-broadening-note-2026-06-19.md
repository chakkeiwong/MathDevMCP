# MathDevMCP Holdout-Local Code-Document Broadening Note

## Date

2026-06-19

## Scope

This note records one more bounded local holdout broadening step that was only
performed because it added a **genuinely missing family** to the local holdout
tier.

It remains a local-only population and local fixture checkpoint, not
holdout-backed generalization evidence.

## What changed locally

A new local-only holdout family was added:

- `HOLDOUT-DSGE-CODEDOC-001`

This introduces a local `code_document_consistency` family into the holdout
seed, which had previously been absent from local holdout coverage.

A matching local candidate-answer fixture was also added.

## Why this addition was justified

This addition satisfies the bounded-broadening rule:

- it adds a **new local family**,
- and it adds a **new failure/judgment style** to the local tier.

So this was not “more of the same.” It was a representativeness-improving
addition.

## Current local family mix after this step

The local holdout seed now includes:

- `evidence_boundary_discipline`
- `retrieval_and_provenance`
- `numerical_oracle_parity`
- `derivation_boundary_and_abstention`
- `code_document_consistency`

The local candidate-answer fixtures now cover all currently populated local
holdout entries.

## What this still does **not** mean

This still does **not** mean:

- the holdout-local tier is fully representative,
- the benchmark has holdout-backed generalization evidence,
- workflow/gate/release integration is justified,
- the benchmark is complete.

## Why this matters

This is a stronger broadening step than a raw case-count increase because it
reduces one of the most obvious remaining local coverage asymmetries: the local
holdout tier now includes all of the major current public judgment families in
some local form.
