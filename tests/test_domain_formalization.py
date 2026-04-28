from pathlib import Path

import pytest

from mathdevmcp.doctor import doctor_report
from mathdevmcp.domain_formalization import formalize_domain_obligation, formalize_domain_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def _requires_lean():
    if not doctor_report()["capabilities"]["lean"]["available"]:
        pytest.skip("Lean executable is unavailable")


def test_formalize_domain_obligation_verifies_curated_hamiltonian_scalar_identity():
    _requires_lean()
    result = formalize_domain_obligation("U + K", "K + U", domain="hamiltonian_scalar", variables={"U": "Nat", "K": "Nat"})

    assert result["status"] == "domain_verified"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "domain_formalization_result"}
    assert result["lean_check"]["status"] == "verified"
    assert result["uses_placeholder_proof"] is False


def test_formalize_domain_obligation_surfaces_missing_assumptions():
    result = formalize_domain_obligation("q + p", "p + q", domain="hamiltonian_scalar", variables={"q": "Nat"})

    assert result["status"] == "missing_assumptions"
    assert result["missing_assumptions"] == ["type for p"]
    assert result["lean_check"] is None


def test_formalize_domain_obligation_abstains_on_unsupported_kalman_notation():
    result = formalize_domain_obligation("\\ell_t", "-\\frac{1}{2}\\log\\det S_t", domain="kalman_scalar", variables={})

    assert result["status"] == "unsupported_notation"
    assert result["lean_check"] is None
    assert result["uses_placeholder_proof"] is False


def test_formalize_domain_label_preserves_latex_provenance_and_verifies():
    _requires_lean()
    result = formalize_domain_label(
        str(FIXTURES),
        "eq:domain-hamiltonian-commute",
        domain="hamiltonian_scalar",
        variables={"U": "Nat", "K": "Nat"},
    )

    assert result["status"] == "domain_verified"
    assert result["provenance"]["label"] == "eq:domain-hamiltonian-commute"
    assert result["obligation"]["lhs"] == "U + K"
    assert result["obligation"]["rhs"] == "K + U"


def test_formalize_domain_label_abstains_on_unsupported_stochastic_notation():
    result = formalize_domain_label(str(FIXTURES), "eq:domain-kalman-unsupported", domain="kalman_scalar", variables={})

    assert result["status"] == "unsupported_notation"
    assert result["provenance"]["label"] == "eq:domain-kalman-unsupported"
    assert result["lean_check"] is None
