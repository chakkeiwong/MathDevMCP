# Using MathDevMCP from GitHub Copilot (VS Code)

GitHub Copilot in VS Code supports MCP servers in **agent mode** (the
"Agent" entry in the Copilot Chat mode picker). The 3-tool MathDevMCP
surface plugs in like any other stdio MCP server. The workflow rules
that ship with the project as `.claude/skills/` and `.claude/agents/`
are Claude Code-specific, so Copilot users load them via
`.github/copilot-instructions.md` instead — the same canonical rules
block referenced from [`workflow-rules.md`](workflow-rules.md).

## 1. Install

```bash
python -m pip install mathdevmcp
# or, for full deterministic-certification power (sympy + lean-dojo):
python -m pip install "mathdevmcp[backends]"
```

After install, `mathdevmcp-mcp` should be runnable from a terminal.
Confirm with `which mathdevmcp-mcp`.

## 2. Configure VS Code's MCP server

VS Code reads MCP server configs from one of:

- **Workspace**: `<project>/.vscode/mcp.json` (recommended for
  per-project servers)
- **User**: VS Code settings → `mcp.servers` in `settings.json`

Use the workspace config for MathDevMCP (it's a per-project tool):

```json
{
  "servers": {
    "mathdevmcp": {
      "type": "stdio",
      "command": "mathdevmcp-mcp"
    }
  }
}
```

Note the differences from Cursor / Claude Code MCP configs:
- Top-level key is `servers`, not `mcpServers`.
- Each server requires an explicit `"type": "stdio"` field.

If `mathdevmcp-mcp` isn't on PATH:

```json
{
  "servers": {
    "mathdevmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"]
    }
  }
}
```

Reload the VS Code window (Cmd/Ctrl+Shift+P → "Developer: Reload
Window"). Open Copilot Chat, switch to **Agent** mode (the mode picker
near the input box), and the 3 tools should appear in the tools list
(click the tools icon in the chat to inspect / toggle).

## 3. Load the workflow rules

VS Code Copilot reads `<project>/.github/copilot-instructions.md` as
workspace-level system context for every Copilot Chat conversation.
This is the equivalent of Cursor's `.cursorrules`.

Copy the canonical rules block from
[`workflow-rules.md`](workflow-rules.md) (the code block under "The
rules block") into `.github/copilot-instructions.md` at your project
root. If the file already exists, paste the block at the bottom under
its own `## MathDevMCP usage` heading so it doesn't collide with
existing instructions.

For finer-grained control, newer VS Code versions also support
per-language / per-path scoped instructions via
`.github/instructions/*.instructions.md` files with `applyTo:` YAML
frontmatter. For MathDevMCP this is overkill — the workspace-level
file is the right granularity since the rules apply whenever the agent
touches the MathDevMCP MCP server.

## What works the same as Claude Code

- All 3 MCP tools and their evidence envelopes.
- Severity-tagged evidence with the diagnostic-abstention contract:
  missing sympy / Lean → `severity: diagnostic`, never a crash.
- The `mathdevmcp` CLI for release / governance / doctor / benchmark
  (run from a VS Code terminal — these were never MCP tools).

## What's different from Claude Code

- **Skills/agents don't auto-load.** `.claude/skills/` and
  `.claude/agents/` are Claude Code-only. Copilot reads
  `.github/copilot-instructions.md` instead.
- **MCP tools require Agent mode.** Copilot Chat's "Ask" and "Edit"
  modes don't surface MCP tools — switch to Agent mode in the chat.
- **No subagent delegation.** `derivation-auditor` and
  `code-doc-consistency-reviewer` exist as Claude Code subagents that
  spawn into separate conversations. In Copilot you stay in one
  conversation; the rules cover the same behaviors as inline guidance.
- **Tool approval prompts.** VS Code prompts before each MCP tool call
  the first time per session (and remembers per-tool decisions). For a
  derivation audit that calls `check_equality` many times, accept "Allow
  for this session" so each obligation doesn't trigger a fresh prompt.

## Other Copilot surfaces

- **JetBrains Copilot** — MCP support is more limited and lags the VS
  Code feature set. Check JetBrains Copilot's release notes for current
  status; if MCP is unavailable, the CLI workflows (`mathdevmcp
  doctor`, `mathdevmcp release-readiness`, etc.) still work from any
  terminal.
- **Copilot CLI** — runs outside an editor; doesn't currently consume
  MCP servers. Use the `mathdevmcp` CLI directly.
- **GitHub.com Copilot Chat** — browser-based, no local MCP support.
  N/A for MathDevMCP.

## Troubleshooting

- **Tools don't appear in Agent mode** — confirm `.vscode/mcp.json`
  uses `"servers"` (not `"mcpServers"`) and includes `"type": "stdio"`.
  Check the MCP server status panel (Cmd/Ctrl+Shift+P → "MCP: Show
  Servers") for startup errors.
- **`mathdevmcp-mcp: command not found`** when VS Code launches the
  server — VS Code's environment may not include the Python install
  directory on PATH. Use the `python -m mathdevmcp.mcp_server` form
  shown above, and ensure `python` resolves to the env where you ran
  `pip install`.
- **`ModuleNotFoundError: No module named 'mcp'`** — your install
  predates the simplification refactor (commit `bf7418d`) when `mcp`
  was buried in an optional extra. Run `pip install -U mathdevmcp`.
- **Tools return `severity: diagnostic` for everything you ask** —
  sympy and Lean aren't installed. Either `pip install
  mathdevmcp[backends]` for sympy, install Lean via
  [`elan`](https://github.com/leanprover/elan) for Lean checks, or
  accept the abstention as the correct behavior (the rules block tells
  Copilot not to overclaim when the backend can't certify).
- **Copilot ignores the rules** — confirm
  `.github/copilot-instructions.md` exists at workspace root and the
  Copilot setting "Use Instruction Files" is enabled (VS Code settings
  → search for `copilot.chat.codeGeneration.useInstructionFiles`).
