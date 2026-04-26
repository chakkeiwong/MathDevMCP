from mathdevmcp.symbolic_backend import check_symbolic_obligation


def test_symbolic_backend_verifies_simple_algebra():
    result = check_symbolic_obligation("a + b", "b + a", backend="sympy")

    assert result["status"] == "equivalent"
    assert result["backend"] == "sympy"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "symbolic_backend_result"}


def test_symbolic_backend_refutes_numeric_false_identity():
    result = check_symbolic_obligation("1 + 1", "3", backend="sympy")

    assert result["status"] == "mismatch"
    assert result["evidence"][0]["kind"] == "backend_counterexample"


def test_symbolic_backend_abstains_on_unsafe_notation():
    result = check_symbolic_obligation("\\partial_i \\ell", "0", backend="sympy")

    assert result["status"] == "inconclusive"
    assert result["evidence"][0]["kind"] == "backend_not_encodable"
