# MCP interface improvement execution plan

## Motivation

PR #1 proposes shrinking the MathDevMCP MCP interface to three deterministic
primitives:

- `latex_label_lookup`,
- `check_equality`,
- `lean_check`.

The motivation is understandable. A smaller MCP surface reduces routing
ambiguity, makes documentation easier to keep synchronized, and avoids exposing
weak wrappers that an agent can reproduce by reading files and reasoning.

However, a three-tool-only interface is too small for MathDevMCP's actual
product value. The project has been built around auditable mathematical
workflows:

```text
source label or code path
→ parser/provenance evidence
→ typed MathObligation diagnostics
→ route decision
→ shape/dimension diagnostics
→ backend evidence or explicit abstention
→ compact colleague-facing report
→ benchmark/release artifact
```

Moving that workflow logic entirely into prose skills would lose important
properties:

- structured result contracts,
- regression tests,
- benchmark-gate coverage,
- cross-client behavior,
- stable failure and abstention semantics,
- reproducible release evidence.

The goal of this plan is therefore not to preserve every current MCP tool. The
goal is to replace both extremes with a tiered, intentional middle interface:
small enough for agents to understand, but rich enough to preserve the tested
workflow spine that makes MathDevMCP useful.

## Decision

Do not merge a three-tool-only MCP surface as the final interface.

Instead, implement a tiered MCP interface with:

1. deterministic primitives,
2. audited workflow tools,
3. operational release/maintenance tools,
4. explicit deprecation metadata for weak or duplicate tools.

PR #1 should be treated as a source of useful patches, not as an interface
architecture to accept unchanged. Salvage:

- `.mcp.json` portability,
- `mcp` as a base dependency if package policy agrees,
- graceful backend-dependent test skips,
- `mathdevmcp install-rules`,
- Cursor/Copilot client instructions,
- better public explanation of the certifying-evidence rule.

Revise or reject:

- removing all workflow tools from MCP,
- relying on prose skills as the only workflow contract,
- stale docs that teach removed tools,
- unversioned breaking MCP API changes,
- schema-inconsistent workflow rules.

## Safety invariant

No parser output, AST match, inferred type, dimension hint, route hint, shape
guard, numeric diagnostic, generated Lean skeleton, LeanDojo tactic result,
benchmark pass, release checklist, skill instruction, or MCP wrapper may become
a verified mathematical claim unless a deterministic backend verifies the claim
under explicit assumptions and MathDevMCP records reproducible evidence.

Interface simplification must not weaken this invariant. If a workflow moves
from Python to a skill, it loses testable contract protection; compensate by
keeping the workflow as a structured tool or by adding an equivalent tested
library/report path.

## Target MCP interface

### Tier 1: deterministic primitives

These tools are stable, low-level, and suitable for direct agent composition.

- `search_latex`
  - Purpose: search indexed LaTeX blocks with provenance.
  - Keep because free-text retrieval is a core agent operation and the local
    index preserves provenance better than ad hoc shell search.

- `latex_label_lookup`
  - Purpose: fetch a labeled block plus paragraph context and provenance.
  - Add as the preferred name.
  - Compatibility: keep `extract_latex_context` and
    `extract_latex_neighborhood` as deprecated aliases for at least one release
    cycle, or make them return structured migration guidance.

- `check_equality`
  - Purpose: check a bounded equality using deterministic backend evidence.
  - Add as the preferred name for `check_proof_obligation`.
  - Compatibility: keep `check_proof_obligation` as a deprecated alias.

- `lean_check`
  - Purpose: compile supplied Lean source and certify only if Lean accepts the
    source and no placeholder proof is present.
  - Add only with token/comment-aware placeholder detection. Substring matching
    on `sorry` or `admit` is not acceptable for a certifying primitive.

### Tier 2: audited workflow tools

These tools preserve MathDevMCP's main value: reproducible mathematical review
reports with contracts, statuses, provenance, and abstention reasons.

- `audit_derivation_v2_label`
  - Keep as the primary proof-audit release spine.
  - It should remain the preferred path for label-level mathematical audit.

- `typed_obligation_label`
  - Keep because typed/dimensional diagnostics are hard to reproduce reliably
    from prose instructions alone.

- `audit_implementation_label`
  - Add as the preferred name for code-vs-document implementation review.
  - It should supersede the current weak `compare_label_code` name.
  - Internally it may call existing `compare_label_to_code`,
    `audit_kalman_recursion`, AST operation graph extraction, shape diagnostics,
    and implementation brief logic as appropriate.
  - Compatibility: keep `compare_label_code` as a deprecated alias or wrapper.

- `audit_kalman_recursion`
  - Keep while Kalman/state-space workflows are a flagship benchmark domain.
  - Mark as domain-specific and stable only for structural audit, not proof.

- `implementation_brief`
  - Keep if it produces a compact, tested handoff object with provenance and
    status.
  - If it remains too compositional or ambiguous, mark experimental or replace
    with `build_review_packet` in a later PR. Do not remove it silently.

### Tier 3: operational tools

These tools support release, CI, and environment diagnosis. They are useful to
coding agents and maintainers, but should stay compact.

- `doctor`
  - Keep. It is the fastest way for an agent to distinguish missing optional
    backends from actual product failures.

- `benchmark_gate`
  - Keep. It is the CI-friendly release signal.

- `release_readiness`
  - Keep unless the team explicitly decides that release work must be CLI-only.
  - If kept, expose profile selection consistently with the CLI.

- `validate_release_corpus`
  - Keep if private/sanitized corpus validation remains part of agent-driven
    release checks.

### Tier 4: deprecated or removable tools

The following should be collapsed, renamed, or moved behind compatibility
aliases:

- `extract_latex_context`
  - Replace with `latex_label_lookup(before=..., after=...)`.

- `extract_latex_neighborhood`
  - Replace with `latex_label_lookup(before=1, after=1)`.

- `compare_doc_code`
  - Deprecate unless upgraded beyond token overlap.

- `compare_label_code`
  - Replace with `audit_implementation_label`.

- `derive_label_step`
  - Deprecate if `audit_derivation_v2_label` covers the use case.

- `run_benchmarks`
  - Prefer `benchmark_gate` unless callers need full case details. If both
    remain, document the distinction.

- `tool_matrix` and `governance_policy`
  - Move to docs/CLI unless MCP clients need dynamic structured access. If
    retained, mark as informational and non-certifying.

## Interface metadata requirements

Add a typed tool registry in `src/mathdevmcp/mcp_facade.py` rather than a plain
name-to-handler dictionary.

Suggested shape:

```python
@dataclass(frozen=True)
class MCPToolSpec:
    name: str
    handler: ToolHandler
    description: str
    tier: str
    stability: str
    output_contract: str
    certifying_capable: bool = False
    deprecated: bool = False
    replacement: str | None = None
    optional_capability: str | None = None
```

Use these stability values:

- `stable`,
- `experimental`,
- `deprecated`.

Use these tiers:

- `primitive`,
- `workflow`,
- `operational`,
- `informational`.

Every MCP tool must declare:

- tier,
- stability,
- output contract,
- whether it can ever return certifying evidence,
- optional backend dependencies,
- deprecation replacement if applicable.

`list_mcp_tools()` should return this metadata so clients can route safely.

## Compatibility and migration policy

Breaking MCP tool removals require an explicit versioned migration plan.

For the next release cycle:

- prefer aliases over removal,
- when an alias is deprecated, return the same result shape plus deprecation
  metadata where possible,
- when a removed tool cannot be safely aliased, return a structured
  `unknown_tool` error with a `replacement` field,
- update README, `mcp/README.md`, operator guide, release report, client rules,
  and tests in the same PR.

Do not keep stale docs that teach removed MCP tools as primary workflow entry
points.

## Implementation phases

### Phase 1: inventory and classification

Files to inspect:

- `src/mathdevmcp/mcp_facade.py`,
- `src/mathdevmcp/mcp_server.py`,
- `src/mathdevmcp/cli.py`,
- `mcp/README.md`,
- `README.md`,
- `docs/mathdevmcp-operator-guide.md`,
- `docs/mathdevmcp-release-report.tex`,
- `.mcp.json`,
- tests under `tests/test_mcp_*`.

Tasks:

1. List every current MCP facade tool and FastMCP server tool.
2. Classify each tool into primitive, workflow, operational, informational, or
   deprecated.
3. Identify duplicate names and alias needs.
4. Identify docs that mention removed or renamed tools.
5. Record the intended final surface in a short table in `mcp/README.md`.

Acceptance criteria:

- there is one authoritative registry of target tools,
- no tool is removed without a replacement decision,
- docs and tests can be updated from the registry.

### Phase 2: registry refactor

Files to edit:

- `src/mathdevmcp/mcp_facade.py`,
- `tests/test_mcp_facade.py`,
- `tests/test_schema_contracts.py` if contract metadata is asserted there.

Tasks:

1. Add `MCPToolSpec`.
2. Replace ad hoc `TOOL_HANDLERS` construction with a spec tuple.
3. Keep existing handlers initially.
4. Make `list_mcp_tools()` return full metadata.
5. Add tests that every spec has tier, stability, contract, description, and
   coherent deprecation metadata.
6. Add tests that every handler name is unique and every deprecated tool has a
   replacement.

Acceptance criteria:

- existing behavior still works,
- the registry is the source of truth,
- tests fail if a future tool is added without metadata.

### Phase 3: add preferred names and compatibility aliases

Files to edit:

- `src/mathdevmcp/mcp_facade.py`,
- `src/mathdevmcp/mcp_server.py`,
- `tests/test_mcp_facade.py`,
- `tests/test_mcp_server.py`.

Tasks:

1. Add `latex_label_lookup` as the preferred label-context primitive.
2. Keep `extract_latex_context` and `extract_latex_neighborhood` as deprecated
   aliases, or return structured migration guidance.
3. Add `check_equality` as the preferred equality primitive.
4. Keep `check_proof_obligation` as a deprecated alias.
5. Add `audit_implementation_label` as the preferred implementation review
   workflow name.
6. Keep `compare_label_code` as a deprecated alias until the replacement has
   enough tests.
7. Ensure FastMCP exposes the same intended server names as the facade registry,
   including aliases only if the team wants schema-level compatibility.

Acceptance criteria:

- new names work,
- old names either work with deprecation metadata or fail with specific
  replacement guidance,
- no client sees a generic `unknown_tool` for a tool removed in the previous
  release.

### Phase 4: Lean placeholder detection hardening

Files to edit:

- `src/mathdevmcp/lean_check.py`,
- `tests/test_lean_check.py`,
- `tests/test_mcp_facade.py`,
- `tests/test_mcp_server.py`.

Tasks:

1. Replace substring placeholder detection with token/comment-aware detection.
2. Treat Lean comments as non-proof text:
   - line comments starting with `--`,
   - block comments `/- ... -/`.
3. Avoid false positives for identifiers such as `sorryCount` or
   `admitTheoremName`.
4. Keep true positives for actual `by sorry`, `:= by admit`, and equivalent
   placeholder tokens.
5. Preserve the existing rule: even if Lean compiles, placeholder proofs are
   `inconclusive` unless explicitly allowed, and never certifying.

Acceptance criteria:

- tests cover comments, strings if practical, identifiers, true `sorry`, true
  `admit`, and `allow_sorry=True`,
- `lean_check` remains deterministic and bounded by timeout.

### Phase 5: documentation and client rules

Files to edit:

- `README.md`,
- `mcp/README.md`,
- `docs/mathdevmcp-operator-guide.md`,
- `docs/mathdevmcp-release-report.tex`,
- `docs/clients/workflow-rules.md` if PR #1's client docs are adopted,
- `src/mathdevmcp/_workflow_rules.py` if `install-rules` is adopted,
- `.claude/skills/*` and `.claude/agents/*` if PR #1's Claude files are
  adopted.

Tasks:

1. Make primary docs teach the tiered surface.
2. Stop teaching removed MCP names as primary entry points.
3. Where old names are mentioned, mark them as deprecated and name the
   replacement.
4. Align all workflow-rule examples with real FastMCP schemas. For example,
   do not call `latex_label_lookup(..., paragraph_context=true)` unless that
   parameter exists in `mcp_server.py`.
5. Add a migration table:

```text
old name                    new name/status
extract_latex_neighborhood  latex_label_lookup
check_proof_obligation      check_equality
compare_label_code          audit_implementation_label
derive_label_step           audit_derivation_v2_label or deprecated
run_benchmarks              benchmark_gate for CI, CLI for full report
```

Acceptance criteria:

- `rg` over primary docs does not find removed tool names except in migration
  sections,
- client rules are schema-valid,
- README and MCP README agree with the registry.

### Phase 6: generated docs and sync tests

Files to edit or add:

- `tests/test_mcp_surface_sync.py`,
- `tests/test_workflow_rules_in_sync.py` if client rules are adopted,
- optional helper in `src/mathdevmcp/mcp_facade.py` to render a markdown table.

Tasks:

1. Add a test that `mcp/README.md` lists every stable MCP tool.
2. Add a test that deprecated tools are documented in the migration table.
3. Add a test that FastMCP exposed server names equal the intended registry
   names.
4. Add a test that portable workflow rules do not mention nonexistent tool
   parameters.

Acceptance criteria:

- doc drift is caught by tests,
- the next interface edit cannot silently desynchronize README, FastMCP, and
  facade metadata.

### Phase 7: PR #1 salvage strategy

Tasks:

1. Cherry-pick or reimplement `.mcp.json` portability.
2. Cherry-pick or reimplement `install-rules` only after workflow rules are
   schema-valid.
3. Accept client docs only after they describe the tiered interface rather than
   a three-tool-only interface.
4. Accept graceful backend test skips if they skip only genuine optional
   backend dependencies and do not hide product regressions.
5. Reject the removal of all workflow tools from MCP.
6. Add a changelog or release note if any MCP names are deprecated.

Acceptance criteria:

- useful PR #1 changes land without adopting the over-shrunk interface,
- migration is explicit,
- workflow tools remain tested and benchmarked.

## Verification plan

Run targeted tests after each phase:

```bash
PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py
PYTHONPATH=src pytest -q tests/test_lean_check.py
PYTHONPATH=src pytest -q tests/test_schema_contracts.py
```

Run full release checks before merge:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
git diff --check
```

If optional backends are available, also run the Lean-focused tests and backend
doctor. Missing optional backends should produce diagnostic abstentions or
skips with explicit reasons, not crashes.

## Final acceptance criteria

The interface improvement is complete when:

- the MCP surface is tiered and documented,
- the stable surface has roughly 8-12 intentional tools rather than 3 or 21,
- every tool has registry metadata,
- every deprecated tool has a replacement or migration response,
- workflow tools retain structured contracts and tests,
- docs and FastMCP schemas agree,
- Lean placeholder detection is not substring-only,
- PR #1's useful install/client fixes are either merged or explicitly tracked
  for a follow-up,
- full tests and benchmark gate pass.

## Non-goals

- Do not rewrite all workflow internals.
- Do not remove tested workflow tools solely because an agent can theoretically
  compose primitives.
- Do not claim the MCP interface certifies arbitrary frontier mathematics.
- Do not make Claude-specific skills the only source of workflow truth.
- Do not require optional LeanDojo/LaTeXML/Sage environments for the base MCP
  server to start.
