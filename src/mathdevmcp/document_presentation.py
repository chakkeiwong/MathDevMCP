"""Small, backend-free presentation helpers for document audit workflows."""

from __future__ import annotations

import re
from typing import Any

from .equation_locator import DISPLAY_ENVIRONMENTS


LATEX_COMMANDS_NOT_SYMBOLS = {
    "begin", "end", "label", "left", "right", "mid", "middle", "mathrm",
    "text", "quad", "qquad", "nonumber", "approx", "in", "sum", "max",
    "min", "frac", "partial",
}


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower() or "target"


def sentence(value: Any) -> str:
    text = " ".join(str(value or "").split())
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else f"{text}."


def split_target(text: str) -> tuple[str | None, str | None, str]:
    target = str(text or "").replace("&=", "=").strip().rstrip(",.")
    if "=" not in target:
        return None, None, target
    lhs, rhs = target.split("=", 1)
    return lhs.strip() or None, rhs.strip() or None, f"{lhs.strip()} = {rhs.strip()}"


def line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def display_pattern() -> re.Pattern[str]:
    envs = "|".join(DISPLAY_ENVIRONMENTS)
    return re.compile(
        rf"\\begin\{{(?P<env>{envs})\*?\}}(?P<body>.*?)\\end\{{(?P=env)\*?\}}",
        re.DOTALL,
    )


def strip_display_markup(source: str) -> str:
    text = re.sub(r"\\begin\{[^}]+\*?\}", "", source)
    text = re.sub(r"\\end\{[^}]+\*?\}", "", text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\nonumber\b", "", text)
    return text.strip()


def operator_inventory(text: str) -> list[str]:
    operators: list[str] = []
    checks = [
        ("equality", r"="),
        ("conditional_expectation", r"\\E\b|\\mathbb\{E\}"),
        ("conditional_bar", r"\\mid|\\middle\|"),
        ("summation", r"\\sum(?![A-Za-z])"),
        ("maximum", r"\\max(?![A-Za-z])"),
        ("minimum", r"\\min(?![A-Za-z])"),
        ("derivative", r"\\partial|\\frac\s*\{d|\\frac\s*\{\\partial"),
        ("indicator", r"\\1\{"),
        ("transpose", r"\\top\b"),
        ("integral", r"\\int\b"),
    ]
    for name, pattern in checks:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            operators.append(name)
    return operators


def symbol_inventory(text: str) -> dict[str, list[str]]:
    macros = sorted(
        {
            f"\\{match.group(1)}"
            for match in re.finditer(r"\\([A-Za-z]+)", text)
            if match.group(1) not in LATEX_COMMANDS_NOT_SYMBOLS
        }
    )
    identifiers = sorted(
        {
            item
            for item in re.findall(r"(?<!\\)\b[A-Za-z][A-Za-z0-9_]*\b", re.sub(r"\\[A-Za-z]+", " ", text))
            if len(item) <= 40
        }
    )
    return {"macros": macros, "identifiers": identifiers}
