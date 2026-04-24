from pathlib import Path

from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.workflow import build_implementation_brief


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_implementation_brief_returns_success_envelope_when_no_label_found():
    result = build_implementation_brief(
        str(FIXTURES),
        "query with no matching label",
        str(FIXTURES / "doc_consistency_good.py"),
    )

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"}



def test_mcp_facade_returns_structured_invalid_arguments_error():
    result = call_mcp_tool("implementation_brief", {"root": str(FIXTURES), "query": "transport"})

    assert result == {
        "ok": False,
        "error": {"type": "invalid_arguments", "message": "Missing required string argument: code"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }
