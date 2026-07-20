"""POSIX stdio transport for environments where AnyIO file adapters hang."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import importlib.metadata
import os
import sys
from typing import Any, AsyncIterator

import anyio
from mcp import types
from mcp.shared.message import SessionMessage

MAX_INPUT_LINE_BYTES = 4 * 1024 * 1024


def _input_size_error(buffer: bytes) -> ValueError | None:
    """Return a typed error when an unterminated input line is too large."""

    if len(buffer) > MAX_INPUT_LINE_BYTES:
        return ValueError("MCP input line exceeds the 4 MiB limit")
    return None


def _split_input_buffer(buffer: bytes) -> tuple[list[bytes], bytes, ValueError | None]:
    """Split complete lines and enforce the limit on the remaining line."""

    lines: list[bytes] = []
    while b"\n" in buffer:
        line, buffer = buffer.split(b"\n", 1)
        error = _input_size_error(line)
        if error is not None:
            return lines, buffer, error
        if line.strip():
            lines.append(line)
    return lines, buffer, _input_size_error(buffer)

@asynccontextmanager
async def posix_stdio_server() -> AsyncIterator[tuple[Any, Any]]:
    """Yield MCP streams backed by event-loop pipe reads, without worker threads."""

    read_send, read_receive = anyio.create_memory_object_stream[SessionMessage | Exception](0)
    write_send, write_receive = anyio.create_memory_object_stream[SessionMessage](0)
    loop = asyncio.get_running_loop()
    chunks: asyncio.Queue[bytes | BaseException] = asyncio.Queue()
    stdin_fd = sys.stdin.fileno()

    def stdin_ready() -> None:
        try:
            chunks.put_nowait(os.read(stdin_fd, 65_536))
        except BaseException as exc:  # Deliver transport failures to the session.
            chunks.put_nowait(exc)

    async def stdin_reader() -> None:
        buffer = b""
        loop.add_reader(stdin_fd, stdin_ready)
        try:
            async with read_send:
                while True:
                    chunk = await chunks.get()
                    if isinstance(chunk, BaseException):
                        await read_send.send(chunk)
                        return
                    if not chunk:
                        if buffer.strip():
                            error = _input_size_error(buffer)
                            if error is not None:
                                await read_send.send(error)
                                return
                            await _send_line(read_send, buffer)
                        return
                    buffer += chunk
                    lines, buffer, error = _split_input_buffer(buffer)
                    if error is not None:
                        await read_send.send(error)
                        return
                    for line in lines:
                        await _send_line(read_send, line)
        finally:
            loop.remove_reader(stdin_fd)

    async def stdout_writer() -> None:
        async with write_receive:
            async for session_message in write_receive:
                payload = session_message.message.model_dump_json(
                    by_alias=True, exclude_none=True
                ).encode("utf-8") + b"\n"
                _write_all(sys.stdout.fileno(), payload)

    async with anyio.create_task_group() as task_group:
        task_group.start_soon(stdin_reader)
        task_group.start_soon(stdout_writer)
        yield read_receive, write_send


async def _send_line(sender: Any, raw: bytes) -> None:
    try:
        message = types.JSONRPCMessage.model_validate_json(raw.decode("utf-8", errors="replace"))
    except Exception as exc:
        await sender.send(exc)
        return
    await sender.send(SessionMessage(message))


def _write_all(fd: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise RuntimeError("MCP stdio write made no progress")
        view = view[written:]


async def run_fastmcp_stdio(server: Any) -> None:
    """Run the tested pinned transport, with an explicit SDK compatibility gate."""

    try:
        version = importlib.metadata.version("mcp")
    except importlib.metadata.PackageNotFoundError as exc:  # pragma: no cover
        raise RuntimeError("MCP runtime metadata is unavailable") from exc
    if version != "1.27.0":
        raise RuntimeError(
            f"MathDevMCP stdio transport is validated only for mcp==1.27.0; observed {version}"
        )
    if os.name != "posix":  # pragma: no cover - declared Linux/WSL support boundary.
        await server.run_stdio_async()
        return
    async with posix_stdio_server() as (read_stream, write_stream):
        # FastMCP 1.27.0 has no public stream-injection API. This is isolated
        # here, version-gated, and covered by the transport compatibility test.
        await server._mcp_server.run(  # noqa: SLF001
            read_stream,
            write_stream,
            server._mcp_server.create_initialization_options(),  # noqa: SLF001
        )
