import pytest

from mathdevmcp.contracts import validate_contract_payload
from mathdevmcp.math_debugging import (
    CERTIFICATION_BOUNDARY,
    assumption_record,
    backend_attempt_record,
    counterexample_record,
    math_question,
    validate_workbench_result,
    workbench_obligation,
    workbench_result,
)


def test_math_question_preserves_target_givens_assumptions_and_contract() -> None:
    question = math_question(
        "derive_or_refute",
        "x + y = y + x",
        givens=["x and y are real"],
        assumptions=["commutative addition"],
        context={"source": "unit-test"},
    )

    assert question["metadata"] == {"schema_version": "1.0", "contract": "math_debugging_question"}
    assert question["target"] == "x + y = y + x"
    assert question["givens"] == ["x and y are real"]
    assert question["assumptions"] == ["commutative addition"]


def test_workbench_result_records_certifying_backend_without_general_proof_claim() -> None:
    question = math_question("prove_or_refute", "a + b = b + a")
    attempt = backend_attempt_record(
        backend="sympy",
        status="proved",
        reason="SymPy simplified lhs-rhs to zero.",
        evidence=[{"kind": "backend_verified"}],
        severity="certifying",
    )
    obligation = workbench_obligation(
        "obl-1",
        lhs="a + b",
        rhs="b + a",
        status="proved",
        reason="Scoped obligation was certified.",
        backend_attempts=[attempt],
    )
    result = workbench_result(
        question,
        status="proved",
        reason="Every scoped obligation has certifying backend evidence.",
        obligations=[obligation],
        backend_attempts=[attempt],
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_debugging_workbench_result"}
    assert result["certification_boundary"] == CERTIFICATION_BOUNDARY
    assert "Only deterministic backend certificates" in result["certification_boundary"]
    assert validate_contract_payload({**result, "ok": True}) == []
    assert validate_workbench_result(result) == []


def test_workbench_result_records_refutation_with_counterexample() -> None:
    question = math_question("prove_or_refute", "1 + 1 = 3")
    counterexample = counterexample_record(
        assignments={},
        lhs_value=2,
        rhs_value=3,
        reason="Concrete evaluation differs.",
        backend="sympy",
    )
    attempt = backend_attempt_record(
        backend="sympy",
        status="refuted",
        reason="SymPy evaluated a nonzero difference.",
        evidence=[{"kind": "backend_counterexample"}],
        severity="blocking",
    )
    obligation = workbench_obligation(
        "obl-1",
        lhs="1 + 1",
        rhs="3",
        status="refuted",
        reason="The scoped obligation was refuted.",
        backend_attempts=[attempt],
        counterexample=counterexample,
    )
    result = workbench_result(
        question,
        status="refuted",
        reason="A scoped obligation has a concrete counterexample.",
        obligations=[obligation],
        backend_attempts=[attempt],
        counterexamples=[counterexample],
    )

    assert result["status"] == "refuted"
    assert result["counterexamples"][0]["lhs_value"] == 2
    assert result["counterexamples"][0]["rhs_value"] == 3
    assert validate_workbench_result(result) == []


def test_workbench_result_records_missing_assumptions_without_claiming_necessity() -> None:
    question = math_question("assumptions_required", "logdet(A) is defined")
    assumption = assumption_record(
        "A is square and positive definite",
        status="missing",
        source="logdet operand",
        necessity="required_by_route",
        used_by=["obl-1"],
    )
    obligation = workbench_obligation(
        "obl-1",
        lhs="logdet(A)",
        rhs="defined",
        status="missing_assumptions",
        reason="The route needs domain assumptions for logdet.",
        missing_assumptions=[assumption],
    )
    result = workbench_result(
        question,
        status="missing_assumptions",
        reason="At least one route-required assumption is missing.",
        obligations=[obligation],
        assumptions=[assumption],
    )

    assert result["assumptions"][0]["necessity"] == "required_by_route"
    assert "necessary" not in result["reason"].lower()
    assert validate_workbench_result(result) == []


def test_workbench_result_preserves_backend_unavailable_and_not_encodable_statuses() -> None:
    question = math_question("prove_or_refute", "theorem t : True")
    unavailable = backend_attempt_record(
        backend="lean",
        status="backend_unavailable",
        reason="Lean executable is unavailable.",
        severity="diagnostic",
    )
    result = workbench_result(
        question,
        status="backend_unavailable",
        reason="No configured backend could check this obligation.",
        backend_attempts=[unavailable],
        actions=[{"kind": "configure_backend", "backend": "lean"}],
    )

    assert result["status"] == "backend_unavailable"
    assert result["backend_attempts"][0]["severity"] == "diagnostic"
    assert validate_workbench_result(result) == []


def test_workbench_kernel_rejects_ambiguous_status_and_bad_severity() -> None:
    question = math_question("prove_or_refute", "x = y")

    with pytest.raises(ValueError):
        workbench_result(question, status="verified", reason="ambiguous legacy status")

    with pytest.raises(ValueError):
        backend_attempt_record(
            backend="sympy",
            status="unknown",
            reason="bad severity",
            severity="proofish",
        )
