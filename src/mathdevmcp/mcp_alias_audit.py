"""Audit active references to deprecated MCP tool names."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from .contracts import attach_contract
from .mcp_facade import MCP_TOOL_SPECS


DEFAULT_INCLUDED_DIRS = ("README.md", "mcp", "docs", "scripts")
DEFAULT_IGNORED_PARTS = {"plans", "generated"}
TEXT_SUFFIXES = {
    ".md",
    ".rst",
    ".txt",
    ".tex",
    ".py",
    ".sh",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}


@dataclass(frozen=True)
class DeprecatedAliasFinding:
    deprecated_name: str
    preferred_replacement: str
    file: str
    line: int
    context: str
    classification: str


def deprecated_aliases() -> dict[str, str]:
    return {spec.name: str(spec.replacement) for spec in MCP_TOOL_SPECS if spec.deprecated and spec.replacement}


def _is_candidate(path: Path, root: Path, *, include_history: bool) -> bool:
    rel = path.relative_to(root)
    if not include_history and any(part in DEFAULT_IGNORED_PARTS for part in rel.parts):
        return False
    if path.is_dir():
        return False
    if path.suffix not in TEXT_SUFFIXES and path.name != "README.md":
        return False
    first = rel.parts[0]
    return first in DEFAULT_INCLUDED_DIRS


def _classify(rel_path: str, line: str, previous_lines: list[str]) -> str:
    lowered = line.lower()
    recent = "\n".join(previous_lines[-12:]).lower()
    if (
        "compatibility aliases remain available" in recent
        or "deprecated compatibility names" in recent
        or "deprecated names remain available" in recent
        or "mcp server exposes these tools" in recent
        or "preferred mcp names for new prompts" in recent
    ):
        return "migration_section"
    if "deprecated" in lowered or "compatibility" in lowered or "replacement" in lowered or "migration" in lowered:
        return "migration_section"
    if "tool:" in lowered or "use " in lowered or "call " in lowered or "mcp `" in lowered or "mcp " in lowered:
        return "active_instruction"
    if rel_path.startswith("docs/mathdevmcp-release-report") or "generated" in rel_path:
        return "generated_evidence"
    return "active_instruction"


def audit_deprecated_alias_usage(root: str | Path, *, include_history: bool = False) -> dict:
    project_root = Path(root).resolve()
    aliases = deprecated_aliases()
    patterns = {name: re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])") for name in aliases}
    findings: list[DeprecatedAliasFinding] = []
    for path in sorted(project_root.rglob("*")):
        if not _is_candidate(path, project_root, include_history=include_history):
            continue
        rel = path.relative_to(project_root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            for name, pattern in patterns.items():
                if pattern.search(line):
                    findings.append(
                        DeprecatedAliasFinding(
                            deprecated_name=name,
                            preferred_replacement=aliases[name],
                            file=rel,
                            line=index,
                            context=line.strip(),
                            classification=_classify(rel, line, lines[: index - 1]),
                        )
                    )
    active = [finding for finding in findings if finding.classification == "active_instruction"]
    status = "mismatch" if active else "consistent"
    reason = (
        "Active instructions still reference deprecated MCP aliases."
        if active
        else "No active deprecated MCP alias instructions were found."
    )
    report = {
        "status": status,
        "reason": reason,
        "include_history": include_history,
        "deprecated_aliases": aliases,
        "counts": {
            "total": len(findings),
            "active_instruction": len(active),
            "migration_section": sum(1 for finding in findings if finding.classification == "migration_section"),
            "generated_evidence": sum(1 for finding in findings if finding.classification == "generated_evidence"),
        },
        "findings": [asdict(finding) for finding in findings],
    }
    return attach_contract(report, "mcp_alias_audit_report")
