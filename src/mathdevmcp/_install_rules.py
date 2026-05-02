"""Install portable MathDevMCP workflow rules into client instruction files."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from ._workflow_rules import WORKFLOW_RULES_TEXT
from .contracts import attach_contract


BEGIN_MARKER = "<!-- BEGIN MATHDEVMCP WORKFLOW RULES -->"
END_MARKER = "<!-- END MATHDEVMCP WORKFLOW RULES -->"
SUPPORTED_CLIENTS = ("cursor", "copilot")


@dataclass(frozen=True)
class InstallRulesResult:
    client: str
    path: str
    status: str
    dry_run: bool
    created_parent: bool
    reason: str
    content: str | None = None


def _target_path(project_root: Path, client: str) -> Path:
    if client == "cursor":
        return project_root / ".cursorrules"
    if client == "copilot":
        return project_root / ".github" / "copilot-instructions.md"
    raise ValueError(f"Unsupported rules client: {client}")


def _marked_block() -> str:
    return f"{BEGIN_MARKER}\n{WORKFLOW_RULES_TEXT}\n{END_MARKER}\n"


def _replace_or_append(existing: str, block: str) -> str:
    if BEGIN_MARKER in existing or END_MARKER in existing:
        start = existing.find(BEGIN_MARKER)
        end = existing.find(END_MARKER)
        if start == -1 or end == -1 or end < start:
            raise ValueError("Existing MathDevMCP workflow-rules markers are malformed.")
        end += len(END_MARKER)
        suffix = existing[end:]
        if suffix.startswith("\n"):
            suffix = suffix[1:]
        return f"{existing[:start]}{block}{suffix}"
    separator = "" if not existing or existing.endswith("\n") else "\n"
    spacer = "" if not existing else "\n"
    return f"{existing}{separator}{spacer}{block}"


def expand_clients(client: str) -> list[str]:
    if client == "all":
        return list(SUPPORTED_CLIENTS)
    if client not in SUPPORTED_CLIENTS:
        raise ValueError(f"Unsupported rules client: {client}")
    return [client]


def install_rules_for_client(project_root: str | Path, client: str, *, dry_run: bool = False) -> dict:
    root = Path(project_root)
    target = _target_path(root, client)
    block = _marked_block()
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    updated = _replace_or_append(existing, block)
    created_parent = not target.parent.exists()
    if updated == existing:
        status = "unchanged"
        reason = "Workflow rules are already installed."
    elif dry_run:
        status = "would_update" if existing else "would_create"
        reason = "Dry run only; no files were modified."
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(updated, encoding="utf-8")
        status = "updated" if existing else "created"
        reason = "Workflow rules were installed."
    result = asdict(
        InstallRulesResult(
            client=client,
            path=str(target),
            status=status,
            dry_run=dry_run,
            created_parent=created_parent and not dry_run and status in {"created", "updated"},
            reason=reason,
            content=updated if dry_run else None,
        )
    )
    return attach_contract(result, "install_rules_result")


def install_rules(project_root: str | Path, client: str, *, dry_run: bool = False) -> dict:
    clients = expand_clients(client)
    results = [install_rules_for_client(project_root, item, dry_run=dry_run) for item in clients]
    status = "unchanged" if all(result["status"] == "unchanged" for result in results) else "updated"
    if dry_run and any(result["status"].startswith("would_") for result in results):
        status = "would_update"
    return attach_contract(
        {
            "status": status,
            "client": client,
            "clients": clients,
            "dry_run": dry_run,
            "results": results,
        },
        "install_rules_report",
    )
