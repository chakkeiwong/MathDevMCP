from pathlib import Path

from mathdevmcp.derivation import derive_step, derive_step_for_label
from mathdevmcp.tool_matrix import tool_matrix


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_derive_step_marks_identical_sides_equivalent():
    result = derive_step("log_pi + logdet", "log_pi + logdet")

    assert result["status"] == "equivalent"


def test_derive_step_flags_same_symbols_as_unverified():
    result = derive_step("a + b", "b + a")

    assert result["status"] == "unverified"
    assert result["evidence"][0]["kind"] == "symbol_overlap"
    assert result["evidence"][0]["severity"] == "supporting"



def test_derive_step_flags_missing_symbol_as_mismatch():
    result = derive_step("log_pi + logdet", "log_pi")

    assert result["status"] == "mismatch"



def test_derive_step_for_label_returns_conservative_provenance():
    result = derive_step_for_label(
        str(FIXTURES),
        "prop:transport-logdet",
        "log_pi + logdet",
        "logdet + log_pi",
    )

    assert result["status"] == "unverified"
    assert result["label"] == "prop:transport-logdet"
    assert result["doc_context"]["file"] == "doc_consistency_good.tex"
    assert result["supported_by_context"] is False
    assert result["step_chain"] == [{"label": "prop:transport-logdet", "supported_by_context": False, "cited_labels": []}]



def test_derive_step_for_label_detects_normalized_context_support():
    result = derive_step_for_label(
        str(FIXTURES),
        "prop:transport-implementation",
        "log pi(u) + logdet",
        "logdet + log pi(u)",
        paragraph_context=True,
    )

    assert result["status"] == "unverified"
    assert result["supported_by_context"] is True
    assert any(item["kind"] == "label_context" for item in result["evidence"])
    assert any(item["kind"] == "label_context" and item["severity"] == "supporting" for item in result["evidence"])



def test_derive_step_for_label_records_cited_step_chain_metadata():
    result = derive_step_for_label(
        str(FIXTURES),
        "eq:transport-density-step",
        "log pi(u) + logdet",
        "logdet + log pi(u)",
        paragraph_context=True,
    )

    assert result["status"] == "unverified"
    assert result["step_chain"] == [{"label": "eq:transport-density-step", "supported_by_context": True, "cited_labels": []}]
    assert result["metadata"] == {"schema_version": "1.0", "contract": "label_derivation_result"}



def test_tool_matrix_includes_derivation_backed_claims():
    problems = {entry["problem"] for entry in tool_matrix()}

    assert "derivation_backed_claims" in problems
