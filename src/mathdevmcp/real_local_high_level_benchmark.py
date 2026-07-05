from __future__ import annotations

"""Schema checks for the local high-level workflow benchmark manifest."""

import json
from pathlib import Path
from importlib.util import find_spec
import shutil
from typing import Any

from .contracts import attach_contract
from .assumptions_for import assumptions_for
from .audit_math_to_code import audit_math_to_code
from .debug_derivation import debug_derivation
from .derive_from import derive_from
from .agent_handoff_packet import validate_agent_handoff_packet
from .high_level_contracts import HIGH_LEVEL_WORKFLOWS
from .prepare_review_packet import prepare_review_packet
from .prove_or_counterexample import prove_or_counterexample

BENCHMARK_HIGH_LEVEL_WORKFLOWS: set[str] = HIGH_LEVEL_WORKFLOWS - {"propose_fix", "audit_and_propose_fix"}

BENCHMARK_CONTRACT = "real_local_high_level_workflow_benchmark_manifest"
ROUTE_AVAILABILITY_CONTRACT = "real_local_high_level_workflow_route_availability_report"
BASELINE_REPORT_CONTRACT = "real_local_high_level_workflow_baseline_report"
PACKET_REPORT_CONTRACT = "real_local_high_level_workflow_packet_report"
FINAL_MATRIX_CONTRACT = "real_local_high_level_workflow_final_matrix"
MANIFEST_CONTRACT = "real_local_high_level_workflow_benchmark_cases"
MANIFEST_SCOPE = "local_non_gating_high_level_workflow_benchmark"

REQUIRED_REVIEW_PACKET_FIELDS: set[str] = {
    "question",
    "human_framing",
    "source_anchors",
    "assumptions",
    "route_availability",
    "derivation_proof_steps",
    "backend_checks",
    "counterexamples",
    "gaps",
    "actions",
    "evidence_classes",
    "non_claims",
}

REQUIRED_RUBRIC_DIMENSIONS: set[str] = {
    "source_grounding",
    "assumption_correctness",
    "derivation_proof_validity",
    "counterexample_quality",
    "backend_evidence",
    "abstention_quality",
    "boundary_discipline",
}

NEGATIVE_CONTROL_EXPECTED_STATUSES: set[str] = {
    "refuted",
    "missing_assumptions",
    "backend_unavailable",
    "not_encodable",
    "insufficient_evidence",
    "routing_only",
}

NEGATIVE_STATUS_REQUIRED_EVIDENCE: dict[str, set[str]] = {
    "refuted": {"backend_counterexample", "scoped_contradiction", "source_adapter"},
    "missing_assumptions": {"missing_assumption"},
    "backend_unavailable": {"backend_unavailable"},
    "not_encodable": {"not_encodable"},
    "insufficient_evidence": {"human_review_required", "review_packet", "backend_unavailable"},
    "routing_only": {"route_availability"},
}

NEGATIVE_STATUS_OUTCOME_KEYWORDS: dict[str, tuple[str, ...]] = {
    "refuted": ("refut", "contradiction", "mismatch", "gap"),
    "missing_assumptions": ("missing_assumptions", "missing assumptions", "missing-assumption"),
    "backend_unavailable": ("backend_unavailable", "backend unavailable", "backend-unavailable"),
    "not_encodable": ("not_encodable", "not encodable", "not-encodable"),
    "insufficient_evidence": ("insufficient_evidence", "insufficient evidence", "justified abstention", "diagnostic_only", "diagnostic-only"),
    "routing_only": ("routing_only", "routing-only", "structural_mismatch", "structural mismatch", "source-mismatch", "route"),
}

NEGATIVE_STATUS_FORBIDDEN_EVIDENCE: dict[str, set[str]] = {
    "routing_only": {"backend_certificate", "backend_counterexample", "scoped_contradiction"},
    "insufficient_evidence": {"backend_certificate", "backend_counterexample", "scoped_contradiction"},
    "missing_assumptions": {"backend_certificate", "backend_counterexample", "scoped_contradiction"},
    "backend_unavailable": {"backend_certificate", "backend_counterexample", "scoped_contradiction"},
    "not_encodable": {"backend_certificate", "backend_counterexample", "scoped_contradiction"},
}

ALLOWED_EXPECTED_EVIDENCE_CLASSES: set[str] = {
    "source_anchor",
    "source_adapter",
    "backend_certificate",
    "backend_counterexample",
    "scoped_contradiction",
    "missing_assumption",
    "proof_gap",
    "structural_match",
    "structural_mismatch",
    "numeric_diagnostic",
    "generated_test",
    "review_packet",
    "human_review_required",
    "backend_unavailable",
    "not_encodable",
    "route_availability",
    "counterexample",
    "non_claim",
    "action",
}

REQUIRED_CASE_FIELDS: set[str] = {
    "id",
    "title",
    "workflow",
    "tier",
    "question",
    "human_framing",
    "source_snapshot",
    "expected_route",
    "expected_outcome_type",
    "expected_evidence_classes",
    "scoring_rubric",
    "negative_control",
    "good_abstention",
    "minimal_packet_schema",
    "forbidden_claims",
}

REQUIRED_HUMAN_FRAMING_FIELDS: set[str] = {
    "case_purpose",
    "local_background",
    "minimal_formula_scaffold",
    "source_context_summary",
    "decision_target",
    "decision_criteria",
    "alternative_explanations",
    "what_would_change_conclusion",
}

SOURCE_ADAPTER_ROUTES: dict[str, dict[str, str]] = {
    "RLHLB-01-ift-sign-gap": {
        "adapter_route": "ift_sign_consistency",
        "predecessor_case_id": "RLHL-01-ift-gradient-bias-sign",
    },
    "RLHLB-02-kalman-loglik-assumptions": {
        "adapter_route": "kalman_prediction_error_loglik",
        "predecessor_case_id": "RLHL-04-kalman-prediction-error-loglik",
    },
    "RLHLB-03-joseph-equivalence": {
        "adapter_route": "joseph_covariance_equivalence",
        "predecessor_case_id": "RLHL-06-joseph-covariance-equivalence",
    },
    "RLHLB-04-affine-pricing-recursion": {
        "adapter_route": "affine_pricing_master_recursion",
        "predecessor_case_id": "RLHL-07-affine-pricing-master-recursion",
    },
    "RLHLB-05-kalman-score-same-scalar": {
        "adapter_route": "kalman_score_same_scalar",
        "predecessor_case_id": "RLHL-10-kalman-score-same-scalar-contract",
    },
}

BASELINE_CALLS: dict[str, dict[str, Any]] = {
    "RLHLB-01-ift-sign-gap": {
        "workflow": "debug_derivation",
        "call": {
            "steps": ["-lam*dr", "lam*dr"],
            "assumptions": [],
            "backend": "auto",
        },
    },
    "RLHLB-02-kalman-loglik-assumptions": {
        "workflow": "assumptions_for",
        "call": {
            "target": "logdet(S) + v.T @ solve(S, v)",
            "provided_assumptions": [],
        },
    },
    "RLHLB-03-joseph-equivalence": {
        "workflow": "prove_or_counterexample",
        "call": {
            "claim": "joseph_scalar_expansion",
            "lhs": "(1-k*h)*p",
            "rhs": "p-k*h*p",
            "assumptions": [],
            "backend": "auto",
        },
    },
    "RLHLB-04-affine-pricing-recursion": {
        "workflow": "derive_from",
        "call": {
            "target": "affine_collect",
            "lhs": "A + B*x",
            "rhs": "A + x*B",
            "givens": [],
            "assumptions": [],
            "backend": "auto",
        },
    },
    "RLHLB-05-kalman-score-same-scalar": {
        "workflow": "assumptions_for",
        "call": {
            "target": "grad(logdet(S) + v.T @ solve(S, v))",
            "provided_assumptions": [],
        },
    },
    "RLHLB-06-state-space-code-missing-solve": {
        "workflow": "audit_math_to_code",
        "call": {
            "math": "logdet(S) + solve(S, innovation)",
            "code_path": "benchmarks/fixtures/doc_department_state_space_missing_solve.py",
            "aliases": {"InnovCov": "S", "Innov": "innovation"},
        },
    },
    "RLHLB-07-proof-boundary-review-packet": {
        "workflow": "prepare_review_packet",
        "call": {
            "question": "Can we produce a packet for a difficult Gaussian score derivation without overclaiming proof?",
            "evidence_case_ids": ["RLHLB-05-kalman-score-same-scalar"],
            "source": {"kind": "phase4_baseline_stub", "anchors_from_case": "RLHLB-07-proof-boundary-review-packet"},
        },
    },
    "RLHLB-08-hmc-value-only-boundary": {
        "workflow": "prove_or_counterexample",
        "call": {
            "claim": "value_only_filtering_likelihood_proves_hmc_readiness",
            "lhs": "value_only_likelihood",
            "rhs": "hmc_production_readiness",
            "assumptions": [],
            "backend": "auto",
        },
    },
    "RLHLB-09-affine-recovery-assumption-limit": {
        "workflow": "derive_from",
        "call": {
            "target": "affine_recovery_text = uniform_neural_solver_bound",
            "givens": ["affine recovery text"],
            "assumptions": [],
            "backend": "auto",
        },
    },
}


def default_benchmark_manifest_path(root: str | Path | None = None) -> Path:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    return root_path / "benchmarks" / "real_tasks" / "holdout_local" / "real_local_high_level_workflow_benchmark_cases.json"


def _root_path(root: str | Path | None = None) -> Path:
    return Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]


def _list_of_strings(value: object) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) and item for item in value) else []


def _parse_line_range(raw: object) -> tuple[int, int] | None:
    if not isinstance(raw, str) or "-" not in raw:
        return None
    left, right = raw.split("-", 1)
    try:
        start = int(left)
        end = int(right)
    except ValueError:
        return None
    if start < 1 or end < start:
        return None
    return start, end


def _policy_boundary() -> list[str]:
    return [
        "This benchmark manifest is local/non-gating only.",
        "It is not public benchmark evidence.",
        "It is not release-readiness evidence.",
        "It is not scientific validation.",
        "It is not a broad theorem-proving claim.",
        "Source, backend, probe, abstention, and residual ledgers must remain separate.",
    ]


def _route_policy_boundary() -> list[str]:
    return [
        "Route availability is pre-baseline routing evidence only.",
        "Route availability is not a proof, refutation, benchmark pass, release-readiness claim, or scientific-validity claim.",
        "Unavailable routes must be preserved as unavailable or unresolved rather than converted into refutations.",
        "Packet stubs may contain empty evidence lists but must preserve the Phase 2 minimal schema fields.",
    ]


def _baseline_policy_boundary() -> list[str]:
    return [
        "This is the pre-repair current-workflow baseline over the local frozen benchmark.",
        "Aggregate rates are diagnostic only and are not promotion criteria.",
        "Baseline results are not release-readiness, public benchmark validity, scientific validation, production correctness, or broad theorem-proving evidence.",
        "Phase 2 manifest and Phase 3 route ledger must remain frozen while this baseline is interpreted.",
    ]


def _packet_policy_boundary() -> list[str]:
    return [
        "Durable packets are review artifacts and not a proof certificate by themselves.",
        "Packet contents preserve source, backend, counterexample, gap, action, and non-claim ledgers separately.",
        "A packet may summarize backend evidence only within the scoped high-level workflow result that produced it.",
        "Packet reports are local/non-gating and do not establish release readiness, public benchmark validity, scientific validation, broad theorem proving, or downstream-agent reliability.",
        "Aggregate accuracy remains unavailable for this local benchmark report.",
    ]


def _add(finding_list: list[dict[str, Any]], *, severity: str, kind: str, **extra: Any) -> None:
    finding_list.append({"severity": severity, "kind": kind, **extra})


def _validate_metadata(payload: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        _add(findings, severity="high", kind="metadata_missing")
        return
    if metadata.get("contract") != MANIFEST_CONTRACT:
        _add(findings, severity="high", kind="metadata_contract_mismatch")
    if metadata.get("scope") != MANIFEST_SCOPE:
        _add(findings, severity="high", kind="metadata_scope_mismatch")
    if metadata.get("schema_version") != "1.0":
        _add(findings, severity="high", kind="metadata_schema_version_mismatch")
    expected_case_count = metadata.get("expected_case_count")
    if not isinstance(expected_case_count, int) or expected_case_count <= 0:
        _add(findings, severity="high", kind="metadata_expected_case_count_missing")

    status_semantics = metadata.get("negative_control_status_semantics")
    if not isinstance(status_semantics, dict):
        _add(findings, severity="high", kind="negative_control_status_semantics_missing")
    else:
        missing = sorted(NEGATIVE_CONTROL_EXPECTED_STATUSES - set(status_semantics))
        if missing:
            _add(findings, severity="high", kind="negative_control_status_semantics_incomplete", missing=missing)
        for status, record in status_semantics.items():
            if status not in NEGATIVE_CONTROL_EXPECTED_STATUSES:
                _add(findings, severity="medium", kind="negative_control_status_semantics_unknown", status=status)
            if not isinstance(record, dict) or not isinstance(record.get("scoring_semantics"), str) or not record["scoring_semantics"]:
                _add(findings, severity="high", kind="negative_control_status_semantics_invalid", status=status)

    packet_schema = metadata.get("minimal_review_packet_schema")
    if not isinstance(packet_schema, dict):
        _add(findings, severity="high", kind="minimal_review_packet_schema_missing")
    else:
        fields = set(_list_of_strings(packet_schema.get("required_fields")))
        missing = sorted(REQUIRED_REVIEW_PACKET_FIELDS - fields)
        if missing:
            _add(findings, severity="high", kind="minimal_review_packet_schema_incomplete", missing=missing)

    workflow_contracts = metadata.get("workflow_evidence_contracts")
    if not isinstance(workflow_contracts, dict):
        _add(findings, severity="high", kind="workflow_evidence_contracts_missing")
    else:
        missing_workflows = sorted(BENCHMARK_HIGH_LEVEL_WORKFLOWS - set(workflow_contracts))
        if missing_workflows:
            _add(findings, severity="high", kind="workflow_evidence_contracts_incomplete", missing=missing_workflows)
        for workflow, contract in workflow_contracts.items():
            if workflow not in BENCHMARK_HIGH_LEVEL_WORKFLOWS:
                _add(findings, severity="medium", kind="workflow_evidence_contract_unknown", workflow=workflow)
            if not isinstance(contract, dict):
                _add(findings, severity="high", kind="workflow_evidence_contract_invalid", workflow=workflow)
                continue
            required = {
                "comparator",
                "primary_criterion",
                "veto_diagnostics",
                "explanatory_diagnostics",
                "good_abstention",
                "forbidden_claims",
                "result_artifact",
            }
            missing_fields = sorted(field for field in required if field not in contract)
            if missing_fields:
                _add(
                    findings,
                    severity="high",
                    kind="workflow_evidence_contract_missing_fields",
                    workflow=workflow,
                    fields=missing_fields,
                )


def _validate_source_snapshot(case: dict[str, Any], findings: list[dict[str, Any]], *, root_path: Path) -> None:
    case_id = str(case.get("id", "<unknown>"))
    snapshot = case.get("source_snapshot")
    if not isinstance(snapshot, dict):
        _add(findings, severity="high", kind="source_snapshot_not_object", case_id=case_id)
        return
    for field in ("source_family", "source_files"):
        if field not in snapshot:
            _add(findings, severity="high", kind="source_snapshot_missing_field", case_id=case_id, field=field)
    source_files = snapshot.get("source_files")
    if not isinstance(source_files, list) or not source_files:
        _add(findings, severity="high", kind="source_files_missing", case_id=case_id)
        return
    for index, item in enumerate(source_files):
        if not isinstance(item, dict):
            _add(findings, severity="high", kind="source_file_not_object", case_id=case_id, index=index)
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            _add(findings, severity="high", kind="source_file_path_missing", case_id=case_id, index=index)
            continue
        if Path(raw_path).is_absolute():
            _add(findings, severity="high", kind="absolute_source_path", case_id=case_id, path=raw_path)
            continue
        if not (root_path / raw_path).resolve().exists():
            _add(findings, severity="high", kind="source_path_missing", case_id=case_id, path=raw_path)
        if _parse_line_range(item.get("line_range")) is None:
            _add(findings, severity="high", kind="source_line_range_invalid", case_id=case_id, path=raw_path)
        if not isinstance(item.get("role"), str) or not item["role"]:
            _add(findings, severity="high", kind="source_role_missing", case_id=case_id, path=raw_path)


def _validate_human_framing(case: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    case_id = str(case.get("id", "<unknown>"))
    framing = case.get("human_framing")
    if not isinstance(framing, dict):
        _add(findings, severity="high", kind="human_framing_not_object", case_id=case_id)
        return
    missing = sorted(field for field in REQUIRED_HUMAN_FRAMING_FIELDS if field not in framing)
    if missing:
        _add(findings, severity="high", kind="human_framing_missing_fields", case_id=case_id, fields=missing)
    for field in REQUIRED_HUMAN_FRAMING_FIELDS:
        value = framing.get(field)
        if field in {"decision_criteria", "alternative_explanations", "what_would_change_conclusion"}:
            if not _list_of_strings(value):
                _add(findings, severity="high", kind="human_framing_list_field_empty", case_id=case_id, field=field)
        elif not isinstance(value, str) or not value.strip():
            _add(findings, severity="high", kind="human_framing_text_field_empty", case_id=case_id, field=field)


def _validate_case(case: dict[str, Any], findings: list[dict[str, Any]], *, root_path: Path) -> None:
    case_id = str(case.get("id", "<unknown>"))
    missing = sorted(field for field in REQUIRED_CASE_FIELDS if field not in case)
    if missing:
        _add(findings, severity="high", kind="case_missing_fields", case_id=case_id, fields=missing)
        return
    if not str(case_id).startswith("RLHLB-"):
        _add(findings, severity="high", kind="case_id_prefix_mismatch", case_id=case_id)
    if case.get("workflow") not in BENCHMARK_HIGH_LEVEL_WORKFLOWS:
        _add(findings, severity="high", kind="case_workflow_unknown", case_id=case_id, workflow=case.get("workflow"))
    if case.get("tier") != "holdout_local":
        _add(findings, severity="high", kind="case_tier_mismatch", case_id=case_id, tier=case.get("tier"))
    if not isinstance(case.get("question"), str) or not case["question"]:
        _add(findings, severity="high", kind="case_question_missing", case_id=case_id)

    _validate_source_snapshot(case, findings, root_path=root_path)
    _validate_human_framing(case, findings)

    evidence_classes = set(_list_of_strings(case.get("expected_evidence_classes")))
    if not evidence_classes:
        _add(findings, severity="high", kind="expected_evidence_classes_missing", case_id=case_id)
    unknown_evidence = sorted(evidence_classes - ALLOWED_EXPECTED_EVIDENCE_CLASSES)
    if unknown_evidence:
        _add(findings, severity="high", kind="expected_evidence_classes_unknown", case_id=case_id, classes=unknown_evidence)

    scoring = case.get("scoring_rubric")
    if not isinstance(scoring, dict):
        _add(findings, severity="high", kind="scoring_rubric_not_object", case_id=case_id)
    else:
        dimensions = set(_list_of_strings(scoring.get("dimensions")))
        missing_dimensions = sorted(REQUIRED_RUBRIC_DIMENSIONS - dimensions)
        if missing_dimensions:
            _add(findings, severity="high", kind="scoring_rubric_dimensions_incomplete", case_id=case_id, missing=missing_dimensions)
        if scoring.get("aggregate_accuracy") is not None:
            _add(findings, severity="high", kind="aggregate_accuracy_forbidden", case_id=case_id)

    negative = case.get("negative_control")
    if not isinstance(negative, dict) or not isinstance(negative.get("is_negative_control"), bool):
        _add(findings, severity="high", kind="negative_control_invalid", case_id=case_id)
    elif negative["is_negative_control"]:
        expected_status = negative.get("expected_status")
        if expected_status not in NEGATIVE_CONTROL_EXPECTED_STATUSES:
            _add(findings, severity="high", kind="negative_control_expected_status_invalid", case_id=case_id, expected_status=expected_status)
        if not isinstance(negative.get("scoring_semantics"), str) or not negative["scoring_semantics"]:
            _add(findings, severity="high", kind="negative_control_scoring_semantics_missing", case_id=case_id)
        if isinstance(expected_status, str):
            required_evidence = NEGATIVE_STATUS_REQUIRED_EVIDENCE.get(expected_status, set())
            if required_evidence and not (evidence_classes & required_evidence):
                _add(
                    findings,
                    severity="high",
                    kind="negative_control_expected_status_missing_evidence",
                    case_id=case_id,
                    expected_status=expected_status,
                    required=sorted(required_evidence),
                )
            forbidden_evidence = NEGATIVE_STATUS_FORBIDDEN_EVIDENCE.get(expected_status, set())
            present_forbidden = sorted(evidence_classes & forbidden_evidence)
            if present_forbidden:
                _add(
                    findings,
                    severity="high",
                    kind="negative_control_expected_status_forbidden_evidence",
                    case_id=case_id,
                    expected_status=expected_status,
                    evidence_classes=present_forbidden,
                )
            outcome_text = str(case.get("expected_outcome_type", "")).lower()
            keywords = NEGATIVE_STATUS_OUTCOME_KEYWORDS.get(expected_status, ())
            if keywords and not any(keyword in outcome_text for keyword in keywords):
                _add(
                    findings,
                    severity="high",
                    kind="negative_control_expected_status_outcome_mismatch",
                    case_id=case_id,
                    expected_status=expected_status,
                    expected_outcome_type=case.get("expected_outcome_type"),
                    allowed_keywords=list(keywords),
                )
            if expected_status == "routing_only" and "route_availability" not in evidence_classes:
                _add(findings, severity="high", kind="routing_only_route_availability_missing", case_id=case_id)

    packet = case.get("minimal_packet_schema")
    if not isinstance(packet, dict):
        _add(findings, severity="high", kind="minimal_packet_schema_not_object", case_id=case_id)
    else:
        fields = set(_list_of_strings(packet.get("required_fields")))
        missing_packet_fields = sorted(REQUIRED_REVIEW_PACKET_FIELDS - fields)
        if missing_packet_fields:
            _add(findings, severity="high", kind="minimal_packet_schema_incomplete", case_id=case_id, missing=missing_packet_fields)

    if not _list_of_strings(case.get("forbidden_claims")):
        _add(findings, severity="high", kind="forbidden_claims_missing", case_id=case_id)
    if not isinstance(case.get("good_abstention"), str) or not case["good_abstention"]:
        _add(findings, severity="high", kind="good_abstention_missing", case_id=case_id)
    if "case_status" in case or "accuracy" in case or "gold_answer" in case:
        _add(findings, severity="high", kind="blended_status_accuracy_or_gold_answer_forbidden", case_id=case_id)


def load_real_local_high_level_benchmark_manifest(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    root_path = _root_path(root)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_benchmark_manifest_path(root_path)
    if not path.exists():
        return attach_contract(
            {
                "status": "inconclusive",
                "path": str(path),
                "cases": [],
                "findings": [{"severity": "high", "kind": "manifest_missing", "path": str(path)}],
                "summary": {
                    "case_total": 0,
                    "workflow_total": 0,
                    "negative_control_total": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _policy_boundary(),
            },
            BENCHMARK_CONTRACT,
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return attach_contract(
            {
                "status": "inconclusive",
                "path": str(path),
                "cases": [],
                "findings": [{"severity": "high", "kind": "manifest_invalid_json", "detail": str(exc)}],
                "summary": {
                    "case_total": 0,
                    "workflow_total": 0,
                    "negative_control_total": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _policy_boundary(),
            },
            BENCHMARK_CONTRACT,
        )

    findings: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        _add(findings, severity="high", kind="manifest_not_object")
        cases: list[dict[str, Any]] = []
    else:
        _validate_metadata(payload, findings)
        raw_cases = payload.get("cases", [])
        if not isinstance(raw_cases, list):
            _add(findings, severity="high", kind="manifest_cases_not_list")
            cases = []
        else:
            cases = [case for case in raw_cases if isinstance(case, dict)]
            if len(cases) != len(raw_cases):
                _add(findings, severity="high", kind="manifest_case_not_object")

    seen: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            _add(findings, severity="high", kind="case_id_missing")
            continue
        if case_id in seen:
            _add(findings, severity="high", kind="duplicate_case_id", case_id=case_id)
        seen.add(case_id)
        _validate_case(case, findings, root_path=root_path)

    workflows = {case.get("workflow") for case in cases if isinstance(case.get("workflow"), str)}
    missing_workflows = sorted(BENCHMARK_HIGH_LEVEL_WORKFLOWS - workflows)
    if missing_workflows:
        _add(findings, severity="high", kind="workflow_coverage_incomplete", missing=missing_workflows)
    if not (5 <= len(cases) <= 10):
        _add(findings, severity="high", kind="case_count_out_of_program_bounds", case_total=len(cases))
    negative_count = sum(1 for case in cases if isinstance(case.get("negative_control"), dict) and case["negative_control"].get("is_negative_control") is True)
    if negative_count < 3:
        _add(findings, severity="high", kind="negative_control_count_too_low", negative_control_total=negative_count)

    expected_case_count = None
    if isinstance(payload, dict) and isinstance(payload.get("metadata"), dict):
        raw_expected_count = payload["metadata"].get("expected_case_count")
        expected_case_count = raw_expected_count if isinstance(raw_expected_count, int) else None
    if expected_case_count is not None and len(cases) != expected_case_count:
        _add(
            findings,
            severity="high",
            kind="case_count_not_frozen_expected_count",
            case_total=len(cases),
            expected_case_count=expected_case_count,
        )

    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "path": str(path),
            "cases": cases,
            "findings": findings,
            "summary": {
                "case_total": len(cases),
                "workflow_total": len(workflows),
                "negative_control_total": negative_count,
                "aggregate_accuracy": None,
                "workflow_coverage": sorted(workflow for workflow in workflows if isinstance(workflow, str)),
            },
            "policy_boundary": _policy_boundary(),
        },
        BENCHMARK_CONTRACT,
    )


def _module_available(name: str) -> bool:
    try:
        return find_spec(name) is not None
    except ModuleNotFoundError:
        return False


def _source_anchors(case: dict[str, Any]) -> list[dict[str, Any]]:
    snapshot = case.get("source_snapshot") if isinstance(case.get("source_snapshot"), dict) else {}
    raw_files = snapshot.get("source_files") if isinstance(snapshot, dict) else []
    anchors: list[dict[str, Any]] = []
    if not isinstance(raw_files, list):
        return anchors
    for item in raw_files:
        if not isinstance(item, dict):
            continue
        anchors.append(
            {
                "path": item.get("path"),
                "line_range": item.get("line_range"),
                "role": item.get("role"),
            }
        )
    return anchors


def _source_adapter_route(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("id", ""))
    route = SOURCE_ADAPTER_ROUTES.get(case_id)
    if route is not None:
        return {
            "state": "present",
            "adapter_route": route["adapter_route"],
            "predecessor_case_id": route["predecessor_case_id"],
            "note": "Known local source-adapter route from predecessor real-local source-adapter program.",
        }
    if "source-adapter" in str(case.get("expected_route", "")).lower():
        return {
            "state": "absent",
            "adapter_route": None,
            "predecessor_case_id": None,
            "note": "Expected route mentions a source adapter, but no concrete adapter route is registered for this benchmark case.",
        }
    return {
        "state": "not_applicable",
        "adapter_route": None,
        "predecessor_case_id": None,
        "note": "Case is routed through structural, review-packet, or source-boundary diagnostics rather than a local schema adapter.",
    }


def _symbolic_route(case: dict[str, Any], *, sympy_available: bool) -> dict[str, Any]:
    workflow = case.get("workflow")
    classes = set(_list_of_strings(case.get("expected_evidence_classes")))
    expected_route = str(case.get("expected_route", "")).lower()
    relevant = workflow in {"derive_from", "prove_or_counterexample", "debug_derivation"} or "backend_certificate" in classes
    if not relevant:
        return {"state": "not_applicable", "backend": "sympy", "available": sympy_available}
    if sympy_available:
        return {
            "state": "available",
            "backend": "sympy",
            "available": True,
            "note": "Conservative symbolic route can be attempted for scalar/encodable sub-obligations only.",
        }
    return {
        "state": "backend_unavailable",
        "backend": "sympy",
        "available": False,
        "note": "SymPy is unavailable; this must not be treated as refutation.",
        "expected_route_hint": expected_route,
    }


def _counterexample_route(case: dict[str, Any]) -> dict[str, Any]:
    workflow = case.get("workflow")
    classes = set(_list_of_strings(case.get("expected_evidence_classes")))
    relevant = workflow in {"derive_from", "prove_or_counterexample", "debug_derivation"} or "backend_counterexample" in classes
    if not relevant:
        return {"state": "skipped_not_applicable", "attempted": False}
    return {
        "state": "available_not_run",
        "attempted": False,
        "note": "Counterexample search is available for bounded encodable obligations but is not executed in Phase 3.",
    }


def _formal_route(case: dict[str, Any]) -> dict[str, Any]:
    workflow = case.get("workflow")
    lean_path = shutil.which("lean")
    relevant = workflow == "prove_or_counterexample"
    if not relevant:
        return {"state": "not_applicable", "backend": "lean", "available": bool(lean_path), "path": lean_path}
    if lean_path:
        return {
            "state": "available_requires_explicit_source",
            "backend": "lean",
            "available": True,
            "path": lean_path,
            "note": "Lean can only certify explicitly supplied Lean source; prose/source anchors are not Lean proofs.",
        }
    return {
        "state": "backend_unavailable",
        "backend": "lean",
        "available": False,
        "path": None,
        "note": "Lean executable is not on PATH; this is not a refutation.",
    }


def _code_equation_route(case: dict[str, Any]) -> dict[str, Any]:
    if case.get("workflow") == "audit_math_to_code":
        return {
            "state": "available",
            "route": "code_implements_equation",
            "note": "Structural code/equation audit route is available and diagnostic only.",
        }
    return {"state": "not_applicable", "route": "code_implements_equation"}


def _review_packet_route(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": "available",
        "route": "prepare_review_packet",
        "required_fields": list(case.get("minimal_packet_schema", {}).get("required_fields", []))
        if isinstance(case.get("minimal_packet_schema"), dict)
        else [],
    }


def _residual_unresolved(case: dict[str, Any], route_availability: dict[str, Any]) -> list[str]:
    residuals: list[str] = []
    source_state = route_availability["source_adapter"]["state"]
    if source_state == "absent":
        residuals.append("source_adapter_absent")
    if route_availability["symbolic_backend"]["state"] == "backend_unavailable":
        residuals.append("symbolic_backend_unavailable")
    if route_availability["formal_backend"]["state"] == "backend_unavailable" and case.get("workflow") == "prove_or_counterexample":
        residuals.append("formal_backend_unavailable")
    if case.get("negative_control", {}).get("is_negative_control") is True:
        residuals.append("negative_control_requires_boundary_preservation")
    if case.get("workflow") == "prepare_review_packet":
        residuals.append("diagnostic_packet_not_certificate")
    return residuals


def _packet_stub(case: dict[str, Any], route_availability: dict[str, Any]) -> dict[str, Any]:
    evidence_classes = _list_of_strings(case.get("expected_evidence_classes"))
    source_adapter = route_availability["source_adapter"]
    derivation_steps: list[dict[str, Any]] = []
    if case.get("workflow") in {"derive_from", "prove_or_counterexample", "debug_derivation"}:
        derivation_steps.append(
            {
                "status": "not_run_in_phase_3",
                "reason": "Phase 3 records route availability only; Phase 4 runs current workflows.",
            }
        )
    backend_checks = [
        route_availability["symbolic_backend"],
        route_availability["formal_backend"],
    ]
    gaps = [{"kind": item, "status": "unresolved"} for item in route_availability["residual_unresolved"]]
    actions = [
        {
            "code": "run_phase4_baseline",
            "description": "Run the current workflow against this frozen case after route availability is recorded.",
        }
    ]
    if source_adapter["state"] == "absent":
        actions.append(
            {
                "code": "human_review_source_adapter_gap",
                "description": "Review whether a local schema adapter is needed before any source-supported claim.",
            }
        )
    forbidden_non_claims = [f"Forbidden claim not made: {claim}." for claim in _list_of_strings(case.get("forbidden_claims"))]
    return {
        "question": case.get("question"),
        "human_framing": _human_framing(case),
        "source_anchors": _source_anchors(case),
        "assumptions": [],
        "route_availability": route_availability,
        "derivation_proof_steps": derivation_steps,
        "backend_checks": backend_checks,
        "counterexamples": [],
        "gaps": gaps,
        "actions": actions,
        "evidence_classes": evidence_classes,
        "non_claims": [
            "This packet stub is not a proof, refutation, benchmark pass, release-readiness claim, or scientific-validity claim.",
            "Phase 3 route availability does not evaluate the mathematical case.",
            *forbidden_non_claims,
        ],
    }


def _packet_stub_missing_fields(packet: dict[str, Any]) -> list[str]:
    return sorted(field for field in REQUIRED_REVIEW_PACKET_FIELDS if field not in packet)


def build_real_local_high_level_route_availability_report(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build the Phase 3 per-case route ledger and minimal packet stubs."""
    manifest = load_real_local_high_level_benchmark_manifest(root=root, manifest_path=manifest_path)
    if manifest.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Benchmark manifest did not validate; route availability was not built.",
                "manifest": manifest,
                "route_ledger": [],
                "packet_stubs": [],
                "findings": [{"severity": "high", "kind": "manifest_inconclusive"}],
                "summary": {
                    "case_total": 0,
                    "packet_stub_total": 0,
                    "source_adapter_present": 0,
                    "source_adapter_absent": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _route_policy_boundary(),
            },
            ROUTE_AVAILABILITY_CONTRACT,
        )

    sympy_available = _module_available("sympy")
    route_ledger: list[dict[str, Any]] = []
    packet_stubs: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        source_adapter = _source_adapter_route(case)
        route_availability = {
            "case_id": case["id"],
            "workflow": case["workflow"],
            "source_adapter": source_adapter,
            "symbolic_backend": _symbolic_route(case, sympy_available=sympy_available),
            "counterexample_path": _counterexample_route(case),
            "formal_backend": _formal_route(case),
            "code_equation_route": _code_equation_route(case),
            "review_packet_route": _review_packet_route(case),
            "negative_control": case.get("negative_control", {}),
            "expected_evidence_classes": case.get("expected_evidence_classes", []),
        }
        route_availability["residual_unresolved"] = _residual_unresolved(case, route_availability)
        packet = _packet_stub(case, route_availability)
        missing_fields = _packet_stub_missing_fields(packet)
        if missing_fields:
            _add(findings, severity="high", kind="packet_stub_missing_fields", case_id=case["id"], fields=missing_fields)
        route_ledger.append(route_availability)
        packet_stubs.append({"case_id": case["id"], "workflow": case["workflow"], "packet": packet})

    source_present = sum(1 for item in route_ledger if item["source_adapter"]["state"] == "present")
    source_absent = sum(1 for item in route_ledger if item["source_adapter"]["state"] == "absent")
    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "reason": "Route availability ledger and packet stubs were built for all frozen cases."
            if status == "consistent"
            else "Route availability ledger or packet stubs have blocking findings.",
            "manifest_path": manifest["path"],
            "route_ledger": route_ledger,
            "packet_stubs": packet_stubs,
            "findings": findings,
            "summary": {
                "case_total": len(route_ledger),
                "packet_stub_total": len(packet_stubs),
                "source_adapter_present": source_present,
                "source_adapter_absent": source_absent,
                "source_adapter_not_applicable": sum(1 for item in route_ledger if item["source_adapter"]["state"] == "not_applicable"),
                "symbolic_backend_available": sympy_available,
                "aggregate_accuracy": None,
            },
            "policy_boundary": _route_policy_boundary(),
        },
        ROUTE_AVAILABILITY_CONTRACT,
    )


def _read_code(root_path: Path, path: str) -> str:
    code_path = (root_path / path).resolve()
    return code_path.read_text(encoding="utf-8")


def _case_by_id(cases: list[dict[str, Any]], case_id: str) -> dict[str, Any]:
    for case in cases:
        if case.get("id") == case_id:
            return case
    raise KeyError(f"case not found: {case_id}")


def _run_baseline_workflow(
    case: dict[str, Any],
    *,
    cases: list[dict[str, Any]],
    root_path: Path,
    prior_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    call_record = BASELINE_CALLS.get(str(case.get("id", "")))
    if call_record is None:
        raise ValueError(f"missing baseline call for case {case.get('id')}")
    workflow = call_record["workflow"]
    if workflow != case.get("workflow"):
        raise ValueError(f"baseline call workflow mismatch for case {case.get('id')}")
    call = dict(call_record["call"])
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
    if workflow == "audit_math_to_code":
        code = _read_code(root_path, call["code_path"])
        return audit_math_to_code(call["math"], code, aliases=call.get("aliases"))
    if workflow == "prepare_review_packet":
        nested = [prior_results[case_id] for case_id in call.get("evidence_case_ids", []) if case_id in prior_results]
        source = dict(call.get("source", {}))
        anchor_case_id = source.get("anchors_from_case")
        if isinstance(anchor_case_id, str):
            source["anchors"] = _source_anchors(_case_by_id(cases, anchor_case_id))
        return prepare_review_packet(call["question"], evidence=nested, source=source, packet_id=str(case.get("id")))
    raise ValueError(f"unsupported baseline workflow: {workflow}")


def _observed_codes(items: Any, field: str = "code") -> set[str]:
    if not isinstance(items, list):
        return set()
    return {item.get(field) for item in items if isinstance(item, dict) and isinstance(item.get(field), str)}


def _expected_status_family(case: dict[str, Any]) -> str | None:
    negative = case.get("negative_control")
    if isinstance(negative, dict) and negative.get("is_negative_control") is True:
        status = negative.get("expected_status")
        return status if isinstance(status, str) else None
    outcome = str(case.get("expected_outcome_type", "")).lower()
    if "success" in outcome or "source-supported" in outcome or "scoped proof" in outcome:
        return "positive_or_abstain"
    return None


def _status_family_match(expected: str | None, result: dict[str, Any]) -> bool:
    status = result.get("status")
    classes = set(_list_of_strings(result.get("evidence_classes")))
    if expected is None:
        return True
    if expected == "refuted":
        return status in {"refuted", "gap_found", "inconclusive"} and bool(classes & {"backend_counterexample", "proof_gap", "human_review_required"})
    if expected == "missing_assumptions":
        return status == "missing_assumptions" or "missing_assumption" in classes
    if expected == "backend_unavailable":
        return status == "backend_unavailable" or "backend_unavailable" in classes
    if expected == "not_encodable":
        return status == "not_encodable" or "not_encodable" in classes
    if expected == "insufficient_evidence":
        return status in {"diagnostic_only", "inconclusive", "backend_unavailable", "not_encodable", "missing_assumptions"} or bool(
            classes & {"review_packet", "human_review_required", "backend_unavailable", "not_encodable", "missing_assumption"}
        )
    if expected == "routing_only":
        return status in {"structural_match", "structural_mismatch", "diagnostic_only"} and bool(
            classes & {"structural_match", "structural_mismatch", "review_packet"}
        )
    if expected == "positive_or_abstain":
        return status in {"proved", "missing_assumptions", "inconclusive", "diagnostic_only", "gap_found", "not_encodable"}
    return False


def _boundary_checks(result: dict[str, Any]) -> dict[str, bool]:
    status = result.get("status")
    classes = set(_list_of_strings(result.get("evidence_classes")))
    certification_source = result.get("certification_source")
    non_claim_codes = _observed_codes(result.get("non_claims"))
    veto_codes = _observed_codes(result.get("veto_reasons"))
    return {
        "global_non_claims_present": {"general_theorem_proving_not_claimed", "release_readiness_not_claimed"}.issubset(non_claim_codes),
        "backend_unavailable_not_refutation": not (status == "refuted" and "backend_unavailable" in classes),
        "not_encodable_not_false": not (status == "refuted" and "not_encodable" in classes),
        "structural_not_proof": not (status == "proved" and bool(classes & {"structural_match", "structural_mismatch"})),
        "review_packet_not_certificate": not ("review_packet" in classes and certification_source != "none"),
        "refutation_has_counterexample_or_gap": status != "refuted" or bool(result.get("counterexamples")) or "proof_gap" in classes,
        "non_certifying_status_has_no_backend_certification": status in {"proved", "refuted"} or certification_source == "none",
        "inconclusive_has_veto_or_action": status != "inconclusive" or bool(result.get("veto_reasons")) or bool(result.get("actions")),
        "certifying_evidence_not_silently_demoted": not (
            bool(classes & {"backend_certificate", "backend_counterexample", "scoped_contradiction"})
            and status not in {"proved", "refuted"}
            and "certifying_evidence_not_promoted" not in veto_codes
        ),
    }


def _failure_class(case: dict[str, Any], result: dict[str, Any], checks: dict[str, bool]) -> str:
    if not all(checks.values()):
        return "boundary_violation"
    expected = _expected_status_family(case)
    if not _status_family_match(expected, result):
        return "unexpected_status_family"
    status = str(result.get("status"))
    if status in {"proved", "refuted", "structural_match", "structural_mismatch", "missing_assumptions", "diagnostic_only", "gap_found"}:
        return "baseline_evaluable"
    if status in {"backend_unavailable", "not_encodable", "inconclusive"}:
        return "correct_abstention_or_route_gap"
    return "residual_unknown"


def _packet_summary(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "fields_present": sorted(field for field in REQUIRED_REVIEW_PACKET_FIELDS if field in packet),
        "source_anchor_count": len(packet.get("source_anchors", [])) if isinstance(packet.get("source_anchors"), list) else 0,
        "gap_count": len(packet.get("gaps", [])) if isinstance(packet.get("gaps"), list) else 0,
        "non_claim_count": len(packet.get("non_claims", [])) if isinstance(packet.get("non_claims"), list) else 0,
    }


def _baseline_result_for_case(
    case: dict[str, Any],
    result: dict[str, Any],
    *,
    route_row: dict[str, Any],
    packet_stub: dict[str, Any],
) -> dict[str, Any]:
    checks = _boundary_checks(result)
    expected_family = _expected_status_family(case)
    family_match = _status_family_match(expected_family, result)
    failure_class = _failure_class(case, result, checks)
    return {
        "case_id": case["id"],
        "workflow": case["workflow"],
        "question": case["question"],
        "observed_status": result.get("status"),
        "observed_evidence_classes": result.get("evidence_classes", []),
        "certification_source": result.get("certification_source"),
        "expected_status_family": expected_family,
        "expected_family_match": family_match,
        "failure_class": failure_class,
        "boundary_checks": checks,
        "route_reference": {
            "source_adapter_state": route_row["source_adapter"]["state"],
            "source_adapter_route": route_row["source_adapter"].get("adapter_route"),
            "symbolic_backend_state": route_row["symbolic_backend"]["state"],
            "formal_backend_state": route_row["formal_backend"]["state"],
            "code_equation_route_state": route_row["code_equation_route"]["state"],
            "residual_unresolved": route_row.get("residual_unresolved", []),
        },
        "packet_summary": _packet_summary(packet_stub["packet"]),
        "result": result,
        "forbidden_claims": case.get("forbidden_claims", []),
    }


def _baseline_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_failure_class: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for item in results:
        by_failure_class[item["failure_class"]] = by_failure_class.get(item["failure_class"], 0) + 1
        status = str(item.get("observed_status"))
        by_status[status] = by_status.get(status, 0) + 1
    boundary_violations = by_failure_class.get("boundary_violation", 0)
    unexpected = by_failure_class.get("unexpected_status_family", 0)
    return {
        "case_total": len(results),
        "boundary_violations": boundary_violations,
        "unexpected_status_family": unexpected,
        "baseline_evaluable": by_failure_class.get("baseline_evaluable", 0),
        "correct_abstention_or_route_gap": by_failure_class.get("correct_abstention_or_route_gap", 0),
        "by_failure_class": dict(sorted(by_failure_class.items())),
        "by_status": dict(sorted(by_status.items())),
        "aggregate_accuracy": None,
    }


def _low_level_from_result(result: dict[str, Any]) -> dict[str, Any] | None:
    evidence = result.get("evidence")
    if not isinstance(evidence, list):
        return None
    for item in evidence:
        if isinstance(item, dict) and isinstance(item.get("low_level"), dict):
            return item["low_level"]
    return None


def _backend_checks_from_result(result: dict[str, Any], route_reference: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = [
        {
            "backend": "sympy",
            "state": route_reference.get("symbolic_backend_state"),
            "source": "route_reference",
        },
        {
            "backend": "lean",
            "state": route_reference.get("formal_backend_state"),
            "source": "route_reference",
        },
    ]
    low_level = _low_level_from_result(result)
    if isinstance(low_level, dict):
        route = low_level.get("route_decision")
        if isinstance(route, dict) and isinstance(route.get("backend_attempt"), dict):
            checks.append({"source": "workflow_result", **route["backend_attempt"]})
        workbench = low_level.get("workbench_result")
        attempts = workbench.get("backend_attempts") if isinstance(workbench, dict) else None
        if isinstance(attempts, list):
            for attempt in attempts:
                if isinstance(attempt, dict):
                    checks.append({"source": "workflow_result", **attempt})
    return checks


def _derivation_steps_from_result(result: dict[str, Any]) -> list[dict[str, Any]]:
    low_level = _low_level_from_result(result)
    steps: list[dict[str, Any]] = []
    if isinstance(low_level, dict):
        raw_steps = low_level.get("steps")
        raw_step_results = low_level.get("step_results")
        if isinstance(raw_step_results, list):
            for item in raw_step_results:
                if isinstance(item, dict):
                    steps.append(item)
        elif isinstance(raw_steps, list):
            steps.extend({"expression": step, "status": "recorded"} for step in raw_steps if isinstance(step, str))
        workbench = low_level.get("workbench_result")
        obligations = workbench.get("obligations") if isinstance(workbench, dict) else None
        if isinstance(obligations, list):
            for obligation in obligations:
                if isinstance(obligation, dict):
                    steps.append({"kind": "obligation", **obligation})
    if not steps:
        steps.append(
            {
                "status": str(result.get("status", "unknown")),
                "reason": str(result.get("answer", "No explicit derivation step was produced.")),
            }
        )
    return steps


def _gaps_from_result(case_result: dict[str, Any]) -> list[dict[str, Any]]:
    result = case_result["result"]
    gaps: list[dict[str, Any]] = []
    for item in result.get("veto_reasons", []) if isinstance(result.get("veto_reasons"), list) else []:
        if isinstance(item, dict):
            gaps.append({"source": "veto_reason", **item})
    for item in case_result["route_reference"].get("residual_unresolved", []):
        gaps.append({"source": "route_reference", "kind": item, "status": "unresolved"})
    if result.get("status") in {"inconclusive", "backend_unavailable", "not_encodable"} and not gaps:
        gaps.append({"source": "workflow_result", "kind": str(result.get("status")), "status": "unresolved"})
    return gaps


def _non_claim_texts(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    for item in result.get("non_claims", []) if isinstance(result.get("non_claims"), list) else []:
        if isinstance(item, dict) and isinstance(item.get("text"), str) and item["text"]:
            texts.append(item["text"])
    texts.extend(f"Forbidden claim not made: {claim}." for claim in _list_of_strings(case.get("forbidden_claims")))
    texts.extend(_packet_policy_boundary())
    seen: set[str] = set()
    deduped: list[str] = []
    for text in texts:
        if text not in seen:
            deduped.append(text)
            seen.add(text)
    return deduped


def _short_text(value: Any, *, max_len: int = 260) -> str:
    text = str(value).replace("\n", " ").strip()
    return text if len(text) <= max_len else f"{text[: max_len - 3]}..."


def _sentence_fragment(value: Any, *, max_len: int = 260) -> str:
    return _short_text(value, max_len=max_len).rstrip(".")


def _source_anchor_summaries(case: dict[str, Any]) -> list[str]:
    summaries: list[str] = []
    for anchor in _source_anchors(case):
        path = anchor.get("path")
        line_range = anchor.get("line_range")
        role = anchor.get("role")
        summaries.append(f"{path}:{line_range} ({role})")
    return summaries


def _source_context_lines(case: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for index, anchor in enumerate(_source_anchors(case), start=1):
        path = anchor.get("path")
        line_range = anchor.get("line_range")
        role = anchor.get("role")
        lines.append(f"{index}. `{path}:{line_range}` supplies {role}.")
    return lines


def _human_framing(case: dict[str, Any]) -> dict[str, Any]:
    framing = case.get("human_framing")
    if not isinstance(framing, dict):
        return {}
    return {
        "case_purpose": str(framing.get("case_purpose", "")),
        "local_background": str(framing.get("local_background", "")),
        "minimal_formula_scaffold": str(framing.get("minimal_formula_scaffold", "")),
        "source_context_summary": str(framing.get("source_context_summary", "")),
        "decision_target": str(framing.get("decision_target", "")),
        "decision_criteria": _list_of_strings(framing.get("decision_criteria")),
        "alternative_explanations": _list_of_strings(framing.get("alternative_explanations")),
        "what_would_change_conclusion": _list_of_strings(framing.get("what_would_change_conclusion")),
    }


def _framing_lines(framing: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for label, key in (
        ("Case purpose", "case_purpose"),
        ("Local background refresher", "local_background"),
        ("Minimal formula scaffold", "minimal_formula_scaffold"),
        ("Source context summary", "source_context_summary"),
        ("Decision target", "decision_target"),
    ):
        value = framing.get(key)
        if isinstance(value, str) and value:
            lines.append(f"{label}: {value}")
    criteria = _list_of_strings(framing.get("decision_criteria"))
    if criteria:
        lines.append("Decision criteria:\n" + "\n".join(f"- {item}" for item in criteria))
    alternatives = _list_of_strings(framing.get("alternative_explanations"))
    if alternatives:
        lines.append("Alternative explanations:\n" + "\n".join(f"- {item}" for item in alternatives))
    changes = _list_of_strings(framing.get("what_would_change_conclusion"))
    if changes:
        lines.append("What would change the conclusion:\n" + "\n".join(f"- {item}" for item in changes))
    return lines


def _format_assumption(item: Any) -> str:
    if not isinstance(item, dict):
        return _short_text(item)
    text = _short_text(item.get("text", item))
    status = item.get("status", "assumption")
    source = item.get("source")
    used_by = item.get("used_by")
    suffixes: list[str] = []
    if source:
        suffixes.append(f"source: {source}")
    if isinstance(used_by, list) and used_by:
        suffixes.append(f"used by: {', '.join(str(value) for value in used_by)}")
    suffix = f" ({'; '.join(suffixes)})" if suffixes else ""
    return f"{status}: {text}{suffix}"


def _format_gap(item: Any) -> str:
    if not isinstance(item, dict):
        return _short_text(item)
    source = item.get("source", "gap")
    kind = item.get("reason", item.get("kind", item.get("code", item)))
    return f"{source}: {_short_text(kind)}"


def _format_action(item: Any) -> str:
    if not isinstance(item, dict):
        return _short_text(item)
    code = item.get("code", item.get("kind", "action"))
    description = item.get("description", item.get("reason", item))
    return f"{code}: {_short_text(description)}"


def _format_counterexample(item: Any) -> str:
    if not isinstance(item, dict):
        return _short_text(item)
    assignments = item.get("assignments")
    assignment_text = ", ".join(f"{key}={value}" for key, value in assignments.items()) if isinstance(assignments, dict) else "recorded assignment"
    lhs_value = item.get("lhs_value")
    rhs_value = item.get("rhs_value")
    backend = item.get("backend")
    reason = item.get("reason")
    values = f"lhs={lhs_value}, rhs={rhs_value}" if lhs_value is not None and rhs_value is not None else "unequal sides"
    backend_text = f" using {backend}" if backend else ""
    reason_text = f" ({_short_text(reason)})" if reason else ""
    return f"{assignment_text} gives {values}{backend_text}{reason_text}"


def _dedupe_text(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for line in lines:
        if line and line not in seen:
            deduped.append(line)
            seen.add(line)
    return deduped


def _obligation_reasoning_lines(steps: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    seen: set[tuple[str, str, str, str]] = set()
    for index, step in enumerate(steps, start=1):
        lhs = step.get("lhs")
        rhs = step.get("rhs")
        status = step.get("status", "unknown")
        reason = step.get("reason", "No reason recorded.")
        key = (_short_text(lhs), _short_text(rhs), _short_text(status), _short_text(reason))
        if key in seen:
            continue
        seen.add(key)
        reason_text = _sentence_fragment(reason)
        if lhs is not None and rhs is not None:
            line = f"{index}. Encoded obligation: `{lhs}` should equal `{rhs}`; observed status `{status}` because {reason_text}."
            missing = step.get("missing_assumptions")
            if isinstance(missing, list) and missing:
                line = f"{line} Missing assumptions attached to this obligation: {'; '.join(_format_assumption(item) for item in missing)}."
            counterexample = step.get("counterexample")
            if isinstance(counterexample, dict):
                line = f"{line} Counterexample attached to this obligation: {_format_counterexample(counterexample)}."
            lines.append(line)
        else:
            lines.append(f"{index}. Recorded workflow step status `{status}` because {reason_text}.")
    return lines


def _backend_reasoning_lines(backend_checks: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for check in backend_checks:
        backend = check.get("backend", "backend")
        status = check.get("status", check.get("state", "unknown"))
        reason = check.get("reason", check.get("note", "No backend reason recorded."))
        expression = check.get("backend_expression")
        evidence = check.get("evidence")
        if isinstance(evidence, list) and evidence and isinstance(evidence[0], dict):
            expression = expression or evidence[0].get("backend_expression")
            reason = reason or evidence[0].get("reason")
        line = f"{backend}: {status}. {_short_text(reason)}"
        if expression is not None:
            line = f"{line} Backend expression: `{_short_text(expression, max_len=120)}`."
        if line not in seen:
            lines.append(line)
            seen.add(line)
    return lines


def _route_availability_lines(packet: dict[str, Any]) -> list[str]:
    route = packet.get("route_availability")
    if not isinstance(route, dict):
        return []
    lines = [
        f"Source adapter route: {route.get('source_adapter_state')} / {route.get('source_adapter_route')}.",
        f"Symbolic backend route: {route.get('symbolic_backend_state')}.",
        f"Formal backend route: {route.get('formal_backend_state')}.",
        f"Code-equation route: {route.get('code_equation_route_state')}.",
    ]
    residuals = route.get("residual_unresolved")
    if isinstance(residuals, list) and residuals:
        lines.append(f"Residual route flags: {', '.join(str(item) for item in residuals)}.")
    return lines


def _actual_backend_lines(backend_checks: list[dict[str, Any]]) -> list[str]:
    actual = [check for check in backend_checks if check.get("source") == "workflow_result"]
    return _backend_reasoning_lines(actual)


def _structural_evidence_lines(result: dict[str, Any]) -> list[str]:
    low_level = _low_level_from_result(result)
    if not isinstance(low_level, dict):
        return []
    lines: list[str] = []
    equation = low_level.get("equation")
    if equation:
        lines.append(f"The structural matcher compared the candidate code against `{equation}`.")
    matched = low_level.get("matched_terms")
    if isinstance(matched, list) and matched:
        lines.append(f"Matched term(s): {', '.join(str(item) for item in matched)}.")
    missing = low_level.get("missing_terms")
    if isinstance(missing, list) and missing:
        lines.append(f"Missing term(s): {', '.join(str(item) for item in missing)}.")
    conflicts = low_level.get("conflicts")
    if isinstance(conflicts, list) and conflicts:
        lines.append(f"Structural conflict(s): {', '.join(_short_text(item) for item in conflicts)}.")
    extra = low_level.get("extra_code_terms")
    if isinstance(extra, list) and extra:
        preview = ", ".join(str(item) for item in extra[:8])
        more = f", ... ({len(extra)} total)" if len(extra) > 8 else ""
        lines.append(f"Extra code terms were recorded for review: {preview}{more}.")
    return lines


def _nested_review_lines(result: dict[str, Any]) -> list[str]:
    low_level = _low_level_from_result(result)
    if not isinstance(low_level, dict):
        return []
    nested = low_level.get("evidence")
    if not isinstance(nested, list):
        return []
    lines: list[str] = []
    for index, item in enumerate(nested, start=1):
        if not isinstance(item, dict):
            continue
        workflow = item.get("workflow", "nested workflow")
        status = item.get("status", "unknown")
        answer = item.get("answer", item.get("reason", "No nested answer recorded."))
        lines.append(f"Nested evidence {index}: `{workflow}` returned `{status}` because {_short_text(answer)}.")
    return lines


def _decisive_evidence_lines(
    case_result: dict[str, Any],
    result: dict[str, Any],
    packet: dict[str, Any],
    *,
    assumption_lines: list[str],
    gap_lines: list[str],
    counterexample_lines: list[str],
) -> list[str]:
    status = str(case_result.get("observed_status"))
    backend_lines = _actual_backend_lines(packet.get("backend_checks", []))
    if status == "proved":
        return backend_lines or ["The case is marked proved because a scoped backend certificate was recorded."]
    if status == "refuted":
        return counterexample_lines or backend_lines or ["The case is marked refuted because a scoped contradiction or proof gap was recorded."]
    if status == "missing_assumptions":
        return assumption_lines or ["The case is blocked because route-required assumptions were not supplied."]
    if status == "structural_mismatch":
        return _structural_evidence_lines(result) or ["The structural matcher recorded a mismatch."]
    if status == "diagnostic_only":
        return _nested_review_lines(result) or ["The packet is diagnostic because it preserves unresolved nested evidence for review."]
    if status == "inconclusive":
        lines = backend_lines + gap_lines
        return lines or ["No certifying proof, refutation, or sufficient assumption set was produced."]
    return backend_lines + gap_lines


def _why_conclusion_follows_lines(
    case_result: dict[str, Any],
    *,
    assumption_lines: list[str],
    gap_lines: list[str],
    counterexample_lines: list[str],
) -> list[str]:
    status = str(case_result.get("observed_status"))
    if status == "proved":
        return [
            "For this scoped algebraic obligation, a backend simplification of `lhs - rhs` to zero is treated as a certificate for the encoded equality.",
            "The conclusion is limited to the encoded symbolic obligation and does not establish implementation correctness, floating-point stability, or a broader theorem.",
        ]
    if status == "refuted":
        return [
            "A universally stated equality or derivation step cannot survive a concrete assignment, under the supplied assumptions, where the two sides differ.",
            f"The decisive counterexample is: {counterexample_lines[0]}." if counterexample_lines else "A counterexample or proof gap was recorded for the scoped obligation.",
            "Therefore the packet localizes a scoped derivation failure rather than condemning the whole source document.",
        ]
    if status == "missing_assumptions":
        return [
            "The target expression uses operations or semantic links whose route requires explicit domain, conformability, differentiability, invertibility, or source-bridge assumptions.",
            f"Those missing items are: {'; '.join(assumption_lines)}." if assumption_lines else "The required assumption ledger is empty or unavailable, so this remains an assumption-blocked result.",
            "Accepting the derivation without these assumptions would silently add mathematical content that the packet has not sourced or checked.",
        ]
    if status == "structural_mismatch":
        return [
            "The audit asks whether the code structurally contains the documented equation, not whether the entire implementation is mathematically wrong.",
            "A required documented term is absent from the matched code structure, so the safe conclusion is structural mismatch plus human review.",
        ]
    if status == "diagnostic_only":
        return [
            "The workflow's artifact is a review packet, so its success condition is preserving evidence and boundaries rather than certifying a theorem.",
            "Because nested evidence remains assumption-blocked or unresolved, the only supported conclusion is diagnostic review, not proof.",
        ]
    if status == "inconclusive":
        return [
            "The run produced neither a backend certificate nor a bounded counterexample for the encoded obligation.",
            f"The blocking gap is: {gap_lines[0]}." if gap_lines else "The blocking gap is unresolved route or domain evidence.",
            "The correct human-facing answer is therefore abstention with the remaining gap made explicit.",
        ]
    return ["The conclusion follows only from the scoped evidence recorded in this packet."]


def _formalization_lines(packet: dict[str, Any]) -> list[str]:
    steps = packet.get("derivation_proof_steps", [])
    if not isinstance(steps, list):
        return []
    lines = _obligation_reasoning_lines([step for step in steps if isinstance(step, dict)])
    return lines or ["No explicit symbolic obligation was recorded; the packet is diagnostic or route-only."]


def _human_conclusion(case_result: dict[str, Any]) -> str:
    status = str(case_result.get("observed_status"))
    workflow = str(case_result.get("workflow"))
    evidence = ", ".join(case_result.get("observed_evidence_classes", [])) or "no evidence class"
    if status == "proved":
        return f"The scoped {workflow} question is certified within the encoded obligation by {evidence}."
    if status == "refuted":
        return f"The scoped {workflow} question is refuted within the encoded obligation by {evidence}."
    if status == "missing_assumptions":
        return "The workflow cannot derive the requested claim from the current inputs because route-required assumptions are missing."
    if status == "structural_mismatch":
        return "The code/document comparison found a structural mismatch; this is diagnostic evidence, not a mathematical refutation."
    if status == "diagnostic_only":
        return "The output is a review packet or diagnostic bundle; it is not a proof certificate."
    if status == "inconclusive":
        return "The workflow did not find a certifying derivation, proof, or counterexample under the current encoding."
    return f"The workflow returned `{status}`; interpret it under the packet evidence boundary."


def _packet_reasoning(case: dict[str, Any], case_result: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    result = case_result["result"]
    human_framing = packet.get("human_framing") if isinstance(packet.get("human_framing"), dict) else _human_framing(case)
    assumptions = packet.get("assumptions", []) if isinstance(packet.get("assumptions"), list) else []
    gaps = packet.get("gaps", []) if isinstance(packet.get("gaps"), list) else []
    counterexamples = packet.get("counterexamples", []) if isinstance(packet.get("counterexamples"), list) else []
    actions = packet.get("actions", []) if isinstance(packet.get("actions"), list) else []
    assumption_lines = [_format_assumption(item) for item in assumptions]
    gap_lines = [_format_gap(item) for item in gaps]
    action_lines = [_format_action(item) for item in actions]
    counterexample_lines = [_format_counterexample(item) for item in counterexamples]
    source_context = _source_context_lines(case)
    formalization = _formalization_lines(packet)
    route_context = _route_availability_lines(packet)
    decisive_evidence = _dedupe_text(
        _decisive_evidence_lines(
            case_result,
            result,
            packet,
            assumption_lines=assumption_lines,
            gap_lines=gap_lines,
            counterexample_lines=counterexample_lines,
        )
    )
    why_conclusion_follows = _why_conclusion_follows_lines(
        case_result,
        assumption_lines=assumption_lines,
        gap_lines=gap_lines,
        counterexample_lines=counterexample_lines,
    )
    boundary_line = (
        "Boundary: this packet is self-contained local review evidence; it is not a release, public benchmark, "
        "scientific-validity, or broad theorem-proving claim."
    )
    framing_summary = " ".join(_framing_lines(human_framing))
    why_lines = [
        f"Question: {case.get('question')}",
        f"Observed workflow result: `{case_result.get('observed_status')}` with evidence class(es) {case_result.get('observed_evidence_classes', [])}.",
        f"Human framing: {framing_summary}",
        f"Source context: {' '.join(source_context)}",
        f"Formalization checked: {' '.join(formalization)}",
        f"Decisive evidence: {' '.join(decisive_evidence)}",
        f"Why the conclusion follows: {' '.join(why_conclusion_follows)}",
    ]
    if route_context:
        why_lines.append(f"Route context: {' '.join(route_context)}")
    if assumption_lines:
        why_lines.append(f"Assumptions still needed: {'; '.join(assumption_lines)}.")
    if gap_lines:
        why_lines.append(f"Remaining gaps or residuals: {'; '.join(gap_lines)}.")
    if action_lines:
        why_lines.append(f"Next review action(s): {'; '.join(action_lines)}.")
    why_lines.append(boundary_line)
    conclusion = _human_conclusion(case_result)
    answer_sections = [
        f"Conclusion: {conclusion}",
        f"Question: {case.get('question')}",
        "Human framing:\n" + "\n\n".join(_framing_lines(human_framing)),
        "Source context:\n" + "\n".join(source_context),
        "Encoded obligation or artifact:\n" + "\n".join(formalization),
        "Decisive evidence:\n" + "\n".join(decisive_evidence),
        "Why the conclusion follows:\n" + "\n".join(why_conclusion_follows),
    ]
    if route_context:
        answer_sections.append("Route context:\n" + "\n".join(route_context))
    if assumption_lines:
        answer_sections.append("Assumptions needed:\n" + "\n".join(assumption_lines))
    if gap_lines:
        answer_sections.append("Remaining gaps:\n" + "\n".join(gap_lines))
    if action_lines:
        answer_sections.append("Suggested next action:\n" + "\n".join(action_lines))
    answer_sections.append(boundary_line)
    return {
        "conclusion": conclusion,
        "why": why_lines,
        "human_framing": human_framing,
        "source_context": source_context,
        "formalization": formalization,
        "route_context": route_context,
        "decisive_evidence": decisive_evidence,
        "why_conclusion_follows": why_conclusion_follows,
        "assumptions_needed": assumption_lines,
        "counterexample_summary": counterexample_lines,
        "remaining_gaps": gap_lines,
        "next_actions": action_lines,
        "limits": [
            "Only the encoded scoped obligation is certified or refuted.",
            "Source anchors identify bounded provenance but are not copied wholesale.",
            "Diagnostics, route availability, structural matches, and review packets are not proofs by themselves.",
            *[claim.replace("Forbidden claim not made: ", "Does not claim: ") for claim in _list_of_strings(case.get("forbidden_claims"))],
        ],
        "answer_text": "\n\n".join(answer_sections),
        "status": result.get("status"),
    }


def _durable_packet(case: dict[str, Any], case_result: dict[str, Any]) -> dict[str, Any]:
    result = case_result["result"]
    packet = {
        "question": case.get("question"),
        "human_framing": _human_framing(case),
        "source_anchors": _source_anchors(case),
        "assumptions": result.get("assumptions", []),
        "route_availability": case_result["route_reference"],
        "derivation_proof_steps": _derivation_steps_from_result(result),
        "backend_checks": _backend_checks_from_result(result, case_result["route_reference"]),
        "counterexamples": result.get("counterexamples", []),
        "gaps": _gaps_from_result(case_result),
        "actions": result.get("actions", []),
        "evidence_classes": result.get("evidence_classes", []),
        "non_claims": _non_claim_texts(case, result),
    }
    packet["reasoning"] = _packet_reasoning(case, case_result, packet)
    return packet


def _packet_completeness(packet: dict[str, Any], case_result: dict[str, Any]) -> dict[str, bool]:
    non_claims = packet.get("non_claims") if isinstance(packet.get("non_claims"), list) else []
    non_claim_text = "\n".join(str(item) for item in non_claims)
    status = case_result.get("observed_status")
    return {
        "required_fields_present": not _packet_stub_missing_fields(packet),
        "human_framing_present": isinstance(packet.get("human_framing"), dict)
        and bool(packet["human_framing"].get("local_background"))
        and bool(packet["human_framing"].get("minimal_formula_scaffold"))
        and bool(packet["human_framing"].get("decision_criteria"))
        and bool(packet["human_framing"].get("what_would_change_conclusion")),
        "source_anchors_present": bool(packet.get("source_anchors")),
        "backend_checks_present": bool(packet.get("backend_checks")),
        "evidence_classes_present": bool(packet.get("evidence_classes")),
        "non_claims_present": bool(non_claims),
        "forbidden_claims_marked": "Forbidden claim not made:" in non_claim_text,
        "local_non_gating_boundary_present": "local/non-gating" in non_claim_text,
        "gaps_or_counterexamples_or_certificate_present": bool(packet.get("gaps"))
        or bool(packet.get("counterexamples"))
        or case_result.get("certification_source") == "backend"
        or status in {"structural_match", "structural_mismatch", "diagnostic_only", "missing_assumptions"},
        "human_reasoning_present": isinstance(packet.get("reasoning"), dict)
        and bool(packet["reasoning"].get("conclusion"))
        and len(packet["reasoning"].get("why", [])) >= 4,
    }


def _packet_summary_from_packets(packet_records: list[dict[str, Any]]) -> dict[str, Any]:
    by_workflow: dict[str, int] = {}
    finding_count = 0
    for item in packet_records:
        workflow = str(item.get("workflow"))
        by_workflow[workflow] = by_workflow.get(workflow, 0) + 1
        finding_count += len(item.get("findings", [])) if isinstance(item.get("findings"), list) else 0
    return {
        "case_total": len(packet_records),
        "packet_total": len(packet_records),
        "packet_findings": finding_count,
        "by_workflow": dict(sorted(by_workflow.items())),
        "aggregate_accuracy": None,
    }


def _final_matrix_row(packet_record: dict[str, Any]) -> dict[str, Any]:
    route = packet_record["packet"]["route_availability"]
    residuals = list(route.get("residual_unresolved", [])) if isinstance(route.get("residual_unresolved"), list) else []
    if packet_record["failure_class"] == "correct_abstention_or_route_gap" and not residuals:
        residuals.append("abstention_or_route_gap_preserved")
    if packet_record["observed_status"] == "missing_assumptions":
        residuals.append("explicit_missing_assumptions_preserved")
    repair_round = "phase05_semantic_placeholder_guard" if packet_record["case_id"] in {
        "RLHLB-08-hmc-value-only-boundary",
        "RLHLB-09-affine-recovery-assumption-limit",
    } else "preexisting_or_phase04_baseline_behavior"
    return {
        "case_id": packet_record["case_id"],
        "workflow": packet_record["workflow"],
        "expected_status_family": packet_record["expected_status_family"],
        "actual_status": packet_record["observed_status"],
        "failure_class": packet_record["failure_class"],
        "expected_route": {
            "source_adapter_state": route.get("source_adapter_state"),
            "source_adapter_route": route.get("source_adapter_route"),
            "symbolic_backend_state": route.get("symbolic_backend_state"),
            "formal_backend_state": route.get("formal_backend_state"),
            "code_equation_route_state": route.get("code_equation_route_state"),
        },
        "actual_route": {
            "certification_source": packet_record["certification_source"],
            "evidence_classes": packet_record["packet"].get("evidence_classes", []),
            "packet_complete": all(packet_record.get("completeness", {}).values()),
        },
        "repair_round": repair_round,
        "remaining_limitation": residuals or ["no_material_residual_in_local_regression_scope"],
        "status_scope": "local_regression_only_not_promoted",
    }


def build_real_local_high_level_baseline_report(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run current high-level workflows against the frozen benchmark manifest."""
    root_path = _root_path(root)
    route_report = build_real_local_high_level_route_availability_report(root=root_path, manifest_path=manifest_path)
    if route_report.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Route availability did not validate; baseline was not run.",
                "route_report": route_report,
                "results": [],
                "summary": {
                    "case_total": 0,
                    "boundary_violations": 0,
                    "unexpected_status_family": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _baseline_policy_boundary(),
            },
            BASELINE_REPORT_CONTRACT,
        )
    manifest = load_real_local_high_level_benchmark_manifest(root=root_path, manifest_path=manifest_path)
    cases = manifest["cases"]
    routes_by_case = {row["case_id"]: row for row in route_report["route_ledger"]}
    packets_by_case = {stub["case_id"]: stub for stub in route_report["packet_stubs"]}
    prior_results: dict[str, dict[str, Any]] = {}
    case_results: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for case in cases:
        case_id = case["id"]
        try:
            workflow_result = _run_baseline_workflow(case, cases=cases, root_path=root_path, prior_results=prior_results)
        except Exception as exc:
            findings.append({"severity": "high", "kind": "workflow_execution_failed", "case_id": case_id, "detail": str(exc)})
            continue
        prior_results[case_id] = workflow_result
        case_results.append(
            _baseline_result_for_case(
                case,
                workflow_result,
                route_row=routes_by_case[case_id],
                packet_stub=packets_by_case[case_id],
            )
        )

    summary = _baseline_summary(case_results)
    status = "completed" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "reason": "Current high-level workflows were run against the frozen real-local benchmark."
            if status == "completed"
            else "At least one current-workflow baseline call failed to execute.",
            "manifest_path": manifest["path"],
            "route_report_summary": route_report["summary"],
            "results": case_results,
            "findings": findings,
            "summary": summary,
            "policy_boundary": _baseline_policy_boundary(),
        },
        BASELINE_REPORT_CONTRACT,
    )


def build_real_local_high_level_packet_report(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build durable review packets from the current real-local baseline."""
    root_path = _root_path(root)
    baseline = build_real_local_high_level_baseline_report(root=root_path, manifest_path=manifest_path)
    if baseline.get("status") != "completed":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Baseline did not complete; durable packets were not built.",
                "baseline_summary": baseline.get("summary", {}),
                "packets": [],
                "findings": [{"severity": "high", "kind": "baseline_inconclusive"}],
                "summary": {
                    "case_total": 0,
                    "packet_total": 0,
                    "packet_findings": 1,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _packet_policy_boundary(),
            },
            PACKET_REPORT_CONTRACT,
        )

    manifest = load_real_local_high_level_benchmark_manifest(root=root_path, manifest_path=manifest_path)
    cases_by_id = {case["id"]: case for case in manifest["cases"]}
    packet_records: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for case_result in baseline["results"]:
        case_id = case_result["case_id"]
        case = cases_by_id[case_id]
        packet = _durable_packet(case, case_result)
        completeness = _packet_completeness(packet, case_result)
        packet_findings: list[dict[str, Any]] = []
        missing = _packet_stub_missing_fields(packet)
        if missing:
            _add(packet_findings, severity="high", kind="packet_missing_fields", fields=missing)
        for check, passed in completeness.items():
            if not passed:
                _add(packet_findings, severity="high", kind="packet_completeness_check_failed", check=check)
        standard_errors = validate_agent_handoff_packet(packet)
        if standard_errors:
            _add(packet_findings, severity="high", kind="agent_handoff_packet_contract_failed", errors=standard_errors)
        if packet_findings:
            findings.extend({"case_id": case_id, **item} for item in packet_findings)
        packet_records.append(
            {
                "case_id": case_id,
                "workflow": case_result["workflow"],
                "observed_status": case_result["observed_status"],
                "failure_class": case_result["failure_class"],
                "certification_source": case_result["certification_source"],
                "expected_status_family": case_result["expected_status_family"],
                "completeness": completeness,
                "findings": packet_findings,
                "packet": packet,
            }
        )

    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "reason": "Durable review packets were built for all frozen benchmark cases."
            if status == "consistent"
            else "At least one durable review packet failed required completeness checks.",
            "manifest_path": baseline["manifest_path"],
            "baseline_summary": baseline["summary"],
            "packets": packet_records,
            "findings": findings,
            "summary": _packet_summary_from_packets(packet_records),
            "policy_boundary": _packet_policy_boundary(),
        },
        PACKET_REPORT_CONTRACT,
    )


def build_real_local_high_level_final_matrix(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build the final per-case closure matrix from the packet report."""
    packet_report = build_real_local_high_level_packet_report(root=root, manifest_path=manifest_path)
    if packet_report.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Packet report was not consistent; final matrix was not built.",
                "packet_report_summary": packet_report.get("summary", {}),
                "matrix": [],
                "findings": [{"severity": "high", "kind": "packet_report_inconclusive"}],
                "summary": {
                    "case_total": 0,
                    "matrix_total": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _packet_policy_boundary(),
            },
            FINAL_MATRIX_CONTRACT,
        )

    rows = [_final_matrix_row(packet_record) for packet_record in packet_report["packets"]]
    findings: list[dict[str, Any]] = []
    if len(rows) != packet_report["summary"]["case_total"]:
        _add(findings, severity="high", kind="matrix_case_count_mismatch")
    if any(row["status_scope"] != "local_regression_only_not_promoted" for row in rows):
        _add(findings, severity="high", kind="matrix_status_scope_mismatch")
    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "reason": "Final local/non-gating per-case closure matrix was built."
            if status == "consistent"
            else "Final matrix has blocking findings.",
            "packet_report_summary": packet_report["summary"],
            "baseline_summary": packet_report["baseline_summary"],
            "matrix": rows,
            "findings": findings,
            "summary": {
                "case_total": len(rows),
                "matrix_total": len(rows),
                "boundary_violations": packet_report["baseline_summary"].get("boundary_violations"),
                "unexpected_status_family": packet_report["baseline_summary"].get("unexpected_status_family"),
                "aggregate_accuracy": None,
            },
            "policy_boundary": _packet_policy_boundary(),
        },
        FINAL_MATRIX_CONTRACT,
    )
