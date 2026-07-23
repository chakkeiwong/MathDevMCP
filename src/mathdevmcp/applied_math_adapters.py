"""Constrained adapters for ResearchAssistant source discovery and DynareMCP.

The adapters use fixed, read-only operations and injectable runners. They do
not execute arbitrary user code or infer paper/code equivalence.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Callable, Sequence


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def discover_local_source_package(source: str | Path, *, max_candidates: int = 100) -> dict[str, Any]:
    """Find adjacent source/code/data artifacts without network access."""

    path = Path(source).expanduser().resolve()
    root = path.parent
    candidates: list[dict[str, Any]] = []
    allowed = {".tex", ".bib", ".yaml", ".yml", ".mod", ".py", ".jl", ".m", ".csv", ".json"}
    try:
        paths = sorted(item for item in root.iterdir() if item.is_file() and item.suffix.lower() in allowed)
    except OSError:
        paths = []
    for item in paths:
        if item == path or len(candidates) >= max_candidates:
            continue
        try:
            resolved = item.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved != item:
            # Discovery is deliberately local and does not follow links,
            # including links that happen to remain inside the directory.
            continue
        data = item.read_bytes()
        role = "source" if item.suffix.lower() in {".tex", ".bib"} else "code_or_model" if item.suffix.lower() in {".mod", ".py", ".jl", ".m"} else "data_or_config"
        candidates.append(
            {
                "path": str(item),
                "role": role,
                "bytes": len(data),
                "sha256": _sha256_bytes(data),
                "discovery": "local_adjacent",
            }
        )
    return {
        "status": "candidates_found" if candidates else "no_candidates",
        "root": str(root),
        "candidates": candidates,
        "non_claim": "Candidate discovery does not establish that an artifact belongs to the paper or is authoritative.",
    }


@dataclass(frozen=True)
class AdapterOutcome:
    command: tuple[str, ...]
    returncode: int | None
    stdout: str
    stderr: str
    duration_seconds: float
    error: str | None = None


AdapterRunner = Callable[[Sequence[str], dict[str, str], float], AdapterOutcome]


def _default_runner(command: Sequence[str], env: dict[str, str], timeout: float) -> AdapterOutcome:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            tuple(command),
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return AdapterOutcome(
            command=tuple(command),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=round(time.monotonic() - started, 6),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return AdapterOutcome(
            command=tuple(command),
            returncode=None,
            stdout="",
            stderr="",
            duration_seconds=round(time.monotonic() - started, 6),
            error=str(exc),
        )


def run_dynare_source_adapter(
    model_path: str | Path,
    *,
    dynare_root: str | Path | None = None,
    output_root: str | Path | None = None,
    timeout_seconds: float = 120.0,
    runner: AdapterRunner | None = None,
) -> dict[str, Any]:
    """Invoke only fixed read-only DynareMCP source operations."""

    path = Path(model_path).expanduser().resolve()
    if path.suffix.lower() != ".mod":
        return {"status": "not_applicable", "operations": [], "path": str(path)}
    if not path.is_file():
        return {"status": "abstention", "reason": "model path is not a file", "path": str(path)}
    root = Path(dynare_root or (Path.home() / "python" / "DynareMCP")).expanduser().resolve()
    if not (root / "src" / "dynaremcp").is_dir():
        return {"status": "abstention", "reason": "DynareMCP source checkout unavailable", "path": str(path)}
    source_bytes = path.read_bytes()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + env.get("PYTHONPATH", "")
    output = Path(output_root or ".mathdevmcp/applied_math_specialists").expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    operations = ("analyze-model-source", "extract-symbol-table", "list-equations", "inspect-timing")
    results: list[dict[str, Any]] = []
    command_runner = runner or _default_runner
    for operation in operations:
        if operation in {"extract-symbol-table", "list-equations"}:
            command = (sys.executable, "-m", "dynaremcp.cli", operation, "--model-path", str(path))
        else:
            command = (sys.executable, "-m", "dynaremcp.cli", operation, str(path))
        if operation == "analyze-model-source":
            command += ("--output-root", str(output))
        outcome = command_runner(command, env, timeout_seconds)
        output_bytes = outcome.stdout.encode("utf-8")
        record: dict[str, Any] = {
            "operation": operation,
            "command": list(command),
            "status": "ok" if outcome.returncode == 0 else "abstention",
            "returncode": outcome.returncode,
            "duration_seconds": outcome.duration_seconds,
            "input": {"path": str(path), "sha256": _sha256_bytes(source_bytes)},
            "output": {"sha256": _sha256_bytes(output_bytes), "bytes": len(output_bytes)},
            "provider": {"name": "DynareMCP", "root": str(root), "operation": operation},
            "non_claim": "DynareMCP source diagnostics do not establish paper/code semantic equivalence.",
        }
        if outcome.error:
            record["error"] = outcome.error
        if outcome.returncode == 0:
            try:
                record["payload"] = json.loads(outcome.stdout)
            except json.JSONDecodeError:
                record["payload"] = {"raw_text": outcome.stdout[:10000]}
        else:
            record["error"] = (outcome.error or outcome.stderr or "provider returned nonzero status")[:1000]
        results.append(record)
    return {
        "status": "completed" if all(item["status"] == "ok" for item in results) else "completed_with_abstentions",
        "path": str(path),
        "operations": results,
        "non_claim": "Successful source diagnostics do not prove mathematical correctness or model equivalence.",
    }
