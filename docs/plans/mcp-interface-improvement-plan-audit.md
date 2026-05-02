# MCP interface improvement plan audit

## Audit stance

This audit treats `mcp-interface-improvement-execution-plan.md` as if it were
written by another developer. The review goal is to find missing points,
overreach, hidden compatibility risks, and false-confidence paths before code
changes begin.

## Overall assessment

The plan is directionally sound. It correctly rejects the three-tool-only MCP
surface as an overcorrection while still acknowledging that the current broad
surface needs structure. The most important design choice is preserving tested
workflow tools as MCP contracts instead of moving all workflow behavior into
client-specific prose skills.

The plan is implementable against current `main`, but a few constraints should
be tightened during execution:

- current `main` already has `MCPToolSpec`; Phase 2 should extend it rather
  than rewrite it;
- FastMCP function signatures must remain schema-valid for both preferred names
  and aliases;
- deprecation metadata should not change existing result contracts unless tests
  are updated deliberately;
- document sync tests should distinguish primary workflow instructions from
  historical migration references;
- PR #1 salvage should avoid adding `.claude/` client-specific files unless
  their schema examples are synchronized with the tiered surface.

## Missing or under-specified points

### 1. Alias result metadata

The plan says deprecated aliases should return the same result shape plus
deprecation metadata "where possible." That is right, but adding fields to
existing contract payloads can break exact-shape tests or downstream clients.

Execution guidance:

- prefer registry-level deprecation metadata first;
- keep alias payloads byte-for-byte compatible unless a test explicitly allows
  a new `deprecation` field;
- if result-level deprecation is added, add it under a stable key and update
  contract tests.

### 2. Tool count target needs nuance

The final acceptance criterion says roughly 8-12 intentional tools. Current
compatibility aliases may keep the exposed server count above that temporarily.

Execution guidance:

- measure the stable preferred surface separately from deprecated aliases;
- allow compatibility aliases to exceed the target during the migration cycle;
- tests should assert stable preferred count, not total alias-inclusive count.

### 3. `audit_implementation_label` scope

The plan proposes `audit_implementation_label`, but its first implementation
could become a mere rename of `compare_label_code`. That would improve naming
but not behavior.

Execution guidance:

- in this pass, implement it as a compatibility wrapper with clear metadata;
- do not claim it is semantically stronger than `compare_label_code` until AST
  and shape evidence are integrated;
- document the hypothesis for the next pass: that `audit_implementation_label`
  should become the structured code/document semantic review spine.

### 4. `lean_check` placeholder parsing limits

Token/comment-aware placeholder detection is necessary, but Lean lexical
syntax is richer than a small custom scanner.

Execution guidance:

- implement a conservative scanner for comments, strings, and identifier
  boundaries;
- do not claim it is a complete Lean lexer;
- add tests for comments, block comments, strings, identifiers, and true
  placeholder tokens;
- keep direct Lean acceptance as the certifying backend boundary.

### 5. Documentation search can over-block

The plan proposes using `rg` so primary docs do not mention removed names except
in migration sections. Release reports and planning documents intentionally
contain historical names.

Execution guidance:

- apply the strict no-stale-primary-instruction rule to README, `mcp/README.md`,
  operator guide, generated client rules, and active skill/client docs;
- allow reset memos and historical plans to contain old names;
- add sync tests against `mcp/README.md` and active workflow rules, not every
  planning artifact.

### 6. PR #1 install-rule salvage depends on packaging policy

Adding `mathdevmcp install-rules` is useful, but it introduces generated rules
that must be kept synchronized with MCP schemas.

Execution guidance:

- implement only the non-invasive pieces in this pass if time allows:
  `.mcp.json` portability and optional client-rule docs;
- if adding `install-rules`, add source/doc sync tests in the same phase;
- do not add workflow rules that call nonexistent parameters.

### 7. Commit hygiene

The user requested a final commit. `.serena/` is untracked and must remain
uncommitted. The plan file is currently untracked and should be included.

Execution guidance:

- use `git status --short` before staging;
- stage only relevant source, tests, docs, and plan/memo artifacts;
- avoid generated PDF rebuilds unless documentation changes require them.

## Phase-by-phase audit

### Phase 1

Justified. Inventory/classification is needed, but the current registry already
contains tool names and contracts. The phase should produce code-visible
classification through registry metadata, not a separate hand-maintained table.

### Phase 2

Justified with modification. Extend `MCPToolSpec` with tier,
`certifying_capable`, `deprecated`, and `replacement`. Keep `server_name` and
`optional_capability`. Add tests for unique names, valid tiers/stabilities, and
coherent deprecations.

### Phase 3

Justified. Preferred names should be added without removing old names:
`latex_label_lookup`, `check_equality`, and `audit_implementation_label`.
FastMCP wrappers need explicit functions for schema-aware clients.

### Phase 4

Justified. `lean_check` is already exposed in current `main` only through
library tests, not MCP; adding it as a primitive requires hardening placeholder
detection first.

### Phase 5

Justified. Documentation must be updated after code changes so names and
schemas match the actual registry. It should not regenerate the full release
PDF unless required.

### Phase 6

Justified. Sync tests are the guardrail that prevents a repeat of PR #1's stale
documentation problem.

### Phase 7

Partially justified. Salvage should be conservative. `.mcp.json` portability is
low risk. `install-rules` is useful but only justified after workflow rules are
schema-valid. Promoting `mcp` to a base dependency is a product/package policy
decision; include it only if tests and release policy agree.

## Audit conclusion

Proceed with implementation. No issue makes the next phase unjustified. The key
execution discipline is to keep compatibility aliases, add metadata before
removal, and avoid letting prose skills replace tested workflow contracts.
