from mathdevmcp.agent_hypothesis_expansion import (
    AGENT_HYPOTHESIS_EXPANSION_CONTRACT,
    AGENT_HYPOTHESIS_EXPANSION_SET_CONTRACT,
    propose_hypothesis_expansions,
    validate_agent_hypothesis_expansion,
)


def _blocker(kind: str = "conditional_law_translation_required") -> dict:
    return {
        "id": f"blocker_{kind}",
        "kind": kind,
        "problem": "The conditional law required by the expectation is not stated as an encodable object.",
        "why": "Conditional expectation notation is only meaningful after the transition kernel is fixed.",
        "required_next_evidence": "State or verify the conditional law.",
        "evidence_refs": ["typed_repair_obligation:test"],
    }


def test_conditional_law_blocker_generates_valid_candidate_expansions() -> None:
    result = propose_hypothesis_expansions(
        _blocker(),
        source_context={"id": "packet_1", "label": "eq:test", "location": "paper.tex > eq:test > line 10"},
        typed_obligation={"id": "typed_1"},
        max_candidates=3,
    )

    assert result["metadata"]["contract"] == AGENT_HYPOTHESIS_EXPANSION_SET_CONTRACT
    assert result["status"] == "candidate_expansions_ready"
    assert result["candidate_count"] == 2
    assert result["validation_errors"] == []
    backends = {candidate["expected_backend"] for candidate in result["candidates"]}
    assert {"sympy", "lean"} <= backends
    for candidate in result["candidates"]:
        assert candidate["metadata"]["contract"] == AGENT_HYPOTHESIS_EXPANSION_CONTRACT
        assert candidate["target_blocker_id"] == "blocker_conditional_law_translation_required"
        assert candidate["provenance"] == "agent_generated_candidate"
        assert candidate["status"] == "candidate_pending_tree_verification"
        assert "not" in candidate["boundary"].lower()
        assert "proof" in candidate["boundary"].lower()
        assert validate_agent_hypothesis_expansion(candidate) == []


def test_macro_blocker_generates_symbol_map_route() -> None:
    result = propose_hypothesis_expansions(_blocker("macro_translation_required"))

    candidate = result["candidates"][0]
    assert candidate["expected_backend"] == "manual_formalization"
    assert "symbol map" in candidate["proposed_route"].lower()
    assert any("macro" in assumption.lower() for assumption in candidate["assumptions_added"])


def test_conditioning_scope_blocker_generates_scope_routes() -> None:
    result = propose_hypothesis_expansions(_blocker("conditioning_scope_translation_required"), max_candidates=3)

    routes = {candidate["id"] for candidate in result["candidates"]}
    assert any("sigma_field_scope" in route for route in routes)
    assert any("kernel_argument_scope" in route for route in routes)
    assert {candidate["expected_backend"] for candidate in result["candidates"]} == {"source_evidence", "lean"}
    assert result["validation_errors"] == []


def test_derivative_interchange_blocker_generates_finite_sum_and_dominated_routes() -> None:
    result = propose_hypothesis_expansions(_blocker("derivative_expectation_interchange_required"), max_candidates=3)

    text = " ".join(candidate["proposed_route"] for candidate in result["candidates"])
    assert "finite sum" in text
    assert "dominated" in text
    assert {candidate["expected_backend"] for candidate in result["candidates"]} == {"sympy", "lean"}
    assert result["validation_errors"] == []


def test_shape_and_multiline_blockers_generate_specific_routes() -> None:
    shape = propose_hypothesis_expansions(_blocker("missing_domain_or_shape_required"))
    multiline = propose_hypothesis_expansions(_blocker("grouped_multiline_obligation_required"))

    assert "conformable" in " ".join(shape["candidates"][0]["assumptions_added"]).lower()
    assert "split" in multiline["candidates"][0]["proposed_route"].lower()
    assert shape["candidates"][0]["expected_backend"] == "manual_formalization"
    assert multiline["candidates"][0]["expected_backend"] == "manual_formalization"


def test_accounting_identity_blocker_generates_finite_horizon_route() -> None:
    result = propose_hypothesis_expansions(_blocker("accounting_identity_condition"))

    candidate = result["candidates"][0]
    assert candidate["expected_backend"] == "sympy"
    assert "finite-horizon" in candidate["proposed_route"]
    assert any("cash-flow components" in assumption for assumption in candidate["assumptions_added"])


def test_validation_rejects_vague_or_raw_unbounded_hypothesis() -> None:
    errors = validate_agent_hypothesis_expansion(
        {
            "metadata": {"schema_version": "1.0", "contract": AGENT_HYPOTHESIS_EXPANSION_CONTRACT},
            "id": "bad",
            "target_blocker_id": "",
            "blocker_kind": "conditional_law_translation_required",
            "proposed_route": "Try stuff.",
            "assumptions_added": [],
            "why_might_close": "Maybe works.",
            "expected_backend": "agent",
            "expected_backend_role": "",
            "success_criterion": "Looks good.",
            "failure_criterion": "Fails.",
            "source_refs": [],
            "provenance": "agent_generated_candidate",
            "status": "candidate_pending_tree_verification",
            "boundary": "Candidate only.",
        }
    )

    assert "target_blocker_id must be a non-empty string" in errors
    assert "assumptions_added must contain at least one non-empty assumption" in errors
    assert "expected_backend is not an allowed backend or evidence route" in errors
    assert "expected_backend_role must be a non-empty string" in errors
    assert "boundary must explicitly state the hypothesis is not proof" in errors
    assert any("too vague" in error for error in errors)


def test_failed_paths_are_not_repeated() -> None:
    first = propose_hypothesis_expansions(_blocker(), max_candidates=1)
    failed = [{"id": first["candidates"][0]["id"]}]

    second = propose_hypothesis_expansions(_blocker(), failed_paths=failed, max_candidates=3)

    assert first["candidates"][0]["id"] not in {candidate["id"] for candidate in second["candidates"]}
    assert second["candidate_count"] == 1
