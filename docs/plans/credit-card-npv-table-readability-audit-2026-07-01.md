# Credit Card NPV Proposal Table Readability Audit

Date: 2026-07-01

## Baseline

The proposal contains many tables and longtables. Several are necessary as
contract or audit ledgers, but a human reader should not have to infer the
argument from dense cells.

## Table Categories

| Category | Examples | Treatment |
|---|---|---|
| Exposition support | Macro evidence-to-model, usage evidence-to-model, component outputs | Keep only after prose explanation. |
| Contract summaries | Decision-context, valuation semantics, request, response, status, operating modes | Keep; add prose before table and split later if too dense. |
| Governance/migration artifacts | Governance, migration, experiment contract | Keep as audit artifacts; prose first. |
| Source/claim ledgers | Claim-support and source-support ledgers | Keep in appendix only; dense by design. |

## Required Readability Rules

1. No dense table should introduce a concept for the first time.
2. Every longtable should have prose immediately before it explaining how to
   read it.
3. Contract tables should be followed by a short paragraph stating the key
   operating implication.
4. Audit ledgers should be labeled as appendices or reference artifacts.

## Immediate Hardening Action

Add prose-first notes around new data inventories and worked contracts. Do not
turn the new sections into table-only exposition.
