# Phase 10 Subplan: Final Regression And Handoff

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Run final focused regressions, write the final source-adapter report and visible
handoff, and state exactly what was and was not concluded.

## Entry Conditions Inherited From Previous Phase

Phase 09 has exposed the local source-adapter report through CLI/docs without
changing release gates or public benchmark policy.

## Required Artifacts

- Final local source-adapter JSON report under `.mathdevmcp/`.
- Final Phase 10 result record.
- Visible stop handoff.
- Updated execution ledger and Claude review trail.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py tests/test_release_smoke.py`
- `python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD"`
- `python3 -m mathdevmcp.cli real-local-high-level-pilot --root "$PWD"`
- `python3 -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"`
- `python3 -m mathdevmcp.cli benchmark-gate --root "$PWD"` as existing-suite regression observation only.
- Claude final read-only review of the final interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did the program complete the five source-adapter obligations while preserving all evidence boundaries? |
| Baseline/comparator | Phase 00 baseline: five adapter-required source obligations. |
| Primary pass criterion | Focused tests pass; source-adapter CLI passes with five source results and zero residual adapter-required gaps; pilot CLI still separates probe/source channels; final handoff records non-claims. |
| Veto diagnostics | Any aggregate source/probe accuracy; adapter report used as benchmark-gate evidence; failed focused tests; unsupported release/scientific/broad proof claim. |
| Explanatory diagnostics | Test output, CLI summaries, benchmark-gate observation, Claude final review. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, production implementation correctness, full LaTeX proof checking. |
| Artifact | Phase 10 result and visible stop handoff. |

## Forbidden Claims / Actions

- Do not claim release readiness or external benchmark validity.
- Do not claim broad theorem proving or full LaTeX derivation competence.
- Do not claim neighboring source documents or production code are globally
  correct.
- Do not modify gates after seeing final results.

## Exact Next-Phase Handoff Conditions

There is no next phase. Completion handoff must list final status, tests, report
paths, unresolved risks, non-claims, and any justified next program.

## Stop Conditions

Stop and write a blocker result if final focused tests fail, source-adapter
report has residual unhandled gaps, Claude/Codex final review does not converge
after five rounds, or a human-required boundary appears.

## Phase-End Protocol

At phase end: run required local checks; write Phase 10 result; write the final
visible handoff; review final interpretation for consistency, correctness,
artifact coverage, and boundary safety.
