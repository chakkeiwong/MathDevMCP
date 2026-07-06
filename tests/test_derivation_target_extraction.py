from pathlib import Path

from mathdevmcp.derivation_target_extraction import (
    extract_derivation_targets,
    extract_derivation_targets_for_label,
    extract_derivation_targets_from_block,
)
from mathdevmcp.latex_index import build_index


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def test_extract_risky_pricing_target_with_source_provenance() -> None:
    index = build_index(DOCS)

    result = extract_derivation_targets_for_label(index, "prop:risky-pricing")

    assert result["status"] == "extracted"
    assert result["fallback_count"] == 0
    assert len(result["targets"]) == 1
    target = result["targets"][0]
    assert target["id"].endswith(":target:eq:risky-pricing")
    assert target["label"] == "eq:risky-pricing"
    assert target["parent_label"] == "prop:risky-pricing"
    assert target["file"] == "risky-debt-maliar-deep-learning-lecture-note.tex"
    assert target["line_start"] == 399
    assert target["line_end"] == 406
    assert target["lhs"] == "b'(1+r)"
    assert "\\E\\left[" in target["rhs"]
    assert "D(k',b',z')R(k',z')" in target["rhs"]
    assert target["source_text"].strip().endswith("\\label{eq:risky-pricing}")
    assert target["extraction_status"] == "extracted"


def test_extract_interior_foc_align_rows_as_two_targets() -> None:
    index = build_index(DOCS)

    result = extract_derivation_targets_for_label(index, "prop:interior-foc")

    assert result["status"] == "extracted"
    targets = result["targets"]
    assert [target["label"] for target in targets] == ["eq:foc-k", "eq:foc-b"]
    assert [target["line_start"] for target in targets] == [776, 781]
    assert [target["environment"] for target in targets] == ["align", "align"]
    assert [target["lhs"] for target in targets] == ["0", "0"]
    assert "m(\\bar e)\\frac{d\\bar e}{dk'}" in targets[0]["rhs"]
    assert "\\beta \\E[V^\\star_k(k',b',z')\\mid z]" in targets[0]["rhs"]
    assert "m(\\bar e)\\frac{d\\bar e}{db'}" in targets[1]["rhs"]
    assert "\\beta \\E[V^\\star_b(k',b',z')\\mid z]" in targets[1]["rhs"]
    assert all(target["extraction_status"] == "extracted" for target in targets)
    assert all("alignment_markers_preserved" in target["uncertainty"] for target in targets)


def test_fallback_full_block_is_explicit_when_no_display_equation_exists() -> None:
    block = {
        "kind": "proposition",
        "file": "toy.tex",
        "line_start": 10,
        "line_end": 12,
        "label": "prop:no-equation",
        "block_id": "toy.tex:10:proposition:prop:no-equation",
        "section_path": ["Toy"],
        "text": "\\begin{proposition}\\label{prop:no-equation}Text only.\\end{proposition}",
    }

    targets = extract_derivation_targets_from_block(block)

    assert len(targets) == 1
    target = targets[0]
    assert target["id"] == "toy.tex:10:proposition:prop:no-equation:target:fallback_full_block"
    assert target["label"] == "prop:no-equation"
    assert target["parent_label"] == "prop:no-equation"
    assert target["line_start"] == 10
    assert target["line_end"] == 12
    assert target["extraction_status"] == "fallback_full_block"
    assert target["localization_status"] == "not_equation"
    assert target["uncertainty"] == ["no_display_equation_in_block"]


def test_extract_derivation_targets_contract_and_stable_ids() -> None:
    result = extract_derivation_targets(DOCS, ["prop:risky-pricing", "prop:interior-foc"])

    assert result["metadata"] == {
        "schema_version": "1.0",
        "contract": "derivation_target_extraction_result",
    }
    assert result["status"] == "extracted"
    assert result["target_count"] == 3
    assert result["fallback_count"] == 0
    assert [target["id"] for target in result["targets"]] == [
        "risky-debt-maliar-deep-learning-lecture-note.tex:395:proposition:prop:risky-pricing:target:eq:risky-pricing",
        "risky-debt-maliar-deep-learning-lecture-note.tex:770:proposition:prop:interior-foc:target:eq:foc-k",
        "risky-debt-maliar-deep-learning-lecture-note.tex:770:proposition:prop:interior-foc:target:eq:foc-b",
    ]
    assert "target_extraction_not_proof" in {item["code"] for item in result["non_claims"]}
