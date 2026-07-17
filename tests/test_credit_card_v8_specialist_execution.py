from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.audit_and_propose_fix import build_audit_fix_report
from mathdevmcp.derivation_target_extraction import extract_derivation_targets_for_label
from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.domain_templates import suggest_domain_templates
from mathdevmcp.latex_index import build_index
from mathdevmcp.proof_packet import build_proof_packet_label


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
DIGEST = hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def test_terminal_template_matches_exact_decorated_source_label() -> None:
    result = suggest_domain_templates(
        label="eq:terminal-value-base",
        equation_text=r"\Delta TV_{i,H}=\frac{\rho_i\widehat{\Delta CF}_{i,H+1}}{r_{disc}+\lambda_i+q_i}",
    )

    assert result["status"] == "suggested"
    assert result["matches"][0]["id"] == "valuation_terminal_value_v1"


def test_terminal_and_accounting_specialists_execute_with_bounded_scope() -> None:
    index = build_index(SOURCE.parent)
    terminal = extract_derivation_targets_for_label(index, "eq:terminal-value-base", file=SOURCE.name)["targets"][0]
    accounting = extract_derivation_targets_for_label(index, "eq:pd-lgd-ead", file=SOURCE.name)["targets"][0]

    terminal_result = terminal["specialist_execution"]
    accounting_result = accounting["specialist_execution"]
    assert terminal_result["status"] == "algebraically_consistent"
    assert terminal_result["result"]["backend_attempt"]["residual"] == "0"
    assert accounting_result["status"] == "structurally_consistent"
    assert accounting_result["result"]["backend_attempt"]["native_result"] == "0"
    assert terminal_result["claim_eligibility"] == accounting_result["claim_eligibility"] == "ineligible"
    assert terminal_result["publication_enabled"] is accounting_result["publication_enabled"] is False


def test_unsupported_scientific_roles_return_typed_abstention() -> None:
    index = build_index(SOURCE.parent)
    for label in (
        "eq:ss-bellman",
        "eq:causal-cashflow-object",
        "eq:experiment-late",
        "eq:randomization-assumption",
    ):
        target = extract_derivation_targets_for_label(index, label, file=SOURCE.name)["targets"][0]
        execution = target["specialist_execution"]
        assert execution["status"] == "typed_abstention"
        assert execution["selected_tool"] is None
        assert execution["result"]["backend_attempt"] is None
        assert execution["result"]["reason"]


def test_specialist_result_propagates_to_proof_fix_and_tree() -> None:
    proof = build_proof_packet_label(
        str(SOURCE.parent),
        "eq:terminal-value-base",
        file=SOURCE.name,
        source_digest=DIGEST,
        summary_only=True,
    )
    fix = build_audit_fix_report(
        "Audit terminal specialist integration",
        root=str(SOURCE.parent),
        labels=["eq:terminal-value-base"],
        target_file=SOURCE.name,
        source_digest=DIGEST,
    )
    tree = audit_document_derivation_tree(
        SOURCE,
        focus_labels=["eq:terminal-value-base"],
        max_attempts=1,
    )

    expected = proof["source"]["specialist_execution"]
    assert expected["status"] == "algebraically_consistent"
    assert fix["audited_evidence"][0]["canonical_target"]["specialist_execution"] == expected
    packet = tree["targets"][0]["semantic_work_packet"]
    assert packet["specialist_execution"] == expected
    assert tree["targets"][0]["tree"]["specialist_execution"] == expected
    assert tree["targets"][0]["tree"]["specialist_backend_evidence"][0]["claim_eligibility"] == "ineligible"
