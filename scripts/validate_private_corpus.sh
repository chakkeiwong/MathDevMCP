#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/validate_private_corpus.sh ROOT [MANIFEST]

Validate a private MathDevMCP release corpus manifest without printing private
paths. MANIFEST defaults to MATHDEVMCP_PRIVATE_CORPUS_MANIFEST.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

ROOT="${1:-$(pwd)}"
MANIFEST="${2:-${MATHDEVMCP_PRIVATE_CORPUS_MANIFEST:-}}"

if [[ -z "$MANIFEST" ]]; then
  echo '{"status":"missing","reason":"No private manifest path was supplied.","private_paths_redacted":true}' >&2
  exit 2
fi

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST="$MANIFEST"

python - "$ROOT" "$MANIFEST" <<'PY'
import json
import sys
from pathlib import Path

from mathdevmcp.contracts import attach_contract
from mathdevmcp.parser_policy import decide_parser_policy
from mathdevmcp.release_corpus import release_corpus_manifest, validate_release_corpus_manifest

root = Path(sys.argv[1]).resolve()
manifest_path = Path(sys.argv[2]).expanduser().resolve()
fixture_root = root / "benchmarks" / "fixtures"

validation = validate_release_corpus_manifest(fixture_root, private_manifest=manifest_path)
full_manifest = release_corpus_manifest(fixture_root, private_manifest=manifest_path, include_private_paths=True)
entries = validation.get("manifest", {}).get("entries", [])
raw_entries = full_manifest.get("entries", [])
private_entries = [entry for entry in entries if str(entry.get("privacy_class", "")).startswith("private")]
release_gated = [entry for entry in private_entries if entry.get("release_gate_enabled")]
raw_by_id = {entry.get("id"): entry for entry in raw_entries}

findings = list(validation.get("findings", []))
parser_reports = []
for entry in release_gated:
    raw_entry = raw_by_id.get(entry.get("id"), {})
    expected_labels = entry.get("expected_labels", [])
    document_root = raw_entry.get("document_root")
    if document_root:
        parser_policy = decide_parser_policy(document_root, backends=entry.get("required_parser_backends") or ["current"], expected_labels=expected_labels)
        parser_status = parser_policy.get("status")
        parser_findings = parser_policy.get("blocking_findings", [])
    else:
        parser_status = "missing_document_root"
        parser_findings = [{"kind": "private_document_root_missing", "severity": "high"}]
    parser_reports.append(
        {
            "entry_id": entry.get("id"),
            "domain": entry.get("domain"),
            "status": parser_status,
            "expected_labels": expected_labels,
            "document_root": "<redacted-private-path>",
            "parser_findings": parser_findings,
        }
    )
    if parser_status != "selected_for_proof_audit":
        findings.append({"entry": entry.get("id"), "severity": "high", "kind": "private_parser_policy_not_selected_for_proof_audit"})
if validation.get("manifest", {}).get("private_manifest", {}).get("status") != "loaded":
    findings.append({"severity": "high", "kind": "private_manifest_not_loaded"})
if not release_gated:
    findings.append({"severity": "high", "kind": "private_release_gated_entries_missing"})

status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "mismatch"
payload = {
    "status": status,
    "reason": "Private corpus manifest is configured and satisfies release-gate privacy checks." if status == "consistent" else "Private corpus manifest is not ready for the private-corpus release profile.",
    "private_paths_redacted": True,
    "manifest": validation.get("manifest", {}),
    "findings": findings,
    "parser_reports": parser_reports,
}
print(json.dumps(attach_contract(payload, "private_corpus_validation_report"), indent=2))
sys.exit(0 if status == "consistent" else 1)
PY
