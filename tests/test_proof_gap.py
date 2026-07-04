from mathdevmcp.math_debugging import validate_workbench_result
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.proof_gap import localize_proof_gap


def test_proof_gap_passes_all_verified_chain() -> None:
    result = localize_proof_gap(["a + b", "b + a", "a + b"])

    assert result["metadata"] == {"schema_version": "1.0", "contract": "proof_gap_result"}
    assert result["status"] == "proved"
    assert result["first_gap"] is None
    assert len(result["step_results"]) == 2
    assert validate_workbench_result(result["workbench_result"]) == []


def test_proof_gap_stops_at_first_refuted_step() -> None:
    result = localize_proof_gap(["1 + 1", "3", "3"])

    assert result["status"] == "refuted"
    assert result["first_gap"]["index"] == 0
    assert len(result["step_results"]) == 1
    assert result["workbench_result"]["counterexamples"] == []


def test_proof_gap_reports_missing_assumption_step() -> None:
    result = localize_proof_gap(["logdet(A)", "trace(A)", "trace(A)"])

    assert result["status"] in {"missing_assumptions", "unknown"}
    assert result["first_gap"]["index"] == 0
    assert len(result["step_results"]) == 1


def test_proof_gap_reports_matrix_commutation_refutation() -> None:
    result = localize_proof_gap(["A*B", "B*A"])

    assert result["status"] == "refuted"
    assert result["first_gap"]["status"] == "refuted"
    assert result["workbench_result"]["counterexamples"]


def test_proof_gap_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool("localize_proof_gap", {"steps": ["1 + 1", "3"]})

    assert "localize_proof_gap" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "proof_gap_result"
    assert result["status"] == "refuted"
