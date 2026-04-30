"""Install the MathDevMCP workflow rules into a non-Claude MCP client's
project-level instructions file.

Behavior is idempotent and non-destructive:

  - If the target file does not exist, create it with the rules block
    (wrapped in marker comments) at the top.
  - If the target file exists and already contains a marked block,
    replace just that block — preserving anything else the user has put
    in the file.
  - If the target file exists but contains no marked block, append the
    marked block at the end with a blank line separator.

`--dry-run` reports what would happen without writing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from ._workflow_rules import MARKER_END, MARKER_START, marked_block


CLIENT_TARGETS: dict[str, Path] = {
    "cursor": Path(".cursorrules"),
    "copilot": Path(".github") / "copilot-instructions.md",
}

CLIENT_CHOICES = ("cursor", "copilot", "all")


@dataclass(frozen=True)
class InstallResult:
    client: str
    path: Path
    action: str       # "create" | "replace" | "append" | "unchanged"
    performed: bool   # True if the file was actually written; False under --dry-run
    reason: str

    def describe(self) -> str:
        """Human-readable verb phrase suitable for CLI output."""
        if self.action == "unchanged":
            return "unchanged"
        if self.performed:
            return {"create": "created", "replace": "replaced", "append": "appended"}[self.action]
        return {"create": "would create", "replace": "would replace", "append": "would append"}[self.action]


_BLOCK_RE = re.compile(
    rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?",
    flags=re.DOTALL,
)


def _classify(existing: str | None, target_block: str) -> tuple[str, str]:
    """Decide what action to take. Returns (action, reason)."""
    if existing is None:
        return "create", "target file did not exist; will create with rules block"
    if MARKER_START in existing and MARKER_END in existing:
        current = _BLOCK_RE.search(existing)
        if current is not None and current.group(0).rstrip("\n") == target_block.rstrip("\n"):
            return "unchanged", "rules block already current"
        return "replace", "existing marked block was out of date; will replace"
    return "append", "target file existed with other content; will append marked block"


def _next_text(existing: str | None, target_block: str, action: str) -> str:
    if action == "create":
        return target_block
    assert existing is not None
    if action == "unchanged":
        return existing
    if action == "replace":
        # Use a lambda replacement so backslashes in the rules text (LaTeX
        # commands like \label, \begin) are not interpreted as regex
        # backreferences in the replacement string.
        return _BLOCK_RE.sub(lambda _match: target_block, existing, count=1)
    # append
    separator = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    return f"{existing}{separator}{target_block}"


def install_for_client(client: str, root: Path, *, dry_run: bool = False) -> InstallResult:
    if client not in CLIENT_TARGETS:
        raise ValueError(f"Unknown client: {client}. Expected one of: {', '.join(CLIENT_TARGETS)}")
    target = (root / CLIENT_TARGETS[client]).resolve()
    existing = target.read_text(encoding="utf-8") if target.exists() else None
    block = marked_block()
    action, reason = _classify(existing, block)
    if dry_run or action == "unchanged":
        return InstallResult(client=client, path=target, action=action, performed=False, reason=reason)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_next_text(existing, block, action), encoding="utf-8")
    return InstallResult(client=client, path=target, action=action, performed=True, reason=reason)


def install_rules(clients: list[str], *, root: Path | None = None, dry_run: bool = False) -> list[InstallResult]:
    if not clients:
        raise ValueError("At least one client must be specified")
    expanded: list[str] = []
    for client in clients:
        if client == "all":
            expanded.extend(CLIENT_TARGETS)
        else:
            expanded.append(client)
    seen: set[str] = set()
    deduped = [c for c in expanded if not (c in seen or seen.add(c))]
    base = (root or Path.cwd()).resolve()
    return [install_for_client(client, base, dry_run=dry_run) for client in deduped]
