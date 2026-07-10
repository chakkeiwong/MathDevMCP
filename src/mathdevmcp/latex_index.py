from __future__ import annotations

from dataclasses import dataclass, asdict
import fnmatch
import json
from pathlib import Path
import re
from typing import Iterable

from .equation_locator import locate_equations_in_file, summarize_equation_localization


@dataclass(frozen=True)
class LatexBlock:
    kind: str
    name: str
    file: str
    line_start: int
    line_end: int
    label: str | None
    title: str | None
    text: str
    block_id: str
    section_path: list[str]


def iter_tex_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.tex")):
        if path.is_file():
            yield path


def _line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _find_label(block_text: str) -> str | None:
    match = re.search(r"\\label\{([^}]+)\}", block_text)
    if match:
        return match.group(1)
    return None


def _extract_title(arg: str | None) -> str | None:
    if arg is None:
        return None
    stripped = arg.strip()
    return stripped or None


SECTION_LEVELS = {
    "part": 0,
    "chapter": 1,
    "section": 2,
    "subsection": 3,
    "subsubsection": 4,
}



def _block_id(relative_path: str, kind: str, line_start: int, label: str | None, title: str | None) -> str:
    suffix = label or title or str(line_start)
    safe = re.sub(r"[^A-Za-z0-9_.:-]+", "-", suffix).strip("-")
    return f"{relative_path}:{line_start}:{kind}:{safe}"



def _with_tex_suffix(path: Path) -> Path:
    if path.suffix:
        return path
    return path.with_suffix(".tex")



def _discover_input_order(root: Path) -> list[Path]:
    tex_files = {path.resolve() for path in iter_tex_files(root)}
    include_pattern = re.compile(r"\\(?:input|include)\{([^}]+)\}")
    referenced: set[Path] = set()
    ordered: list[Path] = []
    visiting: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in ordered or path in visiting or path not in tex_files:
            return
        visiting.add(path)
        text = path.read_text(encoding="utf-8")
        for match in include_pattern.finditer(text):
            child = _with_tex_suffix((path.parent / match.group(1)).resolve())
            referenced.add(child)
            visit(child)
        visiting.remove(path)
        ordered.append(path)

    roots = sorted(tex_files - referenced)
    for path in roots:
        visit(path)
    for path in sorted(tex_files):
        visit(path)
    return ordered



def extract_latex_blocks(root: Path) -> list[LatexBlock]:
    root = root.resolve()
    blocks: list[LatexBlock] = []
    env_pattern = re.compile(
        r"\\begin\{(?P<env>theorem|proposition|lemma|corollary|definition|assumption|example|remark)\}"
        r"(?:\[(?P<title>[^\]]*)\])?"
        r"(?P<body>.*?)"
        r"\\end\{(?P=env)\}",
        re.DOTALL,
    )
    equation_pattern = re.compile(
        r"\\begin\{(?P<env>equation|align|alignat|gather|multline)\*?\}"
        r"(?P<body>.*?)"
        r"\\end\{(?P=env)\*?\}",
        re.DOTALL,
    )
    section_pattern = re.compile(
        r"\\(?P<kind>part|chapter|section|subsection|subsubsection)\*?\{(?P<title>[^{}]+)\}"
    )

    for path in _discover_input_order(root):
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(root))
        section_matches = list(section_pattern.finditer(text))
        section_stack: list[tuple[int, str]] = []
        section_lookup: list[tuple[int, list[str]]] = []
        for match in section_matches:
            level = SECTION_LEVELS[match.group("kind")]
            title = match.group("title").strip()
            while section_stack and section_stack[-1][0] >= level:
                section_stack.pop()
            section_stack.append((level, title))
            section_lookup.append((match.start(), [name for _, name in section_stack]))
            line = _line_number_at(text, match.start())
            blocks.append(
                LatexBlock(
                    kind=match.group("kind"),
                    name=title,
                    file=rel,
                    line_start=line,
                    line_end=line,
                    label=None,
                    title=title,
                    text=match.group(0),
                    block_id=_block_id(rel, match.group("kind"), line, None, title),
                    section_path=[name for _, name in section_stack],
                )
            )

        def section_path_for(offset: int) -> list[str]:
            current: list[str] = []
            for match_offset, path_names in section_lookup:
                if match_offset > offset:
                    break
                current = path_names
            return current.copy()

        for match in env_pattern.finditer(text):
            body = match.group(0)
            line_start = _line_number_at(text, match.start())
            title = _extract_title(match.group("title"))
            label = _find_label(body)
            blocks.append(
                LatexBlock(
                    kind=match.group("env"),
                    name=match.group("env"),
                    file=rel,
                    line_start=line_start,
                    line_end=_line_number_at(text, match.end()),
                    label=label,
                    title=title,
                    text=body.strip(),
                    block_id=_block_id(rel, match.group("env"), line_start, label, title),
                    section_path=section_path_for(match.start()),
                )
            )
        for match in equation_pattern.finditer(text):
            body = match.group(0)
            line_start = _line_number_at(text, match.start())
            label = _find_label(body)
            blocks.append(
                LatexBlock(
                    kind=match.group("env"),
                    name=match.group("env"),
                    file=rel,
                    line_start=line_start,
                    line_end=_line_number_at(text, match.end()),
                    label=label,
                    title=None,
                    text=body.strip(),
                    block_id=_block_id(rel, match.group("env"), line_start, label, None),
                    section_path=section_path_for(match.start()),
                )
            )
    return sorted(blocks, key=lambda block: (block.file, block.line_start, block.kind))


def locate_equations(root: Path) -> list[dict]:
    root = root.resolve()
    rows: list[dict] = []
    for path in _discover_input_order(root):
        try:
            rows.extend(locate_equations_in_file(path, root=root))
        except UnicodeDecodeError:
            rows.append(
                {
                    "id": f"{path}:0:decode_error",
                    "environment": "unknown",
                    "file": str(path),
                    "line_start": 0,
                    "line_end": 0,
                    "label": None,
                    "row_index": 0,
                    "text": "",
                    "source_text": "",
                    "localization_status": "failed",
                    "uncertainty": ["decode_error"],
                }
            )
    return sorted(rows, key=lambda row: (row.get("file", ""), row.get("line_start", 0), row.get("row_index", 0)))


def _index_diagnostics(root: Path, blocks: list[LatexBlock], equation_rows: list[dict]) -> dict:
    seen: dict[str, list[dict]] = {}
    for block in blocks:
        if block.label:
            seen.setdefault(block.label, []).append({"file": block.file, "line_start": block.line_start, "block_id": block.block_id})
    duplicate_labels = {label: locations for label, locations in seen.items() if len(locations) > 1}
    tex_files = [str(path.relative_to(root)) for path in iter_tex_files(root)]
    return {
        "status": "indexed_with_diagnostics",
        "parsed_files": tex_files,
        "failed_files": [],
        "skipped_files": [],
        "duplicate_labels": duplicate_labels,
        "equation_localization": summarize_equation_localization(equation_rows),
    }






def build_index(root: Path) -> dict:
    root = root.resolve()
    blocks = extract_latex_blocks(root)
    equation_rows = locate_equations(root)
    labels = {block.label: asdict(block) for block in blocks if block.label}
    return {
        "root": str(root.resolve()),
        "n_blocks": len(blocks),
        "n_labels": len(labels),
        "n_equation_rows": len(equation_rows),
        "blocks": [asdict(block) for block in blocks],
        "labels": labels,
        "equation_rows": equation_rows,
        "diagnostics": _index_diagnostics(root, blocks, equation_rows),
    }








def write_index(root: Path, output: Path) -> dict:
    index = build_index(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index



def search_index(index: dict, query: str, limit: int = 10) -> list[dict]:
    return search_index_filtered(index, query, limit=limit)


def _normalize_file_filters(value: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    return [str(item) for item in value if str(item)]


def _file_matches_any(relative_file: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative_file, pattern) for pattern in patterns)


def _file_allowed(relative_file: str, *, file: str | None = None, include_globs: list[str] | None = None, exclude_globs: list[str] | None = None) -> bool:
    include_patterns = _normalize_file_filters(include_globs)
    exclude_patterns = _normalize_file_filters(exclude_globs)
    exact_file = str(file) if file else ""
    if exact_file and relative_file != exact_file:
        return False
    if include_patterns and not _file_matches_any(relative_file, include_patterns):
        return False
    if exclude_patterns and _file_matches_any(relative_file, exclude_patterns):
        return False
    return True


def filter_index_blocks(
    index: dict,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> list[dict]:
    return [
        block
        for block in index.get("blocks", [])
        if _file_allowed(str(block.get("file") or ""), file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    ]


def _filtered_label_block(
    index: dict,
    label: str,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> dict | None:
    for block in filter_index_blocks(index, file=file, include_globs=include_globs, exclude_globs=exclude_globs):
        if block.get("label") == label:
            return block
    return None


def search_index_filtered(
    index: dict,
    query: str,
    limit: int = 10,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> list[dict]:
    terms = [term.lower() for term in re.findall(r"[A-Za-z0-9_\\-]+", query) if term]
    scored: list[tuple[int, dict]] = []
    for block in filter_index_blocks(index, file=file, include_globs=include_globs, exclude_globs=exclude_globs):
        haystack = " ".join(
            str(block.get(field) or "")
            for field in ("kind", "name", "file", "label", "title", "text", "block_id", "section_path")
        ).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            scored.append((score, block))
    scored.sort(key=lambda item: (-item[0], item[1]["file"], item[1]["line_start"]))
    return [block | {"score": score} for score, block in scored[:limit]]




def _read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


def extract_context(root: Path, relative_path: str, line_start: int, line_end: int, before: int = 2, after: int = 2) -> dict:
    root = root.resolve()
    lines = _read_lines(root, relative_path)
    start = max(1, line_start - before)
    end = min(len(lines), line_end + after)
    excerpt = [
        {"line": i, "text": lines[i - 1]}
        for i in range(start, end + 1)
    ]
    return {
        "file": relative_path,
        "line_start": line_start,
        "line_end": line_end,
        "context_start": start,
        "context_end": end,
        "excerpt": excerpt,
    }



def extract_paragraph_context(root: Path, relative_path: str, line_start: int, line_end: int, before: int = 1, after: int = 1) -> dict:
    root = root.resolve()
    lines = _read_lines(root, relative_path)
    paragraphs: list[tuple[int, int, list[str]]] = []
    start: int | None = None
    collected: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if line.strip():
            if start is None:
                start = idx
            collected.append(line)
        elif start is not None:
            paragraphs.append((start, idx - 1, collected))
            start = None
            collected = []
    if start is not None:
        paragraphs.append((start, len(lines), collected))

    selected = [i for i, (para_start, para_end, _) in enumerate(paragraphs) if not (para_end < line_start or para_start > line_end)]
    if not selected:
        selected = [i for i, (para_start, _, _) in enumerate(paragraphs) if para_start >= line_start][:1]
    if not selected:
        selected = [len(paragraphs) - 1] if paragraphs else []
    chosen = paragraphs[max(0, selected[0] - before):min(len(paragraphs), selected[-1] + after + 1)] if selected else []

    excerpt = [
        {"line_start": para_start, "line_end": para_end, "text": "\n".join(text)}
        for para_start, para_end, text in chosen
    ]
    return {
        "file": relative_path,
        "line_start": line_start,
        "line_end": line_end,
        "context_start": excerpt[0]["line_start"] if excerpt else line_start,
        "context_end": excerpt[-1]["line_end"] if excerpt else line_end,
        "paragraphs": excerpt,
    }


def find_label_text_fallback(
    root: Path,
    label: str,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> dict | None:
    root = root.resolve()
    needle = rf"\label{{{label}}}"
    for path in _discover_input_order(root):
        relative_file = str(path.relative_to(root))
        if not _file_allowed(relative_file, file=file, include_globs=include_globs, exclude_globs=exclude_globs):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            if needle in line:
                return {
                    "file": relative_file,
                    "line_start": index,
                    "line_end": index,
                    "label": label,
                    "kind": "unknown",
                    "block_id": None,
                    "section_path": [],
                    "status": "fallback_text_context",
                    "warnings": ["label_not_in_index", "latex_ast_block_parse_failed_or_stale_cache"],
                }
    return None


def _fallback_context(
    root: Path,
    label: str,
    before: int,
    after: int,
    *,
    paragraph: bool,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> dict:
    fallback = find_label_text_fallback(root, label, file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    if fallback is None:
        raise KeyError(f"Unknown label: {label}")
    context = (
        extract_paragraph_context(root, fallback["file"], fallback["line_start"], fallback["line_end"], before=before, after=after)
        if paragraph
        else extract_context(root, fallback["file"], fallback["line_start"], fallback["line_end"], before=before, after=after)
    )
    context.update(fallback)
    return context



def extract_paragraph_context_for_label(
    index: dict,
    label: str,
    before: int = 1,
    after: int = 1,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> dict:
    root = Path(index["root"])
    block = _filtered_label_block(index, label, file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    if block is None and not (file or include_globs or exclude_globs):
        block = index.get("labels", {}).get(label)
    if not block:
        return _fallback_context(root, label, before, after, paragraph=True, file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    context = extract_paragraph_context(root, block["file"], block["line_start"], block["line_end"], before=before, after=after)
    context["label"] = label
    context["kind"] = block["kind"]
    context["block_id"] = block.get("block_id")
    context["section_path"] = block.get("section_path", [])
    return context



def extract_context_for_label(
    index: dict,
    label: str,
    before: int = 2,
    after: int = 2,
    *,
    file: str | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
) -> dict:
    root = Path(index["root"])
    block = _filtered_label_block(index, label, file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    if block is None and not (file or include_globs or exclude_globs):
        block = index.get("labels", {}).get(label)
    if not block:
        return _fallback_context(root, label, before, after, paragraph=False, file=file, include_globs=include_globs, exclude_globs=exclude_globs)
    context = extract_context(root, block["file"], block["line_start"], block["line_end"], before=before, after=after)
    context["label"] = label
    context["kind"] = block["kind"]
    context["block_id"] = block.get("block_id")
    context["section_path"] = block.get("section_path", [])
    return context
