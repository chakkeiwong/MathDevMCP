# Phase 03 Subplan: Formalization Stub And Backend Attempt Integration

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Generate bounded formalization stubs for SymPy, Sage, and Lean when the
semantic packet and branch assumptions provide enough structure, and record
precise blockers when they do not.

## Entry Conditions Inherited From Previous Phase

- Candidate assumption branches exist and name the obligations they close.
- External-tool-first policy remains active for derivation/proof/search paths.

## Required Artifacts

- Formalization stub records:
  - target backend;
  - generated source or expression;
  - assumptions encoded;
  - unsupported symbols/operators;
  - validation status;
  - evidence references;
  - certification boundary.
- Adapter integration that attempts only bounded checks and records diagnostic
  evidence when stubs are not certifying.
- Tests with mocked backend runners and no required network/install.
- Phase result:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-03-result-2026-07-08.md`
- Phase result must include a run manifest and decision table as specified in
  the master program.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_external_tool_adapters.py tests/test_derivation_branch_controller.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_branch_controller.py`
- `git diff --check`
- Optional real backend smoke only if already installed and bounded.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the tool show the next concrete backend check instead of saying only "formalize the claim"? |
| Baseline/comparator | Current backend attempts often receive raw LaTeX fragments and return diagnostic blockers. |
| Primary criterion | For each supported branch, report includes a backend-specific stub or an explicit unsupported-formalization blocker. |
| Veto diagnostics | Stub represented as proof; backend unavailability treated as refutation; unbounded backend command; missing tool/version evidence. |
| Explanatory diagnostics | Missing Lean project context, unsupported stochastic operator, unsupported macro, timeout. |
| Not concluded | Stub generation is not formal proof unless the certifying backend verifies it. |
| Artifact | Tests, bounded adapter evidence, and Phase 03 result note. |

## Forbidden Claims Or Actions

- Do not call LeanDojo/Pantograph/LeanSearch as certifying backends.
- Do not require package installation in this phase without explicit approval.
- Do not run long proof search or network fetches.

## Exact Next-Phase Handoff Conditions

Advance to Phase 04 only if:

- formalization blockers are specific and actionable;
- stub-only evidence cannot promote a branch;
- available backend attempts are captured as bounded evidence objects.

## Stop Conditions

Stop if:

- a backend call cannot be bounded by timeout or artifact capture;
- environment setup is required before a useful stub contract can be tested;
- proof-claim boundaries would need weakening to produce a nicer report.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write the Phase 03 result / close record.
3. Draft or refresh Phase 04 subplan.
4. Review Phase 04 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
