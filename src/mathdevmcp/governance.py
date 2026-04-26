from __future__ import annotations

from .contracts import attach_contract


def governance_policy() -> dict:
    policy = {
        "external_command_policy": {
            "allowlist": ["latexml", "pandoc", "lean", "lake", "sage"],
            "timeout_required": True,
            "structured_failure_required": True,
        },
        "private_corpus_policy": {
            "no_private_documents_in_git": True,
            "commit_only_manifest_stubs": True,
            "no_exfiltration": "Private source documents and code should not be sent to external services by MathDevMCP workflows.",
        },
        "artifact_policy": {
            "generated_lean_skeletons_are_not_certificates": True,
            "numeric_diagnostics_require_safe_artifacts": True,
            "retain_benchmark_and_doctor_outputs_for_release_reviews": True,
        },
        "verified_claim_policy": {
            "requires_deterministic_backend_evidence": True,
            "diagnostic_evidence_is_not_proof": True,
            "expected_abstention_is_quality_signal": True,
        },
    }
    return attach_contract({"status": "consistent", "reason": "Governance policy is available for release review.", "policy": policy}, "governance_policy")
