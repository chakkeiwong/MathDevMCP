import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp._install_rules import BEGIN_MARKER, END_MARKER, install_rules
from mathdevmcp._workflow_rules import WORKFLOW_RULES_TEXT, validate_workflow_rules_against_mcp_surface, WORKFLOW_CALL_EXAMPLES
from mathdevmcp.mcp_facade import MCP_TOOL_SPECS


ROOT = Path(__file__).resolve().parent.parent


def test_workflow_rules_doc_matches_packaged_rules():
    text = (ROOT / "docs" / "clients" / "workflow-rules.md").read_text(encoding="utf-8")

    assert text.rstrip("\n") == WORKFLOW_RULES_TEXT


def test_workflow_rules_examples_are_schema_valid_and_use_registered_tools():
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}

    assert validate_workflow_rules_against_mcp_surface() == []
    assert {example.tool for example in WORKFLOW_CALL_EXAMPLES}.issubset(registry_names)
    assert "paragraph_context" not in WORKFLOW_RULES_TEXT


def test_install_rules_cursor_is_idempotent_and_preserves_existing_text(tmp_path):
    target = tmp_path / ".cursorrules"
    target.write_text("Existing project guidance.\n", encoding="utf-8")

    first = install_rules(tmp_path, "cursor")
    second = install_rules(tmp_path, "cursor")
    text = target.read_text(encoding="utf-8")

    assert first["results"][0]["status"] == "updated"
    assert second["results"][0]["status"] == "unchanged"
    assert text.startswith("Existing project guidance.")
    assert text.count(BEGIN_MARKER) == 1
    assert text.count(END_MARKER) == 1
    assert WORKFLOW_RULES_TEXT in text


def test_install_rules_dry_run_does_not_write(tmp_path):
    result = install_rules(tmp_path, "cursor", dry_run=True)

    assert result["status"] == "would_update"
    assert result["results"][0]["status"] == "would_create"
    assert result["results"][0]["content"] is not None
    assert not (tmp_path / ".cursorrules").exists()


def test_install_rules_copilot_creates_parent_directory(tmp_path):
    result = install_rules(tmp_path, "copilot")
    target = tmp_path / ".github" / "copilot-instructions.md"

    assert target.exists()
    assert result["results"][0]["created_parent"] is True
    assert WORKFLOW_RULES_TEXT in target.read_text(encoding="utf-8")


def test_install_rules_all_expands_without_duplicates(tmp_path):
    result = install_rules(tmp_path, "all")

    assert result["clients"] == ["cursor", "copilot"]
    assert len({item["client"] for item in result["results"]}) == 2
    assert (tmp_path / ".cursorrules").exists()
    assert (tmp_path / ".github" / "copilot-instructions.md").exists()


def test_cli_install_rules_reports_json_contract(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "install-rules",
            "cursor",
            "--root",
            str(tmp_path),
            "--dry-run",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["metadata"] == {"schema_version": "1.0", "contract": "install_rules_report"}
    assert payload["status"] == "would_update"
