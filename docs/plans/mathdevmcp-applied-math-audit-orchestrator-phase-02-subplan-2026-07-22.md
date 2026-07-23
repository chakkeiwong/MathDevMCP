# Phase 02 Subplan: Obligation Generation And Coverage

## Objective

Generate discipline-neutral obligation families and ensure every selected
obligation has an explicit disposition in the report.

## Entry Conditions

Phase 01 IR and artifact tests pass.

## Required Artifacts

Obligation catalog, disposition taxonomy, coverage projection, fixtures, and a
phase result note.

## Required Checks

Coverage conservation, stable IDs, duplicate detection, no-text extraction
abstention, unsupported-family handling, and response-size checks.

## Evidence Contract

`not_checkable`, `extraction_blocked`, `backend_abstention`, and
`not_applicable` are valid outcomes, not hidden failures or successes.

## Forbidden Claims/Actions

Do not treat keyword hits as defects, raw finding count as recall, or unresolved
obligations as consistent.

## Handoff Conditions

The compact projection reports counts and artifact handles; detailed records
reconstruct all obligations and dispositions exactly.

## Stop Conditions

Stop if an applicable obligation can disappear from compact or detailed output.
