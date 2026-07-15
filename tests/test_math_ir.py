from pathlib import Path

import pytest

from mathdevmcp.evidence_manifest import EvidenceValidationError
from mathdevmcp.math_ir import (
    build_typed_assumption,
    diagnose_typed_obligation,
    obligation_from_audit_obligation,
    resolve_symbol_roles,
    typed_repair_obligation_from_packet,
    validate_typed_assumption,
    validate_math_obligation,
)
from mathdevmcp.matrix_ir import matrix_ir_from_equation_row, parse_matrix_obligation
from mathdevmcp.proof_audit import audit_derivation_for_label
from mathdevmcp.typed_workflows import typed_obligation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def _scope(*, file: str = "doc.tex", label: str = "eq:target") -> dict:
    return {
        "entry_source_digest": "a" * 64,
        "file": file,
        "label": label,
        "obligation_digest": "b" * 64,
    }


def _source_ref(*, file: str = "doc.tex") -> dict:
    return {
        "file": file,
        "source_digest": "c" * 64,
        "byte_span": {"start": 10, "end": 20},
        "line_span": {"start": 2, "end": 3},
        "enclosing_node_id": "ctx_" + "d" * 64,
        "dependency_path": ["ctx_" + "e" * 64, "edge_" + "f" * 64],
        "applicability_reason": "The declaration explicitly names the target.",
    }


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


def test_pi_is_not_unconditionally_posterior() -> None:
    typed = diagnose_typed_obligation(
        {"id": "pi", "lhs": r"\pi(x)", "rhs": "y", "source_text": r"\pi(x)=y"}
    )["obligation"]

    assert "posterior" not in typed["unresolved_constructs"]
    assert all(item["role"] != "posterior_candidate" for item in typed["typed_symbols"])


def test_card_pi_resolves_policy_or_remains_not_searched() -> None:
    evidence = {
        "symbol": r"\pi",
        "proposed_role": "policy_candidate",
        "scope": _scope(),
        "evidence_kind": "exact_declaration",
        "source_refs": [_source_ref()],
        "applicability_reason": "The source explicitly defines pi as the downstream policy.",
    }
    resolved = resolve_symbol_roles(
        [r"\pi"], scope=_scope(), evidence_records=[evidence], search_state="source_supported"
    )
    withheld = resolve_symbol_roles(
        [r"\pi"], scope=_scope(), evidence_records=[], search_state="not_searched"
    )

    assert resolved["resolutions"][0]["state"] == "resolved"
    assert resolved["resolutions"][0]["role"] == "policy_candidate"
    assert withheld["resolutions"][0]["state"] == "not_searched"


def test_explicit_override_has_provenance_and_scope() -> None:
    override = {
        "symbol": "x",
        "proposed_role": "scalar_candidate",
        "scope": _scope(),
        "source_refs": [_source_ref()],
        "applicability_reason": "Human-provided scoped convention.",
        "override_provenance": {
            "authority": "human_user",
            "artifact_ref": "docs/reviews/notation.json",
            "artifact_sha256": "1" * 64,
        },
    }
    result = resolve_symbol_roles(
        ["x"], scope=_scope(), evidence_records=[], overrides=[override], search_state="source_supported"
    )

    assert result["resolutions"][0]["state"] == "resolved"
    candidate = result["candidates"][0]
    assert candidate["priority_class"] == "scoped_override"
    assert candidate["override_provenance"] == override["override_provenance"]


def test_override_cannot_leak_to_another_file_or_label() -> None:
    override = {
        "symbol": "x",
        "proposed_role": "scalar_candidate",
        "scope": _scope(file="other.tex", label="eq:other"),
        "source_refs": [_source_ref(file="other.tex")],
        "applicability_reason": "Scoped elsewhere.",
        "override_provenance": {
            "authority": "human_user",
            "artifact_ref": "docs/reviews/notation.json",
            "artifact_sha256": "1" * 64,
        },
    }
    result = resolve_symbol_roles(
        ["x"], scope=_scope(), evidence_records=[], overrides=[override], search_state="source_supported"
    )

    assert result["resolutions"][0]["state"] == "unknown"
    assert result["candidates"] == []
    assert result["diagnostics"][0]["kind"] == "override_scope_mismatch"


def test_conflicting_roles_remain_ambiguous() -> None:
    records = [
        {
            "symbol": "x",
            "proposed_role": role,
            "scope": _scope(),
            "evidence_kind": "exact_declaration",
            "source_refs": [_source_ref()],
            "applicability_reason": "Exact but conflicting declaration.",
        }
        for role in ("scalar_candidate", "vector_candidate")
    ]
    result = resolve_symbol_roles(
        ["x"], scope=_scope(), evidence_records=records, search_state="source_supported"
    )

    assert result["resolutions"][0]["state"] == "ambiguous"
    assert result["resolutions"][0]["role"] is None


def test_lexical_role_is_candidate_not_fact() -> None:
    result = resolve_symbol_roles(
        ["posterior"],
        scope=_scope(),
        evidence_records=[
            {
                "symbol": "posterior",
                "proposed_role": "posterior_candidate",
                "scope": _scope(),
                "evidence_kind": "lexical_heuristic",
                "source_refs": [],
                "applicability_reason": "Spelling-only heuristic.",
            }
        ],
        search_state="source_supported",
    )

    assert result["resolutions"][0]["state"] == "candidate"
    assert result["resolutions"][0]["role"] is None


def test_candidate_assumption_does_not_become_stated() -> None:
    assumption = build_typed_assumption(
        predicate="f is differentiable",
        formal_predicate=None,
        kind="regularity",
        subjects=["f"],
        support_state="candidate_assumption",
        source_refs=[],
        encoding_state="not_yet_encoded",
        closes_blocker_ids=["blocker_f"],
    )

    assert assumption["support_state"] == "candidate_assumption"
    assert assumption["source_refs"] == []


def test_source_supported_requires_exact_ref_and_rejects_none_line() -> None:
    with pytest.raises(EvidenceValidationError):
        build_typed_assumption(
            predicate="f is differentiable",
            formal_predicate=None,
            kind="regularity",
            subjects=["f"],
            support_state="source_supported",
            source_refs=[{"file": "doc.tex", "line_span": {"start": None, "end": 2}}],
            encoding_state="not_yet_encoded",
            closes_blocker_ids=[],
        )


def test_not_found_requires_completed_search_for_typed_assumption() -> None:
    with pytest.raises(EvidenceValidationError):
        build_typed_assumption(
            predicate="f is differentiable",
            formal_predicate=None,
            kind="regularity",
            subjects=["f"],
            support_state="not_found_after_search",
            source_refs=[],
            encoding_state="not_applicable",
            closes_blocker_ids=[],
            search_completed=False,
        )


def test_assumption_identity_is_stable_but_binding_tracks_support_and_encoding() -> None:
    common = {
        "predicate": "f is differentiable",
        "formal_predicate": None,
        "kind": "regularity",
        "subjects": ["f"],
        "closes_blocker_ids": ["blocker_f"],
    }
    candidate = build_typed_assumption(
        **common,
        support_state="candidate_assumption",
        source_refs=[],
        encoding_state="not_yet_encoded",
    )
    supported = build_typed_assumption(
        **common,
        support_state="source_supported",
        source_refs=[_source_ref()],
        encoding_state="not_applicable",
    )

    assert candidate["assumption_id"] == supported["assumption_id"]
    assert candidate["binding_digest"] != supported["binding_digest"]
    assert validate_typed_assumption(supported) == supported


def test_source_support_does_not_imply_encoded_or_mathematically_sufficient() -> None:
    assumption = build_typed_assumption(
        predicate="f is differentiable",
        formal_predicate=None,
        kind="regularity",
        subjects=["f"],
        support_state="source_supported",
        source_refs=[_source_ref()],
        encoding_state="not_yet_encoded",
        closes_blocker_ids=["blocker_f"],
    )

    assert assumption["encoding_state"] == "not_yet_encoded"
    assert assumption["mathematical_sufficiency"] == "not_established"


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
