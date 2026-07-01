from mathdevmcp.derive_or_refute import derive_or_refute
from mathdevmcp.equation_code_match import code_implements_equation
from mathdevmcp.math_review_packet import build_math_review_packet
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.notation_reconciliation import reconcile_notation


def test_math_review_packet_aggregates_true_identity_without_overclaim() -> None:
    evidence = derive_or_refute("a + b = b + a")
    packet = build_math_review_packet("Can we derive commutativity?", evidence=[evidence])

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "math_review_packet"}
    assert packet["status"] == "review_ready"
    assert packet["obligations"]
    assert "not a proof certificate" in packet["certification_boundary"]


def test_math_review_packet_blocks_false_identity() -> None:
    evidence = derive_or_refute("1 + 1 = 3")
    packet = build_math_review_packet("Can we prove 1+1=3?", evidence=[evidence])

    assert packet["status"] == "blocked_by_refutation"
    assert any(attempt["status"] == "refuted" for attempt in packet["backend_attempts"])


def test_math_review_packet_marks_missing_assumptions_for_review() -> None:
    evidence = {"status": "missing_assumptions", "actions": [{"kind": "add_assumption"}]}
    packet = build_math_review_packet("Can we use log(x)?", evidence=[evidence])

    assert packet["status"] == "needs_human_review"
    assert packet["actions"] == [{"kind": "add_assumption"}]


def test_math_review_packet_keeps_code_mismatch_nested() -> None:
    evidence = code_implements_equation("logdet(S)", "def f(S):\n    return trace(S)\n")
    packet = build_math_review_packet("Does code implement logdet(S)?", evidence=[evidence])

    assert packet["status"] == "needs_human_review"
    assert packet["code_links"][0]["status"] == "mismatch"


def test_math_review_packet_keeps_notation_conflict_visible() -> None:
    evidence = reconcile_notation(
        [{"symbol": "r", "alias_of": "r", "sign": "+"}],
        [{"symbol": "r", "alias_of": "r", "sign": "-"}],
    )
    packet = build_math_review_packet("Are conventions aligned?", evidence=[evidence])

    assert packet["status"] == "needs_human_review"
    assert packet["notation_conflicts"][0]["kind"] == "sign"


def test_math_review_packet_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "math_review_packet",
        {"question": "Review claim", "evidence": [{"status": "missing_assumptions"}]},
    )

    assert "math_review_packet" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "math_review_packet"
    assert result["status"] == "needs_human_review"
