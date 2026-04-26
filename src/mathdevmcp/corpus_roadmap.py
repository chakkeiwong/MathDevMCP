from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import contract_metadata


@dataclass(frozen=True)
class CorpusRoadmapEntry:
    category: str
    privacy: str
    public_fixture_status: str
    required_false_confidence_seed: str
    expected_abstention_policy: str


def department_corpus_roadmap() -> dict:
    entries = [
        CorpusRoadmapEntry("kalman_state_space", "synthetic_or_sanitized_and_private", "active", "missing_solve_or_covariance_update", "unsupported stochastic notation must abstain"),
        CorpusRoadmapEntry("hmc_nuts", "synthetic_or_sanitized_and_private", "active", "missing_gradient_or_mh_correction", "short diagnostics are not convergence evidence"),
        CorpusRoadmapEntry("particle_filters", "synthetic_or_sanitized_and_private", "active", "missing_logsumexp_normalization", "weight degeneracy claims require diagnostics"),
        CorpusRoadmapEntry("dsge_macro_finance", "private_preferred", "planned", "missing_stationarity_or_rank_condition", "model-solution claims require explicit assumptions"),
        CorpusRoadmapEntry("stochastic_volatility", "private_preferred", "planned", "wrong_state_or_observation_variance", "likelihood claims require shape and distribution assumptions"),
        CorpusRoadmapEntry("sde_pde_numerics", "private_preferred", "planned", "unstated_boundary_or_stability_condition", "numerical stability claims require diagnostics"),
        CorpusRoadmapEntry("ml_llm_objectives", "synthetic_or_sanitized_and_private", "planned", "missing_normalization_or_loss_term", "training-loss claims are empirical unless derived"),
        CorpusRoadmapEntry("bayesian_elbo_vi", "synthetic_or_sanitized_and_private", "planned", "missing_entropy_or_jacobian_term", "variational claims require objective and support assumptions"),
        CorpusRoadmapEntry("computational_physics_algorithms", "synthetic_or_sanitized_and_private", "planned", "missing_conservation_or_discretization_term", "physics-inspired diagnostics are not proofs"),
    ]
    return {"ok": True, "entries": [asdict(entry) for entry in entries], "metadata": contract_metadata("department_corpus_roadmap")}
