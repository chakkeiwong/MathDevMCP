from __future__ import annotations

from dataclasses import dataclass, asdict
import fnmatch
import hashlib
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import stat
from typing import Iterable, Mapping

from .equation_locator import locate_equations_in_file, summarize_equation_localization
from .evidence_manifest import EvidenceValidationError, validate_logical_path


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


@dataclass(frozen=True)
class EntryRootedSnapshot:
    logical_ref: str
    raw_bytes: bytes
    source_digest: str
    byte_count: int
    line_count: int
    parse_state: str
    directives: tuple[dict, ...]


@dataclass(frozen=True)
class EntryRootedDiscovery:
    entry_ref: str
    snapshots: dict[str, EntryRootedSnapshot]
    considered_files: tuple[str, ...]
    reachable_files: tuple[str, ...]
    excluded_sibling_files: tuple[str, ...]
    unsearched_files: tuple[dict, ...]
    diagnostics: tuple[dict, ...]
    integrity_vetoes: tuple[str, ...]
    traversal_counts: dict[str, int]


_ENTRY_BUDGET_KEYS = frozenset(
    {"max_files", "max_bytes", "max_nodes", "max_edges", "max_dependency_expansions"}
)
_LIVE_INCLUDE_RE = re.compile(rb"\\(input|include)\s*\{([^{}]+)\}")
_INCLUDE_COMMAND_RE = re.compile(rb"\\(?:input|include)\b")


def _entry_budget(value: Mapping[str, int]) -> dict[str, int]:
    if not isinstance(value, Mapping) or set(value) != _ENTRY_BUDGET_KEYS:
        raise EvidenceValidationError(
            f"entry-rooted budget keys must be exactly {sorted(_ENTRY_BUDGET_KEYS)}"
        )
    result: dict[str, int] = {}
    for key in sorted(_ENTRY_BUDGET_KEYS):
        item = value[key]
        if type(item) is not int or item <= 0:
            raise EvidenceValidationError(f"entry-rooted budget {key} must be a positive integer")
        result[key] = item
    return result


def _live_latex_bytes(raw: bytes) -> bytes:
    """Blank comments without changing any byte offsets."""
    output = bytearray(raw)
    offset = 0
    for line in raw.splitlines(keepends=True):
        for index, value in enumerate(line):
            if value != ord("%"):
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == ord("\\"):
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                end = len(line.rstrip(b"\r\n"))
                output[offset + index:offset + end] = b" " * (end - index)
                break
        offset += len(line)
    return bytes(output)


def _normalize_include_ref(source_ref: str, target: str) -> tuple[str | None, str | None]:
    if not target or "\x00" in target or "\\" in target or target.startswith("/"):
        return None, "path_traversal"
    raw = PurePosixPath(source_ref).parent.joinpath(PurePosixPath(target))
    parts: list[str] = []
    for part in raw.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                return None, "path_traversal"
            parts.pop()
        else:
            parts.append(part)
    if not parts:
        return None, "path_traversal"
    logical = PurePosixPath(*parts)
    if not logical.suffix:
        logical = logical.with_suffix(".tex")
    if logical.suffix != ".tex":
        return None, "unsupported_include_form"
    try:
        return validate_logical_path(logical.as_posix(), name="include target"), None
    except EvidenceValidationError:
        return None, "path_traversal"


def _safe_regular_bytes(root: Path, logical_ref: str) -> tuple[bytes | None, str | None]:
    validate_logical_path(logical_ref, name="entry-rooted logical ref")
    current = root
    parts = logical_ref.split("/")
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            return None, "missing"
        if stat.S_ISLNK(info.st_mode):
            return None, "symlink"
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            return None, "special"
        if index == len(parts) - 1 and not stat.S_ISREG(info.st_mode):
            return None, "special"
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(current, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            return None, "special"
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks), None
    finally:
        os.close(fd)


def _scan_entry_directives(raw: bytes, source_ref: str) -> tuple[tuple[dict, ...], list[dict]]:
    live = _live_latex_bytes(raw)
    directives: list[dict] = []
    diagnostics: list[dict] = []
    matched_starts: set[int] = set()
    for match in _LIVE_INCLUDE_RE.finditer(live):
        matched_starts.add(match.start())
        try:
            target_text = match.group(2).decode("utf-8", "strict").strip()
        except UnicodeDecodeError:
            target_text = ""
        target_ref, error = _normalize_include_ref(source_ref, target_text)
        directive = {
            "kind": match.group(1).decode("ascii"),
            "source_file": source_ref,
            "target_text": target_text,
            "target_file": target_ref,
            "byte_span": {"start": match.start(), "end": match.end()},
            "line_span": {
                "start": raw[:match.start()].count(b"\n") + 1,
                "end": raw[:match.end()].count(b"\n") + 1,
            },
        }
        directives.append(directive)
        if error:
            diagnostics.append(
                {
                    "kind": error,
                    "classification": "integrity" if error == "path_traversal" else "engineering",
                    "source_file": source_ref,
                    "target_file": target_text,
                    "byte_span": directive["byte_span"],
                }
            )
    for match in _INCLUDE_COMMAND_RE.finditer(live):
        if match.start() not in matched_starts:
            diagnostics.append(
                {
                    "kind": "unsupported_include_form",
                    "classification": "engineering",
                    "source_file": source_ref,
                    "target_file": None,
                    "byte_span": {"start": match.start(), "end": match.end()},
                }
            )
    directives.sort(key=lambda item: (item["byte_span"]["start"], item["kind"]))
    diagnostics.sort(
        key=lambda item: (
            item.get("source_file", "").encode("utf-8"),
            int(item.get("byte_span", {}).get("start", -1)),
            item["kind"],
        )
    )
    return tuple(directives), diagnostics


def _entry_tex_inventory(root: Path) -> tuple[str, ...]:
    refs: list[str] = []
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        names[:] = sorted(name for name in names if not (base / name).is_symlink())
        for name in sorted(files):
            path = base / name
            if path.suffix != ".tex" or path.is_symlink() or not path.is_file():
                continue
            refs.append(path.relative_to(root).as_posix())
    return tuple(sorted(refs, key=lambda item: item.encode("utf-8")))


def discover_entry_rooted_tex_files(
    root: Path,
    entry_ref: str,
    *,
    budget: Mapping[str, int],
) -> EntryRootedDiscovery:
    """Discover only the explicit entry/include closure, preserving exact bytes."""
    limits = _entry_budget(budget)
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir():
        raise EvidenceValidationError("entry-rooted corpus root must be a non-symlink directory")
    entry = validate_logical_path(entry_ref, name="entry_ref")
    if not entry.endswith(".tex"):
        raise EvidenceValidationError("entry_ref must name a .tex file")

    snapshots: dict[str, EntryRootedSnapshot] = {}
    diagnostics: list[dict] = []
    unsearched: list[dict] = []
    considered: set[str] = {entry}
    queue: list[tuple[str, tuple[str, ...]]] = [(entry, ())]
    expansions = 0
    total_bytes = 0

    while queue:
        logical_ref, ancestors = queue.pop(0)
        if logical_ref in snapshots:
            continue
        if len(snapshots) >= limits["max_files"]:
            unsearched.append({"file": logical_ref, "reason": "max_files"})
            continue
        raw, error = _safe_regular_bytes(root, logical_ref)
        if error:
            if logical_ref == entry:
                raise EvidenceValidationError(f"entry_ref is unavailable or unsafe: {error}")
            kind = "symlink_include" if error == "symlink" else "missing_include" if error == "missing" else "special_include"
            diagnostics.append(
                {
                    "kind": kind,
                    "classification": "integrity" if error in {"symlink", "special"} else "engineering",
                    "source_file": ancestors[-1] if ancestors else entry,
                    "target_file": logical_ref,
                    "byte_span": None,
                }
            )
            unsearched.append({"file": logical_ref, "reason": kind})
            continue
        assert raw is not None
        if total_bytes + len(raw) > limits["max_bytes"]:
            unsearched.append({"file": logical_ref, "reason": "max_bytes"})
            continue
        total_bytes += len(raw)
        try:
            raw.decode("utf-8", "strict")
            parse_state = "parsed"
        except UnicodeDecodeError:
            parse_state = "decode_error"
            diagnostics.append(
                {
                    "kind": "decode_failure",
                    "classification": "engineering",
                    "source_file": logical_ref,
                    "target_file": logical_ref,
                    "byte_span": {"start": 0, "end": len(raw)},
                }
            )
        directives, scan_diagnostics = _scan_entry_directives(raw, logical_ref) if parse_state == "parsed" else ((), [])
        diagnostics.extend(scan_diagnostics)
        snapshots[logical_ref] = EntryRootedSnapshot(
            logical_ref=logical_ref,
            raw_bytes=raw,
            source_digest=hashlib.sha256(raw).hexdigest(),
            byte_count=len(raw),
            line_count=raw.count(b"\n") + (0 if raw.endswith(b"\n") and raw else 1),
            parse_state=parse_state,
            directives=directives,
        )
        for directive in directives:
            target = directive["target_file"]
            if target is None:
                continue
            considered.add(target)
            if target in ancestors or target == logical_ref:
                diagnostics.append(
                    {
                        "kind": "include_cycle",
                        "classification": "engineering",
                        "source_file": logical_ref,
                        "target_file": target,
                        "byte_span": directive["byte_span"],
                    }
                )
                continue
            if expansions >= limits["max_dependency_expansions"]:
                unsearched.append({"file": target, "reason": "max_dependency_expansions"})
                continue
            expansions += 1
            queue.append((target, (*ancestors, logical_ref)))

    inventory = _entry_tex_inventory(root)
    reachable = tuple(sorted(snapshots, key=lambda item: item.encode("utf-8")))
    excluded = tuple(item for item in inventory if item not in snapshots)
    diagnostics.sort(
        key=lambda item: (
            str(item.get("source_file", "")).encode("utf-8"),
            int((item.get("byte_span") or {}).get("start", -1)),
            item["kind"],
            str(item.get("target_file") or "").encode("utf-8"),
        )
    )
    unsearched.sort(key=lambda item: (item["file"].encode("utf-8"), item["reason"]))
    vetoes = tuple(
        f"{item['kind']}:{item.get('source_file')}:{item.get('target_file')}"
        for item in diagnostics
        if item["classification"] == "integrity"
    )
    return EntryRootedDiscovery(
        entry_ref=entry,
        snapshots=snapshots,
        considered_files=tuple(sorted(considered, key=lambda item: item.encode("utf-8"))),
        reachable_files=reachable,
        excluded_sibling_files=excluded,
        unsearched_files=tuple(unsearched),
        diagnostics=tuple(diagnostics),
        integrity_vetoes=vetoes,
        traversal_counts={
            "files": len(snapshots),
            "bytes": total_bytes,
            "dependency_expansions": expansions,
        },
    )


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


def _label_occurrences(blocks: list[LatexBlock], equation_rows: list[dict]) -> dict[str, list[dict]]:
    display_kinds = {"equation", "align", "alignat", "aligned", "gather", "multline"}
    occurrences: dict[str, list[dict]] = {}

    for block in blocks:
        if block.kind not in display_kinds and block.label:
            occurrences.setdefault(block.label, []).append(asdict(block))

    display_blocks = [block for block in blocks if block.kind in display_kinds]
    for row in equation_rows:
        labels = row.get("explicit_labels", [])
        if not isinstance(labels, list) or not labels:
            continue
        parent = next(
            (
                block
                for block in display_blocks
                if block.file == row.get("file")
                and block.line_start <= int(row.get("line_start", 0)) <= block.line_end
                and block.line_start <= int(row.get("line_end", 0)) <= block.line_end
            ),
            None,
        )
        for label in labels:
            if parent is None:
                occurrence = {
                    "kind": row.get("environment"),
                    "name": row.get("environment"),
                    "file": row.get("file"),
                    "line_start": row.get("line_start"),
                    "line_end": row.get("line_end"),
                    "label": label,
                    "title": None,
                    "text": row.get("source_text", ""),
                    "block_id": f"{row.get('file')}:{row.get('environment_start_byte')}:{row.get('environment')}:{label}",
                    "section_path": [],
                }
            else:
                occurrence = asdict(parent)
                occurrence["label"] = label
                occurrence["block_id"] = _block_id(parent.file, parent.kind, parent.line_start, label, None)
            occurrence["label_source"] = "explicit_equation_row"
            occurrence["label_span"] = next(
                (
                    {key: item[key] for key in ("start_byte", "end_byte", "line_start", "line_end")}
                    for item in row.get("label_spans", [])
                    if item.get("label") == label
                ),
                None,
            )
            occurrence["environment_id"] = row.get("environment_id")
            occurrence["environment_start_byte"] = row.get("environment_start_byte")
            occurrence["environment_end_byte"] = row.get("environment_end_byte")
            occurrences.setdefault(label, []).append(occurrence)

    for label, values in occurrences.items():
        values.sort(
            key=lambda item: (
                str(item.get("file", "")).encode("utf-8"),
                int(item.get("line_start", 0)),
                int((item.get("label_span") or {}).get("start_byte", -1)),
            )
        )
    return occurrences


def _index_diagnostics(root: Path, label_occurrences: dict[str, list[dict]], equation_rows: list[dict]) -> dict:
    duplicate_labels = {
        label: [
            {
                "file": item.get("file"),
                "line_start": item.get("line_start"),
                "block_id": item.get("block_id"),
                "label_span": item.get("label_span"),
            }
            for item in locations
        ]
        for label, locations in label_occurrences.items()
        if len(locations) > 1
    }
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
    label_occurrences = _label_occurrences(blocks, equation_rows)
    labels = {label: values[0] for label, values in label_occurrences.items() if len(values) == 1}
    return {
        "root": str(root.resolve()),
        "n_blocks": len(blocks),
        "n_labels": len(labels),
        "n_equation_rows": len(equation_rows),
        "blocks": [asdict(block) for block in blocks],
        "labels": labels,
        "label_occurrences": label_occurrences,
        "equation_rows": equation_rows,
        "diagnostics": _index_diagnostics(root, label_occurrences, equation_rows),
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


def resolve_label_occurrences(index: dict, label: str, *, file: str | None = None) -> dict:
    """Resolve a label without hiding duplicate source occurrences."""
    occurrences = index.get("label_occurrences", {}).get(label, [])
    if not isinstance(occurrences, list):
        occurrences = []
    matches = [item for item in occurrences if isinstance(item, dict) and (file is None or item.get("file") == file)]
    if len(matches) == 1:
        return {"status": "resolved", "label": label, "file": file, "occurrence": matches[0], "occurrences": matches}
    if not matches:
        return {"status": "label_not_found", "label": label, "file": file, "occurrence": None, "occurrences": []}
    return {
        "status": "ambiguous",
        "label": label,
        "file": file,
        "occurrence": None,
        "occurrences": matches,
        "reason": "The label has multiple source occurrences; supply the exact workspace-relative file.",
    }


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
