#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
OUT="${MATHDEVMCP_SECURITY_ARTIFACT:-$ROOT/.security-scan.json}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" - "$ROOT" "$OUT" <<'PY'
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()


def run_optional(name, args):
    path = shutil.which(name)
    if not path:
        return {"status": "not_available", "tool": name}
    result = subprocess.run(
        args,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return {
        "status": "passed" if result.returncode == 0 else "failed",
        "tool": name,
        "returncode": result.returncode,
        "stdout_digest": hashlib.sha256(result.stdout.encode()).hexdigest(),
    }


checks = {
    "pip_audit": run_optional("pip-audit", ["pip-audit"]),
    "secret_scan": run_optional("gitleaks", ["gitleaks", "detect", "--no-banner", "--source", str(root)]),
    "sbom": run_optional("syft", ["syft", str(root), "-o", "json"]),
}
report = {
    "schema_version": "mathdevmcp-security-scan@1",
    "scope": "engineering_supply_chain_only",
    "checks": checks,
    "claims": {
        "mathematical_correctness": "not_evaluated",
        "security_completeness": "not_claimed_when_tools_unavailable",
    },
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
failed = [item for item in checks.values() if item.get("status") == "failed"]
sys.exit(1 if failed else 0)
PY
