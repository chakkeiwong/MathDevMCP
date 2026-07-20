#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:--1}"
if [[ -n "${MATHDEVMCP_HANDOFF_ARTIFACT_DIR:-}" ]]; then
  ARTIFACT_DIR="$MATHDEVMCP_HANDOFF_ARTIFACT_DIR"
else
  ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/mathdevmcp-handoff.XXXXXX")"
fi
mkdir -p "$ARTIFACT_DIR"
echo "Handoff evidence directory: $ARTIFACT_DIR"

"$ROOT/scripts/maintainer_check.sh"
set +e
MATHDEVMCP_FULL_TIMEOUT="${MATHDEVMCP_FULL_TIMEOUT:-1800}" bash "$ROOT/scripts/test_lanes.sh" full >"$ARTIFACT_DIR/full-lane.txt" 2>&1
FULL_STATUS=$?
set -e
if [[ "$FULL_STATUS" -ne 0 ]]; then
  echo "Department handoff blocked: full test lane failed or timed out (status $FULL_STATUS)." >&2
  tail -40 "$ARTIFACT_DIR/full-lane.txt" >&2 || true
  exit "$FULL_STATUS"
fi
"$ROOT/scripts/release_smoke.sh" "$ROOT"
MATHDEVMCP_SECURITY_SCAN_MODE=required MATHDEVMCP_SECURITY_ARTIFACT="$ARTIFACT_DIR/security.json" bash "$ROOT/scripts/security_scan.sh" "$ROOT"
REPORT=$(mktemp)
trap 'rm -f "$REPORT"' EXIT
python -m mathdevmcp.cli release-readiness --root "$ROOT" --profile base >"$REPORT" || true
cp "$REPORT" "$ARTIFACT_DIR/release-readiness.json"
python - "$REPORT" <<'PY'
import json
import sys

from mathdevmcp.release_policy import release_claim_ready

report = json.loads(open(sys.argv[1], encoding="utf-8").read())
if not release_claim_ready(report):
    print("Department handoff blocked: release claim is not ready.", file=sys.stderr)
    print(json.dumps({
        "status": report.get("status"),
        "dirty_worktree": report.get("dirty_worktree"),
        "blockers": report.get("blockers", []),
        "caveats": report.get("caveats", []),
    }, indent=2), file=sys.stderr)
    raise SystemExit(1)
PY

echo "Controlled internal maintainer handoff gate passed."
