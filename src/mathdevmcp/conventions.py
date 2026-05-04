"""Notation and sign-convention registry helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .contracts import attach_contract


@dataclass(frozen=True)
class ConventionRecord:
    id: str
    kind: str
    description: str
    applies_to: list[str]
    sign: str | None = None


def load_convention_registry(path: str | Path) -> dict:
    path = Path(path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": f"Convention registry could not be parsed: {exc.__class__.__name__}.",
                "path": str(path),
                "conventions": [],
                "findings": [{"kind": "convention_registry_parse_failed", "severity": "high", "reason": str(exc)}],
            },
            "convention_registry",
        )
    records = []
    for item in raw.get("conventions", []):
        if isinstance(item, dict):
            records.append(
                asdict(
                    ConventionRecord(
                        id=str(item.get("id", "")),
                        kind=str(item.get("kind", "unknown")),
                        description=str(item.get("description", "")),
                        applies_to=[str(value) for value in item.get("applies_to", [])],
                        sign=str(item["sign"]) if item.get("sign") is not None else None,
                    )
                )
            )
    findings = []
    ids = [record["id"] for record in records if record["id"]]
    if len(ids) != len(set(ids)):
        findings.append({"kind": "duplicate_convention_id", "severity": "high", "reason": "Convention ids must be unique."})
    status = "mismatch" if findings else "consistent"
    return attach_contract(
        {
            "status": status,
            "reason": "Convention registry parsed.",
            "path": str(path),
            "conventions": records,
            "findings": findings,
        },
        "convention_registry",
    )


def find_conventions_for_label(registry: dict, label: str) -> dict:
    matches = [
        item
        for item in registry.get("conventions", [])
        if label in item.get("applies_to", []) or "*" in item.get("applies_to", [])
    ]
    return attach_contract(
        {
            "status": "consistent" if matches else "inconclusive",
            "reason": "Conventions were matched for label." if matches else "No explicit convention matched the label.",
            "label": label,
            "conventions": matches,
        },
        "label_convention_context",
    )
