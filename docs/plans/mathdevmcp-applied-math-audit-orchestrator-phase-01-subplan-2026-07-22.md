# Phase 01 Subplan: Discipline-Neutral Applied-Math IR

## Objective

Represent PDF, LaTeX, code, and data inputs as source-bound records and retain
equation/section/claim objects without pretending extraction is proof.

## Entry Conditions

Phase 0 baseline, API, evidence contract, and skeptical audit are closed.

## Required Artifacts

`src/mathdevmcp/applied_math_audit.py`, schema tests, source-digest fixtures,
and a phase result note.

## Required Checks

Schema validation, deterministic source identity, LaTeX equation/label capture,
PDF extraction limitation preservation, invalid-input handling, and compact /
detailed artifact reconstruction.

## Evidence Contract

Raw source text, PDF parser output, normalized objects, and later backend output
must carry distinct evidence tiers and source references.

## Forbidden Claims/Actions

No OCR-to-LaTeX certification, no inferred equation creation from keywords, no
source edits, and no specialist invocation from this phase.

## Handoff Conditions

The IR can represent a PDF-only input and a structured LaTeX input; the source
digest and extraction status survive in the detailed artifact.

## Stop Conditions

Stop if source spans/digests cannot be retained or compact output cannot resolve
the detailed artifact.
