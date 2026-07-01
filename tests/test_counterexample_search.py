from mathdevmcp.counterexample_search import find_counterexample
from mathdevmcp.math_debugging import validate_workbench_result


def test_counterexample_search_refutes_false_scalar_identity() -> None:
    result = find_counterexample("x + 1", "x + 2")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "counterexample_search_result"}
    assert result["status"] == "refuted"
    assert result["counterexample"]["lhs_value"] != result["counterexample"]["rhs_value"]
    assert result["workbench_result"]["status"] == "refuted"
    assert validate_workbench_result(result["workbench_result"]) == []


def test_counterexample_search_keeps_no_hit_as_unknown_not_proof() -> None:
    result = find_counterexample("x + y", "y + x")

    assert result["status"] == "unknown"
    assert result["counterexample"] is None
    assert "No counterexample" in result["reason"]
    assert "proof" not in result["reason"].lower()
    assert result["workbench_result"]["backend_attempts"][0]["severity"] == "diagnostic"


def test_counterexample_search_refutes_matrix_commutativity_with_fixed_2x2_example() -> None:
    result = find_counterexample("A*B", "B*A")

    assert result["status"] == "refuted"
    assert result["backend"] == "bounded_matrix_probe"
    assert result["counterexample"]["assignments"]["A"] == [[1, 1], [0, 1]]
    assert result["counterexample"]["lhs_value"] != result["counterexample"]["rhs_value"]


def test_counterexample_search_reports_unsafe_expression_not_encodable() -> None:
    result = find_counterexample("__import__('os')", "0")

    assert result["status"] == "not_encodable"
    assert result["counterexample"] is None
    assert result["workbench_result"]["status"] == "not_encodable"
