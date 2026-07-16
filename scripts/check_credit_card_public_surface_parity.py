from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import hashlib

from mathdevmcp import mcp_server


workspace = Path("/home/chakwong/python/MathDevMCP")
evidence = workspace / ".local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair"
first = json.loads((evidence / "tool-results/audit_document_derivation_tree.json").read_text())
token = first["page"]["page_token"]
artifact_root = evidence / "document-derivation-artifacts"
source = workspace / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex"
labels = [
    "eq:panel-npv-functional",
    "eq:incremental-cash-flow",
    "eq:incremental-npv",
    "eq:terminal-value-base",
]

command = [
    os.sys.executable,
    "-m",
    "mathdevmcp.cli",
    "audit-document-derivation-tree",
    str(source),
]
for label in labels:
    command.extend(["--focus-label", label])
command.extend(
    [
        "--max-labels",
        "4",
        "--budget-profile",
        "standard",
        "--max-attempts",
        "3",
        "--backend-env",
        "mathdevmcp-backends",
        "--search-mode",
        "agent_guided",
        "--grounding-policy",
        "strict",
        "--workers",
        "1",
        "--response-mode",
        "compact",
        "--artifact-root",
        str(artifact_root),
        "--target-limit",
        "1",
        "--target-cursor",
        token,
    ]
)
completed = subprocess.run(
    command,
    cwd=workspace,
    env=dict(os.environ),
    capture_output=True,
    text=True,
    timeout=60,
    check=False,
)
cli_result = json.loads(completed.stdout) if completed.returncode == 0 else None
server_result = mcp_server.audit_document_derivation_tree(
    str(source),
    focus_labels=labels,
    max_labels=4,
    budget_profile="standard",
    max_attempts=3,
    backend_env="mathdevmcp-backends",
    search_mode="agent_guided",
    grounding_policy="strict",
    workers=1,
    response_mode="compact",
    artifact_root=str(artifact_root),
    target_limit=1,
    target_cursor=token,
)
server_public = server_result.model_dump(by_alias=True, exclude_none=True)
server_structured = server_public.get("structuredContent")
normalized_server = dict(server_structured) if isinstance(server_structured, dict) else server_structured
if isinstance(normalized_server, dict):
    normalized_server.pop("ok", None)


def differences(left, right, path=""):
    if type(left) is not type(right):
        return [{"path": path, "left_type": type(left).__name__, "right_type": type(right).__name__}]
    if isinstance(left, dict):
        rows = []
        for key in sorted(set(left) | set(right)):
            child = f"{path}.{key}" if path else key
            if key not in left or key not in right:
                rows.append({"path": child, "left_present": key in left, "right_present": key in right})
            else:
                rows.extend(differences(left[key], right[key], child))
            if len(rows) >= 20:
                return rows
        return rows
    if isinstance(left, list):
        if len(left) != len(right):
            return [{"path": path, "left_length": len(left), "right_length": len(right)}]
        rows = []
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            rows.extend(differences(left_item, right_item, f"{path}[{index}]"))
            if len(rows) >= 20:
                return rows
        return rows
    return [] if left == right else [{"path": path, "left": left, "right": right}]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

print(
    json.dumps(
        {
            "cli_exit_code": completed.returncode,
            "cli_stderr_empty": not completed.stderr,
            "equal": cli_result == normalized_server,
            "transport_envelope_difference": "FastMCP structuredContent adds ok=true; CLI canonical response omits the facade envelope field.",
            "cli_status": cli_result.get("status") if isinstance(cli_result, dict) else None,
            "server_status": server_structured.get("status") if isinstance(server_structured, dict) else None,
            "server_is_error": server_public.get("isError", False),
            "cli_digest": digest(cli_result),
            "server_digest": digest(normalized_server),
            "differences": differences(cli_result, normalized_server),
            "page_index": cli_result.get("page", {}).get("page_index") if isinstance(cli_result, dict) else None,
            "target_ids": cli_result.get("page", {}).get("target_ids") if isinstance(cli_result, dict) else None,
            "publication_mode": cli_result.get("publication_mode") if isinstance(cli_result, dict) else None,
        },
        sort_keys=True,
    )
)
