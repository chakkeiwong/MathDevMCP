"""Parser backend measurement for label preservation and provenance quality."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib
import json
import re
import stat
import subprocess
import tempfile
import time
from typing import Any
import xml.etree.ElementTree as ET

from .backend_env import backend_bin, backend_subprocess_env
from .contracts import attach_contract, contract_metadata
from .evidence_manifest import (
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
)
from .latex_index import build_index


@dataclass(frozen=True)
class ParserBackendResult:
    backend: str
    status: str
    reason: str
    labels_found: int
    environments_found: int
    align_like_found: int
    provenance_quality: str
    runtime_seconds: float
    labels: list[str]
    quality_checks: dict[str, bool]
    details: dict


@dataclass(frozen=True)
class ParserBenchmarkReport:
    ok: bool
    results: list[dict]
    summary: dict[str, int]
    metadata: dict[str, str]


P02_ORACLE_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02r3-"
    "timeout-policy-recovery-oracle-2026-07-12.json"
)
P02_RESULT_ROUND_PARENT = Path(".local/mathdevmcp/evidence/p02r3-20260712/result-rounds")
P02_FIDELITY_FIELDS = (
    "exact_requested_label_set",
    "exact_owner_label_spans",
    "exact_owned_row_spans",
    "exact_excluded_sibling_spans",
    "exact_nested_environment_stack",
    "exact_source_byte_roundtrip",
    "explicit_uncertainty_localization",
)


def _tex_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.tex") if path.is_file())


def _read_all_tex(root: Path) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in _tex_files(root))


def _file_parser_metrics(root: Path) -> dict:
    metrics: dict[str, dict] = {}
    label_pattern = re.compile(r"\\label\{([^}]+)\}")
    env_pattern = re.compile(r"\\begin\{([^}]+)\}")
    include_pattern = re.compile(r"\\(?:input|include)\{([^}]+)\}")
    macro_pattern = re.compile(r"\\(?:newcommand|renewcommand|DeclareMathOperator)\b")
    for path in _tex_files(root):
        text = path.read_text(encoding="utf-8")
        labels = label_pattern.findall(text)
        envs = env_pattern.findall(text)
        relative = str(path.relative_to(root))
        metrics[relative] = {
            "labels": sorted(labels),
            "label_count": len(labels),
            "environment_count": len(envs),
            "environment_type_counts": {env: envs.count(env) for env in sorted(set(envs))},
            "include_targets": include_pattern.findall(text),
            "macro_definition_count": len(macro_pattern.findall(text)),
        }
    return metrics


def _include_status(root: Path, per_file: dict) -> dict:
    all_files = {str(path.relative_to(root)) for path in _tex_files(root)}
    resolved: list[dict] = []
    missing: list[dict] = []
    for relative, metrics in per_file.items():
        parent = root / relative
        for target in metrics.get("include_targets", []):
            candidate = parent.parent / target
            if not candidate.suffix:
                candidate = candidate.with_suffix(".tex")
            item = {
                "from": relative,
                "target": target,
                "resolved": str(candidate.relative_to(root)) if candidate.exists() else None,
            }
            if candidate.exists() and str(candidate.relative_to(root)) in all_files:
                resolved.append(item)
            else:
                missing.append(item)
    return {"mode": "textual_input_order", "resolved": resolved, "missing": missing, "has_includes": bool(resolved or missing)}


def _duplicate_label_findings(per_file: dict) -> list[str]:
    labels: list[str] = []
    for metrics in per_file.values():
        labels.extend(metrics.get("labels", []))
    return sorted(label for label in set(labels) if labels.count(label) > 1)


def _expected_labels(root: Path, expected_labels: Iterable[str] | None = None) -> set[str]:
    if expected_labels is not None:
        return set(expected_labels)
    return set(build_index(root).get("labels", {}).keys())


def _quality(labels: list[str], environments: int, align_like: int, provenance_quality: str, expected_labels: set[str]) -> dict[str, bool]:
    label_set = set(labels)
    return {
        "label_preservation": bool(expected_labels) and expected_labels.issubset(label_set),
        "environment_recognition": environments > 0,
        "align_detection": align_like > 0,
        "provenance_available": provenance_quality in {"line", "file", "source"},
}


def _provenance_score(provenance_quality: str) -> float:
    return {"line": 1.0, "file": 0.75, "source": 0.5, "none": 0.0}.get(provenance_quality, 0.0)


def _result(backend: str, status: str, reason: str, *, expected_labels: set[str] | None = None, labels: list[str] | None = None, environments: int = 0, align_like: int = 0, provenance_quality: str = "none", runtime_seconds: float = 0.0, details: dict | None = None) -> dict:
    raw_labels = labels or []
    label_list = sorted(set(raw_labels))
    expected = expected_labels or set()
    generated_like = sorted(label for label in label_list if label.startswith(("ltxid", "autopage", "auto:", "generated:")))
    missing = sorted(expected - set(label_list))
    recall = (len(expected - set(missing)) / len(expected)) if expected else 0.0
    precision = (len(expected & set(label_list)) / len(label_list)) if label_list else 0.0
    duplicate_labels = sorted(label for label in set(raw_labels) if raw_labels.count(label) > 1)
    environment_types = sorted((details or {}).get("environment_types", []))
    payload = ParserBackendResult(
        backend=backend,
        status=status,
        reason=reason,
        labels_found=len(label_list),
        environments_found=environments,
        align_like_found=align_like,
        provenance_quality=provenance_quality,
        runtime_seconds=runtime_seconds,
        labels=label_list,
        quality_checks=_quality(label_list, environments, align_like, provenance_quality, expected),
        details={
            **(details or {}),
            "expected_labels": sorted(expected),
            "missing_expected_labels": missing,
            "generated_like_labels": generated_like,
            "expected_label_recall": recall,
            "expected_label_precision": precision,
            "provenance_score": _provenance_score(provenance_quality),
            "generated_label_count": len(generated_like),
            "source_span_quality": provenance_quality,
            "section_path_quality": "available" if provenance_quality == "line" else "unknown",
            "macro_visibility": "textual" if backend == "current" else "backend_dependent",
            "environment_types": environment_types,
            "duplicate_label_findings": (details or {}).get("duplicate_label_findings", duplicate_labels),
            "multi_file_coverage": len(_tex_files(Path(details["root"]))) if details and "root" in details else None,
            "fatal_errors": (details or {}).get("errors", []),
            "warnings": (details or {}).get("warnings", []),
            "environment_count": environments,
            "align_like_count": align_like,
        },
    )
    return attach_contract(asdict(payload), "parser_backend_result")


def _current_parser(root: Path, started: float, expected_labels: set[str]) -> dict:
    index = build_index(root)
    blocks = index.get("blocks", [])
    labels = [block.get("label") for block in blocks if block.get("label")]
    per_file = _file_parser_metrics(root)
    environment_types = sorted({block.get("kind") for block in index.get("blocks", []) if block.get("kind")})
    environment_type_counts = {kind: sum(1 for block in blocks if block.get("kind") == kind) for kind in environment_types}
    environments = sum(1 for block in index.get("blocks", []) if block.get("kind") in {"equation", "align", "alignat", "gather", "multline", "theorem", "proposition", "lemma", "assumption"})
    align_like = sum(1 for block in index.get("blocks", []) if block.get("kind") in {"align", "alignat"})
    return _result(
        "current",
        "parsed",
        "Current lightweight parser completed.",
        labels=labels,
        expected_labels=expected_labels,
        environments=environments,
        align_like=align_like,
        provenance_quality="line",
        runtime_seconds=time.perf_counter() - started,
        details={
            "n_blocks": index.get("n_blocks"),
            "n_labels": index.get("n_labels"),
            "environment_types": environment_types,
            "environment_type_counts": environment_type_counts,
            "tex_files_scanned": [str(path.relative_to(root)) for path in _tex_files(root)],
            "per_file_metrics": per_file,
            "include_status": _include_status(root, per_file),
            "macro_summary": {
                "total_macro_definitions": sum(item["macro_definition_count"] for item in per_file.values()),
                "files_with_macros": sorted(path for path, item in per_file.items() if item["macro_definition_count"]),
            },
            "duplicate_label_findings": _duplicate_label_findings(per_file),
            "root": str(root),
        },
    )


def _latexml_parser(root: Path, started: float, expected_labels: set[str]) -> dict:
    latexml = backend_bin("latexml")
    if latexml is None:
        return _result("latexml", "inconclusive", "latexml executable is unavailable.", runtime_seconds=time.perf_counter() - started)
    labels: set[str] = set()
    environments = 0
    align_like = 0
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="mathdevmcp-latexml-") as tmp:
        for tex in _tex_files(root):
            output = Path(tmp) / f"{tex.stem}.xml"
            completed = subprocess.run([latexml, "--quiet", f"--dest={output}", str(tex)], check=False, capture_output=True, text=True, timeout=60, env=backend_subprocess_env())
            if completed.returncode != 0:
                errors.append(f"{tex.name}: {completed.stderr[-500:]}")
                continue
            text = output.read_text(encoding="utf-8") if output.exists() else ""
            labels.update(label for label in expected_labels if label in text)
            environments += len(re.findall(r"<ltx:(?:equation|theorem|para|Math)", text))
            align_like += text.count("align")
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                errors.append(f"{tex.name}: XML parse error {exc}")
    status = "parsed" if labels or environments else "inconclusive"
    return _result(
        "latexml",
        status,
        "LaTeXML parsed at least part of the corpus." if status == "parsed" else "LaTeXML did not recover labels or environments.",
        labels=list(labels),
        expected_labels=expected_labels,
        environments=environments,
        align_like=align_like,
        provenance_quality="source",
        runtime_seconds=time.perf_counter() - started,
        details={"errors": errors[:5], "root": str(root)},
    )


def _pandoc_parser(root: Path, started: float, expected_labels: set[str]) -> dict:
    pandoc = backend_bin("pandoc")
    if pandoc is None:
        return _result("pandoc", "inconclusive", "pandoc executable is unavailable.", runtime_seconds=time.perf_counter() - started)
    labels: set[str] = set()
    environments = 0
    align_like = 0
    errors: list[str] = []
    for tex in _tex_files(root):
        completed = subprocess.run([pandoc, "-f", "latex", "-t", "json", str(tex)], check=False, capture_output=True, text=True, timeout=30, env=backend_subprocess_env())
        if completed.returncode != 0:
            errors.append(f"{tex.name}: {completed.stderr[-500:]}")
            continue
        labels.update(label for label in expected_labels if label in completed.stdout)
        try:
            data = json.loads(completed.stdout)
            blocks = data.get("blocks", [])
            environments += len(blocks)
            text = json.dumps(data)
            align_like += text.count("align")
        except json.JSONDecodeError as exc:
            errors.append(f"{tex.name}: JSON parse error {exc}")
    status = "parsed" if labels or environments else "inconclusive"
    return _result(
        "pandoc",
        status,
        "Pandoc parsed at least part of the corpus." if status == "parsed" else "Pandoc did not recover labels or blocks.",
        labels=list(labels),
        expected_labels=expected_labels,
        environments=environments,
        align_like=align_like,
        provenance_quality="source",
        runtime_seconds=time.perf_counter() - started,
        details={"errors": errors[:5], "root": str(root)},
    )


def run_parser_backend(root: str | Path, backend: str, *, expected_labels: Iterable[str] | None = None) -> dict:
    root = Path(root)
    started = time.perf_counter()
    expected_label_set = _expected_labels(root, expected_labels)
    try:
        if backend == "current":
            return _current_parser(root, started, expected_label_set)
        if backend == "latexml":
            return _latexml_parser(root, started, expected_label_set)
        if backend == "pandoc":
            return _pandoc_parser(root, started, expected_label_set)
    except Exception as exc:
        return _result(backend, "inconclusive", f"{backend} parser failed: {exc}", expected_labels=expected_label_set, runtime_seconds=time.perf_counter() - started)
    return _result(backend, "inconclusive", f"Unknown parser backend: {backend}", expected_labels=expected_label_set, runtime_seconds=time.perf_counter() - started)


def compare_parser_backends(root: str | Path, backends: list[str] | None = None, *, expected_labels: Iterable[str] | None = None) -> dict:
    backend_list = backends or ["current", "latexml", "pandoc"]
    results = [run_parser_backend(root, backend, expected_labels=expected_labels) for backend in backend_list]
    summary = {
        "total": len(results),
        "parsed": sum(1 for result in results if result["status"] == "parsed"),
        "inconclusive": sum(1 for result in results if result["status"] == "inconclusive"),
        "label_preserving": sum(1 for result in results if result["quality_checks"]["label_preservation"]),
        "provenance_available": sum(1 for result in results if result["quality_checks"]["provenance_available"]),
    }
    summary["backend_comparison_matrix"] = {
        result["backend"]: {
            "status": result["status"],
            "labels_found": result["labels_found"],
            "provenance_quality": result["provenance_quality"],
            "missing_expected_labels": result["details"].get("missing_expected_labels", []),
            "role_hint": "candidate_for_proof_audit" if result["backend"] == "current" and result["quality_checks"]["provenance_available"] else "context_or_optional_evidence",
        }
        for result in results
    }
    return asdict(ParserBenchmarkReport(ok=True, results=results, summary=summary, metadata=contract_metadata("parser_benchmark_report")))


def compare_p02_fidelity_vectors(current: Sequence[int], candidate: Sequence[int]) -> dict[str, Any]:
    """Compare the reviewed seven-bit vectors in priority order."""
    left = list(current)
    right = list(candidate)
    if len(left) != len(P02_FIDELITY_FIELDS) or len(right) != len(P02_FIDELITY_FIELDS):
        raise ValueError("Phase 02 fidelity vectors must contain exactly seven bits")
    if any(type(value) is not int or value not in {0, 1} for value in [*left, *right]):
        raise ValueError("Phase 02 fidelity vectors contain only integer bits")
    first_difference = next((index for index, pair in enumerate(zip(left, right, strict=True)) if pair[0] != pair[1]), None)
    if first_difference is None:
        relation = "equal_retain_current"
    elif right[first_difference] > left[first_difference]:
        relation = "candidate_materially_better"
    else:
        relation = "current_materially_better"
    return {
        "schema_version": "p02_fidelity_vector_comparison@1",
        "fields": list(P02_FIDELITY_FIELDS),
        "current": left,
        "candidate": right,
        "first_differing_field": P02_FIDELITY_FIELDS[first_difference] if first_difference is not None else None,
        "relation": relation,
    }


def _p02_root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / P02_ORACLE_REF).is_file():
        raise ValueError("Phase 02R3 parser fidelity must run from the MathDevMCP workspace root")
    return root


def _p02_round_ref(round_root: str | Path) -> str:
    value = Path(round_root)
    if (
        value.is_absolute()
        or value.parent != P02_RESULT_ROUND_PARENT
        or value.name not in {f"rr0{i}" for i in range(1, 6)}
    ):
        raise ValueError("Phase 02R3 parser round root is outside the reviewed result-round scope")
    return value.as_posix()


def _p02_load_profile(root: Path) -> dict[str, Any]:
    from .extraction_evidence import load_profile

    effective, _materialized = load_profile(root)
    profile = effective["parser_fidelity_profile"]
    if tuple(profile["fidelity_vector_fields_in_priority_order"]) != P02_FIDELITY_FIELDS:
        raise ValueError("Phase 02R3 parser fidelity field registry mismatch")
    if list(profile["executables"]) != ["latexml", "pandoc"]:
        raise ValueError("Phase 02R3 parser backend order differs from the reviewed profile")
    if len(profile["source_allowlist"]) != 13 or len(set(profile["source_allowlist"])) != 13:
        raise ValueError("Phase 02R3 parser source allowlist is not exact and unique")
    return profile


def _p02_environment(profile: dict[str, Any], round_ref: str) -> dict[str, str]:
    return {key: value.replace("RR", round_ref) for key, value in profile["environment"].items()}


def _p02_write(root: Path, ref: str, data: bytes) -> dict[str, Any]:
    result = atomic_write_bytes_no_replace(root, ref, data)
    return {"ref": ref, "sha256": result["sha256"], "byte_count": result["byte_count"]}


def _p02_write_json(root: Path, ref: str, record: dict[str, Any]) -> dict[str, Any]:
    return _p02_write(root, ref, canonical_json_bytes(record))


def _p02_read_regular(root: Path, ref: str) -> bytes:
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise ValueError(f"Phase 02R2 raw artifact is not regular: {ref}")
    return raw


def _p02_raw_binding(root: Path, ref: str, *, required: bool) -> dict[str, Any]:
    path = root / ref
    exists = path.exists() or path.is_symlink()
    if not exists:
        if required:
            raise ValueError(f"Phase 02R2 required raw artifact is absent: {ref}")
        return {"byte_count": None, "present": False, "ref": ref, "sha256": None}
    raw = _p02_read_regular(root, ref)
    return {
        "byte_count": len(raw),
        "present": True,
        "ref": ref,
        "sha256": content_digest(raw),
    }


def _p02_prepare_directories(root: Path, round_ref: str) -> None:
    round_path = root / round_ref
    current = root
    for part in Path(round_ref).parts:
        current = current / part
        if current.is_symlink() or not current.is_dir():
            raise ValueError("Phase 02R2 parser round root is absent or unsafe")
    parser_path = round_path / "parser"
    if parser_path.exists() or parser_path.is_symlink():
        raise ValueError("Phase 02R2 parser subtree must be absent before the one-shot action")
    parser_path.mkdir(mode=0o700, exist_ok=False)
    for path in (
        parser_path / "home",
        parser_path / "latexml",
        parser_path / "pandoc",
        parser_path / "receipts",
        parser_path / "observations",
        parser_path / "expected-values",
    ):
        if path.exists() or path.is_symlink():
            if path.is_symlink() or not path.is_dir():
                raise ValueError(f"unsafe Phase 02R2 parser directory: {path.relative_to(root)}")
        else:
            path.mkdir(mode=0o700, exist_ok=False)


def _p02_run(
    root: Path,
    argv: list[str],
    *,
    environment: dict[str, str],
    timeout: int,
) -> tuple[int | None, bytes, bytes, bool, int]:
    started = time.perf_counter_ns()
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            timeout=timeout,
        )
        return completed.returncode, completed.stdout, completed.stderr, False, time.perf_counter_ns() - started
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, bytes) else (exc.stdout or "").encode("utf-8", "replace")
        stderr = exc.stderr if isinstance(exc.stderr, bytes) else (exc.stderr or "").encode("utf-8", "replace")
        return None, stdout, stderr, True, time.perf_counter_ns() - started


def run_p02_parser_fidelity(round_root: str | Path) -> dict[str, Any]:
    """Run and independently verify the exact reviewed P02R3 parser profile."""
    root = _p02_root()
    round_ref = _p02_round_ref(round_root)
    profile = _p02_load_profile(root)
    environment = _p02_environment(profile, round_ref)
    implementation_manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    _p02_read_regular(root, implementation_manifest_ref)
    _p02_prepare_directories(root, round_ref)

    version_receipts: dict[str, dict[str, str]] = {}
    timed_out_invocation_count = 0
    for backend, executable in profile["executables"].items():
        argv = list(executable["version_argv"])
        exit_code, stdout, stderr, timed_out, wall_ns = _p02_run(
            root,
            argv,
            environment=environment,
            timeout=executable["version_timeout_seconds"],
        )
        stdout_ref = f"{round_ref}/parser/receipts/{backend}-version.stdout"
        stderr_ref = f"{round_ref}/parser/receipts/{backend}-version.stderr"
        _p02_write(root, stdout_ref, stdout)
        _p02_write(root, stderr_ref, stderr)
        version_record = {
            "argv": argv,
            "backend": backend,
            "environment": environment,
            "exit_code": exit_code,
            "schema_version": "p02r2_parser_version_invocation_receipt@1",
            "stderr": _p02_raw_binding(root, stderr_ref, required=True),
            "stdout": _p02_raw_binding(root, stdout_ref, required=True),
            "timed_out": timed_out,
            "timeout_seconds": executable["version_timeout_seconds"],
            "wall_time_ns": wall_ns,
        }
        version_ref = f"{round_ref}/parser/receipts/{backend}-version-raw.json"
        version_artifact = _p02_write_json(root, version_ref, version_record)
        version_receipts[backend] = {
            "ref": version_ref,
            "sha256": version_artifact["sha256"],
        }
        timed_out_invocation_count += int(timed_out)

    source_receipt_count = 0
    for source_ref in profile["source_allowlist"]:
        case_token = hashlib.sha256(source_ref.encode("utf-8")).hexdigest()
        for backend, executable in profile["executables"].items():
            source_before = content_digest(_p02_read_regular(root, source_ref))
            argv = [
                value.replace("RR", round_ref).replace("CASE", case_token).replace("SOURCE", source_ref)
                for value in executable["fidelity_argv_template"]
            ]
            for output_ref in (
                f"{round_ref}/parser/latexml/{case_token}.log",
                f"{round_ref}/parser/latexml/{case_token}.xml",
            ):
                if backend == "latexml" and ((root / output_ref).exists() or (root / output_ref).is_symlink()):
                    raise ValueError(f"Phase 02 parser output already exists: {output_ref}")
            exit_code, stdout, stderr, timed_out, wall_ns = _p02_run(
                root,
                argv,
                environment=environment,
                timeout=executable["source_timeout_seconds"],
            )
            stdout_ref = f"{round_ref}/parser/receipts/{backend}-{case_token}.stdout"
            stderr_ref = f"{round_ref}/parser/receipts/{backend}-{case_token}.stderr"
            _p02_write(root, stdout_ref, stdout)
            _p02_write(root, stderr_ref, stderr)
            source_after = content_digest(_p02_read_regular(root, source_ref))
            stdout_binding = _p02_raw_binding(root, stdout_ref, required=True)
            stderr_binding = _p02_raw_binding(root, stderr_ref, required=True)
            if backend == "latexml":
                output_binding = _p02_raw_binding(
                    root,
                    f"{round_ref}/parser/latexml/{case_token}.xml",
                    required=False,
                )
                log_binding = _p02_raw_binding(
                    root,
                    f"{round_ref}/parser/latexml/{case_token}.log",
                    required=False,
                )
            else:
                output_binding = dict(stdout_binding)
                log_binding = None
            record = {
                "argv": argv,
                "backend": backend,
                "case_token": case_token,
                "environment": environment,
                "exit_code": exit_code,
                "log": log_binding,
                "output": output_binding,
                "schema_version": "p02r2_parser_source_invocation_receipt@1",
                "source_ref": source_ref,
                "source_sha256_after": source_after,
                "source_sha256_before": source_before,
                "stderr": stderr_binding,
                "stdout": stdout_binding,
                "timed_out": timed_out,
                "timeout_seconds": executable["source_timeout_seconds"],
                "version_receipt_ref": version_receipts[backend]["ref"],
                "version_receipt_sha256": version_receipts[backend]["sha256"],
                "wall_time_ns": wall_ns,
            }
            receipt_ref = f"{round_ref}/parser/receipts/{backend}-{case_token}-raw.json"
            _p02_write_json(root, receipt_ref, record)
            source_receipt_count += 1
            timed_out_invocation_count += int(timed_out)
            if source_after != source_before:
                raise ValueError(f"Phase 02R3 parser mutated a protected source: {source_ref}")

    if len(version_receipts) != 2 or source_receipt_count != 26:
        raise ValueError("Phase 02R3 parser runner did not seal exactly 2+26 raw receipts")

    from .extraction_evidence import (
        build_expected_value_projections,
        build_parser_comparison,
        build_parser_raw_observations,
        verify_parser_comparison,
        verify_parser_timeout_gate,
    )

    observations = build_parser_raw_observations(root, round_ref, implementation_manifest_ref)
    for item in observations:
        _p02_write_json(root, item["ref"], item["record"])
    projections = build_expected_value_projections(root, round_ref)
    for item in projections:
        _p02_write_json(root, item["ref"], item["record"])

    comparison = build_parser_comparison(root, round_ref, implementation_manifest_ref)
    comparison_ref = f"{round_ref}/parser/parser-comparison.json"
    artifact = _p02_write_json(root, comparison_ref, comparison)
    verified = verify_parser_comparison(root, comparison_ref, implementation_manifest_ref)
    if verified["sha256"] != artifact["sha256"] or verified["record"] != comparison:
        raise ValueError("Phase 02R3 parser comparison differs from independent reconstruction")
    timeout_gate = verify_parser_timeout_gate(root, round_ref, implementation_manifest_ref)
    if timeout_gate["timed_out_invocation_count"] != timed_out_invocation_count:
        raise ValueError("Phase 02R3 timeout count differs from independent receipt reconstruction")
    if not timeout_gate["all_invocations_completed_within_ceiling"]:
        raise ValueError("Phase 02R3 parser timeout gate failed")
    return {
        "comparison_ref": comparison_ref,
        "comparison_sha256": artifact["sha256"],
        "comparison": comparison,
        "observation_artifact_count": len(observations),
        "projection_artifact_count": len(projections),
        "version_invocation_count": len(version_receipts),
        "source_invocation_count": source_receipt_count,
        "timed_out_invocation_count": timed_out_invocation_count,
        "timeout_gate": timeout_gate,
    }
