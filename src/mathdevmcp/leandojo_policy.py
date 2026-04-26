from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract
from .leandojo_spike import leandojo_import_smoke


@dataclass(frozen=True)
class LeanDojoBackendPolicy:
    status: str
    reason: str
    import_smoke: dict
    required_artifacts: list[str]
    final_certificate_policy: str


def leandojo_backend_policy(*, traced_repo_available: bool = False, run_import_smoke: bool = True) -> dict:
    smoke = leandojo_import_smoke() if run_import_smoke else {
        "status": "not_run",
        "reason": "LeanDojo import smoke was skipped for a policy-only check.",
        "details": {},
    }
    required = [
        "pinned Lean/Lake toolchain",
        "traced Lean repository target",
        "theorem entry compatible with LeanDojo",
        "bounded tactic script",
        "direct Lean final check artifact",
    ]
    if smoke["status"] == "not_run":
        status = "inconclusive"
        reason = "LeanDojo policy requires a separate import smoke and traced repository theorem target before Dojo(entry)."
    elif smoke["status"] != "available":
        status = "inconclusive"
        reason = "LeanDojo import/API readiness is unavailable."
    elif not traced_repo_available:
        status = "inconclusive"
        reason = "LeanDojo imports, but no traced repository theorem target is available for Dojo(entry)."
    else:
        status = "dojo_ready_candidate"
        reason = "LeanDojo import readiness and traced repository target are available; direct Lean final check is still required."
    result = LeanDojoBackendPolicy(
        status=status,
        reason=reason,
        import_smoke=smoke,
        required_artifacts=required,
        final_certificate_policy="Any LeanDojo proof script must be reconstructed and accepted by a direct Lean final check with placeholders disallowed.",
    )
    return attach_contract(asdict(result), "leandojo_backend_policy")
