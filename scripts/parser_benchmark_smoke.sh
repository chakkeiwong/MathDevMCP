#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
export PYTHONPATH="$ROOT/src"

python -m mathdevmcp.cli parser-benchmark --root "$ROOT/benchmarks/fixtures" --backend current
