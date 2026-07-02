# Phase 5 Subplan: Math-To-Code Trace Artifacts

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Make math-to-code audits produce traceability artifacts that map documented
math terms to code operations, missing terms, aliases, and audit-only extras.

## Entry Conditions

- Phase 4 route artifacts are available for review packet reuse as diagnostic
  evidence separate from certifying proof/refutation evidence.
- Existing math-to-code tests pass.
- Derivation route plans are diagnostic trace context only and must not be
  treated as proof that code implements the documented math.

## Required Artifacts

- Updated `src/mathdevmcp/audit_math_to_code.py`,
  `src/mathdevmcp/equation_code_match.py`,
  `src/mathdevmcp/agent_workflows.py`, and/or
  `src/mathdevmcp/operation_consistency.py`.
- Focused tests in `tests/test_audit_math_to_code.py` and
  `tests/test_agent_workflows.py`.
- Phase 5 result record.
- Refreshed Phase 6 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_audit_math_to_code.py tests/test_agent_workflows.py tests/test_equation_code_match.py`
- `git diff --check` over touched files.
- Claude read-only review for semantic-boundary changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can code audits show exactly which documented terms are matched, missing, aliased, or extra? |
| Baseline/comparator | Existing structural audit behavior, Phase 4 route-plan artifacts, and benchmark case RLHLB-06. |
| Primary criterion | Outputs include a trace map and preserve structural-only boundary. |
| Veto diagnostics | Structural match claimed as semantic proof; missing term hidden by alias; equivalent implementation ruled out without trace. |
| Explanatory diagnostics | Term map, alias map, missing/extra operation lists. |
| Not concluded | No proof that code is mathematically correct or incorrect globally. |

## Forbidden Claims/Actions

- Do not treat structural evidence as semantic proof.
- Do not claim whole-codebase correctness or falsity.
- Do not execute untrusted generated code.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only if math-to-code trace outputs can be embedded in review
packets without being promoted to proof.

## Stop Conditions

Stop if source/code trace semantics are ambiguous enough that a human decision
is required, or if tests need runtime execution outside safe local fixtures.
