"""Release profile policy and machine-readable readiness reporting.

The release profiles let the base product remain usable while strict profiles
turn optional evidence into blockers. Keep this module as the single place where
profile requirements, blockers, caveats, and evidence commands are assembled.
"""

from __future__ import annotations

import importlib.metadata
import os
import subprocess
from pathlib import Path

from .contracts import attach_contract
from .backend_env import run_backend_python
from .doctor import doctor_report
from .governance import governance_policy, validate_governance
from .parser_policy import decide_parser_policy
from .release_corpus import validate_release_corpus_manifest
from .release_profiles import PROFILE_POLICY_VERSION, RELEASE_PROFILES


def release_readiness_report(root: str | Path, *, profile: str = "base") -> dict:
    """Return the release status for a repository and release profile."""
    from .benchmarks import benchmark_gate_report

    root_path = Path(root)
    profile = _normalize_profile(profile)
    gate = benchmark_gate_report(root_path, include_release_policy=False)
    doctor = doctor_report()
    parser = decide_parser_policy(str(root_path / "benchmarks" / "fixtures"), backends=["current"])
    governance = governance_policy()
    governance_validation = validate_governance(root_path)
    release_corpus_validation = validate_release_corpus_manifest(root_path / "benchmarks" / "fixtures")
    dirty = bool(_git(root_path, ["status", "--short"]).strip())
    commit = _git(root_path, ["rev-parse", "--short", "HEAD"]).strip() or "unknown"
    blockers: list[dict] = []
    caveats: list[dict] = []
    profile_policy = _profile_policy(profile)
    backend_ok: bool | None = None
    backend_version: str | None = None
    backend_detail: str | None = None
    if profile_policy["requires_backend"]:
        # The backend profile validates LeanDojo through the documented isolated
        # environment; the active Python environment is allowed to omit it.
        backend_ok, backend_version, backend_detail = _run_backend_python_with_default_env("lean_dojo", package="lean-dojo")
    if not gate["passed"]:
        blockers.append({"kind": "benchmark_gate_failed", "severity": "high"})
    if parser.get("status") not in {"selected", "selected_for_proof_audit"}:
        blockers.append({"kind": "parser_policy_not_selected_for_proof_audit", "severity": "high"})
    if dirty:
        caveats.append({"kind": "dirty_worktree", "severity": "medium"})
    lean = doctor["capabilities"].get("lean", {})
    if lean.get("detail") != "available" and _profile_caveat_applies(profile_policy, "lean_toolchain"):
        caveats.append(
            {
                "kind": "lean_version_or_toolchain_caveat",
                "severity": "medium",
                "detail": lean.get("detail"),
                "version": lean.get("version"),
                "profile_scope": "backend_or_full",
            }
        )
    if doctor.get("conflicts") and _profile_caveat_applies(profile_policy, "active_env_dependency_conflict", backend_ok=backend_ok):
        caveats.append(
            {
                "kind": "dependency_conflicts",
                "severity": "medium",
                "conflicts": doctor["conflicts"],
                "profile_scope": "backend_or_full",
            }
        )
    latexml = doctor["capabilities"].get("latexml", {})
    if not latexml.get("available"):
        latexml_finding = {
            "kind": "latexml_optional_backend_unavailable",
            "severity": "medium",
            "detail": latexml.get("detail"),
            "install_hint": "Install OS package latexml or set MATHDEVMCP_LATEXML_PATH.",
        }
        if profile_policy["requires_latexml"]:
            blockers.append(latexml_finding | {"kind": "latexml_required_backend_unavailable", "severity": "high"})
        elif _profile_caveat_applies(profile_policy, "latexml"):
            caveats.append(latexml_finding)
    if profile_policy["requires_backend"]:
        backend_evidence = {
            "kind": "backend_lean_dojo_unavailable",
            "severity": "high",
            "detail": backend_detail,
            "version": backend_version,
            "backend_conda_env": os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV", "mathdevmcp-backends"),
            "install_hint": "Run scripts/setup_backend_env.sh and set MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends.",
        }
        if not backend_ok:
            blockers.append(backend_evidence)
    if release_corpus_validation.get("status") == "mismatch":
        blockers.append(
            {
                "kind": "release_corpus_validation_failed",
                "severity": "high",
                "findings": release_corpus_validation.get("findings", []),
            }
        )
    private_manifest = release_corpus_validation.get("manifest", {}).get("private_manifest", {})
    private_entries = [
        entry
        for entry in release_corpus_validation.get("manifest", {}).get("entries", [])
        if str(entry.get("privacy_class", "")).startswith("private") and entry.get("release_gate_enabled")
    ]
    if profile_policy["requires_private_corpus"]:
        if private_manifest.get("status") != "loaded":
            blockers.append(
                {
                    "kind": "private_corpus_manifest_required",
                    "severity": "high",
                    "detail": private_manifest.get("status", "not_configured"),
                    "install_hint": "Set MATHDEVMCP_PRIVATE_CORPUS_MANIFEST to an external manifest path and run scripts/validate_private_corpus.sh.",
                }
            )
        elif not private_entries:
            blockers.append(
                {
                    "kind": "private_corpus_release_gated_entries_missing",
                    "severity": "high",
                    "detail": "The private manifest loaded, but no release-gated private entries are visible.",
                }
            )
    elif private_manifest.get("status") in {"not_configured", "missing"} and _profile_caveat_applies(profile_policy, "private_corpus"):
        caveats.append(
            {
                "kind": "private_corpus_not_configured",
                "severity": "low",
                "detail": private_manifest.get("status", "not_configured"),
                "profile_scope": "private-corpus_or_full",
            }
        )
    if governance_validation.get("status") == "mismatch":
        blockers.append({"kind": "governance_validation_failed", "severity": "high", "findings": governance_validation.get("findings", [])})
    if profile_policy["requires_public_surface"]:
        from .public_release import public_release_check

        public_surface = public_release_check(root_path)
        if public_surface["status"] == "mismatch":
            for finding in public_surface["blockers"]:
                blockers.append(
                    {
                        "kind": finding["kind"],
                        "severity": "high",
                        "check": finding.get("check"),
                        "detail": finding.get("detail", finding.get("path", "")),
                    }
                )
    if blockers:
        recommendation = "not_ready"
        reason = "Release readiness has blocking findings."
    elif caveats:
        recommendation = "ready_with_caveats"
        reason = "Release gates passed with documented caveats."
    else:
        recommendation = "ready"
        reason = "Release gates passed without detected caveats."
    return attach_contract(
        {
            "status": recommendation,
            "reason": reason,
            "profile": profile,
            "profile_policy_version": PROFILE_POLICY_VERSION,
            "required_capabilities": profile_policy["required_capabilities"],
            "optional_capabilities": profile_policy["optional_capabilities"],
            "evidence_commands": _evidence_commands(profile),
            "package_version": _package_version(),
            "git_commit": commit,
            "dirty_worktree": dirty,
            "benchmark_gate": gate,
            "doctor_summary": doctor,
            "parser_policy": parser,
            "governance_policy": governance,
            "governance_validation": governance_validation,
            "release_corpus_validation": release_corpus_validation,
            "schema_version": "1.0",
            "blockers": blockers,
            "caveats": caveats,
        },
        "release_readiness_report",
    )


def release_claim_ready(report: dict) -> bool:
    """Only a clean, fully evidenced report can authorize a release claim."""

    return (
        report.get("status") == "ready"
        and report.get("dirty_worktree") is False
        and not report.get("caveats")
        and not report.get("blockers")
    )


def backend_environment_policy() -> dict:
    """Return the profile-scoped backend environment policy."""

    profiles = {profile: _profile_policy(profile) for profile in sorted(RELEASE_PROFILES)}
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Backend and Lean dependencies are profile-scoped; base/public checks stay usable without strict optional backend evidence.",
            "base_policy": "The base package and base release profile do not require LeanDojo, LaTeXML, private corpora, or the mcp package as a base dependency.",
            "mcp_policy": "MCP-facing installs use the optional [mcp] extra; public release checks inspect MCP source/docs without importing the optional runtime.",
            "lean_policy": "Direct Lean rejection is a mismatch, while missing executables, toolchain download failures, timeouts, and placeholders are diagnostic/inconclusive.",
            "strict_profiles": {
                "backend": "Requires isolated LeanDojo backend evidence.",
                "latexml": "Requires a validating LaTeXML executable.",
                "private-corpus": "Requires an external release-gated private corpus manifest.",
                "full": "Requires backend, LaTeXML, and private corpus evidence.",
            },
            "profiles": profiles,
        },
        "backend_environment_policy",
    )


def _run_backend_python_with_default_env(module: str, *, package: str) -> tuple[bool, str | None, str]:
    previous = os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV")
    if not previous:
        os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = "mathdevmcp-backends"
    try:
        return run_backend_python(module, package=package)
    finally:
        if previous is None:
            os.environ.pop("MATHDEVMCP_BACKEND_CONDA_ENV", None)
        else:
            os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = previous


def _normalize_profile(profile: str) -> str:
    normalized = (profile or "base").strip().lower()
    if normalized not in RELEASE_PROFILES:
        raise ValueError(f"Unknown release profile: {profile}. Expected one of: {', '.join(sorted(RELEASE_PROFILES))}")
    return normalized


def _profile_policy(profile: str) -> dict:
    requires_backend = profile in {"backend", "full"}
    requires_latexml = profile in {"latexml", "full"}
    requires_private = profile in {"private-corpus", "full"}
    requires_public_surface = profile == "public"
    required = ["benchmark_gate", "current_parser_policy", "governance_validation", "release_corpus_manifest"]
    optional = ["latexml", "lean_dojo_backend_env", "private_corpus_manifest"]
    if requires_backend:
        required.append("lean_dojo_backend_env")
        optional = [item for item in optional if item != "lean_dojo_backend_env"]
    if requires_latexml:
        required.append("latexml")
        optional = [item for item in optional if item != "latexml"]
    if requires_private:
        required.append("private_corpus_manifest")
        optional = [item for item in optional if item != "private_corpus_manifest"]
    if requires_public_surface:
        required.extend(["mcp_surface_consistency", "packaging_support_matrix", "documentation_sync", "ci_release_gate", "quality_gate"])
    return {
        "profile": profile,
        "requires_backend": requires_backend,
        "requires_latexml": requires_latexml,
        "requires_private_corpus": requires_private,
        "requires_public_surface": requires_public_surface,
        "required_capabilities": required,
        "optional_capabilities": optional,
    }


def _profile_caveat_applies(profile_policy: dict, kind: str, *, backend_ok: bool | None = None) -> bool:
    """Return whether an optional evidence caveat should affect this profile."""

    profile = profile_policy["profile"]
    if kind == "lean_toolchain":
        return profile_policy["requires_backend"]
    if kind == "active_env_dependency_conflict":
        return profile_policy["requires_backend"] and backend_ok is not True
    if kind == "latexml":
        return profile not in {"public"} and not profile_policy["requires_latexml"]
    if kind == "private_corpus":
        return profile_policy["requires_private_corpus"]
    return True


def _evidence_commands(profile: str) -> list[str]:
    commands = [
        'PYTHONPATH=src python -m mathdevmcp.cli doctor',
        f'PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile {profile}',
        'PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root "$PWD/benchmarks/fixtures"',
        'scripts/release_smoke.sh "$PWD"',
    ]
    if profile in {"backend", "full"}:
        commands.append('scripts/backend_env_doctor.sh "$PWD"')
        commands.append('scripts/validate_backend_install.sh "$PWD"')
    if profile in {"latexml", "full"}:
        commands.append('MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"')
    else:
        commands.append('scripts/validate_latexml_backend.sh "$PWD"')
    if profile in {"private-corpus", "full"}:
        commands.append('MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json scripts/validate_private_corpus.sh "$PWD"')
    if profile == "public":
        commands.append('PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"')
        commands.append('scripts/quality_gate.sh')
    return commands


def _git(root: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True, timeout=5)
    except Exception:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout


def _package_version() -> str:
    try:
        return importlib.metadata.version("mathdevmcp")
    except importlib.metadata.PackageNotFoundError:
        return "editable_or_uninstalled"
