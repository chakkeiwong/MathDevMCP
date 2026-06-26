from __future__ import annotations

"""Loader and validator for the real-task public benchmark manifest."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .contracts import attach_contract


_ALLOWED_FAMILIES = {
    "retrieval_and_provenance",
    "code_document_consistency",
    "derivation_boundary_and_abstention",
    "numerical_oracle_parity",
    "evidence_boundary_discipline",
}
_ALLOWED_DIFFICULTIES = {"easy", "medium", "hard"}
_ALLOWED_STATUSES = {"consistent", "mismatch", "unverified", "inconclusive", "equivalent"}


@dataclass(frozen=True)
class RealTaskGoldSpec:
    expected_status: str
    expected_substatus: str | None
    expected_labels: list[str]
    required_terms: list[str]
    forbidden_claims: list[str]
    required_next_actions: list[str]
    evidence_class: str
    false_confidence_veto: bool


@dataclass(frozen=True)
class RealTaskCaseEntry:
    id: str
    family: str
    repo: str
    task_type: str
    difficulty: str
    public: bool
    document_roots: list[str]
    document_files: list[str]
    code_roots: list[str]
    code_files: list[str]
    labels: list[str]
    prompt: str
    gold: RealTaskGoldSpec
    notes: str


@dataclass(frozen=True)
class RealTaskManifestLoad:
    cases: list[RealTaskCaseEntry]
    source: dict[str, Any]
    findings: list[dict[str, Any]]


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_manifest_path(root: str | Path | None = None) -> Path:
    base = Path(root).resolve() if root is not None else _default_repo_root()
    return base / "benchmarks" / "real_tasks" / "manifests" / "public_cases.json"


def _non_empty_string(value: object, *, field: str, case_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Real-task case {case_id!r} field {field!r} must be a non-empty string.")
    return value


def _optional_string(value: object, *, field: str, case_id: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Real-task case {case_id!r} field {field!r} must be a string or null.")
    return value


def _list_of_strings(value: object, *, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"Real-task case {case_id!r} field {field!r} must be a list of non-empty strings.")
    return value


def _bool_field(value: object, *, field: str, case_id: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"Real-task case {case_id!r} field {field!r} must be a boolean.")
    return value


def _gold_from_mapping(value: object, *, case_id: str) -> RealTaskGoldSpec:
    if not isinstance(value, dict):
        raise ValueError(f"Real-task case {case_id!r} field 'gold' must be a JSON object.")
    required = {
        "expected_status",
        "expected_labels",
        "required_terms",
        "forbidden_claims",
        "required_next_actions",
        "evidence_class",
        "false_confidence_veto",
    }
    missing = sorted(field for field in required if field not in value)
    if missing:
        raise ValueError(f"Real-task case {case_id!r} gold spec is missing required fields: {', '.join(missing)}")
    return RealTaskGoldSpec(
        expected_status=_non_empty_string(value.get("expected_status"), field="gold.expected_status", case_id=case_id),
        expected_substatus=_optional_string(value.get("expected_substatus"), field="gold.expected_substatus", case_id=case_id),
        expected_labels=_list_of_strings(value.get("expected_labels"), field="gold.expected_labels", case_id=case_id),
        required_terms=_list_of_strings(value.get("required_terms"), field="gold.required_terms", case_id=case_id),
        forbidden_claims=_list_of_strings(value.get("forbidden_claims"), field="gold.forbidden_claims", case_id=case_id),
        required_next_actions=_list_of_strings(value.get("required_next_actions"), field="gold.required_next_actions", case_id=case_id),
        evidence_class=_non_empty_string(value.get("evidence_class"), field="gold.evidence_class", case_id=case_id),
        false_confidence_veto=_bool_field(value.get("false_confidence_veto"), field="gold.false_confidence_veto", case_id=case_id),
    )


def _case_from_mapping(value: object) -> RealTaskCaseEntry:
    if not isinstance(value, dict):
        raise ValueError("Real-task benchmark cases must be JSON objects.")
    required = {
        "id",
        "family",
        "repo",
        "task_type",
        "difficulty",
        "public",
        "document_roots",
        "document_files",
        "code_roots",
        "code_files",
        "labels",
        "prompt",
        "gold",
        "notes",
    }
    missing = sorted(field for field in required if field not in value)
    if missing:
        raise ValueError(f"Real-task benchmark case is missing required fields: {', '.join(missing)}")
    case_id = _non_empty_string(value.get("id"), field="id", case_id="<unknown>")
    return RealTaskCaseEntry(
        id=case_id,
        family=_non_empty_string(value.get("family"), field="family", case_id=case_id),
        repo=_non_empty_string(value.get("repo"), field="repo", case_id=case_id),
        task_type=_non_empty_string(value.get("task_type"), field="task_type", case_id=case_id),
        difficulty=_non_empty_string(value.get("difficulty"), field="difficulty", case_id=case_id),
        public=_bool_field(value.get("public"), field="public", case_id=case_id),
        document_roots=_list_of_strings(value.get("document_roots"), field="document_roots", case_id=case_id),
        document_files=_list_of_strings(value.get("document_files"), field="document_files", case_id=case_id),
        code_roots=_list_of_strings(value.get("code_roots"), field="code_roots", case_id=case_id),
        code_files=_list_of_strings(value.get("code_files"), field="code_files", case_id=case_id),
        labels=_list_of_strings(value.get("labels"), field="labels", case_id=case_id),
        prompt=_non_empty_string(value.get("prompt"), field="prompt", case_id=case_id),
        gold=_gold_from_mapping(value.get("gold"), case_id=case_id),
        notes=_non_empty_string(value.get("notes"), field="notes", case_id=case_id),
    )


def _load_manifest_json(path: Path) -> RealTaskManifestLoad:
    if not path.exists():
        return RealTaskManifestLoad([], {"path": str(path), "status": "missing"}, [{"severity": "high", "kind": "manifest_missing", "path": str(path)}])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return RealTaskManifestLoad([], {"path": str(path), "status": "invalid_json"}, [{"severity": "high", "kind": "manifest_invalid_json", "detail": str(exc)}])
    if isinstance(payload, list):
        raw_cases = payload
        metadata = {"schema_version": None, "contract": None}
    elif isinstance(payload, dict):
        raw_cases = payload.get("cases", [])
        metadata = payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {}
    else:
        return RealTaskManifestLoad([], {"path": str(path), "status": "invalid_shape"}, [{"severity": "high", "kind": "manifest_invalid_shape"}])
    if not isinstance(raw_cases, list):
        return RealTaskManifestLoad([], {"path": str(path), "status": "invalid_shape"}, [{"severity": "high", "kind": "manifest_cases_not_list"}])
    cases: list[RealTaskCaseEntry] = []
    findings: list[dict[str, Any]] = []
    for index, item in enumerate(raw_cases):
        try:
            cases.append(_case_from_mapping(item))
        except ValueError as exc:
            findings.append({"severity": "high", "kind": "real_task_case_invalid", "case_index": index, "detail": str(exc)})
    status = "loaded" if not findings else "invalid_entries"
    return RealTaskManifestLoad(cases, {"path": str(path), "status": status, "metadata": metadata, "cases": len(cases)}, findings)


def _resolve_repo_relative(root: Path, raw_path: str) -> Path:
    return (root / raw_path).resolve()


def _validate_manifest_metadata(metadata: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    if metadata.get("schema_version") != "1.0":
        findings.append({"severity": "high", "kind": "manifest_schema_version_mismatch", "expected": "1.0", "observed": metadata.get("schema_version")})
    if metadata.get("contract") != "real_task_public_case_manifest":
        findings.append({"severity": "high", "kind": "manifest_contract_mismatch", "expected": "real_task_public_case_manifest", "observed": metadata.get("contract")})


def _validate_case(case: RealTaskCaseEntry, *, root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if case.family not in _ALLOWED_FAMILIES:
        findings.append({"severity": "high", "kind": "unsupported_case_family", "case_id": case.id, "observed": case.family})
    if case.difficulty not in _ALLOWED_DIFFICULTIES:
        findings.append({"severity": "high", "kind": "unsupported_case_difficulty", "case_id": case.id, "observed": case.difficulty})
    if case.gold.expected_status not in _ALLOWED_STATUSES:
        findings.append({"severity": "high", "kind": "unsupported_expected_status", "case_id": case.id, "observed": case.gold.expected_status})
    if case.gold.expected_labels and not case.document_files:
        findings.append({"severity": "high", "kind": "expected_labels_without_document_files", "case_id": case.id})
    if case.code_files and not case.code_roots:
        findings.append({"severity": "high", "kind": "code_files_without_code_roots", "case_id": case.id})
    for field, paths in {
        "document_roots": case.document_roots,
        "document_files": case.document_files,
        "code_roots": case.code_roots,
        "code_files": case.code_files,
    }.items():
        seen: set[str] = set()
        for raw_path in paths:
            path_obj = Path(raw_path)
            if path_obj.is_absolute():
                findings.append({"severity": "high", "kind": "absolute_path_not_allowed", "case_id": case.id, "field": field, "path": raw_path})
                continue
            if raw_path in seen:
                findings.append({"severity": "medium", "kind": "duplicate_case_path", "case_id": case.id, "field": field, "path": raw_path})
                continue
            seen.add(raw_path)
            resolved = _resolve_repo_relative(root, raw_path)
            if not resolved.exists():
                findings.append({"severity": "high", "kind": "referenced_path_missing", "case_id": case.id, "field": field, "path": raw_path})
    return findings


def load_real_task_public_manifest(root: str | Path | None = None, manifest_path: str | Path | None = None) -> dict:
    repo_root = Path(root).resolve() if root is not None else _default_repo_root()
    path = Path(manifest_path).resolve() if manifest_path is not None else _default_manifest_path(repo_root)
    loaded = _load_manifest_json(path)
    status = "consistent" if loaded.source.get("status") == "loaded" else "inconclusive"
    reason = "Real-task public manifest loaded." if status == "consistent" else "Real-task public manifest could not be fully loaded."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "path": str(path),
            "repo_root": str(repo_root),
            "manifest_metadata": loaded.source.get("metadata", {}),
            "cases": [asdict(case) for case in loaded.cases],
            "findings": loaded.findings,
        },
        "real_task_public_case_manifest",
    )


def validate_real_task_public_manifest(root: str | Path | None = None, manifest_path: str | Path | None = None) -> dict:
    repo_root = Path(root).resolve() if root is not None else _default_repo_root()
    manifest = load_real_task_public_manifest(repo_root, manifest_path=manifest_path)
    findings: list[dict[str, Any]] = list(manifest.get("findings", []))
    metadata = manifest.get("manifest_metadata", {}) if isinstance(manifest.get("manifest_metadata", {}), dict) else {}
    _validate_manifest_metadata(metadata, findings)
    seen_ids: set[str] = set()
    for case_dict in manifest.get("cases", []):
        case = _case_from_mapping(case_dict)
        if case.id in seen_ids:
            findings.append({"severity": "high", "kind": "duplicate_case_id", "case_id": case.id})
        seen_ids.add(case.id)
        findings.extend(_validate_case(case, root=repo_root))
    if manifest.get("status") == "inconclusive":
        status = "inconclusive"
        reason = "Real-task public manifest validation could not complete because the manifest did not load cleanly."
    else:
        status = "mismatch" if any(item.get("severity") == "high" for item in findings) else "consistent"
        reason = "Real-task public manifest validation completed."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "findings": findings,
            "manifest": manifest,
        },
        "real_task_public_case_validation_report",
    )
