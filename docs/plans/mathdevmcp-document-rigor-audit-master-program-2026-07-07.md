# Math Document Rigor Audit Master Program

Date: 2026-07-07

Status: `EXECUTED_WITH_BOUNDED_NON_CLAIMS`

## Objective

Build a reusable Python workflow that audits a substantial LaTeX mathematical
document and produces an agent-consumable rigor gap/proposal report.

The first real target document is:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`

The workflow must produce structured JSON and Markdown reports that make clear:

- where a problem occurs;
- what the problem is;
- why it is mathematically or evidentially a problem;
- what concrete repair is proposed;
- what assumptions or formalization route would close the gap;
- which deterministic tools were used;
- what was not proved or concluded.

## Role Contract

Codex is supervisor and executor.

Claude may be used only as a read-only reviewer for material plans, subplans,
implementation diffs, result records, and blocker plans. Claude is not an
execution authority and cannot approve crossing human, runtime, model-file,
funding, product-capability, release, public-benchmark, or scientific-claim
boundaries.

## Baseline

Current relevant tool surface includes:

- equation localization: `locate_equations_in_file`;
- backend provenance: `doctor_report`, `lean_readiness`;
- assumption discovery: `assumptions_for`, `audit_and_propose_assumptions`;
- derivation routes: `derive_from`, `derive_or_refute`,
  `audit_and_propose_derivations`, `audit_and_propose_fix`;
- typed diagnostics: `typed_obligation_label`;
- direct proof checking: `lean_check`;
- optional proof-search environment: LeanDojo in isolated backend env
  `mathdevmcp-backends`, with direct Lean check required for certification.

Recent diagnostic fix: `doctor` and `lean_readiness` distinguish active Python
from backend Python so LeanDojo unavailable in the active env is not mistaken
for machine-level unavailability.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, Plan Review, And Launch | `docs/plans/mathdevmcp-document-rigor-audit-phase-00-governance-review-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-00-governance-review-result-2026-07-07.md` |
| 1 | Core Python Workflow MVP | `docs/plans/mathdevmcp-document-rigor-audit-phase-01-core-workflow-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-01-core-workflow-result-2026-07-07.md` |
| 2 | CLI And MCP Exposure | `docs/plans/mathdevmcp-document-rigor-audit-phase-02-cli-mcp-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-02-cli-mcp-result-2026-07-07.md` |
| 3 | Apply To Credit-Card NPV Document | `docs/plans/mathdevmcp-document-rigor-audit-phase-03-credit-card-application-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-03-credit-card-application-result-2026-07-07.md` |
| 4 | Regression, Review, And Handoff | `docs/plans/mathdevmcp-document-rigor-audit-phase-04-regression-closeout-subplan-2026-07-07.md` | `docs/plans/mathdevmcp-document-rigor-audit-phase-04-regression-closeout-result-2026-07-07.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP provide a reusable Python workflow that turns a large mathematical LaTeX document into a structured rigor gap/proposal report? |
| Baseline/comparator | Current manual process plus existing low/high-level tools listed above. |
| Primary pass criterion | The workflow produces valid JSON and readable Markdown with backend provenance, partial-coverage metadata, tool-use ledger, and concrete gap/proposal entries for the target document. |
| Veto diagnostics | Yes/no-only output; missing locations; missing mathematical rationale; hidden environment scope; LeanDojo treated as proof certificate; no partial-coverage warning; source edits made to the target document during audit; unsupported product/scientific/release claims. |
| Explanatory diagnostics | Focused unit tests, CLI smoke, MCP facade/server parity checks, generated credit-card NPV audit artifacts, Claude read-only reviews. |
| Not concluded | The document is not proved correct; the NPV model is not scientifically validated; credit-card product capability is not certified; LeanDojo search traces are not certificates; partial coverage is not full-document rigor. |
| Artifacts | Master program, subplans, visible runbook, ledger, review trail, phase results, source/test diffs, generated JSON/Markdown audit reports. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start with focused label coverage | Large target document has 214 labeled rows | Keeps first report inspectable and prevents noisy whole-document false confidence | Important sections omitted or coverage mistaken as complete | Coverage table and explicit `partial_coverage` status | Reviewed baseline |
| Use existing tools as subcalls | Current MathDevMCP workflow surface | Avoids reinventing parsers/provers and preserves deterministic evidence contracts | Tool output too low-level or missing concrete proposals | Per-gap renderer requires location/problem/why/fix fields | Reviewed default |
| Treat LeanDojo as proof search only | LeanDojo policy and direct Lean boundary | Prevents proof-search trace from becoming certificate | Agent claims LeanDojo proved a result without direct `lean_check` | Report has separate proof-search and certification fields | Reviewed default |
| Do not edit target LaTeX in audit phase | User asked for report/application first | Keeps audit reproducible and non-destructive | Audit silently changes document | Phase 3 checks `git diff -- docs/...final_submission.tex` | Reviewed default |
| Expose CLI/MCP after library tests | Existing project pattern | Keeps Python contract stable before interface expansion | Interface diverges from library contract | CLI/MCP tests compare contract names and artifacts | Hypothesis |

## Phase-End Protocol

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. run Claude read-only review for material subplans/results when available;
6. patch fixable issues visibly and rerun focused checks;
7. stop after five Claude review rounds for the same blocker.

## Forbidden Claims And Actions

- Do not claim full proof of a document.
- Do not claim scientific validity, product readiness, release readiness, or
  public benchmark validity.
- Do not use LeanDojo as certification without direct Lean checking.
- Do not hide backend environment scope.
- Do not edit the target credit-card NPV LaTeX source during audit phases.
- Do not mutate unrelated dirty worktree changes.
- Do not install packages, fetch network resources, or run destructive git
  commands without explicit user approval.

## Overall Stop Conditions

Stop and write a visible handoff if:

- required local tests fail in a way that invalidates the current phase;
- a source/document edit boundary is crossed unintentionally;
- Claude and Codex do not converge after five rounds on the same material
  blocker;
- a package/network/runtime/human-decision boundary is required;
- generated reports cannot preserve location/problem/why/fix/tool-use fields.
