from mathdevmcp.literature_local_audit import literature_local_audit
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.notation_reconciliation import reconcile_notation


THEOREM_ASSUMPTIONS = [
    {"id": "compactness", "text": "Parameter space is compact."},
    {"id": "full_rank", "text": "Information matrix has full rank."},
    {"id": "stationarity", "text": "State process is stationary."},
]


def test_literature_local_audit_full_match_supports_applicability() -> None:
    result = literature_local_audit("theorem:synthetic", THEOREM_ASSUMPTIONS, THEOREM_ASSUMPTIONS)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "literature_local_audit_result"}
    assert result["status"] == "applicability_supported"
    assert len(result["matched_assumptions"]) == 3
    assert "does not verify the paper theorem" in result["applicability_boundary"]


def test_literature_local_audit_reports_missing_compactness() -> None:
    result = literature_local_audit(
        "theorem:synthetic",
        THEOREM_ASSUMPTIONS,
        [item for item in THEOREM_ASSUMPTIONS if item["id"] != "compactness"],
    )

    assert result["status"] == "applicability_gap"
    assert result["missing_assumptions"][0]["assumption_id"] == "compactness"


def test_literature_local_audit_reports_missing_full_rank() -> None:
    result = literature_local_audit(
        "theorem:synthetic",
        THEOREM_ASSUMPTIONS,
        [item for item in THEOREM_ASSUMPTIONS if item["id"] != "full_rank"],
    )

    assert result["status"] == "applicability_gap"
    assert any(item["assumption_id"] == "full_rank" for item in result["missing_assumptions"])


def test_literature_local_audit_reports_stationarity_mismatch() -> None:
    local = [
        {"id": "compactness", "text": "Parameter space is compact."},
        {"id": "full_rank", "text": "Information matrix has full rank."},
        {"id": "stationarity", "text": "Unit root case is allowed.", "status": "conflict"},
    ]

    result = literature_local_audit("theorem:synthetic", THEOREM_ASSUMPTIONS, local)

    assert result["status"] == "applicability_conflict"
    assert result["conflicting_assumptions"][0]["assumption_id"] == "stationarity"


def test_literature_local_audit_reports_notation_conflict() -> None:
    notation = reconcile_notation(
        [{"symbol": "r", "alias_of": "r", "sign": "+"}],
        [{"symbol": "r", "alias_of": "r", "sign": "-"}],
    )

    result = literature_local_audit("theorem:synthetic", THEOREM_ASSUMPTIONS, THEOREM_ASSUMPTIONS, notation_audit=notation)

    assert result["status"] == "applicability_conflict"
    assert result["notation_notes"][0]["kind"] == "sign"


def test_literature_local_audit_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "literature_local_audit",
        {
            "theorem_id": "theorem:synthetic",
            "theorem_assumptions": THEOREM_ASSUMPTIONS,
            "local_assumptions": THEOREM_ASSUMPTIONS,
        },
    )

    assert "literature_local_audit" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "literature_local_audit_result"
    assert result["status"] == "applicability_supported"
