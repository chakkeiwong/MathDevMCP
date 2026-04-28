from __future__ import annotations

from dataclasses import asdict, dataclass
import os
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
    timeout_seconds: float
    dojo_requested: bool


def _environment() -> dict:
    doctor = doctor_report()
    return {
        "python_executable": sys.executable,
        "lean": doctor["capabilities"].get("lean", {}),
        "lean_dojo": doctor["capabilities"].get("lean_dojo", {}),
        "lake": {"path": shutil.which("lake"), "status": "available" if shutil.which("lake") else "unavailable"},
    }


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _timeout_seconds(value: float | None) -> float:
    if value is not None:
        return value
    raw = os.environ.get("MATHDEVMCP_LEANDOJO_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return 30.0
    try:
        parsed = float(raw)
    except ValueError:
        return 30.0
    return max(1.0, parsed)


def attempt_leandojo_tiny_theorem(
    *,
    traced_repo_path: str | None = None,
    theorem_name: str | None = None,
    lean_source: str | None = None,
    tactic_script: list[str] | None = None,
    run_dojo: bool = False,
    timeout_seconds: float | None = None,
) -> dict:
    traced_repo_path = traced_repo_path or os.environ.get("MATHDEVMCP_LEANDOJO_FIXTURE", "").strip() or None
    theorem_name = theorem_name or os.environ.get("MATHDEVMCP_LEANDOJO_THEOREM", "").strip() or None
    run_dojo = run_dojo or _env_flag("MATHDEVMCP_LEANDOJO_RUN_DOJO")
    timeout = _timeout_seconds(timeout_seconds)
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
            timeout_seconds=timeout,
            dojo_requested=False,
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
            timeout_seconds=timeout,
            dojo_requested=True,
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
            timeout_seconds=timeout,
            dojo_requested=True,
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
            timeout_seconds=timeout,
            dojo_requested=True,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    final = check_lean_source(lean_source, allow_sorry=False) if lean_source else None
    result = LeanDojoAttemptResult(
        status="inconclusive",
        reason="Traced repository metadata exists, but the release-candidate backend still treats real Dojo(entry) proof search as unvalidated until a pinned local integration fixture is added.",
        environment=environment,
        traced_repo_target=target,
        tactic_trace=tactic_script or [],
        final_lean_check=final,
        required_artifacts=required,
        timeout_seconds=timeout,
        dojo_requested=True,
    )
    return attach_contract(asdict(result), "leandojo_attempt_result")
