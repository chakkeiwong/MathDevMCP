import hashlib
import json
from pathlib import Path
import time

from mathdevmcp.derivation_search_tree import branch_promotion_report
from mathdevmcp.external_tool_adapters import (
    EvidenceContext,
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


def _context(*, label: str = "eq:test", max_output_bytes: int = 4096) -> EvidenceContext:
    source = b"x + 1 = 1 + x"
    target = "x + 1 = 1 + x"
    return EvidenceContext(
        source_logical_id="synthetic/source.tex",
        source_file="synthetic/source.tex",
        source_label=label,
        source_bytes=source,
        source_spans=({"start_byte": 0, "end_byte": len(source)},),
        parser_version="synthetic-1",
        obligation_digest=hashlib.sha256(target.encode()).hexdigest(),
        normalized_target=target,
        branch_id="branch_test",
        branch_lineage=("root", "branch_test"),
        typed_assumptions=({"id": "scalar", "kind": "domain", "statement": "x is real."},),
        native_input_bytes=target.encode(),
        native_input_media_type="text/plain",
        tool_name="sympy",
        adapter_version="p01-test",
        backend_version="fake",
        executable_id="fake_runner",
        timeout_ms=1000,
        max_output_bytes=max_output_bytes,
        expected_result_class="synthetic_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=(
            "no_real_document_extraction",
            "no_backend_conformance",
            "no_mathematical_certification",
            "no_branch_local_scheduler",
            "no_publication_eligibility",
            "no_source_document_edit",
            "no_multiprocess_support",
            "no_release_readiness",
        ),
        policy_version="p01-test",
    )


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


def test_late_algebra_runner_is_classified_as_timeout() -> None:
    def late_runner(target, *, lhs=None, rhs=None, backend="auto"):
        time.sleep(0.02)
        return {"status": "proved", "reason": "late"}

    result = adapt_algebra_check("x = x", timeout_seconds=0.001, runner=late_runner)
    assert result["status"] == "backend_timeout"
    assert result["attempt"]["certification_status"] == "diagnostic"


def test_fake_lean_verified_label_remains_diagnostic_without_exact_live_binding() -> None:
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
    assert attempt["status"] == "diagnostic"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["timeout_seconds"] == 3
    assert attempt["live_execution_binding_verified"] is False
    assert branch_promotion_report(node)["can_promote"] is False


def test_lean_placeholder_or_inconclusive_remains_diagnostic() -> None:
    def fake_runner(source, *, timeout_seconds=10, allow_sorry=False):
        return {
            "status": "inconclusive",
            "reason": "Lean source contains a placeholder proof.",
            "metadata": {"schema_version": "1.0", "contract": "lean_check_result"},
        }

    result = adapt_lean_check("example : True := by sorry", runner=fake_runner)
    attempt = result["attempt"]

    assert attempt["status"] == "diagnostic"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["output_ref"] is None
    assert branch_promotion_report(_node(attempt))["can_promote"] is False


def test_lean_proof_term_mismatch_is_not_mathematical_refutation() -> None:
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

    assert attempt["status"] == "diagnostic"
    assert attempt["evidence_kind"] == "diagnostic"
    assert attempt["certification_status"] == "diagnostic"
    assert attempt["output_ref"] is None
    assert branch_promotion_report(node)["can_promote"] is False


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


def test_complete_context_seals_verified_manifest_with_stable_request_identity(tmp_path) -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "proved",
            "reason": "Synthetic runner resolved the scoped fixture.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    first = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=fake_runner,
        evidence_context=_context(),
        artifact_root=tmp_path / "first",
    )
    second = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=fake_runner,
        evidence_context=_context(),
        artifact_root=tmp_path / "second",
    )
    left = first["evidence_attachment"]
    right = second["evidence_attachment"]
    assert first["certification_state"] == "verified_manifest"
    assert first["claim_eligibility"] == "ineligible"
    assert first["publication_enabled"] is False
    assert left["request_digest"] == right["request_digest"]
    assert left["attempt_id"] == right["attempt_id"]
    assert left["execution_id"] != right["execution_id"]
    assert left["run_id"] != right["run_id"]
    assert first["attempt"]["output_ref"] == left["manifest_ref"]


def test_source_label_is_part_of_v1_request_identity(tmp_path) -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {"status": "unknown", "reason": "Synthetic unknown."}

    left = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=fake_runner,
        evidence_context=_context(label="eq:left"),
        artifact_root=tmp_path / "left",
    )
    right = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=fake_runner,
        evidence_context=_context(label="eq:right"),
        artifact_root=tmp_path / "right",
    )
    assert left["evidence_attachment"]["request_digest"] != right["evidence_attachment"]["request_digest"]


def test_v1_runner_exception_is_sealed_bounded_and_nonclaiming(tmp_path) -> None:
    def fail_runner(target, *, lhs=None, rhs=None, backend="auto"):
        raise RuntimeError("x" * 200)

    result = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=fail_runner,
        evidence_context=_context(max_output_bytes=32),
        artifact_root=tmp_path / "error",
    )
    assert result["status"] == "adapter_error"
    assert result["evidence_attachment"]["integrity_state"] == "verified"
    assert result["claim_eligibility"] == "ineligible"
    assert result["publication_enabled"] is False


def test_structured_result_truncation_is_explicit_integrity_error(tmp_path) -> None:
    def oversized_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {"status": "proved", "reason": "x" * 512}

    result = adapt_algebra_check(
        "x + 1 = 1 + x",
        runner=oversized_runner,
        evidence_context=_context(max_output_bytes=32),
        artifact_root=tmp_path / "truncated",
    )
    attachment = result["evidence_attachment"]
    manifest_ref = Path(attachment["manifest_ref"])
    manifest_path = tmp_path / "truncated" / manifest_ref
    manifest = json.loads(manifest_path.read_bytes())

    assert attachment["integrity_state"] == "verified"
    assert manifest["result"]["outcome"] == "integrity_error"
    assert manifest["result"]["stderr_truncated"] is False
    assert manifest["result"]["structured_result"]["role"] == "structured_result_truncated"
    assert manifest["result"]["structured_result"]["media_type"] == "application/octet-stream"
    assert manifest["interpretation"]["veto_ids"] == ["structured_result_truncated"]
    assert manifest["interpretation"]["certified_scope"] is None
    assert result["claim_eligibility"] == "ineligible"


def test_context_without_artifact_root_remains_explicit_legacy() -> None:
    def fake_runner(target, *, lhs=None, rhs=None, backend="auto"):
        return {"status": "proved", "reason": "Synthetic raw result."}

    result = adapt_algebra_check("x + 1 = 1 + x", runner=fake_runner, evidence_context=_context())
    assert result["evidence_attachment"] is None
    assert result["certification_state"] == "unbound_legacy_evidence"
    assert result["attempt"]["evidence_schema_version"] == "0-legacy"
    assert result["claim_eligibility"] == "ineligible"
