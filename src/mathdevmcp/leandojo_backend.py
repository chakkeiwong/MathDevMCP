from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shutil
import sys

from .contracts import attach_contract
from .doctor import doctor_report
from .lean_check import check_lean_source


@dataclass(frozen=True)
class LeanDojoAttemptResult:
    status: str
    reason: str
    environment: dict
    traced_repo_target: dict | None
    tactic_trace: list[str]
    final_lean_check: dict | None
    required_artifacts: list[str]


def _environment() -> dict:
    doctor = doctor_report()
    return {
        "python_executable": sys.executable,
        "lean": doctor["capabilities"].get("lean", {}),
        "lean_dojo": doctor["capabilities"].get("lean_dojo", {}),
        "lake": {"path": shutil.which("lake"), "status": "available" if shutil.which("lake") else "unavailable"},
    }


def attempt_leandojo_tiny_theorem(
    *,
    traced_repo_path: str | None = None,
    theorem_name: str | None = None,
    lean_source: str | None = None,
    tactic_script: list[str] | None = None,
    run_dojo: bool = False,
) -> dict:
    environment = _environment()
    required = [
        "LeanDojo import/API availability",
        "pinned Lean/Lake toolchain",
        "traced repository path",
        "theorem entry name",
        "bounded tactic script",
        "direct Lean final check artifact",
    ]
    target = {"path": traced_repo_path, "theorem": theorem_name} if traced_repo_path or theorem_name else None
    if not run_dojo:
        final = check_lean_source(lean_source, allow_sorry=False) if lean_source else None
        result = LeanDojoAttemptResult(
            status="inconclusive",
            reason="Real Dojo(entry) interaction was not requested; this is a policy/readiness boundary.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=final,
            required_artifacts=required,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    if not traced_repo_path or not theorem_name:
        result = LeanDojoAttemptResult(
            status="inconclusive",
            reason="Real Dojo(entry) interaction requires a traced repository path and theorem entry.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=None,
            required_artifacts=required,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    if environment["lean_dojo"].get("status") != "available":
        result = LeanDojoAttemptResult(
            status="inconclusive",
            reason="LeanDojo is unavailable in this Python environment.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=None,
            required_artifacts=required,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    if not Path(traced_repo_path).exists():
        result = LeanDojoAttemptResult(
            status="inconclusive",
            reason="Configured traced repository path does not exist.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=None,
            required_artifacts=required,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    final = check_lean_source(lean_source, allow_sorry=False) if lean_source else None
    result = LeanDojoAttemptResult(
        status="inconclusive",
        reason="Traced repository metadata exists, but the conservative backend does not run an unbounded Dojo loop without a pinned local integration fixture.",
        environment=environment,
        traced_repo_target=target,
        tactic_trace=tactic_script or [],
        final_lean_check=final,
        required_artifacts=required,
    )
    return attach_contract(asdict(result), "leandojo_attempt_result")
