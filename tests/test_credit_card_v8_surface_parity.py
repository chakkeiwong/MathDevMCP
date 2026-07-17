from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.document_derivation_tree import (
    _section_map,
    _semantic_packet_from_label_scoped_target,
    extract_document_derivation_obligations,
)
from mathdevmcp.latex_index import build_index, extract_paragraph_context_for_label
from mathdevmcp.math_document_rigor import plan_math_document_rigor_audit
from mathdevmcp.negative_evidence import build_negative_evidence_packet
from mathdevmcp.proof_packet import build_proof_packet_label


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
LABELS = [
    "eq:panel-npv-functional",
    "eq:incremental-cash-flow",
    "eq:pd-lgd-ead",
    "eq:balance-stock-flow",
    "eq:terminal-value-base",
    "eq:ss-bellman",
    "eq:causal-cashflow-object",
    "eq:experiment-late",
    "eq:randomization-assumption",
]


def test_v8_rigor_and_tree_extraction_share_nine_canonical_objects() -> None:
    rigor = plan_math_document_rigor_audit(SOURCE, focus_labels=LABELS, max_labels=9)
    tree = extract_document_derivation_obligations(SOURCE, focus_labels=LABELS)

    rigor_targets = {item["label"]: item for item in rigor["target_selection"]["targets"]}
    tree_targets = {item["label"]: item for item in tree["targets"]}
    index = build_index(SOURCE.parent)
    sections = _section_map(SOURCE.read_text(encoding="utf-8"))
    tree_packets = {
        label: _semantic_packet_from_label_scoped_target(
            tree_targets[label],
            tex_path=SOURCE,
            sections=sections,
            paragraph_context=extract_paragraph_context_for_label(
                index, label, before=1, after=1, file=SOURCE.name
            ),
        )
        for label in LABELS
    }

    assert list(rigor_targets) == LABELS
    assert set(tree_targets) == set(LABELS)
    assert tree["adapter_eligible_target_count"] == 9
    for label in LABELS:
        assert rigor_targets[label]["text"] == tree_targets[label]["target"]
        assert rigor_targets[label]["claim_type"] == tree_targets[label]["routing_role"]["role"]
        assert rigor_targets[label]["obligation_digest"] == tree_targets[label]["obligation_digest"]
        assert [item["id"] for item in rigor_targets[label]["local_obligations"]] == [
            item["id"] for item in tree_packets[label]["local_obligations"]
        ]
    assert "\\Delta PPNR" in rigor_targets["eq:incremental-cash-flow"]["text"]
    assert "\\Delta RelValue" in rigor_targets["eq:incremental-cash-flow"]["text"]
    assert rigor_targets["eq:causal-cashflow-object"]["normalized_target"]["kind"] == "conditional_expectation_object"
    assert rigor_targets["eq:randomization-assumption"]["normalized_target"]["kind"] == "conditional_independence"


def test_v8_proof_and_negative_packets_cannot_drift_from_canonical_source() -> None:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    for label in ("eq:incremental-cash-flow", "eq:causal-cashflow-object", "eq:randomization-assumption"):
        proof = build_proof_packet_label(
            str(SOURCE.parent),
            label,
            file=SOURCE.name,
            source_digest=digest,
            summary_only=True,
        )
        negative = build_negative_evidence_packet(label, proof["proof_audit_v2"])

        for key in ("target", "normalized_target", "routing_role", "obligation_digest", "source_digest"):
            assert proof["source"][key] == negative["source"][key]
        assert proof["source"]["target"] not in {r"\begin{equation}", r"\begin{align}"}
