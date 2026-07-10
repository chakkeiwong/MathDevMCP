from mathdevmcp.derivation_search_tree import branch_promotion_report
from mathdevmcp.external_tool_adapters import (
    adapt_algebra_check,
    adapt_counterexample_search,
    adapt_lean_check,
    adapt_proof_state_evidence,
    adapt_retrieval_evidence,
    adapt_static_extraction_evidence,
)


def _node(attempt: dict) -> dict:
    return {
        "id": "node",
        "target": "target",
        "status": attempt["status"] if attempt["status"] in {"proved", "refuted"} else "partial",
        "backend_attempts": [attempt],
    }


def test_sympy_algebra_proof_maps_to_certifying_backend_attempt() -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "proved",
            "reason": "SymPy simplified the scoped equality to zero.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    result = adapt_algebra_check("a + b = b + a", tool="sympy", runner=fake_runner)
    attempt = result["attempt"]

    assert result["metadata"]["contract"] == "external_tool_adapter_attempt_result"
    assert result["source_contract"] == "derive_or_refute_result"
    assert attempt["tool"] == "sympy"
    assert attempt["status"] == "proved"
    assert attempt["evidence_kind"] == "certifying_backend"
    assert attempt["certification_status"] == "certified"
    assert branch_promotion_report(_node(attempt))["can_promote"] is True


def test_sage_backend_unavailable_maps_to_diagnostic_not_refutation() -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "backend_unavailable",
            "reason": "Sage is unavailable in this environment.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    result = adapt_algebra_check("det(A) = det(A)", tool="sage", runner=fake_runner)
    attempt = result["attempt"]

    assert attempt["status"] == "backend_unavailable"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["output_ref"] is None
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_counterexample_result_maps_to_refuting_attempt() -> None:
    def fake_runner(lhs, rhs):
        return {
            "status": "refuted",
            "reason": "A concrete counterexample was found.",
            "backend": "bounded_matrix_probe",
            "counterexample": {"assignments": {"A": [[1, 1], [0, 1]], "B": [[1, 0], [1, 1]]}},
            "metadata": {"schema_version": "1.0", "contract": "counterexample_search_result"},
        }

    result = adapt_counterexample_search("A*B", "B*A", runner=fake_runner)
    attempt = result["attempt"]
    node = _node(attempt)
    node["status"] = "refuted"

    assert attempt["status"] == "counterexample_found"
    assert attempt["evidence_kind"] == "counterexample"
    assert attempt["certification_status"] == "counterexample"
    assert branch_promotion_report(node)["can_promote"] is True


def test_algebra_scoped_contradiction_maps_to_refuting_attempt() -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "refuted",
            "reason": "Backend found a scoped contradiction for the encoded equality.",
            "counterexample_search": None,
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    result = adapt_algebra_check("1 + 1 = 3", tool="sympy", runner=fake_runner)
    attempt = result["attempt"]
    node = _node(attempt)
    node["status"] = "refuted"

    assert attempt["status"] == "refuted"
    assert attempt["evidence_kind"] == "scoped_contradiction"
    assert attempt["certification_status"] == "refuting"
    assert attempt["output_ref"]
    assert branch_promotion_report(node)["can_promote"] is True


def test_counterexample_unknown_remains_diagnostic() -> None:
    def fake_runner(lhs, rhs):
        return {
            "status": "unknown",
            "reason": "No counterexample was found in the bounded search.",
            "backend": "sympy_finite_domain",
            "counterexample": None,
            "metadata": {"schema_version": "1.0", "contract": "counterexample_search_result"},
        }

    result = adapt_counterexample_search("x + 1", "1 + x", runner=fake_runner)
    attempt = result["attempt"]

    assert attempt["status"] == "unknown"
    assert attempt["evidence_kind"] == "diagnostic"
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_counterexample_timeout_like_result_remains_diagnostic() -> None:
    def fake_runner(lhs, rhs):
        return {
            "status": "backend_timeout",
            "reason": "Counterexample search timed out.",
            "backend": "sympy_finite_domain",
            "counterexample": None,
            "metadata": {"schema_version": "1.0", "contract": "counterexample_search_result"},
        }

    result = adapt_counterexample_search("f(x)", "g(x)", timeout_seconds=1, runner=fake_runner)
    attempt = result["attempt"]

    assert attempt["status"] == "backend_timeout"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["timeout_seconds"] == 1
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_lean_verified_maps_to_lean_check_certificate() -> None:
    def fake_runner(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "verified",
            "reason": "Lean accepted the source without placeholders.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check("example : True := by trivial", timeout_seconds=3, runner=fake_runner)
    attempt = result["attempt"]
    node = _node(attempt)
    node["status"] = "proved"

    assert attempt["tool"] == "lean"
    assert attempt["status"] == "proved"
    assert attempt["evidence_kind"] == "lean_check"
    assert attempt["certification_status"] == "certified"
    assert attempt["timeout_seconds"] == 3
    assert branch_promotion_report(node)["can_promote"] is True


def test_lean_placeholder_or_inconclusive_remains_diagnostic() -> None:
    def fake_runner(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "inconclusive",
            "reason": "Lean source contains a placeholder proof.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check("example : True := by sorry", runner=fake_runner)
    attempt = result["attempt"]

    assert attempt["status"] == "inconclusive"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["output_ref"] is None
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_lean_mismatch_maps_to_scoped_contradiction_refutation() -> None:
    def fake_runner(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "mismatch",
            "reason": "Lean rejected the supplied proof artifact.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check("example : False := by trivial", timeout_seconds=2, runner=fake_runner)
    attempt = result["attempt"]
    node = _node(attempt)
    node["status"] = "refuted"

    assert attempt["status"] == "refuted"
    assert attempt["evidence_kind"] == "scoped_contradiction"
    assert attempt["certification_status"] == "refuting"
    assert attempt["output_ref"]
    assert branch_promotion_report(node)["can_promote"] is True


def test_adapter_exception_is_bounded_diagnostic_attempt() -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        raise RuntimeError("backend exploded")

    result = adapt_algebra_check("x = x", runner=fake_runner)
    attempt = result["attempt"]

    assert result["status"] == "adapter_error"
    assert result["source_contract"] == "external_tool_adapter_error"
    assert attempt["evidence_kind"] == "diagnostic"
    assert "backend exploded" in result["reason"]


def test_retrieval_static_and_proof_state_adapters_are_non_certifying() -> None:
    retrieval = adapt_retrieval_evidence(
        tool="leansearchv2",
        query="Nat.add_comm",
        hits=[{"name": "Nat.add_comm"}],
        version="0.1.0",
    )
    static = adapt_static_extraction_evidence(
        tool="jixia",
        target="Demo.lean",
        extracted={"declarations": ["demo"]},
    )
    proof_state = adapt_proof_state_evidence(
        tool="pantograph",
        target="example : True := by",
        trace=[{"state": "goals"}],
    )

    for result, evidence_kind in (
        (retrieval, "retrieval"),
        (static, "static_extraction"),
        (proof_state, "proof_state"),
    ):
        attempt = result["attempt"]
        assert attempt["evidence_kind"] == evidence_kind
        assert attempt["certification_status"] == "diagnostic"
        node = _node(attempt)
        node["status"] = "proved"
        report = branch_promotion_report(node)
        assert report["can_promote"] is False
        assert "proved status requires scoped certifying backend evidence" in report["errors"]
