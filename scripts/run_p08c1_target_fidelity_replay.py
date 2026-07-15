#!/usr/bin/env python3
"""Create and verify the Phase 08C1 target-fidelity replay artifact."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any, Mapping


WORKSPACE = Path(__file__).resolve().parent.parent
P08A_EXTRACTION = WORKSPACE / (
    ".local/mathdevmcp/evidence/p08-20260714/runs/"
    "20260714T045222Z-a0e295b097c0/p08a/extraction.json"
)
P08A_EXTRACTION_SHA256 = "8a0386d360068ff3ee481ea88a170a41abeae6dce5716a55a7c75660859e4da0"
P08A_EXTRACTION_DIGEST = "5b33819c3df0d1380d62c8fbe9c0042f326340dc0b2b398224285a202652c576"
P08C_CARD_AUDIT = WORKSPACE / (
    ".local/mathdevmcp/evidence/p08-20260714/continuations/"
    "20260714T080342Z-3a1e3445eeab/p08c/card-audit.json"
)
P08C_CARD_AUDIT_SHA256 = "25360385c7fab0012965ac14cf9bdb11eef0687296e9f1ff46c616c882f6fcfd"
P08C_DECISION_DIGEST = "0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3"
PLAN_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-08c1-"
    "label-scoped-audit-integration-repair-subplan-2026-07-14.md"
)
RESULT_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-08c1-"
    "label-scoped-audit-integration-repair-result-2026-07-14.md"
)
CODE_REFS = (
    "scripts/run_p08c1_target_fidelity_replay.py",
    "src/mathdevmcp/document_derivation_tree.py",
    "src/mathdevmcp/derivation_target_extraction.py",
    "src/mathdevmcp/label_scoped_obligation.py",
)
SOURCE_BINDINGS = {
    "card": {
        "ref": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "sha256": "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
        "focus_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
        "target_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
        "context_labels": [],
    },
    "risky": {
        "ref": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
        "sha256": "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
        "focus_labels": ["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
        "target_labels": ["eq:foc-k", "eq:foc-b"],
        "context_labels": ["prop:interior-foc"],
    },
}
TARGET_LABELS = tuple(
    label for binding in SOURCE_BINDINGS.values() for label in binding["target_labels"]
)


class ReplayError(RuntimeError):
    pass


def _require_runtime_boundary() -> None:
    if Path.cwd().resolve() != WORKSPACE:
        raise ReplayError(f"replay must run from the workspace root: {WORKSPACE}")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise ReplayError("replay requires CUDA_VISIBLE_DEVICES=-1 before Python startup")


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReplayError("value is not canonical-JSON serializable") from exc


def _sha256(value: bytes | Any) -> str:
    raw = value if isinstance(value, bytes) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _read_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ReplayError(f"required regular file is absent or symlinked: {path}")
    return path.read_bytes()


def _load_canonical(path: Path) -> dict[str, Any]:
    raw = _read_bytes(path)
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReplayError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict) or _canonical(value) != raw:
        raise ReplayError(f"artifact is not a canonical JSON object: {path}")
    return value


def _write_new(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        raise ReplayError(f"replay never overwrites an artifact: {path}")
    raw = _canonical(dict(value))
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if _read_bytes(path) != raw:
        raise ReplayError(f"artifact reopen mismatch: {path}")


def _file_binding(path: Path, *, ref: str) -> dict[str, Any]:
    raw = _read_bytes(path)
    return {"ref": ref, "sha256": _sha256(raw), "byte_count": len(raw)}


def _require_frozen_inputs() -> dict[str, Any]:
    p08a_raw = _read_bytes(P08A_EXTRACTION)
    if _sha256(p08a_raw) != P08A_EXTRACTION_SHA256:
        raise ReplayError("immutable P08A extraction file SHA-256 drift")
    extraction = _load_canonical(P08A_EXTRACTION)
    if extraction.get("extraction_digest") != P08A_EXTRACTION_DIGEST:
        raise ReplayError("immutable P08A extraction semantic digest drift")
    p08c_raw = _read_bytes(P08C_CARD_AUDIT)
    if _sha256(p08c_raw) != P08C_CARD_AUDIT_SHA256:
        raise ReplayError("immutable P08C card audit SHA-256 drift")
    for binding in SOURCE_BINDINGS.values():
        if _sha256(_read_bytes(WORKSPACE / binding["ref"])) != binding["sha256"]:
            raise ReplayError(f"frozen source SHA-256 drift: {binding['ref']}")
    return extraction


def _obligations_by_label(extraction: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for group in extraction.get("groups", []):
        if not isinstance(group, Mapping):
            continue
        result = group.get("result") if isinstance(group.get("result"), Mapping) else {}
        for obligation in result.get("obligations", []):
            if not isinstance(obligation, Mapping):
                continue
            label = str(obligation.get("label", ""))
            if label not in TARGET_LABELS:
                continue
            candidate = dict(obligation)
            previous = records.get(label)
            if previous is not None and previous != candidate:
                raise ReplayError(f"P08A has inconsistent duplicate obligations for {label}")
            records[label] = candidate
    missing = sorted(set(TARGET_LABELS) - set(records))
    if missing:
        raise ReplayError(f"P08A lacks frozen target obligations: {missing}")
    return records


def _nonempty_backend_attempts(value: Any, *, path: str = "root") -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "backend_attempts" and isinstance(child, list) and child:
                found.append(child_path)
            found.extend(_nonempty_backend_attempts(child, path=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_nonempty_backend_attempts(child, path=f"{path}[{index}]"))
    return found


def _expected_lhs_rhs(obligation: Mapping[str, Any]) -> tuple[str, str, str]:
    normalized = obligation.get("normalized_target")
    if not isinstance(normalized, Mapping) or normalized.get("complete_lhs_rhs") is not True:
        raise ReplayError(f"P08A obligation is not complete: {obligation.get('label')}")
    members = [str(item) for item in normalized.get("members", [])]
    if len(members) < 2 or not all(members):
        raise ReplayError(f"P08A obligation lacks relation members: {obligation.get('label')}")
    token = r" \coloneqq " if normalized.get("kind") == "aligned_definition" else " = "
    return members[0], token.join(members[1:]), str(normalized["display_text"])


def _validate_document(
    document: str,
    audit: Mapping[str, Any],
    obligations: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    binding = SOURCE_BINDINGS[document]
    targets = [item for item in audit.get("targets", []) if isinstance(item, Mapping)]
    contexts = [item for item in audit.get("context_targets", []) if isinstance(item, Mapping)]
    extraction = audit.get("target_extraction") if isinstance(audit.get("target_extraction"), Mapping) else {}
    execution = audit.get("execution") if isinstance(audit.get("execution"), Mapping) else {}
    coverage = audit.get("coverage") if isinstance(audit.get("coverage"), Mapping) else {}
    if (
        audit.get("tex_path") != binding["ref"]
        or audit.get("publication_mode") != "disabled"
        or audit.get("publication_enabled") is not False
        or audit.get("promotion", {}).get("can_promote") is not False
        or execution.get("failure_count") != 0
        or execution.get("failures") != []
        or coverage.get("missing_focus_labels") != []
        or [item.get("label") for item in targets] != binding["target_labels"]
        or [item.get("label") for item in contexts] != binding["context_labels"]
        or extraction.get("method") != "validated_label_scoped_obligation"
        or extraction.get("failure_count") != 0
        or extraction.get("fallback_to_locator_row") is not False
        or extraction.get("selected_target_labels") != binding["target_labels"]
    ):
        raise ReplayError(f"{document} audit boundary or target order mismatch")
    backend_paths = _nonempty_backend_attempts(audit)
    if backend_paths:
        raise ReplayError(f"{document} replay contains backend attempts: {backend_paths[:4]}")

    comparisons: list[dict[str, Any]] = []
    for target in targets:
        label = str(target.get("label", ""))
        expected = obligations[label]
        packet = target.get("semantic_work_packet")
        tree = target.get("tree")
        if not isinstance(packet, Mapping) or not isinstance(tree, Mapping):
            raise ReplayError(f"{label} lacks semantic packet or tree")
        lhs, rhs, normalized_target = _expected_lhs_rhs(expected)
        typed = packet.get("typed_repair_obligation")
        tree_typed = tree.get("typed_repair_obligations")
        if (
            target.get("obligation_id") != expected["obligation_id"]
            or target.get("obligation_digest") != expected["obligation_digest"]
            or packet.get("target_ingress") != "validated_label_scoped_obligation"
            or packet.get("obligation_id") != expected["obligation_id"]
            or packet.get("obligation_digest") != expected["obligation_digest"]
            or packet.get("label_scoped_obligation") != expected
            or packet.get("normalized_target") != expected["normalized_target"]
            or packet.get("target") != normalized_target
            or packet.get("grouped_target") != normalized_target
            or packet.get("lhs") != lhs
            or packet.get("rhs") != rhs
            or packet.get("source_text") != expected["source_math"]
            or packet.get("full_display_source") != expected["source_math"]
            or packet.get("operator_inventory") != expected["operator_inventory"]
            or packet.get("symbol_inventory") != expected["symbol_inventory"]
            or packet.get("owned_spans") != expected["owned_spans"]
            or packet.get("excluded_spans") != expected["excluded_spans"]
            or packet.get("display_labels") != [label]
            or packet.get("source_span", {}).get("source_digest")
            != expected["document"]["source_digest"]
            or not isinstance(typed, Mapping)
            or typed.get("target") != normalized_target
            or typed.get("lhs") != lhs
            or typed.get("rhs") != rhs
            or not isinstance(tree_typed, list)
            or not tree_typed
            or tree_typed[0] != typed
            or any(
                blocker.get("kind") == "grouped_multiline_obligation_required"
                for blocker in tree.get("blockers", [])
                if isinstance(blocker, Mapping)
            )
            or tree.get("document_ready_repair_proposals") != []
        ):
            raise ReplayError(f"{label} differs from its exact P08A obligation")
        comparisons.append(
            {
                "label": label,
                "obligation_id": expected["obligation_id"],
                "obligation_digest": expected["obligation_digest"],
                "normalized_target_sha256": _sha256(expected["normalized_target"]),
                "source_math_sha256": _sha256(str(expected["source_math"]).encode("utf-8")),
                "owned_spans_sha256": _sha256(expected["owned_spans"]),
                "excluded_spans_sha256": _sha256(expected["excluded_spans"]),
                "semantic_packet_sha256": _sha256(packet),
                "complete_lhs_rhs": True,
                "exact_obligation_record_match": True,
                "tree_consumed_typed_packet": True,
            }
        )
    return comparisons


def _mutation_matrix(
    audits: Mapping[str, Mapping[str, Any]],
    obligations: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    mutations = {
        "target_text": lambda value: value["targets"][0]["semantic_work_packet"].__setitem__("target", "mutated"),
        "lhs_missing": lambda value: value["targets"][0]["semantic_work_packet"].__setitem__("lhs", ""),
        "obligation_digest": lambda value: value["targets"][0]["semantic_work_packet"].__setitem__("obligation_digest", "0" * 64),
        "owned_span": lambda value: value["targets"][0]["semantic_work_packet"]["owned_spans"][0].__setitem__("end_byte", -1),
        "operator_inventory": lambda value: value["targets"][0]["semantic_work_packet"].__setitem__("operator_inventory", ["equality", "summation"]),
        "obligation_record": lambda value: value["targets"][0]["semantic_work_packet"].__setitem__("label_scoped_obligation", {}),
        "target_order": lambda value: value["targets"].reverse(),
    }
    records: list[dict[str, Any]] = []
    for document, audit in audits.items():
        for mutation_id, mutate in mutations.items():
            candidate = deepcopy(audit)
            mutate(candidate)
            try:
                _validate_document(document, candidate, obligations)
            except (ReplayError, KeyError, IndexError, TypeError, AttributeError):
                rejected = True
            else:
                rejected = False
            if not rejected:
                raise ReplayError(f"target-fidelity validator accepted mutation: {document}/{mutation_id}")
            records.append({"document": document, "mutation_id": mutation_id, "rejected": True})
    return records


def _stale_p08c_diagnostic(obligations: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    audit = _load_canonical(P08C_CARD_AUDIT)
    target = next(
        item
        for item in audit.get("targets", [])
        if isinstance(item, Mapping) and item.get("label") == "eq:incremental-cash-flow"
    )
    packet = target.get("semantic_work_packet") if isinstance(target.get("semantic_work_packet"), Mapping) else {}
    expected = obligations["eq:incremental-cash-flow"]
    return {
        "authority": "diagnostic_history_only",
        "p08c_audit_sha256": P08C_CARD_AUDIT_SHA256,
        "p08c_decision_digest": P08C_DECISION_DIGEST,
        "label": "eq:incremental-cash-flow",
        "p08a_obligation_digest": expected["obligation_digest"],
        "p08c_target": packet.get("target"),
        "p08c_lhs": packet.get("lhs"),
        "p08c_rhs": packet.get("rhs"),
        "p08c_has_label_scoped_obligation": isinstance(packet.get("label_scoped_obligation"), Mapping),
        "exact_obligation_record_match": packet.get("label_scoped_obligation") == expected,
        "classification": "continuation_row_only_target_fidelity_defect",
    }


def _git_record() -> dict[str, Any]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
    ).stdout
    return {"commit": commit, "dirty": bool(status), "status_sha256": _sha256(status)}


def _code_bindings() -> list[dict[str, Any]]:
    return [_file_binding(WORKSPACE / ref, ref=ref) for ref in CODE_REFS]


def _comparison_record(
    audits: Mapping[str, Mapping[str, Any]],
    obligations: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    comparisons = {
        document: _validate_document(document, audit, obligations)
        for document, audit in audits.items()
    }
    return {
        "schema_version": "p08c1_target_fidelity@1",
        "question": "Do all five frozen audit targets preserve their exact P08A label-scoped obligations?",
        "comparator": {
            "ref": str(P08A_EXTRACTION.relative_to(WORKSPACE)),
            "sha256": P08A_EXTRACTION_SHA256,
            "extraction_digest": P08A_EXTRACTION_DIGEST,
        },
        "documents": comparisons,
        "ordered_target_labels": [
            item["label"] for document in ("card", "risky") for item in comparisons[document]
        ],
        "mutation_matrix": _mutation_matrix(audits, obligations),
        "stale_p08c_diagnostic": _stale_p08c_diagnostic(obligations),
        "primary_criterion_met": True,
        "vetoes": [],
        "non_claims": [
            "Target fidelity does not prove any frozen equation.",
            "The replay adds no mathematical backend evidence.",
            "The replay does not establish compact-product, publication, default, release, or mission readiness.",
        ],
    }


def _create(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    _require_runtime_boundary()
    extraction = _require_frozen_inputs()
    obligations = _obligations_by_label(extraction)
    sys.path.insert(0, str(WORKSPACE / "src"))
    from mathdevmcp.document_derivation_tree import audit_document_derivation_tree

    audits: dict[str, dict[str, Any]] = {}
    invocation_counts: dict[str, int] = {}
    for document, binding in SOURCE_BINDINGS.items():
        invocation_counts[document] = invocation_counts.get(document, 0) + 1
        audits[document] = audit_document_derivation_tree(
            Path(binding["ref"]),
            focus_labels=list(binding["focus_labels"]),
            max_labels=30,
            budget_profile="smoke",
            max_attempts=0,
            backend_env="mathdevmcp-backends",
            search_mode="agent_guided",
            grounding_policy="strict",
            workers=1,
        )
    if invocation_counts != {"card": 1, "risky": 1}:
        raise ReplayError("replay must invoke each document audit exactly once")
    comparison = _comparison_record(audits, obligations)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = _sha256({"timestamp": timestamp, "code": _code_bindings()})[:12]
    run_root = Path(args.output_root) / f"{timestamp}-{suffix}"
    run_root = (WORKSPACE / run_root).resolve() if not run_root.is_absolute() else run_root.resolve()
    expected_parent = (WORKSPACE / ".local/mathdevmcp/evidence/p08-20260714/p08c1").resolve()
    if run_root.parent != expected_parent:
        raise ReplayError(f"run root must be a direct child of {expected_parent}")
    if run_root.exists() or run_root.is_symlink():
        raise ReplayError(f"fresh replay root already exists: {run_root}")

    _write_new(run_root / "card-audit.json", audits["card"])
    _write_new(run_root / "risky-audit.json", audits["risky"])
    _write_new(run_root / "target-fidelity.json", comparison)
    manifest = {
        "schema_version": "p08c1_run_manifest@1",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git": _git_record(),
        "command": [str(item) for item in sys.argv],
        "interpreter": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "environment": os.environ.get("CONDA_DEFAULT_ENV") or "system/default Python environment",
        "cpu_gpu": "CPU-only replay; CUDA devices intentionally hidden.",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "seeds": "N/A; deterministic parsing and audit with max_attempts=0",
        "wall_time_seconds": round(time.monotonic() - started, 6),
        "raw_audit_invocations": invocation_counts,
        "mathematical_backend_attempt_count": 0,
        "source_bindings": SOURCE_BINDINGS,
        "p08a_extraction_sha256": P08A_EXTRACTION_SHA256,
        "code_bindings": _code_bindings(),
        "plan_ref": PLAN_REF,
        "result_ref": RESULT_REF,
    }
    _write_new(run_root / "run-manifest.json", manifest)
    inventory = [
        _file_binding(run_root / ref, ref=ref)
        for ref in ("card-audit.json", "risky-audit.json", "target-fidelity.json", "run-manifest.json")
    ]
    decision = {
        "schema_version": "p08c1_decision@1",
        "status": "PASS_P08C1_TARGET_FIDELITY",
        "primary_criterion_met": True,
        "vetoes": [],
        "raw_audit_invocations": invocation_counts,
        "mathematical_backend_attempt_count": 0,
        "publication_enabled": False,
        "can_promote": False,
        "formal_proof_certified": False,
        "artifact_inventory": inventory,
        "artifact_inventory_digest": _sha256(inventory),
        "non_claims": comparison["non_claims"],
    }
    decision["decision_digest"] = _sha256(decision)
    _write_new(run_root / "decision.json", decision)
    return {
        "status": decision["status"],
        "run_root": str(run_root.relative_to(WORKSPACE)),
        "decision_digest": decision["decision_digest"],
    }


def _verify(args: argparse.Namespace) -> dict[str, Any]:
    _require_runtime_boundary()
    extraction = _require_frozen_inputs()
    obligations = _obligations_by_label(extraction)
    run_root = Path(args.run_root)
    run_root = (WORKSPACE / run_root).resolve() if not run_root.is_absolute() else run_root.resolve()
    expected_parent = (WORKSPACE / ".local/mathdevmcp/evidence/p08-20260714/p08c1").resolve()
    if run_root.parent != expected_parent:
        raise ReplayError(f"run root must be a direct child of {expected_parent}")
    decision = _load_canonical(run_root / "decision.json")
    expected_digest = _sha256({key: value for key, value in decision.items() if key != "decision_digest"})
    if decision.get("decision_digest") != expected_digest:
        raise ReplayError("decision digest mismatch")
    if args.expected_decision_digest and decision["decision_digest"] != args.expected_decision_digest:
        raise ReplayError("decision differs from create handoff")
    inventory = [
        _file_binding(run_root / ref, ref=ref)
        for ref in ("card-audit.json", "risky-audit.json", "target-fidelity.json", "run-manifest.json")
    ]
    if (
        decision.get("status") != "PASS_P08C1_TARGET_FIDELITY"
        or decision.get("primary_criterion_met") is not True
        or decision.get("vetoes") != []
        or decision.get("mathematical_backend_attempt_count") != 0
        or decision.get("publication_enabled") is not False
        or decision.get("can_promote") is not False
        or decision.get("artifact_inventory") != inventory
        or decision.get("artifact_inventory_digest") != _sha256(inventory)
    ):
        raise ReplayError("decision boundary or inventory mismatch")
    manifest = _load_canonical(run_root / "run-manifest.json")
    if (
        manifest.get("schema_version") != "p08c1_run_manifest@1"
        or manifest.get("raw_audit_invocations") != {"card": 1, "risky": 1}
        or manifest.get("mathematical_backend_attempt_count") != 0
        or manifest.get("p08a_extraction_sha256") != P08A_EXTRACTION_SHA256
        or manifest.get("code_bindings") != _code_bindings()
    ):
        raise ReplayError("run manifest mismatch")
    audits = {
        "card": _load_canonical(run_root / "card-audit.json"),
        "risky": _load_canonical(run_root / "risky-audit.json"),
    }
    reconstructed = _comparison_record(audits, obligations)
    if _load_canonical(run_root / "target-fidelity.json") != reconstructed:
        raise ReplayError("target-fidelity artifact differs from independent reconstruction")
    return {
        "status": decision["status"],
        "verified": True,
        "run_root": str(run_root.relative_to(WORKSPACE)),
        "decision_digest": decision["decision_digest"],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument(
        "--output-root",
        default=".local/mathdevmcp/evidence/p08-20260714/p08c1",
    )
    create.set_defaults(handler=_create)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--run-root", required=True)
    verify.add_argument("--expected-decision-digest")
    verify.set_defaults(handler=_verify)
    return parser


def main() -> int:
    try:
        args = _parser().parse_args()
        print(json.dumps(args.handler(args), sort_keys=True))
        return 0
    except (ReplayError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(json.dumps({"status": "ERROR_P08C1_REPLAY", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
