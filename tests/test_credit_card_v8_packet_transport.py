from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

from mathdevmcp.agent_report_artifacts import (
    AGENT_REPORT_TRANSPORT_BYTES,
    compact_evidence_packet,
    persist_agent_report,
    resolve_agent_report,
)
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.mcp_server import negative_evidence_label, proof_packet_label
from mathdevmcp.document_derivation_response import (
    COMPACT_PAYLOAD_TARGET_BYTES,
    PUBLIC_TRANSPORT_TARGET_BYTES,
    build_document_derivation_audit_request,
    compile_document_derivation_response,
    document_derivation_public_surface_sizes,
    resolve_document_derivation_records,
)
from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.negative_evidence import build_negative_evidence_packet
from mathdevmcp.proof_packet import build_proof_packet_label


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
DIGEST = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
LABELS = [
    "eq:panel-npv-functional",
    "eq:incremental-cash-flow",
    "eq:pd-lgd-ead",
    "eq:balance-stock-flow",
    "eq:terminal-value-base",
    "eq:ss-bellman",
    "eq:causal-cashflow-object",
    "eq:experiment-late",
    "eq:randomization-assumption",
]


def _canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def _assert_compact_parity(compact: dict, detailed: dict, artifact_root: Path) -> None:
    source = detailed["source"]
    assert compact["status"] == detailed["status"]
    assert compact["source"] == source
    assert compact["source"]["target"] == source["target"]
    assert compact["source"]["normalized_target"] == source["normalized_target"]
    assert compact["source"]["routing_role"] == source["routing_role"]
    assert compact["source"]["specialist_execution"] == source["specialist_execution"]
    assert compact["vetoes"] == {
        "claim_eligibility": "ineligible",
        "publication_enabled": False,
        "promotion_allowed": False,
    }
    assert compact["non_claims"]
    assert compact["payload_guardrail"]["status"] == "met"
    assert compact["payload_guardrail"]["canonical_byte_count"] == len(_canonical(compact))
    assert len(_canonical(compact)) <= AGENT_REPORT_TRANSPORT_BYTES
    resolved = resolve_agent_report(artifact_root, compact["artifact"]["sha256"])
    assert resolved["report"] == detailed
    assert _canonical(resolved["report"]) == _canonical(detailed)


def test_all_v8_proof_and_negative_packets_are_bounded_and_exactly_resolvable(tmp_path: Path) -> None:
    for label in LABELS:
        proof = build_proof_packet_label(
            str(SOURCE.parent),
            label,
            file=SOURCE.name,
            source_digest=DIGEST,
            summary_only=True,
        )
        negative = build_negative_evidence_packet(label, proof["proof_audit_v2"])
        for detailed in (proof, negative):
            compact = compact_evidence_packet(detailed, persist_agent_report(detailed, tmp_path))
            _assert_compact_parity(compact, detailed, tmp_path)


def test_exact_packet_compact_cli_facade_fastmcp_parity(tmp_path: Path) -> None:
    label = "eq:terminal-value-base"
    arguments = {
        "root": str(SOURCE.parent),
        "label": label,
        "file": SOURCE.name,
        "source_digest": DIGEST,
        "summary_only": True,
        "response_mode": "compact",
        "artifact_root": str(tmp_path),
    }
    facade = call_mcp_tool("proof_packet_label", arguments)
    server = proof_packet_label(**arguments)
    command = [
        sys.executable,
        "-m",
        "mathdevmcp.cli",
        "proof-packet-label",
        label,
        "--root",
        str(SOURCE.parent),
        "--file",
        SOURCE.name,
        "--source-digest",
        DIGEST,
        "--summary-only",
        "--response-mode",
        "compact",
        "--artifact-root",
        str(tmp_path),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src"), "CUDA_VISIBLE_DEVICES": "-1"},
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    cli = json.loads(completed.stdout)
    normalized_facade = {key: value for key, value in facade.items() if key != "ok"}
    normalized_server = {key: value for key, value in server.items() if key != "ok"}
    assert cli == normalized_facade == normalized_server

    negative_args = {key: value for key, value in arguments.items() if key != "summary_only"}
    negative_facade = call_mcp_tool("negative_evidence_label", negative_args)
    negative_server = negative_evidence_label(**negative_args)
    assert negative_facade == negative_server
    assert len(_canonical(negative_facade)) <= AGENT_REPORT_TRANSPORT_BYTES


def test_compact_tree_writes_bounded_all_label_markdown(tmp_path: Path) -> None:
    output = tmp_path / "tree.md"
    result = call_mcp_tool(
        "audit_document_derivation_tree",
        {
            "tex_path": str(SOURCE),
            "focus_labels": LABELS,
            "max_labels": len(LABELS),
            "max_attempts": 1,
            "response_mode": "compact",
            "artifact_root": str(tmp_path / "artifacts"),
            "target_limit": 1,
            "output_md": str(output),
        },
    )

    assert result["ok"] is True
    raw = output.read_bytes()
    assert 0 < len(raw) <= AGENT_REPORT_TRANSPORT_BYTES
    text = raw.decode("utf-8")
    assert text.startswith("# Compact Document Derivation Tree Audit")
    assert all(label in text for label in LABELS)
    assert "Exact detailed records remain" in text
    assert "does not establish whole-document correctness" in text


def test_compact_rigor_writes_bounded_resolvable_markdown(tmp_path: Path) -> None:
    output = tmp_path / "rigor.md"
    artifact_root = tmp_path / "artifacts"
    result = call_mcp_tool(
        "audit_math_document_rigor",
        {
            "tex_path": str(SOURCE),
            "focus_labels": ["eq:ss-bellman", "eq:randomization-assumption"],
            "max_labels": 2,
            "validation_backends": ["sympy"],
            "response_mode": "compact",
            "artifact_root": str(artifact_root),
            "output_md": str(output),
        },
    )

    raw = output.read_bytes()
    assert 0 < len(raw) <= AGENT_REPORT_TRANSPORT_BYTES
    text = raw.decode("utf-8")
    assert text.startswith("# Compact Math Document Rigor Audit")
    assert "eq:ss-bellman" in text
    assert "eq:randomization-assumption" in text
    assert "bellman_transition_kernel" in text
    assert "assignment_mechanism_recorded" in text
    assert result["source"]["source_digest"] == DIGEST
    by_label = {item["label"]: item for item in result["target_selection"]["targets"]}
    assert "bellman_transition_kernel" in by_label["eq:ss-bellman"]["local_obligation_ids"]
    assert "assignment_mechanism_recorded" in by_label["eq:randomization-assumption"]["local_obligation_ids"]
    assert result["payload_guardrail"]["status"] == "met"
    resolved = resolve_agent_report(artifact_root, result["artifact"]["sha256"])
    assert resolved["report"]["source"]["source_digest"] == DIGEST


def test_all_v8_compact_tree_pages_meet_budget_and_resolve_exact_targets(tmp_path: Path) -> None:
    audit = audit_document_derivation_tree(
        SOURCE,
        focus_labels=LABELS,
        max_labels=len(LABELS),
        max_attempts=1,
    )
    request = build_document_derivation_audit_request(
        SOURCE,
        focus_labels=LABELS,
        max_labels=len(LABELS),
        max_attempts=1,
    )
    cursor = None
    seen: list[str] = []
    for expected_label in LABELS:
        response = compile_document_derivation_response(
            audit,
            request,
            response_mode="compact",
            artifact_root=tmp_path,
            target_limit=1,
            target_cursor=cursor,
        )
        sizes = document_derivation_public_surface_sizes(response)
        assert sizes["canonical_response"] <= COMPACT_PAYLOAD_TARGET_BYTES
        assert max(
            sizes["cli_stdout"],
            sizes["facade"],
            sizes["call_tool_result"],
            sizes["stdio_jsonrpc_line"],
        ) <= PUBLIC_TRANSPORT_TARGET_BYTES
        assert response["payload_guardrail"]["status"] == "met"
        target = response["targets"][0]
        assert target["label"] == expected_label
        assert target["source_evidence"]["target"]
        assert target["source_evidence"]["normalized_target"]["kind"]
        assert target["source_evidence"]["routing_role"]["role"]
        assert target["source_evidence"]["boundary"]["promotion_allowed"] is False
        target_id = target["target_id"]
        resolved_target = resolve_document_derivation_records(
            response["page"]["page_token"],
            "target_text",
            artifact_root=tmp_path,
            target_id=target_id,
        )
        resolved_obligation = resolve_document_derivation_records(
            response["page"]["page_token"],
            "label_scoped_obligation",
            artifact_root=tmp_path,
            target_id=target_id,
        )
        assert resolved_target["records"][0]["record"] == target["source_evidence"]["target"]
        assert resolved_obligation["records"][0]["record"]["obligation_digest"] == target["source_evidence"]["source"]["obligation_digest"]
        seen.append(target["label"])
        cursor = response["page"]["page_token"]
    assert seen == LABELS
