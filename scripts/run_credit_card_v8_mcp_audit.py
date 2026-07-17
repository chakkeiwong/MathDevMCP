from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from mathdevmcp import mcp_server
from mathdevmcp.mcp_facade import call_mcp_tool


WORKSPACE = Path(__file__).resolve().parent.parent
SOURCE = WORKSPACE / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
DOC_ROOT = SOURCE.parent
SOURCE_SHA256 = "e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b"
EVIDENCE_ROOT = WORKSPACE / ".local/mathdevmcp/evidence/credit-card-v8-mcp-audit-20260716"
ARTIFACT_ROOT = EVIDENCE_ROOT / "document-artifacts"
REPORT_ROOT = WORKSPACE / "docs/reviews/credit-card-v8-mcp-audit"

APPLICATION_LABELS = [
    "eq:panel-npv-functional",
    "eq:incremental-cash-flow",
    "eq:incremental-npv",
    "eq:terminal-value-base",
]

DEEP_LABELS = [
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

def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def _load_application_harness():
    path = WORKSPACE / "scripts/run_credit_card_mission_audit.py"
    spec = importlib.util.spec_from_file_location("mathdevmcp_v8_application_harness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the reviewed public-tool application harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_application_inventory() -> dict[str, Any]:
    harness = _load_application_harness()
    harness.SOURCE = SOURCE
    harness.DOC_ROOT = DOC_ROOT
    harness.DEFAULT_EVIDENCE_ROOT = EVIDENCE_ROOT
    harness.EVIDENCE_ROOT = EVIDENCE_ROOT
    harness.ARTIFACT_ROOT = EVIDENCE_ROOT / "application-document-artifacts"
    harness.FOCUS_LABELS = list(APPLICATION_LABELS)
    harness.EXPECTED_SOURCE_SHA256 = SOURCE_SHA256
    saved_argv = sys.argv
    try:
        sys.argv = [
            str(WORKSPACE / "scripts/run_credit_card_mission_audit.py"),
            "--source",
            str(SOURCE.relative_to(WORKSPACE)),
            "--artifact-root",
            str(EVIDENCE_ROOT.relative_to(WORKSPACE)),
        ]
        harness.main()
    finally:
        sys.argv = saved_argv
    return json.loads((EVIDENCE_ROOT / "tool-audit-manifest.json").read_text(encoding="utf-8"))


def invoke(name: str, arguments: dict[str, Any], output_name: str) -> dict[str, Any] | list[dict[str, Any]]:
    try:
        result = call_mcp_tool(name, arguments)
    except Exception as exc:  # Preserve public failures for critical inspection.
        result = {
            "ok": False,
            "status": "invocation_error",
            "tool": name,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }
    write_json(EVIDENCE_ROOT / "deep-results" / output_name, result)
    return result


def render_tool_application(manifest: dict[str, Any]) -> None:
    frozen = manifest.get("frozen_original_57", {}).get("records", [])
    added = manifest.get("current_registry_delta", {}).get("records", [])
    records = [*frozen, *added]
    lines = [
        "# Credit-Card v8 MCP Tool Application",
        "",
        f"Source: `{SOURCE.relative_to(WORKSPACE)}`",
        f"Source SHA-256: `{SOURCE_SHA256}`",
        "",
        "## Accounting",
        "",
        f"- Current registered tools: {manifest.get('registered_tool_count', 0)}",
        f"- Accounted tools: {manifest.get('accounted_tool_count', 0)}",
        f"- Missing tools: `{manifest.get('missing_registered_tools', [])}`",
        f"- Duplicate records: `{manifest.get('duplicate_tool_records', [])}`",
        "- A successful invocation is operational evidence only, not mathematical validation.",
        "",
        "## Tool Ledger",
        "",
        "| Tool | Classification | Status | Bytes | Contract | Error |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for record in records:
        result = record.get("result", {}) if isinstance(record.get("result"), dict) else {}
        error = result.get("error", "")
        if isinstance(error, dict):
            error = f"{error.get('type', '')}: {error.get('message', error)}"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record.get('tool', '')}`",
                    f"`{record.get('classification', '')}`",
                    f"`{result.get('status', '')}`",
                    str(result.get("byte_count", "")),
                    f"`{result.get('contract', '')}`",
                    str(error).replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Applicability Boundary",
            "",
            "Tools requiring a bound implementation, Python method body, literature theorem mapping, or explicit temporal field map are classified inapplicable when v8 does not supply that input. No unrelated input was invented to improve coverage.",
            "",
            "## Raw Evidence",
            "",
            f"Manifest: `{(EVIDENCE_ROOT / 'tool-audit-manifest.json').relative_to(WORKSPACE)}`",
            "",
        ]
    )
    (REPORT_ROOT / "credit-card-v8-mcp-tool-application.md").write_text("\n".join(lines), encoding="utf-8")


def run_native_markdown_reports() -> dict[str, Any]:
    (EVIDENCE_ROOT / "native-reports").mkdir(parents=True, exist_ok=True)
    common = {
        "focus_labels": DEEP_LABELS,
        "max_labels": len(DEEP_LABELS),
    }
    rigor = invoke(
        "audit_math_document_rigor",
        {
            "tex_path": str(SOURCE),
            **common,
            "backend_env": "mathdevmcp-backends",
            "validation_backends": ["sympy"],
            "response_mode": "compact",
            "artifact_root": str(ARTIFACT_ROOT),
            "output_md": str(REPORT_ROOT / "credit-card-v8-rigor-audit.md"),
            "output_json": str(EVIDENCE_ROOT / "native-reports/rigor-audit.json"),
        },
        "rigor-audit-result.json",
    )
    fix = invoke(
        "audit_and_propose_fix",
        {
            "question": "Audit the selected v8 equations and propose only source-bound, evidence-complete repairs.",
            "root": str(DOC_ROOT),
            "labels": DEEP_LABELS,
            "file": SOURCE.name,
            "source_digest": SOURCE_SHA256,
            "target_file": SOURCE.name,
            "source_digest": SOURCE_SHA256,
            "paragraph_context": True,
            "summary_only": True,
            "backend": "sympy",
            "validate_proposed_fixes": True,
            "backend_order": ["sympy"],
            "workers": 1,
            "output_path": str(REPORT_ROOT / "credit-card-v8-audit-and-fix.md"),
        },
        "audit-and-fix-result.json",
    )
    tree = invoke(
        "audit_document_derivation_tree",
        {
            "tex_path": str(SOURCE),
            **common,
            "budget_profile": "standard",
            "max_attempts": 3,
            "backend_env": "mathdevmcp-backends",
            "search_mode": "agent_guided",
            "grounding_policy": "strict",
            "workers": 1,
            "response_mode": "compact",
            "artifact_root": str(ARTIFACT_ROOT),
            "target_limit": 1,
            "output_md": str(REPORT_ROOT / "credit-card-v8-derivation-tree-audit.md"),
            "output_json": str(EVIDENCE_ROOT / "native-reports/derivation-tree-audit.json"),
        },
        "derivation-tree-compact-result.json",
    )
    assumptions = invoke(
        "audit_and_propose_assumptions",
        {
            "question": "Which explicit assumptions are needed by the selected v8 mathematical objects?",
            "root": str(DOC_ROOT),
            "labels": DEEP_LABELS,
            "file": SOURCE.name,
            "source_digest": SOURCE_SHA256,
            "provided_assumptions": ["terminal-value denominator is nonzero"],
            "output_path": str(REPORT_ROOT / "credit-card-v8-assumption-audit.md"),
        },
        "assumption-audit-result.json",
    )
    derivations = invoke(
        "audit_and_propose_derivations",
        {
            "question": "Which derivation steps or formalizations are unsupported in the selected v8 objects?",
            "root": str(DOC_ROOT),
            "labels": DEEP_LABELS,
            "file": SOURCE.name,
            "source_digest": SOURCE_SHA256,
            "assumptions": ["terminal-value denominator is nonzero"],
            "backend": "auto",
            "output_path": str(REPORT_ROOT / "credit-card-v8-derivation-audit.md"),
        },
        "derivation-audit-result.json",
    )
    return {
        "rigor": rigor,
        "fix": fix,
        "tree": tree,
        "assumptions": assumptions,
        "derivations": derivations,
    }


def run_packet_reports() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for label in DEEP_LABELS:
        token = label.replace(":", "_")
        arguments = {
            "root": str(DOC_ROOT),
            "label": label,
            "file": SOURCE.name,
            "source_digest": SOURCE_SHA256,
            "response_mode": "compact",
            "artifact_root": str(ARTIFACT_ROOT),
        }
        proof = invoke("proof_packet_label", arguments, f"proof-packet-{token}.json")
        negative = invoke("negative_evidence_label", arguments, f"negative-evidence-{token}.json")
        proof_raw = canonical_bytes(proof)
        negative_raw = canonical_bytes(negative)
        source = proof.get("source", {}) if isinstance(proof, dict) and isinstance(proof.get("source"), dict) else {}
        negative_source = negative.get("source", {}) if isinstance(negative, dict) and isinstance(negative.get("source"), dict) else {}
        role = source.get("routing_role", {}).get("role") if isinstance(source.get("routing_role"), dict) else None
        negative_role = negative_source.get("routing_role", {}).get("role") if isinstance(negative_source.get("routing_role"), dict) else None
        if not role or role != negative_role:
            raise RuntimeError(f"proof/negative canonical routing role drift for {label}: {role!r} != {negative_role!r}")
        rows.append(
            {
                "label": label,
                "role": role,
                "proof_status": proof.get("status") if isinstance(proof, dict) else None,
                "negative_status": negative.get("status") if isinstance(negative, dict) else None,
                "source_file": source.get("file"),
                "source_digest": source.get("source_digest"),
                "source_status": source.get("status"),
                "proof_bytes": len(proof_raw),
                "negative_bytes": len(negative_raw),
                "proof_sha256": digest_bytes(proof_raw),
                "negative_sha256": digest_bytes(negative_raw),
            }
        )
    lines = [
        "# Credit-Card v8 Proof And Negative-Evidence Packets",
        "",
        "These packets are diagnostic evidence bundles. Their statuses and sizes do not establish proof, refutation, causal validity, economic validity, or publication readiness.",
        "",
        "| Label | Source role | Proof status | Negative status | Source binding | Proof bytes | Negative bytes |",
        "| --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for row in rows:
        binding = f"{row['source_file']} / {row['source_digest'] or row['source_status']}"
        lines.append(
            f"| `{row['label']}` | `{row['role']}` | `{row['proof_status']}` | `{row['negative_status']}` | `{binding}` | {row['proof_bytes']} | {row['negative_bytes']} |"
        )
    lines.extend(["", "## Digest Ledger", ""])
    for row in rows:
        lines.append(f"- `{row['label']}` proof `{row['proof_sha256']}`; negative `{row['negative_sha256']}`")
    lines.extend(["", f"Raw packets: `{(EVIDENCE_ROOT / 'deep-results').relative_to(WORKSPACE)}`", ""])
    (REPORT_ROOT / "credit-card-v8-proof-and-negative-evidence-packets.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(EVIDENCE_ROOT / "packet-ledger.json", rows)
    return {"rows": rows}


def _normalized_fastmcp_payload(result: Any) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    public = result.model_dump(by_alias=True, exclude_none=True)
    structured = public.get("structuredContent")
    normalized = dict(structured) if isinstance(structured, dict) else None
    if normalized is not None:
        normalized.pop("ok", None)
    return normalized, public


def run_parity(tree: Any) -> dict[str, Any]:
    if not isinstance(tree, dict) or not isinstance(tree.get("page"), dict):
        return {"status": "blocked", "reason": "document tree did not return a compact page"}
    token = tree["page"].get("page_token")
    if not isinstance(token, str) or not token:
        return {"status": "blocked", "reason": "document tree did not return a continuation token"}
    command = [sys.executable, "-m", "mathdevmcp.cli", "audit-document-derivation-tree", str(SOURCE)]
    for label in DEEP_LABELS:
        command.extend(["--focus-label", label])
    command.extend(
        [
            "--max-labels", str(len(DEEP_LABELS)),
            "--budget-profile", "standard",
            "--max-attempts", "3",
            "--backend-env", "mathdevmcp-backends",
            "--search-mode", "agent_guided",
            "--grounding-policy", "strict",
            "--workers", "1",
            "--response-mode", "compact",
            "--artifact-root", str(ARTIFACT_ROOT),
            "--target-limit", "1",
            "--target-cursor", token,
        ]
    )
    completed = subprocess.run(
        command,
        cwd=WORKSPACE,
        env=dict(os.environ),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    cli = json.loads(completed.stdout) if completed.returncode == 0 else None
    server = mcp_server.audit_document_derivation_tree(
        str(SOURCE),
        focus_labels=DEEP_LABELS,
        max_labels=len(DEEP_LABELS),
        budget_profile="standard",
        max_attempts=3,
        backend_env="mathdevmcp-backends",
        search_mode="agent_guided",
        grounding_policy="strict",
        workers=1,
        response_mode="compact",
        artifact_root=str(ARTIFACT_ROOT),
        target_limit=1,
        target_cursor=token,
    )
    normalized_server, server_public = _normalized_fastmcp_payload(server)
    return {
        "status": "equal" if cli == normalized_server else "different",
        "cli_exit_code": completed.returncode,
        "cli_stderr": completed.stderr,
        "cli_sha256": digest_bytes(canonical_bytes(cli)),
        "server_sha256": digest_bytes(canonical_bytes(normalized_server)),
        "server_is_error": server_public.get("isError", False),
        "cli_status": cli.get("status") if isinstance(cli, dict) else None,
        "server_status": normalized_server.get("status") if isinstance(normalized_server, dict) else None,
        "publication_mode": cli.get("publication_mode") if isinstance(cli, dict) else None,
        "equal": cli == normalized_server,
    }


def main() -> None:
    if digest_bytes(SOURCE.read_bytes()) != SOURCE_SHA256:
        raise RuntimeError("v8 source digest changed before audit")
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = run_application_inventory()
    render_tool_application(manifest)
    reports = run_native_markdown_reports()
    packets = run_packet_reports()
    parity = run_parity(reports["tree"])
    write_json(EVIDENCE_ROOT / "public-surface-parity.json", parity)
    final_digest = digest_bytes(SOURCE.read_bytes())
    if final_digest != SOURCE_SHA256:
        raise RuntimeError("v8 source digest changed during audit")
    summary = {
        "source": str(SOURCE.relative_to(WORKSPACE)),
        "source_sha256": final_digest,
        "registered_tool_count": manifest.get("registered_tool_count"),
        "accounted_tool_count": manifest.get("accounted_tool_count"),
        "missing_registered_tools": manifest.get("missing_registered_tools"),
        "report_files": sorted(path.name for path in REPORT_ROOT.glob("*.md")),
        "packet_count": len(packets["rows"]),
        "parity": parity,
        "non_claims": [
            "The nine selected labels do not establish whole-document correctness.",
            "Successful invocation does not establish mathematical or scientific validity.",
            "No source edit, publication, or release action is authorized.",
        ],
    }
    write_json(EVIDENCE_ROOT / "v8-audit-summary.json", summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
