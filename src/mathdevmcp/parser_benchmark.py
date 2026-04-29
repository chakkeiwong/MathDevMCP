from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET

from .backend_env import backend_bin, backend_subprocess_env
from .contracts import attach_contract, contract_metadata
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
