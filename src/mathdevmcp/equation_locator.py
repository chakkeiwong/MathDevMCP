"""Byte-preserving localization for supported LaTeX display environments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
import re
from typing import Any

from .contracts import attach_contract
from .evidence_manifest import canonical_json_bytes


DISPLAY_ENVIRONMENTS = ("equation", "align", "alignat", "aligned", "gather", "multline")
P02_DISPLAY_ENVIRONMENTS = ("equation", "equation*", "align", "align*", "aligned", "aligned*")
P02_LOCATOR_VERSION = "p02_lightweight_locator@1"

_ASCII_WHITESPACE = b" \t\r\n\f\v"
_ENVIRONMENT_TOKEN_RE = re.compile(rb"\\(begin|end)\{([A-Za-z]+\*?)\}")
_LABEL_RE = re.compile(rb"\\label\s*\{([^{}]+)\}")
_NUMBER_SUPPRESSOR_RE = re.compile(rb"\\(?:nonumber|notag)(?![A-Za-z])")


@dataclass(frozen=True)
class EquationRow:
    id: str
    environment: str
    file: str
    line_start: int
    line_end: int
    label: str | None
    row_index: int
    text: str
    source_text: str
    localization_status: str
    uncertainty: list[str]
    byte_start: int
    byte_end: int
    environment_id: str
    environment_start_byte: int
    environment_end_byte: int
    environment_starred: bool
    environment_stack: list[str]
    environment_stack_descriptors: list[dict[str, Any]]
    explicit_label: str | None
    explicit_labels: list[str]
    label_span: dict[str, int] | None
    label_spans: list[dict[str, int | str]]
    has_nonumber: bool
    had_row_terminator: bool
    ownership_status: str
    source_digest: str
    locator_version: str
    sequence_group: int


@dataclass(frozen=True)
class _Environment:
    name: str
    start: int
    begin_end: int
    end_start: int
    end: int
    ancestor_starts: tuple[int, ...]

    @property
    def kind(self) -> str:
        return self.name[:-1] if self.name.endswith("*") else self.name

    @property
    def starred(self) -> bool:
        return self.name.endswith("*")


def _line_number_at(raw: bytes, offset: int) -> int:
    return raw[:offset].count(b"\n") + 1


def _comment_mask(raw: bytes) -> bytes:
    """Mask unescaped comments without changing byte offsets."""
    masked = bytearray(raw)
    line_start = 0
    while line_start < len(raw):
        line_end = raw.find(b"\n", line_start)
        if line_end < 0:
            line_end = len(raw)
        # Search only percent-byte candidates. Scanning every byte in every
        # source line made indexing large real documents needlessly expensive.
        position = raw.find(b"%", line_start, line_end)
        while position >= 0:
            backslashes = 0
            cursor = position - 1
            while cursor >= line_start and raw[cursor] == ord("\\"):
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                masked[position:line_end] = b" " * (line_end - position)
                break
            position = raw.find(b"%", position + 1, line_end)
        line_start = line_end + 1
    return bytes(masked)


def _is_escaped(raw: bytes, position: int, lower_bound: int) -> bool:
    backslashes = 0
    cursor = position - 1
    while cursor >= lower_bound and raw[cursor] == ord("\\"):
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _localized_environments(raw: bytes) -> list[_Environment]:
    try:
        raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("LaTeX source must be strict UTF-8") from exc

    supported = set(P02_DISPLAY_ENVIRONMENTS)
    stack: list[tuple[str, int, int, tuple[int, ...]]] = []
    completed: list[_Environment] = []
    for match in _ENVIRONMENT_TOKEN_RE.finditer(_comment_mask(raw)):
        operation = match.group(1).decode("ascii")
        name = match.group(2).decode("ascii")
        if name not in supported:
            continue
        if operation == "begin":
            stack.append((name, match.start(), match.end(), tuple(item[1] for item in stack)))
            continue
        if not stack or stack[-1][0] != name:
            raise ValueError("crossed or unmatched supported LaTeX display environment")
        opened_name, start, begin_end, ancestors = stack.pop()
        completed.append(
            _Environment(
                name=opened_name,
                start=start,
                begin_end=begin_end,
                end_start=match.start(),
                end=match.end(),
                ancestor_starts=ancestors,
            )
        )
    if stack:
        raise ValueError("unclosed supported LaTeX display environment")
    return sorted(completed, key=lambda item: (item.start, -item.end))


def _environment_descriptors(
    environment: _Environment,
    by_start: dict[int, _Environment],
    source_digest: str,
) -> list[dict[str, Any]]:
    chain = [by_start[start] for start in environment.ancestor_starts] + [environment]
    identity_stack: list[dict[str, Any]] = []
    descriptors: list[dict[str, Any]] = []
    for item in chain:
        identity_stack.append({"kind": item.kind, "starred": item.starred})
        payload = {
            "source_digest": source_digest,
            "start_byte": item.start,
            "end_byte": item.end,
            "environment_stack": [dict(entry) for entry in identity_stack],
        }
        descriptors.append(
            {
                "environment_id": "env_" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest(),
                "kind": item.kind,
                "starred": item.starred,
                "start_byte": item.start,
                "end_byte": item.end,
            }
        )
    return descriptors


def _trim_span(raw: bytes, start: int, end: int) -> tuple[int, int]:
    while start < end and raw[start] in _ASCII_WHITESPACE:
        start += 1
    while end > start and raw[end - 1] in _ASCII_WHITESPACE:
        end -= 1
    return start, end


def _row_parts(raw: bytes, environment: _Environment) -> list[tuple[int, int, bool, int]]:
    """Return nonempty row spans, terminator state, and blank-row barrier id."""
    masked = _comment_mask(raw)
    start = environment.begin_end
    cursor = start
    brace_depth = 0
    parts: list[tuple[int, int, bool, int]] = []
    sequence_group = 0

    def add_part(part_start: int, part_end: int, terminated: bool) -> None:
        nonlocal sequence_group
        trimmed_start, trimmed_end = _trim_span(raw, part_start, part_end)
        if trimmed_start < trimmed_end:
            parts.append((trimmed_start, trimmed_end, terminated, sequence_group))
        elif parts:
            sequence_group += 1

    while cursor < environment.end_start:
        byte = masked[cursor]
        if byte == ord("{") and not _is_escaped(masked, cursor, environment.begin_end):
            brace_depth += 1
            cursor += 1
            continue
        if byte == ord("}") and not _is_escaped(masked, cursor, environment.begin_end):
            brace_depth -= 1
            if brace_depth < 0:
                raise ValueError("invalid brace depth in LaTeX display environment")
            cursor += 1
            continue
        if (
            byte == ord("\\")
            and cursor + 1 < environment.end_start
            and masked[cursor + 1] == ord("\\")
            and brace_depth == 0
        ):
            add_part(start, cursor, True)
            cursor += 2
            start = cursor
            continue
        cursor += 1
    if brace_depth != 0:
        raise ValueError("invalid brace depth in LaTeX display environment")
    add_part(start, environment.end_start, False)
    return parts


def _label_facts(raw: bytes, start: int, end: int) -> tuple[list[str], list[dict[str, int | str]]]:
    labels: list[str] = []
    spans: list[dict[str, int | str]] = []
    for match in _LABEL_RE.finditer(_comment_mask(raw[start:end])):
        label = match.group(1).decode("utf-8", "strict")
        absolute_start = start + match.start()
        absolute_end = start + match.end()
        labels.append(label)
        spans.append(
            {
                "label": label,
                "start_byte": absolute_start,
                "end_byte": absolute_end,
                "line_start": _line_number_at(raw, absolute_start),
                "line_end": _line_number_at(raw, absolute_end),
            }
        )
    return labels, spans


def _strip_labels(text: str) -> str:
    return re.sub(r"\\label\s*\{[^{}]+\}", "", text).strip()


def locate_equations_in_bytes(raw: bytes, *, relative_path: str = "<memory>") -> list[dict]:
    """Locate source rows using half-open UTF-8 byte intervals."""
    environments = _localized_environments(raw)
    source_digest = hashlib.sha256(raw).hexdigest()
    by_start = {item.start: item for item in environments}
    parent_starts = {start for item in environments for start in item.ancestor_starts}
    rows: list[EquationRow] = []

    # Rows are emitted from innermost supported environments. Parent display
    # tokens remain in the environment stack but cannot duplicate child math.
    for environment in environments:
        if environment.start in parent_starts:
            continue
        descriptors = _environment_descriptors(environment, by_start, source_digest)
        environment_ids = [item["environment_id"] for item in descriptors]
        for row_index, (start, end, terminated, sequence_group) in enumerate(_row_parts(raw, environment)):
            source_text = raw[start:end].decode("utf-8", "strict")
            labels, label_spans = _label_facts(raw, start, end)
            explicit_label = labels[0] if len(labels) == 1 else None
            uncertainty: list[str] = []
            if "\\" in source_text and "\\label" not in source_text:
                uncertainty.append("macros_not_expanded")
            if environment.kind in {"align", "alignat", "aligned"} and "&" in source_text:
                uncertainty.append("alignment_markers_preserved")
            if len(labels) > 1:
                uncertainty.append("multiple_explicit_labels")
            label_span = None
            if len(label_spans) == 1:
                label_span = {key: int(label_spans[0][key]) for key in ("start_byte", "end_byte", "line_start", "line_end")}
            rows.append(
                EquationRow(
                    id=f"{relative_path}:{_line_number_at(raw, start)}:{environment.kind}:{row_index}",
                    environment=environment.kind,
                    file=relative_path,
                    line_start=_line_number_at(raw, start),
                    line_end=_line_number_at(raw, end),
                    label=explicit_label,
                    row_index=row_index,
                    text=_strip_labels(source_text),
                    source_text=source_text,
                    localization_status="localized_with_uncertainty" if uncertainty else "localized",
                    uncertainty=uncertainty,
                    byte_start=start,
                    byte_end=end,
                    environment_id=str(descriptors[-1]["environment_id"]),
                    environment_start_byte=environment.start,
                    environment_end_byte=environment.end,
                    environment_starred=environment.starred,
                    environment_stack=environment_ids,
                    environment_stack_descriptors=descriptors,
                    explicit_label=explicit_label,
                    explicit_labels=labels,
                    label_span=label_span,
                    label_spans=label_spans,
                    has_nonumber=_NUMBER_SUPPRESSOR_RE.search(_comment_mask(raw[start:end])) is not None,
                    had_row_terminator=terminated,
                    ownership_status="unallocated",
                    source_digest=source_digest,
                    locator_version=P02_LOCATOR_VERSION,
                    sequence_group=sequence_group,
                )
            )
    return [asdict(row) for row in rows]


def locate_equations_in_text(text: str, *, relative_path: str = "<memory>") -> list[dict]:
    return locate_equations_in_bytes(text.encode("utf-8"), relative_path=relative_path)


def locate_equations_in_file(path: Path, *, root: Path | None = None) -> list[dict]:
    root = root.resolve() if root is not None else path.parent.resolve()
    try:
        relative_path = str(path.resolve().relative_to(root))
    except ValueError:
        relative_path = str(path)
    return locate_equations_in_bytes(path.read_bytes(), relative_path=relative_path)


def summarize_equation_localization(rows: list[dict]) -> dict:
    uncertain = [row for row in rows if row.get("uncertainty")]
    by_environment: dict[str, int] = {}
    for row in rows:
        env = str(row.get("environment", "unknown"))
        by_environment[env] = by_environment.get(env, 0) + 1
    return attach_contract(
        {
            "status": "localized" if rows and not uncertain else "localized_with_uncertainty" if rows else "not_found",
            "reason": "Equation rows were localized with source spans." if rows else "No display equations were found.",
            "row_count": len(rows),
            "uncertain_row_count": len(uncertain),
            "by_environment": by_environment,
        },
        "equation_localization_summary",
    )
