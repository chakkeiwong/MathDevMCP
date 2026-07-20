"""Small reusable helpers shared by capstone runners and their tests."""

from __future__ import annotations

import re
from typing import Any


def normalized_phrase_present(text: str, phrase: str) -> bool:
    """Return whether a phrase occurs after normalizing whitespace."""

    normalized_phrase = re.sub(r"\s+", " ", phrase).strip()
    normalized_text = re.sub(r"\s+", " ", text).strip()
    return normalized_phrase in normalized_text


def status_of(value: Any) -> str:
    """Return the status used by capstone evidence ledgers."""

    if isinstance(value, dict):
        if isinstance(value.get("status"), str):
            return str(value["status"])
        if isinstance(value.get("error"), dict):
            return str(value["error"].get("code", "error"))
        return "no_status"
    return type(value).__name__
