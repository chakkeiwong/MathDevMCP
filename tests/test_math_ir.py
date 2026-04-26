from pathlib import Path

from mathdevmcp.math_ir import obligation_from_audit_obligation, validate_math_obligation
from mathdevmcp.proof_audit import audit_derivation_for_label


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


def test_validate_math_obligation_rejects_malformed_payload():
    errors = validate_math_obligation({"metadata": {"contract": "wrong"}, "kind": "bad", "backend_suitability": "bad"})

    assert "metadata.contract must be math_obligation" in errors
    assert "kind is invalid" in errors
    assert "backend_suitability is invalid" in errors
