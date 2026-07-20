"""Executable checks for release-closeout hypotheses.

The hypotheses here are release-process and evidence-boundary claims. They do
not certify arbitrary mathematics; they verify that release evidence remains
profile-scoped, reproducible, and redacted.
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .public_release import public_release_check
from .release_corpus import validate_release_corpus_manifest
from .release_policy import release_claim_ready, release_readiness_report
from .release_profile_analysis import release_profile_analysis


RELEASE_HYPOTHESIS_CHECK_VERSION = "2026-05-release-hypotheses"
BOUNDARY_DOCS = (
    "README.md",
    "docs/mathdevmcp-release-policy.md",
    "docs/mathdevmcp-maintainer-guide.md",
    "docs/mathdevmcp-deployment-guide.md",
    "docs/mathdevmcp-release-report.tex",
)


def release_hypothesis_check(
    root: str | Path,
    *,
    public: bool = True,
    strict_full: bool = False,
    require_canonical_backend: bool = False,
) -> dict[str, Any]:
    """Return an executable report for release-closeout hypotheses."""

    root_path = Path(root)
    checks: list[dict[str, Any]] = [
        _publication_invariant(root_path),
        _ci_hypothesis_gate(root_path),
        _evidence_boundary(root_path),
    ]
    if strict_full:
        checks.append(_strict_full_reproducibility(root_path, require_canonical_backend=require_canonical_backend))
    else:
        checks.append(_strict_full_skipped(require_canonical_backend=require_canonical_backend))

    blockers = [finding for check in checks for finding in check["findings"] if finding["severity"] == "high"]
    caveats = [finding for check in checks for finding in check["findings"] if finding["severity"] != "high"]
    status = "consistent" if not blockers else "mismatch"
    reason = "Release hypotheses are executable and currently satisfied." if status == "consistent" else "Release hypotheses have blocking findings."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "check_version": RELEASE_HYPOTHESIS_CHECK_VERSION,
            "mode": {
                "public": public,
                "strict_full": strict_full,
                "require_canonical_backend": require_canonical_backend,
            },
            "checks": checks,
            "blockers": blockers,
            "caveats": caveats,
        },
        "release_hypothesis_check",
    )


def _publication_invariant(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    public_surface = public_release_check(root)
    public_ready = release_readiness_report(root, profile="public")
    profile_analysis = release_profile_analysis(root)
    if public_surface["status"] != "consistent":
        findings.append(
            {
                "check": "publication_invariant",
                "severity": "high",
                "kind": "public_release_surface_not_consistent",
                "detail": public_surface["status"],
            }
        )
    if not release_claim_ready(public_ready):
        severity = "high"
        findings.append(
            {
                "check": "publication_invariant",
                "severity": severity,
                "kind": "public_profile_not_clean_ready",
                "detail": public_ready["status"],
                "caveats": [item.get("kind") for item in public_ready.get("caveats", [])],
            }
        )
    base_public = profile_analysis.get("release_claims", {}).get("base_public", {})
    if base_public.get("claim_ready") is not True:
        findings.append(
            {
                "check": "publication_invariant",
                "severity": "high",
                "kind": "base_public_claim_not_ready",
                "detail": base_public.get("status", "unknown"),
            }
        )
    return _check_result(
        "publication_invariant",
        findings,
        evidence={
            "git_commit": public_ready.get("git_commit"),
            "dirty_worktree": public_ready.get("dirty_worktree"),
            "public_release_surface_status": public_surface["status"],
            "public_profile_status": public_ready["status"],
            "base_public_claim_status": base_public.get("status"),
            "next_hypotheses": profile_analysis.get("next_hypotheses", []),
        },
    )


def _ci_hypothesis_gate(root: Path) -> dict[str, Any]:
    path = root / ".github" / "workflows" / "ci.yml"
    findings: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {"workflow": str(path.relative_to(root)), "strict_full_requires_secrets": True}
    if not path.exists():
        findings.append({"check": "ci_hypothesis_gate", "severity": "high", "kind": "ci_workflow_missing", "path": str(path)})
        return _check_result("ci_hypothesis_gate", findings, evidence=evidence)
    text = path.read_text(encoding="utf-8")
    for marker in ["release-hypothesis-check", "--public"]:
        if marker not in text:
            findings.append({"check": "ci_hypothesis_gate", "severity": "high", "kind": "ci_hypothesis_command_missing", "detail": marker})
    forbidden_public_markers = ["--strict-full", "MATHDEVMCP_PRIVATE_CORPUS_MANIFEST:"]
    public_step_block = _extract_ci_public_hypothesis_step(text)
    for marker in forbidden_public_markers:
        if marker in public_step_block:
            findings.append({"check": "ci_hypothesis_gate", "severity": "high", "kind": "public_ci_requires_strict_secret", "detail": marker})
    evidence["public_step_present"] = bool(public_step_block)
    return _check_result("ci_hypothesis_gate", findings, evidence=evidence)


def _extract_ci_public_hypothesis_step(text: str) -> str:
    marker = "Release hypothesis check"
    index = text.find(marker)
    if index < 0:
        return ""
    next_step = text.find("\n      - name:", index + len(marker))
    return text[index:] if next_step < 0 else text[index:next_step]


def _strict_full_reproducibility(root: Path, *, require_canonical_backend: bool) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    selected_backend = os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV", "")
    expected_backend = "mathdevmcp-backends"
    backend_spec = _backend_spec(root)
    if not backend_spec["valid"]:
        findings.append(
            {
                "check": "strict_full_reproducibility",
                "severity": "high",
                "kind": "canonical_backend_spec_invalid",
                "detail": backend_spec["reason"],
            }
        )
    if require_canonical_backend and selected_backend != expected_backend:
        findings.append(
            {
                "check": "strict_full_reproducibility",
                "severity": "high",
                "kind": "canonical_backend_env_not_selected",
                "detail": selected_backend or "not_set",
                "expected": expected_backend,
            }
        )
    if not os.environ.get("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST"):
        findings.append(
            {
                "check": "strict_full_reproducibility",
                "severity": "high",
                "kind": "private_manifest_env_required_for_strict_full",
            }
        )
    if os.environ.get("MATHDEVMCP_REQUIRE_LATEXML") != "1":
        findings.append({"check": "strict_full_reproducibility", "severity": "high", "kind": "latexml_strict_env_required"})

    full = release_readiness_report(root, profile="full")
    if not release_claim_ready(full):
        severity = "high"
        findings.append(
            {
                "check": "strict_full_reproducibility",
                "severity": severity,
                "kind": "full_profile_not_clean_ready",
                "detail": full["status"],
                "blockers": [item.get("kind") for item in full.get("blockers", [])],
                "caveats": [item.get("kind") for item in full.get("caveats", [])],
            }
        )
    release_corpus = full.get("release_corpus_validation", {})
    manifest = release_corpus.get("manifest", {})
    private_manifest = manifest.get("private_manifest", {})
    if private_manifest.get("status") != "loaded":
        findings.append(
            {
                "check": "strict_full_reproducibility",
                "severity": "high",
                "kind": "private_manifest_not_loaded",
                "detail": private_manifest.get("status"),
            }
        )
    if manifest.get("private_paths_redacted") is not True:
        findings.append({"check": "strict_full_reproducibility", "severity": "high", "kind": "private_paths_not_redacted"})
    doctor = full.get("doctor_summary", {})
    capabilities = doctor.get("capabilities", {})
    return _check_result(
        "strict_full_reproducibility",
        findings,
        evidence={
            "selected_backend_env": selected_backend or "not_set",
            "canonical_backend_env": expected_backend,
            "canonical_backend_required": require_canonical_backend,
            "backend_spec": backend_spec,
            "full_profile_status": full["status"],
            "full_profile_blockers": [item.get("kind") for item in full.get("blockers", [])],
            "full_profile_caveats": [item.get("kind") for item in full.get("caveats", [])],
            "lean": _capability_summary(capabilities.get("lean", {})),
            "lean_dojo": _capability_summary(capabilities.get("lean_dojo", {})),
            "latexml": _capability_summary(capabilities.get("latexml", {})),
            "private_manifest_status": private_manifest.get("status"),
            "private_manifest_entries": private_manifest.get("entries", 0),
            "private_paths_redacted": manifest.get("private_paths_redacted"),
        },
    )


def _strict_full_skipped(*, require_canonical_backend: bool) -> dict[str, Any]:
    caveat = {
        "check": "strict_full_reproducibility",
        "severity": "low",
        "kind": "strict_full_check_not_requested",
        "detail": "Run with --strict-full and configured backend/LaTeXML/private-manifest evidence.",
    }
    return _check_result(
        "strict_full_reproducibility",
        [caveat],
        evidence={"canonical_backend_required": require_canonical_backend, "strict_full": False},
    )


def _backend_spec(root: Path) -> dict[str, Any]:
    path = root / "environment-backends.yml"
    if not path.exists():
        return {"valid": False, "reason": "environment-backends.yml missing"}
    text = path.read_text(encoding="utf-8")
    required = ["name: mathdevmcp-backends", "python=3.11", "sympy=1.14", "lean-dojo==4.20.0"]
    missing = [marker for marker in required if marker not in text]
    return {"valid": not missing, "reason": "ok" if not missing else "missing " + ", ".join(missing), "path": str(path.name)}


def _evidence_boundary(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    phrase_sets = [
        ("does not certify", "arbitrary mathematics"),
        ("deterministic backend", "cert"),
        ("diagnostic", "proof"),
    ]
    docs_with_boundary: list[str] = []
    for relative in BOUNDARY_DOCS:
        path = root / relative
        if not path.exists():
            findings.append({"check": "evidence_boundary", "severity": "high", "kind": "boundary_doc_missing", "path": relative})
            continue
        text = path.read_text(encoding="utf-8").lower()
        if any(all(piece in text for piece in phrase_set) for phrase_set in phrase_sets):
            docs_with_boundary.append(relative)
    required_docs = {"docs/mathdevmcp-release-policy.md", "docs/mathdevmcp-maintainer-guide.md", "docs/mathdevmcp-release-report.tex"}
    missing_required = sorted(required_docs - set(docs_with_boundary))
    for relative in missing_required:
        findings.append({"check": "evidence_boundary", "severity": "high", "kind": "release_boundary_language_missing", "path": relative})
    return _check_result("evidence_boundary", findings, evidence={"docs_with_boundary_language": docs_with_boundary})


def _capability_summary(capability: dict[str, Any]) -> dict[str, Any]:
    return {
        "available": bool(capability.get("available")),
        "status": capability.get("status"),
        "detail": capability.get("detail"),
        "version": capability.get("version"),
    }


def _check_result(name: str, findings: list[dict[str, Any]], *, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    status = "consistent" if not any(item["severity"] == "high" for item in findings) else "mismatch"
    return {"name": name, "status": status, "findings": findings, "evidence": evidence or {}}
