# Phase 3 Result: Apply To Credit-Card NPV Document

Date: 2026-07-07

Status: `PASSED_AFTER_REPAIR`

## Objective

Run the new document-rigor workflow on the credit-card NPV final submission and
generate agent-consumable JSON and Markdown rigor reports.

## Target

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`

## Generated Artifacts

- `docs/reviews/credit-card-npv-component-proposal-rigor-audit.md`
- `docs/reviews/credit-card-npv-component-proposal-rigor-audit.json`
- Log: `/tmp/mathdevmcp-rigor-logs/credit-card-rigor-audit.log`

## Run Command

```text
python3 -m mathdevmcp.cli audit-math-document-rigor docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex --focus-label eq:proposal-objective --focus-label eq:panel-npv-functional --focus-label eq:incremental-npv --focus-label eq:ss-bellman --focus-label eq:experiment-npv-estimand --focus-label eq:policy-value-estimator --output-md docs/reviews/credit-card-npv-component-proposal-rigor-audit.md --output-json docs/reviews/credit-card-npv-component-proposal-rigor-audit.json --validation-backend lean --validation-backend sage --validation-backend sympy
```

## Repair During Phase

The first run exposed two veto diagnostics:

1. backend provenance recorded `backend_env` but still ran `doctor` in active
   Python, so LeanDojo appeared unavailable;
2. delegated explicit-label auditing used the whole target folder and could
   pick duplicate labels from older proposal versions.

Repairs:

- `audit_math_document_rigor` now scopes `MATHDEVMCP_BACKEND_CONDA_ENV` while
  running backend provenance.
- delegated `audit_and_propose_fix` now runs against a temporary single-file
  audit root copied from the exact target `.tex` file.
- regression tests cover both issues.

## Report Summary

From `docs/reviews/credit-card-npv-component-proposal-rigor-audit.json`:

- contract: `math_document_rigor_audit`;
- target file: `credit_card_npv_component_proposal_final_submission.tex`;
- selected equation rows: `6`;
- available labeled equation rows: `214`;
- coverage status: `partial_coverage`;
- gaps: `21`;
- proposals: `21`;
- LeanDojo status: available in backend Python;
- LeanDojo backend env: `mathdevmcp-backends`;
- LeanDojo version: `4.20.0`.

## Local Checks

Report shape summary:

- JSON contract is `math_document_rigor_audit`;
- Markdown includes backend provenance, tool uses, locations, problems, why
  fields, and proposed fixes;
- all inspected gap locations in the sampled summary point to
  `credit_card_npv_component_proposal_final_submission.tex`;
- Markdown records `exact_file_root: temporary_single_file_copy`.

Target source mutation check:

- `git diff -- docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`
- Result: empty.

Focused tests after final target-selection repair:

- `python3 -m pytest -q tests/test_math_document_rigor.py tests/test_math_document_rigor_interfaces.py`
- Result: `10 passed in 224.03s`

Final artifact verification:

- selected labels:
  `eq:proposal-objective`, `eq:panel-npv-functional`,
  `eq:incremental-npv`, `eq:ss-bellman`,
  `eq:experiment-npv-estimand`, `eq:policy-value-estimator`;
- no duplicate `eq:ss-bellman` selected target remained;
- no sibling draft filename hits were found in the generated Markdown report;
- target source mutation check remained empty.

## Gate Assessment

Primary criterion:

- Met after repair for the selected-label application scope: the generated
  JSON/Markdown reports exist and include concrete locations, problems,
  mathematical rationale, proposed fixes, backend provenance, and explicit
  partial coverage.

Veto diagnostics:

- Report is handwavy: not observed for selected labels; entries include
  location/problem/why/fix.
- Report omits locations: not observed.
- Target source modified: not observed.
- LeanDojo proof-search promoted to certificate: not observed.
- Folder duplicate versions included by mistake: repaired and regression tested.

## Non-Claims

- The report is partial coverage, not full-document proof.
- The report does not scientifically validate the NPV model.
- The report does not certify product capability.
- LeanDojo availability is not a proof certificate.

## Next Handoff

Proceed to Phase 4 regression, review, and handoff.
