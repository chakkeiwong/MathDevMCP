# Phase 01 Subplan: Page-Aware Evidence Packets

## Objective

Turn source input into page/block/equation evidence packets without claiming
that parser output is faithful mathematics.

## Entry Conditions

Phase 00 baseline is frozen and the current source digest can be reproduced.

## Required Artifacts

`src/mathdevmcp/applied_math_ir.py`, packet schema tests, and a Phase 01 result.

## Required Checks/Tests/Reviews

Test multi-page text, form-feed page boundaries, LaTeX equation labels and line
anchors, missing page identity, source-change detection, and parser limitation
propagation. Review that every packet retains a raw source reference.

## Evidence Contract

Packets preserve source digest, parser/provider, page or line, character span,
raw text, candidate kind, and confidence. Candidate equations remain
non-certifying.

## Forbidden Claims/Actions

No OCR-to-equation invention, parser merging without attribution, or dropped
page identity.

## Exact Handoff Conditions

PDF and TeX fixtures produce deterministic packets; malformed or changed input
fails visibly; Phase 02 can consume packets without reparsing raw text.

## Stop Conditions

Stop if a packet cannot be traced back to a source location or provider failure
is hidden.
