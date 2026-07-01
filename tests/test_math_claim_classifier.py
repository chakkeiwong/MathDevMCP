from mathdevmcp.claim_support import build_claim_support_packet
from mathdevmcp.derive_or_refute import derive_or_refute
from mathdevmcp.equation_code_match import code_implements_equation
from mathdevmcp.math_claim_classifier import classify_math_claim
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def test_classify_math_claim_marks_backend_proved_derivation() -> None:
    evidence = derive_or_refute("(a+b)*(a-b) = a*a - b*b")

    result = classify_math_claim("(a+b)*(a-b) = a*a - b*b", evidence=[evidence])

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_claim_classification"}
    assert result["classification"] in {"backend_proved", "derived_identity"}
    assert "certify" in result["proof_boundary"]


def test_classify_math_claim_marks_counterexample_as_refuted() -> None:
    evidence = {"status": "refuted", "counterexample": {"x": 0}}

    result = classify_math_claim("x = x + 1", evidence=[evidence])

    assert result["classification"] == "refuted"
    assert result["next_action"] == "inspect_counterexample"


def test_classify_math_claim_keeps_numeric_support_out_of_proof() -> None:
    evidence = {"status": "numeric_supported", "numeric": True}

    result = classify_math_claim("sin(x)^2 + cos(x)^2 = 1", evidence=[evidence])

    assert result["classification"] == "numeric_supported"
    assert result["next_action"] == "seek_symbolic_proof_or_counterexample"


def test_classify_math_claim_keeps_code_match_diagnostic() -> None:
    evidence = code_implements_equation("logdet(S)", "def f(S):\n    return logdet(S)\n")

    result = classify_math_claim("code implements logdet(S)", evidence=[evidence])

    assert result["classification"] == "unsupported"
    assert "diagnostic" in result["reason"]


def test_classify_math_claim_preserves_backend_unavailable_boundary() -> None:
    evidence = {"status": "backend_unavailable", "reason": "Lean unavailable"}

    result = classify_math_claim("P = NP", evidence=[evidence])

    assert result["classification"] == "unsupported"
    assert "not refutation" in result["reason"]


def test_classify_math_claim_uses_claim_support_assumption() -> None:
    evidence = build_claim_support_packet("Assume x > 0.", assumption=True)

    result = classify_math_claim("Assume x > 0.", evidence=[evidence])

    assert result["classification"] == "assumption"
    assert result["next_action"] == "record_assumption_scope"


def test_classify_math_claim_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "classify_math_claim",
        {"claim": "Assume x > 0.", "evidence": [{"metadata": {"contract": "claim_support_packet"}, "claim_status": "model_assumption"}]},
    )

    assert "classify_math_claim" in names
    assert result["ok"] is True
    assert result["classification"] == "assumption"
    assert result["metadata"]["contract"] == "math_claim_classification"
