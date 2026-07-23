#!/usr/bin/env python3
"""Initialize the installed stdio MCP server and call one deterministic tool."""

from __future__ import annotations

import argparse
import anyio
from datetime import timedelta
import json
import os
from pathlib import Path
import sys
import time
import traceback

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _run(command: str, command_args: list[str], cwd: Path) -> dict[str, object]:
    parameters = StdioServerParameters(
        command=command,
        args=command_args,
        env={
            "CUDA_VISIBLE_DEVICES": "-1",
            **({"MATHDEVMCP_MCP_PROFILE": os.environ["MATHDEVMCP_MCP_PROFILE"]} if "MATHDEVMCP_MCP_PROFILE" in os.environ else {}),
        },
        cwd=cwd,
    )
    started = time.monotonic()
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
            read_timeout_seconds=timedelta(seconds=45),
        ) as session:
            initialized = await session.initialize()
            initialized_seconds = time.monotonic() - started
            listed = await session.list_tools()
            listed_seconds = time.monotonic() - started
            tool_names = sorted(tool.name for tool in listed.tools)
            profile = os.environ.get("MATHDEVMCP_MCP_PROFILE", "stable").strip().lower()
            expected_count = {"stable": 23, "all": 71}.get(profile)
            if expected_count is None:
                raise RuntimeError(f"unsupported MCP smoke profile: {profile}")
            if len(tool_names) != expected_count or "doctor" not in tool_names:
                raise RuntimeError(
                    f"installed MCP server advertised {len(tool_names)} tools; expected {expected_count} for {profile}"
                )
            result = await session.call_tool("doctor", {})
            if result.isError:
                raise RuntimeError("installed MCP server returned an error for doctor")
            return {
                "status": "passed",
                "server_name": initialized.serverInfo.name,
                "tool_count": len(tool_names),
                "profile": profile,
                "doctor_called": True,
                "initialized_seconds": round(initialized_seconds, 3),
                "listed_seconds": round(listed_seconds, 3),
                "total_seconds": round(time.monotonic() - started, 3),
            }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Checkout or installed-project working directory")
    parser.add_argument("--command", default=sys.executable, help="Python interpreter for the installed package")
    args = parser.parse_args(argv)

    try:
        report = anyio.run(
            _run,
            args.command,
            ["-m", "mathdevmcp.mcp_entrypoint"],
            Path(args.root).resolve(),
        )
    except Exception as exc:
        print("MCP stdio smoke failed:", file=sys.stderr)
        traceback.print_exception(exc, file=sys.stderr)
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
