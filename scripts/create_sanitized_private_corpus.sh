#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/create_sanitized_private_corpus.sh OUTPUT_DIR

Create an external sanitized private-corpus manifest and tiny LaTeX/code corpus
outside the repository. The generated manifest is intended for local release
gate validation; do not commit the populated manifest.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

OUT="${1:-}"
if [[ -z "$OUT" ]]; then
  usage >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT="$(python -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$OUT")"

case "$OUT" in
  "$ROOT"|"$ROOT"/*)
    echo "Refusing to create sanitized private corpus inside the repository: $OUT" >&2
    exit 2
    ;;
esac

mkdir -p "$OUT"
export MATHDEVMCP_SANITIZED_PRIVATE_CORPUS_OUT="$OUT"

python - <<'PY'
import json
import os
from pathlib import Path

out = Path(os.environ["MATHDEVMCP_SANITIZED_PRIVATE_CORPUS_OUT"])

entries = [
    {
        "id": "private_dsge_macro_finance_euler",
        "domain": "dsge_macro_finance",
        "dirname": "dsge",
        "labels": ["eq:private-euler-equation", "eq:private-sdf"],
        "tex": r"""
\section{Sanitized DSGE Euler Equation}
\begin{equation}
\label{eq:private-euler-equation}
E_t[m_{t+1} R_{t+1}] = 1
\end{equation}
\begin{equation}
\label{eq:private-sdf}
m_{t+1} = \beta \frac{u'(c_{t+1})}{u'(c_t)}
\end{equation}
""",
        "operations": ["expectation", "euler_residual"],
        "abstentions": ["private_calibration_assumption_review"],
        "seeds": ["missing_discount_factor_seed"],
    },
    {
        "id": "private_stochastic_volatility_likelihood",
        "domain": "stochastic_volatility",
        "dirname": "stochastic-volatility",
        "labels": ["eq:private-sv-transition", "eq:private-sv-likelihood"],
        "tex": r"""
\section{Sanitized Stochastic Volatility Likelihood}
\begin{equation}
\label{eq:private-sv-transition}
h_t = \mu + \phi(h_{t-1}-\mu) + \eta_t
\end{equation}
\begin{equation}
\label{eq:private-sv-likelihood}
y_t \mid h_t \sim \mathcal{N}(0, \exp(h_t))
\end{equation}
""",
        "operations": ["logdet", "innovation_update", "posterior_or_likelihood"],
        "abstentions": ["latent_volatility_prior_review"],
        "seeds": ["missing_jacobian_seed"],
    },
    {
        "id": "private_sde_pde_numerics",
        "domain": "sde_pde_numerics",
        "dirname": "sde-pde",
        "labels": ["eq:private-euler-maruyama", "eq:private-pde-residual"],
        "tex": r"""
\section{Sanitized SDE/PDE Numerics}
\begin{equation}
\label{eq:private-euler-maruyama}
X_{n+1}=X_n + b(X_n)\Delta t + \sigma(X_n)\sqrt{\Delta t}\xi_n
\end{equation}
\begin{equation}
\label{eq:private-pde-residual}
r_i = \frac{u_i^{n+1}-u_i^n}{\Delta t} - \mathcal{L}u_i^n
\end{equation}
""",
        "operations": ["time_step_update", "stability_condition"],
        "abstentions": ["discretization_assumption_review"],
        "seeds": ["unstable_step_size_seed"],
    },
    {
        "id": "private_ml_llm_objective",
        "domain": "ml_llm_objective",
        "dirname": "ml-objectives",
        "labels": ["eq:private-loss", "eq:private-gradient"],
        "tex": r"""
\section{Sanitized ML Objective}
\begin{equation}
\label{eq:private-loss}
\mathcal{L}(\theta)= -\sum_i \log p_\theta(y_i \mid x_i)
\end{equation}
\begin{equation}
\label{eq:private-gradient}
\nabla_\theta \mathcal{L}(\theta)= -\sum_i \nabla_\theta \log p_\theta(y_i \mid x_i)
\end{equation}
""",
        "operations": ["gradient", "posterior_or_likelihood"],
        "abstentions": ["data_pipeline_assumption_review"],
        "seeds": ["wrong_sign_gradient_seed"],
    },
    {
        "id": "private_bayesian_elbo_vi",
        "domain": "bayesian_elbo_vi",
        "dirname": "elbo-vi",
        "labels": ["eq:private-elbo", "eq:private-reparameterization-gradient"],
        "tex": r"""
\section{Sanitized Bayesian VI}
\begin{equation}
\label{eq:private-elbo}
\mathcal{E}(\lambda)=E_{q_\lambda(z)}[\log p(x,z)-\log q_\lambda(z)]
\end{equation}
\begin{equation}
\label{eq:private-reparameterization-gradient}
\nabla_\lambda \mathcal{E}(\lambda)=E_\epsilon[\nabla_\lambda f(T_\lambda(\epsilon))]
\end{equation}
""",
        "operations": ["gradient", "expectation", "posterior_or_likelihood"],
        "abstentions": ["variational_family_assumption_review"],
        "seeds": ["missing_entropy_seed"],
    },
    {
        "id": "private_computational_physics_mcmc",
        "domain": "computational_physics_mcmc",
        "dirname": "physics-mcmc",
        "labels": ["eq:private-acceptance-ratio", "eq:private-hamiltonian-flow"],
        "tex": r"""
\section{Sanitized Computational Physics MCMC}
\begin{equation}
\label{eq:private-acceptance-ratio}
\alpha = \min\{1,\exp[-H(q',p')+H(q,p)]\}
\end{equation}
\begin{equation}
\label{eq:private-hamiltonian-flow}
\dot q = \nabla_p H(q,p),\qquad \dot p = -\nabla_q H(q,p)
\end{equation}
""",
        "operations": ["hamiltonian_energy", "gradient", "leapfrog_update"],
        "abstentions": ["ergodicity_assumption_review"],
        "seeds": ["missing_metropolis_correction_seed"],
    },
]

manifest_entries = []
for entry in entries:
    domain_root = out / entry["dirname"]
    doc_root = domain_root / "docs"
    code_root = domain_root / "code"
    doc_root.mkdir(parents=True, exist_ok=True)
    code_root.mkdir(parents=True, exist_ok=True)
    (doc_root / "model.tex").write_text(entry["tex"].strip() + "\n", encoding="utf-8")
    (code_root / "implementation.py").write_text(
        "# Sanitized placeholder implementation used for private-corpus release validation.\n"
        "def diagnostic_placeholder():\n"
        "    return 'sanitized'\n",
        encoding="utf-8",
    )
    manifest_entries.append(
        {
            "id": entry["id"],
            "domain": entry["domain"],
            "privacy_class": "private_sanitized_external",
            "document_root": str(doc_root),
            "code_roots": [str(code_root)],
            "expected_labels": entry["labels"],
            "expected_operations": entry["operations"],
            "expected_abstentions": entry["abstentions"],
            "seeded_false_confidence_cases": entry["seeds"],
            "required_parser_backends": ["current"],
            "release_gate_enabled": True,
            "notes": "External sanitized private-corpus release gate fixture. Do not commit populated manifests with real private paths.",
        }
    )

manifest = out / "manifest.json"
manifest.write_text(json.dumps({"entries": manifest_entries}, indent=2), encoding="utf-8")
print(manifest)
PY
