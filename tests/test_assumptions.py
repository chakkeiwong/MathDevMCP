from pathlib import Path

from mathdevmcp.assumptions import diagnose_assumptions_for_label, diagnose_assumptions_for_obligation
from mathdevmcp.proof_audit import audit_derivation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_assumption_diagnostic_surfaces_missing_inverse_and_derivative_assumptions():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-kalman", backend="sympy")
    result = diagnose_assumptions_for_obligation(audit["obligations"][0], context_text="Kalman likelihood score")

    assert result["status"] == "missing_assumptions"
    missing = {item["text"] for item in result["missing_assumptions"]}
    assert "invertibility or positive definiteness for inverse" in missing
    assert "differentiability for derivative" in missing
    assert result["metadata"] == {"schema_version": "1.0", "contract": "assumption_diagnostic"}


def test_assumption_diagnostic_uses_explicit_assumptions():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-kalman", backend="sympy")
    result = diagnose_assumptions_for_obligation(
        audit["obligations"][0],
        context_text="Assume S_t is positive definite and differentiable in the parameter.",
    )

    assert result["explicit_assumptions"]
    missing = {item["text"] for item in result["missing_assumptions"]}
    assert "invertibility or positive definiteness for inverse" not in missing
    assert "differentiability for derivative" not in missing


def test_assumption_diagnostic_for_label_preserves_context():
    result = diagnose_assumptions_for_label(str(FIXTURES), "eq:proof-audit-kalman", context_text="Kalman likelihood")

    assert result["label"] == "eq:proof-audit-kalman"
    assert result["doc_context"]["label"] == "eq:proof-audit-kalman"
