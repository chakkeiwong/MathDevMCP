from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
from typing import Iterable


@dataclass(frozen=True)
class CodeHit:
    kind: str
    name: str
    file: str
    line: int
    text: str


def iter_code_files(root: Path) -> Iterable[Path]:
    patterns = ("*.py", "*.tex", "*.md")
    for pattern in patterns:
        for path in sorted(root.rglob(pattern)):
            if path.is_file() and ".git" not in path.parts:
                yield path


def search_files(root: Path, query: str, limit: int = 20) -> list[dict]:
    root = root.resolve()
    terms = [term.lower() for term in re.findall(r"[A-Za-z0-9_\\-]+", query) if term]
    hits: list[tuple[int, CodeHit]] = []
    for path in iter_code_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        rel = str(path.relative_to(root))
        for i, line in enumerate(lines, start=1):
            haystack = line.lower()
            score = sum(1 for term in terms if term in haystack)
            if score:
                kind = "latex" if path.suffix == ".tex" else "markdown" if path.suffix == ".md" else "code"
                name = line.strip()[:120]
                hits.append((score, CodeHit(kind=kind, name=name, file=rel, line=i, text=line.strip())))
    hits.sort(key=lambda item: (-item[0], item[1].file, item[1].line))
    return [asdict(hit) | {"score": score} for score, hit in hits[:limit]]
