from pathlib import Path

from mathdevmcp.consistency import compare_label_to_code
from mathdevmcp.derivation import derive_step_for_label


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_compare_label_to_code_attaches_contract_metadata_and_provenance():
    result = compare_label_to_code(
        str(FIXTURES),
        "prop:transport-mismatch",
        str(FIXTURES / "doc_consistency_bad.py"),
        required_terms=["logdet"],
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert result["provenance"] == {
        "file": "doc_consistency_bad.tex",
        "line_start": 1,
        "line_end": 3,
        "label": "prop:transport-mismatch",
        "block_id": "doc_consistency_bad.tex:1:proposition:prop:transport-mismatch",
        "section_path": [],
    }


def test_derive_step_for_label_attaches_contract_metadata_and_provenance():
    result = derive_step_for_label(
        str(FIXTURES),
        "prop:transport-implementation",
        "log pi(u) + logdet",
        "logdet + log pi(u)",
        paragraph_context=True,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "label_derivation_result"}
    assert result["provenance"] == {
        "file": "doc_consistency_context.tex",
        "line_start": 4,
        "line_end": 6,
        "label": "prop:transport-implementation",
        "block_id": "doc_consistency_context.tex:4:proposition:prop:transport-implementation",
        "section_path": ["Transport implementation context"],
    }
