from __future__ import annotations

"""Release corpus manifest assembly and privacy-preserving validation.

The release corpus contains public fixtures committed with the repository plus
optional external private entries. Normal reports deliberately redact private
paths; unredacted paths are used only inside validation routines that need to
read local private documents.
"""

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess

from .contracts import attach_contract


PRIVATE_PRIVACY_CLASSES = {"private_external", "private_sanitized_external"}
PUBLIC_PRIVACY_CLASSES = {"public_fixture"}
RELEASE_PRIVACY_CLASSES = PRIVATE_PRIVACY_CLASSES | PUBLIC_PRIVACY_CLASSES


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


@dataclass(frozen=True)
class PrivateManifestLoad:
    entries: list[ReleaseCorpusEntry]
    source: dict
    findings: list[dict]


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


def _list_of_strings(value: object, *, field: str, entry_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field {field!r} must be a list of strings.")
    return value


def _entry_from_mapping(item: object) -> ReleaseCorpusEntry:
    if not isinstance(item, dict):
        raise ValueError("Private corpus manifest entries must be JSON objects.")
    fields = set(ReleaseCorpusEntry.__dataclass_fields__)
    missing = sorted(field for field in fields if field not in item)
    if missing:
        raise ValueError(f"Private corpus manifest entry is missing required fields: {', '.join(missing)}")
    entry_id = item.get("id", "<unknown>")
    if not isinstance(entry_id, str) or not entry_id:
        raise ValueError("Private corpus manifest entry field 'id' must be a non-empty string.")
    if not isinstance(item["domain"], str) or not item["domain"]:
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field 'domain' must be a non-empty string.")
    if item["document_root"] is not None and not isinstance(item["document_root"], str):
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field 'document_root' must be a string or null.")
    if not isinstance(item["privacy_class"], str) or not item["privacy_class"]:
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field 'privacy_class' must be a non-empty string.")
    if not isinstance(item["release_gate_enabled"], bool):
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field 'release_gate_enabled' must be a boolean.")
    if not isinstance(item["notes"], str):
        raise ValueError(f"Private corpus manifest entry {entry_id!r} field 'notes' must be a string.")
    return ReleaseCorpusEntry(
        id=entry_id,
        domain=item["domain"],
        privacy_class=item["privacy_class"],
        document_root=item["document_root"],
        code_roots=_list_of_strings(item["code_roots"], field="code_roots", entry_id=entry_id),
        expected_labels=_list_of_strings(item["expected_labels"], field="expected_labels", entry_id=entry_id),
        expected_operations=_list_of_strings(item["expected_operations"], field="expected_operations", entry_id=entry_id),
        expected_abstentions=_list_of_strings(item["expected_abstentions"], field="expected_abstentions", entry_id=entry_id),
        seeded_false_confidence_cases=_list_of_strings(item["seeded_false_confidence_cases"], field="seeded_false_confidence_cases", entry_id=entry_id),
        required_parser_backends=_list_of_strings(item["required_parser_backends"], field="required_parser_backends", entry_id=entry_id),
        release_gate_enabled=item["release_gate_enabled"],
        notes=item["notes"],
    )


def _load_private_entries(private_manifest: str | Path | None = None, *, repo_root: Path | None = None) -> PrivateManifestLoad:
    path = _private_manifest_path(private_manifest)
    if path is None:
        return PrivateManifestLoad([], {"configured": False, "path": None, "status": "not_configured"}, [])
    if repo_root is not None and _is_relative_to(path, repo_root):
        return PrivateManifestLoad(
            [],
            {"configured": True, "path": "<redacted-private-manifest>", "status": "inside_checkout"},
            [{"severity": "high", "kind": "private_manifest_inside_checkout"}],
        )
    if not path.exists():
        return PrivateManifestLoad([], {"configured": True, "path": "<redacted-private-manifest>", "status": "missing"}, [])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return PrivateManifestLoad(
            [],
            {"configured": True, "path": "<redacted-private-manifest>", "status": "invalid_json"},
            [{"severity": "high", "kind": "private_manifest_invalid_json", "detail": str(exc)}],
        )
    if isinstance(data, list):
        raw_entries = data
    elif isinstance(data, dict):
        raw_entries = data.get("entries", [])
    else:
        return PrivateManifestLoad(
            [],
            {"configured": True, "path": "<redacted-private-manifest>", "status": "invalid_shape"},
            [{"severity": "high", "kind": "private_manifest_invalid_shape"}],
        )
    if not isinstance(raw_entries, list):
        return PrivateManifestLoad(
            [],
            {"configured": True, "path": "<redacted-private-manifest>", "status": "invalid_shape"},
            [{"severity": "high", "kind": "private_manifest_entries_not_list"}],
        )
    entries: list[ReleaseCorpusEntry] = []
    findings: list[dict] = []
    for index, item in enumerate(raw_entries):
        try:
            entries.append(_entry_from_mapping(item))
        except ValueError as exc:
            findings.append({"severity": "high", "kind": "private_manifest_entry_invalid", "entry_index": index, "detail": str(exc)})
    status = "loaded" if not findings else "invalid_entries"
    return PrivateManifestLoad(entries, {"configured": True, "path": "<redacted-private-manifest>", "status": status, "entries": len(entries)}, findings)


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
            ["eq:dept-particle-normalization", "eq:dept-particle-ess"],
            ["logsumexp", "particle_normalization"],
            ["particle_filter_weight_degeneracy_review"],
            ["particle_filter_missing_logsumexp_seed"],
            ["current"],
            True,
            "Public sanitized particle-filter fixture covers log-sum-exp normalization and ESS diagnostics.",
        ),
        ReleaseCorpusEntry(
            "dsge_macro_finance_euler_public",
            "dsge_macro_finance",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-euler-equation", "eq:dept-sdf"],
            ["expectation", "euler_residual"],
            ["private_calibration_assumption_review"],
            ["missing_discount_factor_seed"],
            ["current"],
            True,
            "Public synthetic macro-finance fixture for Euler residual and stochastic discount factor structure.",
        ),
        ReleaseCorpusEntry(
            "stochastic_volatility_likelihood_public",
            "stochastic_volatility",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-sv-transition", "eq:dept-sv-likelihood"],
            ["innovation_update", "posterior_or_likelihood"],
            ["latent_volatility_prior_review"],
            ["missing_jacobian_seed"],
            ["current"],
            True,
            "Public synthetic stochastic-volatility transition and likelihood fixture.",
        ),
        ReleaseCorpusEntry(
            "sde_pde_numerics_public",
            "sde_pde_numerics",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-euler-maruyama", "eq:dept-pde-stability"],
            ["time_step_update", "stability_condition"],
            ["discretization_assumption_review"],
            ["unstable_step_size_seed"],
            ["current"],
            True,
            "Public synthetic SDE/PDE discretization and stability fixture.",
        ),
        ReleaseCorpusEntry(
            "ml_llm_objective_public",
            "ml_llm_objective",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-ml-loss", "eq:dept-ml-gradient"],
            ["gradient", "posterior_or_likelihood"],
            ["data_pipeline_assumption_review"],
            ["wrong_sign_gradient_seed"],
            ["current"],
            True,
            "Public synthetic ML objective and gradient sign fixture.",
        ),
        ReleaseCorpusEntry(
            "bayesian_elbo_vi_public",
            "bayesian_elbo_vi",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-elbo", "eq:dept-reparameterization-gradient"],
            ["elbo_objective", "reparameterization_gradient", "expectation"],
            ["variational_family_assumption_review"],
            ["missing_entropy_seed"],
            ["current"],
            True,
            "Public synthetic ELBO and reparameterization-gradient fixture.",
        ),
        ReleaseCorpusEntry(
            "computational_physics_mcmc_public",
            "computational_physics_mcmc",
            "public_fixture",
            str(base),
            [str(base)],
            ["eq:dept-acceptance-ratio", "eq:dept-hamiltonian-flow"],
            ["acceptance_ratio", "hamiltonian_energy", "gradient"],
            ["ergodicity_assumption_review"],
            ["missing_metropolis_correction_seed"],
            ["current"],
            True,
            "Public synthetic computational-physics MCMC acceptance and Hamiltonian fixture.",
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
    private_load = _load_private_entries(private_manifest, repo_root=_repo_root(base))
    entries.extend(private_load.entries)
    public_entries = entries if include_private_paths else [_redact_private_entry(entry) for entry in entries]
    return attach_contract(
        {
            "entries": [asdict(entry) for entry in public_entries],
            "private_manifest": private_load.source,
            "private_paths_redacted": not include_private_paths,
            "manifest_findings": private_load.findings,
        },
        "release_corpus_manifest",
    )


def validate_release_corpus_manifest(root: str | Path | None = None, *, private_manifest: str | Path | None = None) -> dict:
    """Validate release corpus privacy, manifest shape, and gate metadata."""
    root_path = Path(root) if root is not None else Path("benchmarks/fixtures")
    manifest = release_corpus_manifest(root_path, private_manifest=private_manifest)
    full_manifest = release_corpus_manifest(root_path, private_manifest=private_manifest, include_private_paths=True)
    repo_root = _repo_root(root_path)
    findings: list[dict] = list(full_manifest.get("manifest_findings", []))
    if full_manifest.get("private_manifest", {}).get("status") == "missing":
        findings.append({"severity": "medium", "kind": "private_manifest_missing"})
    if full_manifest.get("private_manifest", {}).get("status") == "loaded":
        if not any(entry["privacy_class"].startswith("private") for entry in full_manifest["entries"]):
            findings.append({"severity": "medium", "kind": "private_manifest_has_no_private_entries"})
    for entry in full_manifest["entries"]:
        if entry["privacy_class"] not in RELEASE_PRIVACY_CLASSES:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "unsupported_privacy_class", "privacy_class": entry["privacy_class"]})
        if entry["privacy_class"].startswith("private"):
            private_paths = [entry["document_root"]] if entry["document_root"] else []
            private_paths.extend(entry["code_roots"])
            for configured in private_paths:
                path = Path(configured).expanduser()
                if _is_relative_to(path, repo_root):
                    findings.append({"entry": entry["id"], "severity": "high", "kind": "private_path_inside_checkout"})
                if entry["release_gate_enabled"] and not path.exists():
                    findings.append({"entry": entry["id"], "severity": "high", "kind": "private_path_missing"})
            if entry["release_gate_enabled"] and entry["privacy_class"] not in PRIVATE_PRIVACY_CLASSES:
                findings.append({"entry": entry["id"], "severity": "high", "kind": "unsupported_private_privacy_class"})
        elif entry["release_gate_enabled"] and entry["privacy_class"] not in PUBLIC_PRIVACY_CLASSES:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "unsupported_public_privacy_class"})
        if entry["release_gate_enabled"] and not entry["expected_labels"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "missing_expected_labels"})
        if entry["release_gate_enabled"] and not entry["required_parser_backends"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "missing_required_parser_backends"})
        if not entry["expected_abstentions"] and not entry["seeded_false_confidence_cases"]:
            findings.append({"entry": entry["id"], "severity": "medium", "kind": "missing_abstention_or_false_confidence_seed"})
        if entry["release_gate_enabled"] and entry["privacy_class"].startswith("private") and not entry["document_root"]:
            findings.append({"entry": entry["id"], "severity": "high", "kind": "release_gated_private_document_root_missing"})
        if entry["release_gate_enabled"] and entry["privacy_class"].startswith("private") and entry["document_root"]:
            path = Path(entry["document_root"]).expanduser()
            if not path.exists():
                findings.append({"entry": entry["id"], "severity": "high", "kind": "private_document_root_missing"})
    status = "consistent" if not any(item["severity"] == "high" for item in findings) else "mismatch"
    reason = "Release corpus manifest satisfies privacy and release-gate checks." if status == "consistent" else "Release corpus manifest has blocking findings."
    return attach_contract({"status": status, "reason": reason, "findings": findings, "manifest": manifest}, "release_corpus_validation_report")
