# MCP server

MathDevMCP now has a true FastMCP stdio server in:

- `src/mathdevmcp/mcp_server.py`

The reusable tool dispatch layer remains in:

- `src/mathdevmcp/mcp_facade.py`

Current MCP tools:

- `search_latex`
- `extract_latex_context`
- `extract_latex_neighborhood`
- `search_code_docs`
- `compare_doc_code`
- `compare_label_code`
- `derive_label_step`
- `implementation_brief`
- `run_benchmarks`
- `get_tool_matrix`

Local launch command:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.mcp_server
```

Installed script entrypoint:

```bash
mathdevmcp-mcp
```

Example Claude Code MCP config:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "/home/chakwong/MathDevMCP/src"
      }
    }
  }
}
```

The MCP server is intentionally thin: all substantive logic remains in the tested library modules under `src/mathdevmcp/`.
