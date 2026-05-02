# MCP interface remaining-gaps plan audit

## Audit stance

This audit treats `mcp-interface-remaining-gaps-execution-plan.md` as another
developer's plan. The goal is to catch hidden scope creep, missing tests, and
false-confidence risks before implementation starts.

## Overall assessment

The plan is justified. It targets the important gaps left by the tiered MCP
interface checkpoint and keeps the right boundary: client rules and aliases can
improve usability, but tested MCP/library contracts remain the source of truth.

The largest implementation risk is Phase 1. A real
`audit_implementation_label` spine could easily become a large product rewrite.
For this checkpoint, the implementation should be a conservative aggregator
over existing modules rather than a new verifier.

## Required execution constraints

### Keep `compare_label_code` compatible

`compare_label_code` should continue returning `label_consistency_result`.
Do not silently change its contract to the richer implementation-audit result.
Existing clients may depend on the old shape.

### Do not overclaim `audit_implementation_label`

Even if required operations are present, the result should not be `verified`.
The strongest status should be `consistent`, meaning "required structural
evidence was found." Mathematical correctness remains unverified unless a
deterministic backend proves a scoped claim.

### Use existing AST/semantic/shape modules first

Phase 1 should compose:

- `compare_label_to_code`,
- `extract_operation_graph`,
- `audit_derivation_v2_for_label`,
- `align_document_to_code`,
- `analyze_shape_semantics`.

Avoid inventing a second AST vocabulary.

### Client rules must be generated from one source

If `install-rules` is added, rules text should live in a Python module and the
Markdown docs should be checked against it. Otherwise rules drift will return.

### Alias audit should not fail on history

Historical plans and reset memos should be ignored by default. The audit should
target active docs/scripts/client rules. Generated release evidence may contain
old CLI names until evidence generation is migrated.

### Backend policy should not require external setup for base tests

Tests should pass when the isolated backend env is absent. Backend/full profile
strictness should still block missing backend envs.

### Package policy should remain conservative

Do not promote `mcp` to a base dependency in this pass. That is a maintainer
packaging decision, and the current support matrix documents MCP-facing extras.

## Missing details and fixes

1. The plan should include CLI wiring for `audit_implementation_label` only if
   needed. Since the CLI already has `compare-label-code`, this pass can keep
   MCP-only preferred naming and defer CLI aliasing.

2. The plan should mention source/path privacy for alias audits. File paths in
   reports should be repo-relative unless a user passes an external root.

3. Release-report evidence regeneration may be too expensive for this pass.
   A source-level narrative update plus sync tests is acceptable if generated
   evidence is explicitly documented as remaining CLI-compatible.

4. `lean_check` scanner improvements beyond the previous pass should be
   test-driven. Do not attempt a full Lean lexer.

## Phase-by-phase audit

### Phase 1

Proceed, but keep the scope to an aggregator contract. Do not refactor
`compare_label_to_code` internals.

### Phase 2

Proceed if the rules are schema-checked. If implementation time gets tight,
installing rules for Cursor/Copilot can still be completed because it is
self-contained.

### Phase 3

Proceed. Alias usage audit is low risk and useful for future deprecation.

### Phase 4

Proceed. Most code already behaves correctly after the previous checkpoint; the
main work is tests/docs/policy clarity.

### Phase 5

Proceed conservatively. Update active narrative and scripts if practical; avoid
manual edits to generated JSON evidence unless regenerated.

### Phase 6

Proceed. Encode the current package policy in tests and docs rather than
changing dependencies.

## Audit conclusion

Proceed with all phases. No phase is unjustified. The main guardrail is to keep
results diagnostic and compositional, not certifying.

