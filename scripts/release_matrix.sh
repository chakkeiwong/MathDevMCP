#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/release_matrix.sh ROOT

Run the local MathDevMCP release profile matrix. Optional profiles are reported
as skipped unless their required environment flags are explicitly configured.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

ROOT="${1:-$(pwd)}"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

run_profile() {
  local profile="$1"
  python -m mathdevmcp.cli release-readiness --root "$ROOT" --profile "$profile"
}

echo '{"profile":"base","status":"running"}'
run_profile base

if [[ -n "${MATHDEVMCP_BACKEND_CONDA_ENV:-}" ]]; then
  echo '{"profile":"backend","status":"running"}'
  run_profile backend
else
  echo '{"profile":"backend","status":"skipped","reason":"MATHDEVMCP_BACKEND_CONDA_ENV is not set"}'
fi

if [[ "${MATHDEVMCP_REQUIRE_LATEXML:-0}" == "1" ]]; then
  echo '{"profile":"latexml","status":"running"}'
  run_profile latexml
else
  echo '{"profile":"latexml","status":"skipped","reason":"MATHDEVMCP_REQUIRE_LATEXML=1 is not set"}'
fi

if [[ -n "${MATHDEVMCP_PRIVATE_CORPUS_MANIFEST:-}" ]]; then
  echo '{"profile":"private-corpus","status":"running"}'
  run_profile private-corpus
else
  echo '{"profile":"private-corpus","status":"skipped","reason":"MATHDEVMCP_PRIVATE_CORPUS_MANIFEST is not set"}'
fi

if [[ "${MATHDEVMCP_RUN_FULL_PROFILE:-0}" == "1" ]]; then
  echo '{"profile":"full","status":"running"}'
  run_profile full
else
  echo '{"profile":"full","status":"skipped","reason":"MATHDEVMCP_RUN_FULL_PROFILE=1 is not set"}'
fi
