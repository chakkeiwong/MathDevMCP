# Phase 8 Subplan: Prepare Review Packet Workflow

## Phase Objective

Implement `prepare_review_packet(question, evidence)` for review-ready
question-level answers.

## Entry Conditions Inherited From Previous Phase

- Contract, kernel, and all preceding high-level workflows exist.
- Low-level math review packet builder is available.

## Required Artifacts

- `prepare_review_packet` function.
- Tests for proof preservation, refutation blocking, missing assumptions,
  structural/numeric diagnostic boundaries, and human-review action items.
- Rubric tests for evidence completeness, provenance, uncertainty/actionability,
  and boundary preservation.
- Phase 8 result record.
- Refreshed Phase 9 subplan.

## Required Checks, Tests, Reviews

- Workflow tests.
- Contract/kernel tests.
- Low-level review packet tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow aggregate evidence into a useful review packet without turning diagnostics into certificates? |
| Baseline/comparator | Direct `build_math_review_packet` outputs and high-level workflow envelopes. |
| Primary pass criterion | Packet preserves certified/refuted/diagnostic/missing-assumption evidence classes and action items; success is scored on evidence completeness, provenance, uncertainty/actionability, and boundary preservation rather than answer-string matching. |
| Veto diagnostics | Review packet called proof certificate; refutation hidden; missing assumptions hidden. |
| Explanatory diagnostics | Packet sections and action list. |
| Not concluded | Human approval or final mathematical publication correctness. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not call packet generation a proof.
- Do not remove negative evidence from packet summaries.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 9 if all high-level workflows exist and return compliant
contract envelopes.

## Stop Conditions

Stop if aggregation cannot preserve negative and diagnostic evidence.
