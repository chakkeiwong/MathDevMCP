from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.valuation_formalization import TERMINAL_VALUE_TARGET, validate_terminal_value_definition


SOURCE = Path("docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex")


def _semantics() -> dict:
    path = SOURCE.resolve()
    raw = path.read_bytes()
    start = raw.index(b"The base-case terminal value should be explicit and bounded.")
    end = raw.index(b"Discounting and funding should use different fields.")
    span = raw[start:end]
    target_start = span.index(b"\\begin{equation}")
    target_end = span.index(b"\\end{equation}") + len(b"\\end{equation}")
    source_target = span[target_start:target_end].decode("utf-8")
    return {
        "role": "definition",
        "authority": "source_evidenced_role",
        "source_path": str(path),
        "source_digest": hashlib.sha256(raw).hexdigest(),
        "source_span": {"start_byte": start, "end_byte": end, "sha256": hashlib.sha256(span).hexdigest()},
        "source_target": source_target,
        "source_target_digest": hashlib.sha256(source_target.encode()).hexdigest(),
        "label": "eq:terminal-value-base",
    }


def test_source_bound_terminal_value_executes_scoped_sympy_check() -> None:
    result = validate_terminal_value_definition(
        TERMINAL_VALUE_TARGET,
        provided_assumptions=["r_disc + lambda_attrition + q != 0"],
        claim_semantics=_semantics(),
    )

    assert result["status"] == "algebraically_consistent"
    assert result["backend_attempt"]["backend"] == "sympy"
    assert result["backend_attempt"]["severity"] == "diagnostic"
    assert result["backend_attempt"]["residual"] == "0"
    assert result["assumption_diagnostic"]["missing_assumptions"] == []
    assert any("economic validity" in item for item in result["non_claims"])


def test_terminal_value_zero_denominator_domain_remains_a_veto() -> None:
    result = validate_terminal_value_definition(
        TERMINAL_VALUE_TARGET,
        provided_assumptions=["r_disc != 0"],
        claim_semantics=_semantics(),
    )

    assert result["status"] == "missing_assumptions"
    assert result["backend_attempt"] is None


def test_terminal_value_adapter_abstains_on_expectation_and_policy_semantics() -> None:
    result = validate_terminal_value_definition(
        r"dTV = \E[rho*dCF_next/(r_disc + lambda_attrition + q) | policy]",
        provided_assumptions=["r_disc + lambda_attrition + q != 0"],
        claim_semantics=_semantics(),
    )

    assert result["status"] == "unsupported_semantics"
    assert result["backend_attempt"] is None
