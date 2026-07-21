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
  contracts)
    timeout "${MATHDEVMCP_CONTRACTS_TIMEOUT:-900}" python -m pytest -q \
      tests/test_contracts.py tests/test_high_level_contracts.py \
      tests/test_evidence_manifest.py tests/test_external_tool_adapters.py \
      tests/test_label_scoped_obligation.py
    ;;
  documents)
    timeout "${MATHDEVMCP_DOCUMENTS_TIMEOUT:-1200}" python -m pytest -q \
      tests/test_document_derivation_tree.py tests/test_document_derivation_response.py \
      tests/test_document_derivation_real_regressions.py tests/test_document_publication_quarantine.py
    ;;
  interfaces)
    timeout "${MATHDEVMCP_INTERFACES_TIMEOUT:-900}" python -m pytest -q \
      tests/test_cli_kalman_recursion.py tests/test_cli_typed_obligation.py \
      tests/test_mcp_facade.py tests/test_mcp_server.py \
      tests/test_mcp_surface_sync.py tests/test_mcp_stdio_transport.py tests/test_mcp_stdio_smoke.py
    ;;
  backends)
    timeout "${MATHDEVMCP_BACKENDS_TIMEOUT:-900}" python -m pytest -q \
      tests/test_backend_protocol.py tests/test_backend_env.py tests/test_doctor.py \
      tests/test_external_tool_adapters.py tests/test_sage_adapter.py tests/test_sympy_adapter.py
    ;;
  release)
    timeout "${MATHDEVMCP_RELEASE_TIMEOUT:-900}" python -m pytest -q \
      tests/test_release_artifacts.py tests/test_release_profile_analysis.py \
      tests/test_release_report_audit.py tests/test_public_release_check.py \
      tests/test_packaging_release_policy.py tests/test_handoff_documentation.py
    ;;
  coverage-core)
    timeout "${MATHDEVMCP_COVERAGE_TIMEOUT:-1200}" coverage run --branch -m pytest -q \
      tests/test_contracts.py tests/test_latex_index.py tests/test_mcp_facade.py \
      tests/test_document_derivation_tree.py tests/test_document_derivation_response.py \
      tests/test_evidence_manifest.py tests/test_release_caveat_closure.py \
      tests/test_release_profile_analysis.py
    coverage report
    ;;
  benchmarks)
    timeout "${MATHDEVMCP_BENCHMARKS_TIMEOUT:-1200}" python -m pytest -q \
      tests/test_context_and_fixtures.py tests/test_workbench_benchmark_schema.py \
      tests/test_real_local_high_level_benchmark.py
    ;;
  full)
    timeout "${MATHDEVMCP_FULL_TIMEOUT:-1800}" python -m pytest -q tests
    ;;
  collect-external)
    python -m pytest --collect-only -q -m requires_external_tool
    ;;
  *)
    echo "Usage: scripts/test_lanes.sh {fast|integration|contracts|documents|interfaces|backends|release|benchmarks|coverage-core|full|collect-external}" >&2
    exit 2
    ;;
esac
