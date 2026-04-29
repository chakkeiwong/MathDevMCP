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
- `check_proof_obligation`
- `audit_derivation_label`
- `audit_derivation_v2_label`
- `audit_kalman_recursion`
- `typed_obligation_label`
- `run_benchmarks`
- `benchmark_gate`
- `tool_matrix`
- `get_tool_matrix`
- `doctor`
- `release_corpus_manifest`
- `validate_release_corpus`
- `governance_policy`
- `release_readiness`

`tool_matrix` is the facade tool name. The FastMCP server keeps the legacy
server alias `get_tool_matrix` for compatibility.

Local launch command:

```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.mcp_server
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
        "PYTHONPATH": "/path/to/MathDevMCP/src"
      }
    }
  }
}
```

The MCP server is intentionally thin: all substantive logic remains in the
tested library modules under `src/mathdevmcp/`. The authoritative tool metadata
lives in the facade registry and is checked against this README during the
public industrial release gate.
