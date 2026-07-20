#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:--1}"

# Wheel CI can set this to exercise installed artifacts without silently
# importing the checkout source tree.
if [[ "${MATHDEVMCP_USE_INSTALLED_PACKAGE:-0}" == "1" ]]; then
  unset PYTHONPATH
fi

python -m compileall -q "$ROOT/src" "$ROOT/tests"
"$ROOT/scripts/audit_release_report_substance.sh"
python -c 'from mathdevmcp.maintainability import maintainability_report; import pathlib, sys; report = maintainability_report(pathlib.Path(sys.argv[1])); print(report["reason"]); raise SystemExit(0 if report["status"] == "consistent" else 1)' "$ROOT"
python -m pytest -q \
  "$ROOT/tests/test_release_report_audit.py" \
  "$ROOT/tests/test_public_release_check.py" \
  "$ROOT/tests/test_packaging_release_policy.py" \
  "$ROOT/tests/test_mcp_facade.py" \
  "$ROOT/tests/test_mcp_server.py" \
  "$ROOT/tests/test_contracts.py" \
  "$ROOT/tests/test_maintainability.py" \
  "$ROOT/tests/test_handoff_documentation.py" \
  "$ROOT/tests/test_mcp_stdio_transport.py" \
  "$ROOT/tests/test_mcp_stdio_smoke.py"
python -m mathdevmcp.cli public-release-check --root "$ROOT"

echo "Maintainer fast check passed. This is not the complete regression suite."
