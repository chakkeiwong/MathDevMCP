# Phase 5 Subplan: External Adapted Pack Ingestion

## Phase Objective

Ingest small diagnostic adapted packs from locally available/provided external
benchmark sources, or write a blocker result if local source paths are absent.

## Entry Conditions Inherited From Previous Phase

- External provenance manifest/template exists.
- Seeded benchmark and quality metrics are already available.

## Required Artifacts

- Diagnostic external adapted cases or blocker result.
- Source manifests for any ingested cases.
- Per-source adaptation ledger for any ingested case family.
- Tests for adapter parsing and diagnostic execution when local samples exist.
- Phase 5 result record.
- Refreshed Phase 6 subplan.

## Required Checks, Tests, Reviews

- Source-path availability precheck.
- Manifest validation.
- Adapter tests if cases are ingested.
- No-network check by documenting all source paths as local/provided.
- `git diff --check`.
- Claude review for external-case boundary if ingestion occurs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can licensed external-style cases be ingested as diagnostic, provenance-controlled benchmark packs? |
| Baseline/comparator | Phase 4 manifest and local seeded benchmark. |
| Primary pass criterion | Either a small diagnostic adapted pack validates and runs with per-source ledgers, or a blocker record states missing local source paths/approval needs while allowing seeded-only progress. |
| Veto diagnostics | Network fetch without approval; external cases enter release gate; source transformation is undocumented; external scores are combined with formal seeded totals. |
| Explanatory diagnostics | Adapter validation and source manifest. |
| Not concluded | External leaderboard score, broad theorem proving, or public redistribution status. |
| Artifact | Diagnostic pack or blocker/result. |

## Forbidden Claims And Actions

- Do not download sources without explicit approval.
- Do not put external diagnostic cases into `benchmark_gate` by default.
- Do not claim a hard formal-proof failure is a product failure when expected
  abstention is correct.
- Do not block seeded formal gate integration solely because local external
  samples are unavailable.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 if either diagnostic external packs exist with manifests or
the absence of local source paths is recorded as a non-blocking seeded-only
condition.

## Stop Conditions

Stop only for the external ingestion path if ingestion requires
network/credentials or if local source material cannot be represented without
violating privacy/redistribution boundaries. Continue seeded-only execution if
the blocker is merely absent local external samples.
