from mathdevmcp.debug_derivation import debug_derivation, score_gap_localization
from mathdevmcp.high_level_contracts import validate_high_level_result


def test_debug_derivation_all_valid_chain_proves_scoped_transitions() -> None:
    result = debug_derivation(["a + b", "b + a", "a + b"])

    assert result["status"] == "proved"
    assert result["evidence_classes"] == ["backend_certificate"]
    assert validate_high_level_result(result) == []


def test_debug_derivation_localizes_first_refuted_step() -> None:
    result = debug_derivation(["1 + 1", "3", "3"])

    assert result["status"] == "inconclusive"
    assert "certifying_evidence_not_promoted" in {item["code"] for item in result["veto_reasons"]}
    assert validate_high_level_result(result) == []


def test_debug_derivation_refutes_when_counterexample_artifact_exists() -> None:
    result = debug_derivation(["A*B", "B*A"])

    assert result["status"] == "refuted"
    assert result["counterexamples"]
    assert validate_high_level_result(result) == []


def test_debug_derivation_missing_assumption_is_gap_not_global_failure() -> None:
    result = debug_derivation(["logdet(A)", "trace(A)", "trace(A)"])

    assert result["status"] == "gap_found"
    assert result["evidence_classes"] == ["proof_gap"]
    assert "gap_localization_not_global_failure" in {item["code"] for item in result["non_claims"]}
    rubric = score_gap_localization(result, expected_index=0, expected_statuses={"missing_assumptions", "unknown"})
    assert rubric["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_debug_derivation_short_chain_is_inconclusive_not_failure() -> None:
    result = debug_derivation(["only one step"])

    assert result["status"] == "gap_found"
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []


def test_gap_localization_rubric_detects_wrong_index() -> None:
    result = debug_derivation(["logdet(A)", "trace(A)", "trace(A)"])
    rubric = score_gap_localization(result, expected_index=1, expected_statuses={"missing_assumptions"})

    assert rubric["status"] == "failed"
    assert rubric["observed_index"] == 0
