"""Shared symlink-safe primitives for identity and generated artifacts."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import uuid
import json
from typing import Any


def _open_parent(destination: Path) -> tuple[int, str]:
    destination = Path(destination)
    if destination.name in {"", ".", ".."}:
        raise ValueError("artifact destination must name a file")
    parts = destination.parent.parts
    if destination.is_absolute():
        descriptor = os.open(destination.anchor, os.O_RDONLY | os.O_DIRECTORY)
        parts = parts[1:]
    else:
        descriptor = os.open(".", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in parts:
            if part in {"", "."}:
                continue
            if part == "..":
                raise ValueError("artifact destination may not traverse '..'")
            try:
                child = os.open(
                    part,
                    os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=descriptor,
                )
            except FileNotFoundError:
                os.mkdir(part, mode=0o700, dir_fd=descriptor)
                child = os.open(
                    part,
                    os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=descriptor,
                )
            except OSError as exc:
                if exc.errno not in {getattr(os, "ELOOP", 40), 20}:
                    raise
                raise ValueError(f"artifact parent is not a real directory: {part}") from exc
            os.close(descriptor)
            descriptor = child
        return descriptor, destination.name
    except BaseException:
        os.close(descriptor)
        raise


def _read_existing(parent_fd: int, name: str) -> bytes | None:
    try:
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
    except FileNotFoundError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("artifact identity collision")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError("short artifact write")
        view = view[written:]


def write_bytes_no_replace(destination: Path, payload: bytes, *, mode: int = 0o600) -> None:
    """Create an identity artifact, accepting only an identical replay."""

    parent_fd, name = _open_parent(Path(destination))
    try:
        existing = _read_existing(parent_fd, name)
        if existing is not None:
            if existing != payload:
                raise ValueError("artifact identity collision")
            return
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(name, flags, mode, dir_fd=parent_fd)
        try:
            _write_all(descriptor, payload)
            os.fsync(descriptor)
        except BaseException:
            try:
                os.unlink(name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
            raise
        finally:
            os.close(descriptor)
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def write_bytes_safe(destination: Path, payload: bytes, *, mode: int = 0o600) -> None:
    """Atomically replace a generated file without following path symlinks."""

    parent_fd, name = _open_parent(Path(destination))
    temporary = f".{name}.tmp-{uuid.uuid4().hex}"
    descriptor: int | None = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary, flags, mode, dir_fd=parent_fd)
        _write_all(descriptor, payload)
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.replace(temporary, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        os.fsync(parent_fd)
    except BaseException:
        if descriptor is not None:
            os.close(descriptor)
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(parent_fd)


def persist_document_outputs(
    result: dict[str, Any],
    *,
    output_md: str | Path | None = None,
    output_json: str | Path | None = None,
) -> dict[str, str]:
    """Persist generated document reports through the shared safe writer."""

    written: dict[str, str] = {}
    markdown = result.get("markdown", "")
    if output_md is not None:
        write_bytes_safe(Path(output_md), str(markdown).encode("utf-8"))
        written["output_md"] = str(output_md)
    if output_json is not None:
        serializable = dict(result)
        serializable.pop("markdown", None)
        write_bytes_safe(
            Path(output_json),
            json.dumps(serializable, indent=2, sort_keys=True).encode("utf-8"),
        )
        written["output_json"] = str(output_json)
    return written
