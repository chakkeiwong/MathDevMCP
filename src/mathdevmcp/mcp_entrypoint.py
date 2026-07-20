"""Dependency-aware console launcher for the optional MCP server."""

from __future__ import annotations

import importlib
import sys


def main(argv: list[str] | None = None) -> int:
    """Launch the MCP server or explain how to install its optional runtime."""

    try:
        # Preflight the named optional dependency before mcp_server imports
        # transitive SDK modules such as AnyIO.
        importlib.import_module("mcp")
        server = importlib.import_module("mathdevmcp.mcp_server")
    except ModuleNotFoundError as exc:
        if exc.name != "mcp":
            raise
        print(
            "MathDevMCP's MCP server requires the optional MCP runtime. "
            'Install it with `python -m pip install "mathdevmcp[mcp]"` '
            'or `python -m pip install -e ".[mcp]"` from a checkout.',
            file=sys.stderr,
        )
        return 2
    return int(server.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
