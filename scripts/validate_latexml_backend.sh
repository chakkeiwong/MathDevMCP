#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/validate_latexml_backend.sh ROOT

Validate the optional LaTeXML parser backend on a MathDevMCP checkout or
fixture root. The command honors MATHDEVMCP_LATEXML_PATH.

By default missing LaTeXML is reported as an optional caveat with exit code 0.
Set MATHDEVMCP_REQUIRE_LATEXML=1 to make missing or inconclusive LaTeXML a
strict failure.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

ROOT="${1:-$(pwd)}"
STRICT="${MATHDEVMCP_REQUIRE_LATEXML:-0}"

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

python - "$ROOT" "$STRICT" <<'PY'
import json
import sys
from pathlib import Path

from mathdevmcp.contracts import attach_contract
from mathdevmcp.doctor import doctor_report
from mathdevmcp.parser_benchmark import run_parser_backend

root = Path(sys.argv[1]).resolve()
strict = sys.argv[2].strip().lower() in {"1", "true", "yes", "on"}
fixture_root = root / "benchmarks" / "fixtures" if (root / "benchmarks" / "fixtures").exists() else root

doctor = doctor_report()
latexml = doctor["capabilities"].get("latexml", {})
if not latexml.get("available"):
    payload = {
        "status": "unavailable",
        "strict": strict,
        "reason": "LaTeXML is unavailable; this is an optional backend caveat unless strict mode is enabled.",
        "install_hint": "Install OS package latexml or set MATHDEVMCP_LATEXML_PATH=/path/to/latexml. Run scripts/setup_latexml_backend.sh for local instructions.",
        "doctor_capability": latexml,
        "parser_result": None,
    }
    print(json.dumps(attach_contract(payload, "latexml_backend_validation"), indent=2))
    sys.exit(1 if strict else 0)

parser_result = run_parser_backend(fixture_root, "latexml")
validated = parser_result["status"] == "parsed" and parser_result["quality_checks"]["label_preservation"]
payload = {
    "status": "validated" if validated else "inconclusive",
    "strict": strict,
    "reason": "LaTeXML preserved expected labels on the benchmark corpus." if validated else "LaTeXML ran but did not produce release-certifying parser evidence.",
    "install_hint": None,
    "doctor_capability": latexml,
    "parser_result": parser_result,
}
print(json.dumps(attach_contract(payload, "latexml_backend_validation"), indent=2))
sys.exit(0 if validated or not strict else 1)
PY
