# MCP server

MathDevMCP exposes a deliberately small set of **deterministic primitives** over
FastMCP stdio. Workflows (consistency, derivation chains, implementation briefs,
release gates) live in `.claude/skills/` and `.claude/agents/`, not as MCP
tools. The rationale and full mapping is in [`docs/mcp-simplification.md`](../docs/mcp-simplification.md).

Server: `src/mathdevmcp/mcp_server.py`
Facade: `src/mathdevmcp/mcp_facade.py`

## Current MCP tools

- `latex_label_lookup` — fetch a labeled LaTeX block plus paragraph neighborhood and provenance. Replaces the former `extract_latex_context` / `extract_latex_neighborhood`. Use `Grep` for free-text search.
- `check_equality` — sympy-backed `lhs == rhs` check. Returns severity-tagged evidence; only `severity: certifying` (`normalized_match` or `backend_verified`) counts as proof. Replaces the former `check_proof_obligation`.
- `lean_check` — compile a supplied Lean source. Verified iff Lean exits 0 and the source has no `sorry`/`admit`. Newly exposed; the underlying library function is `lean_check.check_lean_source`.

That's the entire surface. If you reach for a tool that isn't here, look for the matching skill or subagent first.

## Skills (project-local, in `.claude/skills/`)

- `audit-derivation` — extract every `=` from a labeled block, run `check_equality` on each, aggregate per the certifying-evidence rule. Replaces `audit_derivation_label`, `audit_derivation_v2_label`, `derive_label_step`.
- `audit-implementation` — check that a code file contains the operations and shape guards the spec at a label demands. Replaces `audit_kalman_recursion`, `implementation_brief`, the per-domain workflow audits.
- `release-check` — run the release-readiness gate via the CLI for a profile and surface blockers. Replaces driving release through MCP.

## Subagents (project-local, in `.claude/agents/`)

- `derivation-auditor` — long-form, multi-block derivation audit with the "only `certifying` counts as verified" rule baked into the agent's identity. Hand off paper sections to it.
- `code-doc-consistency-reviewer` — find drift between a labeled spec and an implementation across operations, identities, assumptions, symbols, and edge cases. Replaces the former token-overlap `compare_*` tools.

## Things that used to be MCP tools, now CLI

Driven via the `mathdevmcp` console script (preferred) or `PYTHONPATH=src python -m mathdevmcp.cli ...`:

- `mathdevmcp doctor` — environment / backend capabilities
- `mathdevmcp benchmark-gate --root .`
- `mathdevmcp release-readiness --root . --profile <profile>`
- `mathdevmcp governance-validate --root .`
- `mathdevmcp validate-release-corpus --root ./benchmarks/fixtures`
- `mathdevmcp public-release-check --root .`

These return JSON suitable for piping into the `release-check` skill.

## Things that used to be MCP tools, now Claude can do directly

- Free-text search across LaTeX or code → `Grep`.
- Token-overlap consistency between a paragraph and a code file → read both with `Read` and compare. The former regex-token overlap collapsed `\sigma` and `\Sigma` to the same token; reading is strictly better.
- Static `tool_matrix` and `governance_policy` lookups → read the source files directly; they were always frozen dicts.

## Local launch

Installed (preferred):

```bash
mathdevmcp-mcp
```

From a checkout without install:

```bash
PYTHONPATH=src python -m mathdevmcp.mcp_server
```

## Claude Code MCP config

After `pip install -e .` (or `pip install mathdevmcp[mcp]`):

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "mathdevmcp-mcp"
    }
  }
}
```

Without install (development checkout):

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {"PYTHONPATH": "src"}
    }
  }
}
```

The `PYTHONPATH` value should be a path relative to the working directory the
client launches the server from, or an absolute path on the local machine —
never a checked-in absolute path from another developer's home directory.

The server is intentionally thin: substantive logic lives in the tested
library modules under `src/mathdevmcp/`. The facade registry
(`MCP_TOOL_SPECS`) is the single source of truth and is asserted against this
README by `tests/test_mcp_surface_sync.py`.
