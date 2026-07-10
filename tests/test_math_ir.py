from pathlib import Path

from mathdevmcp.math_ir import (
    diagnose_typed_obligation,
    obligation_from_audit_obligation,
    typed_repair_obligation_from_packet,
    validate_math_obligation,
)
from mathdevmcp.matrix_ir import matrix_ir_from_equation_row, parse_matrix_obligation
from mathdevmcp.proof_audit import audit_derivation_for_label
from mathdevmcp.typed_workflows import typed_obligation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_math_obligation_ir_preserves_provenance_and_symbols():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")
    ir = obligation_from_audit_obligation(audit["obligations"][0])

    assert validate_math_obligation(ir) == []
    assert ir["kind"] == "equation"
    assert ir["backend_suitability"] == "symbolic"
    assert ir["provenance"]["label"] == "eq:proof-audit-single"
    assert {symbol["name"] for symbol in ir["symbols"]} == {"a", "b"}


def test_math_obligation_ir_marks_unresolved_domain_constructs():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-kalman", backend="sympy")
    ir = obligation_from_audit_obligation(audit["obligations"][0])

    assert "derivative" in ir["unresolved_constructs"]
    assert "matrix_inverse" in ir["unresolved_constructs"]
    assert ir["backend_suitability"] == "human_review"
    assert ir["diagnostic_status"] == "needs_assumptions"
    assert any(item["kind"] == "invertibility_required" for item in ir["dimension_constraints"])
    assert any(item["backend"] == "human_review" for item in ir["backend_route_hints"])


def test_math_obligation_ir_records_state_space_typed_candidates():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:dept-state-space-likelihood", backend="sympy")
    ir = obligation_from_audit_obligation(audit["obligations"][0])

    assert validate_math_obligation(ir) == []
    roles = {item["name"]: item["role"] for item in ir["typed_symbols"]}
    assert roles["InnovCov"] == "covariance_matrix_candidate"
    assert "matrix_inverse" in ir["unresolved_constructs"]
    assert "determinant" in ir["unresolved_constructs"]
    assert {item["kind"] for item in ir["dimension_constraints"]} >= {"invertibility_required", "square_matrix_required"}
    assert ir["diagnostic_status"] == "needs_assumptions"


def test_typed_diagnostic_uses_explicit_context_to_reduce_missing_constraints():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:dept-state-space-likelihood", backend="sympy")
    typed = diagnose_typed_obligation(
        audit["obligations"][0],
        context_text="The covariance matrices are square, symmetric, and positive semidefinite.",
    )

    assert typed["metadata"] == {"schema_version": "1.0", "contract": "typed_math_obligation_diagnostic"}
    assert typed["missing_constraints"] == []
    assert typed["status"] == "typed_review"


def test_typed_obligation_for_label_reports_hmc_posterior_review():
    result = typed_obligation_for_label(str(FIXTURES), "eq:dept-hmc-leapfrog")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "typed_obligation_label_diagnostic"}
    assert result["status"] == "unverified"
    obligation = result["typed_diagnostic"]["obligation"]
    assert "derivative" in obligation["unresolved_constructs"]
    assert any(item["kind"] == "differentiability_required" for item in obligation["dimension_constraints"])
    assert any(item["role"] == "posterior_candidate" for item in obligation["typed_symbols"])


def test_validate_math_obligation_rejects_malformed_payload():
    errors = validate_math_obligation({"metadata": {"contract": "wrong"}, "kind": "bad", "backend_suitability": "bad", "diagnostic_status": "bad"})

    assert "metadata.contract must be math_obligation" in errors
    assert "kind is invalid" in errors
    assert "backend_suitability is invalid" in errors
    assert "diagnostic_status is invalid" in errors


def test_typed_repair_obligation_from_packet_preserves_context_graph_blockers():
    packet = {
        "id": "semantic_packet_eq_foc_k_0",
        "label": "eq:foc-k",
        "target": r"0 = m(\bar e)d\bar e/dk' + \beta \E[V^\star_k(k',b',z')\mid z]",
        "lhs": "0",
        "rhs": r"m(\bar e)d\bar e/dk' + \beta \E[V^\star_k(k',b',z')\mid z]",
        "source_text": r"0 &= m(\bar e)d\bar e/dk' + \beta \E[V^\star_k(k',b',z')\mid z]",
        "operator_inventory": ["equality", "conditional_expectation", "derivative"],
        "source_span": {"file": "doc.tex", "line_start": 10, "line_end": 12, "label": "eq:foc-k"},
        "paragraph_context": {
            "paragraphs": [
                {
                    "line_start": 8,
                    "line_end": 9,
                    "text": "Suppose the action is interior and the relevant functions are differentiable.",
                }
            ]
        },
        "context_graph": {
            "nodes": [
                {
                    "id": "assumption_relevant_functions_differentiable",
                    "kind": "candidate_assumption",
                    "status": "nearby_stated",
                    "summary": "The relevant functions are differentiable.",
                    "mathematical_role": "supports local derivative notation",
                    "source_refs": [{"file": "doc.tex", "line_start": 8, "line_end": 9}],
                    "evidence_refs": ["doc:8"],
                },
                {
                    "id": "requirement_conditional_integrability",
                    "kind": "candidate_assumption",
                    "status": "unresolved",
                    "summary": "Random terms inside the conditional expectation are measurable and integrable.",
                    "mathematical_role": "finite expectation condition",
                    "why_status": "No integrability statement appears.",
                    "required_next_evidence": "State integrability.",
                    "source_refs": [{"file": "doc.tex", "line_start": 10, "line_end": 12}],
                    "evidence_refs": ["eq:foc-k"],
                },
            ]
        },
    }

    typed = typed_repair_obligation_from_packet(packet)

    assert typed["metadata"] == {"schema_version": "1.0", "contract": "typed_repair_obligation"}
    assert typed["target_label"] == "eq:foc-k"
    assert "expectation" in typed["unresolved_constructs"]
    assert "integrability" in typed["unresolved_constructs"]
    statuses = {item["id"]: item["status"] for item in typed["assumptions"]}
    assert statuses["assumption_relevant_functions_differentiable"] == "nearby_stated"
    assert statuses["requirement_conditional_integrability"] == "unresolved"
    assert typed["encodability"]["status"] == "blocked_pending_typed_assumptions"
    assert any(hint["backend"] == "manual_formalization" for hint in typed["route_hints"])
    assert "not proof" in typed["certification_boundary"]


def test_matrix_ir_preserves_noncommutative_ordered_products():
    result = parse_matrix_obligation(r"dS^{-1} = - S^{-1} dS S^{-1}")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "matrix_ir"}
    assert result["status"] == "parsed"
    assert result["rhs"]["kind"] == "MatMul"
    assert result["rhs"]["properties"]["noncommutative"] is True
    assert result["ordered_products"].count("S^{-1}") == 2
    assert any(child["kind"] == "Inv" for child in result["rhs"]["children"])


def test_matrix_ir_from_equation_row_carries_provenance():
    result = matrix_ir_from_equation_row(
        {
            "file": "chapter.tex",
            "line_start": 10,
            "line_end": 10,
            "label": "eq:test",
            "row_index": 0,
            "localization_status": "localized",
            "text": r"\log \det S = y",
        }
    )

    assert result["lhs"]["kind"] == "LogDet"
    assert result["lhs"]["provenance"]["label"] == "eq:test"
    assert "proof" not in result["certification_boundary"].lower() or "not proof" in result["certification_boundary"].lower()
