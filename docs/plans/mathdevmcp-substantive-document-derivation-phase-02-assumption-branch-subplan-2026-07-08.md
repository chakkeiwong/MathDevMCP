# Phase 02 Subplan: Assumption Branch Closure

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Turn deterministic obligation templates into candidate assumption branches that
are instantiated in document notation and explicitly show which derivation gap
they close.

## Entry Conditions Inherited From Previous Phase

- Semantic packets include full display source and symbol/operator inventory.
- Row-fragment blockers are recorded when full proof targets cannot be safely
  reconstructed.

## Required Artifacts

- Branch records attached to document tree roots:
  - branch id;
  - assumptions;
  - closes obligations;
  - derivation route under assumptions;
  - external-tool-first ledger with tools considered, role, availability or
    version evidence, selected route, and why any available tool was not used;
  - validation status;
  - evidence references;
  - non-minimality boundary.
- Tests requiring branch-linked assumptions for NPV, conditional expectation,
  Bellman recursion, shape/conformability, and differentiability/interchange
  routes.
- Phase result:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-02-result-2026-07-08.md`
- Phase result must include a run manifest and decision table as specified in
  the master program.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_actionable_abstentions.py tests/test_assumption_discovery.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/actionable_abstentions.py src/mathdevmcp/assumption_discovery.py`
- `git diff --check`
- Read-only review of branch contract if assumptions affect scientific claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each proposed assumption set be consumed by an agent as a possible closure route rather than a generic suggestion? |
| Baseline/comparator | Current `possible_assumption_sets` lists with limited connection to exact document variables and patch text. |
| Primary criterion | Each branch states the obligations it closes, includes a route that mentions source-local symbols/operators where available, and records branch-level external-tool-first consideration evidence. |
| Veto diagnostics | Assumption branch not tied to an obligation; no mathematical why; no derivation route; no external-tool ledger; globally minimal assumption claim. |
| Explanatory diagnostics | Template miss, ambiguous symbols, multiple sufficient branches. |
| Not concluded | Branches are sufficient candidates, not necessary or minimal assumptions unless backend-certified. |
| Artifact | Tests and Phase 02 result note. |

## Forbidden Claims Or Actions

- Do not claim proposed assumptions are globally minimal.
- Do not treat a deterministic route rule as proof.
- Do not let deterministic templates become unrecorded in-house search; each
  branch must say what external tools were considered and why they were or were
  not used.
- Do not hide ambiguity by selecting only one branch when alternatives are
  material.

## Exact Next-Phase Handoff Conditions

Advance to Phase 03 only if:

- each branch has a machine-readable closure link;
- each branch has branch-level external-tool consideration evidence;
- branch text is document-local rather than purely generic;
- tests fail if branch route or mathematical why is omitted.

## Stop Conditions

Stop if:

- branch generation requires domain knowledge not available from source spans,
  deterministic templates, or existing tools;
- assumptions would make substantive scientific claims that require user
  direction.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write the Phase 02 result / close record.
3. Draft or refresh Phase 03 subplan.
4. Review Phase 03 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
