from mathdevmcp.ast_operation_graph import build_ast_operation_graph
from mathdevmcp.code_contracts import diagnose_code_contracts


def test_code_contracts_detect_shape_dtype_batch_and_finite_evidence():
    graph = build_ast_operation_graph(
        """
def target(x):
    assert x.shape[0] > 0
    y = x.astype("float64")
    batch = y.shape[0]
    return isfinite(y).all()
"""
    )
    result = diagnose_code_contracts(graph)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "code_contract_diagnostics"}
    statuses = {finding["kind"]: finding["status"] for finding in result["findings"]}
    assert statuses["shape_contract"] == "supported"
    assert statuses["dtype_contract"] == "supported"
    assert statuses["batch_axis_contract"] == "supported"
    assert statuses["finite_value_contract"] == "supported"


def test_code_contracts_report_missing_policies_as_unverified():
    graph = build_ast_operation_graph(
        """
def target(x):
    return x + 1
"""
    )
    result = diagnose_code_contracts(graph)

    assert result["status"] == "unverified"
    assert any(finding["kind"] == "dtype_contract" for finding in result["findings"])
    assert "not mathematical proof" in result["verification_boundary"]
