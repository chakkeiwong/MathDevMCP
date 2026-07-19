from __future__ import annotations

import json
from pathlib import Path

from mathdevmcp.math_document_rigor import audit_math_document_rigor
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.mcp_server import audit_math_document_rigor as server_audit_math_document_rigor


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/industry_dsge_readability_pilot/missing_neumann_condition/document.tex"


def test_library_profiles_and_editorial_contract_are_explicit(tmp_path) -> None:
    actionable = audit_math_document_rigor(
        FIXTURE,
        output_md=tmp_path / "actionable.md",
        focus_labels=["eq:leontief"],
        max_labels=1,
        report_profile="actionable",
        validation_backends=["sympy"],
    )
    forensic = audit_math_document_rigor(
        FIXTURE,
        output_md=tmp_path / "forensic.md",
        focus_labels=["eq:leontief"],
        max_labels=1,
        report_profile="forensic",
        validation_backends=["sympy"],
    )

    assert actionable["report_profile"] == "actionable"
    assert forensic["report_profile"] == "forensic"
    assert actionable["editorial_integration"]["schema_version"] == "exposition_surface_diagnostics@1"
    assert actionable["editorial_integration"]["records"][0]["source"] == actionable["source"]
    assert actionable["actionable_markdown"] == (tmp_path / "actionable.md").read_text(encoding="utf-8")
    assert forensic["forensic_markdown"] == (tmp_path / "forensic.md").read_text(encoding="utf-8")
    assert "## Backend Provenance" not in actionable["markdown"]
    assert "## Backend Provenance" in forensic["markdown"]


def test_facade_and_fastmcp_use_same_profile_contract(tmp_path) -> None:
    args = {
        "tex_path": str(FIXTURE),
        "focus_labels": ["eq:leontief"],
        "max_labels": 1,
        "report_profile": "forensic",
        "validation_backends": ["sympy"],
        "output_json": str(tmp_path / "facade.json"),
    }
    facade = call_mcp_tool("audit_math_document_rigor", args)
    server = server_audit_math_document_rigor(
        str(FIXTURE),
        focus_labels=["eq:leontief"],
        max_labels=1,
        report_profile="forensic",
        validation_backends=["sympy"],
    )

    assert facade["report_profile"] == server["report_profile"] == "forensic"
    assert facade["source"] == server["source"]
    assert facade["issues"] == server["issues"]
    assert facade["editorial_integration"]["records"][0]["record_digest"] == server["editorial_integration"]["records"][0]["record_digest"]
    assert json.loads((tmp_path / "facade.json").read_text(encoding="utf-8"))["report_profile"] == "forensic"
