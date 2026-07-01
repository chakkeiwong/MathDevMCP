from mathdevmcp.high_level_contracts import (
    HIGH_LEVEL_CONTRACT,
    action,
    assumption_record,
    default_non_claims,
    evidence_entry,
    high_level_result,
    non_claim,
    validate_high_level_result,
    veto_reason,
)


def _proved_result() -> dict:
    return high_level_result(
        status="proved",
        workflow="derive_from",
        question="Can I derive a + b = b + a?",
        claim_class="derivation",
        answer="The scoped target is certified by a backend.",
        evidence=[
            evidence_entry(
                id="ev-backend-proof",
                evidence_class="backend_certificate",
                source="backend",
                summary="SymPy simplified lhs-rhs to zero.",
            )
        ],
        certification_source="backend",
    )


def test_high_level_result_builds_stable_contract_envelope() -> None:
    result = _proved_result()

    assert result["metadata"] == {"schema_version": "1.0", "contract": HIGH_LEVEL_CONTRACT}
    assert result["status"] == "proved"
    assert result["workflow"] == "derive_from"
    assert result["claim_class"] == "derivation"
    assert result["evidence_classes"] == ["backend_certificate"]
    assert validate_high_level_result(result) == []


def test_evidence_classes_must_match_raw_evidence_even_when_empty() -> None:
    result = high_level_result(
        status="inconclusive",
        workflow="prove_or_counterexample",
        question="Can we prove P?",
        claim_class="proof",
        answer="No bounded evidence was available.",
        evidence=[],
        certification_source="none",
        veto_reasons=[veto_reason("no_backend_route", "No route was available.")],
    )

    assert result["evidence_classes"] == []
    assert validate_high_level_result(result) == []

    result["evidence_classes"] = ["backend_certificate"]
    assert validate_high_level_result(result) == ["evidence_classes must equal sorted deduplicated evidence classes"]


def test_proved_requires_backend_certificate_from_backend_source() -> None:
    result = _proved_result()
    result["evidence"][0]["source"] = "sympy"

    assert validate_high_level_result(result) == [
        "certification_source backend requires backend_certificate evidence from backend"
    ]


def test_proved_rejects_numeric_or_structural_only_certification() -> None:
    result = high_level_result(
        status="proved",
        workflow="derive_from",
        question="Can I derive X?",
        claim_class="derivation",
        answer="Incorrectly promoted diagnostic evidence.",
        evidence=[
            evidence_entry(
                id="ev-numeric",
                evidence_class="numeric_diagnostic",
                source="diagnostic",
                summary="Probe points agreed.",
            )
        ],
        certification_source="backend",
    )

    assert validate_high_level_result(result) == [
        "certification_source backend requires backend_certificate evidence from backend",
        "proved requires backend_certificate evidence",
    ]


def test_refuted_requires_backend_counterexample_and_counterexample_object() -> None:
    result = high_level_result(
        status="refuted",
        workflow="prove_or_counterexample",
        question="Can we prove 1 + 1 = 3?",
        claim_class="proof",
        answer="The scoped claim is refuted.",
        evidence=[
            evidence_entry(
                id="ev-counterexample",
                evidence_class="backend_counterexample",
                source="backend",
                summary="Concrete evaluation gives 2 != 3.",
            )
        ],
        certification_source="backend",
    )

    assert validate_high_level_result(result) == [
        "backend_counterexample refutation requires counterexamples"
    ]

    result["counterexamples"] = [{"assignments": {}, "lhs_value": 2, "rhs_value": 3}]
    assert validate_high_level_result(result) == []


def test_refuted_scoped_contradiction_does_not_require_counterexample_object() -> None:
    result = high_level_result(
        status="refuted",
        workflow="debug_derivation",
        question="Where does the derivation fail?",
        claim_class="derivation_debugging",
        answer="A scoped contradiction was found at step 2.",
        evidence=[
            evidence_entry(
                id="ev-contradiction",
                evidence_class="scoped_contradiction",
                source="scoped_contradiction",
                summary="Step 2 contradicts the previous equation.",
            )
        ],
        certification_source="scoped_contradiction",
    )

    assert validate_high_level_result(result) == []


def test_backend_unavailable_is_not_refutation() -> None:
    result = high_level_result(
        status="backend_unavailable",
        workflow="prove_or_counterexample",
        question="Can Lean prove theorem T?",
        claim_class="proof",
        answer="The backend is unavailable.",
        evidence=[
            evidence_entry(
                id="ev-backend-unavailable",
                evidence_class="backend_unavailable",
                source="lean",
                summary="Lean executable is not configured.",
            )
        ],
        certification_source="none",
        veto_reasons=[veto_reason("backend_unavailable", "Lean was not configured.")],
    )

    assert validate_high_level_result(result) == []

    result["status"] = "refuted"
    result["certification_source"] = "backend"
    assert "refuted requires backend_counterexample or scoped_contradiction evidence" in validate_high_level_result(result)


def test_missing_assumptions_requires_assumption_records_and_nonclaim() -> None:
    result = high_level_result(
        status="missing_assumptions",
        workflow="assumptions_for",
        question="What assumptions are needed for logdet(A)?",
        claim_class="assumption_discovery",
        answer="A route-required assumption is missing.",
        evidence=[
            evidence_entry(
                id="ev-missing-assumption",
                evidence_class="missing_assumption",
                source="route",
                summary="logdet requires positive definiteness in this route.",
            )
        ],
        certification_source="none",
        assumptions=[
            assumption_record(
                text="A is symmetric positive definite.",
                status="missing",
                source="logdet route",
                necessity="required_by_route",
            )
        ],
    )

    assert validate_high_level_result(result) == []

    result["assumptions"] = []
    assert validate_high_level_result(result) == ["missing_assumptions requires assumptions"]


def test_structural_and_diagnostic_statuses_preserve_nonclaim_boundaries() -> None:
    structural = high_level_result(
        status="structural_match",
        workflow="audit_math_to_code",
        question="Does code implement logdet(S)?",
        claim_class="math_to_code",
        answer="The expression structurally matches.",
        evidence=[
            evidence_entry(
                id="ev-structural",
                evidence_class="structural_match",
                source="ast_matcher",
                summary="Required term logdet is present.",
            )
        ],
        certification_source="none",
    )
    diagnostic = high_level_result(
        status="diagnostic_only",
        workflow="prepare_review_packet",
        question="Prepare a review packet.",
        claim_class="review_packet",
        answer="A diagnostic review packet was prepared.",
        evidence=[
            evidence_entry(
                id="ev-review",
                evidence_class="review_packet",
                source="packet_builder",
                summary="Packet aggregates available evidence.",
            )
        ],
        certification_source="none",
    )

    assert validate_high_level_result(structural) == []
    assert validate_high_level_result(diagnostic) == []

    structural["non_claims"] = default_non_claims()
    assert validate_high_level_result(structural) == [
        "non_claims missing required status code: structural_evidence_not_proof"
    ]


def test_certifying_evidence_inside_abstention_requires_veto() -> None:
    result = high_level_result(
        status="inconclusive",
        workflow="prove_or_counterexample",
        question="Can we prove P?",
        claim_class="proof",
        answer="Evidence was not promoted because of a scope conflict.",
        evidence=[
            evidence_entry(
                id="ev-proof",
                evidence_class="backend_certificate",
                source="backend",
                summary="Backend certificate applies to a different scope.",
            )
        ],
        certification_source="none",
        veto_reasons=[veto_reason("scope_mismatch", "The certificate applies to another claim.")],
    )

    assert validate_high_level_result(result) == [
        "certifying or blocking evidence in non-certifying status requires certifying_evidence_not_promoted veto"
    ]

    result["veto_reasons"].append(veto_reason("certifying_evidence_not_promoted", "Scope mismatch prevents promotion."))
    assert validate_high_level_result(result) == []


def test_validator_rejects_freeform_claim_class_unknown_top_level_and_duplicate_evidence_ids() -> None:
    result = _proved_result()
    result["claim_class"] = "general_theorem"
    result["unexpected"] = True
    result["evidence"].append(
        evidence_entry(
            id="ev-backend-proof",
            evidence_class="backend_certificate",
            source="backend",
            summary="Duplicate id.",
        )
    )
    result["evidence_classes"] = ["backend_certificate"]

    assert validate_high_level_result(result) == [
        "unknown top-level fields: unexpected",
        "claim_class is unsupported",
        "claim_class does not match workflow",
        "evidence[1].id is duplicated",
    ]


def test_nested_extension_metadata_is_allowed_when_required_fields_are_valid() -> None:
    result = high_level_result(
        status="not_encodable",
        workflow="prove_or_counterexample",
        question="Can this informal theorem be checked?",
        claim_class="proof",
        answer="The claim is not encodable by the current route.",
        evidence=[
            evidence_entry(
                id="ev-not-encodable",
                evidence_class="not_encodable",
                source="router",
                summary="The route requires formal source.",
                extra={"raw_backend_payload": {"detail": "kept as nested extension metadata"}},
            )
        ],
        certification_source="none",
        veto_reasons=[veto_reason("not_encodable", "No formal source was provided.")],
        actions=[action("formalize_claim", "Provide a formal statement.")],
    )

    assert validate_high_level_result(result) == []


def test_non_claim_entries_require_code_and_text() -> None:
    result = _proved_result()
    result["non_claims"] = [non_claim("general_theorem_proving_not_claimed", "No broad theorem-proving claim.")]

    assert validate_high_level_result(result) == [
        "non_claims missing required global codes: release_readiness_not_claimed"
    ]
