import anyio
import pytest

import mathdevmcp.mcp_stdio_transport as transport


@pytest.mark.anyio
async def test_send_line_parses_jsonrpc_message() -> None:
    sender, receiver = anyio.create_memory_object_stream(1)
    raw = b'{"jsonrpc":"2.0","id":1,"method":"ping"}'

    await transport._send_line(sender, raw)
    message = await receiver.receive()

    assert message.message.root.jsonrpc == "2.0"
    assert message.message.root.id == 1
    assert message.message.root.method == "ping"


@pytest.mark.anyio
async def test_send_line_delivers_parse_failure() -> None:
    sender, receiver = anyio.create_memory_object_stream(1)

    await transport._send_line(sender, b"not-json")
    result = await receiver.receive()

    assert isinstance(result, Exception)


def test_write_all_retries_partial_writes(monkeypatch) -> None:
    chunks: list[bytes] = []

    def partial_write(_fd: int, payload: memoryview) -> int:
        raw = bytes(payload[:2])
        chunks.append(raw)
        return len(raw)

    monkeypatch.setattr(transport.os, "write", partial_write)

    transport._write_all(1, b"abcdef")

    assert b"".join(chunks) == b"abcdef"


def test_write_all_rejects_zero_progress(monkeypatch) -> None:
    monkeypatch.setattr(transport.os, "write", lambda _fd, _payload: 0)

    with pytest.raises(RuntimeError, match="no progress"):
        transport._write_all(1, b"x")


def test_input_size_limit_checks_unterminated_residual_after_split() -> None:
    complete = b'{"jsonrpc":"2.0","id":1,"method":"ping"}'
    lines, residual, error = transport._split_input_buffer(
        complete + b"\n" + b"x" * (transport.MAX_INPUT_LINE_BYTES + 1)
    )
    assert lines == [complete]
    assert len(residual) == transport.MAX_INPUT_LINE_BYTES + 1
    assert isinstance(error, ValueError)
    assert "4 MiB" in str(error)


def test_input_size_limit_allows_exact_limit() -> None:
    assert transport._input_size_error(b"x" * transport.MAX_INPUT_LINE_BYTES) is None
