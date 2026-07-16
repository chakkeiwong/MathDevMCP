from __future__ import annotations

"""Local-only real-source pilot runner for high-level math workflows."""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .assumptions_for import assumptions_for
from .contracts import attach_contract
from .debug_derivation import debug_derivation
from .derive_from import derive_from
from .prove_or_counterexample import prove_or_counterexample


@dataclass(frozen=True)
class PilotValidation:
    status: str
    path: str
    cases: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    policy_boundary: list[str]


def default_manifest_path(root: str | Path | None = None) -> Path:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    return root_path / "benchmarks" / "real_tasks" / "holdout_local" / "high_level_pilot_cases.json"


def _root_path(root: str | Path | None = None) -> Path:
    return Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]


def _list_of_strings(value: object) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) and item for item in value) else []


def _required_case_fields() -> set[str]:
    return {
        "id",
        "title",
        "workflow",
        "tier",
        "source_snapshot",
        "source_obligation",
        "executable_probe",
        "adapter_gap",
        "forbidden_claims",
    }


def _case_findings(case: dict[str, Any], *, root_path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    case_id = str(case.get("id", "<unknown>"))
    missing = sorted(field for field in _required_case_fields() if field not in case)
    if missing:
        findings.append({"severity": "high", "kind": "case_missing_fields", "case_id": case_id, "fields": missing})
        return findings

    if case.get("tier") != "holdout_local":
        findings.append({"severity": "high", "kind": "case_not_holdout_local", "case_id": case_id})

    source = case.get("source_snapshot")
    if not isinstance(source, dict):
        findings.append({"severity": "high", "kind": "source_snapshot_not_object", "case_id": case_id})
    else:
        for field in ["repo", "repo_path", "git_commit_short", "repo_dirty", "source_file_dirty", "source_files"]:
            if field not in source:
                findings.append({"severity": "high", "kind": "source_snapshot_missing_field", "case_id": case_id, "field": field})
        source_files = source.get("source_files")
        if not isinstance(source_files, list) or not source_files:
            findings.append({"severity": "high", "kind": "source_files_missing", "case_id": case_id})
        else:
            for index, item in enumerate(source_files):
                if not isinstance(item, dict):
                    findings.append({"severity": "high", "kind": "source_file_not_object", "case_id": case_id, "index": index})
                    continue
                raw_path = item.get("path")
                if not isinstance(raw_path, str) or not raw_path:
                    findings.append({"severity": "high", "kind": "source_file_path_missing", "case_id": case_id, "index": index})
                    continue
                if Path(raw_path).is_absolute():
                    findings.append({"severity": "high", "kind": "absolute_source_path", "case_id": case_id, "path": raw_path})
                    continue
                if not (root_path / raw_path).resolve().exists():
                    findings.append({"severity": "high", "kind": "source_path_missing", "case_id": case_id, "path": raw_path})
                if not isinstance(item.get("line_range"), str) or not item["line_range"]:
                    findings.append({"severity": "high", "kind": "source_line_range_missing", "case_id": case_id, "path": raw_path})

    source_obligation = case.get("source_obligation")
    probe = case.get("executable_probe")
    adapter_gap = case.get("adapter_gap")
    if not isinstance(source_obligation, dict) or not source_obligation.get("question"):
        findings.append({"severity": "high", "kind": "source_obligation_invalid", "case_id": case_id})
    if not isinstance(probe, dict) or not isinstance(probe.get("call"), dict) or not isinstance(probe.get("expected"), dict):
        findings.append({"severity": "high", "kind": "executable_probe_invalid", "case_id": case_id})
    else:
        if probe.get("workflow") != case.get("workflow"):
            findings.append({"severity": "high", "kind": "probe_workflow_mismatch", "case_id": case_id})
        if not probe.get("faithfulness") or not probe.get("does_not_prove"):
            findings.append({"severity": "high", "kind": "probe_boundary_missing", "case_id": case_id})
    if not isinstance(adapter_gap, dict) or adapter_gap.get("status") != "adapter_required":
        findings.append({"severity": "high", "kind": "adapter_gap_not_recorded", "case_id": case_id})
    if not _list_of_strings(case.get("forbidden_claims")):
        findings.append({"severity": "high", "kind": "forbidden_claims_missing", "case_id": case_id})
    if "case_status" in case or "accuracy" in case:
        findings.append({"severity": "high", "kind": "blended_status_or_accuracy_forbidden", "case_id": case_id})
    return findings


def load_high_level_pilot_manifest(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    root_path = _root_path(root)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_manifest_path(root_path)
    policy_boundary = [
        "This is a local real-source high-level pilot only.",
        "It is not public benchmark evidence.",
        "It is not benchmark-gate evidence.",
        "It is not release-readiness evidence.",
        "Executable probes are not full proofs of source obligations.",
    ]

    if not path.exists():
        return attach_contract(
            PilotValidation("inconclusive", str(path), [], [{"severity": "high", "kind": "manifest_missing", "path": str(path)}], policy_boundary).__dict__,
            "real_local_high_level_pilot_manifest",
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return attach_contract(
            PilotValidation("inconclusive", str(path), [], [{"severity": "high", "kind": "manifest_invalid_json", "detail": str(exc)}], policy_boundary).__dict__,
            "real_local_high_level_pilot_manifest",
        )

    findings: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        findings.append({"severity": "high", "kind": "manifest_not_object"})
        cases: list[dict[str, Any]] = []
    else:
        metadata = payload.get("metadata", {})
        if not isinstance(metadata, dict) or metadata.get("contract") != "real_local_high_level_pilot_cases":
            findings.append({"severity": "high", "kind": "manifest_contract_mismatch"})
        if isinstance(metadata, dict) and metadata.get("scope") != "local_non_gating_pilot_only":
            findings.append({"severity": "high", "kind": "manifest_scope_mismatch"})
        raw_cases = payload.get("cases", [])
        if not isinstance(raw_cases, list):
            findings.append({"severity": "high", "kind": "manifest_cases_not_list"})
            cases = []
        else:
            cases = [case for case in raw_cases if isinstance(case, dict)]
            if len(cases) != len(raw_cases):
                findings.append({"severity": "high", "kind": "manifest_case_not_object"})

    seen: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            findings.append({"severity": "high", "kind": "case_id_missing"})
            continue
        if case_id in seen:
            findings.append({"severity": "high", "kind": "duplicate_case_id", "case_id": case_id})
        seen.add(case_id)
        findings.extend(_case_findings(case, root_path=root_path))

    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        PilotValidation(status, str(path), cases, findings, policy_boundary).__dict__,
        "real_local_high_level_pilot_manifest",
    )


def _run_probe(case: dict[str, Any]) -> dict[str, Any]:
    probe = case["executable_probe"]
    workflow = probe["workflow"]
    call = probe["call"]
    if workflow == "debug_derivation":
        return debug_derivation(call["steps"], assumptions=call.get("assumptions"), backend=call.get("backend", "auto"))
    if workflow == "assumptions_for":
        return assumptions_for(call["target"], provided_assumptions=call.get("provided_assumptions"))
    if workflow == "prove_or_counterexample":
        return prove_or_counterexample(
            call["claim"],
            assumptions=call.get("assumptions"),
            lhs=call.get("lhs"),
            rhs=call.get("rhs"),
            backend=call.get("backend", "auto"),
            lean_source=call.get("lean_source"),
        )
    if workflow == "derive_from":
        return derive_from(
            call["target"],
            givens=call.get("givens"),
            assumptions=call.get("assumptions"),
            lhs=call.get("lhs"),
            rhs=call.get("rhs"),
            backend=call.get("backend", "auto"),
        )
    raise ValueError(f"unsupported high-level pilot workflow: {workflow}")


def score_probe_result(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    expected = case["executable_probe"]["expected"]
    required_non_claims = set(_list_of_strings(expected.get("required_non_claim_codes")))
    observed_non_claims = {item.get("code") for item in result.get("non_claims", []) if isinstance(item, dict)}
    required_vetoes = set(_list_of_strings(expected.get("required_veto_codes")))
    observed_vetoes = {item.get("code") for item in result.get("veto_reasons", []) if isinstance(item, dict)}
    required_assumption_terms = _list_of_strings(expected.get("required_assumption_terms"))
    observed_assumption_text = " ".join(
        str(item.get("text", "")).lower() for item in result.get("assumptions", []) if isinstance(item, dict)
    )
    required_evidence_classes = set(_list_of_strings(expected.get("evidence_classes")))
    optional_evidence_classes = set(_list_of_strings(expected.get("optional_evidence_classes")))
    observed_evidence_classes = set(_list_of_strings(result.get("evidence_classes")))

    checks = {
        "status_match": result.get("status") == expected.get("status"),
        "evidence_classes_match": (
            required_evidence_classes.issubset(observed_evidence_classes)
            and observed_evidence_classes.issubset(required_evidence_classes | optional_evidence_classes)
        ),
        "certification_source_match": result.get("certification_source") == expected.get("certification_source"),
        "required_non_claims_present": required_non_claims.issubset(observed_non_claims),
        "required_vetoes_present": required_vetoes.issubset(observed_vetoes),
        "required_assumption_terms_present": all(term.lower() in observed_assumption_text for term in required_assumption_terms),
        "counterexample_presence_match": (
            True
            if "expected_counterexample" not in expected
            else bool(result.get("counterexamples")) is bool(expected.get("expected_counterexample"))
        ),
        "source_probe_channels_separate": "case_status" not in case and "accuracy" not in case,
        "adapter_gap_visible": isinstance(case.get("adapter_gap"), dict) and case["adapter_gap"].get("status") == "adapter_required",
    }
    status = "passed" if all(checks.values()) else "failed"
    return attach_contract(
        {
            "case_id": case.get("id"),
            "status": status,
            "checks": checks,
            "observed": {
                "status": result.get("status"),
                "evidence_classes": result.get("evidence_classes"),
                "certification_source": result.get("certification_source"),
                "non_claim_codes": sorted(code for code in observed_non_claims if isinstance(code, str)),
                "veto_codes": sorted(code for code in observed_vetoes if isinstance(code, str)),
                "assumptions": [item.get("text") for item in result.get("assumptions", []) if isinstance(item, dict)],
                "counterexamples_present": bool(result.get("counterexamples")),
            },
            "expected": expected,
            "source_channel": {
                "expected_boundary": case.get("source_obligation", {}).get("expected_boundary"),
                "adapter_required": case.get("source_obligation", {}).get("adapter_required") is True,
            },
            "adapter_gap": case.get("adapter_gap"),
            "forbidden_claims": case.get("forbidden_claims", []),
        },
        "real_local_high_level_pilot_probe_score",
    )


def run_high_level_pilot(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    manifest = load_high_level_pilot_manifest(root=root, manifest_path=manifest_path)
    if manifest.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Pilot manifest did not validate; executable probes were not run.",
                "manifest": manifest,
                "source_obligation_ledger": [],
                "probe_ledger": [],
                "adapter_gap_ledger": [],
                "summary": {
                    "case_total": 0,
                    "probe_passed": 0,
                    "probe_failed": 0,
                    "adapter_required": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": manifest.get("policy_boundary", []),
            },
            "real_local_high_level_pilot_report",
        )

    source_ledger: list[dict[str, Any]] = []
    probe_ledger: list[dict[str, Any]] = []
    adapter_ledger: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        source_ledger.append(
            {
                "case_id": case["id"],
                "title": case["title"],
                "workflow": case["workflow"],
                "question": case["source_obligation"]["question"],
                "expected_boundary": case["source_obligation"]["expected_boundary"],
                "adapter_required": case["source_obligation"].get("adapter_required") is True,
                "source_files": case["source_snapshot"]["source_files"],
            }
        )
        adapter_ledger.append({"case_id": case["id"], **case["adapter_gap"]})
        result = _run_probe(case)
        probe_ledger.append(score_probe_result(case, result))

    probe_passed = sum(1 for item in probe_ledger if item.get("status") == "passed")
    probe_failed = sum(1 for item in probe_ledger if item.get("status") == "failed")
    adapter_required = sum(1 for item in adapter_ledger if item.get("status") == "adapter_required")
    status = "passed" if probe_failed == 0 else "failed"
    return attach_contract(
        {
            "status": status,
            "reason": "All executable probes passed declared boundary checks." if status == "passed" else "At least one executable probe failed declared boundary checks.",
            "manifest_path": manifest["path"],
            "source_obligation_ledger": source_ledger,
            "probe_ledger": probe_ledger,
            "adapter_gap_ledger": adapter_ledger,
            "summary": {
                "case_total": len(manifest["cases"]),
                "probe_passed": probe_passed,
                "probe_failed": probe_failed,
                "adapter_required": adapter_required,
                "aggregate_accuracy": None,
            },
            "policy_boundary": [
                *manifest.get("policy_boundary", []),
                "Source-obligation, executable-probe, and adapter-gap channels are intentionally separate.",
                "No single aggregate pilot accuracy metric is emitted.",
            ],
        },
        "real_local_high_level_pilot_report",
    )
