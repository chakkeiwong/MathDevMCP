#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:--1}"

lane="${1:-fast}"
case "$lane" in
  fast)
    timeout "${MATHDEVMCP_FAST_TIMEOUT:-300}" python -m pytest -q \
      tests/test_backend_protocol.py tests/test_release_artifacts.py \
      tests/test_release_profile_analysis.py tests/test_real_tasks_manifest.py \
      tests/test_mcp_surface_sync.py tests/test_mcp_stdio_transport.py \
      tests/test_mcp_stdio_smoke.py tests/test_doctor.py
    ;;
  integration)
    timeout "${MATHDEVMCP_INTEGRATION_TIMEOUT:-900}" python -m pytest -q \
      tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_public_release_check.py \
      tests/test_packaging_release_policy.py tests/test_direct_module_boundaries.py
    ;;
  full)
    timeout "${MATHDEVMCP_FULL_TIMEOUT:-1800}" python -m pytest -q tests
    ;;
  collect-external)
    python -m pytest --collect-only -q -m requires_external_tool
    ;;
  *)
    echo "Usage: scripts/test_lanes.sh {fast|integration|full|collect-external}" >&2
    exit 2
    ;;
esac
