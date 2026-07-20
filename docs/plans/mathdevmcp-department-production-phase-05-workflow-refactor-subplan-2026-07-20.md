# P05 Subplan: Workflow And Validator Refactoring

## Objective

Decompose the document-derivation workflow and highest-risk validators into
testable stages and named rule pipelines.

## Entry Conditions

P04 dependency boundaries pass and full public contract characterization exists.

## Required Artifacts

- Separate document context-graph, orchestration, response-projection, and
  Markdown-rendering seams.
- Named rule groups for `validate_high_level_result` and Phase 06 promotion
  evaluation/verification.
- Deterministic mutation matrices and property/invariant tests preserving exact
  error ordering and verdicts.
- Before/after module/function complexity report.

## Required Checks

- Document derivation, response, red-team, credit-card parity, promotion policy,
  high-level contract, MCP, CLI, and benchmark tests.
- Golden Markdown and canonical JSON equality where persisted outputs exist.
- Coverage floors for extracted modules.

## Evidence Contract

Complexity reduction is explanatory. Promotion requires unchanged externally
observable contracts and improved independently testable rule/stage boundaries.

## Forbidden Actions

- No scientific logic simplification merely to reduce complexity.
- No change to error order, status taxonomy, claim eligibility, or publication
  default without a separate scientific/product decision.

## Handoff

P06 begins when extracted stages are behaviorally equivalent and covered.

## Stop Conditions

Golden outputs diverge or a mutation reveals the old behavior was ambiguous and
requires owner/scientific direction.
