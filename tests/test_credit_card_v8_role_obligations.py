from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.assumptions_for import audit_and_propose_assumptions
from mathdevmcp.document_derivation_tree import (
    _section_map,
    _semantic_packet_from_label_scoped_target,
    extract_document_derivation_obligations,
)
from mathdevmcp.latex_index import build_index, extract_paragraph_context_for_label


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"


def _packets(labels: list[str]) -> dict[str, dict]:
    extraction = extract_document_derivation_obligations(SOURCE, focus_labels=labels)
    index = build_index(SOURCE.parent)
    sections = _section_map(SOURCE.read_text(encoding="utf-8"))
    return {
        target["label"]: _semantic_packet_from_label_scoped_target(
            target,
            tex_path=SOURCE,
            sections=sections,
            paragraph_context=extract_paragraph_context_for_label(
                index, target["label"], before=1, after=1, file=SOURCE.name
            ),
        )
        for target in extraction["targets"]
    }


def test_accounting_obligations_are_local_and_downstream_is_separate() -> None:
    packets = _packets(["eq:pd-lgd-ead", "eq:balance-stock-flow"])
    for packet in packets.values():
        local = {item["id"] for item in packet["local_obligations"]}
        downstream = {item["id"] for item in packet["downstream_integration_obligations"]}
        assert local == {"component_definitions", "sign_units_timing_aligned", "local_component_exhaustiveness"}
        assert "discount_horizon_terminal_value_defined" not in local
        assert downstream == {"downstream_counterfactual_mapping", "downstream_discount_terminal_policy"}


def test_specialist_roles_receive_scoped_obligations_without_false_shape_blocker() -> None:
    packets = _packets(
        [
            "eq:terminal-value-base",
            "eq:ss-bellman",
            "eq:causal-cashflow-object",
            "eq:experiment-late",
            "eq:randomization-assumption",
        ]
    )
    ids = {label: {item["id"] for item in packet["local_obligations"]} for label, packet in packets.items()}

    assert "terminal_denominator_nonzero" in ids["eq:terminal-value-base"]
    assert {"bellman_transition_kernel", "bellman_policy_measurability"}.issubset(ids["eq:ss-bellman"])
    assert "causal_identification_separate" in ids["eq:causal-cashflow-object"]
    assert {"late_nonzero_first_stage", "late_monotonicity", "late_complier_interpretation"}.issubset(ids["eq:experiment-late"])
    assert {"assignment_mechanism_recorded", "interference_and_override_diagnostics"}.issubset(ids["eq:randomization-assumption"])
    constraints = packets["eq:ss-bellman"]["typed_repair_obligation"].get("constraints", [])
    assert not any(item.get("kind") == "conformable_product_required" for item in constraints)


def test_assumption_audit_reuses_source_role_local_obligations() -> None:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    result = audit_and_propose_assumptions(
        "Audit source-role-local assumptions",
        root=str(SOURCE.parent),
        labels=["eq:incremental-cash-flow", "eq:ss-bellman", "eq:randomization-assumption"],
        file=SOURCE.name,
        source_digest=digest,
    )

    by_label = {item["source"]["label"]: item for item in result["target_results"]}
    assert set(by_label) == {"eq:incremental-cash-flow", "eq:ss-bellman", "eq:randomization-assumption"}
    assert all(item["source"]["assumption_route"] == "source_role_specific" for item in by_label.values())
    assert {item["source"]["role_obligations"]["role"] for item in by_label.values()} == {
        "accounting_identity",
        "policy_value_recursion",
        "identification_assumption",
    }
    assert not any(
        gap["id"].endswith("unknown_route")
        for item in by_label.values()
        for gap in item["gaps"]
    )
    assert {
        obligation["id"]
        for obligation in by_label["eq:incremental-cash-flow"]["proposals"][0]["local_obligations"]
    } == {"component_definitions", "sign_units_timing_aligned", "local_component_exhaustiveness"}
