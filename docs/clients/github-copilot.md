# GitHub Copilot Setup

Use VS Code Copilot agent mode with a stdio MCP server configuration.

Example `.vscode/mcp.json` server entry:

```json
{
  "servers": {
    "mathdevmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

Install the portable workflow block into `.github/copilot-instructions.md`:

```bash
mathdevmcp install-rules copilot --root .
```

Install Cursor and Copilot rules in one pass:

```bash
mathdevmcp install-rules all --root .
```

The rules keep the same safety boundary as the MCP contracts: client guidance
does not certify math; deterministic backend evidence does.
