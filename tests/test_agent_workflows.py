from pathlib import Path

from mathdevmcp.agent_workflows import audit_likelihood_implementation


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_audit_likelihood_implementation_detects_missing_operation(tmp_path):
    code = tmp_path / "likelihood.py"
    code.write_text("def ll(S, v):\n    return v @ v\n", encoding="utf-8")

    result = audit_likelihood_implementation(
        str(FIXTURES),
        "eq:proof-audit-kalman",
        str(code),
        required_operations=["logdet", "quadratic_form"],
        context_text="Kalman likelihood",
    )

    assert result["status"] == "mismatch"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "likelihood_implementation_audit"}
    assert "logdet" in result["operation_consistency"]["missing_operations"]


def test_audit_likelihood_implementation_reports_unverified_when_assumptions_missing(tmp_path):
    code = tmp_path / "likelihood.py"
    code.write_text("def ll(S, v):\n    return slogdet(S)[1] + v @ solve(S, v)\n", encoding="utf-8")

    result = audit_likelihood_implementation(
        str(FIXTURES),
        "eq:proof-audit-kalman",
        str(code),
        required_operations=["logdet", "quadratic_form", "inverse_or_solve"],
        context_text="Kalman likelihood",
    )

    assert result["status"] == "unverified"
    assert result["assumption_diagnostic"]["status"] == "missing_assumptions"
