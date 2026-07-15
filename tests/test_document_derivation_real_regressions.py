from pathlib import Path
import hashlib

from mathdevmcp.document_derivation_tree import (
    audit_document_derivation_tree,
    extract_document_derivation_obligations,
)


ROOT = Path(__file__).resolve().parent.parent
CARD_SOURCE_SHA256 = "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8"
RISKY_SOURCE_SHA256 = "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1"


def test_frozen_real_document_source_digests_are_explicit() -> None:
    card = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"
    risky = ROOT / "docs/risky-debt-maliar-deep-learning-lecture-note.tex"

    assert hashlib.sha256(card.read_bytes()).hexdigest() == CARD_SOURCE_SHA256
    assert hashlib.sha256(risky.read_bytes()).hexdigest() == RISKY_SOURCE_SHA256


def test_credit_card_labels_reconstruct_as_separate_exact_obligations_without_backend() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"

    result = extract_document_derivation_obligations(
        source,
        focus_labels=["eq:incremental-cash-flow", "eq:incremental-npv"],
    )

    assert result["status"] == "extracted"
    assert result["backend_request_count"] == 0
    assert result["publication_enabled"] is False
    assert [item["label"] for item in result["obligations"]] == [
        "eq:incremental-cash-flow",
        "eq:incremental-npv",
    ]
    assert [item["obligation_digest"] for item in result["obligations"]] == [
        "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0",
        "d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac",
    ]
    assert result["obligations"][0]["operator_inventory"] == ["equality"]
    assert "summation" not in result["obligations"][0]["operator_inventory"]
    assert result["obligations"][1]["operator_inventory"] == [
        "equality",
        "conditional_expectation",
        "conditional_bar",
        "summation",
    ]
    assert result["obligations"][0]["excluded_spans"][0]["excluded_sibling_label"] == "eq:incremental-npv"
    assert {
        item["excluded_sibling_label"]
        for item in result["obligations"][1]["excluded_spans"]
    } == {"eq:incremental-cash-flow"}


def test_risky_debt_proposition_keeps_two_exact_foc_children_without_backend() -> None:
    source = ROOT / "docs/risky-debt-maliar-deep-learning-lecture-note.tex"

    result = extract_document_derivation_obligations(source, focus_labels=["prop:interior-foc"])

    assert result["status"] == "extracted"
    assert result["backend_request_count"] == 0
    assert result["publication_enabled"] is False
    assert [item["label"] for item in result["obligations"]] == ["eq:foc-k", "eq:foc-b"]
    assert [item["obligation_digest"] for item in result["obligations"]] == [
        "d987e605da2d4e509d0d65289a56e9b7f5d121273543bdf74276b9fb4c23bba5",
        "8d04797cf7e394624890ab2e0b0688f22d86d9194de94af3aa1407fb1a45edca",
    ]
    assert [target["label"] for target in result["targets"]] == ["eq:foc-k", "eq:foc-b"]
    assert all(target["parent_label"] == "prop:interior-foc" for target in result["targets"])
    assert result["obligations"][0]["excluded_spans"][0]["excluded_sibling_label"] == "eq:foc-b"
    assert result["obligations"][1]["excluded_spans"][0]["excluded_sibling_label"] == "eq:foc-k"


def test_frozen_card_audit_uses_complete_cash_flow_obligation() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"

    result = audit_document_derivation_tree(
        source,
        focus_labels=["eq:incremental-cash-flow"],
        budget_profile="smoke",
        max_attempts=0,
    )

    assert result["target_extraction"]["failure_count"] == 0
    assert result["target_extraction"]["fallback_to_locator_row"] is False
    assert result["coverage"]["missing_focus_labels"] == []
    assert [target["label"] for target in result["targets"]] == ["eq:incremental-cash-flow"]
    target = result["targets"][0]
    packet = target["semantic_work_packet"]
    assert target["obligation_digest"] == packet["obligation_digest"] == (
        "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0"
    )
    assert packet["target_ingress"] == "validated_label_scoped_obligation"
    assert packet["target"] == packet["normalized_target"]["display_text"]
    assert packet["lhs"] == r"\Delta CF_{i,t+h}(a,\pi;s)"
    assert packet["rhs"].startswith(r"\Delta PPNR_{i,t+h}(a,\pi;s)")
    assert r"\Delta Tax_{i,t+h}(a,\pi;s)" in packet["rhs"]
    assert packet["operator_inventory"] == ["equality"]
    assert packet["display_labels"] == ["eq:incremental-cash-flow"]
    assert {
        span["excluded_sibling_label"] for span in packet["excluded_spans"]
    } == {"eq:incremental-npv"}
    assert not any(
        blocker.get("kind") == "grouped_multiline_obligation_required"
        for blocker in target["tree"]["blockers"]
    )


def test_audit_reconstructs_relation_head_when_label_is_on_continuation(tmp_path: Path) -> None:
    source = tmp_path / "continued.tex"
    source.write_text(
        r"""
\begin{align}
\Delta CF
&= \Delta PPNR - \Delta EL
\nonumber\\
&\quad - \Delta Tax + \Delta RelValue
\label{eq:continued-cash-flow}
\end{align}
""",
        encoding="utf-8",
    )

    result = audit_document_derivation_tree(
        source,
        focus_labels=["eq:continued-cash-flow"],
        budget_profile="smoke",
        max_attempts=0,
    )

    packet = result["targets"][0]["semantic_work_packet"]
    assert result["target_extraction"]["failure_count"] == 0
    assert packet["target"] == (
        r"\Delta CF = \Delta PPNR - \Delta EL - \Delta Tax + \Delta RelValue"
    )
    assert packet["lhs"] == r"\Delta CF"
    assert packet["rhs"] == r"\Delta PPNR - \Delta EL - \Delta Tax + \Delta RelValue"
    assert packet["display_row_count"] == 2
    assert packet["label_scoped_obligation"]["continuation_spans"]


def test_audit_never_falls_back_to_orphaned_continuation_row(tmp_path: Path) -> None:
    source = tmp_path / "orphan.tex"
    source.write_text(
        r"""
\begin{align}
&\quad + r \label{eq:orphan}
\end{align}
""",
        encoding="utf-8",
    )

    result = audit_document_derivation_tree(
        source,
        focus_labels=["eq:orphan"],
        budget_profile="smoke",
        max_attempts=0,
    )

    assert result["targets"] == []
    assert result["target_extraction"]["failure_count"] == 1
    assert result["target_extraction"]["fallback_to_locator_row"] is False
    assert result["target_extraction"]["failures"][0]["status"] == "quarantined"
    assert result["coverage"]["missing_focus_labels"] == ["eq:orphan"]
