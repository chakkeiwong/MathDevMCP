# MCP server

MathDevMCP exposes a tiered FastMCP stdio interface. The goal is a small,
intentional surface, not a three-tool-only surface. Deterministic primitives
stay easy to call, while tested workflow tools remain available as structured
contracts with provenance, abstention reasons, and benchmark coverage.

Server: `src/mathdevmcp/mcp_server.py`

Facade registry: `src/mathdevmcp/mcp_facade.py`

## Preferred stable surface

### Primitive Tools

- `search_latex` - search indexed LaTeX blocks with provenance.
- `latex_label_lookup` - fetch a labeled LaTeX block plus paragraph
  neighborhood and provenance.
- `search_code_docs` - search code and document files together.
- `check_equality` - check `lhs == rhs` with a deterministic symbolic backend
  when available.
- `lean_check` - compile supplied Lean source. Certifying only when Lean exits
  0 and the source has no placeholder proof tokens.

### Workflow Tools

- `audit_implementation_label` - audit a labeled document block against a code
  implementation. This is the preferred name for code/document drift review.
- `derive_label_step` - check a concrete expression-to-expression claim against
  labeled document context.
- `implementation_brief` - build a compact document-grounded handoff report.
- `audit_derivation_label` - audit obligations extracted from a labeled block.
- `audit_derivation_v2_label` - run the primary release-spine proof audit with
  typed diagnostics, route decisions, backend evidence, and abstentions.
- `audit_kalman_recursion` - audit AST-level Kalman recursion structure in code.
- `typed_obligation_label` - build typed/dimensional diagnostics for a labeled
  math obligation.

### Operational Tools

- `run_benchmarks` - return the full seeded benchmark report.
- `benchmark_gate` - return the CI-friendly benchmark gate result.
- `doctor` - report environment and optional backend capabilities.
- `release_corpus_manifest` - return public/private release corpus metadata.
- `validate_release_corpus` - validate corpus privacy and release-gate fields.
- `release_readiness` - return a profile-specific release-readiness report.

### Informational Tools

- `tool_matrix` - facade name for the static problem/tool matrix.
- `get_tool_matrix` - FastMCP server alias for `tool_matrix`.
- `governance_policy` - return the security and governance policy.

## Deprecated Compatibility Names

Deprecated names remain available for a migration cycle. Prefer the new names
in prompts, client rules, and new code.

| Deprecated name | Preferred replacement |
|---|---|
| `extract_latex_context` | `latex_label_lookup` with tighter `before`/`after` values |
| `extract_latex_neighborhood` | `latex_label_lookup` |
| `check_proof_obligation` | `check_equality` |
| `compare_label_code` | `audit_implementation_label` |

Experimental or legacy workflow names that remain available but should be used
carefully:

- `compare_doc_code` - token/document overlap check; prefer a richer
  implementation audit when a label and code path are available.

## Launch

Installed script entrypoint:

```bash
mathdevmcp-mcp
```

From a checkout without installation:

```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.mcp_server
```

Claude Code MCP config from a checkout:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/MathDevMCP/src"
      }
    }
  }
}
```

The MCP server is intentionally thin: substantive logic remains in tested
library modules under `src/mathdevmcp/`. The facade registry is the source of
truth for tool metadata and is checked against this README during tests.
