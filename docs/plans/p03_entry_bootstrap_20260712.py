from __future__ import annotations

"""Preflight or create the reviewed Phase 03 entry snapshot exactly once."""

import json
import importlib.metadata as importlib_metadata
from email.parser import BytesParser
from email.policy import compat32
import os
from pathlib import Path
import runpy
import stat
import sys
import sysconfig
from typing import Any, Iterable

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)
from mathdevmcp.extraction_evidence import (
    validate_candidate,
    validate_final,
    verify_bundle_index,
    verify_obligation_bundle,
    verify_receipt_index,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
BOOTSTRAP_REF = "docs/plans/p03_entry_bootstrap_20260712.py"
PLAN_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-subplan-2026-07-12.md"
)
MASTER_REF = "docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md"
P02_CLOSE_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-close-2026-07-12.md"
P02_STABLE_REF = ".local/mathdevmcp/evidence/p02r3-20260712/phase-results/P02-decision.json"
P02_FINAL_REF = ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/P02-final-decision-candidate.json"
P02_TERMINAL_INDEX_REF = ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/receipts/receipt-index-24.json"
P02_BUNDLE_INDEX_REF = ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/extraction-bundle/bundle-index.json"
P02_OBLIGATIONS_REF = ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/extraction-bundle/obligations.json"
R1_REVIEW_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03-plan-review-r1-result-2026-07-12.md"
R1_BLOCKER_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03-plan-review-r1-blocker-result-2026-07-12.md"
REVIEW_REF = "docs/reviews/mathdevmcp-real-document-remediation-phase-03-plan-review-r2-result-2026-07-12.md"
BUDGET_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-03-review-budget-authorization-2026-07-12.json"
EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p03-20260712"
ENTRY_ROOT_REF = f"{EVIDENCE_ROOT_REF}/entry"
ENTRY_RECORD_REF = f"{ENTRY_ROOT_REF}/entry-record.json"
IMPLEMENTATION_MANIFEST_REF = f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt"
PROTECTED_MANIFEST_REF = f"{ENTRY_ROOT_REF}/protected-entry-sha256.txt"
IMMUTABLE_MANIFEST_REF = f"{ENTRY_ROOT_REF}/immutable-input-sha256.txt"

EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p03-entry-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}
EXPECTED_PYTHON_PREFIX = "/home/chakwong/miniconda3/envs/tfgpu"
EXPECTED_PYTHON_VERSION = "3.11.15"
EXPECTED_PURELIB = f"{EXPECTED_PYTHON_PREFIX}/lib/python3.11/site-packages"
EXPECTED_PYTEST_VERSION = "9.0.2"
EXPECTED_PYTEST_METADATA_REL = "pytest-9.0.2.dist-info/METADATA"
EXPECTED_PYTEST_METADATA_SHA256 = "14131718cc1f40cfecb5eac338037029a519b6392876100afec1e949f023d1ed"
EXPECTED_DIGESTS = {
    MASTER_REF: "5166192908f2a370a88538c07fefe79df984999059d85671087ddcc06a5b4182",
    P02_CLOSE_REF: "cdd9b708c18f3f5ea99d1a6e026d3c20f1b9cfa2fca2d7dbe21e329033c4a01b",
    P02_STABLE_REF: "f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d",
    P02_FINAL_REF: "f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d",
    P02_TERMINAL_INDEX_REF: "8f56a72b4575ee3c87122c8656931d7bbb5040a5a3c024edb5f2909b81a78fd0",
    P02_BUNDLE_INDEX_REF: "19776da1c8c9a548b19dcf6123a10af8755ab56355801b337847e1563995dc0d",
    P02_OBLIGATIONS_REF: "5aa6681e215d12f382e96f46f9f695cf80e1632affa0dd8bc39069eae78d85a0",
    "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex": (
        "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8"
    ),
    "docs/risky-debt-maliar-deep-learning-lecture-note.tex": (
        "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1"
    ),
}
REPAIR_HISTORY_DIGESTS = {
    R1_REVIEW_REF: "4e4c2c235f53b035ec4a5780f02165a4662630782e3f5862a524edbd4ab9cd03",
    R1_BLOCKER_REF: "0b76111e955eb6e555b9bb711ad4c876ed487ad878cbe53f62a63021d7eedf90",
}
P02_PASS_ACTIONS = (
    "init_round",
    "localizer_tests",
    "obligation_tests",
    "target_integration_tests",
    "parser_fidelity_tests",
    "frozen_regressions",
    "p00_quarantine",
    "generate_extraction_bundle",
    "mutation_ambiguity_gate",
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
P03_PASS_ACTIONS = (
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
P03_FAILURE_SUFFIX_ACTIONS = (
    "bind_scoped_repair",
    "close_round",
)
ALLOWLIST_EXACT = {
    "src/mathdevmcp/document_context_graph.py",
    "src/mathdevmcp/context_evidence.py",
    "src/mathdevmcp/latex_index.py",
    "src/mathdevmcp/document_derivation_tree.py",
    "src/mathdevmcp/math_ir.py",
    "src/mathdevmcp/notation_reconciliation.py",
    "scripts/generate_p03_context_evidence.py",
    "scripts/p03_governance.py",
    "tests/p03_no_backend_guard.py",
    "tests/test_context_evidence.py",
    "tests/test_context_real_regressions.py",
    "tests/test_document_context_graph.py",
    "tests/test_document_context_resolver.py",
    "tests/test_latex_index.py",
    "tests/test_document_derivation_tree.py",
    "tests/test_document_derivation_real_regressions.py",
    "tests/test_math_ir.py",
    "tests/test_notation_reconciliation.py",
}
ALLOWLIST_PREFIXES = ("tests/fixtures/document_context_graph/",)


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"P03 entry artifact is not regular: {ref}")
    return raw


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _strict_object(raw: bytes, name: str, *, canonical: bool = True) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON bytes")

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise EvidenceValidationError(f"{name} contains duplicate key {key}")
            value[key] = item
        return value

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict JSON") from exc
    if type(value) is not dict:
        raise EvidenceValidationError(f"{name} must be an object")
    if canonical and canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"{name} is not canonical JSON")
    return value


def _validate_invocation(argv: list[str]) -> str:
    if len(argv) != 2 or argv[0] != "--mode" or argv[1] not in {"preflight", "create"}:
        raise EvidenceValidationError("P03 bootstrap accepts exactly --mode preflight|create")
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("P03 bootstrap process argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("P03 bootstrap environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("P03 bootstrap runtime flags are not exact")
    return argv[1]


def _measure_runtime() -> dict[str, Any]:
    python_version = ".".join(str(item) for item in sys.version_info[:3])
    purelib = sysconfig.get_path("purelib")
    if (
        sys.prefix != EXPECTED_PYTHON_PREFIX
        or python_version != EXPECTED_PYTHON_VERSION
        or purelib != EXPECTED_PURELIB
    ):
        raise EvidenceValidationError("P03 bootstrap Python runtime provenance mismatch")

    distributions = [
        item
        for item in importlib_metadata.distributions(path=[purelib])
        if (item.metadata.get("Name") or "").casefold() == "pytest"
    ]
    if len(distributions) != 1:
        raise EvidenceValidationError("P03 bootstrap requires exactly one pytest distribution")
    distribution = distributions[0]
    dist_info, metadata_name = EXPECTED_PYTEST_METADATA_REL.split("/", 1)
    expected_distribution_path = Path(purelib) / dist_info
    distribution_path = getattr(distribution, "_path", None)
    metadata_matches = [
        item
        for item in (distribution.files or [])
        if str(item) == EXPECTED_PYTEST_METADATA_REL
    ]
    if (
        distribution.version != EXPECTED_PYTEST_VERSION
        or distribution_path != expected_distribution_path
        or len(metadata_matches) != 1
    ):
        raise EvidenceValidationError("P03 bootstrap pytest distribution provenance mismatch")

    purelib_fd = os.open(purelib, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        dist_fd = os.open(
            dist_info,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=purelib_fd,
        )
        try:
            metadata_fd = os.open(metadata_name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dist_fd)
            try:
                info = os.fstat(metadata_fd)
                if not stat.S_ISREG(info.st_mode):
                    raise EvidenceValidationError("P03 pytest metadata is not a regular file")
                chunks: list[bytes] = []
                while True:
                    chunk = os.read(metadata_fd, 65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
            finally:
                os.close(metadata_fd)
        finally:
            os.close(dist_fd)
    finally:
        os.close(purelib_fd)
    metadata_raw = b"".join(chunks)
    metadata_sha256 = content_digest(metadata_raw)
    if metadata_sha256 != EXPECTED_PYTEST_METADATA_SHA256:
        raise EvidenceValidationError("P03 pytest metadata bytes drifted")
    metadata = BytesParser(policy=compat32).parsebytes(metadata_raw, headersonly=True)
    if (
        metadata.get("Name") != "pytest"
        or metadata.get("Version") != EXPECTED_PYTEST_VERSION
        or distribution.metadata.get("Name") != metadata.get("Name")
        or distribution.version != metadata.get("Version")
    ):
        raise EvidenceValidationError("P03 pytest measured metadata identity mismatch")
    return {
        "schema_version": "p03_runtime_measurement@1",
        "measurement_method": "sys.version_info+sysconfig+importlib.metadata+nofollow_raw_metadata@1",
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "python_version": python_version,
        "python_version_source": "sys.version_info",
        "purelib": purelib,
        "pytest_distribution_path": str(distribution_path),
        "pytest_distribution_name": distribution.metadata["Name"],
        "pytest_version": distribution.version,
        "pytest_version_source": "stdlib_importlib.metadata_distribution",
        "pytest_metadata_relative_path": EXPECTED_PYTEST_METADATA_REL,
        "pytest_metadata_sha256": metadata_sha256,
        "pytest_metadata_byte_count": len(metadata_raw),
    }


def _manifest(root: Path, refs: Iterable[str]) -> bytes:
    unique = sorted(set(refs), key=lambda item: item.encode("utf-8"))
    if not unique:
        raise EvidenceValidationError("P03 entry manifest cannot be empty")
    records = []
    for ref in unique:
        records.append(f"{_sha(root, ref)}  {ref}\n".encode("utf-8"))
    return b"".join(records)


def _tree_refs(root: Path, top_ref: str) -> set[str]:
    top = root / top_ref
    if top.is_symlink() or not top.is_dir():
        raise EvidenceValidationError(f"protected evidence tree is unsafe: {top_ref}")
    refs: set[str] = set()
    for path in top.rglob("*"):
        if path.is_symlink():
            raise EvidenceValidationError(f"symlink in protected evidence tree: {path}")
        if path.is_file():
            refs.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise EvidenceValidationError(f"special path in protected evidence tree: {path}")
    return refs


def _implementation_refs(root: Path) -> set[str]:
    refs: set[str] = set()
    for top_name in ("src", "tests", "scripts"):
        for path in (root / top_name).rglob("*"):
            if path.is_symlink():
                raise EvidenceValidationError(f"symlink in implementation tree: {path}")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
                refs.add(path.relative_to(root).as_posix())
    return refs


def _dirty_refs(root: Path) -> set[str]:
    base = runpy.run_path(
        str(root / "docs/plans/p02_entry_bootstrap_20260711.py"),
        run_name="p03_entry_manifest_helpers",
    )
    return set(base["_dirty_refs"](root))


def _verify_p02(root: Path) -> dict[str, Any]:
    for ref, expected in EXPECTED_DIGESTS.items():
        if _sha(root, ref) != expected:
            raise EvidenceValidationError(f"P03 predecessor binding drift: {ref}")
    stable_raw = _read(root, P02_STABLE_REF)
    final_raw = _read(root, P02_FINAL_REF)
    if stable_raw != final_raw:
        raise EvidenceValidationError("P02 stable and final-candidate bytes differ")
    stable_info = os.stat(root / P02_STABLE_REF, follow_symlinks=False)
    final_info = os.stat(root / P02_FINAL_REF, follow_symlinks=False)
    if (
        not stat.S_ISREG(stable_info.st_mode)
        or not stat.S_ISREG(final_info.st_mode)
        or stable_info.st_dev != final_info.st_dev
        or stable_info.st_ino != final_info.st_ino
        or stable_info.st_nlink < 2
    ):
        raise EvidenceValidationError("P02 stable hard-link identity mismatch")
    final = validate_final(_strict_object(stable_raw, "P02 stable decision"))
    candidate_ref = final["candidate_decision_ref"]
    candidate_raw = _read(root, candidate_ref)
    if _sha(root, candidate_ref) != final["candidate_decision_sha256"]:
        raise EvidenceValidationError("P02 candidate binding drift")
    candidate = validate_candidate(_strict_object(candidate_raw, "P02 candidate"))
    chain = verify_receipt_index(root, P02_TERMINAL_INDEX_REF)
    if chain["index_sha256"] != EXPECTED_DIGESTS[P02_TERMINAL_INDEX_REF]:
        raise EvidenceValidationError("P02 terminal receipt-index digest mismatch")
    actions = tuple(item["record"]["check_id"] for item in chain["receipts"])
    if actions != P02_PASS_ACTIONS or any(item["record"]["exit_code"] != 0 for item in chain["receipts"]):
        raise EvidenceValidationError("P02 terminal action sequence is not the exact zero-exit pass path")
    terminal = chain["receipts"][-1]["record"]
    if terminal["bindings"].get("same_inode") is not True or terminal["bindings"].get("same_digest") is not True:
        raise EvidenceValidationError("P02 terminal publication equality is absent")
    bundle = verify_bundle_index(root, P02_BUNDLE_INDEX_REF)
    obligations = verify_obligation_bundle(root, P02_OBLIGATIONS_REF)
    records = obligations["record"]["obligations"]
    obligation_bindings = [
        {
            "obligation_digest": item["obligation"]["obligation_digest"],
            "extraction_state": item["obligation"]["extraction_state"],
            "adapter_eligible": item["obligation"]["adapter_eligible"],
        }
        for item in records
    ]
    digests = [item["obligation_digest"] for item in obligation_bindings]
    state_counts = {"valid_complete": 0, "ambiguous": 0, "orphaned": 0}
    eligible_count = 0
    for binding in obligation_bindings:
        state = binding["extraction_state"]
        eligible = binding["adapter_eligible"]
        if state not in state_counts or type(eligible) is not bool:
            raise EvidenceValidationError("P02 obligation state/eligibility is outside the P03 registry")
        state_counts[state] += 1
        eligible_count += int(eligible)
        if eligible != (state == "valid_complete"):
            raise EvidenceValidationError("P02 obligation state and adapter eligibility disagree")
    if (
        len(records) != 17
        or len(set(digests)) != 17
        or state_counts != {"valid_complete": 14, "ambiguous": 2, "orphaned": 1}
        or eligible_count != 14
        or bundle["record"]["semantic_digest"] != "98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395"
        or bundle["record"]["backend_request_count"] != 0
        or bundle["record"]["source_edit_count"] != 0
        or candidate["backend_request_count"] != 0
        or candidate["source_edit_count"] != 0
    ):
        raise EvidenceValidationError("P02 obligation/bundle boundary mismatch")
    return {
        "final": final,
        "candidate": candidate,
        "chain": chain,
        "obligation_bindings": obligation_bindings,
        "state_counts": state_counts,
        "eligible_count": eligible_count,
    }


def _verify_review(root: Path) -> str:
    raw = _read(root, REVIEW_REF)
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("P03 plan review violates bounded UTF-8 grammar")
    lines = raw.decode("utf-8", "strict").splitlines()
    required = {
        "Reviewed Phase 03 plan SHA-256": _sha(root, PLAN_REF),
        "Reviewed Phase 03 entry bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
        "Reviewed master plan SHA-256": EXPECTED_DIGESTS[MASTER_REF],
        "Reviewed P02 stable decision SHA-256": EXPECTED_DIGESTS[P02_STABLE_REF],
        "Reviewed P02 terminal receipt-index SHA-256": EXPECTED_DIGESTS[P02_TERMINAL_INDEX_REF],
        "Reviewed P02 extraction-bundle semantic digest": "98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395",
        "Reviewed P02 close SHA-256": EXPECTED_DIGESTS[P02_CLOSE_REF],
        "Reviewed Phase 03 R1 review SHA-256": REPAIR_HISTORY_DIGESTS[R1_REVIEW_REF],
        "Reviewed Phase 03 R1 blocker SHA-256": REPAIR_HISTORY_DIGESTS[R1_BLOCKER_REF],
    }
    for label, digest in required.items():
        line = f"{label}: `{digest}`"
        if lines.count(line) != 1 or sum(label in item for item in lines) != 1:
            raise EvidenceValidationError(f"P03 plan review binding is not unique: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if verdicts != ["VERDICT: AGREE"] or not nonempty or nonempty[-1] != "VERDICT: AGREE":
        raise EvidenceValidationError("P03 plan review is not uniquely agreeing")
    return content_digest(raw)


def _verify_budget(root: Path) -> tuple[str, dict[str, Any]]:
    raw = _read(root, BUDGET_REF)
    value = _strict_object(raw, "P03 review-budget authorization")
    expected_keys = {
        "schema_version",
        "phase",
        "date",
        "plan_sha256",
        "plan_review_sha256",
        "result_review_rounds_reserved",
        "final_seal_audit_rounds_reserved",
        "authority",
        "non_claim",
    }
    if (
        set(value) != expected_keys
        or value["schema_version"] != "p03_review_budget_authorization@1"
        or value["phase"] != "P03"
        or value["date"] != "2026-07-12"
        or value["plan_sha256"] != _sha(root, PLAN_REF)
        or value["plan_review_sha256"] != _sha(root, REVIEW_REF)
        or value["result_review_rounds_reserved"] != 1
        or value["final_seal_audit_rounds_reserved"] != 1
        or value["authority"] != "human_user"
        or value["non_claim"] != "Review budget is execution authority only, not a technical verdict or signature."
    ):
        raise EvidenceValidationError("P03 review-budget authorization mismatch")
    return content_digest(raw), value


def _mkdir_entry(root: Path) -> None:
    parent_ref = ".local/mathdevmcp/evidence"
    parent = root / parent_ref
    if parent.is_symlink() or not parent.is_dir():
        raise EvidenceValidationError("P03 evidence parent is unsafe")
    parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.mkdir("p03-20260712", mode=0o700, dir_fd=parent_fd)
        phase_fd = os.open("p03-20260712", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            os.mkdir("entry", mode=0o700, dir_fd=phase_fd)
        finally:
            os.close(phase_fd)
    finally:
        os.close(parent_fd)


def _preflight(root: Path) -> dict[str, Any]:
    if (root / EVIDENCE_ROOT_REF).exists() or (root / EVIDENCE_ROOT_REF).is_symlink():
        raise EvidenceValidationError("P03 evidence root must be absent")
    p02 = _verify_p02(root)
    for ref, expected in REPAIR_HISTORY_DIGESTS.items():
        if _sha(root, ref) != expected:
            raise EvidenceValidationError(f"P03 repair-history binding drift: {ref}")
    runtime = _measure_runtime()
    if _sha(root, PLAN_REF) == "" or _sha(root, BOOTSTRAP_REF) == "":
        raise EvidenceValidationError("P03 reviewed planning artifacts are empty")
    if (
        len(P03_PASS_ACTIONS) != 24
        or len(set(P03_PASS_ACTIONS)) != 24
        or P03_FAILURE_SUFFIX_ACTIONS != ("bind_scoped_repair", "close_round")
        or set(P03_PASS_ACTIONS) & set(P03_FAILURE_SUFFIX_ACTIONS)
    ):
        raise EvidenceValidationError("P03 action registry is not exact and unique")
    for ref in sorted(ALLOWLIST_EXACT, key=lambda item: item.encode("utf-8")):
        validate_logical_path(ref)
        if not ref.startswith(("src/", "tests/", "scripts/")):
            raise EvidenceValidationError("P03 implementation allowlist escapes implementation roots")
    for prefix in ALLOWLIST_PREFIXES:
        validate_logical_path(prefix.rstrip("/"))
        if not prefix.endswith("/") or not prefix.startswith("tests/fixtures/"):
            raise EvidenceValidationError("P03 implementation allowlist prefix is invalid")
    return {
        "mode": "preflight",
        "status": "PASS_NO_WRITE",
        "p02_stable_sha256": EXPECTED_DIGESTS[P02_STABLE_REF],
        "p02_terminal_receipt_index_sha256": p02["chain"]["index_sha256"],
        "p02_obligation_count": len(p02["obligation_bindings"]),
        "p02_ordered_obligation_bindings": p02["obligation_bindings"],
        "p02_obligation_state_counts": p02["state_counts"],
        "p02_adapter_eligible_count": p02["eligible_count"],
        "p03_pass_actions": list(P03_PASS_ACTIONS),
        "p03_failure_suffix_actions": list(P03_FAILURE_SUFFIX_ACTIONS),
        "runtime_measurement": runtime,
        "repaired_from_review_ref": R1_REVIEW_REF,
        "repaired_from_review_sha256": REPAIR_HISTORY_DIGESTS[R1_REVIEW_REF],
        "repair_blocker_ref": R1_BLOCKER_REF,
        "repair_blocker_sha256": REPAIR_HISTORY_DIGESTS[R1_BLOCKER_REF],
        "plan_sha256": _sha(root, PLAN_REF),
        "bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "entry_root_absent": True,
    }


def _create(root: Path) -> dict[str, Any]:
    preflight = _preflight(root)
    review_sha = _verify_review(root)
    budget_sha, _budget = _verify_budget(root)
    implementation_refs = _implementation_refs(root)
    implementation = _manifest(root, implementation_refs)
    immutable_refs = (
        set(EXPECTED_DIGESTS)
        | set(REPAIR_HISTORY_DIGESTS)
        | {PLAN_REF, BOOTSTRAP_REF, REVIEW_REF, BUDGET_REF}
    )
    immutable = _manifest(root, immutable_refs)
    output_refs = {IMPLEMENTATION_MANIFEST_REF, PROTECTED_MANIFEST_REF, IMMUTABLE_MANIFEST_REF, ENTRY_RECORD_REF}
    protected_refs = {
        ref
        for ref in _dirty_refs(root) - ALLOWLIST_EXACT - output_refs
        if not any(ref.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)
    }
    protected_refs.update(
        {
            PLAN_REF,
            BOOTSTRAP_REF,
            REVIEW_REF,
            R1_REVIEW_REF,
            R1_BLOCKER_REF,
            BUDGET_REF,
            MASTER_REF,
            P02_CLOSE_REF,
        }
    )
    for tree in (
        ".local/mathdevmcp/evidence/p00-20260711",
        ".local/mathdevmcp/evidence/p01-20260711",
        ".local/mathdevmcp/evidence/p02-20260711",
        ".local/mathdevmcp/evidence/p02r2-20260712",
        ".local/mathdevmcp/evidence/p02r3-20260712",
    ):
        protected_refs.update(_tree_refs(root, tree))
    protected = _manifest(root, protected_refs)
    record = {
        "schema_version": "p03_entry_record@1",
        "phase": "P03",
        "date": "2026-07-12",
        "reviewed_plan_ref": PLAN_REF,
        "reviewed_plan_sha256": _sha(root, PLAN_REF),
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "entry_bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "agreeing_plan_review_ref": REVIEW_REF,
        "agreeing_plan_review_sha256": review_sha,
        "review_budget_authorization_ref": BUDGET_REF,
        "review_budget_authorization_sha256": budget_sha,
        "repaired_from_review_ref": R1_REVIEW_REF,
        "repaired_from_review_sha256": REPAIR_HISTORY_DIGESTS[R1_REVIEW_REF],
        "repair_blocker_ref": R1_BLOCKER_REF,
        "repair_blocker_sha256": REPAIR_HISTORY_DIGESTS[R1_BLOCKER_REF],
        "master_plan_ref": MASTER_REF,
        "master_plan_sha256": EXPECTED_DIGESTS[MASTER_REF],
        "p02_close_ref": P02_CLOSE_REF,
        "p02_close_sha256": EXPECTED_DIGESTS[P02_CLOSE_REF],
        "p02_stable_decision_ref": P02_STABLE_REF,
        "p02_stable_decision_sha256": EXPECTED_DIGESTS[P02_STABLE_REF],
        "p02_terminal_receipt_index_ref": P02_TERMINAL_INDEX_REF,
        "p02_terminal_receipt_index_sha256": EXPECTED_DIGESTS[P02_TERMINAL_INDEX_REF],
        "p02_extraction_bundle_index_ref": P02_BUNDLE_INDEX_REF,
        "p02_extraction_bundle_index_sha256": EXPECTED_DIGESTS[P02_BUNDLE_INDEX_REF],
        "p02_obligations_ref": P02_OBLIGATIONS_REF,
        "p02_obligations_sha256": EXPECTED_DIGESTS[P02_OBLIGATIONS_REF],
        "p02_extraction_bundle_semantic_digest": "98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395",
        "p02_ordered_obligation_bindings": preflight["p02_ordered_obligation_bindings"],
        "p02_obligation_state_counts": preflight["p02_obligation_state_counts"],
        "p02_adapter_eligible_count": preflight["p02_adapter_eligible_count"],
        "p03_pass_actions": list(P03_PASS_ACTIONS),
        "p03_failure_suffix_actions": list(P03_FAILURE_SUFFIX_ACTIONS),
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "implementation_entry_manifest_sha256": content_digest(implementation),
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "protected_entry_manifest_sha256": content_digest(protected),
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "immutable_input_manifest_sha256": content_digest(immutable),
        "python": PYTHON,
        "python_version": preflight["runtime_measurement"]["python_version"],
        "pytest_version": preflight["runtime_measurement"]["pytest_version"],
        "runtime_measurement": preflight["runtime_measurement"],
        "device_mode": "cpu_only_no_gpu_requested",
        "publication_mode": "disabled",
        "implementation_allowlist_exact": sorted(ALLOWLIST_EXACT, key=lambda item: item.encode("utf-8")),
        "implementation_allowlist_prefixes": list(ALLOWLIST_PREFIXES),
    }
    payloads = {
        IMPLEMENTATION_MANIFEST_REF: implementation,
        PROTECTED_MANIFEST_REF: protected,
        IMMUTABLE_MANIFEST_REF: immutable,
        ENTRY_RECORD_REF: canonical_json_bytes(record),
    }
    _mkdir_entry(root)
    for ref in (IMPLEMENTATION_MANIFEST_REF, PROTECTED_MANIFEST_REF, IMMUTABLE_MANIFEST_REF, ENTRY_RECORD_REF):
        atomic_write_bytes_no_replace(root, ref, payloads[ref])
    reopened = {ref: _read(root, ref) for ref in payloads}
    if reopened != payloads:
        raise EvidenceValidationError("P03 entry reopen mismatch")
    phase = root / EVIDENCE_ROOT_REF
    entry = root / ENTRY_ROOT_REF
    if (
        phase.is_symlink()
        or entry.is_symlink()
        or {item.name for item in phase.iterdir()} != {"entry"}
        or {item.name for item in entry.iterdir()} != {Path(ref).name for ref in payloads}
        or any(item.is_symlink() or not item.is_file() for item in entry.iterdir())
    ):
        raise EvidenceValidationError("P03 entry tree shape mismatch")
    return {
        **preflight,
        "mode": "create",
        "status": "ENTRY_CREATED",
        "entry_record_ref": ENTRY_RECORD_REF,
        "entry_record_sha256": content_digest(reopened[ENTRY_RECORD_REF]),
    }


def main() -> int:
    mode = _validate_invocation(sys.argv[1:])
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("P03 bootstrap must run from the workspace root")
    result = _preflight(root) if mode == "preflight" else _create(root)
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.buffer.write(
            canonical_json_bytes({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}) + b"\n"
        )
        raise SystemExit(2)
