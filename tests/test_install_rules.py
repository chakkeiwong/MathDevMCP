"""Tests for the `mathdevmcp install-rules` workflow-rules installer."""

from __future__ import annotations

from pathlib import Path

import pytest

from mathdevmcp._install_rules import (
    CLIENT_TARGETS,
    InstallResult,
    install_for_client,
    install_rules,
)
from mathdevmcp._workflow_rules import MARKER_END, MARKER_START, WORKFLOW_RULES


def test_install_create_when_target_missing(tmp_path: Path):
    result = install_for_client("cursor", tmp_path)

    assert result.action == "create"
    assert result.performed is True
    target = tmp_path / ".cursorrules"
    assert target.exists()
    text = target.read_text(encoding="utf-8")
    assert text.startswith(MARKER_START)
    assert text.rstrip().endswith(MARKER_END)
    assert WORKFLOW_RULES.strip() in text


def test_install_unchanged_when_block_already_current(tmp_path: Path):
    install_for_client("cursor", tmp_path)
    second = install_for_client("cursor", tmp_path)

    assert second.action == "unchanged"
    assert second.performed is False


def test_install_replaces_outdated_marked_block(tmp_path: Path):
    target = tmp_path / ".cursorrules"
    target.write_text(
        f"# project rules\n\n{MARKER_START}\nold mathdevmcp content\n{MARKER_END}\n",
        encoding="utf-8",
    )

    result = install_for_client("cursor", tmp_path)

    assert result.action == "replace"
    assert result.performed is True
    text = target.read_text(encoding="utf-8")
    assert "old mathdevmcp content" not in text
    assert "# project rules" in text
    assert WORKFLOW_RULES.strip() in text


def test_install_appends_when_target_has_unrelated_content(tmp_path: Path):
    target = tmp_path / ".cursorrules"
    target.write_text("# my own rules\n\nDo X.\n", encoding="utf-8")

    result = install_for_client("cursor", tmp_path)

    assert result.action == "append"
    assert result.performed is True
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# my own rules")
    assert "Do X." in text
    assert MARKER_START in text
    assert MARKER_END in text


def test_install_creates_parent_directory_for_copilot(tmp_path: Path):
    result = install_for_client("copilot", tmp_path)

    assert result.action == "create"
    assert (tmp_path / ".github" / "copilot-instructions.md").exists()


def test_dry_run_does_not_write(tmp_path: Path):
    result = install_for_client("cursor", tmp_path, dry_run=True)

    assert result.action == "create"
    assert result.performed is False
    assert not (tmp_path / ".cursorrules").exists()


def test_install_rules_all_expands_to_every_client(tmp_path: Path):
    results = install_rules(["all"], root=tmp_path)

    clients = [r.client for r in results]
    assert set(clients) == set(CLIENT_TARGETS)
    for r in results:
        assert r.performed is True


def test_install_rules_deduplicates_repeated_clients(tmp_path: Path):
    results = install_rules(["cursor", "all", "cursor"], root=tmp_path)

    clients = [r.client for r in results]
    assert clients.count("cursor") == 1


def test_unknown_client_raises_value_error(tmp_path: Path):
    with pytest.raises(ValueError, match="Unknown client"):
        install_for_client("vim", tmp_path)


def test_describe_phrasing(tmp_path: Path):
    created = install_for_client("cursor", tmp_path)
    assert created.describe() == "created"

    unchanged = install_for_client("cursor", tmp_path)
    assert unchanged.describe() == "unchanged"

    dry = install_for_client("copilot", tmp_path, dry_run=True)
    assert dry.describe() == "would create"
