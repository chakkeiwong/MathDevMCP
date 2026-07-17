from pathlib import Path

from mathdevmcp.derivation_target_extraction import (
    build_proposition_context_packet,
    extract_derivation_targets,
    extract_derivation_targets_for_label,
    extract_derivation_targets_from_block,
)
from mathdevmcp.latex_index import build_index


ROOT = Path(__file__).resolve().parent.parent


def test_v8_nine_targets_share_typed_relation_and_source_role_contract() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
    index = build_index(source.parent)
    expected = {
        "eq:panel-npv-functional": ("equality", "policy_value_recursion"),
        "eq:incremental-cash-flow": ("equality", "accounting_identity"),
        "eq:pd-lgd-ead": ("equality", "accounting_identity"),
        "eq:balance-stock-flow": ("equality", "accounting_identity"),
        "eq:terminal-value-base": ("equality", "placeholder_definition"),
        "eq:ss-bellman": ("equality", "policy_value_recursion"),
        "eq:causal-cashflow-object": ("conditional_expectation_object", "causal_estimand_object"),
        "eq:experiment-late": ("equality", "statistical_estimator"),
        "eq:randomization-assumption": ("conditional_independence", "identification_assumption"),
    }

    for label, (kind, role) in expected.items():
        result = extract_derivation_targets_for_label(index, label, file=source.name)
        assert result["status"] == "extracted"
        assert len(result["targets"]) == 1
        target = result["targets"][0]
        assert target["normalized_target"]["kind"] == kind
        assert target["routing_role"]["role"] == role
        assert target["routing_role"]["authority"] == "source_evidenced_role"
        assert target["routing_role"]["obligation_digest"] == target["obligation_digest"]
        assert "does not establish" in target["routing_role"]["non_claims"][0]
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


def test_build_proposition_context_packet_for_interior_foc() -> None:
    index = build_index(DOCS)

    result = build_proposition_context_packet(index, "prop:interior-foc")

    assert result["metadata"]["contract"] == "proposition_context_packet_result"
    assert result["status"] == "context_packet_ready"
    packet = result["context_packet"]
    assert packet["label"] == "prop:interior-foc"
    assert packet["kind"] == "proposition"
    assert packet["file"] == "risky-debt-maliar-deep-learning-lecture-note.tex"
    assert packet["line_start"] == 770
    assert packet["line_end"] == 787
    assert "Interior first-order conditions" in packet["title"]
    assert [target["label"] for target in packet["equation_targets"]] == ["eq:foc-k", "eq:foc-b"]
    assert any("continuation state" in item for item in packet["hypotheses"])
    assert any("differentiable" in item for item in packet["hypotheses"])
    assert "This proposition context packet localizes source evidence" in packet["non_claim"]
    assert "context_packet_not_proof" in {item["code"] for item in result["non_claims"]}


def test_phase02_exact_file_label_returns_one_validated_obligation() -> None:
    index = build_index(DOCS)
    result = extract_derivation_targets_for_label(
        index,
        "eq:incremental-cash-flow",
        file="docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
    )

    assert result["status"] == "extracted"
    assert len(result["targets"]) == len(result["obligations"]) == 1
    target = result["targets"][0]
    assert target["obligation_digest"] == "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0"
    assert target["operator_inventory"] == ["equality"]
    assert target["excluded_spans"][0]["excluded_sibling_label"] == "eq:incremental-npv"


def test_phase02_prop_container_keeps_foc_children_as_distinct_obligations() -> None:
    result = extract_derivation_targets_for_label(build_index(DOCS), "prop:interior-foc")

    assert [item["label"] for item in result["obligations"]] == ["eq:foc-k", "eq:foc-b"]
    assert len({item["obligation_digest"] for item in result["obligations"]}) == 2
    assert [target["label"] for target in result["targets"]] == ["eq:foc-k", "eq:foc-b"]


def test_phase02_bare_duplicate_label_emits_no_target(tmp_path: Path) -> None:
    for name, rhs in (("a.tex", "1"), ("b.tex", "2")):
        (tmp_path / name).write_text(
            f"\\begin{{equation}}\nx = {rhs}\n\\label{{eq:duplicate}}\n\\end{{equation}}\n",
            encoding="utf-8",
        )
    result = extract_derivation_targets_for_label(build_index(tmp_path), "eq:duplicate")

    assert result["status"] == "ambiguous"
    assert result["targets"] == []
    assert result["ambiguities"][0]["code"] == "duplicate_label_across_files"
