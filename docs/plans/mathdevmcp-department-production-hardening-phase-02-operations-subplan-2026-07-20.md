# Phase 02 Department Corpus, Security, And Operations

## Objective

Convert trusted internal-beta assumptions into an explicit department support
boundary with approved corpus validation, security checks, ownership, and
rollback evidence.

## Entry Conditions

Phase 01 produces a reproducible wheel and release identity.

## Required Artifacts

- Approved external sanitized/private corpus manifest, or an explicit signed
  decision excluding private-document support from the release claim.
- Department support matrix and owner/escalation record.
- Security checklist: path confinement, private-path redaction, subprocess
  timeout, secret scan, dependency scan, license inventory, and SBOM.
- Incident, retention, backup/rollback, and uninstall/revocation procedures.
- Stable MCP profile definition with explicit experimental opt-in.

## Checks

- `validate_private_corpus.sh` and private/full release profiles when claiming
  department-document support.
- Redaction and path-confinement negative tests.
- Vulnerability/license/secret/SBOM tools when available; record unavailable
  tools and do not silently call them passed.
- Install, rollback, and client-configuration rehearsal.
- Verify experimental tools are not represented as stable support.

## Evidence Contract

The primary question is operational safety and supportability, not mathematical
correctness. A missing scanner or private corpus is a release residual, not a
pass.

## Forbidden Claims/Actions

- Do not expose the MCP as a network service under this phase.
- Do not transmit private documents to external services.
- Do not treat redaction tests as authorization to include private data.

## Handoff Conditions

The department owner signs the deployment boundary and either supplies the
approved corpus manifest or explicitly narrows the support claim.

## Stop Conditions

Stop for missing data/privacy authority, scanner absence without an approved
fallback, or any request for shared-service exposure.
