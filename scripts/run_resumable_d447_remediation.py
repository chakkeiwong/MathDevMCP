from __future__ import annotations

"""Run the D447 resumable deep-workflow calibration and capstone replay."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any
import uuid

from mathdevmcp.agent_report_artifacts import persist_agent_report
from mathdevmcp.audit_and_propose_fix import audit_and_propose_fix
from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.math_document_rigor import audit_math_document_rigor
from mathdevmcp.resumable_audit import (
    _audit_fix_semantic_projection,
    build_resumable_audit_fix_result,
    create_resumable_audit_session,
    persist_resumable_audit_session,
    run_session_label_audits,
    validate_resumable_audit_batch,
)
from mathdevmcp.resumable_tree import (
    assemble_resumable_tree_result,
    create_resumable_tree_session,
    persist_resumable_tree_session,
    run_resumable_tree_targets,
)


REPO = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d447.tex")
SOURCE_DIGEST = "c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690"
PRIOR_ROOT = REPO / ".local/mathdevmcp/evidence/bgs-d447-capstone-20260717"
PRIOR_INPUT = PRIOR_ROOT / "phase-04/all-label-audit-fix-input.json"
EVIDENCE_ROOT = REPO / ".local/mathdevmcp/evidence/resumable-d447-remediation-20260718"
ARTIFACT_ROOT = EVIDENCE_ROOT / "artifacts"
PLAN = "docs/plans/mathdevmcp-resumable-full-document-gap-remediation-master-program-2026-07-18.md"


def _labels() -> list[str]:
    payload = json.loads(PRIOR_INPUT.read_text(encoding="utf-8"))
    labels = payload.get("arguments", {}).get("labels")
    if not isinstance(labels, list) or len(labels) != 566 or labels != list(dict.fromkeys(labels)):
        raise RuntimeError("frozen D447 label inventory is invalid")
    return [str(label) for label in labels]


def _slice_labels() -> list[str]:
    payload = json.loads((PRIOR_ROOT / "jobs/phase-03-audit-fix-input.json").read_text(encoding="utf-8"))
    labels = payload.get("arguments", {}).get("labels")
    if not isinstance(labels, list) or len(labels) != 18 or labels != list(dict.fromkeys(labels)):
        raise RuntimeError("frozen D447 18-label inventory is invalid")
    return [str(label) for label in labels]


def _git_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _manifest() -> dict[str, Any]:
    labels = _labels()
    return {
        "schema_version": "resumable_d447_remediation_run_manifest@1",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": _git_commit(),
        "command": [sys.executable, str(Path(__file__).resolve())],
        "environment": {
            "python": platform.python_version(),
            "executable": sys.executable,
            "platform": platform.platform(),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "execution_mode": "cpu_only" if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1" else "not_verified_cpu_only",
        },
        "source": {
            "path": str(SOURCE),
            "sha256": SOURCE_DIGEST,
            "label_inventory_source": str(PRIOR_INPUT.relative_to(REPO)),
            "indexed_non_nested_label_count": len(labels),
            "canonical_target_count": 434,
            "typed_relation_shape_abstention_count": 132,
            "nested_ownership_abstention_count": 7,
        },
        "random_seeds": "N/A; deterministic document audit",
        "plan": PLAN,
        "result": "docs/plans/mathdevmcp-resumable-full-document-gap-remediation-result-2026-07-18.md",
        "artifact_root": str(EVIDENCE_ROOT.relative_to(REPO)),
        "gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1",
        "data_version": "Frozen D447 SHA-256 and predeclared 566-label inventory",
        "independent_generalization": "not_tested_no_verified_clean_holdout",
        "non_claim": "Workflow completion is not proof of D447 mathematics, scientific validity, or publication readiness.",
    }


def _check_environment() -> None:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_DIGEST:
        raise RuntimeError("D447 source digest drift")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise RuntimeError("set CUDA_VISIBLE_DEVICES=-1 before running the D447 replay")
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = EVIDENCE_ROOT / "run-manifest.json"
    manifest = _manifest()
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["created_at"] = existing.get("created_at", manifest["created_at"])
        manifest["baseline_amendment"] = {
            "finding": "The prior 566-extractable description conflated indexed non-nested rows with adapter eligibility.",
            "repaired_inventory": "434 canonical targets plus 132 source-bound typed relation-shape abstentions",
        }
    _write_json(manifest_path, manifest)


def _audit_session(labels: list[str]):
    return create_resumable_audit_session(
        SOURCE.parent,
        SOURCE.name,
        labels,
        source_digest=SOURCE_DIGEST,
        backend="sympy",
        paragraph_context=True,
        summary_only=True,
    )


def _classified_inventory() -> dict[str, Any]:
    path = EVIDENCE_ROOT / "label-inventory.json"
    if path.exists():
        inventory = json.loads(path.read_text(encoding="utf-8"))
        if (
            inventory.get("source_digest") == SOURCE_DIGEST
            and inventory.get("ordered_labels") == _labels()
            and inventory.get("canonical_target_count") == 434
            and inventory.get("typed_abstention_count") == 132
        ):
            return inventory
        raise RuntimeError("persisted D447 label inventory does not match the reviewed baseline")
    started = time.perf_counter()
    session, _, _ = _audit_session(_labels())
    canonical = [item["label"] for item in session["bindings"] if item["binding_type"] == "canonical_target"]
    abstentions = [
        {
            "label": item["label"],
            "obligation_id": item["obligation_id"],
            "obligation_digest": item["obligation_digest"],
            "extraction_status": item["extraction_status"],
            "reason": item["extraction_reason"],
        }
        for item in session["bindings"]
        if item["binding_type"] == "typed_abstention"
    ]
    if len(canonical) != 434 or len(abstentions) != 132:
        raise RuntimeError("D447 canonical/abstention inventory differs from the reviewed 434/132 baseline")
    inventory = {
        "schema_version": "resumable_d447_label_inventory@1",
        "source_digest": SOURCE_DIGEST,
        "ordered_labels": _labels(),
        "indexed_non_nested_label_count": 566,
        "canonical_target_count": len(canonical),
        "typed_abstention_count": len(abstentions),
        "canonical_target_labels": canonical,
        "typed_abstentions": abstentions,
        "elapsed_seconds": time.perf_counter() - started,
        "authority": "exact source-bound extraction status",
        "non_claim": "Canonical target eligibility and typed abstention are extraction states, not mathematical verdicts.",
    }
    _write_json(path, inventory)
    return inventory


def _tree_session(labels: list[str], *, max_attempts: int = 3):
    return create_resumable_tree_session(
        SOURCE,
        labels,
        source_digest=SOURCE_DIGEST,
        budget_profile="standard",
        max_attempts=max_attempts,
        backend_env="mathdevmcp-backends",
        search_mode="agent_guided",
        grounding_policy="strict",
    )


def _batch_summary(batch: dict[str, Any], *, elapsed: float, phase: str) -> dict[str, Any]:
    return {
        "schema_version": "resumable_d447_batch_result@1",
        "phase": phase,
        "session_id": batch.get("session_id"),
        "requested_count": batch.get("requested_count"),
        "completed_count": batch.get("completed_count"),
        "produced_count": batch.get("produced_count"),
        "attempted_count": batch.get("attempted_count"),
        "reused_count": batch.get("reused_count"),
        "failed_count": batch.get("failed_count", 0),
        "failures": batch.get("failures", []),
        "pending_count": batch.get("pending_count"),
        "complete": batch.get("complete"),
        "elapsed_seconds": elapsed,
        "source_digest": SOURCE_DIGEST,
        "publication_enabled": False,
        "non_claim": "Batch timing and completion are engineering evidence, not mathematical correctness evidence.",
    }


def run_calibration() -> dict[str, Any]:
    labels = _labels()
    results: list[dict[str, Any]] = []
    for size in (1, 4, 8, 16):
        rung_root = EVIDENCE_ROOT / "calibration" / str(size)
        started = time.perf_counter()
        session, index, parser = _audit_session(labels[:size])
        persist_resumable_audit_session(session, rung_root)
        batch = run_session_label_audits(session, rung_root, index=index, parser_policy=parser)
        elapsed = time.perf_counter() - started
        validate_resumable_audit_batch(batch, session)
        result = _batch_summary(batch, elapsed=elapsed, phase=f"calibration_audit_{size}")
        results.append(result)
        _write_json(rung_root / "result.json", result)
        if elapsed > 600:
            break
    passed = all(item["complete"] and not item["failed_count"] and item["elapsed_seconds"] <= 600 for item in results)
    output = {
        "schema_version": "resumable_d447_calibration@1",
        "status": "passed" if passed else "stopped_on_veto",
        "rungs": results,
        "selected_batch_size": max((item["requested_count"] for item in results if item["complete"] and item["elapsed_seconds"] < 480), default=1),
        "timings_are_descriptive_only": True,
        "publication_enabled": False,
    }
    _write_json(EVIDENCE_ROOT / "calibration/result.json", output)
    return output


def run_audit_batch(size: int, *, label_count: int = 566, lane: str = "full") -> dict[str, Any]:
    selected = _labels()[:label_count]
    root = EVIDENCE_ROOT / lane / "audit"
    started = time.perf_counter()
    session, index, parser = _audit_session(selected)
    persist_resumable_audit_session(session, root)
    batch = run_session_label_audits(
        session,
        root,
        max_new_records=size,
        index=index,
        parser_policy=parser,
    )
    elapsed = time.perf_counter() - started
    result = _batch_summary(batch, elapsed=elapsed, phase=f"{lane}_audit")
    _write_json(root / "latest-result.json", result)
    return result


def run_audit_complete(size: int, *, label_count: int = 566, lane: str = "full") -> dict[str, Any]:
    selected = _labels()[:label_count]
    root = EVIDENCE_ROOT / lane / "audit"
    session, index, parser = _audit_session(selected)
    persist_resumable_audit_session(session, root)
    history: list[dict[str, Any]] = []
    while True:
        started = time.perf_counter()
        batch = run_session_label_audits(
            session,
            root,
            max_new_records=size,
            index=index,
            parser_policy=parser,
        )
        result = _batch_summary(batch, elapsed=time.perf_counter() - started, phase=f"{lane}_audit")
        history.append(result)
        _write_json(root / "latest-result.json", result)
        _write_json(root / "completion-history.json", history)
        if result["failed_count"]:
            raise RuntimeError(f"audit batch failed: {result['failures']}")
        if result["complete"]:
            return result


def _load_complete_audit_batch(labels: list[str], lane: str) -> tuple[dict[str, Any], dict[str, Any]]:
    root = EVIDENCE_ROOT / lane / "audit"
    session, index, parser = _audit_session(labels)
    persist_resumable_audit_session(session, root)
    batch = run_session_label_audits(session, root, max_new_records=0, index=index, parser_policy=parser)
    validate_resumable_audit_batch(batch, session)
    return session, batch


def run_audit_aggregate(*, label_count: int = 566, lane: str = "full") -> dict[str, Any]:
    labels = _labels()[:label_count]
    session, batch = _load_complete_audit_batch(labels, lane)
    result = build_resumable_audit_fix_result(
        session,
        batch,
        "Audit every currently extractable D447 label without editing the source; preserve exact source binding, branch alternatives, actionable abstentions, and nonclaims.",
        validate_proposed_fixes=False,
    )
    artifact = persist_agent_report(result, ARTIFACT_ROOT)
    summary = {
        "schema_version": "resumable_d447_audit_aggregate@1",
        "status": result["status"],
        "coverage": result["evidence"][0]["low_level"]["coverage"],
        "resumable_evidence": result["evidence"][0]["low_level"]["resumable_evidence"],
        "artifact": artifact,
        "publication_enabled": False,
    }
    _write_json(EVIDENCE_ROOT / lane / "audit-aggregate.json", summary)
    return summary


def run_rigor(*, label_count: int = 566, lane: str = "full") -> dict[str, Any]:
    labels = _labels()[:label_count]
    session, batch = _load_complete_audit_batch(labels, lane)
    aggregate = build_resumable_audit_fix_result(
        session,
        batch,
        "Audit every currently extractable D447 label without editing the source; preserve exact source binding, branch alternatives, actionable abstentions, and nonclaims.",
        validate_proposed_fixes=False,
    )
    started = time.perf_counter()
    result = audit_math_document_rigor(
        SOURCE,
        focus_labels=labels,
        max_labels=len(labels),
        backend_env="mathdevmcp-backends",
        validation_backends=["sympy"],
        audit_fix_result=aggregate,
    )
    elapsed = time.perf_counter() - started
    artifact = persist_agent_report(result, ARTIFACT_ROOT)
    summary = {
        "schema_version": "resumable_d447_rigor_result@1",
        "status": result.get("coverage", {}).get("status"),
        "coverage": result.get("coverage"),
        "elapsed_seconds": elapsed,
        "artifact": artifact,
        "audit_recomputed": False,
        "publication_enabled": False,
        "non_claims": result.get("non_claims", []),
    }
    _write_json(EVIDENCE_ROOT / lane / "rigor-result.json", summary)
    return summary


def run_tree_batch(size: int, *, label_count: int = 566, lane: str = "full", max_attempts: int = 3) -> dict[str, Any]:
    inventory = _classified_inventory()
    labels = inventory["canonical_target_labels"][: min(label_count, inventory["canonical_target_count"])]
    root = EVIDENCE_ROOT / lane / "tree"
    started = time.perf_counter()
    session, context = _tree_session(labels, max_attempts=max_attempts)
    persist_resumable_tree_session(session, root)
    batch = run_resumable_tree_targets(session, context, root, max_new_records=size)
    elapsed = time.perf_counter() - started
    result = _batch_summary(batch, elapsed=elapsed, phase=f"{lane}_tree")
    result["typed_abstention_count"] = inventory["typed_abstention_count"] if label_count >= 566 else 0
    result["typed_abstentions"] = inventory["typed_abstentions"] if label_count >= 566 else []
    _write_json(root / "latest-result.json", result)
    return result


def run_tree_complete(size: int, *, label_count: int = 566, lane: str = "full", max_attempts: int = 3) -> dict[str, Any]:
    inventory = _classified_inventory()
    labels = inventory["canonical_target_labels"][: min(label_count, inventory["canonical_target_count"])]
    root = EVIDENCE_ROOT / lane / "tree"
    session, context = _tree_session(labels, max_attempts=max_attempts)
    persist_resumable_tree_session(session, root)
    history: list[dict[str, Any]] = []
    while True:
        started = time.perf_counter()
        batch = run_resumable_tree_targets(session, context, root, max_new_records=size)
        result = _batch_summary(batch, elapsed=time.perf_counter() - started, phase=f"{lane}_tree")
        if label_count >= 566:
            result["typed_abstention_count"] = inventory["typed_abstention_count"]
            result["typed_abstentions"] = inventory["typed_abstentions"]
        history.append(result)
        _write_json(root / "latest-result.json", result)
        _write_json(root / "completion-history.json", history)
        if result["complete"]:
            return result


def run_tree_aggregate(*, label_count: int = 566, lane: str = "full", max_attempts: int = 3) -> dict[str, Any]:
    inventory = _classified_inventory()
    labels = inventory["canonical_target_labels"][: min(label_count, inventory["canonical_target_count"])]
    root = EVIDENCE_ROOT / lane / "tree"
    session, context = _tree_session(labels, max_attempts=max_attempts)
    persist_resumable_tree_session(session, root)
    batch = run_resumable_tree_targets(session, context, root, max_new_records=0)
    result = assemble_resumable_tree_result(session, batch)
    result["full_document_coverage"] = {
        "indexed_non_nested_label_count": inventory["indexed_non_nested_label_count"] if label_count >= 566 else label_count,
        "canonical_tree_target_count": len(labels),
        "typed_relation_shape_abstention_count": inventory["typed_abstention_count"] if label_count >= 566 else 0,
        "typed_relation_shape_abstentions": inventory["typed_abstentions"] if label_count >= 566 else [],
        "nested_ownership_abstention_count": 7 if label_count >= 566 else 0,
        "accounting_complete": label_count < 566 or len(labels) + inventory["typed_abstention_count"] == 566,
        "non_claim": "Typed abstentions are exact coverage states, not executed derivation trees or mathematical refutations.",
    }
    artifact = persist_agent_report(result, ARTIFACT_ROOT)
    summary = {
        "schema_version": "resumable_d447_tree_aggregate@1",
        "status": result.get("coverage", {}).get("status"),
        "coverage": result.get("coverage"),
        "resumable_evidence": result.get("resumable_evidence"),
        "indexed_non_nested_label_count": inventory["indexed_non_nested_label_count"] if label_count >= 566 else label_count,
        "canonical_target_count": len(labels),
        "typed_abstention_count": inventory["typed_abstention_count"] if label_count >= 566 else 0,
        "typed_abstentions": inventory["typed_abstentions"] if label_count >= 566 else [],
        "artifact": artifact,
        "publication_enabled": result.get("publication_enabled", False),
        "publication_mode": result.get("publication_mode"),
        "non_claims": result.get("non_claims", []),
    }
    _write_json(EVIDENCE_ROOT / lane / "tree-aggregate.json", summary)
    return summary


def _tree_semantic_projection(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: result[key]
        for key in (
            "coverage",
            "target_extraction",
            "targets",
            "context_targets",
            "publication_mode",
            "publication_veto_ids",
            "non_claims",
        )
    }


def run_equivalence_18() -> dict[str, Any]:
    labels = _slice_labels()
    root = EVIDENCE_ROOT / "equivalence18"
    question = (
        "Audit the D447 C.71--C.77 slice and propose only source-bound diagnostic repairs; "
        "do not edit the source or collapse live branches."
    )

    prior_result_path = root / "result.json"
    prior_projections_path = root / "semantic-projections.json"
    prior_result = json.loads(prior_result_path.read_text(encoding="utf-8")) if prior_result_path.exists() else None
    prior_projections = json.loads(prior_projections_path.read_text(encoding="utf-8")) if prior_projections_path.exists() else None
    reusable_baseline = (
        isinstance(prior_result, dict)
        and prior_result.get("labels") == labels
        and prior_result.get("source_digest") == SOURCE_DIGEST
        and isinstance(prior_projections, dict)
        and isinstance(prior_projections.get("audit_uninterrupted"), dict)
        and isinstance(prior_projections.get("tree_uninterrupted"), dict)
        and prior_result.get("tree", {}).get("semantic_equivalence") is True
    )
    if reusable_baseline:
        uninterrupted_audit_projection = prior_projections["audit_uninterrupted"]
        uninterrupted_tree_projection = prior_projections["tree_uninterrupted"]
        uninterrupted_audit_seconds = prior_result["audit"]["uninterrupted_seconds"]
        uninterrupted_tree_seconds = prior_result["tree"]["uninterrupted_seconds"]
    else:
        audit_started = time.perf_counter()
        uninterrupted_audit = audit_and_propose_fix(
            question,
            root=str(SOURCE.parent),
            labels=labels,
            target_file=SOURCE.name,
            source_digest=SOURCE_DIGEST,
            backend="sympy",
            paragraph_context=True,
            summary_only=True,
            validate_proposed_fixes=False,
            workers=1,
        )
        uninterrupted_audit_seconds = time.perf_counter() - audit_started
        uninterrupted_audit_projection = _audit_fix_semantic_projection(
            uninterrupted_audit["evidence"][0]["low_level"]
        )
    audit_session, index, parser = _audit_session(labels)
    audit_root = root / "audit"
    persist_resumable_audit_session(audit_session, audit_root)
    first_audit = run_session_label_audits(
        audit_session,
        audit_root,
        max_new_records=7,
        index=index,
        parser_policy=parser,
    )
    resumed_audit_batch = run_session_label_audits(
        audit_session,
        audit_root,
        index=index,
        parser_policy=parser,
    )
    resumed_audit = build_resumable_audit_fix_result(
        audit_session,
        resumed_audit_batch,
        question,
        validate_proposed_fixes=False,
    )
    resumed_audit_projection = _audit_fix_semantic_projection(
        resumed_audit["evidence"][0]["low_level"]
    )
    uninterrupted_audit_bytes = canonical_json_bytes(uninterrupted_audit_projection)
    resumed_audit_bytes = canonical_json_bytes(resumed_audit_projection)

    if reusable_baseline:
        resumed_tree_projection = prior_projections["tree_resumed"]
        first_tree_completed_count = prior_result["tree"]["interruption_completed_count"]
        resumed_tree_reused_count = prior_result["tree"]["resumed_reused_count"]
        resumed_tree_completed_count = prior_result["tree"]["resumed_completed_count"]
    else:
        tree_started = time.perf_counter()
        uninterrupted_tree = audit_document_derivation_tree(
            SOURCE,
            focus_labels=labels,
            max_labels=len(labels),
            budget_profile="standard",
            max_attempts=3,
            backend_env="mathdevmcp-backends",
            search_mode="agent_guided",
            grounding_policy="strict",
            workers=1,
        )
        uninterrupted_tree_seconds = time.perf_counter() - tree_started
        tree_session, context = _tree_session(labels, max_attempts=3)
        tree_root = root / "tree"
        persist_resumable_tree_session(tree_session, tree_root)
        first_tree = run_resumable_tree_targets(tree_session, context, tree_root, max_new_records=7)
        resumed_tree_batch = run_resumable_tree_targets(tree_session, context, tree_root)
        resumed_tree = assemble_resumable_tree_result(tree_session, resumed_tree_batch)
        uninterrupted_tree_projection = _tree_semantic_projection(uninterrupted_tree)
        resumed_tree_projection = _tree_semantic_projection(resumed_tree)
        first_tree_completed_count = first_tree["completed_count"]
        resumed_tree_reused_count = resumed_tree_batch["reused_count"]
        resumed_tree_completed_count = resumed_tree_batch["completed_count"]
    uninterrupted_tree_bytes = canonical_json_bytes(uninterrupted_tree_projection)
    resumed_tree_bytes = canonical_json_bytes(resumed_tree_projection)

    projections = {
        "audit_uninterrupted": uninterrupted_audit_projection,
        "audit_resumed": resumed_audit_projection,
        "tree_uninterrupted": uninterrupted_tree_projection,
        "tree_resumed": resumed_tree_projection,
    }
    _write_json(root / "semantic-projections.json", projections)
    result = {
        "schema_version": "resumable_d447_equivalence18@1",
        "status": "passed" if uninterrupted_audit_bytes == resumed_audit_bytes and uninterrupted_tree_bytes == resumed_tree_bytes else "failed",
        "labels": labels,
        "source_digest": SOURCE_DIGEST,
        "audit": {
            "semantic_equivalence": uninterrupted_audit_bytes == resumed_audit_bytes,
            "projection_sha256": hashlib.sha256(uninterrupted_audit_bytes).hexdigest(),
            "uninterrupted_seconds": uninterrupted_audit_seconds,
            "interruption_completed_count": first_audit["completed_count"],
            "resumed_reused_count": resumed_audit_batch["reused_count"],
            "resumed_completed_count": resumed_audit_batch["completed_count"],
            "uninterrupted_projection_reused": reusable_baseline,
        },
        "tree": {
            "semantic_equivalence": uninterrupted_tree_bytes == resumed_tree_bytes,
            "projection_sha256": hashlib.sha256(uninterrupted_tree_bytes).hexdigest(),
            "uninterrupted_seconds": uninterrupted_tree_seconds,
            "interruption_completed_count": first_tree_completed_count,
            "resumed_reused_count": resumed_tree_reused_count,
            "resumed_completed_count": resumed_tree_completed_count,
            "prior_passing_comparator_reused": reusable_baseline,
        },
        "projection_artifact": "equivalence18/semantic-projections.json",
        "publication_enabled": False,
        "non_claim": "Semantic workflow equivalence is engineering evidence; it is not proof of the D447 mathematics.",
    }
    _write_json(root / "result.json", result)
    if result["status"] != "passed":
        raise RuntimeError("D447 18-label uninterrupted/resumed semantic equivalence failed")
    return result


def status() -> dict[str, Any]:
    paths = {
        "calibration": EVIDENCE_ROOT / "calibration/result.json",
        "rung64_audit": EVIDENCE_ROOT / "rung64/audit/latest-result.json",
        "rung64_tree": EVIDENCE_ROOT / "rung64/tree/latest-result.json",
        "full_audit": EVIDENCE_ROOT / "full/audit/latest-result.json",
        "full_tree": EVIDENCE_ROOT / "full/tree/latest-result.json",
        "full_audit_aggregate": EVIDENCE_ROOT / "full/audit-aggregate.json",
        "full_rigor": EVIDENCE_ROOT / "full/rigor-result.json",
        "full_tree_aggregate": EVIDENCE_ROOT / "full/tree-aggregate.json",
        "equivalence18": EVIDENCE_ROOT / "equivalence18/result.json",
    }
    result = {
        key: json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"status": "not_run"}
        for key, path in paths.items()
    }
    result["source_digest_valid"] = hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_DIGEST
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("calibrate")
    sub.add_parser("equivalence18")
    for name in ("audit-batch", "audit-complete", "tree-batch", "tree-complete"):
        item = sub.add_parser(name)
        item.add_argument("--size", type=int, required=True)
        item.add_argument("--label-count", type=int, default=566)
        item.add_argument("--lane", default="full")
        if name in {"tree-batch", "tree-complete"}:
            item.add_argument("--max-attempts", type=int, default=3)
    for name in ("audit-aggregate", "rigor", "tree-aggregate"):
        item = sub.add_parser(name)
        item.add_argument("--label-count", type=int, default=566)
        item.add_argument("--lane", default="full")
        if name == "tree-aggregate":
            item.add_argument("--max-attempts", type=int, default=3)
    sub.add_parser("status")
    args = parser.parse_args()
    _check_environment()
    if args.mode == "calibrate":
        result = run_calibration()
    elif args.mode == "equivalence18":
        result = run_equivalence_18()
    elif args.mode == "audit-batch":
        result = run_audit_batch(args.size, label_count=args.label_count, lane=args.lane)
    elif args.mode == "audit-complete":
        result = run_audit_complete(args.size, label_count=args.label_count, lane=args.lane)
    elif args.mode == "audit-aggregate":
        result = run_audit_aggregate(label_count=args.label_count, lane=args.lane)
    elif args.mode == "rigor":
        result = run_rigor(label_count=args.label_count, lane=args.lane)
    elif args.mode == "tree-batch":
        result = run_tree_batch(args.size, label_count=args.label_count, lane=args.lane, max_attempts=args.max_attempts)
    elif args.mode == "tree-complete":
        result = run_tree_complete(args.size, label_count=args.label_count, lane=args.lane, max_attempts=args.max_attempts)
    elif args.mode == "tree-aggregate":
        result = run_tree_aggregate(label_count=args.label_count, lane=args.lane, max_attempts=args.max_attempts)
    else:
        result = status()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
