from pathlib import Path

from mathdevmcp.implementation_audit import audit_implementation_label
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_implementation_label as server_audit_implementation_label


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
LABEL = "eq:dept-state-space-likelihood"


def test_implementation_audit_missing_solve_reports_mismatch():
    result = audit_implementation_label(
        str(FIXTURES),
        LABEL,
        str(FIXTURES / "doc_department_state_space_missing_solve.py"),
        required_terms=["logdet"],
        required_operations=["logdet", "inverse_or_solve"],
    )

    assert result["status"] == "mismatch"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_audit_result"}
    assert result["term_comparison"]["metadata"]["contract"] == "label_consistency_result"
    assert result["ast_operation_graph"]["metadata"]["contract"] == "ast_operation_graph"
    assert result["semantic_alignment"]["metadata"]["contract"] == "semantic_alignment_report"
    assert result["shape_semantics"]["metadata"]["contract"] == "shape_semantic_report"
    assert result["proof_audit_v2"]["metadata"]["contract"] == "proof_audit_v2_result"
    assert any(action["kind"] == "required_operation_missing" for action in result["actions"])
    assert "inverse_or_solve" in result["semantic_alignment"]["required_operations"]


def test_implementation_audit_good_fixture_is_diagnostic_not_verified():
    result = audit_implementation_label(
        str(FIXTURES),
        LABEL,
        str(FIXTURES / "doc_department_state_space_jax.py"),
        required_terms=["logdet"],
        required_operations=["logdet", "inverse_or_solve"],
    )

    assert result["status"] in {"consistent", "unverified"}
    assert result["status"] != "verified"
    assert "verified" not in {result["status"], result["shape_semantics"]["status"], result["semantic_alignment"]["status"]}
    assert result["required_operations"] == ["logdet", "inverse_or_solve"]
    assert "logdet" in result["observed_operations"]
    assert "inverse_or_solve" in result["observed_operations"]
    assert "diagnostic" in result["verification_boundary"].lower()


def test_mcp_preferred_implementation_audit_has_new_contract_and_alias_stays_legacy():
    args = {
        "root": str(FIXTURES),
        "label": LABEL,
        "code": str(FIXTURES / "doc_department_state_space_missing_solve.py"),
        "required_terms": ["logdet"],
        "required_operations": ["logdet", "inverse_or_solve"],
    }

    preferred = call_mcp_tool("audit_implementation_label", args)
    legacy = call_mcp_tool("compare_label_code", args)
    tools = {tool["name"]: tool for tool in list_mcp_tools()}

    assert preferred["metadata"] == {"schema_version": "1.0", "contract": "implementation_audit_result"}
    assert preferred["status"] == "mismatch"
    assert legacy["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert "ast_operation_graph" not in legacy
    assert tools["audit_implementation_label"]["output_contract"] == "implementation_audit_result"
    assert tools["compare_label_code"]["output_contract"] == "label_consistency_result"


def test_fastmcp_wrapper_exposes_implementation_audit_contract():
    result = server_audit_implementation_label(
        str(FIXTURES),
        LABEL,
        str(FIXTURES / "doc_department_state_space_missing_solve.py"),
        required_terms=["logdet"],
        required_operations=["logdet", "inverse_or_solve"],
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_audit_result"}
    assert result["status"] == "mismatch"
