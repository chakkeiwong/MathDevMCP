from __future__ import annotations

import json
from pathlib import Path

from .latex_index import build_index, iter_tex_files


def _index_fingerprint(root: Path) -> dict:
    root = root.resolve()
    files = []
    for path in iter_tex_files(root):
        stat = path.stat()
        files.append(
            {
                "path": str(path.relative_to(root)),
                "mtime_ns": stat.st_mtime_ns,
                "size": stat.st_size,
            }
        )
    return {"root": str(root), "files": files}


def _read_cached_index(cache_path: Path) -> dict | None:
    try:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_or_build_index(root: Path, cache_path: Path) -> dict:
    fingerprint = _index_fingerprint(root)
    if cache_path.exists():
        cached = _read_cached_index(cache_path)
        if cached and cached.get("fingerprint") == fingerprint and isinstance(cached.get("index"), dict):
            index = cached["index"]
            index["cache"] = {"path": str(cache_path), "hit": True}
            return index

    index = build_index(root)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps({"fingerprint": fingerprint, "index": index}, indent=2), encoding="utf-8")
    index["cache"] = {"path": str(cache_path), "hit": False}
    return index
