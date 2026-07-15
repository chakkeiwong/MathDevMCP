import hashlib

import pytest

from mathdevmcp.sympy_adapter import (
    SympyScalarObligation,
    SympySymbol,
    run_sympy_scalar_obligation,
    sympy_native_input_bytes,
)


def _obligation(
    lhs="(x + 1)**2",
    rhs="x**2 + 2*x + 1",
    *,
    domain="rational",
    predicates=(),
):
    target = f"{lhs} = {rhs}"
    return SympyScalarObligation(
        branch_id="branch_sympy",
        branch_lineage=("root", "branch_sympy"),
        obligation_digest=hashlib.sha256(target.encode()).hexdigest(),
        target=target,
        lhs=lhs,
        rhs=rhs,
        symbols=(SympySymbol("x", domain, tuple(predicates)),),
    )


def test_polynomial_identity_records_canonical_srepr() -> None:
    result = run_sympy_scalar_obligation(_obligation())
    assert result["status"] == "certified"
    assert result["live_tool_executed"] is True
    assert result["can_promote"] is False
    assert result["evidence"]["output_ref"].startswith("mathdevmcp://sympy/")
    details = result["evidence"]["details"]
    assert details["srepr_lhs"]
    assert details["srepr_rhs"]
    assert details["srepr_difference"] == "Integer(0)"


def test_false_numeric_identity_has_scoped_constant_witness() -> None:
    result = run_sympy_scalar_obligation(_obligation("1 + 1", "3"))
    assert result["status"] == "refuted"
    assert result["evidence"]["refutation_witness"] == {
        "kind": "constant_difference",
        "difference": "-1",
    }
    assert result["can_promote"] is False


def test_division_identity_requires_nonzero_predicate() -> None:
    blocked = run_sympy_scalar_obligation(_obligation("x/x", "1", domain="real"))
    scoped = run_sympy_scalar_obligation(
        _obligation("x/x", "1", domain="real", predicates=("nonzero",))
    )
    assert blocked["status"] == "translation_error"
    assert "nonzero" in blocked["reason"]
    assert blocked["live_tool_executed"] is False
    assert scoped["status"] == "certified"
    assert (
        blocked["request"]["request_digest"]
        != scoped["request"]["request_digest"]
    )


def test_real_square_root_identity_requires_nonnegative_predicate() -> None:
    blocked = run_sympy_scalar_obligation(_obligation("sqrt(x)**2", "x", domain="real"))
    scoped = run_sympy_scalar_obligation(
        _obligation(
            "sqrt(x)**2", "x", domain="real", predicates=("nonnegative",)
        )
    )
    assert blocked["status"] == "translation_error"
    assert "nonnegative" in blocked["reason"]
    assert scoped["status"] == "certified"


def test_logarithm_requires_positive_symbol_predicate() -> None:
    blocked = run_sympy_scalar_obligation(_obligation("log(x)", "log(x)", domain="real"))
    scoped = run_sympy_scalar_obligation(
        _obligation("log(x)", "log(x)", domain="real", predicates=("positive",))
    )
    assert blocked["status"] == "translation_error"
    assert "positive" in blocked["reason"]
    assert scoped["status"] == "certified"


@pytest.mark.parametrize(
    ("lhs", "rhs", "reason_fragment"),
    [
        ("(x + 1)/(x + 1)", "1", "Compound denominators"),
        ("(x + 1)**-1", "1/(x + 1)", "compound base"),
        ("sqrt(x + 1)**2", "x + 1", "compound square-root"),
        ("log(x + 1)", "log(x + 1)", "compound logarithm"),
        ("x**65", "x**65", "exponent magnitude"),
        (str(2**300), str(2**300), "Integer literal"),
    ],
)
def test_expression_level_assumptions_and_resource_heavy_literals_abstain(
    lhs, rhs, reason_fragment
) -> None:
    result = run_sympy_scalar_obligation(
        _obligation(lhs, rhs, domain="real", predicates=("nonzero", "nonnegative"))
    )
    assert result["status"] == "translation_error"
    assert reason_fragment in result["reason"]
    assert result["live_tool_executed"] is False


def test_negative_symbol_power_requires_nonzero() -> None:
    blocked = run_sympy_scalar_obligation(_obligation("x**-1", "1/x", domain="real"))
    scoped = run_sympy_scalar_obligation(
        _obligation("x**-1", "1/x", domain="real", predicates=("nonzero",))
    )
    assert blocked["status"] == "translation_error"
    assert scoped["status"] == "certified"


@pytest.mark.parametrize(
    ("domain", "expected", "forbidden"),
    [
        ("integer", "integer=True", ("rational=False", "real=False")),
        ("rational", "rational=True", ("integer=False", "real=False")),
        ("real", "real=True", ("integer=False", "rational=False")),
    ],
)
def test_domain_encoding_asserts_only_positive_facts(domain, expected, forbidden) -> None:
    result = run_sympy_scalar_obligation(_obligation(domain=domain))
    srepr = result["evidence"]["details"]["srepr_lhs"]
    assert expected in srepr
    assert all(item not in srepr for item in forbidden)


@pytest.mark.parametrize(
    ("domain", "predicates"),
    [("complex", ()), ("real", ("negative",)), ("real", ("positive", "nonnegative"))],
)
def test_unsupported_or_contradictory_declarations_abstain(domain, predicates) -> None:
    result = run_sympy_scalar_obligation(
        _obligation(domain=domain, predicates=predicates)
    )
    assert result["status"] == "unsupported"
    assert result["can_promote"] is False


@pytest.mark.parametrize(
    "expression",
    ["__import__('os')", "x[0]", "lambda: x", "x < 2", "unknown(x)"],
)
def test_malformed_or_out_of_scope_expression_is_not_executed(expression) -> None:
    result = run_sympy_scalar_obligation(_obligation(expression, "x"))
    assert result["status"] == "translation_error"
    assert result["live_tool_executed"] is False


def test_injected_runner_is_fake_and_cannot_promote() -> None:
    def runner(payload, *, timeout_seconds):
        return {
            "status": "certified",
            "reason": "Synthetic success.",
            "srepr_difference": "Integer(0)",
        }

    result = run_sympy_scalar_obligation(_obligation(), runner=runner)
    assert result["status"] == "certified"
    assert result["execution"]["kind"] == "fake_runner"
    assert result["live_tool_executed"] is False
    assert result["can_promote"] is False
    assert result["evidence"]["details"] == {"srepr_difference": "Integer(0)"}


@pytest.mark.parametrize(
    ("runner", "status"),
    [
        (lambda payload, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")), "execution_error"),
        (lambda payload, **kwargs: (_ for _ in ()).throw(TimeoutError()), "timeout"),
        (lambda payload, **kwargs: ["not", "an", "object"], "malformed_output"),
        (lambda payload, **kwargs: {"status": "invented", "reason": "x"}, "malformed_output"),
    ],
)
def test_runner_failures_are_closed_nonmathematical_statuses(runner, status) -> None:
    result = run_sympy_scalar_obligation(_obligation(), runner=runner)
    assert result["status"] == status
    assert result["can_promote"] is False


def test_timeout_and_output_limits_are_bound_to_request() -> None:
    def large(payload, *, timeout_seconds):
        return {
            "status": "diagnostic",
            "reason": "large evidence",
            "srepr_difference": "x" * 1_000,
        }

    result = run_sympy_scalar_obligation(
        _obligation(), timeout_seconds=0.25, max_output_bytes=64, runner=large
    )
    assert result["status"] == "truncated_output"
    assert result["request"]["resource_limits"] == {
        "timeout_ms": 250,
        "max_output_bytes": 64,
        "max_artifact_bytes": 64,
    }


def test_native_bytes_and_request_identity_are_deterministic() -> None:
    obligation = _obligation(predicates=("nonzero",))
    assert sympy_native_input_bytes(obligation) == sympy_native_input_bytes(obligation)
    first = run_sympy_scalar_obligation(obligation, runner=lambda p, **k: {"status": "diagnostic", "reason": "x"})
    second = run_sympy_scalar_obligation(obligation, runner=lambda p, **k: {"status": "diagnostic", "reason": "x"})
    assert first["request"]["request_digest"] == second["request"]["request_digest"]


def test_sympy_target_must_exactly_match_encoded_sides() -> None:
    obligation = _obligation()
    changed = SympyScalarObligation(
        **{**obligation.__dict__, "target": "x = x"}
    )
    called = False

    def runner(payload, **kwargs):
        nonlocal called
        called = True
        return {"status": "certified", "reason": "should not run"}

    result = run_sympy_scalar_obligation(changed, runner=runner)
    assert result["status"] == "unsupported"
    assert called is False
