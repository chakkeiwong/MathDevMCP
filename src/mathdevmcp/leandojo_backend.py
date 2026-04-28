from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import shutil
import sys
import time

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
    readiness: dict
    dojo_evidence: dict | None


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


def _leandojo_import_details() -> dict:
    try:
        import lean_dojo
        from lean_dojo import Dojo, LeanGitRepo, Theorem, TracedRepo, trace
    except Exception as exc:
        return {
            "available": False,
            "version": None,
            "error": f"{type(exc).__name__}: {exc}",
            "has_dojo": False,
            "has_repo": False,
            "has_theorem": False,
            "has_traced_repo": False,
            "has_trace": False,
        }
    return {
        "available": True,
        "version": getattr(lean_dojo, "__version__", "unknown"),
        "error": None,
        "has_dojo": Dojo is not None,
        "has_repo": LeanGitRepo is not None,
        "has_theorem": Theorem is not None,
        "has_traced_repo": TracedRepo is not None,
        "has_trace": trace is not None,
    }


def _fixture_details(path: str | None, theorem_name: str | None) -> dict:
    if not path:
        return {
            "available": False,
            "path": None,
            "theorem": theorem_name,
            "missing": ["traced repository path"],
            "lean_files": [],
        }
    root = Path(path)
    expected = ["lean-toolchain", "lakefile.lean"]
    missing = [name for name in expected if not (root / name).exists()]
    lean_files = sorted(str(item.relative_to(root)) for item in root.glob("*.lean")) if root.exists() else []
    if not lean_files:
        missing.append("Lean source file")
    if not theorem_name:
        missing.append("theorem entry name")
    return {
        "available": root.exists() and not missing,
        "path": str(root),
        "theorem": theorem_name,
        "missing": missing,
        "lean_files": lean_files,
        "toolchain": (root / "lean-toolchain").read_text(encoding="utf-8").strip() if (root / "lean-toolchain").exists() else None,
    }


def _readiness(
    *,
    import_details: dict,
    fixture_details: dict,
    trace_available: bool = False,
    dojo_entered: bool = False,
    tactics_executed: bool = False,
    final_lean_check: dict | None = None,
) -> dict:
    return {
        "import_available": bool(import_details.get("available")),
        "fixture_available": bool(fixture_details.get("available")),
        "trace_available": trace_available,
        "dojo_entered": dojo_entered,
        "tactics_executed": tactics_executed,
        "final_lean_check_passed": final_lean_check is not None and final_lean_check.get("status") == "verified",
        "leandojo_version": import_details.get("version"),
        "import_error": import_details.get("error"),
        "fixture_missing": fixture_details.get("missing", []),
    }


def _tactic_script(configured: list[str] | None) -> list[str]:
    if configured:
        return configured
    raw = os.environ.get("MATHDEVMCP_LEANDOJO_TACTICS", "").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(";") if item.strip()]


def _status_from_final_check(final: dict | None, *, dojo_entered: bool, tactics_finished: bool) -> tuple[str, str]:
    if final is None:
        return "inconclusive", "No final Lean proof artifact was supplied for direct checking."
    if final.get("status") == "verified" and dojo_entered and tactics_finished:
        return "verified", "LeanDojo tactics finished and the reconstructed Lean proof passed direct Lean checking."
    if final.get("status") == "verified":
        return "inconclusive", "Direct Lean accepted the proof artifact, but real Dojo(entry) proof search was not completed."
    if final.get("status") == "mismatch":
        return "mismatch", "The final Lean proof artifact was rejected by direct Lean checking."
    return "inconclusive", "The final Lean proof artifact did not produce a certificate."


def _attempt_real_dojo(
    *,
    traced_repo_path: str,
    theorem_name: str,
    tactic_script: list[str],
    timeout: float,
) -> dict:
    started = time.perf_counter()
    evidence = {
        "status": "inconclusive",
        "reason": "",
        "trace_available": False,
        "dojo_entered": False,
        "tactics_executed": False,
        "tactic_trace": [],
        "runtime_seconds": 0.0,
        "error": None,
    }
    if not tactic_script:
        evidence["reason"] = "No bounded tactic script was supplied."
        evidence["runtime_seconds"] = time.perf_counter() - started
        return evidence
    try:
        from lean_dojo import Dojo, LeanGitRepo, Theorem, trace
    except Exception as exc:
        evidence["reason"] = "LeanDojo import failed before Dojo(entry)."
        evidence["error"] = f"{type(exc).__name__}: {exc}"
        evidence["runtime_seconds"] = time.perf_counter() - started
        return evidence
    try:
        repo = LeanGitRepo.from_path(traced_repo_path)
        trace(repo, dst_dir=os.environ.get("MATHDEVMCP_LEANDOJO_TRACE_DIR") or None, build_deps=False)
        evidence["trace_available"] = True
        theorem_file = Path(os.environ.get("MATHDEVMCP_LEANDOJO_FILE", "MathDevMCPDemo.lean"))
        theorem = Theorem(repo, theorem_file, theorem_name)
        with Dojo(theorem, timeout=int(timeout), build_deps=False) as (dojo, state):
            evidence["dojo_entered"] = True
            current = state
            for tactic in tactic_script:
                result = dojo.run_tac(current, tactic)
                item = {"tactic": tactic, "result_type": type(result).__name__, "state": str(result)[:1000]}
                evidence["tactic_trace"].append(item)
                if type(result).__name__ == "ProofFinished":
                    evidence["tactics_executed"] = True
                    evidence["status"] = "finished"
                    evidence["reason"] = "LeanDojo accepted the bounded tactic script."
                    break
                if type(result).__name__ == "LeanError":
                    evidence["reason"] = "LeanDojo returned a Lean error for the tactic script."
                    break
                current = result
            else:
                evidence["tactics_executed"] = bool(evidence["tactic_trace"])
                evidence["reason"] = "LeanDojo tactic script ended before proof completion."
    except Exception as exc:
        evidence["reason"] = "Real Dojo(entry) interaction could not be completed in this environment."
        evidence["error"] = f"{type(exc).__name__}: {exc}"
    evidence["runtime_seconds"] = time.perf_counter() - started
    return evidence


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
    import_details = _leandojo_import_details()
    fixture = _fixture_details(traced_repo_path, theorem_name)
    tactic_script = _tactic_script(tactic_script)
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
        status, reason = _status_from_final_check(final, dojo_entered=False, tactics_finished=False)
        result = LeanDojoAttemptResult(
            status="inconclusive" if status == "verified" else status,
            reason="Real Dojo(entry) interaction was not requested; this is a policy/readiness boundary.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=final,
            required_artifacts=required,
            timeout_seconds=timeout,
            dojo_requested=False,
            readiness=_readiness(import_details=import_details, fixture_details=fixture, final_lean_check=final),
            dojo_evidence=None,
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
            readiness=_readiness(import_details=import_details, fixture_details=fixture),
            dojo_evidence=None,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    if environment["lean_dojo"].get("status") != "available" or not import_details.get("available"):
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
            readiness=_readiness(import_details=import_details, fixture_details=fixture),
            dojo_evidence=None,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    if not fixture["available"]:
        result = LeanDojoAttemptResult(
            status="inconclusive",
            reason="Configured LeanDojo fixture is incomplete.",
            environment=environment,
            traced_repo_target=target,
            tactic_trace=tactic_script or [],
            final_lean_check=None,
            required_artifacts=required,
            timeout_seconds=timeout,
            dojo_requested=True,
            readiness=_readiness(import_details=import_details, fixture_details=fixture),
            dojo_evidence=None,
        )
        return attach_contract(asdict(result), "leandojo_attempt_result")
    final = check_lean_source(lean_source, allow_sorry=False) if lean_source else None
    dojo_evidence = _attempt_real_dojo(
        traced_repo_path=traced_repo_path,
        theorem_name=theorem_name,
        tactic_script=tactic_script,
        timeout=timeout,
    )
    status, reason = _status_from_final_check(
        final,
        dojo_entered=bool(dojo_evidence.get("dojo_entered")),
        tactics_finished=dojo_evidence.get("status") == "finished",
    )
    if status == "inconclusive" and dojo_evidence.get("error"):
        reason = f"{reason} LeanDojo blocker: {dojo_evidence['error']}"
    result = LeanDojoAttemptResult(
        status=status,
        reason=reason,
        environment=environment,
        traced_repo_target=target,
        tactic_trace=dojo_evidence.get("tactic_trace") or tactic_script or [],
        final_lean_check=final,
        required_artifacts=required,
        timeout_seconds=timeout,
        dojo_requested=True,
        readiness=_readiness(
            import_details=import_details,
            fixture_details=fixture,
            trace_available=bool(dojo_evidence.get("trace_available")),
            dojo_entered=bool(dojo_evidence.get("dojo_entered")),
            tactics_executed=bool(dojo_evidence.get("tactics_executed")),
            final_lean_check=final,
        ),
        dojo_evidence=dojo_evidence,
    )
    return attach_contract(asdict(result), "leandojo_attempt_result")
