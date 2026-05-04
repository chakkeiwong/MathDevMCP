"""Source-local equation localization for LaTeX display environments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from .contracts import attach_contract


DISPLAY_ENVIRONMENTS = ("equation", "align", "alignat", "aligned", "gather", "multline")


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


def _line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _find_label(text: str) -> str | None:
    match = re.search(r"\\label\{([^}]+)\}", text)
    return match.group(1) if match else None


def _strip_labels(text: str) -> str:
    return re.sub(r"\\label\{[^}]+\}", "", text).strip()


def _environment_pattern() -> re.Pattern[str]:
    envs = "|".join(DISPLAY_ENVIRONMENTS)
    return re.compile(
        rf"\\begin\{{(?P<env>{envs})\*?\}}(?P<body>.*?)\\end\{{(?P=env)\*?\}}",
        re.DOTALL,
    )


def _split_rows(body: str, env: str) -> list[tuple[int, str]]:
    if env in {"align", "alignat", "aligned"}:
        parts = re.split(r"(?<!\\)\\\\", body)
    else:
        parts = [body]
    rows: list[tuple[int, str]] = []
    offset = 0
    for part in parts:
        relative = body.find(part, offset)
        offset = relative + len(part) if relative >= 0 else offset
        stripped = part.strip()
        if stripped:
            leading = len(part) - len(part.lstrip())
            rows.append((max(relative, 0) + leading, stripped))
    return rows


def locate_equations_in_text(text: str, *, relative_path: str = "<memory>") -> list[dict]:
    rows: list[EquationRow] = []
    for match in _environment_pattern().finditer(text):
        env = match.group("env")
        body = match.group("body")
        env_label = _find_label(match.group(0))
        for row_index, (relative_offset, row_text) in enumerate(_split_rows(body, env)):
            row_start_offset = match.start("body") + relative_offset
            row_end_offset = row_start_offset + len(row_text)
            uncertainty: list[str] = []
            if "\\" in row_text and "\\label" not in row_text:
                uncertainty.append("macros_not_expanded")
            if env in {"align", "alignat", "aligned"} and "&" in row_text:
                uncertainty.append("alignment_markers_preserved")
            label = _find_label(row_text) or env_label
            clean_text = _strip_labels(row_text)
            line_start = _line_number_at(text, row_start_offset)
            line_end = _line_number_at(text, row_end_offset)
            rows.append(
                EquationRow(
                    id=f"{relative_path}:{line_start}:{env}:{row_index}",
                    environment=env,
                    file=relative_path,
                    line_start=line_start,
                    line_end=line_end,
                    label=label,
                    row_index=row_index,
                    text=clean_text,
                    source_text=row_text,
                    localization_status="localized_with_uncertainty" if uncertainty else "localized",
                    uncertainty=uncertainty,
                )
            )
    return [asdict(row) for row in rows]


def locate_equations_in_file(path: Path, *, root: Path | None = None) -> list[dict]:
    root = root.resolve() if root is not None else path.parent.resolve()
    text = path.read_text(encoding="utf-8")
    try:
        relative_path = str(path.resolve().relative_to(root))
    except ValueError:
        relative_path = str(path)
    return locate_equations_in_text(text, relative_path=relative_path)


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
