# Using MathDevMCP from Cursor

Cursor speaks the same MCP stdio protocol as Claude Code, so the 3-tool
MathDevMCP surface works in Cursor with one configuration step. The
project-local skills (`.claude/skills/`) and subagents (`.claude/agents/`)
are Claude Code-specific and Cursor doesn't read them — Cursor users
need to load the workflow instructions through Cursor's own rules
system. The rules content below is the bridge.

## 1. Install

```bash
python -m pip install mathdevmcp
# or, for full deterministic-certification power (sympy + lean-dojo):
python -m pip install "mathdevmcp[backends]"
```

After install, `mathdevmcp-mcp` should be runnable from a terminal.
Confirm with `which mathdevmcp-mcp`.

## 2. Configure Cursor's MCP server

Add the server to either `~/.cursor/mcp.json` (active in every
workspace) or `<project>/.cursor/mcp.json` (project-scoped):

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "mathdevmcp-mcp"
    }
  }
}
```

Restart Cursor. The 3 tools — `latex_label_lookup`, `check_equality`,
`lean_check` — should appear in the agent's tool list.

If `mathdevmcp-mcp` isn't on PATH (rare; happens with some Python
installs), use the module form instead:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"]
    }
  }
}
```

## 3. Load the workflow rules

Copy the canonical rules block from
[`workflow-rules.md`](workflow-rules.md) (the code block under "The
rules block") into either:

- `<project>/.cursorrules` (legacy, single-file workspace rules)
- `<project>/.cursor/rules/mathdevmcp.mdc` (newer multi-file format)

Either location works. The rules give Cursor the same workflow
instructions Claude Code reads from `.claude/skills/`: how to audit a
labeled derivation, how to audit a code implementation against a spec,
how to drive release-readiness, and the certifying-evidence rule.

## What works the same as Claude Code

- All 3 MCP tools and their evidence envelopes.
- Severity-tagged evidence with the diagnostic-abstention contract:
  missing sympy / Lean → `severity: diagnostic`, never a crash.
- The `mathdevmcp` CLI for release / governance / doctor / benchmark
  (run from a Cursor terminal — these were never MCP tools).

## What's different from Claude Code

- **Skills/agents don't auto-load.** Claude Code automatically discovers
  `.claude/skills/` and `.claude/agents/`. Cursor doesn't. The rules
  block below is how you give Cursor the same workflow knowledge.
- **No subagent delegation.** `derivation-auditor` and
  `code-doc-consistency-reviewer` exist as Claude Code subagents that
  spawn into separate conversations. In Cursor you stay in one
  conversation; the rules cover the same behaviors as inline guidance.

## Troubleshooting

- **`mathdevmcp-mcp: command not found`** — pip didn't install scripts
  on PATH. Use the `python -m mathdevmcp.mcp_server` form shown above.
- **`ModuleNotFoundError: No module named 'mcp'`** — your install
  predates the simplification refactor (commit `bf7418d`) when `mcp`
  was buried in an optional extra. Run `pip install -U mathdevmcp`.
- **Tools return `severity: diagnostic` for everything you ask** —
  sympy and Lean aren't installed. Either `pip install
  mathdevmcp[backends]` for sympy, install Lean via
  [`elan`](https://github.com/leanprover/elan) for Lean checks, or
  accept the abstention as the correct behavior — the rules below
  explicitly tell Cursor not to overclaim when the backend can't
  certify.
- **Tools work but Cursor doesn't follow the workflow** — make sure
  the rules block is loaded (Cursor settings → Rules, or check that
  `.cursorrules` exists at workspace root). Cursor needs to read the
  rules at conversation start.

The rules block lives in [`workflow-rules.md`](workflow-rules.md) and
is shared with the GitHub Copilot setup; updating it in one place keeps
all non-Claude clients consistent.
