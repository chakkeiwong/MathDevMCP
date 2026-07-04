from mathdevmcp.assumptions_for import assumptions_for
from mathdevmcp.audit_math_to_code import audit_math_to_code
from mathdevmcp.debug_derivation import debug_derivation
from mathdevmcp.derive_from import derive_from
from mathdevmcp.high_level_contracts import TOP_LEVEL_FIELDS, action, default_non_claims, evidence_entry, high_level_result, validate_high_level_result, veto_reason
from mathdevmcp.notation_reconciliation import reconcile_notation
from mathdevmcp.prepare_review_packet import prepare_review_packet, review_packet_agent_handoff, score_review_packet
from mathdevmcp.prove_or_counterexample import prove_or_counterexample


def _backend_unavailable_evidence() -> dict:
    result = high_level_result(
        status="backend_unavailable",
        workflow="prove_or_counterexample",
        question="Can we prove with a missing backend?",
        claim_class="proof",
        answer="The requested symbolic backend is unavailable in this local fixture.",
        evidence=[
            evidence_entry(
                id="phase3:backend-unavailable",
                evidence_class="backend_unavailable",
                source="phase3_fixture",
                summary="The requested symbolic backend is unavailable in this local fixture.",
                extra={"backend": "missing_fixture_backend"},
            )
        ],
        certification_source="none",
        veto_reasons=[veto_reason("backend_unavailable", "The requested symbolic backend is unavailable.")],
        actions=[action("configure_backend", "Configure or choose an available backend before retrying.")],
        non_claims=default_non_claims(extra_codes={"backend_unavailable_not_refutation"}),
    )
    assert validate_high_level_result(result) == []
    return result


def test_prepare_review_packet_preserves_proof_as_nested_evidence_not_certificate() -> None:
    nested = derive_from("a + b = b + a")
    result = prepare_review_packet("Review derivation", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert result["certification_source"] == "none"
    assert result["evidence_classes"] == ["review_packet"]
    assert low_level["backend_checks"]
    assert "not recertified" in low_level["backend_checks"][0]["boundary"]
    assert score_review_packet(result)["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_refutation_blocker() -> None:
    nested = prove_or_counterexample("A*B = B*A")
    result = prepare_review_packet("Review failed proof", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert low_level["status"] == "blocked_by_refutation"
    assert low_level["evidence"][0]["counterexamples"]
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_missing_assumptions() -> None:
    nested = assumptions_for("logdet(A)")
    result = prepare_review_packet("Review assumptions", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert low_level["status"] == "needs_human_review"
    assert low_level["assumptions"]
    assert any(gap["kind"] == "missing_assumptions" for gap in low_level["residual_gaps"])
    assert result["actions"]
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_preserves_structural_boundary() -> None:
    nested = audit_math_to_code("logdet(S)", "def f(S):\n    return logdet(S)\n")
    result = prepare_review_packet("Review code audit", evidence=[nested])
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert "diagnostic_evidence_not_proof" in {item["code"] for item in result["non_claims"]}
    assert low_level["trace_maps"]
    assert "not semantic proof" in low_level["trace_maps"][0]["boundary"]
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_compiles_route_trace_risks_and_non_claims() -> None:
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    code_audit = audit_math_to_code(
        "logdet(Sigma) + trace(Cov)",
        "def f(S):\n    return logdet(S) + trace(S)\n",
        aliases={"Sigma": "S", "Cov": "S"},
    )
    result = prepare_review_packet(
        "Review derivation and implementation context",
        evidence=[derived, code_audit],
        source={"context_summary": "Local review fixture with one derivation and one structural code audit."},
    )
    low_level = result["evidence"][0]["low_level"]
    risk_codes = {item["code"] for item in low_level["risk_register"]}
    non_claim_codes = {item["code"] for item in low_level["non_claims"]}

    assert low_level["route_plans"]
    assert low_level["route_plans"][0]["route_plan"]["givens"] == ["a,b are scalars"]
    assert low_level["trace_maps"][0]["trace_map"]["alias_collisions"] == [
        {"mapped_code_term": "S", "equation_terms": ["Cov", "Sigma"]}
    ]
    assert low_level["nested_evidence_summary"]
    assert low_level["decision_criteria"]
    assert low_level["agent_handoff"]["scoped_question"] == "Review derivation and implementation context"
    assert low_level["agent_handoff"]["source_context"] == "Local review fixture with one derivation and one structural code audit."
    assert low_level["agent_handoff"]["evidence_ledger"]
    assert low_level["agent_handoff"]["veto_risks"]
    assert low_level["agent_handoff"]["non_claim_boundary"]
    assert "diagnostic review handoff" in low_level["agent_handoff"]["next_artifact"]
    assert result["agent_handoff"] == low_level["agent_handoff"]
    assert {"route_plans_are_diagnostic", "trace_maps_are_structural"}.issubset(risk_codes)
    assert "givens_not_formal_assumptions" in non_claim_codes
    assert "diagnostic_route_and_trace_context_not_proof" in non_claim_codes
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_prepare_review_packet_additive_compatibility_contract_is_bounded() -> None:
    derived = derive_from("a + b = b + a", givens=["a,b are scalars"])
    result = prepare_review_packet(
        "Review additive compatibility",
        evidence=[derived],
        source={"context_summary": "Compatibility fixture."},
    )
    low_level = result["evidence"][0]["low_level"]
    compact = review_packet_agent_handoff(result)

    required_high_level_fields = {
        "metadata",
        "status",
        "workflow",
        "question",
        "claim_class",
        "answer",
        "evidence",
        "evidence_classes",
        "certification_source",
        "veto_reasons",
        "assumptions",
        "counterexamples",
        "actions",
        "non_claims",
        "evidence_ledger",
    }
    required_handoff_fields = {
        "scoped_question",
        "status",
        "reason",
        "evidence_ledger",
        "assumption_gap_ledger",
        "veto_risks",
        "non_claim_boundary",
        "next_actions",
        "next_artifact",
        "certification_boundary",
    }

    assert required_high_level_fields.issubset(result)
    assert "agent_handoff" in TOP_LEVEL_FIELDS
    assert result["agent_handoff"] == low_level["agent_handoff"]
    assert required_handoff_fields.issubset(compact)
    assert "not a proof certificate" in compact["certification_boundary"]
    assert validate_high_level_result(result) == []

    unknown_addition = dict(result)
    unknown_addition["external_closed_schema_probe"] = True
    assert validate_high_level_result(unknown_addition) == [
        "unknown top-level fields: external_closed_schema_probe"
    ]


def test_review_packet_rubric_fails_empty_packet_for_completeness() -> None:
    result = prepare_review_packet("Empty packet")
    rubric = score_review_packet(result)
    low_level = result["evidence"][0]["low_level"]

    assert result["status"] == "diagnostic_only"
    assert any(item["code"] == "empty_packet" for item in low_level["risk_register"])
    assert rubric["status"] == "failed"
    assert rubric["checks"]["has_nested_evidence"] is False


def test_prepare_review_packet_handoff_covers_realistic_case_matrix() -> None:
    cases = [
        {
            "name": "missing assumptions",
            "question": "Review missing assumptions",
            "evidence": [assumptions_for("logdet(A)")],
            "gap_kind": "missing_assumptions",
            "next_actions": {"human_review"},
        },
        {
            "name": "route gap",
            "question": "Review derivation gap",
            "evidence": [debug_derivation(["logdet(A)", "trace(A)", "trace(A)"])],
            "gap_kind": "gap_found",
            "next_actions": {"human_review"},
        },
        {
            "name": "not encodable",
            "question": "Review malformed proof claim",
            "evidence": [prove_or_counterexample("informal theorem with no equality")],
            "gap_kind": "not_encodable",
            "next_actions": {"formalize_claim"},
        },
        {
            "name": "backend unavailable",
            "question": "Review backend unavailable",
            "evidence": [_backend_unavailable_evidence()],
            "gap_kind": "backend_unavailable",
            "next_actions": {"configure_backend"},
        },
        {
            "name": "math code mismatch",
            "question": "Review code mismatch",
            "evidence": [audit_math_to_code("logdet(S)", "def f(S):\n    return trace(S)\n")],
            "gap_kind": "structural_mismatch",
            "next_actions": {"human_review"},
        },
        {
            "name": "notation conflict",
            "question": "Review notation conflict",
            "evidence": [
                reconcile_notation(
                    [{"symbol": "r", "alias_of": "r", "sign": "+"}],
                    [{"symbol": "r", "alias_of": "r", "sign": "-"}],
                )
            ],
            "gap_kind": None,
            "next_actions": {"human_review", "inspect_packet"},
        },
        {
            "name": "deterministic refutation",
            "question": "Review refutation",
            "evidence": [prove_or_counterexample("A*B = B*A")],
            "gap_kind": None,
            "next_actions": {"human_review", "inspect_packet"},
        },
        {
            "name": "deterministic verification",
            "question": "Review verified derivation",
            "evidence": [derive_from("a + b = b + a", givens=["a,b are scalars"])],
            "gap_kind": None,
            "next_actions": {"human_review", "inspect_packet"},
        },
    ]

    observed: dict[str, dict[str, str | bool]] = {}
    for case in cases:
        result = prepare_review_packet(case["question"], evidence=case["evidence"])
        handoff = result["agent_handoff"]
        gap_kinds = {item.get("kind") for item in handoff["assumption_gap_ledger"]}
        non_claim_codes = {item.get("code") for item in handoff["non_claim_boundary"]}
        action_kinds = {item.get("kind") for item in handoff["next_actions"]}

        assert result["status"] == "diagnostic_only"
        assert result["certification_source"] == "none"
        assert handoff["scoped_question"] == case["question"]
        assert handoff["evidence_ledger"]
        assert handoff["non_claim_boundary"]
        assert "review_packet_not_proof_certificate" in non_claim_codes
        assert "not a proof certificate" in handoff["certification_boundary"]
        assert action_kinds & case["next_actions"]
        if case["gap_kind"] is not None:
            assert case["gap_kind"] in gap_kinds
        observed[str(case["name"])] = {
            "low_level_status": result["evidence"][0]["low_level"]["status"],
            "has_gap": bool(handoff["assumption_gap_ledger"]),
            "has_veto_risk": bool(handoff["veto_risks"]),
            "has_next_action": bool(handoff["next_actions"]),
        }

    assert observed["missing assumptions"]["has_gap"] is True
    assert observed["route gap"]["has_gap"] is True
    assert observed["not encodable"]["has_gap"] is True
    assert observed["backend unavailable"]["has_gap"] is True
    assert observed["math code mismatch"]["has_gap"] is True
    assert observed["notation conflict"]["low_level_status"] == "needs_human_review"
    assert observed["deterministic refutation"]["low_level_status"] == "blocked_by_refutation"
    assert observed["deterministic verification"]["low_level_status"] == "review_ready"
