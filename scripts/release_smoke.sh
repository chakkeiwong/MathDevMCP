#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
export PYTHONPATH="$ROOT/src"

python -m mathdevmcp.cli doctor
python -m mathdevmcp.cli parser-benchmark --root "$ROOT/benchmarks/fixtures" --backend current
python -m mathdevmcp.cli benchmark-gate --root "$ROOT"
python -m mathdevmcp.cli validate-release-corpus --root "$ROOT/benchmarks/fixtures"
python -m mathdevmcp.cli governance-policy
python -m mathdevmcp.cli validate-governance --root "$ROOT"
python -m mathdevmcp.cli release-readiness --root "$ROOT"
