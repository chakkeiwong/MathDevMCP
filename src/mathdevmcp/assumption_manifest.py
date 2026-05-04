"""Minimal assumption manifest parser and linter."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .contracts import attach_contract


@dataclass(frozen=True)
class ManifestObject:
    name: str
    kind: str
    shape: list[Any]
    properties: dict[str, Any]


def _load_text_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except Exception:
        # Tiny fallback: accept JSON-compatible YAML, which is enough for safe fixtures.
        return json.loads(text)
    loaded = yaml.safe_load(text)
    return loaded if isinstance(loaded, dict) else {}


def load_assumption_manifest(path: str | Path) -> dict:
    path = Path(path)
    try:
        manifest = _load_text_manifest(path)
    except Exception as exc:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": f"Assumption manifest could not be parsed: {exc.__class__.__name__}.",
                "path": str(path),
                "objects": [],
                "rules": [],
                "domains": [],
                "findings": [{"kind": "manifest_parse_failed", "severity": "high", "reason": str(exc)}],
            },
            "assumption_manifest",
        )
    objects = []
    for name, spec in (manifest.get("objects") or {}).items():
        spec = spec if isinstance(spec, dict) else {}
        properties = {key: value for key, value in spec.items() if key not in {"kind", "shape"}}
        objects.append(asdict(ManifestObject(str(name), str(spec.get("kind", "unknown")), list(spec.get("shape", [])), properties)))
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Assumption manifest parsed.",
            "path": str(path),
            "objects": objects,
            "rules": list(manifest.get("rules") or []),
            "domains": list(manifest.get("domains") or []),
            "findings": [],
        },
        "assumption_manifest",
    )


def assumptions_from_manifest(manifest: dict) -> list[dict]:
    assumptions: list[dict] = []
    for obj in manifest.get("objects", []):
        name = obj.get("name")
        kind = obj.get("kind")
        if name and kind:
            assumptions.append({"text": f"{name} is a {kind}", "status": "explicit_assumption", "source": "assumption_manifest"})
        shape = obj.get("shape")
        if name and shape:
            assumptions.append({"text": f"{name} has shape {shape}", "status": "explicit_assumption", "source": "assumption_manifest"})
        for prop, value in obj.get("properties", {}).items():
            if value is True:
                assumptions.append({"text": f"{name} is {prop}", "status": "explicit_assumption", "source": "assumption_manifest"})
    for rule in manifest.get("rules", []):
        assumptions.append({"text": f"rule:{rule}", "status": "explicit_assumption", "source": "assumption_manifest"})
    return assumptions


def lint_assumption_manifest(manifest: dict, index: dict | None = None) -> dict:
    findings: list[dict] = []
    names = [obj.get("name") for obj in manifest.get("objects", []) if obj.get("name")]
    if len(names) != len(set(names)):
        findings.append({"kind": "duplicate_manifest_object", "severity": "high", "reason": "Manifest declares the same object more than once."})
    if index is not None:
        index_text = " ".join(str(block.get("text", "")) for block in index.get("blocks", []))
        for name in names:
            if name and str(name) not in index_text:
                findings.append({"kind": "manifest_symbol_not_found", "severity": "medium", "target": name, "reason": "Manifest symbol was not found in indexed LaTeX text."})
    status = "mismatch" if any(item.get("severity") == "high" for item in findings) else "consistent"
    return attach_contract(
        {"status": status, "reason": "Assumption manifest lint completed.", "findings": findings},
        "assumption_manifest_lint",
    )
