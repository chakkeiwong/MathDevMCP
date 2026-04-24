from pathlib import Path

from mathdevmcp.code_search import search_files
from mathdevmcp.consistency import compare_doc_to_code
from mathdevmcp.tool_matrix import tool_matrix


def test_search_files_finds_code_and_docs(tmp_path: Path):
    (tmp_path / "doc.tex").write_text("Jacobian determinant identity", encoding="utf-8")
    (tmp_path / "model.py").write_text("def jacobian_logdet():\n    return 0\n", encoding="utf-8")

    hits = search_files(tmp_path, "Jacobian", limit=5)

    assert len(hits) == 2
    assert {hit["kind"] for hit in hits} == {"latex", "code"}


def test_compare_doc_to_code_reports_missing_required_terms(tmp_path: Path):
    result = compare_doc_to_code(
        "The algorithm requires jacobian logdet correction.",
        "def target(u): return likelihood(u)",
        required_terms=["jacobian", "logdet"],
    )

    assert result["status"] == "mismatch"
    assert result["missing_in_code"] == ["jacobian", "logdet"]
    assert {finding["kind"] for finding in result["findings"]} == {"missing_term", "extra_code_terms"}
    assert result["extra_in_code"] == ["def", "likelihood", "return", "target"]
    assert all(finding["severity"] == "required" for finding in result["findings"] if finding["kind"] == "missing_term")
    assert next(finding for finding in result["findings"] if finding["kind"] == "extra_code_terms")["severity"] == "audit_only"


def test_tool_matrix_contains_core_problem_classes():
    problems = {entry["problem"] for entry in tool_matrix()}

    assert "long_document_tracking" in problems
    assert "code_doc_consistency" in problems
    assert "derivation_backed_claims" in problems
    assert "document_grounded_implementation" in problems
