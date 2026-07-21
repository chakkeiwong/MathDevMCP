from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Mapping

from .backend_env import BackendConfig, backend_bin, backend_subprocess_env
from .contracts import attach_contract


@dataclass(frozen=True)
class LeanCheckResult:
    status: str
    reason: str
    evidence: list[dict]


@dataclass(frozen=True)
class LeanTargetBinding:
    """Exact initial-scope binding from one branch target to one Lean theorem."""

    branch_id: str
    normalized_target: str
    typed_assumptions: tuple[dict[str, Any], ...]
    theorem_name: str
    theorem_binders: tuple[str, ...]
    theorem_statement: str
    imports: tuple[str, ...]
    source_sha256: str
    project_root: str
    lean_toolchain: str
    executable_path: str
    executable_version: str


@dataclass(frozen=True)
class LeanDiagnosticContext:
    """Verified local Lean file/goal prerequisite for diagnostic integrations."""

    lean_file: str
    source_sha256: str
    project_root: str
    lean_toolchain: str
    goal: str
    goal_digest: str
    binding_status: str = "verified"


LEAN_TARGET_BINDING_SCHEMA = "p05_lean_target_binding@1"
LEAN_TARGET_BINDING_BOUNDARY = (
    "This record binds one exact Lean declaration to one normalized branch "
    "target and typed assumption set. It is not a certificate until the exact "
    "source is accepted by the bound executable/project/toolchain and a live "
    "manifest verifies."
)
_PLACEHOLDER_MARKERS = (
    "sorry",
    "admit",
    "by?",
    "exact?",
    "apply?",
    "simp?",
    "aesop?",
    "omega?",
    "?_",
)
_IDENTIFIER_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'.")
_LEAN_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_'.]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _lean_path(explicit: str | None = None, backend_config: BackendConfig | None = None) -> str | None:
    if explicit:
        return explicit
    configured = backend_bin("lean", backend_config)
    if configured is not None:
        return configured
    env_path = os.environ.get("PATH", "")
    elan_bin = str(Path.home() / ".elan" / "bin")
    path = f"{elan_bin}:{env_path}"
    return shutil.which("lean", path=path)


def _source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def _uses_placeholder(source: str) -> bool:
    """Detect Lean placeholder tokens outside comments, strings, and identifiers.

    This is a conservative scanner, not a full Lean lexer. Its job is to avoid
    obvious false positives such as comments and identifiers while preserving
    the safety rule that actual `sorry`/`admit` tokens cannot certify a proof.
    """
    index = 0
    length = len(source)
    block_comment_depth = 0
    in_string = False
    while index < length:
        current = source[index]
        nxt = source[index + 1] if index + 1 < length else ""

        if block_comment_depth:
            if current == "/" and nxt == "-":
                block_comment_depth += 1
                index += 2
                continue
            if current == "-" and nxt == "/":
                block_comment_depth -= 1
                index += 2
                continue
            index += 1
            continue

        if in_string:
            if current == "\\":
                index += 2
                continue
            if current == '"':
                in_string = False
            index += 1
            continue

        if current == "-" and nxt == "-":
            newline = source.find("\n", index + 2)
            if newline == -1:
                break
            index = newline + 1
            continue
        if current == "/" and nxt == "-":
            block_comment_depth = 1
            index += 2
            continue
        if current == '"':
            in_string = True
            index += 1
            continue

        for marker in _PLACEHOLDER_MARKERS:
            if source.startswith(marker, index):
                before = source[index - 1] if index > 0 else ""
                after_index = index + len(marker)
                after = source[after_index] if after_index < length else ""
                if before not in _IDENTIFIER_CHARS and after not in _IDENTIFIER_CHARS:
                    return True
        index += 1
    return False


def _lean_code_only(source: str) -> str:
    """Blank comments and strings while preserving token separation and lines."""
    output = list(source)
    index = 0
    block_comment_depth = 0
    in_string = False
    while index < len(source):
        current = source[index]
        nxt = source[index + 1] if index + 1 < len(source) else ""
        if block_comment_depth:
            if current == "/" and nxt == "-":
                output[index] = output[index + 1] = " "
                block_comment_depth += 1
                index += 2
                continue
            if current == "-" and nxt == "/":
                output[index] = output[index + 1] = " "
                block_comment_depth -= 1
                index += 2
                continue
            if current != "\n":
                output[index] = " "
            index += 1
            continue
        if in_string:
            if current == "\\":
                output[index] = " "
                if index + 1 < len(source):
                    output[index + 1] = " "
                index += 2
                continue
            if current == '"':
                output[index] = " "
                in_string = False
            elif current != "\n":
                output[index] = " "
            index += 1
            continue
        if current == "-" and nxt == "-":
            output[index] = output[index + 1] = " "
            index += 2
            while index < len(source) and source[index] != "\n":
                output[index] = " "
                index += 1
            continue
        if current == "/" and nxt == "-":
            output[index] = output[index + 1] = " "
            block_comment_depth = 1
            index += 2
            continue
        if current == '"':
            output[index] = " "
            in_string = True
        index += 1
    return "".join(output)


def _lean_version(lean: str, *, environment: dict[str, str] | None = None) -> str:
    try:
        completed = subprocess.run(
            [lean, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
            env=environment or backend_subprocess_env(),
        )
    except Exception:
        return "unavailable"
    return (completed.stdout or completed.stderr).strip()


def _lean_environment_failure(output: str) -> bool:
    lowered = output.lower()
    markers = (
        "error during download",
        "could not resolve host",
        "could not resolve hostname",
        "connection refused",
        "failed to download",
        "toolchain",
    )
    return any(marker in lowered for marker in markers)


def _evidence(
    kind: str,
    *,
    command: list[str],
    source: str,
    uses_sorry: bool,
    lean_version: str,
    project_root: str | None,
    lean_toolchain: str | None,
    returncode: int | None = None,
    stdout: str = "",
    stderr: str = "",
    reason: str,
) -> dict:
    return {
        "kind": kind,
        "backend": "lean",
        "backend_status": kind.removeprefix("lean_"),
        "reason": reason,
        "command": command,
        "returncode": returncode,
        "stdout": stdout[-2000:],
        "stderr": stderr[-2000:],
        "uses_sorry": uses_sorry,
        "source_sha256": _source_hash(source),
        "lean_version": lean_version,
        "executable_realpath": os.path.realpath(command[0]) if command and Path(command[0]).is_absolute() else command[0] if command else None,
        "project_root": project_root,
        "lean_toolchain": lean_toolchain,
        "severity": "certifying" if kind == "lean_verified" else ("blocking" if kind == "lean_failed" else "diagnostic"),
        "evidence_kind": "deterministic_backend",
        "diagnostic_only": kind not in {"lean_verified", "lean_failed"},
        "certificate": {"backend": "lean", "source_sha256": _source_hash(source)} if kind == "lean_verified" else None,
        "verification_boundary": "Lean accepted the source without placeholders." if kind == "lean_verified" else reason,
    }


def _normalize_lean_text(value: str) -> str:
    return " ".join(value.split())


def validate_lean_diagnostic_context(context: LeanDiagnosticContext) -> dict[str, Any]:
    errors: list[str] = []
    project = Path(context.project_root)
    lean_file = Path(context.lean_file)
    project_real = os.path.realpath(project)
    file_real = os.path.realpath(lean_file)
    if context.binding_status != "verified":
        errors.append("diagnostic Lean context binding_status must be verified")
    if not project.is_absolute() or not project.is_dir():
        errors.append("diagnostic project_root must be an existing absolute directory")
    if not lean_file.is_absolute() or not lean_file.is_file():
        errors.append("diagnostic lean_file must be an existing absolute file")
    elif os.path.commonpath([project_real, file_real]) != project_real:
        errors.append("diagnostic lean_file must be inside project_root")
    else:
        try:
            observed_source_digest = hashlib.sha256(lean_file.read_bytes()).hexdigest()
        except OSError:
            observed_source_digest = ""
        if observed_source_digest != context.source_sha256:
            errors.append("diagnostic Lean source digest mismatch")
    toolchain_path = project / "lean-toolchain"
    if not toolchain_path.is_file():
        errors.append("diagnostic project has no lean-toolchain file")
    else:
        try:
            observed_toolchain = toolchain_path.read_text(encoding="utf-8").strip()
        except OSError:
            observed_toolchain = ""
        if observed_toolchain != context.lean_toolchain:
            errors.append("diagnostic lean-toolchain mismatch")
    normalized_goal = _normalize_lean_text(context.goal)
    if not normalized_goal:
        errors.append("diagnostic Lean goal must be non-empty")
    expected_goal_digest = hashlib.sha256(normalized_goal.encode("utf-8")).hexdigest()
    if context.goal_digest != expected_goal_digest:
        errors.append("diagnostic Lean goal digest mismatch")
    return {
        "status": "verified" if not errors else "invalid",
        "errors": errors,
        "can_execute_diagnostic_route": not errors,
        "record": {
            "lean_file": file_real,
            "source_sha256": context.source_sha256,
            "project_root": project_real,
            "lean_toolchain": context.lean_toolchain,
            "goal": normalized_goal,
            "goal_digest": context.goal_digest,
            "binding_status": context.binding_status,
        },
        "boundary": "A verified local Lean goal permits diagnostic tool use only; it is not proof.",
    }


def _binding_digest_payload(binding: LeanTargetBinding) -> dict[str, Any]:
    return {
        "schema_version": LEAN_TARGET_BINDING_SCHEMA,
        "branch_id": binding.branch_id,
        "normalized_target": _normalize_lean_text(binding.normalized_target),
        "typed_assumptions": [dict(item) for item in binding.typed_assumptions],
        "theorem_name": binding.theorem_name,
        "theorem_binders": list(binding.theorem_binders),
        "theorem_statement": _normalize_lean_text(binding.theorem_statement),
        "imports": list(binding.imports),
        "source_sha256": binding.source_sha256,
        "project_root": os.path.realpath(binding.project_root),
        "lean_toolchain": binding.lean_toolchain,
        "executable_path": os.path.realpath(binding.executable_path),
        "executable_version": binding.executable_version,
    }


def validate_lean_target_binding(source: str, binding: LeanTargetBinding) -> dict[str, Any]:
    """Validate an exact, deliberately narrow Lean theorem binding."""
    errors: list[str] = []
    if not isinstance(source, str) or not source.strip():
        errors.append("Lean source must be non-empty")
    if not isinstance(binding.branch_id, str) or not binding.branch_id:
        errors.append("branch_id must be non-empty")
    if not _LEAN_IDENTIFIER.fullmatch(binding.theorem_name):
        errors.append("theorem_name is not a supported Lean identifier")
    if not _SHA256.fullmatch(binding.source_sha256):
        errors.append("source_sha256 is invalid")
    elif _source_hash(source) != binding.source_sha256:
        errors.append("Lean source digest does not match the binding")
    normalized_target = _normalize_lean_text(binding.normalized_target)
    normalized_statement = _normalize_lean_text(binding.theorem_statement)
    if not normalized_target or normalized_target != normalized_statement:
        errors.append("theorem_statement does not exactly match normalized_target")
    if normalized_statement in {"True", "False"}:
        errors.append("placeholder theorem shapes True/False are outside certifying scope")
    if _uses_placeholder(source):
        errors.append("Lean source contains a reviewed placeholder or suggestion token")

    if any(not isinstance(item, dict) for item in binding.typed_assumptions):
        errors.append("typed_assumptions must contain objects")
    assumption_binders: list[str] = []
    for item in binding.typed_assumptions:
        binder = item.get("lean_binder") if isinstance(item, dict) else None
        if not isinstance(binder, str) or not binder.strip():
            errors.append("every typed assumption must bind an exact lean_binder")
            continue
        assumption_binders.append(_normalize_lean_text(binder))
    declared_binders = [_normalize_lean_text(item) for item in binding.theorem_binders]
    if assumption_binders != declared_binders:
        errors.append("typed assumption binders do not exactly match theorem_binders")

    code_only = _lean_code_only(source)
    import_lines = [
        _normalize_lean_text(line.strip().removeprefix("import "))
        for line in code_only.splitlines()
        if line.strip().startswith("import ")
    ]
    expected_imports = [_normalize_lean_text(item) for item in binding.imports]
    if import_lines != expected_imports:
        errors.append("Lean import list does not exactly match the binding")
    expected_head = _normalize_lean_text(
        " ".join(
            [
                "theorem",
                binding.theorem_name,
                *binding.theorem_binders,
                ":",
                binding.theorem_statement,
                ":=",
            ]
        )
    )
    normalized_source = _normalize_lean_text(code_only)
    if expected_head not in normalized_source:
        errors.append("bound theorem declaration head is absent or changed")
    declaration_names = re.findall(
        r"\b(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_'.]*)", code_only
    )
    example_count = len(re.findall(r"\bexample\s*:", code_only))
    if example_count or len(declaration_names) != 1 or declaration_names[0] != binding.theorem_name:
        errors.append("source must contain exactly the one bound named theorem")

    project_root = Path(binding.project_root)
    if not project_root.is_absolute() or not project_root.is_dir():
        errors.append("project_root must be an existing absolute directory")
    else:
        toolchain_path = project_root / "lean-toolchain"
        if not toolchain_path.is_file():
            errors.append("project_root has no lean-toolchain file")
        else:
            try:
                observed_toolchain = toolchain_path.read_text(encoding="utf-8").strip()
            except OSError:
                observed_toolchain = ""
            if observed_toolchain != binding.lean_toolchain:
                errors.append("lean-toolchain content does not match the binding")
    executable = Path(binding.executable_path)
    if not executable.is_absolute() or not executable.is_file() or not os.access(executable, os.X_OK):
        errors.append("executable_path must be an existing executable absolute file")
    if not isinstance(binding.executable_version, str) or not binding.executable_version:
        errors.append("executable_version must be non-empty")

    payload = _binding_digest_payload(binding)
    payload["typed_assumption_digest"] = hashlib.sha256(
        json.dumps(
            payload["typed_assumptions"],
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    payload["binding_digest"] = hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": LEAN_TARGET_BINDING_SCHEMA,
        "status": "bound" if not errors else "binding_error",
        "errors": errors,
        "record": payload,
        "can_certify": not errors,
        "boundary": LEAN_TARGET_BINDING_BOUNDARY,
    }


def lean_execution_matches_binding(
    result: Mapping[str, Any], binding_record: Mapping[str, Any]
) -> bool:
    """Check that one raw Lean result came from the exact bound process route."""
    if result.get("status") != "verified":
        return False
    evidence = result.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != 1 or not isinstance(evidence[0], dict):
        return False
    item = evidence[0]
    command = item.get("command")
    return bool(
        item.get("kind") == "lean_verified"
        and item.get("returncode") == 0
        and item.get("uses_sorry") is False
        and item.get("source_sha256") == binding_record.get("source_sha256")
        and isinstance(command, list)
        and command
        and os.path.realpath(command[0]) == binding_record.get("executable_path")
        and item.get("executable_realpath") == binding_record.get("executable_path")
        and item.get("lean_version") == binding_record.get("executable_version")
        and item.get("project_root") == binding_record.get("project_root")
        and item.get("lean_toolchain") == binding_record.get("lean_toolchain")
    )


def check_lean_source(
    source: str,
    *,
    timeout_seconds: int = 10,
    allow_sorry: bool = False,
    executable: str | None = None,
    project_root: str | None = None,
    lean_toolchain: str | None = None,
    backend_config: BackendConfig | None = None,
) -> dict:
    lean = _lean_path(executable, backend_config)
    uses_sorry = _uses_placeholder(source)
    resolved_project_root = os.path.realpath(project_root) if project_root else None
    environment = backend_subprocess_env(backend_config)
    if lean_toolchain:
        environment["ELAN_TOOLCHAIN"] = lean_toolchain
    if lean is None:
        evidence = _evidence(
            "lean_unavailable",
            command=["lean", "<tempfile>"],
            source=source,
            uses_sorry=uses_sorry,
            lean_version="unavailable",
            project_root=resolved_project_root,
            lean_toolchain=lean_toolchain,
            reason="Lean executable was not found.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    version = _lean_version(lean, environment=environment)
    if uses_sorry and not allow_sorry:
        evidence = _evidence(
            "lean_placeholder",
            command=[lean, "<not-run>"],
            source=source,
            uses_sorry=True,
            lean_version=version,
            project_root=resolved_project_root,
            lean_toolchain=lean_toolchain,
            reason="Lean source contains a placeholder proof and certified mode disallows placeholders.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    with tempfile.TemporaryDirectory(prefix="mathdevmcp-lean-") as tmp:
        lean_file = Path(tmp) / "Check.lean"
        lean_file.write_text(source, encoding="utf-8")
        command = [lean, str(lean_file)]
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=environment,
                cwd=resolved_project_root,
            )
        except FileNotFoundError:
            evidence = _evidence(
                "lean_unavailable",
                command=command,
                source=source,
                uses_sorry=uses_sorry,
                lean_version=version,
                project_root=resolved_project_root,
                lean_toolchain=lean_toolchain,
                reason="Lean executable was not found.",
            )
            return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")
        except subprocess.TimeoutExpired:
            evidence = _evidence(
                "lean_timeout",
                command=command,
                source=source,
                uses_sorry=uses_sorry,
                lean_version=version,
                project_root=resolved_project_root,
                lean_toolchain=lean_toolchain,
                reason=f"Lean check timed out after {timeout_seconds} seconds.",
            )
            return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    if completed.returncode == 0 and not uses_sorry:
        evidence = _evidence(
            "lean_verified",
            command=command,
            source=source,
            uses_sorry=False,
            lean_version=version,
            project_root=resolved_project_root,
            lean_toolchain=lean_toolchain,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean accepted the source without placeholder proofs.",
        )
        return attach_contract(asdict(LeanCheckResult("verified", evidence["reason"], [evidence])), "lean_check_result")
    if completed.returncode == 0 and uses_sorry:
        evidence = _evidence(
            "lean_placeholder",
            command=command,
            source=source,
            uses_sorry=True,
            lean_version=version,
            project_root=resolved_project_root,
            lean_toolchain=lean_toolchain,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean accepted the source, but the proof uses a placeholder.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")
    combined_output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if _lean_environment_failure(combined_output):
        evidence = _evidence(
            "lean_unavailable",
            command=command,
            source=source,
            uses_sorry=uses_sorry,
            lean_version=version,
            project_root=resolved_project_root,
            lean_toolchain=lean_toolchain,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean execution failed because the configured toolchain or network-dependent environment is unavailable.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")
    evidence = _evidence(
        "lean_failed",
        command=command,
        source=source,
        uses_sorry=uses_sorry,
        lean_version=version,
        project_root=resolved_project_root,
        lean_toolchain=lean_toolchain,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        reason="Lean rejected the supplied proof artifact.",
    )
    return attach_contract(asdict(LeanCheckResult("mismatch", evidence["reason"], [evidence])), "lean_check_result")
