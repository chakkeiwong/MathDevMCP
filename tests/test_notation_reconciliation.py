from mathdevmcp.notation_reconciliation import reconcile_notation
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def test_reconcile_notation_matches_explicit_aliases() -> None:
    result = reconcile_notation(
        [{"symbol": "Sigma", "alias_of": "S", "sign": "+", "orientation": "matrix"}],
        [{"symbol": "S", "sign": "+", "orientation": "matrix"}],
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "notation_reconciliation_result"}
    assert result["status"] in {"consistent", "unresolved"}
    assert result["matched_aliases"] == [{"left_symbol": "Sigma", "right_symbol": "S"}]
    assert "does not prove semantic identity" in result["evidence_boundary"]


def test_reconcile_notation_reports_sign_reversal() -> None:
    result = reconcile_notation(
        [{"symbol": "r", "alias_of": "r", "sign": "+"}],
        [{"symbol": "r", "alias_of": "r", "sign": "-"}],
    )

    assert result["status"] == "conflict"
    assert result["conflicts"][0]["kind"] == "sign"


def test_reconcile_notation_reports_alias_conflict() -> None:
    result = reconcile_notation(
        [{"symbol": "beta", "alias_of": "discount"}],
        [{"symbol": "beta", "alias_of": "slope"}],
    )

    assert result["status"] == "conflict"
    assert result["conflicts"][0]["kind"] == "alias_of"


def test_reconcile_notation_reports_time_index_mismatch() -> None:
    result = reconcile_notation(
        [{"symbol": "x", "alias_of": "x", "time_index": "t"}],
        [{"symbol": "x", "alias_of": "x", "time_index": "t+1"}],
    )

    assert result["status"] == "conflict"
    assert result["conflicts"][0]["kind"] == "time_index"


def test_reconcile_notation_reports_orientation_mismatch() -> None:
    result = reconcile_notation(
        [{"symbol": "v", "alias_of": "v", "orientation": "row"}],
        [{"symbol": "v", "alias_of": "v", "orientation": "column"}],
    )

    assert result["status"] == "conflict"
    assert result["conflicts"][0]["kind"] == "orientation"


def test_reconcile_notation_reports_unresolved_alias() -> None:
    result = reconcile_notation(
        [{"symbol": "kappa", "sign": "+"}],
        [{"symbol": "lambda", "sign": "+"}],
    )

    assert result["status"] == "unresolved"
    assert result["unresolved_symbols"]
    assert result["unresolved_symbols"][0]["human_decision_required"] is True


def test_duplicate_alias_candidates_are_not_first_match_resolved() -> None:
    result = reconcile_notation(
        [{"symbol": "Sigma", "alias_of": "S", "orientation": "matrix"}],
        [
            {"symbol": "S", "orientation": "matrix", "domain": "state"},
            {"symbol": "S", "orientation": "matrix", "domain": "observation"},
        ],
    )

    assert result["status"] == "unresolved"
    assert result["matched_aliases"] == []
    assert len(result["candidate_matches"]) == 2
    assert result["ambiguous_aliases"][0]["left_symbol"] == "Sigma"


def test_reconcile_notation_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "reconcile_notation",
        {
            "left_records": [{"symbol": "r", "alias_of": "r", "sign": "+"}],
            "right_records": [{"symbol": "r", "alias_of": "r", "sign": "-"}],
        },
    )

    assert "reconcile_notation" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "notation_reconciliation_result"
    assert result["status"] == "conflict"
