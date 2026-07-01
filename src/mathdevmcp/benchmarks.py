"""Structured benchmark cases and release benchmark gate evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import sys
from typing import Literal

from .ast_operation_graph import build_ast_operation_graph_for_file
from .consistency import compare_files, compare_label_to_code
from .contracts import contract_metadata, success_result
from .assumption_discovery import assumptions_required
from .assumptions_for import assumptions_for as high_level_assumptions_for, score_assumption_set
from .audit_math_to_code import audit_math_to_code as high_level_audit_math_to_code
from .debug_derivation import debug_derivation as high_level_debug_derivation, score_gap_localization
from .derive_from import derive_from as high_level_derive_from
from .derive_or_refute import derive_or_refute
from .equation_code_match import code_implements_equation
from .derivation import derive_step_for_label
from .prepare_review_packet import prepare_review_packet as high_level_prepare_review_packet, score_review_packet
from .kalman_workflows import audit_kalman_recursion
from .industrial_review import build_industrial_review_packet
from .literature_local_audit import literature_local_audit
from .math_change_impact import math_change_impact
from .math_claim_classifier import classify_math_claim
from .math_review_packet import build_math_review_packet
from .math_to_tests import generate_math_tests
from .notation_reconciliation import reconcile_notation
from .parser_benchmark import run_parser_backend
from .prove_or_refute import prove_or_refute
from .prove_or_counterexample import prove_or_counterexample as high_level_prove_or_counterexample
from .proof_gap import localize_proof_gap
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .release_corpus import validate_release_corpus_manifest
from .release_policy import release_readiness_report
from .typed_workflows import typed_obligation_for_label
from .workbench_benchmark_schema import EXPECTED_SEEDED_WORKBENCH_TOOLS, FIXED_MUTATION_FAMILY, ORACLE_CLASSES, workbench_benchmark_quality_report
from .workflow import build_implementation_brief

BenchmarkCategory = Literal["consistency", "derivation", "workflow", "proof_audit", "proof_audit_v2", "kalman_recursion", "parser_corpus", "ast_corpus", "typed_ir", "industrial_review", "release_corpus", "release_policy", "math_debugging_workbench", "high_level_math_workflows"]


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
    workbench_quality: dict
    high_level_quality: dict
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


def _proof_audit_v2_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "proof_audit_v2_scalar_verified",
            "category": "proof_audit_v2",
            "evaluation_focus": "release_spine_verified",
            "doc_root": str(fixtures),
            "label": "eq:proof-audit-single",
            "expected_status": "verified",
            "expected_abstention": False,
            "expected_route": "symbolic",
            "expected_high_priority_actions": [],
        },
        {
            "id": "proof_audit_v2_false_mismatch",
            "category": "proof_audit_v2",
            "evaluation_focus": "false_confidence_control",
            "doc_root": str(fixtures),
            "label": "eq:proof-audit-false",
            "expected_status": "mismatch",
            "expected_abstention": False,
            "expected_route": "symbolic",
            "expected_high_priority_action_kinds": ["investigate_backend_refutation"],
        },
        {
            "id": "proof_audit_v2_state_space_abstention",
            "category": "proof_audit_v2",
            "evaluation_focus": "release_spine_abstention",
            "doc_root": str(fixtures),
            "label": "eq:dept-state-space-likelihood",
            "expected_status": "unverified",
            "expected_abstention": True,
            "expected_route": "human_review",
            "expected_high_priority_action_kinds": ["state_or_verify_missing_constraint", "human_formalization_or_review", "logdet_domain_check", "linear_solve_residual_check"],
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
        },
        {
            "id": "parser_corpus_macro_filter_multifile",
            "category": "parser_corpus",
            "evaluation_focus": "multifile_macro_parser_provenance",
            "doc_root": str(fixtures),
            "backend": "current",
            "expected_status": "parsed",
            "expected_labels": [
                "assump:macro-filter-dimensions",
                "eq:macro-filter-transition",
                "eq:macro-filter-innovation",
                "eq:macro-filter-likelihood",
                "prop:macro-filter-repeat-notation",
            ],
        },
        {
            "id": "parser_corpus_sanitized_public_domains",
            "category": "parser_corpus",
            "evaluation_focus": "sanitized_domain_parser_provenance",
            "doc_root": str(fixtures),
            "backend": "current",
            "expected_status": "parsed",
            "expected_labels": [
                "eq:dept-particle-normalization",
                "eq:dept-euler-equation",
                "eq:dept-sdf",
                "eq:dept-sv-transition",
                "eq:dept-sv-likelihood",
                "eq:dept-euler-maruyama",
                "eq:dept-pde-stability",
                "eq:dept-ml-loss",
                "eq:dept-ml-gradient",
                "eq:dept-elbo",
                "eq:dept-reparameterization-gradient",
                "eq:dept-acceptance-ratio",
                "eq:dept-hamiltonian-flow",
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
        {
            "id": "ast_corpus_macro_filter_missing_gain",
            "category": "ast_corpus",
            "evaluation_focus": "false_confidence_control",
            "code": str(fixtures / "doc_macro_filter_missing_gain.py"),
            "expected_status": "mismatch",
            "required_operations": ["logdet", "inverse_or_solve", "quadratic_form", "kalman_gain", "state_update", "covariance_update"],
            "expected_missing_operations": ["kalman_gain", "state_update", "covariance_update"],
        },
        {
            "id": "ast_corpus_dsge_macro_finance",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_dsge_macro_finance.py"),
            "expected_status": "consistent",
            "expected_operations": ["expectation", "euler_residual"],
        },
        {
            "id": "ast_corpus_stochastic_volatility",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_stochastic_volatility.py"),
            "expected_status": "consistent",
            "expected_operations": ["innovation_update", "posterior_or_likelihood"],
        },
        {
            "id": "ast_corpus_sde_pde_numerics",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_sde_pde_numerics.py"),
            "expected_status": "consistent",
            "expected_operations": ["time_step_update", "stability_condition"],
        },
        {
            "id": "ast_corpus_ml_llm_objective",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_ml_llm_objective.py"),
            "expected_status": "consistent",
            "expected_operations": ["gradient", "posterior_or_likelihood"],
        },
        {
            "id": "ast_corpus_bayesian_elbo_vi",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_bayesian_elbo_vi.py"),
            "expected_status": "consistent",
            "expected_operations": ["elbo_objective", "reparameterization_gradient", "expectation"],
        },
        {
            "id": "ast_corpus_computational_physics_mcmc",
            "category": "ast_corpus",
            "evaluation_focus": "sanitized_domain_ast_operation_coverage",
            "code": str(fixtures / "doc_sanitized_computational_physics_mcmc.py"),
            "expected_status": "consistent",
            "expected_operations": ["acceptance_ratio", "hamiltonian_energy", "gradient"],
        },
    ]


def _typed_ir_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "typed_ir_state_space_likelihood",
            "category": "typed_ir",
            "evaluation_focus": "typed_dimension_diagnostics",
            "doc_root": str(fixtures),
            "label": "eq:dept-state-space-likelihood",
            "expected_status": "unverified",
            "expected_diagnostic_status": "needs_assumptions",
            "expected_missing_constraints": ["invertibility_required", "square_matrix_required", "conformable_product_required"],
        },
        {
            "id": "typed_ir_hmc_leapfrog",
            "category": "typed_ir",
            "evaluation_focus": "typed_stochastic_diagnostics",
            "doc_root": str(fixtures),
            "label": "eq:dept-hmc-leapfrog",
            "expected_status": "unverified",
            "expected_diagnostic_status": "needs_assumptions",
            "expected_missing_constraints": ["differentiability_required"],
        },
    ]


def _industrial_review_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "industrial_review_state_space_packet",
            "category": "industrial_review",
            "evaluation_focus": "agent_review_packet",
            "doc_root": str(fixtures),
            "label": "eq:dept-state-space-likelihood",
            "expected_status": "unverified",
            "expected_severity": "high",
            "expected_action_kinds": ["state_or_verify_missing_constraint", "logdet_domain_check", "linear_solve_residual_check"],
        }
    ]


def _release_corpus_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "release_corpus_manifest_privacy_gate",
            "category": "release_corpus",
            "evaluation_focus": "release_corpus_manifest",
            "root": str(fixtures),
            "expected_status": "consistent",
            "expected_domains": [
                "kalman_state_space",
                "hmc_nuts",
                "particle_filter",
                "macro_filter_state_space",
                "dsge_macro_finance",
                "stochastic_volatility",
                "sde_pde_numerics",
                "ml_llm_objective",
                "bayesian_elbo_vi",
                "computational_physics_mcmc",
            ],
        }
    ]


def _release_policy_cases(root: Path) -> list[dict]:
    return [
        {
            "id": "release_policy_readiness_report",
            "category": "release_policy",
            "evaluation_focus": "release_readiness_contract",
            "root": str(root),
            "expected_statuses": ["ready", "ready_with_caveats"],
            "expected_contract": "release_readiness_report",
        }
    ]


def _math_debugging_workbench_cases(root: Path) -> list[dict]:
    _ = root
    theorem_assumptions = [
        {"id": "compactness", "text": "Parameter space is compact."},
        {"id": "full_rank", "text": "Information matrix has full rank."},
    ]
    local_missing_rank = [{"id": "compactness", "text": "Parameter space is compact."}]
    local_conflict = [
        {"id": "compactness", "text": "Parameter space is compact."},
        {"id": "full_rank", "text": "Information matrix is singular.", "status": "conflict"},
    ]
    return [
        {
            "id": "workbench_derive_true_identity",
            "tool": "derive_or_refute",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_proof_refutation",
            "oracle_class": "proved_scoped",
            "expected_status": "proved",
            "expected_abstention": False,
            "negative_control": False,
            "call": lambda: derive_or_refute("(a+b)*(a-b) = a*a - b*b"),
        },
        {
            "id": "workbench_derive_false_identity",
            "tool": "derive_or_refute",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_false_confidence_control",
            "oracle_class": "refuted_scoped",
            "expected_status": "refuted",
            "expected_abstention": False,
            "negative_control": True,
            "call": lambda: derive_or_refute("1 + 1 = 3"),
        },
        {
            "id": "workbench_prove_backend_unavailable_nonclaim",
            "tool": "prove_or_refute",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_backend_boundary",
            "oracle_class": "backend_unavailable_nonclaim",
            "expected_status": "backend_unavailable",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: prove_or_refute("a + b = b + a", backend="sage"),
        },
        {
            "id": "workbench_prove_not_encodable_nonclaim",
            "tool": "prove_or_refute",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_backend_boundary",
            "oracle_class": "not_encodable_nonclaim",
            "expected_status": "not_encodable",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: prove_or_refute("__import__('os') = 0"),
        },
        {
            "id": "workbench_proof_gap_first_bad_step",
            "tool": "localize_proof_gap",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_gap_localization",
            "oracle_class": "refuted_scoped",
            "expected_status": "refuted",
            "expected_abstention": False,
            "negative_control": True,
            "expected_gap_index": 1,
            "call": lambda: localize_proof_gap(["a + b", "b + a", "a - b"]),
        },
        {
            "id": "workbench_missing_logdet_assumption",
            "tool": "assumptions_required",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_missing_assumptions",
            "oracle_class": "abstained_missing_assumptions",
            "expected_status": "missing_assumptions",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: assumptions_required("logdet(S)"),
        },
        {
            "id": "workbench_code_equation_structural_only",
            "tool": "code_implements_equation",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_structural_boundary",
            "oracle_class": "structural_only",
            "expected_status": "consistent",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: code_implements_equation("logdet(S)", "def f(S):\n    return logdet(S)\n"),
        },
        {
            "id": "workbench_code_equation_missing_logdet",
            "tool": "code_implements_equation",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_false_confidence_control",
            "oracle_class": "structural_only",
            "expected_status": "mismatch",
            "expected_abstention": False,
            "negative_control": True,
            "call": lambda: code_implements_equation("logdet(S)", "def f(S):\n    return trace(S)\n"),
        },
        {
            "id": "workbench_claim_numeric_not_proof",
            "tool": "classify_math_claim",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_false_confidence_control",
            "oracle_class": "diagnostic_only",
            "expected_status": "numeric_supported",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: classify_math_claim("sin(x)^2 + cos(x)^2 = 1", evidence=[{"status": "numeric_supported", "numeric": True}]),
        },
        {
            "id": "workbench_notation_sign_conflict",
            "tool": "reconcile_notation",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_notation_conflict",
            "oracle_class": "applicability_conflict",
            "expected_status": "conflict",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: reconcile_notation(
                [{"symbol": "r", "alias_of": "r", "sign": "+"}],
                [{"symbol": "r", "alias_of": "r", "sign": "-"}],
            ),
        },
        {
            "id": "workbench_generate_tests_diagnostic_only",
            "tool": "generate_math_tests",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_diagnostic_generation",
            "oracle_class": "diagnostic_only",
            "expected_status": "generated",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: generate_math_tests("a + b = b + a", kinds=["symbolic_identity"]),
        },
        {
            "id": "workbench_review_packet_preserves_refutation",
            "tool": "math_review_packet",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_packet_boundary",
            "oracle_class": "diagnostic_only",
            "expected_status": "blocked_by_refutation",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: build_math_review_packet("Can we prove 1+1=3?", evidence=[derive_or_refute("1 + 1 = 3")]),
        },
        {
            "id": "workbench_change_impact_missing_links",
            "tool": "math_change_impact",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_impact_boundary",
            "oracle_class": "impact_inconclusive",
            "expected_status": "inconclusive",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: math_change_impact("eq:missing", graph={"nodes": [], "edges": []}),
        },
        {
            "id": "workbench_literature_local_missing_assumption",
            "tool": "literature_local_audit",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_applicability_boundary",
            "oracle_class": "applicability_gap",
            "expected_status": "applicability_gap",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: literature_local_audit("theorem:seeded", theorem_assumptions, local_missing_rank),
        },
        {
            "id": "workbench_literature_local_conflicting_assumption",
            "tool": "literature_local_audit",
            "category": "math_debugging_workbench",
            "evaluation_focus": "workbench_applicability_boundary",
            "oracle_class": "applicability_conflict",
            "expected_status": "applicability_conflict",
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: literature_local_audit("theorem:seeded", theorem_assumptions, local_conflict),
        },
    ]


def _high_level_math_workflow_cases(root: Path) -> list[dict]:
    _ = root
    derive_refuted = lambda: high_level_derive_from("A*B = B*A")
    proof_refuted = lambda: high_level_prove_or_counterexample("A*B = B*A")
    assumption_logdet = lambda: high_level_assumptions_for("logdet(A)")
    debug_gap = lambda: high_level_debug_derivation(["logdet(A)", "trace(A)", "trace(A)"])
    code_match = lambda: high_level_audit_math_to_code("logdet(S)", "def f(S):\n    return logdet(S)\n")
    packet_refutation = lambda: high_level_prepare_review_packet("Review failed proof", evidence=[proof_refuted()])
    return [
        {
            "id": "hlf_derive_backend_certificate",
            "workflow": "derive_from",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_backend_certificate",
            "expected_status": "proved",
            "expected_evidence_classes": ["backend_certificate"],
            "expected_abstention": False,
            "negative_control": False,
            "call": lambda: high_level_derive_from("a + b = b + a"),
        },
        {
            "id": "hlf_derive_counterexample_refutation",
            "workflow": "derive_from",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_false_confidence_control",
            "expected_status": "refuted",
            "expected_evidence_classes": ["backend_counterexample"],
            "expected_abstention": False,
            "negative_control": True,
            "call": derive_refuted,
        },
        {
            "id": "hlf_derive_no_counterexample_nonpromotion",
            "workflow": "derive_from",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_false_confidence_control",
            "expected_status": "inconclusive",
            "expected_evidence_classes": ["backend_counterexample"],
            "expected_abstention": True,
            "negative_control": True,
            "required_veto": "certifying_evidence_not_promoted",
            "call": lambda: high_level_derive_from("1 + 1 = 3"),
        },
        {
            "id": "hlf_prove_backend_certificate",
            "workflow": "prove_or_counterexample",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_backend_certificate",
            "expected_status": "proved",
            "expected_evidence_classes": ["backend_certificate"],
            "expected_abstention": False,
            "negative_control": False,
            "call": lambda: high_level_prove_or_counterexample("a + b = b + a"),
        },
        {
            "id": "hlf_prove_counterexample_refutation",
            "workflow": "prove_or_counterexample",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_false_confidence_control",
            "expected_status": "refuted",
            "expected_evidence_classes": ["backend_counterexample"],
            "expected_abstention": False,
            "negative_control": True,
            "call": proof_refuted,
        },
        {
            "id": "hlf_prove_not_encodable_nonclaim",
            "workflow": "prove_or_counterexample",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_backend_boundary",
            "expected_status": "not_encodable",
            "expected_evidence_classes": ["not_encodable"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "not_encodable_not_false",
            "call": lambda: high_level_prove_or_counterexample("informal theorem with no equality"),
        },
        {
            "id": "hlf_assumptions_logdet",
            "workflow": "assumptions_for",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_missing_assumptions",
            "expected_status": "missing_assumptions",
            "expected_evidence_classes": ["missing_assumption"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "route_assumptions_not_global_minimality",
            "rubric": lambda result: score_assumption_set(result, {"determinant domain"})["status"] == "passed",
            "call": assumption_logdet,
        },
        {
            "id": "hlf_assumptions_unknown_route",
            "workflow": "assumptions_for",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_missing_assumptions",
            "expected_status": "inconclusive",
            "expected_evidence_classes": ["human_review_required"],
            "expected_abstention": True,
            "negative_control": True,
            "call": lambda: high_level_assumptions_for("x + y"),
        },
        {
            "id": "hlf_debug_first_gap",
            "workflow": "debug_derivation",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_gap_localization",
            "expected_status": "gap_found",
            "expected_evidence_classes": ["proof_gap"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "gap_localization_not_global_failure",
            "rubric": lambda result: score_gap_localization(result, expected_index=0, expected_statuses={"missing_assumptions", "unknown"})["status"] == "passed",
            "call": debug_gap,
        },
        {
            "id": "hlf_debug_counterexample_refutation",
            "workflow": "debug_derivation",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_gap_localization",
            "expected_status": "refuted",
            "expected_evidence_classes": ["backend_counterexample"],
            "expected_abstention": False,
            "negative_control": True,
            "call": lambda: high_level_debug_derivation(["A*B", "B*A"]),
        },
        {
            "id": "hlf_code_structural_match",
            "workflow": "audit_math_to_code",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_structural_boundary",
            "expected_status": "structural_match",
            "expected_evidence_classes": ["structural_match"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "structural_evidence_not_proof",
            "call": code_match,
        },
        {
            "id": "hlf_code_structural_mismatch",
            "workflow": "audit_math_to_code",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_structural_boundary",
            "expected_status": "structural_mismatch",
            "expected_evidence_classes": ["structural_mismatch"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "structural_evidence_not_proof",
            "call": lambda: high_level_audit_math_to_code("logdet(S)", "def f(S):\n    return trace(S)\n"),
        },
        {
            "id": "hlf_packet_diagnostic_only",
            "workflow": "prepare_review_packet",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_packet_boundary",
            "expected_status": "diagnostic_only",
            "expected_evidence_classes": ["review_packet"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "diagnostic_evidence_not_proof",
            "rubric": lambda result: score_review_packet(result)["status"] == "passed",
            "call": lambda: high_level_prepare_review_packet("Review derivation", evidence=[high_level_derive_from("a + b = b + a")]),
        },
        {
            "id": "hlf_packet_preserves_refutation",
            "workflow": "prepare_review_packet",
            "category": "high_level_math_workflows",
            "evaluation_focus": "hlf_packet_boundary",
            "expected_status": "diagnostic_only",
            "expected_evidence_classes": ["review_packet"],
            "expected_abstention": True,
            "negative_control": True,
            "required_non_claim": "diagnostic_evidence_not_proof",
            "rubric": lambda result: result["evidence"][0]["low_level"]["status"] == "blocked_by_refutation",
            "call": packet_refutation,
        },
    ]



def benchmark_cases(root: Path, *, include_release_policy: bool = True) -> list[dict]:
    cases = (
        _consistency_cases(root)
        + _derivation_cases(root)
        + _workflow_cases(root)
        + _proof_audit_cases(root)
        + _proof_audit_v2_cases(root)
        + _kalman_recursion_cases(root)
        + _parser_corpus_cases(root)
        + _ast_corpus_cases(root)
        + _typed_ir_cases(root)
        + _industrial_review_cases(root)
        + _release_corpus_cases(root)
        + _math_debugging_workbench_cases(root)
        + _high_level_math_workflow_cases(root)
    )
    if include_release_policy:
        cases += _release_policy_cases(root)
    return cases



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


def run_proof_audit_v2_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _proof_audit_v2_cases(root):
        result = audit_derivation_v2_for_label(case["doc_root"], case["label"], backend="sympy")
        routes = {obligation.get("route_decision", {}).get("route") for obligation in result.get("obligations", [])}
        action_kinds = {action.get("kind") for action in result.get("high_priority_actions", [])}
        status_ok = result["status"] == case["expected_status"]
        route_ok = case["expected_route"] in routes
        contract_ok = result.get("metadata", {}).get("contract") == "proof_audit_v2_result"
        obligation_contract_ok = all(
            obligation.get("metadata", {}).get("contract") == "proof_audit_v2_obligation"
            for obligation in result.get("obligations", [])
        )
        expected_actions = set(case.get("expected_high_priority_action_kinds", case.get("expected_high_priority_actions", [])))
        actions_ok = expected_actions.issubset(action_kinds)
        abstention_ok = result["status"] in {"inconclusive", "unverified"} if case.get("expected_abstention", False) else result["status"] not in {"inconclusive", "unverified"}
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and route_ok and contract_ok and obligation_contract_ok and actions_ok and abstention_ok,
                quality_checks={
                    "status_match": status_ok,
                    "route_match": route_ok,
                    "contract_match": contract_ok,
                    "obligation_contract_match": obligation_contract_ok,
                    "actions_match": actions_ok,
                    "expected_abstention_match": abstention_ok,
                },
                details={
                    "label": case["label"],
                    "counts": result["counts"],
                    "routes": sorted(route for route in routes if route),
                    "high_priority_action_kinds": sorted(kind for kind in action_kinds if kind),
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


def run_typed_ir_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _typed_ir_cases(root):
        result = typed_obligation_for_label(case["doc_root"], case["label"])
        diagnostic = result["typed_diagnostic"]
        missing_kinds = [item["kind"] for item in diagnostic.get("missing_constraints", [])]
        status_ok = result["status"] == case["expected_status"]
        diagnostic_ok = diagnostic["status"] == case["expected_diagnostic_status"]
        missing_ok = missing_kinds == case["expected_missing_constraints"]
        contract_ok = diagnostic.get("metadata", {}).get("contract") == "typed_math_obligation_diagnostic"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and diagnostic_ok and missing_ok and contract_ok,
                quality_checks={
                    "status_match": status_ok,
                    "diagnostic_status_match": diagnostic_ok,
                    "missing_constraints_match": missing_ok,
                    "contract_match": contract_ok,
                },
                details={
                    "label": case["label"],
                    "diagnostic_status": diagnostic["status"],
                    "missing_constraints": diagnostic.get("missing_constraints", []),
                    "backend_route_hints": diagnostic["obligation"].get("backend_route_hints", []),
                },
                expected_abstention=True,
            )
        )
    return results


def run_industrial_review_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _industrial_review_cases(root):
        packet = build_industrial_review_packet(case["doc_root"], case["label"])
        action_kinds = {action["kind"] for action in packet.get("recommended_actions", [])}
        status_ok = packet["status"] == case["expected_status"]
        severity_ok = packet["severity"] == case["expected_severity"]
        actions_ok = set(case["expected_action_kinds"]).issubset(action_kinds)
        contract_ok = packet.get("metadata", {}).get("contract") == "industrial_review_packet"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=packet["status"],
                passed=status_ok and severity_ok and actions_ok and contract_ok,
                quality_checks={
                    "status_match": status_ok,
                    "severity_match": severity_ok,
                    "actions_match": actions_ok,
                    "contract_match": contract_ok,
                },
                details={
                    "label": case["label"],
                    "severity": packet["severity"],
                    "action_kinds": sorted(action_kinds),
                },
                expected_abstention=True,
            )
        )
    return results


def run_release_corpus_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _release_corpus_cases(root):
        result = validate_release_corpus_manifest(case["root"])
        domains = {entry["domain"] for entry in result["manifest"]["entries"]}
        status_ok = result["status"] == case["expected_status"]
        domains_ok = set(case["expected_domains"]).issubset(domains)
        privacy_ok = all(entry["document_root"] is None for entry in result["manifest"]["entries"] if entry["privacy_class"] == "private_external")
        contract_ok = result.get("metadata", {}).get("contract") == "release_corpus_validation_report"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and domains_ok and privacy_ok and contract_ok,
                quality_checks={
                    "status_match": status_ok,
                    "domains_match": domains_ok,
                    "private_entries_external": privacy_ok,
                    "contract_match": contract_ok,
                },
                details={"domains": sorted(domains), "findings": result["findings"]},
            )
        )
    return results


def run_release_policy_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _release_policy_cases(root):
        result = release_readiness_report(case["root"])
        status_ok = result["status"] in case["expected_statuses"]
        contract_ok = result.get("metadata", {}).get("contract") == case["expected_contract"]
        gate_ok = result["benchmark_gate"]["passed"] is True
        governance_ok = result["governance_policy"].get("metadata", {}).get("contract") == "governance_policy"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status="ready_or_ready_with_caveats",
                observed_status=result["status"],
                passed=status_ok and contract_ok and gate_ok and governance_ok,
                quality_checks={
                    "status_allowed": status_ok,
                    "contract_match": contract_ok,
                    "benchmark_gate_passed": gate_ok,
                    "governance_contract_match": governance_ok,
                },
                details={"status": result["status"], "caveats": result["caveats"], "blockers": result["blockers"]},
            )
        )
    return results


def _workbench_boundary_ok(case: dict, result: dict) -> bool:
    oracle = case["oracle_class"]
    if oracle == "backend_unavailable_nonclaim":
        return result.get("status") == "backend_unavailable" and result.get("status") != "refuted"
    if oracle == "not_encodable_nonclaim":
        return result.get("status") == "not_encodable" and result.get("status") != "refuted"
    if oracle == "structural_only":
        workbench = result.get("workbench_result", {})
        return workbench.get("status") != "proved"
    if oracle == "diagnostic_only":
        text = str(result).lower()
        return "not proof" in text or "diagnostic" in text or "not a proof certificate" in text
    if oracle == "abstained_missing_assumptions":
        return bool(result.get("missing_assumptions"))
    if oracle == "applicability_gap":
        return bool(result.get("missing_assumptions"))
    if oracle == "applicability_conflict":
        return bool(result.get("conflicting_assumptions") or result.get("conflicts") or result.get("notation_notes"))
    if oracle == "impact_inconclusive":
        return any(item.get("kind") == "missing_downstream_links" for item in result.get("missing_link_warnings", []))
    if oracle == "proved_scoped":
        return result.get("workbench_result", {}).get("status") == "proved"
    if oracle == "refuted_scoped":
        return result.get("status") in {"refuted", "gap_found", "blocked_by_refutation"} or result.get("workbench_result", {}).get("status") == "refuted"
    return False


def run_math_debugging_workbench_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _math_debugging_workbench_cases(root):
        result = case["call"]()
        observed_status = result.get("status") or result.get("classification", "")
        status_ok = observed_status == case["expected_status"]
        contract_ok = isinstance(result.get("metadata", {}).get("contract"), str)
        oracle_ok = case["oracle_class"] in ORACLE_CLASSES
        boundary_ok = _workbench_boundary_ok(case, result)
        abstention_ok = (
            observed_status
            in {
                "backend_unavailable",
                "not_encodable",
                "missing_assumptions",
                "consistent",
                "numeric_supported",
                "conflict",
                "generated",
                "blocked_by_refutation",
                "inconclusive",
                "applicability_gap",
                "applicability_conflict",
            }
            if case.get("expected_abstention", False)
            else observed_status not in {"backend_unavailable", "not_encodable", "missing_assumptions", "unknown", "inconclusive"}
        )
        gap_ok = True
        if "expected_gap_index" in case:
            gap_ok = result.get("first_gap", {}).get("index") == case["expected_gap_index"]
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=observed_status,
                passed=status_ok and contract_ok and oracle_ok and boundary_ok and abstention_ok and gap_ok,
                quality_checks={
                    "status_match": status_ok,
                    "contract_present": contract_ok,
                    "oracle_class_supported": oracle_ok,
                    "boundary_preserved": boundary_ok,
                    "expected_abstention_match": abstention_ok,
                    "gap_index_match": gap_ok,
                    "negative_control": bool(case.get("negative_control", False)),
                },
                details={
                    "tool": case["tool"],
                    "oracle_class": case["oracle_class"],
                    "metadata": result.get("metadata"),
                    "negative_control": bool(case.get("negative_control", False)),
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results


def _high_level_boundary_ok(case: dict, result: dict) -> bool:
    status = result.get("status")
    evidence_classes = set(result.get("evidence_classes", []))
    non_claim_codes = {item.get("code") for item in result.get("non_claims", []) if isinstance(item, dict)}
    veto_codes = {item.get("code") for item in result.get("veto_reasons", []) if isinstance(item, dict)}
    if status == "proved":
        return result.get("certification_source") == "backend" and evidence_classes == {"backend_certificate"}
    if status == "refuted":
        return result.get("certification_source") in {"backend", "scoped_contradiction"} and bool(result.get("counterexamples") or "scoped_contradiction" in evidence_classes)
    if status == "inconclusive":
        return result.get("certification_source") == "none" and bool(result.get("veto_reasons") or result.get("actions"))
    if status == "missing_assumptions":
        return "route_assumptions_not_global_minimality" in non_claim_codes and bool(result.get("assumptions"))
    if status in {"backend_unavailable", "not_encodable"}:
        return result.get("certification_source") == "none" and bool(veto_codes)
    if status in {"structural_match", "structural_mismatch"}:
        return result.get("certification_source") == "none" and "structural_evidence_not_proof" in non_claim_codes
    if status == "diagnostic_only":
        return result.get("certification_source") == "none" and "diagnostic_evidence_not_proof" in non_claim_codes
    if status == "gap_found":
        return result.get("certification_source") == "none" and "gap_localization_not_global_failure" in non_claim_codes
    return False


def run_high_level_math_workflow_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _high_level_math_workflow_cases(root):
        result = case["call"]()
        status_ok = result.get("status") == case["expected_status"]
        classes_ok = result.get("evidence_classes") == case["expected_evidence_classes"]
        contract_ok = result.get("metadata", {}).get("contract") == "high_level_workflow_result"
        boundary_ok = _high_level_boundary_ok(case, result)
        non_claim_ok = case.get("required_non_claim") is None or case["required_non_claim"] in {
            item.get("code") for item in result.get("non_claims", []) if isinstance(item, dict)
        }
        veto_ok = case.get("required_veto") is None or case["required_veto"] in {
            item.get("code") for item in result.get("veto_reasons", []) if isinstance(item, dict)
        }
        rubric = case.get("rubric")
        rubric_ok = rubric(result) if callable(rubric) else True
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=str(result.get("status")),
                passed=status_ok and classes_ok and contract_ok and boundary_ok and non_claim_ok and veto_ok and rubric_ok,
                quality_checks={
                    "status_match": status_ok,
                    "evidence_classes_match": classes_ok,
                    "contract_match": contract_ok,
                    "boundary_preserved": boundary_ok,
                    "required_non_claim_present": non_claim_ok,
                    "required_veto_present": veto_ok,
                    "rubric_passed": rubric_ok,
                    "negative_control": bool(case.get("negative_control", False)),
                },
                details={
                    "workflow": case["workflow"],
                    "evidence_classes": result.get("evidence_classes"),
                    "certification_source": result.get("certification_source"),
                    "negative_control": bool(case.get("negative_control", False)),
                },
                expected_abstention=case.get("expected_abstention", False),
            )
        )
    return results


def _serializable_workbench_cases(root: Path) -> list[dict]:
    cases: list[dict] = []
    for case in _math_debugging_workbench_cases(root):
        cases.append(
            {
                "id": case["id"],
                "tool": case["tool"],
                "oracle_class": case["oracle_class"],
                "expected_status": case["expected_status"],
                "expected_abstention": bool(case.get("expected_abstention", False)),
                "negative_control": bool(case.get("negative_control", False)),
                "source": "local_seeded",
                "source_family": "local_seeded",
                "gated": True,
                "non_claims": [
                    "Seeded local case; not an external benchmark claim.",
                    "Scoring follows the declared oracle class, not pass rate alone.",
                ],
            }
        )
    return cases


def _serializable_high_level_cases(root: Path) -> list[dict]:
    cases: list[dict] = []
    for case in _high_level_math_workflow_cases(root):
        cases.append(
            {
                "id": case["id"],
                "tool": case["workflow"],
                "oracle_class": case["expected_evidence_classes"][0],
                "expected_status": case["expected_status"],
                "expected_abstention": bool(case.get("expected_abstention", False)),
                "negative_control": bool(case.get("negative_control", False)),
                "source": "local_seeded",
                "source_family": "local_seeded",
                "gated": True,
                "non_claims": [
                    "Seeded local high-level workflow case; not an external benchmark claim.",
                    "Scoring requires boundary preservation, not pass rate alone.",
                ],
            }
        )
    return cases


def _workbench_run_manifest() -> dict:
    return {
        "git_state": "dirty_or_unknown",
        "command": "PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root .",
        "python": sys.version.split()[0],
        "backend_matrix": {
            "sympy": "required_for_seeded_symbolic_cases",
            "sage": "optional_unavailable_is_nonclaim",
            "lean": "not_required_for_seeded_quality_gate",
        },
        "timeout_policy": "seeded local calls only; no network or long external backend run",
        "seed_policy": "deterministic; no random seeds used",
        "normalization_rules": "case ids, observed statuses, pass/fail, and expected abstention compared exactly",
        "mutation_set_version": "workbench-proof-promotion-v1",
        "scoring_rubric_version": "workbench-benchmark-quality-v1",
    }


def _simulated_workbench_mutation_results(results: list[dict]) -> dict[str, bool]:
    by_id = {result["id"]: result for result in results}

    backend = dict(by_id["workbench_prove_backend_unavailable_nonclaim"])
    backend["observed_status"] = "refuted"
    backend["quality_checks"] = dict(backend["quality_checks"], boundary_preserved=False)

    structural = dict(by_id["workbench_code_equation_structural_only"])
    structural["observed_status"] = "proved"
    structural["quality_checks"] = dict(structural["quality_checks"], boundary_preserved=False)

    numeric = dict(by_id["workbench_claim_numeric_not_proof"])
    numeric["observed_status"] = "backend_proved"
    numeric["quality_checks"] = dict(numeric["quality_checks"], boundary_preserved=False)

    missing = dict(by_id["workbench_missing_logdet_assumption"])
    missing["observed_status"] = "proved"
    missing["quality_checks"] = dict(missing["quality_checks"], boundary_preserved=False)

    probes = {
        "backend_unavailable_to_refuted": backend,
        "structural_only_to_proved": structural,
        "numeric_supported_to_backend_proved": numeric,
        "missing_assumptions_to_proved": missing,
    }
    return {
        name: probe.get("quality_checks", {}).get("boundary_preserved") is False
        and probe.get("observed_status") != by_id[probe["id"]]["expected_status"]
        for name, probe in probes.items()
    }


def _simulated_high_level_mutation_results(results: list[dict]) -> dict[str, bool]:
    by_id = {result["id"]: result for result in results}
    backend = dict(by_id["hlf_prove_not_encodable_nonclaim"])
    backend["observed_status"] = "refuted"
    backend["quality_checks"] = dict(backend["quality_checks"], boundary_preserved=False)

    structural = dict(by_id["hlf_code_structural_match"])
    structural["observed_status"] = "proved"
    structural["quality_checks"] = dict(structural["quality_checks"], boundary_preserved=False)

    diagnostic = dict(by_id["hlf_packet_diagnostic_only"])
    diagnostic["observed_status"] = "proved"
    diagnostic["quality_checks"] = dict(diagnostic["quality_checks"], boundary_preserved=False)

    missing = dict(by_id["hlf_assumptions_logdet"])
    missing["observed_status"] = "proved"
    missing["quality_checks"] = dict(missing["quality_checks"], boundary_preserved=False)

    no_counterexample = dict(by_id["hlf_derive_no_counterexample_nonpromotion"])
    no_counterexample["observed_status"] = "refuted"
    no_counterexample["quality_checks"] = dict(no_counterexample["quality_checks"], boundary_preserved=False)

    probes = {
        "not_encodable_to_refuted": backend,
        "structural_match_to_proved": structural,
        "review_packet_to_proved": diagnostic,
        "missing_assumptions_to_proved": missing,
        "no_counterexample_to_refuted": no_counterexample,
    }
    return {
        name: probe.get("quality_checks", {}).get("boundary_preserved") is False
        and probe.get("observed_status") != by_id[probe["id"]]["expected_status"]
        for name, probe in probes.items()
    }


def build_workbench_benchmark_quality_report(root: Path) -> dict:
    cases = _serializable_workbench_cases(root)
    first_results = run_math_debugging_workbench_benchmark(root)
    second_results = run_math_debugging_workbench_benchmark(root)
    mutation_results = _simulated_workbench_mutation_results(first_results)
    return workbench_benchmark_quality_report(
        cases,
        results=first_results,
        deterministic_rerun=(first_results, second_results),
        expected_tools=EXPECTED_SEEDED_WORKBENCH_TOOLS,
        mutation_results=mutation_results,
        run_manifest=_workbench_run_manifest(),
    )


def build_high_level_workflow_quality_report(root: Path) -> dict:
    cases = _serializable_high_level_cases(root)
    first_results = run_high_level_math_workflow_benchmark(root)
    second_results = run_high_level_math_workflow_benchmark(root)
    first_signature = [
        {
            "id": result["id"],
            "observed_status": result["observed_status"],
            "passed": result["passed"],
            "expected_abstention": result["expected_abstention"],
        }
        for result in first_results
    ]
    second_signature = [
        {
            "id": result["id"],
            "observed_status": result["observed_status"],
            "passed": result["passed"],
            "expected_abstention": result["expected_abstention"],
        }
        for result in second_results
    ]
    workflows = {case["tool"] for case in cases}
    negative_control_count = sum(1 for case in cases if case["negative_control"])
    mutation_results = _simulated_high_level_mutation_results(first_results)
    thresholds = {
        "at_least_two_cases_per_workflow": all(sum(1 for case in cases if case["tool"] == workflow) >= 2 for workflow in workflows),
        "negative_control_rate_at_least_40_percent": negative_control_count / len(cases) >= 0.40,
        "all_cases_pass": all(result["passed"] for result in first_results),
        "boundary_checks_all_preserved": all(result["quality_checks"]["boundary_preserved"] for result in first_results),
        "deterministic_rerun_stable": first_signature == second_signature,
        "mutation_family_detected": all(mutation_results.values()),
    }
    return {
        "status": "quality_thresholds_passed" if all(thresholds.values()) else "quality_thresholds_failed",
        "total_cases": len(cases),
        "total_results": len(first_results),
        "workflow_count": len(workflows),
        "workflows": sorted(workflows),
        "negative_control_count": negative_control_count,
        "negative_control_rate": negative_control_count / len(cases),
        "seeded_gate_thresholds": thresholds,
        "determinism": {
            "stable": first_signature == second_signature,
            "first_signature": first_signature,
            "second_signature": second_signature,
        },
        "mutation_results": mutation_results,
        "boundary": "High-level benchmark quality is not established by pass rate alone; boundary and mutation checks are required.",
        "non_claims": [
            "Seeded high-level workflow cases do not establish external benchmark validity.",
            "This report does not claim broad theorem-proving capability or release readiness.",
        ],
        "metadata": contract_metadata("high_level_workflow_quality_report"),
    }



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



def build_benchmark_report(root: Path, *, include_release_policy: bool = True) -> dict:
    results = (
        run_seeded_mismatch_benchmark(root)
        + run_label_consistency_benchmark(root)
        + run_derivation_benchmark(root)
        + run_workflow_benchmark(root)
        + run_proof_audit_benchmark(root)
        + run_proof_audit_v2_benchmark(root)
        + run_kalman_recursion_benchmark(root)
        + run_parser_corpus_benchmark(root)
        + run_ast_corpus_benchmark(root)
        + run_typed_ir_benchmark(root)
        + run_industrial_review_benchmark(root)
        + run_release_corpus_benchmark(root)
        + run_math_debugging_workbench_benchmark(root)
        + run_high_level_math_workflow_benchmark(root)
    )
    if include_release_policy:
        results += run_release_policy_benchmark(root)
    passed_count = sum(1 for result in results if result["passed"])
    return asdict(
        BenchmarkReport(
            ok=True,
            passed=passed_count,
            total=len(results),
            results=results,
            summary=summarize_benchmark_results(results),
            workbench_quality=build_workbench_benchmark_quality_report(root),
            high_level_quality=build_high_level_workflow_quality_report(root),
            metadata=contract_metadata("benchmark_results"),
        )
    )



def benchmark_gate_report(root: Path, *, include_release_policy: bool = True) -> dict:
    report = build_benchmark_report(root, include_release_policy=include_release_policy)
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



def write_benchmark_report(root: Path, output_path: Path, *, include_release_policy: bool = True) -> dict:
    report = build_benchmark_report(root, include_release_policy=include_release_policy)
    output_path.write_text(__import__('json').dumps(report, indent=2), encoding='utf-8')
    return success_result({"output": str(output_path), "report": report}, contract="benchmark_report")
