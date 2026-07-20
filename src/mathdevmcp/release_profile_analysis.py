"""Cross-profile release analysis built from profile readiness reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .release_policy import release_claim_ready, release_readiness_report
from .release_profiles import PROFILE_POLICY_VERSION, RELEASE_PROFILES


PROFILE_ORDER = ("base", "public", "backend", "latexml", "private-corpus", "full")
STRICT_PROFILES = {"backend", "latexml", "private-corpus", "full"}


def release_profile_analysis(root: str | Path) -> dict:
    """Return a compact analysis of all release profiles."""

    root_path = Path(root)
    reports = {profile: release_readiness_report(root_path, profile=profile) for profile in PROFILE_ORDER if profile in RELEASE_PROFILES}
    profiles = [_profile_entry(profile, reports[profile]) for profile in PROFILE_ORDER if profile in reports]
    strict_blockers = {
        profile: {
            "status": reports[profile]["status"],
            "blockers": reports[profile]["blockers"],
            "caveats": reports[profile]["caveats"],
            "next_action": _next_action(profile, reports[profile]),
        }
        for profile in PROFILE_ORDER
        if profile in STRICT_PROFILES and profile in reports and (reports[profile]["blockers"] or reports[profile]["caveats"])
    }
    claims = _release_claims(reports)
    base_public_ready = claims["base_public"]["claim_ready"]
    strict_blocked = any(not claims[name]["claim_ready"] for name in ("backend", "latexml", "private_corpus", "full"))
    if not base_public_ready:
        status = "not_ready"
        reason = "Base/public release claims have blocking findings."
    elif strict_blocked:
        status = "ready_with_caveats"
        reason = "Base/public release claims are ready; one or more strict profiles still require external evidence."
    else:
        status = "ready"
        reason = "All release profile claims are ready."
    first = reports[PROFILE_ORDER[0]]
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "profile_policy_version": PROFILE_POLICY_VERSION,
            "git_commit": first.get("git_commit", "unknown"),
            "dirty_worktree": any(bool(report.get("dirty_worktree")) for report in reports.values()),
            "profiles": profiles,
            "release_claims": claims,
            "strict_profile_blockers": strict_blockers,
            "doctor_highlights": _doctor_highlights(first),
            "next_hypotheses": _next_hypotheses(reports),
            "schema_version": "1.0",
        },
        "release_profile_analysis",
    )


def _profile_entry(profile: str, report: dict[str, Any]) -> dict:
    return {
        "profile": profile,
        "status": report["status"],
        "claim_ready": release_claim_ready(report),
        "strict": profile in STRICT_PROFILES,
        "public_claim": profile == "public",
        "required_capabilities": report["required_capabilities"],
        "optional_capabilities": report["optional_capabilities"],
        "blockers": report["blockers"],
        "caveats": report["caveats"],
        "interpretation": _interpretation(profile, report),
        "next_action": _next_action(profile, report),
    }


def _release_claims(reports: dict[str, dict]) -> dict[str, dict]:
    base = reports["base"]
    public = reports["public"]
    base_public_ready = release_claim_ready(base) and release_claim_ready(public)
    base_public_status = "not_ready" if not base_public_ready else "ready"
    return {
        "base_public": {
            "claim_ready": base_public_ready,
            "profiles": ["base", "public"],
            "status": base_public_status,
            "interpretation": "Public/base release claim is justified when both base and public profiles have no blockers.",
        },
        "backend": _single_claim(reports["backend"], "backend", "Backend claim requires isolated LeanDojo backend evidence."),
        "latexml": _single_claim(reports["latexml"], "latexml", "LaTeXML claim requires strict executable validation."),
        "private_corpus": _single_claim(reports["private-corpus"], "private-corpus", "Private-corpus claim requires an external release-gated manifest."),
        "full": _single_claim(reports["full"], "full", "Full claim requires backend, LaTeXML, and private corpus evidence."),
    }


def _single_claim(report: dict, profile: str, interpretation: str) -> dict:
    return {
        "claim_ready": release_claim_ready(report),
        "profiles": [profile],
        "status": report["status"],
        "interpretation": interpretation,
        "blocker_kinds": [blocker.get("kind", "unknown") for blocker in report["blockers"]],
    }


def _interpretation(profile: str, report: dict) -> str:
    if report["status"] == "not_ready":
        return f"{profile} profile is not ready because required profile evidence is missing or failed."
    if profile in {"base", "public"}:
        return f"{profile} profile is ready for the public/base release scope."
    if profile in STRICT_PROFILES:
        return f"{profile} strict profile is ready under its required evidence."
    return f"{profile} profile is ready."


def _next_action(profile: str, report: dict) -> str:
    blocker_kinds = {blocker.get("kind") for blocker in report["blockers"]}
    caveat_kinds = {caveat.get("kind") for caveat in report["caveats"]}
    if profile in {"base", "public"} and report["status"] in {"ready", "ready_with_caveats"}:
        return "Proceed with public/base release process; push, merge, or tag according to project policy."
    if "backend_lean_dojo_unavailable" in blocker_kinds:
        return "Configure the isolated backend environment and rerun release-readiness --profile backend."
    if "latexml_required_backend_unavailable" in blocker_kinds:
        return "Install or point MATHDEVMCP_LATEXML_PATH at LaTeXML and rerun the latexml profile."
    if "private_corpus_manifest_required" in blocker_kinds:
        return "Set MATHDEVMCP_PRIVATE_CORPUS_MANIFEST to an external sanitized/private manifest and rerun the profile."
    if "private_corpus_release_gated_entries_missing" in blocker_kinds:
        return "Add release-gated private manifest entries outside git and rerun private-corpus validation."
    if "lean_version_or_toolchain_caveat" in caveat_kinds:
        return "Populate the Lean toolchain cache or set the backend Lean path before claiming strict backend/full readiness."
    if report["status"] == "ready_with_caveats":
        return "Review caveats and decide whether they are acceptable for this profile."
    return "No profile-specific action is required."


def _doctor_highlights(report: dict) -> dict:
    doctor = report.get("doctor_summary", {})
    capabilities = doctor.get("capabilities", {})
    lean = capabilities.get("lean", {})
    latexml = capabilities.get("latexml", {})
    lean_dojo = capabilities.get("lean_dojo", {})
    return {
        "lean": {
            "available": bool(lean.get("available")),
            "status": lean.get("status"),
            "detail": lean.get("detail"),
            "version": lean.get("version"),
        },
        "latexml": {
            "available": bool(latexml.get("available")),
            "status": latexml.get("status"),
            "detail": latexml.get("detail"),
            "version": latexml.get("version"),
        },
        "lean_dojo": {
            "available": bool(lean_dojo.get("available")),
            "status": lean_dojo.get("status"),
            "detail": lean_dojo.get("detail"),
            "version": lean_dojo.get("version"),
        },
        "dependency_conflicts": list(doctor.get("conflicts", [])),
    }


def _next_hypotheses(reports: dict[str, dict]) -> list[dict]:
    hypotheses = [
        {
            "id": "public_base_release_process",
            "claim": "Public/base release remains ready after publication steps.",
            "test": 'Push/merge/tag the current commits, then rerun release-profile-analysis and release-readiness --profile public.',
            "expected_result": "base_public claim remains ready and dirty_worktree remains false.",
        }
    ]
    if reports["backend"]["status"] == "not_ready":
        hypotheses.append(
            {
                "id": "backend_env_readiness",
                "claim": "A configured isolated backend environment makes the backend profile ready or exposes a real backend defect.",
                "test": "Set MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends with a working Lean toolchain cache, then rerun release-readiness --profile backend.",
                "expected_result": "backend profile has no backend_lean_dojo_unavailable blocker.",
            }
        )
    if reports["private-corpus"]["status"] == "not_ready":
        hypotheses.append(
            {
                "id": "private_corpus_manifest_readiness",
                "claim": "An external sanitized/private manifest satisfies private-corpus release gates without path leaks.",
                "test": "Set MATHDEVMCP_PRIVATE_CORPUS_MANIFEST to an external manifest and rerun validate-private-corpus plus release-readiness --profile private-corpus.",
                "expected_result": "private-corpus profile has no private_corpus_manifest_required blocker and output redacts private paths.",
            }
        )
    if reports["full"]["status"] == "not_ready":
        hypotheses.append(
            {
                "id": "full_profile_readiness",
                "claim": "Full internal release readiness follows only after backend, LaTeXML, and private-corpus profiles all pass.",
                "test": "Provide all strict external evidence and rerun release-readiness --profile full.",
                "expected_result": "full profile is ready or reports only newly surfaced strict-profile defects.",
            }
        )
    return hypotheses
