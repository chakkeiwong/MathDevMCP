from __future__ import annotations

"""Audit, preflight, or create the additive P03R2 round-close recovery."""

import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
BOOTSTRAP_REF = "docs/plans/p03r2_round_close_recovery_20260713.py"
PLAN_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-subplan-2026-07-13.md"
BUDGET_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-review-budget-2026-07-13.json"
CONSUMPTION_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-review-budget-consumption-2026-07-13.json"
PLAN_REVIEW_R1_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-plan-review-r1-result-2026-07-13.md"
PLAN_REVIEW_R2_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-plan-review-r2-result-2026-07-13.md"
PLAN_REVIEW_R3_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-plan-review-r3-result-2026-07-13.md"
PLAN_REVIEW_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-plan-review-r4-result-2026-07-13.md"
RESULT_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-result-2026-07-13.md"
RESULT_REVIEW_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-result-review-r1-result-2026-07-13.md"
REHEARSAL_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-rehearsal-result-2026-07-13.json"
RECOVERY_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/round-close-recovery.json"
ORDINARY_CLOSE_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/round-close.json"
RR02_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr02"
STABLE_REF = ".local/mathdevmcp/evidence/p03-20260712/phase-results/P03-decision.json"
GOVERNANCE_REF = "scripts/p03_governance.py"
CONTEXT_REF = "src/mathdevmcp/context_evidence.py"
TEST_REF = "tests/test_context_evidence.py"

RESULT_REVIEW_RR01_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03-result-review-rr01-result-2026-07-12.md"
SCOPED_REPAIR_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/scoped-repair.json"
RECEIPT20_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-20.json"
INDEX20_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-index-20.json"
RECEIPT21_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-21.json"
INDEX21_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-index-21.json"
RECEIPT22_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-22.json"
INDEX22_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-index-22.json"
STDERR_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/logs/close-round.stderr"
ORIGINAL_CONTROLLER_REF = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/implementation-exit-sha256.txt"
ENTRY_RECORD_REF = ".local/mathdevmcp/evidence/p03-20260712/entry/entry-record.json"

FIXED_DIGESTS = {
    RESULT_REVIEW_RR01_REF: "4524a31392a3f44313eef1ca365c7f6772c738374aa08b090b34a6a163f5abbd",
    SCOPED_REPAIR_REF: "d56ffeea654bba740c74dca8b9b4fb086dd2121c860c194fb8d3bda077edc8e8",
    RECEIPT20_REF: "0fa2a0ca60e9f74fe26de58d8b8c6ea7827070cae403490c84158a2a853834e3",
    INDEX20_REF: "c1ea34780bfa7f964e1159beb9b7d50b1d1bc9e6cd988150fc93907411e3bd1c",
    RECEIPT21_REF: "43aeade9321f1ffc71c2cbc667aa60f254ce2de308bb97a9dae9d6ed5601d182",
    INDEX21_REF: "0a84685796cbe33b98e89806afe82ca3c8d868fcaa79d5678be171be831b60cb",
    RECEIPT22_REF: "1b06a16752b50549f6576e859d9dcd801f25fd56e99b72c489a7fd954e04f4e1",
    INDEX22_REF: "fc222e0e65cf252b07687427dab2f9be52deb81c2bb4d38c625e181430f64429",
    STDERR_REF: "4afc5d90fa1675eb3cef5386a977dd5d9142959d7556b3677bf22f95687ce57b",
    ORIGINAL_CONTROLLER_REF: "db5f4528ce70a35b1fcb572964508a028cff03407f5d0cfe1fa4a030d1851101",
}
ORIGINAL_CONTROLLER_SHA256 = "5125ebc3239916bf51c3f07b161eb7a3082d8c84477417956d48cfb23a4cd5fc"
PLAN_REVIEW_R1_SHA256 = "83a710e15064c0a8d8b72452c1f2801ef8fd1715f539564b3a81191673ac0779"
PLAN_REVIEW_R2_SHA256 = "458ffeacfd9c4bd5e5294d965210d619b62e107b5d92ae197fb64d9dbfe95147"
PLAN_REVIEW_R3_SHA256 = "39f3e3a2fa4eb53705bbaf79c79a900e26a7f7c3bee85698c6f0310b4ddbb6d0"
PASS_ACTIONS = (
    "init_round",
    "context_graph_tests",
    "resolver_tests",
    "symbol_assumption_tests",
    "report_boundary_tests",
    "frozen_context_regressions",
    "p00_quarantine",
    "generate_context_bundle",
    "mutation_gate",
    "zero_backend_source_edit_gate",
    "compile",
    "protected_check",
    "implementation_exit",
    "allowlist",
    "diff",
    "bind_result",
    "build_run_manifest",
    "build_candidate",
    "candidate_gate",
    "result_review_binding",
    "build_final_candidate",
    "final_candidate_gate",
    "final_seal_audit_binding",
    "stable_publication",
)
FAILURE_ACTIONS = ("bind_scoped_repair", "close_round")
FAILED_CHAIN_ACTIONS = (*PASS_ACTIONS[:20], *FAILURE_ACTIONS)
NON_CLAIMS = [
    "Recovery does not change the failed close_round receipt or make it successful.",
    "Recovery is governance evidence only, not a Phase 03 pass or scientific claim.",
    "Publication, mathematical backends, source edits, Phase 04, and release readiness remain disabled.",
]
EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p03r2-recovery-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}


def _root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("P03R2 recovery must run at the repository root")
    return root


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"P03R2 recovery artifact is not regular: {ref}")
    return raw


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _json(root: Path, ref: str) -> dict[str, Any]:
    raw = _read(root, ref)
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"P03R2 recovery JSON is invalid: {ref}") from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"P03R2 recovery JSON is noncanonical: {ref}")
    return value


def _review(root: Path, ref: str, required: dict[str, str]) -> str:
    raw = _read(root, ref)
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"P03R2 review bytes are invalid: {ref}")
    lines = raw.decode("utf-8", "strict").splitlines()
    for label, digest in required.items():
        expected = f"{label}: `{digest}`"
        if lines.count(expected) != 1 or sum(label in line for line in lines) != 1:
            raise EvidenceValidationError(f"P03R2 review binding mismatch: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if verdicts != ["VERDICT: AGREE"] or not nonempty or nonempty[-1] != "VERDICT: AGREE":
        raise EvidenceValidationError(f"P03R2 review is not uniquely agreeing: {ref}")
    return content_digest(raw)


def _verify_fixed(root: Path) -> None:
    for ref, digest in FIXED_DIGESTS.items():
        if _sha(root, ref) != digest:
            raise EvidenceValidationError(f"P03R2 fixed artifact drift: {ref}")
    _verify_failed_chain(root)
    receipt20 = _json(root, RECEIPT20_REF)
    receipt21 = _json(root, RECEIPT21_REF)
    receipt22 = _json(root, RECEIPT22_REF)
    if (
        receipt20.get("action") != "result_review_binding"
        or receipt20.get("exit_code") != 0
        or receipt20.get("bindings", {}).get("review_verdict") != "REVISE"
        or receipt21.get("action") != "bind_scoped_repair"
        or receipt21.get("exit_code") != 0
        or receipt21.get("bindings", {}).get("scoped_repair_sha256") != FIXED_DIGESTS[SCOPED_REPAIR_REF]
        or receipt22.get("action") != "close_round"
        or receipt22.get("exit_code") != 1
        or any(value is not None for value in receipt22.get("bindings", {}).values())
        or _read(root, STDERR_REF)
        != b"EvidenceValidationError: Phase 03 scoped-repair trigger binding mismatch\n"
    ):
        raise EvidenceValidationError("P03R2 failed-close state mismatch")
    receipt13 = _json(root, ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-13.json")
    if receipt13.get("bindings") != {
        "implementation_exit_manifest_ref": ORIGINAL_CONTROLLER_REF,
        "implementation_exit_manifest_sha256": FIXED_DIGESTS[ORIGINAL_CONTROLLER_REF],
    }:
        raise EvidenceValidationError("P03R2 implementation manifest is not bound by receipt 13")
    original_manifest = _read(root, ORIGINAL_CONTROLLER_REF).decode("utf-8", "strict").splitlines()
    expected = f"{ORIGINAL_CONTROLLER_SHA256}  {GOVERNANCE_REF}"
    if original_manifest.count(expected) != 1:
        raise EvidenceValidationError("P03R2 original controller provenance mismatch")


def _verify_failed_chain(root: Path) -> None:
    terminal = _json(root, INDEX22_REF)
    if (
        set(terminal) != {"schema_version", "phase", "result_round", "receipts", "head_sequence", "head_sha256"}
        or terminal["schema_version"] != "p03_receipt_index@1"
        or terminal["phase"] != "P03"
        or terminal["result_round"] != "rr01"
        or terminal["head_sequence"] != 22
        or len(terminal["receipts"]) != 22
        or terminal["head_sha256"] != FIXED_DIGESTS[RECEIPT22_REF]
    ):
        raise EvidenceValidationError("P03R2 terminal receipt-index schema mismatch")
    prior: str | None = None
    for sequence, (entry, action) in enumerate(zip(terminal["receipts"], FAILED_CHAIN_ACTIONS, strict=True), start=1):
        receipt_ref = f".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-{sequence:02d}.json"
        if entry != {
            "sequence": sequence,
            "action": action,
            "receipt_ref": receipt_ref,
            "receipt_sha256": entry.get("receipt_sha256"),
        }:
            raise EvidenceValidationError("P03R2 terminal receipt-index entry mismatch")
        raw = _read(root, receipt_ref)
        if content_digest(raw) != entry["receipt_sha256"]:
            raise EvidenceValidationError("P03R2 receipt digest drift")
        receipt = _json(root, receipt_ref)
        if (
            receipt.get("schema_version") != "p03_command_receipt@1"
            or receipt.get("phase") != "P03"
            or receipt.get("result_round") != "rr01"
            or receipt.get("sequence") != sequence
            or receipt.get("action") != action
            or receipt.get("prior_receipt_sha256") != prior
        ):
            raise EvidenceValidationError("P03R2 receipt chain mismatch")
        for stream in ("stdout", "stderr"):
            stream_raw = _read(root, receipt[f"{stream}_ref"])
            if (
                content_digest(stream_raw) != receipt[f"{stream}_sha256"]
                or len(stream_raw) != receipt[f"{stream}_byte_count"]
            ):
                raise EvidenceValidationError("P03R2 receipt stream binding drift")
        prior = entry["receipt_sha256"]
    for sequence, ref, expected_digest in (
        (20, INDEX20_REF, FIXED_DIGESTS[INDEX20_REF]),
        (21, INDEX21_REF, FIXED_DIGESTS[INDEX21_REF]),
    ):
        prefix_raw = _read(root, ref)
        if content_digest(prefix_raw) != expected_digest:
            raise EvidenceValidationError("P03R2 receipt-index prefix digest drift")
        prefix = _json(root, ref)
        expected = {
            **terminal,
            "receipts": terminal["receipts"][:sequence],
            "head_sequence": sequence,
            "head_sha256": terminal["receipts"][sequence - 1]["receipt_sha256"],
        }
        if prefix != expected:
            raise EvidenceValidationError("P03R2 receipt-index prefix is not exact")


def _verify_absence(root: Path, *, recovery_may_exist: bool) -> None:
    refs = [ORDINARY_CLOSE_REF, RR02_REF, STABLE_REF]
    if not recovery_may_exist:
        refs.append(RECOVERY_REF)
    for ref in refs:
        path = root / ref
        if path.exists() or path.is_symlink():
            raise EvidenceValidationError(f"P03R2 recovery requires absent path: {ref}")


def _authority(root: Path) -> tuple[str, str]:
    value = _json(root, BUDGET_REF)
    if (
        value.get("schema_version") != "p03r2_review_budget_authorization@1"
        or value.get("phase") != "P03"
        or value.get("authority") != "human_user"
        or value.get("additional_review_rounds_authorized") != 5
        or value.get("remaining_additional_rounds_after_planned_uses") != 2
        or value.get("final_seal_audit_reservation")
        != "original_distinct_reservation_remains_untouched"
    ):
        raise EvidenceValidationError("P03R2 review authority mismatch")
    consumption = _json(root, CONSUMPTION_REF)
    if (
        consumption.get("schema_version") != "p03r2_review_budget_consumption@1"
        or consumption.get("source_authority_ref") != BUDGET_REF
        or consumption.get("source_authority_sha256") != _sha(root, BUDGET_REF)
        or consumption.get("additional_review_rounds_authorized") != 5
        or consumption.get("remaining_unallocated_additional_rounds") != 0
        or consumption.get("planned_remaining_reviews") != [
            "p03r2_round_close_recovery_result_review",
            "replacement_p03_result_review",
        ]
        or consumption.get("final_seal_audit_reservation")
        != "original_distinct_reservation_remains_untouched"
        or consumption.get("consumed_reviews") != [
            {
                "review_kind": "p03r2_round_close_recovery_plan_review_r1",
                "review_ref": PLAN_REVIEW_R1_REF,
                "review_sha256": PLAN_REVIEW_R1_SHA256,
                "verdict": "REVISE",
            },
            {
                "review_kind": "p03r2_round_close_recovery_plan_review_r2",
                "review_ref": PLAN_REVIEW_R2_REF,
                "review_sha256": PLAN_REVIEW_R2_SHA256,
                "verdict": "REVISE",
            },
            {
                "review_kind": "p03r2_round_close_recovery_plan_review_r3",
                "review_ref": PLAN_REVIEW_R3_REF,
                "review_sha256": PLAN_REVIEW_R3_SHA256,
                "verdict": "REVISE",
            },
        ]
        or _sha(root, PLAN_REVIEW_R1_REF) != PLAN_REVIEW_R1_SHA256
        or _sha(root, PLAN_REVIEW_R2_REF) != PLAN_REVIEW_R2_SHA256
        or _sha(root, PLAN_REVIEW_R3_REF) != PLAN_REVIEW_R3_SHA256
    ):
        raise EvidenceValidationError("P03R2 review-budget consumption mismatch")
    return _sha(root, BUDGET_REF), _sha(root, CONSUMPTION_REF)


def _plan_review(root: Path) -> str:
    return _review(
        root,
        PLAN_REVIEW_REF,
        {
            "Reviewed repaired P03R2 recovery plan SHA-256": _sha(root, PLAN_REF),
            "Reviewed repaired P03R2 recovery bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
            "Reviewed P03R2 review budget SHA-256": _sha(root, BUDGET_REF),
            "Reviewed P03R2 review consumption SHA-256": _sha(root, CONSUMPTION_REF),
            "Reviewed P03R2 R1 review SHA-256": PLAN_REVIEW_R1_SHA256,
            "Reviewed P03R2 R2 review SHA-256": PLAN_REVIEW_R2_SHA256,
            "Reviewed P03R2 R3 review SHA-256": PLAN_REVIEW_R3_SHA256,
            "Reviewed P03 rr01 terminal receipt-index SHA-256": FIXED_DIGESTS[INDEX22_REF],
            "Reviewed P03 rr01 failed close receipt SHA-256": FIXED_DIGESTS[RECEIPT22_REF],
        },
    )


def _result_review(root: Path, plan_review_sha256: str) -> str:
    return _review(
        root,
        RESULT_REVIEW_REF,
        {
            "Reviewed P03R2 recovery plan-review SHA-256": plan_review_sha256,
            "Reviewed repaired P03 governance SHA-256": _sha(root, GOVERNANCE_REF),
            "Reviewed repaired P03 context evidence SHA-256": _sha(root, CONTEXT_REF),
            "Reviewed repaired P03 context tests SHA-256": _sha(root, TEST_REF),
            "Reviewed P03R2 recovery bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
            "Reviewed P03R2 rehearsal result SHA-256": _sha(root, REHEARSAL_REF),
            "Reviewed P03R2 recovery result SHA-256": _sha(root, RESULT_REF),
        },
    )


def _expected_record(root: Path, *, recovery_may_exist: bool) -> dict[str, Any]:
    _verify_fixed(root)
    _verify_absence(root, recovery_may_exist=recovery_may_exist)
    budget_sha, consumption_sha = _authority(root)
    plan_review_sha = _plan_review(root)
    result_review_sha = _result_review(root, plan_review_sha)
    required_refs = (PLAN_REF, BOOTSTRAP_REF, PLAN_REVIEW_REF, RESULT_REF, RESULT_REVIEW_REF, REHEARSAL_REF)
    record = {
        "schema_version": "p03r2_round_close_recovery@1",
        "phase": "P03",
        "recovery": "P03R2",
        "result_round": "rr01",
        "decision": "blocked",
        "publication_mode": "disabled",
        "close_reason": "result_review_revise_with_failed_close_governance_recovery",
        "result_review_ref": RESULT_REVIEW_RR01_REF,
        "result_review_sha256": FIXED_DIGESTS[RESULT_REVIEW_RR01_REF],
        "source_receipt_index_ref": INDEX20_REF,
        "source_receipt_index_sha256": FIXED_DIGESTS[INDEX20_REF],
        "scoped_repair_ref": SCOPED_REPAIR_REF,
        "scoped_repair_sha256": FIXED_DIGESTS[SCOPED_REPAIR_REF],
        "scoped_repair_binding_receipt_ref": RECEIPT21_REF,
        "scoped_repair_binding_receipt_sha256": FIXED_DIGESTS[RECEIPT21_REF],
        "scoped_repair_binding_index_ref": INDEX21_REF,
        "scoped_repair_binding_index_sha256": FIXED_DIGESTS[INDEX21_REF],
        "failed_close_receipt_ref": RECEIPT22_REF,
        "failed_close_receipt_sha256": FIXED_DIGESTS[RECEIPT22_REF],
        "terminal_receipt_index_ref": INDEX22_REF,
        "terminal_receipt_index_sha256": FIXED_DIGESTS[INDEX22_REF],
        "failed_close_stderr_ref": STDERR_REF,
        "failed_close_stderr_sha256": FIXED_DIGESTS[STDERR_REF],
        "original_controller_sha256": ORIGINAL_CONTROLLER_SHA256,
        "repaired_controller_ref": GOVERNANCE_REF,
        "repaired_controller_sha256": _sha(root, GOVERNANCE_REF),
        "repaired_context_evidence_ref": CONTEXT_REF,
        "repaired_context_evidence_sha256": _sha(root, CONTEXT_REF),
        "repaired_test_ref": TEST_REF,
        "repaired_test_sha256": _sha(root, TEST_REF),
        "recovery_plan_ref": PLAN_REF,
        "recovery_plan_sha256": _sha(root, PLAN_REF),
        "recovery_budget_ref": BUDGET_REF,
        "recovery_budget_sha256": budget_sha,
        "recovery_budget_consumption_ref": CONSUMPTION_REF,
        "recovery_budget_consumption_sha256": consumption_sha,
        "recovery_plan_review_r1_ref": PLAN_REVIEW_R1_REF,
        "recovery_plan_review_r1_sha256": PLAN_REVIEW_R1_SHA256,
        "recovery_plan_review_r2_ref": PLAN_REVIEW_R2_REF,
        "recovery_plan_review_r2_sha256": PLAN_REVIEW_R2_SHA256,
        "recovery_plan_review_r3_ref": PLAN_REVIEW_R3_REF,
        "recovery_plan_review_r3_sha256": PLAN_REVIEW_R3_SHA256,
        "recovery_bootstrap_ref": BOOTSTRAP_REF,
        "recovery_bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "recovery_plan_review_ref": PLAN_REVIEW_REF,
        "recovery_plan_review_sha256": plan_review_sha,
        "recovery_result_ref": RESULT_REF,
        "recovery_result_sha256": _sha(root, RESULT_REF),
        "recovery_result_review_ref": RESULT_REVIEW_REF,
        "recovery_result_review_sha256": result_review_sha,
        "rehearsal_result_ref": REHEARSAL_REF,
        "rehearsal_result_sha256": _sha(root, REHEARSAL_REF),
        "original_close_action_exit_code": 1,
        "non_claims": NON_CLAIMS,
    }
    record["readiness_digest"] = content_digest(
        [
            {ref: _sha(root, ref) for ref in required_refs},
            record,
        ]
    )
    return record


def _verify_existing(root: Path) -> dict[str, Any]:
    value = _json(root, RECOVERY_REF)
    expected = _expected_record(root, recovery_may_exist=True)
    if value != expected:
        raise EvidenceValidationError("P03R2 existing recovery differs from exact reconstruction")
    return value


def _invocation(argv: list[str]) -> tuple[str, str | None]:
    if argv == ["--mode", "audit"]:
        mode, readiness = "audit", None
    elif argv == ["--mode", "preflight"]:
        mode, readiness = "preflight", None
    elif len(argv) == 4 and argv[:2] == ["--mode", "create"] and argv[2] == "--readiness-digest":
        digest = argv[3]
        if len(digest) == 64 and all(char in "0123456789abcdef" for char in digest):
            mode, readiness = "create", digest
        else:
            raise EvidenceValidationError("P03R2 recovery readiness digest is invalid")
    else:
        raise EvidenceValidationError("P03R2 recovery accepts audit, preflight, or readiness-bound create")
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("P03R2 recovery argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("P03R2 recovery environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("P03R2 recovery runtime flags are not exact")
    return mode, readiness


def main(argv: list[str] | None = None) -> int:
    mode, supplied = _invocation(sys.argv[1:] if argv is None else argv)
    root = _root()
    if mode == "audit":
        if (root / RECOVERY_REF).exists():
            _verify_existing(root)
            state = "RECOVERY_PRESENT_AND_VALID"
        else:
            _verify_fixed(root)
            _verify_absence(root, recovery_may_exist=False)
            _authority(root)
            state = "FAILED_CLOSE_PRESERVED"
        result = {"mode": mode, "state": state, "terminal_receipt_index_sha256": FIXED_DIGESTS[INDEX22_REF]}
    elif (root / RECOVERY_REF).exists() or (root / RECOVERY_REF).is_symlink():
        raise EvidenceValidationError("P03R2 preflight/create forbid an existing recovery path")
    else:
        record = _expected_record(root, recovery_may_exist=False)
        if mode == "preflight":
            result = {"mode": mode, "state": "READY_NO_WRITE", "readiness_digest": record["readiness_digest"]}
        else:
            if supplied != record["readiness_digest"]:
                raise EvidenceValidationError("P03R2 recovery readiness digest mismatch")
            atomic_write_bytes_no_replace(root, RECOVERY_REF, canonical_json_bytes(record), mode=0o600)
            if _verify_existing(root) != record:
                raise EvidenceValidationError("P03R2 recovery failed immediate reopen verification")
            result = {"mode": mode, "state": "RECOVERY_CREATED", "recovery_sha256": _sha(root, RECOVERY_REF)}
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvidenceValidationError as exc:
        sys.stdout.buffer.write(canonical_json_bytes({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}) + b"\n")
        raise SystemExit(2)
