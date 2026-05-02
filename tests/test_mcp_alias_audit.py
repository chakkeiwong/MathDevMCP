import json
import subprocess
import sys

from mathdevmcp.mcp_alias_audit import audit_deprecated_alias_usage, deprecated_aliases


def test_deprecated_alias_mapping_comes_from_mcp_registry():
    aliases = deprecated_aliases()

    assert aliases["compare_label_code"] == "audit_implementation_label"
    assert aliases["check_proof_obligation"] == "check_equality"
    assert aliases["extract_latex_neighborhood"] == "latex_label_lookup"


def test_alias_audit_allows_migration_sections(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "operator.md").write_text(
        "Deprecated compatibility alias `compare_label_code` maps to `audit_implementation_label`.\n",
        encoding="utf-8",
    )

    report = audit_deprecated_alias_usage(tmp_path)

    assert report["status"] == "consistent"
    assert report["counts"]["migration_section"] == 1
    assert report["counts"]["active_instruction"] == 0


def test_alias_audit_flags_active_instructions(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("Use `compare_label_code` to check implementations.\n", encoding="utf-8")

    report = audit_deprecated_alias_usage(tmp_path)

    assert report["status"] == "mismatch"
    assert report["counts"]["active_instruction"] == 1
    assert report["findings"][0]["preferred_replacement"] == "audit_implementation_label"


def test_alias_audit_ignores_historical_plans_by_default(tmp_path):
    plans = tmp_path / "docs" / "plans"
    plans.mkdir(parents=True)
    (plans / "old.md").write_text("Use `compare_label_code` in the old proposal.\n", encoding="utf-8")

    default = audit_deprecated_alias_usage(tmp_path)
    historical = audit_deprecated_alias_usage(tmp_path, include_history=True)

    assert default["counts"]["total"] == 0
    assert historical["counts"]["active_instruction"] == 1


def test_cli_audit_mcp_aliases_returns_json_contract(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("Use `compare_label_code` to check implementations.\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "audit-mcp-aliases", "--root", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "mcp_alias_audit_report"}
    assert payload["status"] == "mismatch"
