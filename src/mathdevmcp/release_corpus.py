from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess

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


def _repo_root(start: Path) -> Path:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start if start.exists() else Path.cwd(),
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return Path.cwd().resolve()
    if completed.returncode != 0:
        return Path.cwd().resolve()
    return Path(completed.stdout.strip()).resolve()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _private_manifest_path(private_manifest: str | Path | None = None) -> Path | None:
    configured = private_manifest or os.environ.get("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", "").strip()
    return Path(configured).expanduser().resolve() if configured else None


def _entry_from_mapping(item: dict) -> ReleaseCorpusEntry:
    fields = set(ReleaseCorpusEntry.__dataclass_fields__)
    missing = sorted(field for field in fields if field not in item)
    if missing:
        raise ValueError(f"Private corpus manifest entry is missing required fields: {', '.join(missing)}")
    return ReleaseCorpusEntry(**{field: item[field] for field in fields})


def _load_private_entries(private_manifest: str | Path | None = None) -> tuple[list[ReleaseCorpusEntry], dict]:
    path = _private_manifest_path(private_manifest)
    if path is None:
        return [], {"configured": False, "path": None, "status": "not_configured"}
    if not path.exists():
        return [], {"configured": True, "path": "<redacted-private-manifest>", "status": "missing"}
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_entries = data if isinstance(data, list) else data.get("entries", [])
    if not isinstance(raw_entries, list):
        raise ValueError("Private corpus manifest must be a list or an object with an entries list.")
    entries = [_entry_from_mapping(item) for item in raw_entries]
    return entries, {"configured": True, "path": "<redacted-private-manifest>", "status": "loaded", "entries": len(entries)}


def _redact_private_entry(entry: ReleaseCorpusEntry) -> ReleaseCorpusEntry:
    if not entry.privacy_class.startswith("private"):
        return entry
    return ReleaseCorpusEntry(
        id=entry.id,
        domain=entry.domain,
        privacy_class=entry.privacy_class,
        document_root=None if entry.document_root else None,
        code_roots=["<redacted-private-path>"] if entry.code_roots else [],
        expected_labels=entry.expected_labels,
        expected_operations=entry.expected_operations,
        expected_abstentions=entry.expected_abstentions,
        seeded_false_confidence_cases=entry.seeded_false_confidence_cases,
        required_parser_backends=entry.required_parser_backends,
        release_gate_enabled=entry.release_gate_enabled,
        notes=entry.notes,
    )


def release_corpus_manifest(
    root: str | Path | None = None,
    *,
    private_manifest: str | Path | None = None,
    include_private_paths: bool = False,
) -> dict:
    base = Path(root) if root is not None else Path("benchmarks/fixtures")
    entries: list[ReleaseCorpusEntry] = [
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
            "macro_filter_multifile",
            "macro_filter_state_space",
            "public_fixture",
            str(base),
            [str(base)],
            [
                "assump:macro-filter-dimensions",
                "eq:macro-filter-transition",
                "eq:macro-filter-innovation",
                "eq:macro-filter-likelihood",
                "prop:macro-filter-repeat-notation",
            ],
            ["logdet", "inverse_or_solve", "quadratic_form", "prediction_update", "innovation_update", "innovation_covariance"],
            ["eq:macro-filter-likelihood", "prop:macro-filter-repeat-notation"],
            ["doc_macro_filter_missing_gain.py"],
            ["current"],
            True,
            "Public sanitized multi-file fixture with macros and repeated notation. The paired code deliberately omits Kalman gain/state/covariance updates.",
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
    private_entries, private_source = _load_private_entries(private_manifest)
    entries.extend(private_entries)
    public_entries = entries if include_private_paths else [_redact_private_entry(entry) for entry in entries]
    return attach_contract(
        {
            "entries": [asdict(entry) for entry in public_entries],
            "private_manifest": private_source,
            "private_paths_redacted": not include_private_paths,
        },
        "release_corpus_manifest",
    )


def validate_release_corpus_manifest(root: str | Path | None = None, *, private_manifest: str | Path | None = None) -> dict:
    root_path = Path(root) if root is not None else Path("benchmarks/fixtures")
    manifest = release_corpus_manifest(root_path, private_manifest=private_manifest)
    full_manifest = release_corpus_manifest(root_path, private_manifest=private_manifest, include_private_paths=True)
    repo_root = _repo_root(root_path)
    findings: list[dict] = []
    if full_manifest.get("private_manifest", {}).get("status") == "missing":
        findings.append({"severity": "medium", "kind": "private_manifest_missing"})
    for entry in full_manifest["entries"]:
        if entry["privacy_class"].startswith("private"):
            private_paths = [entry["document_root"]] if entry["document_root"] else []
            private_paths.extend(entry["code_roots"])
            for configured in private_paths:
                path = Path(configured).expanduser()
                if _is_relative_to(path, repo_root):
                    findings.append({"entry": entry["id"], "severity": "high", "kind": "private_path_inside_checkout"})
        if entry["release_gate_enabled"] and not entry["expected_labels"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "missing_expected_labels"})
        if not entry["expected_abstentions"] and not entry["seeded_false_confidence_cases"]:
            findings.append({"entry": entry["id"], "severity": "medium", "kind": "missing_abstention_or_false_confidence_seed"})
        if entry["release_gate_enabled"] and entry["privacy_class"].startswith("private") and not entry["document_root"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "release_gated_private_document_root_missing"})
    status = "consistent" if not any(item["severity"] == "high" for item in findings) else "mismatch"
    reason = "Release corpus manifest satisfies privacy and release-gate checks." if status == "consistent" else "Release corpus manifest has blocking findings."
    return attach_contract({"status": status, "reason": reason, "findings": findings, "manifest": manifest}, "release_corpus_validation_report")
