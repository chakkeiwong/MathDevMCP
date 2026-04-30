from pathlib import Path

from mathdevmcp.benchmarks import build_benchmark_report
from mathdevmcp.consistency import compare_label_to_code
from mathdevmcp.contracts import validate_contract_payload, validate_derivation_evidence, validate_consistency_findings
from mathdevmcp.derivation import derive_step_for_label
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.workflow import build_implementation_brief


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent


def test_implementation_brief_returns_success_envelope_when_no_label_found():
    result = build_implementation_brief(
        str(FIXTURES),
        "query with no matching label",
        str(FIXTURES / "doc_consistency_good.py"),
    )

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"}



def test_mcp_facade_returns_structured_invalid_arguments_error():
    result = call_mcp_tool("check_equality", {"lhs": "a"})

    assert result == {
        "ok": False,
        "error": {"type": "invalid_arguments", "message": "Missing required string argument: rhs"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }


def test_mcp_facade_returns_structured_tool_execution_error(monkeypatch):
    from mathdevmcp.mcp_facade import TOOL_HANDLERS

    def broken_handler(_args):
        raise RuntimeError("/home/chakwong/private/details")

    monkeypatch.setitem(TOOL_HANDLERS, "check_equality", broken_handler)
    result = call_mcp_tool("check_equality", {"lhs": "a", "rhs": "a"})

    assert result == {
        "ok": False,
        "error": {"type": "tool_execution_error", "message": "MathDevMCP tool failed during execution: check_equality"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }
    assert validate_contract_payload(result) == []



def test_validate_contract_payload_accepts_success_and_error_envelopes():
    success = build_implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
    )
    error = call_mcp_tool("check_equality", {"lhs": "a"})

    assert validate_contract_payload(success) == []
    assert validate_contract_payload(error) == []



def test_validate_contract_payload_rejects_missing_or_wrong_contract_fields():
    assert validate_contract_payload({}) == ["missing ok"]
    assert validate_contract_payload({"ok": True}) == ["missing metadata"]
    assert validate_contract_payload({"ok": True, "metadata": {"schema_version": "2.0", "contract": "x"}}) == [
        "metadata.schema_version must be 1.0"
    ]
    assert validate_contract_payload({"ok": False, "metadata": {"schema_version": "1.0", "contract": "error"}}) == [
        "error payload missing error"
    ]



def test_benchmark_report_contract_is_validated_recursively():
    report = build_benchmark_report(ROOT)

    assert validate_contract_payload(report) == []



def test_validate_consistency_findings_accepts_current_nested_schema():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-implementation",
        str(FIXTURES / "doc_consistency_context_good.py"),
        paragraph_context=True,
        required_terms=["logdet"],
    )

    assert validate_consistency_findings(result["findings"]) == []



def test_validate_derivation_evidence_accepts_current_nested_schema():
    result = derive_step_for_label(
        str(FIXTURES),
        "prop:transport-implementation",
        "log pi(u) + logdet",
        "logdet + log pi(u)",
        paragraph_context=True,
    )

    assert validate_derivation_evidence(result["evidence"]) == []



def test_nested_schema_validators_reject_malformed_items():
    assert validate_consistency_findings([{"kind": "missing_term", "term": "logdet", "severity": "audit_only"}]) == [
        "findings[0].present_in_code must be a boolean",
        "findings[0].severity must be required for missing_term",
    ]
    assert validate_derivation_evidence([{"kind": "symbol_mismatch", "severity": "supporting"}]) == [
        "evidence[0].severity must be blocking for symbol_mismatch"
    ]
