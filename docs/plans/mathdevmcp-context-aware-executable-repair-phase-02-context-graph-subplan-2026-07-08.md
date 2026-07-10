# Phase 02 Subplan: Local Mathematical Context Graph

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Build a deterministic context graph around each target so the tool can separate
stated, inferred, missing, and unresolved assumptions.

## Entry Conditions Inherited From Previous Phase

- Proposition/context packets exist for proposition labels and display-equation
  labels.
- Source spans preserve parent proposition, equations, statement text, and
  proof/context snippets.

## Required Artifacts

- Context graph records for definitions, hypotheses, referenced equations,
  notation declarations, symbols, operators, and candidate assumptions.
- Status fields: `stated`, `nearby_stated`, `inferred_candidate`,
  `missing`, `unresolved`.
- Tests on `prop:interior-foc` showing interiority/differentiability are
  stated, while expectation-interchange/integrability remains missing or
  unresolved.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-02-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_assumption_discovery.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/assumption_discovery.py`
- `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow avoid proposing assumptions that are already stated nearby? |
| Baseline/comparator | Current branch generation proposes sufficient assumptions without a local context graph. |
| Primary criterion | Context graph marks at least one proposition-stated assumption as stated and at least one route-required condition as missing/unresolved. |
| Veto diagnostics | All assumptions marked missing; all assumptions marked stated without evidence; no source references. |
| Explanatory diagnostics | Ambiguous wording, missing definitions, macro-only symbols. |
| Not concluded | Context graph statuses are diagnostics, not proof of adequacy. |
| Artifact | Tests and Phase 02 result. |

## Forbidden Claims Or Actions

- Do not claim a stated assumption is sufficient unless the derivation branch
  closes under backend evidence.
- Do not use agent judgment without source references.

## Exact Next-Phase Handoff Conditions

Advance to Phase 03 only if context graph entries can feed typed obligations
with source evidence and assumption status.

## Stop Conditions

Stop if source evidence cannot distinguish stated from missing assumptions for
the frozen risky-debt proposition.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 02 result / close record.
3. Draft or refresh Phase 03 subplan.
4. Review Phase 03 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
