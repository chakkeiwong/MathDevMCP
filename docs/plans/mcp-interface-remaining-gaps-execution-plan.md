# MCP interface remaining-gaps execution plan

## Motivation

The previous MCP interface checkpoint replaced the proposed three-tool-only
surface with a tiered interface. It preserved tested workflow contracts, added
preferred names, kept compatibility aliases, hardened `lean_check`, and
introduced documentation sync tests.

That checkpoint intentionally left several gaps:

1. `audit_implementation_label` is still behavior-compatible with
   `compare_label_code`, not a full implementation-audit spine.
2. Client-rule installation from PR #1 was deferred because the rules must be
   rewritten for the tiered interface and schema-tested.
3. Deprecated MCP aliases remain exposed for migration.
4. Lean/backend profile readiness is still environment-coupled.
5. Release-report generated evidence and examples still need preferred-name
   alignment.
6. `lean_check` placeholder detection is conservative, not a full Lean lexer.
7. Package policy for the `mcp` dependency remains explicit but undecided.
8. Claude/Cursor/Copilot workflow guidance should supplement, not replace,
   tested MCP workflow contracts.

This plan addresses all of those gaps with conservative, measurable slices.

## Safety invariant

No parser output, AST match, inferred type, dimension hint, route hint, shape
guard, generated client rule, Lean placeholder scan, backend environment check,
benchmark pass, or MCP wrapper may become a verified mathematical claim unless
a deterministic backend verifies the claim under explicit assumptions and
MathDevMCP records reproducible evidence.

## Phase 1: implementation-audit spine

### Goal

Make `audit_implementation_label` more than a rename by returning a structured
implementation-audit packet that combines:

- labeled document context,
- legacy term comparison,
- proof-audit v2 evidence when available,
- AST operation graph evidence,
- semantic operation alignment,
- shape semantic diagnostics,
- severity-ranked actions,
- explicit diagnostic-only status.

### Implementation instructions

Add a module such as `src/mathdevmcp/implementation_audit.py` with
`audit_implementation_label(...)`.

The function should:

1. accept `root`, `label`, `code_path`, `before`, `after`,
   `paragraph_context`, `required_terms`, and optional `required_operations`;
2. reuse `compare_label_to_code(...)` for backward-compatible term evidence;
3. parse the code through `build_operation_graph_from_code` or equivalent AST
   graph API;
4. call `audit_derivation_v2_for_label(..., summary_only=False)` when possible;
5. call `align_document_to_code(...)`;
6. call `analyze_shape_semantics(...)`;
7. aggregate status conservatively:
   - `mismatch` if required terms/operations are missing,
   - `unverified` if evidence is diagnostic-only or shape policies are missing,
   - `consistent` only if required evidence is present and no high-severity
     diagnostic gap is found,
   - never `verified`;
8. attach a new contract, for example `implementation_audit_result`.

Update MCP `audit_implementation_label` to call this new function. Keep
`compare_label_code` as the legacy alias returning the old
`label_consistency_result` contract for compatibility.

### Tests

Add tests for:

- missing solve/logdet-like operation produces `mismatch`;
- good state-space fixture produces `unverified` or `consistent` with AST
  evidence, not `verified`;
- result includes nested contracts for term comparison, AST graph, semantic
  alignment, and shape semantics;
- MCP facade and FastMCP wrapper expose the new contract;
- `compare_label_code` remains backward-compatible.

## Phase 2: schema-checked client rules and install command

### Goal

Adopt the useful PR #1 `install-rules` idea, but generate rules for the tiered
interface and test that the rules mention only real tools and parameters.

### Implementation instructions

Add:

- `src/mathdevmcp/_workflow_rules.py`,
- `src/mathdevmcp/_install_rules.py`,
- CLI subcommand `mathdevmcp install-rules <cursor|copilot|all>`,
- `docs/clients/workflow-rules.md`,
- `docs/clients/cursor.md`,
- `docs/clients/github-copilot.md`.

Rules must prefer:

- `latex_label_lookup(root, label, before?, after?, cache?)`,
- `check_equality(lhs, rhs, assumptions?, backend?)`,
- `lean_check(source, timeout_seconds?, allow_sorry?)`,
- `audit_derivation_v2_label(...)`,
- `audit_implementation_label(...)`,
- `benchmark_gate(...)`,
- `release_readiness(...)`.

Rules must not call nonexistent parameters such as
`paragraph_context=true` on `latex_label_lookup`.

### Tests

Add tests for:

- idempotent install behavior,
- dry-run behavior,
- parent directory creation,
- `all` expansion and deduplication,
- docs rules matching the package rules string,
- all rule-mentioned MCP tool names exist in `MCP_TOOL_SPECS`,
- all documented call examples use schema-valid parameters.

## Phase 3: deprecated alias usage audit

### Goal

Keep aliases for migration but make usage visible and retirement measurable.

### Implementation instructions

Add a small module such as `src/mathdevmcp/mcp_alias_audit.py` that scans
active docs/scripts for deprecated MCP names and returns:

- deprecated name,
- preferred replacement,
- file,
- line,
- context,
- classification: migration section, generated evidence, active instruction.

Expose it through CLI only, unless an MCP use case is clear:

```bash
python -m mathdevmcp.cli audit-mcp-aliases --root .
```

Do not fail on historical planning documents or generated evidence by default.
Fail only on active instruction locations.

### Tests

Add tests that:

- migration-table references are allowed,
- active instruction references are findings,
- historical `docs/plans` references are ignored by default,
- the CLI returns JSON with a stable contract.

## Phase 4: backend and Lean environment policy

### Goal

Separate base/public release checks from strict backend checks and make Lean
toolchain failures consistently diagnostic unless direct Lean rejects a source.

### Implementation instructions

The previous pass already made Lean toolchain/download failures inconclusive.
This phase should add explicit policy docs and a small release-report helper:

- base/public profiles do not require `mathdevmcp-backends`;
- backend/full profiles block if the backend env is missing;
- tests must be environment-aware;
- `lean_check` should continue to classify unavailable toolchains as
  `inconclusive`, not `mismatch`.

Update docs:

- support matrix,
- maintainer guide,
- operator guide if needed.

### Tests

Add or adjust tests so:

- base release can be `ready_with_caveats` with missing backend env;
- backend profile reports a clear blocker if backend env is missing;
- backend profile passes if backend env is configured in environments that have
  it;
- Lean toolchain download failures remain `inconclusive`.

## Phase 5: release evidence preferred names

### Goal

Stop new release-facing examples from teaching legacy MCP names.

### Implementation instructions

Update evidence generation code or committed snippets where appropriate so
narrative examples use:

- `latex_label_lookup`,
- `audit_implementation_label`,
- `check_equality`,
- `lean_check`.

Generated CLI evidence may still show CLI subcommands such as
`compare-label-code` until those CLI aliases are changed, but the report should
name preferred MCP tools in conversations and prompt maps.

### Tests

Extend doc sync tests so active report narrative has no primary
`Tool: compare_label_code` or `Tool: extract_latex_neighborhood` examples.

## Phase 6: package policy and docs sync

### Goal

Document the package dependency decision and keep it test-backed.

### Implementation instructions

Do not change `mcp` from optional to base dependency unless explicitly chosen
by maintainers. Instead:

- document that base library import remains lightweight;
- document that MCP-facing installs use `.[mcp]`;
- keep `mathdevmcp-mcp` behavior tested under the current packaging policy;
- add a package-policy test that encodes the decision.

### Tests

Run:

- packaging metadata tests,
- release-candidate installation tests,
- MCP sync tests,
- full suite,
- benchmark gate,
- base release-readiness,
- public release check,
- `git diff --check`.

## Final acceptance criteria

This checkpoint is complete when:

- `audit_implementation_label` returns a structured implementation-audit
  contract with AST/semantic/shape evidence,
- generated client rules exist and are schema-checked,
- deprecated alias usage is auditable,
- backend policy is documented and environment-aware,
- active release-facing examples prefer current MCP names,
- package policy remains explicit,
- full tests and benchmark gate pass,
- reset memo records every phase and caveat,
- changes are committed.

