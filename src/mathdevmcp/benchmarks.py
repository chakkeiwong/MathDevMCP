from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .ast_operation_graph import build_ast_operation_graph_for_file
from .consistency import compare_files, compare_label_to_code
from .contracts import contract_metadata, success_result
from .derivation import derive_step_for_label
from .kalman_workflows import audit_kalman_recursion
from .parser_benchmark import run_parser_backend
from .proof_audit import audit_derivation_for_label
from .workflow import build_implementation_brief

BenchmarkCategory = Literal["consistency", "derivation", "workflow", "proof_audit", "kalman_recursion", "parser_corpus", "ast_corpus"]


@dataclass(frozen=True)
class BenchmarkResult:
    id: str
    category: BenchmarkCategory
    evaluation_focus: str
    expected_status: str
    observed_status: str
    expected_abstention: bool
    passed: bool
    quality_checks: dict[str, bool]
    details: dict


@dataclass(frozen=True)
class BenchmarkSummary:
    by_category: dict[str, dict[str, int]]
    by_focus: dict[str, dict[str, int]]
    expected_abstentions: int


@dataclass(frozen=True)
class BenchmarkReport:
    ok: bool
    passed: int
    total: int
    results: list[dict]
    summary: dict[str, dict[str, dict[str, int]]]
    metadata: dict[str, str]


@dataclass(frozen=True)
class BenchmarkGateResult:
    ok: bool
    passed: bool
    total: int
    passed_count: int
    failed_count: int
    summary: dict[str, dict[str, dict[str, int]]]
    policy: dict
    metadata: dict[str, str]



def benchmark_gate_policy() -> dict:
    return {
        "name": "all_benchmarks_must_pass",
        "required_pass_rate": 1.0,
        "allow_category_failures": {},
        "description": "Every benchmark case must pass; no category-specific failure budget is currently allowed.",
    }



def _doc_context_matches_expectation(doc_context: dict, expected: dict) -> bool:
    return all(doc_context.get(key) == value for key, value in expected.items())



def _benchmark_result(
    *,
    benchmark_id: str,
    category: BenchmarkCategory,
    evaluation_focus: str,
    expected_status: str,
    observed_status: str,
    passed: bool,
    quality_checks: dict[str, bool],
    details: dict,
    expected_abstention: bool = False,
) -> dict:
    return asdict(
        BenchmarkResult(
            id=benchmark_id,
            category=category,
            evaluation_focus=evaluation_focus,
            expected_status=expected_status,
            observed_status=observed_status,
            expected_abstention=expected_abstention,
            passed=passed,
            quality_checks=quality_checks,
            details=details,
        )
    )



def _consistency_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "doc_consistency_good",
            "category": "consistency",
            "evaluation_focus": "status_regression",
            "doc": str(fixtures / "doc_consistency_good.tex"),
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
        },
        {
            "id": "doc_consistency_bad",
            "category": "consistency",
            "evaluation_focus": "status_regression",
            "doc": str(fixtures / "doc_consistency_bad.tex"),
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_missing_in_code": ["logdet"],
        },
        {
            "id": "label_consistency_good",
            "category": "consistency",
            "evaluation_focus": "provenance_correctness",
            "doc_root": str(fixtures),
            "label": "prop:transport-logdet",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
        },
        {
            "id": "label_consistency_bad",
            "category": "consistency",
            "evaluation_focus": "provenance_correctness",
            "doc_root": str(fixtures),
            "label": "prop:transport-mismatch",
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_missing_in_code": ["logdet"],
            "expected_doc_context": {"file": "doc_consistency_bad.tex", "label": "prop:transport-mismatch"},
        },
        {
            "id": "label_consistency_hamiltonian_energy",
            "category": "consistency",
            "evaluation_focus": "realistic_fixture",
            "doc_root": str(fixtures),
            "label": "prop:hamiltonian-energy",
            "code": str(fixtures / "doc_realistic_hamiltonian.py"),
            "required_terms": ["potential_energy", "kinetic_energy"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
            "expected_doc_context": {"file": "doc_realistic_hamiltonian.tex", "label": "prop:hamiltonian-energy"},
        },
    ]



def _derivation_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "derivation_context_support",
            "category": "derivation",
            "evaluation_focus": "abstention_quality",
            "doc_root": str(fixtures),
            "label": "prop:transport-implementation",
            "lhs": "log pi(u) + logdet",
            "rhs": "logdet + log pi(u)",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_supported_by_context": True,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_consistency_context.tex", "label": "prop:transport-implementation"},
        },
        {
            "id": "derivation_symbol_mismatch",
            "category": "derivation",
            "evaluation_focus": "false_confidence_control",
            "doc_root": str(fixtures),
            "label": "eq:transport-density-step",
            "lhs": "log pi(u) + logdet",
            "rhs": "log pi(u)",
            "paragraph_context": True,
            "expected_status": "mismatch",
            "expected_abstention": False,
            "expected_supported_by_context": True,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_derivation_chain.tex", "label": "eq:transport-density-step"},
        },
        {
            "id": "derivation_realistic_kalman_hessian_abstention",
            "category": "derivation",
            "evaluation_focus": "realistic_abstention",
            "doc_root": str(fixtures),
            "label": "eq:kalman-innovation-score-local",
            "lhs": "trace + S_t + inverse + d_i + S_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + d_i + v_t + S_t + inverse + v_t",
            "rhs": "d_i + v_t + S_t + inverse + v_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + trace + S_t + inverse + d_i + S_t",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_supported_by_context": False,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_realistic_kalman_hessian.tex", "label": "eq:kalman-innovation-score-local"},
        },
        {
            "id": "derivation_multilabel_kalman_score_abstention",
            "category": "derivation",
            "evaluation_focus": "multilabel_provenance",
            "doc_root": str(fixtures),
            "label": "eq:kalman-score-contribution",
            "lhs": "trace + S_t + inverse + d_i + S_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + d_i + v_t + S_t + inverse + v_t",
            "rhs": "d_i + v_t + S_t + inverse + v_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + trace + S_t + inverse + d_i + S_t",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_supported_by_context": False,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_multilabel_kalman_chain.tex", "label": "eq:kalman-score-contribution"},
        },
        {
            "id": "derivation_longdoc_kalman_score_abstention",
            "category": "derivation",
            "evaluation_focus": "long_document_provenance",
            "doc_root": str(fixtures),
            "label": "eq:longdoc-score-contribution",
            "lhs": "trace + S_t + inverse + d_i + S_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + d_i + v_t + S_t + inverse + v_t",
            "rhs": "d_i + v_t + S_t + inverse + v_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + trace + S_t + inverse + d_i + S_t",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_supported_by_context": False,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_longdoc_kalman_retrieval.tex", "label": "eq:longdoc-score-contribution", "section_path": ["Likelihood derivative notes"]},
        },
        {
            "id": "derivation_repeat_label_kalman_score_abstention",
            "category": "derivation",
            "evaluation_focus": "repeat_label_stability",
            "doc_root": str(fixtures),
            "label": "eq:repeat-kalman-target-score",
            "lhs": "trace + S_t + inverse + d_i + S_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + d_i + v_t + S_t + inverse + v_t",
            "rhs": "d_i + v_t + S_t + inverse + v_t + quadratic + v_t + S_t + inverse + d_i + S_t + S_t + inverse + v_t + trace + S_t + inverse + d_i + S_t",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_supported_by_context": False,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_repeat_label_kalman_scale.tex", "label": "eq:repeat-kalman-target-score", "section_path": ["Target likelihood derivative block"]},
        },
    ]



def _workflow_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "workflow_implementation_brief_consistent",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport log-determinant identity",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_selected_label": "prop:transport-logdet",
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
            "expected_check_statuses": {"consistency": "consistent"},
        },
        {
            "id": "workflow_implementation_brief_unverified",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport log-determinant identity",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "lhs": "log_pi + logdet",
            "rhs": "logdet + log_pi",
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_selected_label": "prop:transport-logdet",
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
            "expected_check_statuses": {"consistency": "consistent", "derivation": "unverified"},
        },
        {
            "id": "workflow_implementation_brief_mismatch",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport identity",
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_selected_label": "prop:transport-mismatch",
            "expected_doc_context": {"file": "doc_consistency_bad.tex", "label": "prop:transport-mismatch"},
            "expected_check_statuses": {"consistency": "mismatch"},
        },
    ]



def _proof_audit_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "proof_audit_single_verified",
            "category": "proof_audit",
            "evaluation_focus": "proof_audit_routing",
            "doc_root": str(fixtures),
            "label": "eq:proof-audit-single",
            "expected_status": "verified",
            "expected_abstention": False,
            "expected_counts": {"verified": 1, "mismatched": 0, "not_encodable": 0, "not_extracted": 0},
            "expected_doc_context": {"file": "doc_proof_audit.tex", "label": "eq:proof-audit-single"},
        },
        {
            "id": "proof_audit_false_mismatch",
            "category": "proof_audit",
            "evaluation_focus": "false_confidence_control",
            "doc_root": str(fixtures),
            "label": "eq:proof-audit-false",
            "expected_status": "mismatch",
            "expected_abstention": False,
            "expected_counts": {"verified": 0, "mismatched": 1, "not_encodable": 0, "not_extracted": 0},
            "expected_doc_context": {"file": "doc_proof_audit.tex", "label": "eq:proof-audit-false"},
        },
        {
            "id": "proof_audit_kalman_abstention",
            "category": "proof_audit",
            "evaluation_focus": "proof_audit_abstention",
            "doc_root": str(fixtures),
            "label": "eq:proof-audit-kalman",
            "expected_status": "inconclusive",
            "expected_abstention": True,
            "expected_counts": {"verified": 0, "mismatched": 0, "not_encodable": 1, "not_extracted": 0},
            "expected_doc_context": {"file": "doc_proof_audit.tex", "label": "eq:proof-audit-kalman"},
        },
    ]


def _kalman_recursion_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "kalman_recursion_structural_unverified",
            "category": "kalman_recursion",
            "evaluation_focus": "ast_recursion_abstention",
            "code": str(fixtures / "doc_kalman_recursion_good.py"),
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_missing_operations": [],
            "expected_missing_guards": ["shape_guard", "covariance_guard"],
        },
        {
            "id": "kalman_recursion_missing_covariance_update",
            "category": "kalman_recursion",
            "evaluation_focus": "false_confidence_control",
            "code": str(fixtures / "doc_kalman_recursion_bad.py"),
            "expected_status": "mismatch",
            "expected_abstention": False,
            "expected_missing_operations": ["covariance_update"],
            "expected_missing_guards": ["shape_guard", "covariance_guard"],
        },
    ]


def _parser_corpus_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "parser_corpus_department_current",
            "category": "parser_corpus",
            "evaluation_focus": "realistic_parser_provenance",
            "doc_root": str(fixtures),
            "backend": "current",
            "expected_status": "parsed",
            "expected_labels": [
                "assump:dept-state-space-guards",
                "eq:dept-state-space-recursion",
                "eq:dept-state-space-likelihood",
                "assump:dept-hmc-regularity",
                "eq:dept-log-posterior",
                "eq:dept-hmc-leapfrog",
                "eq:dept-hmc-hamiltonian",
            ],
        }
    ]


def _ast_corpus_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "ast_corpus_state_space_jax",
            "category": "ast_corpus",
            "evaluation_focus": "realistic_ast_operation_coverage",
            "code": str(fixtures / "doc_department_state_space_jax.py"),
            "expected_status": "consistent",
            "expected_operations": ["logdet", "inverse_or_solve", "scan_loop", "shape_guard", "covariance_guard", "prediction_update", "covariance_update"],
        },
        {
            "id": "ast_corpus_hmc_jax",
            "category": "ast_corpus",
            "evaluation_focus": "realistic_ast_operation_coverage",
            "code": str(fixtures / "doc_department_hmc_jax.py"),
            "expected_status": "consistent",
            "expected_operations": ["gradient", "leapfrog_update", "posterior_or_likelihood", "hamiltonian_energy", "quadratic_form"],
        },
        {
            "id": "ast_corpus_particle_filter",
            "category": "ast_corpus",
            "evaluation_focus": "realistic_ast_operation_coverage",
            "code": str(fixtures / "doc_department_particle_filter.py"),
            "expected_status": "consistent",
            "expected_operations": ["logsumexp", "particle_normalization", "posterior_or_likelihood"],
        },
        {
            "id": "ast_corpus_state_space_missing_solve",
            "category": "ast_corpus",
            "evaluation_focus": "false_confidence_control",
            "code": str(fixtures / "doc_department_state_space_missing_solve.py"),
            "expected_status": "mismatch",
            "required_operations": ["logdet", "inverse_or_solve", "quadratic_form"],
            "expected_missing_operations": ["inverse_or_solve"],
        },
    ]



def benchmark_cases(root: Path) -> list[dict]:
    return (
        _consistency_cases(root)
        + _derivation_cases(root)
        + _workflow_cases(root)
        + _proof_audit_cases(root)
        + _kalman_recursion_cases(root)
        + _parser_corpus_cases(root)
        + _ast_corpus_cases(root)
    )



def write_seeded_mismatch_benchmark(root: Path) -> list[dict]:
    return [case for case in _consistency_cases(root) if case["id"] in {"doc_consistency_good", "doc_consistency_bad"}]



def run_seeded_mismatch_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in write_seeded_mismatch_benchmark(root):
        result = compare_files(case["doc"], case["code"], required_terms=case["required_terms"])
        status_ok = result["status"] == case["expected_status"]
        missing_ok = result["missing_in_code"] == case["expected_missing_in_code"]
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and missing_ok,
                quality_checks={
                    "status_match": status_ok,
                    "missing_terms_match": missing_ok,
                },
                details={
                    "missing_in_code": result["missing_in_code"],
                    "findings": result["findings"],
                },
            )
        )
    return results



def run_label_consistency_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in [item for item in _consistency_cases(root) if "label" in item]:
        result = compare_label_to_code(case["doc_root"], case["label"], case["code"], required_terms=case["required_terms"])
        status_ok = result["status"] == case["expected_status"]
        missing_ok = result["missing_in_code"] == case["expected_missing_in_code"]
        provenance_ok = _doc_context_matches_expectation(result["doc_context"], case["expected_doc_context"])
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and missing_ok and provenance_ok,
                quality_checks={
                    "status_match": status_ok,
                    "missing_terms_match": missing_ok,
                    "provenance_match": provenance_ok,
                },
                details={
                    "label": case["label"],
                    "missing_in_code": result["missing_in_code"],
                    "doc_context": result["doc_context"],
                },
            )
        )
    return results



def run_derivation_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _derivation_cases(root):
        result = derive_step_for_label(
            case["doc_root"],
            case["label"],
            case["lhs"],
            case["rhs"],
            paragraph_context=case["paragraph_context"],
        )
        status_ok = result["status"] == case["expected_status"]
        context_ok = result["supported_by_context"] == case["expected_supported_by_context"]
        cited_labels = result["step_chain"][0]["cited_labels"]
        cited_ok = cited_labels == case["expected_cited_labels"]
        provenance_ok = _doc_context_matches_expectation(result["doc_context"], case["expected_doc_context"])
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and context_ok and cited_ok and provenance_ok,
                quality_checks={
                    "status_match": status_ok,
                    "supported_by_context_match": context_ok,
                    "cited_labels_match": cited_ok,
                    "provenance_match": provenance_ok,
                    "expected_abstention_match": result["status"] == "unverified" if case.get("expected_abstention", False) else result["status"] != "unverified",
                },
                details={
                    "label": case["label"],
                    "supported_by_context": result["supported_by_context"],
                    "step_chain": result["step_chain"],
                    "doc_context": result["doc_context"],
                    "evidence": result["evidence"],
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results



def run_workflow_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _workflow_cases(root):
        result = build_implementation_brief(
            case["doc_root"],
            case["query"],
            case["code"],
            required_terms=case.get("required_terms"),
            lhs=case.get("lhs"),
            rhs=case.get("rhs"),
        )
        status_ok = result["status"] == case["expected_status"]
        label_ok = result["selected_label"] == case["expected_selected_label"]
        provenance_ok = _doc_context_matches_expectation(result.get("doc_context", {}), case["expected_doc_context"])
        checks_ok = all(
            result["checks"].get(name, {}).get("status") == expected_status
            for name, expected_status in case["expected_check_statuses"].items()
        )
        envelope_ok = result.get("ok") is True and result.get("metadata", {}).get("contract") == "implementation_brief"
        abstention_ok = result["status"] == "unverified" if case.get("expected_abstention", False) else result["status"] != "unverified"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and label_ok and provenance_ok and checks_ok and envelope_ok and abstention_ok,
                quality_checks={
                    "status_match": status_ok,
                    "selected_label_match": label_ok,
                    "provenance_match": provenance_ok,
                    "check_statuses_match": checks_ok,
                    "envelope_match": envelope_ok,
                    "expected_abstention_match": abstention_ok,
                },
                details={
                    "metadata": result.get("metadata"),
                    "ok": result.get("ok"),
                    "selected_label": result["selected_label"],
                    "doc_context": result.get("doc_context"),
                    "checks": result["checks"],
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results



def run_proof_audit_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _proof_audit_cases(root):
        result = audit_derivation_for_label(case["doc_root"], case["label"], backend="sympy")
        status_ok = result["status"] == case["expected_status"]
        counts_ok = all(result["counts"].get(key) == value for key, value in case["expected_counts"].items())
        provenance_ok = _doc_context_matches_expectation(result["doc_context"], case["expected_doc_context"])
        abstention_ok = result["status"] in {"inconclusive", "unverified"} if case.get("expected_abstention", False) else result["status"] not in {"inconclusive", "unverified"}
        evidence_ok = all(obligation.get("provenance", {}).get("label") == case["label"] for obligation in result["obligations"])
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and counts_ok and provenance_ok and abstention_ok and evidence_ok,
                quality_checks={
                    "status_match": status_ok,
                    "counts_match": counts_ok,
                    "provenance_match": provenance_ok,
                    "expected_abstention_match": abstention_ok,
                    "obligation_provenance_match": evidence_ok,
                },
                details={
                    "label": case["label"],
                    "counts": result["counts"],
                    "doc_context": result["doc_context"],
                    "obligations": result["obligations"],
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results


def run_kalman_recursion_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _kalman_recursion_cases(root):
        result = audit_kalman_recursion(case["code"])
        status_ok = result["status"] == case["expected_status"]
        missing_ops_ok = result["missing_operations"] == case["expected_missing_operations"]
        missing_guards_ok = result["shape_diagnostics"]["missing_guards"] == case["expected_missing_guards"]
        ast_contract_ok = result["ast_operation_graph"].get("metadata", {}).get("contract") == "ast_operation_graph"
        abstention_ok = result["status"] in {"inconclusive", "unverified"} if case.get("expected_abstention", False) else result["status"] not in {"inconclusive", "unverified"}
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and missing_ops_ok and missing_guards_ok and ast_contract_ok and abstention_ok,
                quality_checks={
                    "status_match": status_ok,
                    "missing_operations_match": missing_ops_ok,
                    "missing_guards_match": missing_guards_ok,
                    "ast_contract_match": ast_contract_ok,
                    "expected_abstention_match": abstention_ok,
                },
                details={
                    "code": case["code"],
                    "missing_operations": result["missing_operations"],
                    "shape_diagnostics": result["shape_diagnostics"],
                    "observed_operations": result["observed_operations"],
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results


def run_parser_corpus_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _parser_corpus_cases(root):
        result = run_parser_backend(case["doc_root"], case["backend"])
        labels = set(result.get("labels", []))
        expected_labels = set(case["expected_labels"])
        status_ok = result["status"] == case["expected_status"]
        labels_ok = expected_labels.issubset(labels)
        provenance_ok = result["quality_checks"].get("provenance_available", False)
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and labels_ok and provenance_ok,
                quality_checks={
                    "status_match": status_ok,
                    "expected_labels_preserved": labels_ok,
                    "provenance_available": provenance_ok,
                },
                details={
                    "backend": case["backend"],
                    "expected_labels": sorted(expected_labels),
                    "missing_expected_labels": sorted(expected_labels - labels),
                    "parser_result": result,
                },
            )
        )
    return results


def run_ast_corpus_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _ast_corpus_cases(root):
        graph = build_ast_operation_graph_for_file(case["code"])
        observed = set(graph.get("operations", []))
        if "required_operations" in case:
            missing = [operation for operation in case["required_operations"] if operation not in observed]
            observed_status = "mismatch" if missing else graph["status"]
            expected_missing = case.get("expected_missing_operations", [])
            missing_ok = missing == expected_missing
            operations_ok = missing_ok
        else:
            missing = []
            observed_status = graph["status"]
            expected_operations = set(case["expected_operations"])
            operations_ok = expected_operations.issubset(observed)
            expected_missing = []
        status_ok = observed_status == case["expected_status"]
        graph_contract_ok = graph.get("metadata", {}).get("contract") == "ast_operation_graph"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=observed_status,
                passed=status_ok and operations_ok and graph_contract_ok,
                quality_checks={
                    "status_match": status_ok,
                    "operations_match": operations_ok,
                    "graph_contract_match": graph_contract_ok,
                },
                details={
                    "code": case["code"],
                    "expected_operations": case.get("expected_operations", case.get("required_operations", [])),
                    "observed_operations": sorted(observed),
                    "missing_operations": missing,
                    "expected_missing_operations": expected_missing,
                },
            )
        )
    return results



def summarize_benchmark_results(results: list[dict]) -> dict:
    category_totals: dict[str, dict[str, int]] = {}
    focus_totals: dict[str, dict[str, int]] = {}
    expected_abstentions = 0
    for result in results:
        category = result["category"]
        focus = result["evaluation_focus"]
        category_bucket = category_totals.setdefault(category, {"total": 0, "passed": 0, "expected_abstentions": 0})
        focus_bucket = focus_totals.setdefault(focus, {"total": 0, "passed": 0, "expected_abstentions": 0})
        category_bucket["total"] += 1
        focus_bucket["total"] += 1
        if result["passed"]:
            category_bucket["passed"] += 1
            focus_bucket["passed"] += 1
        if result.get("expected_abstention", False):
            expected_abstentions += 1
            category_bucket["expected_abstentions"] += 1
            focus_bucket["expected_abstentions"] += 1
    return asdict(
        BenchmarkSummary(
            by_category=category_totals,
            by_focus=focus_totals,
            expected_abstentions=expected_abstentions,
        )
    )



def build_benchmark_report(root: Path) -> dict:
    results = (
        run_seeded_mismatch_benchmark(root)
        + run_label_consistency_benchmark(root)
        + run_derivation_benchmark(root)
        + run_workflow_benchmark(root)
        + run_proof_audit_benchmark(root)
        + run_kalman_recursion_benchmark(root)
        + run_parser_corpus_benchmark(root)
        + run_ast_corpus_benchmark(root)
    )
    passed_count = sum(1 for result in results if result["passed"])
    return asdict(
        BenchmarkReport(
            ok=True,
            passed=passed_count,
            total=len(results),
            results=results,
            summary=summarize_benchmark_results(results),
            metadata=contract_metadata("benchmark_results"),
        )
    )



def benchmark_gate_report(root: Path) -> dict:
    report = build_benchmark_report(root)
    total = report["total"]
    passed_count = report["passed"]
    return asdict(
        BenchmarkGateResult(
            ok=True,
            passed=passed_count == total,
            total=total,
            passed_count=passed_count,
            failed_count=total - passed_count,
            summary=report["summary"],
            policy=benchmark_gate_policy(),
            metadata=contract_metadata("benchmark_gate"),
        )
    )



def write_benchmark_report(root: Path, output_path: Path) -> dict:
    report = build_benchmark_report(root)
    output_path.write_text(__import__('json').dumps(report, indent=2), encoding='utf-8')
    return success_result({"output": str(output_path), "report": report}, contract="benchmark_report")
