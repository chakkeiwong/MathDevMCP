from __future__ import annotations

"""Schemas and quality metrics for workbench benchmark cases."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Literal

from .contracts import attach_contract


OracleClass = Literal[
    "proved_scoped",
    "refuted_scoped",
    "abstained_missing_assumptions",
    "backend_unavailable_nonclaim",
    "not_encodable_nonclaim",
    "structural_only",
    "diagnostic_only",
    "applicability_gap",
    "applicability_conflict",
    "impact_inconclusive",
]

ORACLE_CLASSES: set[str] = {
    "proved_scoped",
    "refuted_scoped",
    "abstained_missing_assumptions",
    "backend_unavailable_nonclaim",
    "not_encodable_nonclaim",
    "structural_only",
    "diagnostic_only",
    "applicability_gap",
    "applicability_conflict",
    "impact_inconclusive",
}

REQUIRED_RUN_MANIFEST_FIELDS: tuple[str, ...] = (
    "git_state",
    "command",
    "python",
    "backend_matrix",
    "timeout_policy",
    "seed_policy",
    "normalization_rules",
    "mutation_set_version",
    "scoring_rubric_version",
)

SEEDED_GATE_REQUIRED_ORACLES: set[str] = {
    "proved_scoped",
    "refuted_scoped",
    "abstained_missing_assumptions",
    "backend_unavailable_nonclaim",
    "structural_only",
    "diagnostic_only",
    "applicability_gap",
    "applicability_conflict",
    "impact_inconclusive",
}

FIXED_MUTATION_FAMILY: tuple[str, ...] = (
    "backend_unavailable_to_refuted",
    "structural_only_to_proved",
    "numeric_supported_to_backend_proved",
    "missing_assumptions_to_proved",
)

EXTERNAL_SOURCE_FAMILIES: set[str] = {
    "ProofNet",
    "TheoremQA",
    "miniF2F",
    "PutnamBench",
    "LeanDojo",
    "SWE-bench",
    "AMBER",
    "construction_verification",
}

EXTERNAL_REVIEW_STATUSES: set[str] = {
    "unreviewed",
    "reviewed_diagnostic",
    "reviewed_gate_candidate",
}

EXTERNAL_GATE_STATUSES: set[str] = {
    "diagnostic_only",
    "seeded_gate_candidate",
}

EXTERNAL_PRIVACY_CLASSES: set[str] = {
    "licensed_external_local",
    "metadata_only",
    "public_redistributable_adapted",
}

EXTERNAL_REDISTRIBUTION_CLASSES: set[str] = {
    "local_only",
    "metadata_only",
    "redistributable_public",
}

EXPECTED_SEEDED_WORKBENCH_TOOLS: set[str] = {
    "assumptions_required",
    "classify_math_claim",
    "code_implements_equation",
    "derive_or_refute",
    "generate_math_tests",
    "literature_local_audit",
    "localize_proof_gap",
    "math_change_impact",
    "math_review_packet",
    "prove_or_refute",
    "reconcile_notation",
}


@dataclass(frozen=True)
class WorkbenchBenchmarkCase:
    id: str
    tool: str
    oracle_class: str
    expected_status: str
    expected_abstention: bool
    negative_control: bool
    source: str = "local_seeded"
    source_family: str = "local_seeded"
    original_id: str = ""
    transformation_notes: str = ""
    gated: bool = False
    non_claims: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExternalAdaptedCaseManifest:
    id: str
    source_family: str
    original_id: str
    local_path: str
    license_status: str
    redistribution: str
    privacy_class: str
    oracle_class: str
    transformation_notes: str
    source_specific_caveats: tuple[str, ...]
    review_status: str
    gate_status: str = "diagnostic_only"
    gated: bool = False


def validate_workbench_benchmark_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("id", "tool", "oracle_class", "expected_status"):
        if not isinstance(case.get(field), str) or not case.get(field):
            errors.append(f"{field} must be a non-empty string")
    if case.get("oracle_class") not in ORACLE_CLASSES:
        errors.append("oracle_class is unsupported")
    for field in ("expected_abstention", "negative_control", "gated"):
        if field in case and not isinstance(case.get(field), bool):
            errors.append(f"{field} must be a boolean")
    if case.get("source_family") not in {None, "", "local_seeded"} and not case.get("original_id"):
        errors.append("external/adapted cases require original_id")
    return errors


def validate_external_adapted_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "id",
        "source_family",
        "original_id",
        "local_path",
        "license_status",
        "redistribution",
        "privacy_class",
        "oracle_class",
        "transformation_notes",
        "review_status",
        "gate_status",
    ):
        if not isinstance(manifest.get(field), str) or not manifest.get(field):
            errors.append(f"{field} must be a non-empty string")
    caveats = manifest.get("source_specific_caveats")
    if not isinstance(caveats, list) or not caveats or not all(isinstance(item, str) and item for item in caveats):
        errors.append("source_specific_caveats must be a non-empty list of strings")
    if manifest.get("source_family") not in EXTERNAL_SOURCE_FAMILIES:
        errors.append("source_family is unsupported")
    if manifest.get("redistribution") not in EXTERNAL_REDISTRIBUTION_CLASSES:
        errors.append("redistribution is unsupported")
    if manifest.get("privacy_class") not in EXTERNAL_PRIVACY_CLASSES:
        errors.append("privacy_class is unsupported")
    if manifest.get("review_status") not in EXTERNAL_REVIEW_STATUSES:
        errors.append("review_status is unsupported")
    if manifest.get("gate_status") not in EXTERNAL_GATE_STATUSES:
        errors.append("gate_status is unsupported")
    if manifest.get("oracle_class") not in ORACLE_CLASSES:
        errors.append("oracle_class is unsupported")
    if manifest.get("gated") is not False or manifest.get("gate_status") != "diagnostic_only":
        errors.append("external adapted cases must start with gated=false")
    if manifest.get("redistribution") == "redistributable_public" and manifest.get("privacy_class") != "public_redistributable_adapted":
        errors.append("public redistribution requires public_redistributable_adapted privacy_class")
    return errors


def validate_external_adapted_manifest_document(document: dict[str, Any]) -> dict:
    entries = document.get("entries")
    errors: list[dict[str, Any]] = []
    if not isinstance(entries, list):
        errors.append({"kind": "entries_not_list", "severity": "high"})
        entries = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append({"kind": "entry_not_object", "severity": "high", "entry_index": index})
            continue
        for error in validate_external_adapted_manifest(entry):
            errors.append({"kind": "entry_invalid", "severity": "high", "entry_index": index, "detail": error})
    rules = document.get("reporting_rules", {})
    if not isinstance(rules, dict):
        errors.append({"kind": "reporting_rules_not_object", "severity": "high"})
        rules = {}
    if rules.get("combine_with_seeded_totals") is not False:
        errors.append({"kind": "external_seeded_total_mix_forbidden", "severity": "high"})
    if rules.get("allow_leaderboard_claims") is not False:
        errors.append({"kind": "leaderboard_claims_forbidden", "severity": "high"})
    if rules.get("allow_release_gate_by_default") is not False:
        errors.append({"kind": "release_gate_by_default_forbidden", "severity": "high"})
    return attach_contract(
        {
            "status": "consistent" if not errors else "mismatch",
            "entry_count": len(entries),
            "findings": errors,
            "reporting_rules": rules,
            "non_claims": [
                "External adapted packs are diagnostic until separately promoted.",
                "Academic license coverage is not public redistribution permission.",
                "External adapted packs are not combined with seeded formal totals.",
            ],
        },
        "external_adapted_manifest_validation",
    )


def load_external_adapted_manifest(path: str | Path) -> dict:
    manifest_path = Path(path)
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return attach_contract(
            {
                "status": "missing",
                "entry_count": 0,
                "findings": [{"kind": "manifest_missing", "severity": "high", "path": str(manifest_path)}],
            },
            "external_adapted_manifest_validation",
        )
    except json.JSONDecodeError as exc:
        return attach_contract(
            {
                "status": "mismatch",
                "entry_count": 0,
                "findings": [{"kind": "manifest_invalid_json", "severity": "high", "detail": str(exc)}],
            },
            "external_adapted_manifest_validation",
        )
    if not isinstance(data, dict):
        return attach_contract(
            {
                "status": "mismatch",
                "entry_count": 0,
                "findings": [{"kind": "manifest_not_object", "severity": "high"}],
            },
            "external_adapted_manifest_validation",
        )
    return validate_external_adapted_manifest_document(data)


def validate_run_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_RUN_MANIFEST_FIELDS:
        if field not in manifest:
            errors.append(f"run manifest missing {field}")
    return errors


def _result_signature(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": result.get("id"),
            "observed_status": result.get("observed_status"),
            "passed": result.get("passed"),
            "expected_abstention": result.get("expected_abstention"),
        }
        for result in sorted(results, key=lambda item: str(item.get("id", "")))
    ]


def workbench_benchmark_quality_report(
    cases: list[dict[str, Any]],
    *,
    results: list[dict[str, Any]] | None = None,
    deterministic_rerun: tuple[list[dict[str, Any]], list[dict[str, Any]]] | None = None,
    expected_tools: set[str] | None = None,
    mutation_results: dict[str, bool] | None = None,
    run_manifest: dict[str, Any] | None = None,
) -> dict:
    mutation_results = mutation_results or {}
    run_manifest = run_manifest or {}
    results = results or []
    expected_tools = expected_tools or set()
    valid_cases = [case for case in cases if not validate_workbench_benchmark_case(case)]
    tools = {case["tool"] for case in valid_cases}
    oracle_classes = {case["oracle_class"] for case in valid_cases}
    negative_controls = [case for case in valid_cases if case.get("negative_control") is True]
    total = len(valid_cases)
    case_ids = {case["id"] for case in valid_cases}
    result_ids = {result.get("id") for result in results}
    negative_control_rate = len(negative_controls) / total if total else 0.0
    mutation_pass = all(mutation_results.get(name) is True for name in FIXED_MUTATION_FAMILY)
    run_manifest_errors = validate_run_manifest(run_manifest)
    if deterministic_rerun is None:
        deterministic_pass = False
    else:
        first, second = deterministic_rerun
        deterministic_pass = _result_signature(first) == _result_signature(second)
    boundary_results = [
        result
        for result in results
        if result.get("category") == "math_debugging_workbench" or result.get("id") in case_ids
    ]
    boundary_pass = bool(boundary_results) and all(
        result.get("quality_checks", {}).get("boundary_preserved") is True
        and result.get("quality_checks", {}).get("oracle_class_supported") is True
        for result in boundary_results
    )
    result_alignment_pass = bool(valid_cases) and case_ids == result_ids
    seeded_gate_thresholds = {
        "tool_coverage_complete": bool(expected_tools) and expected_tools.issubset(tools),
        "required_oracle_coverage": SEEDED_GATE_REQUIRED_ORACLES.issubset(oracle_classes),
        "negative_control_rate_at_least_40_percent": negative_control_rate >= 0.40,
        "boundary_checks_all_preserved": boundary_pass,
        "case_result_ids_align": result_alignment_pass,
        "deterministic_rerun_stable": deterministic_pass,
        "fixed_mutation_family_detected": mutation_pass,
        "run_manifest_complete": not run_manifest_errors,
    }
    result = {
        "status": "quality_thresholds_passed" if all(seeded_gate_thresholds.values()) else "quality_thresholds_failed",
        "total_cases": total,
        "total_results": len(results),
        "tool_count": len(tools),
        "tools": sorted(tools),
        "expected_tools": sorted(expected_tools),
        "missing_tools": sorted(expected_tools - tools),
        "oracle_classes": sorted(oracle_classes),
        "missing_oracle_classes": sorted(SEEDED_GATE_REQUIRED_ORACLES - oracle_classes),
        "negative_control_count": len(negative_controls),
        "negative_control_rate": negative_control_rate,
        "seeded_gate_thresholds": seeded_gate_thresholds,
        "threshold_denominators": {
            "tool_coverage": len(expected_tools),
            "oracle_coverage": len(SEEDED_GATE_REQUIRED_ORACLES),
            "negative_control_rate": total,
            "boundary_checks": len(boundary_results),
            "case_result_alignment": total,
            "determinism_runs": 2 if deterministic_rerun is not None else 0,
            "mutation_family": len(FIXED_MUTATION_FAMILY),
            "run_manifest": len(REQUIRED_RUN_MANIFEST_FIELDS),
        },
        "result_alignment": {
            "missing_results": sorted(case_ids - result_ids),
            "unexpected_results": sorted(item for item in result_ids - case_ids if isinstance(item, str)),
        },
        "determinism": {
            "stable": deterministic_pass,
            "first_signature": _result_signature(deterministic_rerun[0]) if deterministic_rerun is not None else [],
            "second_signature": _result_signature(deterministic_rerun[1]) if deterministic_rerun is not None else [],
        },
        "mutation_results": {name: bool(mutation_results.get(name)) for name in FIXED_MUTATION_FAMILY},
        "run_manifest_errors": run_manifest_errors,
        "run_manifest": run_manifest,
        "boundary": "Benchmark quality is not established by pass rate alone; false-confidence sensitivity is required.",
        "non_claims": [
            "The fixed mutation family is diagnostic, not a complete adversarial benchmark.",
            "Seeded benchmark quality does not establish external validity.",
            "This report does not claim broad theorem-proving capability or release readiness.",
        ],
    }
    return attach_contract(result, "workbench_benchmark_quality_report")


def seeded_case(**kwargs: Any) -> dict[str, Any]:
    data = asdict(WorkbenchBenchmarkCase(**kwargs))
    data["non_claims"] = list(data["non_claims"])
    return data


def external_manifest(**kwargs: Any) -> dict[str, Any]:
    data = asdict(ExternalAdaptedCaseManifest(**kwargs))
    data["source_specific_caveats"] = list(data["source_specific_caveats"])
    return data
