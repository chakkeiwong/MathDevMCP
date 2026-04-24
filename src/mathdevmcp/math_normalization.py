from __future__ import annotations

import re


def normalize_math_text(text: str) -> str:
    replacements = {
        r"\\log": "log",
        r"\\pi": "pi",
        r"\\det": "det",
        r"\\left": "",
        r"\\right": "",
        "π": "pi",
    }
    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"\\([A-Za-z]+)\s*\(([^()]*)\)", r"\1\2", normalized)
    normalized = re.sub(r"([A-Za-z]+)\s*\(([^()]*)\)", r"\1\2", normalized)
    normalized = re.sub(r"\\([A-Za-z]+)", r"\1", normalized)
    return re.sub(r"\s+", "", normalized)


def normalize_math_tokens(text: str) -> str:
    normalized = text
    replacements = {
        r"\\log": "log",
        r"\\pi": "pi",
        r"\\det": "det",
        r"\\left": "",
        r"\\right": "",
        "π": "pi",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"\\([A-Za-z]+)\s*\(([^()]*)\)", r"\1 \2", normalized)
    normalized = re.sub(r"([A-Za-z]+)\s*\(([^()]*)\)", r"\1 \2", normalized)
    normalized = re.sub(r"\\([A-Za-z]+)", r"\1", normalized)
    normalized = re.sub(r"[:()+\-=]", " ", normalized)
    return normalized
