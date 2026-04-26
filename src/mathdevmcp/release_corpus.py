from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .contracts import attach_contract


@dataclass(frozen=True)
class ReleaseCorpusEntry:
    id: str
    domain: str
    privacy_class: str
    document_root: str | None
    code_roots: list[str]
    expected_labels: list[str]
    expected_operations: list[str]
    expected_abstentions: list[str]
    seeded_false_confidence_cases: list[str]
    required_parser_backends: list[str]
    release_gate_enabled: bool
    notes: str


def release_corpus_manifest(root: str | Path | None = None) -> dict:
    base = Path(root) if root is not None else Path("benchmarks/fixtures")
    entries = [
        ReleaseCorpusEntry(
            "kalman_state_space_extended",
            "kalman_state_space",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-state-space-recursion", "eq:dept-state-space-likelihood"],
            ["logdet", "inverse_or_solve", "quadratic_form", "prediction_update", "covariance_update"],
            ["eq:dept-state-space-likelihood"],
            ["doc_department_state_space_missing_solve.py"],
            ["current"],
            True,
            "Existing sanitized state-space fixtures exercise parser, AST, typed IR, and proof-audit v2 abstention.",
        ),
        ReleaseCorpusEntry(
            "hmc_nuts_leapfrog",
            "hmc_nuts",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-hmc-leapfrog", "eq:dept-hmc-hamiltonian"],
            ["gradient", "leapfrog_update", "hamiltonian_energy"],
            ["eq:dept-hmc-leapfrog"],
            ["hmc_missing_gradient_seed"],
            ["current"],
            True,
            "Sanitized HMC fixtures cover leapfrog and Hamiltonian structure without claiming full NUTS correctness.",
        ),
        ReleaseCorpusEntry(
            "particle_filter_logsumexp",
            "particle_filter",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-particle-normalization"],
            ["logsumexp", "particle_normalization"],
            ["particle_filter_weight_degeneracy_review"],
            ["particle_filter_missing_logsumexp_seed"],
            ["current"],
            False,
            "Code fixture exists; document label should be added before this domain becomes release-gated.",
        ),
        ReleaseCorpusEntry(
            "dsge_macro_finance_euler",
            "dsge_macro_finance",
            "private_external",
            None,
            [],
            ["eq:private-euler-equation", "eq:private-sdf"],
            ["expectation", "euler_residual"],
            ["private_calibration_assumption_review"],
            ["missing_discount_factor_seed"],
            ["current"],
            False,
            "Private corpus placeholder. Do not commit source documents.",
        ),
        ReleaseCorpusEntry(
            "stochastic_volatility_likelihood",
            "stochastic_volatility",
            "private_external",
            None,
            [],
            ["eq:private-sv-transition", "eq:private-sv-likelihood"],
            ["logdet", "innovation_update", "posterior_or_likelihood"],
            ["latent_volatility_prior_review"],
            ["missing_jacobian_seed"],
            ["current"],
            False,
            "Private/sanitized fixture still needed.",
        ),
        ReleaseCorpusEntry(
            "sde_pde_numerics",
            "sde_pde_numerics",
            "private_external",
            None,
            [],
            ["eq:private-euler-maruyama", "eq:private-pde-residual"],
            ["time_step_update", "stability_condition"],
            ["discretization_assumption_review"],
            ["unstable_step_size_seed"],
            ["current"],
            False,
            "Private/sanitized fixture still needed.",
        ),
        ReleaseCorpusEntry(
            "ml_llm_objective",
            "ml_llm_objective",
            "private_external",
            None,
            [],
            ["eq:private-loss", "eq:private-gradient"],
            ["gradient", "posterior_or_likelihood"],
            ["data_pipeline_assumption_review"],
            ["wrong_sign_gradient_seed"],
            ["current"],
            False,
            "Private/sanitized fixture still needed.",
        ),
        ReleaseCorpusEntry(
            "bayesian_elbo_vi",
            "bayesian_elbo_vi",
            "private_external",
            None,
            [],
            ["eq:private-elbo", "eq:private-reparameterization-gradient"],
            ["gradient", "expectation", "posterior_or_likelihood"],
            ["variational_family_assumption_review"],
            ["missing_entropy_seed"],
            ["current"],
            False,
            "Private/sanitized fixture still needed.",
        ),
        ReleaseCorpusEntry(
            "computational_physics_mcmc",
            "computational_physics_mcmc",
            "private_external",
            None,
            [],
            ["eq:private-acceptance-ratio", "eq:private-hamiltonian-flow"],
            ["hamiltonian_energy", "gradient", "leapfrog_update"],
            ["ergodicity_assumption_review"],
            ["missing_metropolis_correction_seed"],
            ["current"],
            False,
            "Private/sanitized fixture still needed.",
        ),
    ]
    return attach_contract({"entries": [asdict(entry) for entry in entries]}, "release_corpus_manifest")


def validate_release_corpus_manifest(root: str | Path | None = None) -> dict:
    manifest = release_corpus_manifest(root)
    findings: list[dict] = []
    for entry in manifest["entries"]:
        if entry["privacy_class"] == "private_external" and entry["document_root"] is not None:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "private_document_root_committed"})
        if entry["release_gate_enabled"] and not entry["expected_labels"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "missing_expected_labels"})
        if not entry["expected_abstentions"] and not entry["seeded_false_confidence_cases"]:
            findings.append({"entry": entry["id"], "severity": "medium", "kind": "missing_abstention_or_false_confidence_seed"})
    status = "consistent" if not any(item["severity"] == "high" for item in findings) else "mismatch"
    reason = "Release corpus manifest satisfies privacy and release-gate checks." if status == "consistent" else "Release corpus manifest has blocking findings."
    return attach_contract({"status": status, "reason": reason, "findings": findings, "manifest": manifest}, "release_corpus_validation_report")
