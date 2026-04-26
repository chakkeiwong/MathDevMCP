from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.util
from pathlib import Path
import tempfile
import time

from .contracts import attach_contract
from .lean_check import check_lean_source


@dataclass(frozen=True)
class LeanDojoSpikeResult:
    status: str
    reason: str
    theorem_name: str
    tactic_trace: list[dict]
    proof_source: str
    direct_check: dict | None
    runtime_seconds: float
    details: dict


def _unavailable(reason: str, started: float, details: dict | None = None) -> dict:
    result = LeanDojoSpikeResult(
        status="inconclusive",
        reason=reason,
        theorem_name="",
        tactic_trace=[],
        proof_source="",
        direct_check=None,
        runtime_seconds=time.perf_counter() - started,
        details=details or {},
    )
    return attach_contract(asdict(result), "leandojo_spike_result")


def leandojo_import_smoke() -> dict:
    started = time.perf_counter()
    if importlib.util.find_spec("lean_dojo") is None:
        return _unavailable("LeanDojo is not importable.", started)
    try:
        import lean_dojo
        from lean_dojo import Dojo, LeanGitRepo, Theorem
    except Exception as exc:
        return _unavailable(f"LeanDojo import failed: {exc}", started)
    result = LeanDojoSpikeResult(
        status="available",
        reason="LeanDojo imports and exposes core interaction classes.",
        theorem_name="",
        tactic_trace=[],
        proof_source="",
        direct_check=None,
        runtime_seconds=time.perf_counter() - started,
        details={
            "version": getattr(lean_dojo, "__version__", "unknown"),
            "has_dojo": Dojo is not None,
            "has_repo": LeanGitRepo is not None,
            "has_theorem": Theorem is not None,
        },
    )
    return attach_contract(asdict(result), "leandojo_spike_result")


def leandojo_tiny_proof_spike() -> dict:
    started = time.perf_counter()
    smoke = leandojo_import_smoke()
    if smoke["status"] != "available":
        return smoke
    proof_source = """theorem mathdevmcp_leandojo_tiny (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
"""
    direct = check_lean_source(proof_source)
    result = LeanDojoSpikeResult(
        status="verified" if direct["status"] == "verified" else "inconclusive",
        reason="Direct Lean verified the tiny proof; real Dojo interaction still needs a traced repository target.",
        theorem_name="mathdevmcp_leandojo_tiny",
        tactic_trace=[{"tactic": "exact Nat.add_comm a b", "status": direct["status"]}],
        proof_source=proof_source,
        direct_check=direct,
        runtime_seconds=time.perf_counter() - started,
        details={
            "leandojo_import": smoke["details"],
            "dojo_interaction": "not_run_without_traced_repo",
            "next_requirement": "Create or trace a Lean repository theorem target before invoking Dojo(entry).",
        },
    )
    return attach_contract(asdict(result), "leandojo_spike_result")
