from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.document_evidence_binding import validate_document_evidence_binding
from mathdevmcp.evidence_manifest import EvidenceValidationError


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


@pytest.fixture(scope="module")
def v8_audit() -> dict:
    return audit_document_derivation_tree(
        SOURCE,
        focus_labels=LABELS,
        max_attempts=1,
    )


@pytest.fixture(scope="module")
def terminal_result(v8_audit) -> tuple[dict, dict, list[dict], dict]:
    target = next(item for item in v8_audit["targets"] if item["label"] == "eq:terminal-value-base")
    packet = target["semantic_work_packet"]
    branches = target["tree"]["assumption_branches"]
    binding = target["tree"]["document_evidence_binding"]
    return v8_audit, packet, branches, binding


def test_all_nine_v8_targets_use_current_replayable_bindings(v8_audit) -> None:
    assert [item["label"] for item in v8_audit["targets"]] == LABELS
    assert v8_audit["evidence_schema_version"] == "1.0"
    assert v8_audit["integrity_binding_verified"] is True
    assert len(v8_audit["document_evidence_binding_refs"]) == 9
    assert v8_audit["promotion"]["errors"] == ["document_repair_publication_quarantined"]
    assert v8_audit["promotion"]["can_promote"] is False
    assert "evidence_binding_error" not in v8_audit["failure_classifications"]
    assert "exact Phase 01 binding" not in v8_audit["backend_provenance"]["certification_boundary"]
    for target in v8_audit["targets"]:
        tree = target["tree"]
        binding = tree["document_evidence_binding"]
        assert validate_document_evidence_binding(
            binding,
            packet=target["semantic_work_packet"],
            branches=tree["assumption_branches"],
            source_path=SOURCE,
        ) == binding
        assert target["evidence_schema_version"] == "1.0"
        assert target["promotion"]["errors"] == ["document_repair_publication_quarantined"]
        assert target["promotion"]["can_promote"] is False
        assert (
            target["tree"]["branch_ranking"]["selected_action"]["action_kind"]
            != "repair_evidence_integrity"
        )
        assert tree["integrity_binding_verified"] is True
        assert tree["publication_enabled"] is False
        assert "until exact binding exists" not in tree["branch_ranking"]["boundary"]
        serialized = str(tree)
        assert "no exact Phase 01 binding" not in serialized
        assert "exact document binding is absent" not in serialized


def test_v8_binding_reconstructs_and_propagates_without_enabling_claims(terminal_result) -> None:
    audit, packet, branches, binding = terminal_result

    assert validate_document_evidence_binding(
        binding,
        packet=packet,
        branches=branches,
        source_path=SOURCE,
    ) == binding
    target = next(item for item in audit["targets"] if item["label"] == "eq:terminal-value-base")
    tree = target["tree"]
    branch = tree["assumption_branches"][0]
    report = tree["document_gap_reports"][0]
    compiler = tree["tool_grounded_proposal_compiler"]
    compiled = compiler["compiled_items"][0]
    surfaces = [audit, target, tree, branch, branch["backend_evidence"], report, report["backend_evidence"], compiler, compiled]
    expected_ref = {
        "binding_id": binding["binding_id"],
        "binding_digest": binding["binding_digest"],
    }

    for surface in surfaces:
        assert surface["evidence_schema_version"] == "1.0"
        assert surface["integrity_binding_status"] == "verified_current_evidence"
        assert surface["integrity_binding_verified"] is True
        assert surface["claim_eligibility"] == "ineligible"
        assert surface["publication_enabled"] is False
    assert target["document_evidence_binding_ref"] == expected_ref
    assert branch["document_evidence_binding_ref"] == expected_ref
    assert report["document_evidence_binding_ref"] == expected_ref
    assert compiler["document_evidence_binding_ref"] == expected_ref
    assert binding["specialist"]["backend_environment"]["selected_tool_version"]
    assert binding["boundary"]["promotion_allowed"] is False
    assert audit["publication_mode"] == "disabled"
    assert audit["coverage"]["promoted_count"] == 0


@pytest.mark.parametrize(
    "mutation",
    [
        "source_digest",
        "obligation",
        "routing_role",
        "branch_id",
        "branch_assumptions",
        "specialist_result",
        "promotion_boundary",
    ],
)
def test_v8_binding_rejects_identity_and_boundary_mutations(mutation: str, terminal_result) -> None:
    _, packet, branches, binding = terminal_result
    changed_packet = deepcopy(packet)
    changed_branches = deepcopy(branches)
    changed_binding = deepcopy(binding)

    if mutation == "source_digest":
        changed_packet["source_span"]["source_digest"] = "0" * 64
    elif mutation == "obligation":
        changed_packet["obligation_digest"] = "0" * 64
    elif mutation == "routing_role":
        changed_packet["routing_role"]["role"] = "definition"
    elif mutation == "branch_id":
        changed_branches[0]["id"] += "_mutated"
    elif mutation == "branch_assumptions":
        changed_branches[0]["assumptions"].append("An unbound assumption.")
    elif mutation == "specialist_result":
        changed_packet["specialist_execution"]["result"]["backend_attempt"]["residual"] = "1"
    elif mutation == "promotion_boundary":
        changed_binding["boundary"]["promotion_allowed"] = True

    with pytest.raises(EvidenceValidationError):
        validate_document_evidence_binding(
            changed_binding,
            packet=changed_packet,
            branches=changed_branches,
            source_path=SOURCE,
        )


def test_v8_binding_rejects_cross_label_and_stale_disk_source(tmp_path: Path, terminal_result) -> None:
    _, packet, branches, binding = terminal_result
    audit = terminal_result[0]
    other = next(item for item in audit["targets"] if item["label"] == "eq:pd-lgd-ead")
    stale_source = tmp_path / SOURCE.name
    stale_source.write_bytes(SOURCE.read_bytes() + b"\n% stale mutation\n")

    with pytest.raises(EvidenceValidationError):
        validate_document_evidence_binding(
            binding,
            packet=other["semantic_work_packet"],
            branches=other["tree"]["assumption_branches"],
            source_path=SOURCE,
        )
    with pytest.raises(EvidenceValidationError, match="source digest is stale"):
        validate_document_evidence_binding(
            binding,
            packet=packet,
            branches=branches,
            source_path=stale_source,
        )
