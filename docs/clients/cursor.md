# Cursor Setup

Use the MCP server through the project checkout or an installed
`mathdevmcp[mcp]` environment.

Example `.cursor/mcp.json` server entry:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

Install the portable workflow block into `.cursorrules`:

```bash
mathdevmcp install-rules cursor --root .
```

Preview without writing:

```bash
mathdevmcp install-rules cursor --root . --dry-run
```

The installed block is delimited by MathDevMCP markers, so existing project
instructions outside the block are preserved.
