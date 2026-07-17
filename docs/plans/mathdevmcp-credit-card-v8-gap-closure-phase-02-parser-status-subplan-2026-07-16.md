# Phase 02 Subplan: Parser Status And Provenance

## Phase Objective

Separate accepted exact-source binding from specialist parser readiness so a
duplicate corpus cannot overwrite a validated label with a false missing-label
status.

## Entry Conditions Inherited From Previous Phase

- Exact selector parity passes Phase 01.
- Proof packets reproduce `inconclusive:source_label_missing` despite exact
  source provenance.

## Required Artifacts

- Explicit `source_binding_status` and `specialist_parser_readiness` fields.
- Corrected proof, negative-packet, audit/fix, and rigor status propagation.
- `mathdevmcp-credit-card-v8-gap-closure-phase-02-result-2026-07-16.md`.

## Required Checks

- Nine exact v8 packets accept source binding.
- True absent labels retain a missing-label status.
- Context-only parser readiness remains non-certifying and names its limit.
- Parser-policy, proof-audit, packet, and grouped-order tests.

## Evidence Contract

- Pass: source provenance, status, blocker, and next action agree.
- Veto: exact accepted source is reported absent or parser readiness is
  reported as mathematical verification.
- Non-claim: parser readiness does not certify a mathematical statement.

## Forbidden Claims And Actions

- Do not hide corpus ambiguity; retain it in a separate diagnostic ledger.
- Do not upgrade `unverified` to `verified` merely by correcting false status.

## Exact Next-Phase Handoff Conditions

Phase 03 may start when the nine exact packets have truthful source and parser
substatuses and missing-label controls remain intact.

## Stop Conditions

Stop if the status taxonomy cannot distinguish provenance from capability
without breaking preserved public status semantics.
