# Phase 4 Subplan: External Source Provenance Protocol

## Phase Objective

Create the manifest/template protocol for licensed external benchmark adapters
without fetching or redistributing external data.

## Entry Conditions Inherited From Previous Phase

- Seeded benchmark quality metrics exist.
- External cases remain diagnostic until promotion criteria are satisfied.

## Required Artifacts

- External adapted benchmark manifest schema/template.
- Documentation of source families, transformation fields, gating status, and
  redistribution boundary.
- Adaptation ledger template requiring source family, original id, local path,
  oracle class, transformation notes, source-specific caveats, and review
  status.
- Tests for manifest validation.
- Phase 4 result record.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- Manifest validation tests.
- Docs grep for forbidden release/leaderboard claims.
- `git diff --check`.
- Claude review for provenance/gating boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can licensed external benchmark sources be represented safely before ingestion? |
| Baseline/comparator | Current private corpus manifest style and benchmark manifest. |
| Primary pass criterion | Manifest distinguishes source, original id, local path, license statement, transformation notes, oracle class, source-specific caveats, privacy, redistribution, review status, and gate status. |
| Veto diagnostics | External cases become gated without deterministic oracle; license statement substitutes for missing provenance; data fetched without approval; aggregate external score hides source heterogeneity. |
| Explanatory diagnostics | Manifest validation output and docs. |
| Not concluded | Any external case quality or benchmark score. |
| Artifact | Manifest/template/tests/result. |

## Forbidden Claims And Actions

- Do not fetch external data.
- Do not commit restricted external content unless explicitly approved and
  marked redistributable.
- Do not treat academic license coverage as public redistribution permission.
- Do not combine external source families into one aggregate score or rank.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 if local/provided external sources can be represented or a
clear blocker protocol exists for missing local source paths.

## Stop Conditions

Stop if provenance fields cannot represent source/license/transformation
boundaries or if ingestion would require unapproved network access.
